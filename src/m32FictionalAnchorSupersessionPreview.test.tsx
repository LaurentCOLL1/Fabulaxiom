import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { previewFictionalAnchorSupersession, confirmFictionalAnchorSupersession } from "./m32FictionalAnchorSupersessionPreview";
import { startFictionalDraft, createFictionalAnchor, createFictionalPrecedence } from "./m32FictionalManualChronology";
import type { FictionalTimeInput } from "./m32FictionalManualChronology";
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
 it("13 renders a deliberate review then confirmation entry point, no direct write",()=>{
   const html=renderToStaticMarkup(createElement(M32ManualChronologyLab,{initial:scene(),revisions:[]}));
   expect(html).toContain("Prévisualiser la correction sans l&#x27;appliquer");
   expect(html).not.toContain("Remplacer sans effacer l&#x27;historique");
   expect(html).not.toContain("Sauvegarde réussie");
 });
});
