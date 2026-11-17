import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { previewFictionalAnchorSupersession, confirmFictionalAnchorSupersession } from "./m32FictionalAnchorSupersessionPreview";
import { startFictionalDraft, createFictionalAnchor, createFictionalPrecedence } from "./m32FictionalManualChronology";
import type { FictionalTimeInput, FictionalRevision } from "./m32FictionalManualChronology";
import type { M32ChronologyProjection, M32TimeKind } from "./M32ChronologyPreview";
import M32ManualChronologyLab from "./M32ManualChronologyLab";

const universe_id="fiction-supersession-review";
const anchor=(id:string,time_kind:M32TimeKind,calendar_name:string|null=null,
 fictional_label:string|null=null,precision_text:string|null=null)=>({
 id,universe_id,time_kind,status:"current" as const,calendar_name,fictional_label,
 precision_text,source_revision_id:null
});
const scene=():M32ChronologyProjection=>({universe_id,reader_reveal_status:"not_authored",
 anchors:[anchor("A","exact","Lunes","Cycle XII"),anchor("B","unknown"),
  anchor("C","approximate","Marées",null,"trois marées"),anchor("D","relative")],
 precedences:[],narration:[]});
const draft=()=>startFictionalDraft(scene());
const sourced=()=>{
 const baseline=scene();
 const revisions: FictionalRevision[]=[
  {universe_id,novel_id:"novel-a",scene_id:"scene-a",revision_id:"rev-a",revision_label:"A initiale"},
  {universe_id,novel_id:"novel-b",scene_id:"scene-b",revision_id:"rev-b",revision_label:"B révisée"},
 ];
 const narration=revisions.map((r,index)=>({
  universe_id,novel_id:r.novel_id,scene_id:r.scene_id,
  novel_title:index===0?"Roman A":"Roman B",chapter_id:"chapter-"+String(index+1),
  chapter_title:"Chapitre inventé",chapter_order:1,scene_order:1,
  scene_title:"Scène inventée "+String(index+1),
 }));
 return startFictionalDraft({
  ...baseline,
  anchors:baseline.anchors.map(a=>a.id==="A"?{...a,source_revision_id:"rev-a"}:a),
  narration,
 },revisions);
};

const input=(kind:M32TimeKind,calendar="",label="",precision=""):FictionalTimeInput=>({
 kind,calendar,label,precision
});
describe("P3aj fiction-only dated supersession review and confirmation",()=>{
 it("01 previews exact-to-approximate while retaining historical anchor",()=>{
   const d=draft(),p=previewFictionalAnchorSupersession(d,"A",input("approximate","Marées","","deux tours"));
   expect(p.old_anchor.time_kind).toBe("exact");
   expect(p.new_anchor.time_kind).toBe("approximate");
   expect(p.new_anchor.calendar_name).toBe("Marées");
   expect(p.new_anchor.precision_text).toBe("deux tours");
   expect(p.candidate.snapshot.anchors.find(x=>x.id==="A")?.status).toBe("superseded");
   expect(p.can_write).toBe(false);expect(p.total_world_order_inferred).toBe(false);
 });
 it("02 unknown-to-exact requires the author's calendar and label",()=>{
   const p=previewFictionalAnchorSupersession(draft(),"B",input("exact","Lunes","jour 7"));
   expect(p.new_anchor.fictional_label).toBe("jour 7");
   expect(p.new_anchor.source_revision_id).toBeNull();
 });
 it("03 relative-to-unknown clears any unsupported calendar",()=>{
   const p=previewFictionalAnchorSupersession(draft(),"D",input("unknown","inutilisé","inutilisé"));
   expect(p.new_anchor.time_kind).toBe("unknown");
   expect(p.new_anchor.calendar_name).toBeNull();
   expect(p.new_anchor.fictional_label).toBeNull();
 });
 it("04 approximate-to-relative does not convert a fictional date",()=>{
   const p=previewFictionalAnchorSupersession(draft(),"C",input("relative","Marées","","précision"));
   expect(p.new_anchor.calendar_name).toBeNull();
   expect(p.new_anchor.precision_text).toBeNull();
 });
 it("05 refuses missing exact calendar and approximate precision",()=>{
   expect(()=>previewFictionalAnchorSupersession(draft(),"A",input("exact","","Cycle"))).toThrow();
   expect(()=>previewFictionalAnchorSupersession(draft(),"A",input("approximate","Marées"))).toThrow();
 });
 it("06 refuses already superseded or absent anchor",()=>{
   const p=previewFictionalAnchorSupersession(draft(),"A",input("unknown"));
   expect(()=>previewFictionalAnchorSupersession(p.candidate,"A",input("unknown"))).toThrow();
   expect(()=>previewFictionalAnchorSupersession(draft(),"missing",input("unknown"))).toThrow();
 });
 it("07 refuses correcting an anchor referenced by a current edge",()=>{
   const d=createFictionalPrecedence(draft(),"A","B","A avant B");
   expect(()=>previewFictionalAnchorSupersession(d,"A",input("unknown"))).toThrow(/révoquer/);
 });
 it("08 refuses unknown or operator-origin drafts",()=>{
   const d={...draft(),data_origin:"operator_sqlite"};
   expect(()=>previewFictionalAnchorSupersession(
     d as ReturnType<typeof draft>,"A",input("unknown"))).toThrow();
 });
 it("09 requires explicit confirmation",()=>{
   const d=draft(),i=input("unknown"),p=previewFictionalAnchorSupersession(d,"A",i);
   expect(()=>confirmFictionalAnchorSupersession(d,"A",i,p,false)).toThrow();
   const after=confirmFictionalAnchorSupersession(d,"A",i,p,true);
   expect(after.snapshot.anchors.find(a=>a.id==="A")?.status).toBe("superseded");
   expect(after.snapshot.anchors.length).toBe(5);
 });
 it("10 refuses forged preview output",()=>{
   const d=draft(),i=input("unknown"),p=previewFictionalAnchorSupersession(d,"A",i);
   expect(()=>confirmFictionalAnchorSupersession(d,"A",i,
     {...p,can_write:true} as unknown as typeof p,true)).toThrow();
   expect(()=>confirmFictionalAnchorSupersession(d,"A",i,
     {...p,new_anchor:{...p.new_anchor,id:"forged"}} ,true)).toThrow();
 });
 it("11 refuses stale preview after other human action",()=>{
   const d=draft(),i=input("unknown"),p=previewFictionalAnchorSupersession(d,"A",i);
   const changed=createFictionalAnchor(d,input("unknown"));
   expect(()=>confirmFictionalAnchorSupersession(changed,"A",i,p,true)).toThrow();
 });
 it("12 never mutates the baseline on valid or refused preview",()=>{
   const d=draft(),bytes=JSON.stringify(d);
   previewFictionalAnchorSupersession(d,"A",input("relative"));
   expect(JSON.stringify(d)).toBe(bytes);
   expect(()=>previewFictionalAnchorSupersession(d,"A",input("exact"))).toThrow();
   expect(JSON.stringify(d)).toBe(bytes);
 });
 it("14 keeps exact immutable source when author corrects a date without changing source",()=>{
   const d=sourced(),i=input("approximate","Marées","","deux marées");
   const p=previewFictionalAnchorSupersession(d,"A",i);
   expect(p.old_anchor.source_revision_id).toBe("rev-a");
   expect(p.new_anchor.source_revision_id).toBe("rev-a");
   const after=confirmFictionalAnchorSupersession(d,"A",i,p,true);
   expect(after.snapshot.anchors.find(a=>a.id==="A")?.source_revision_id).toBe("rev-a");
   expect(after.snapshot.anchors.find(a=>a.id===p.new_anchor.id)?.source_revision_id).toBe("rev-a");
   expect(d.snapshot.anchors.find(a=>a.id==="A")?.status).toBe("current");
 });
 it("15 changes source explicitly across fictional novels and preserves original historical provenance",()=>{
   const d=sourced(),i={...input("relative"),source_scene_id:"scene-b",source_revision_id:"rev-b"};
   const p=previewFictionalAnchorSupersession(d,"A",i);
   expect(p.old_anchor.source_revision_id).toBe("rev-a");
   expect(p.new_anchor.source_revision_id).toBe("rev-b");
   const after=confirmFictionalAnchorSupersession(d,"A",i,p,true);
   expect(after.snapshot.anchors.find(a=>a.id==="A")?.source_revision_id).toBe("rev-a");
   expect(after.snapshot.anchors.find(a=>a.id==="A")?.status).toBe("superseded");
   expect(after.snapshot.anchors.find(a=>a.id===p.new_anchor.id)?.source_revision_id).toBe("rev-b");
   expect(after.snapshot.precedences).toHaveLength(0);
 });
 it("16 refuses a revision ID paired with the wrong scene ID",()=>{
   const d=sourced();
   expect(()=>previewFictionalAnchorSupersession(d,"A",
     {...input("relative"),source_scene_id:"scene-a",source_revision_id:"rev-b"})).toThrow();
   expect(d.audit).toHaveLength(0);
 });
 it("17 refuses a nonexistent or foreign historical revision",()=>{
   const d=sourced();
   expect(()=>previewFictionalAnchorSupersession(d,"A",
     {...input("relative"),source_scene_id:"scene-b",source_revision_id:"rev-foreign"})).toThrow();
   expect(d.snapshot.anchors.find(a=>a.id==="A")?.source_revision_id).toBe("rev-a");
 });
 it("18 refuses confirmation after a different source revision was selected",()=>{
   const d=sourced(),first={...input("relative"),source_scene_id:"scene-b",source_revision_id:"rev-b"};
   const reviewed=previewFictionalAnchorSupersession(d,"A",first);
   const changed={...input("relative"),source_scene_id:"scene-a",source_revision_id:"rev-a"};
   expect(()=>confirmFictionalAnchorSupersession(d,"A",changed,reviewed,true)).toThrow();
   expect(d.snapshot.anchors.find(a=>a.id==="A")?.status).toBe("current");
 });
 it("19 requires deliberate null source to detach new version without erasing the old source",()=>{
   const d=sourced(),i={...input("unknown"),source_scene_id:null,source_revision_id:null};
   const reviewed=previewFictionalAnchorSupersession(d,"A",i);
   const after=confirmFictionalAnchorSupersession(d,"A",i,reviewed,true);
   expect(after.snapshot.anchors.find(a=>a.id==="A")?.source_revision_id).toBe("rev-a");
   expect(after.snapshot.anchors.find(a=>a.id===reviewed.new_anchor.id)?.source_revision_id).toBeNull();
 });
 it("20 displays explicit old and new fictional novel and scene identities",()=>{
   const d=sourced(),i={...input("relative"),source_scene_id:"scene-b",source_revision_id:"rev-b"};
   const p=previewFictionalAnchorSupersession(d,"A",i);
   expect(p.old_source).toMatchObject({universe_id,novel_id:"novel-a",scene_id:"scene-a",revision_id:"rev-a"});
   expect(p.new_source).toMatchObject({universe_id,novel_id:"novel-b",scene_id:"scene-b",revision_id:"rev-b"});
   expect(p.old_anchor.source_revision_id).toBe("rev-a");
   expect(p.new_anchor.source_revision_id).toBe("rev-b");
   expect(p.can_write).toBe(false);
 });
 it("21 retains same fictional source identity when only authored date changes",()=>{
   const p=previewFictionalAnchorSupersession(sourced(),"A",input("unknown"));
   expect(p.old_source).toMatchObject({novel_id:"novel-a",scene_id:"scene-a"});
   expect(p.new_source).toEqual(p.old_source);
   expect(p.old_source).not.toBe(p.new_source);
 });
 it("22 explicitly removing source leaves historical identity intact",()=>{
   const i={...input("relative"),source_scene_id:null,source_revision_id:null};
   const p=previewFictionalAnchorSupersession(sourced(),"A",i);
   expect(p.old_source?.revision_id).toBe("rev-a");
   expect(p.new_source).toBeNull();
 });
 it("23 source-free anchors do not fabricate novel or scene identity",()=>{
   const p=previewFictionalAnchorSupersession(draft(),"B",input("relative"));
   expect(p.old_source).toBeNull();
   expect(p.new_source).toBeNull();
 });
 it("24 confirmation rejects fabricated novel or scene in reviewed provenance",()=>{
   const d=sourced(),i={...input("relative"),source_scene_id:"scene-b",source_revision_id:"rev-b"};
   const p=previewFictionalAnchorSupersession(d,"A",i);
   const forged={...p,new_source:{...p.new_source!,novel_id:"novel-foreign",scene_id:"scene-foreign"}};
   expect(()=>confirmFictionalAnchorSupersession(d,"A",i,forged,true)).toThrow();
   expect(d.snapshot.anchors.find(a=>a.id==="A")?.status).toBe("current");
 });
 it("25 renders an explicit source-detachment control without persistence",()=>{
   const html=renderToStaticMarkup(createElement(M32ManualChronologyLab,
     {initial:scene(),revisions:[]}));
   expect(html).toContain("Détacher explicitement la source historique");
   expect(html).toContain("Ce choix ne modifie pas l&#x27;ancre historique");
   expect(html).not.toContain("Sauvegarde réussie");
 });
 it("26 explains exclusive fictional source choice without hidden save",()=>{
   const html=renderToStaticMarkup(createElement(M32ManualChronologyLab,
     {initial:scene(),revisions:[]}));
   expect(html).toContain("sélection de scène/révision proposée");
   expect(html).toContain("annule");
   expect(html).toContain("Détacher explicitement la source historique");
   expect(html).not.toContain("Sauvegarde réussie");
 });

 it("27 preserves explicit immutable fictional provenance",()=>{
   const p=previewFictionalAnchorSupersession(sourced(),"A",input("unknown"));
   expect(p.source_transition).toBe("retained");
   expect(p.new_source?.revision_id).toBe("rev-a");
 });
 it("28 reports cross-novel fictional source replacement",()=>{
   const p=previewFictionalAnchorSupersession(sourced(),"A",
     {...input("relative"),source_scene_id:"scene-b",source_revision_id:"rev-b"});
   expect(p.source_transition).toBe("replaced");
   expect(p.old_source?.novel_id).toBe("novel-a");
   expect(p.new_source?.novel_id).toBe("novel-b");
 });
 it("29 reports deliberate source detachment and retained historical evidence",()=>{
   const p=previewFictionalAnchorSupersession(sourced(),"A",
     {...input("unknown"),source_scene_id:null,source_revision_id:null});
   expect(p.source_transition).toBe("detached");
   expect(p.old_source?.revision_id).toBe("rev-a");
   expect(p.new_source).toBeNull();
 });
 it("30 reports linking a source to a previously unsourced anchor",()=>{
   const p=previewFictionalAnchorSupersession(sourced(),"B",
     {...input("relative"),source_scene_id:"scene-b",source_revision_id:"rev-b"});
   expect(p.source_transition).toBe("linked");
   expect(p.old_source).toBeNull();
 });
 it("31 refuses to invent source identity on two source-free versions",()=>{
   const p=previewFictionalAnchorSupersession(sourced(),"B",input("relative"));
   expect(p.source_transition).toBe("none");
   expect(p.old_source).toBeNull();
   expect(p.new_source).toBeNull();
 });
 it("32 rejects forged source-transition decision at RAM confirmation",()=>{
   const d=sourced(),i=input("unknown");
   const p=previewFictionalAnchorSupersession(d,"A",i);
   expect(()=>confirmFictionalAnchorSupersession(d,"A",i,
     {...p,source_transition:"detached"},true)).toThrow();
   expect(d.snapshot.anchors.find(a=>a.id==="A")?.status).toBe("current");
 });
 it("13 renders a deliberate review then confirmation entry point, no direct write",()=>{
   const html=renderToStaticMarkup(createElement(M32ManualChronologyLab,{initial:scene(),revisions:[]}));
   expect(html).toContain("Prévisualiser la correction sans l&#x27;appliquer");
   expect(html).not.toContain("Remplacer sans effacer l&#x27;historique");
   expect(html).not.toContain("Sauvegarde réussie");
 });
});
