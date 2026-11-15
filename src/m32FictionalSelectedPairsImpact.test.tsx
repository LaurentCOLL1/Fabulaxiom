import {createElement} from "react";
import {renderToStaticMarkup} from "react-dom/server";
import {describe,expect,it} from "vitest";
import M32FictionalHumanOrderBatchLab from "./M32FictionalHumanOrderBatchLab";
import {previewFictionalRepairSelectedPairs,type FictionalRepairSelectedPair,
  type FictionalHumanOrderRepair} from "./m32FictionalHumanOrderBatch";
import {startFictionalDraft,createFictionalPrecedence} from "./m32FictionalManualChronology";
import type {M32ChronologyProjection} from "./M32ChronologyPreview";
const universe_id="fiction-selected-pairs";
const anchor=(id:string,status:"current"|"revoked"="current")=>({id,universe_id,status,time_kind:"unknown" as const,calendar_name:null,fictional_label:null,precision_text:null,source_revision_id:null});
const scenario=():M32ChronologyProjection=>({universe_id,reader_reveal_status:"not_authored",anchors:[anchor("A"),anchor("B"),anchor("C"),anchor("D"),anchor("old","revoked")],precedences:[],narration:[]});
const draft=()=>createFictionalPrecedence(createFictionalPrecedence(startFictionalDraft(scenario()),"A","B","Human A-B"),"B","C","Human B-C");
const revoke=():FictionalHumanOrderRepair=>({precedence_id:"fiction-draft-0002",revoke_reason:"Human revocation",replacement:null});
const replace=(left:string,right:string):FictionalHumanOrderRepair=>({precedence_id:"fiction-draft-0002",revoke_reason:"Human correction",replacement:{before_anchor_id:left,after_anchor_id:right,reason:"Human replacement"}});
const pair=(left_anchor_id:string,right_anchor_id:string):FictionalRepairSelectedPair=>({left_anchor_id,right_anchor_id});
describe("M3.2 P3af up to eight explicitly chosen fictional relation pairs",()=>{
it("01 classifies changed and unaffected pairs without total chronology",()=>{
 const p=previewFictionalRepairSelectedPairs(draft(),[revoke()],[pair("A","C"),pair("A","B")]);
 expect(p.selected_pairs.map(x=>[x.before.relation,x.after.relation])).toEqual([["before","incomparable"],["before","before"]]);
 expect(p.changed_relation_count).toBe(1);expect(p.changed_witness_count).toBe(1);
 expect(p.preview_only).toBe(true);expect(p.can_write).toBe(false);expect(p.world_order_inferred).toBe(false);
});
it("02 keeps relation but reports changed witness after replacement",()=>{
 const p=previewFictionalRepairSelectedPairs(draft(),[replace("B","C")],[pair("A","C")]);
 expect(p.changed_relation_count).toBe(0);expect(p.changed_witness_count).toBe(1);
 expect(p.selected_pairs[0].after.witness[1].precedence_id).toBe("fiction-draft-0003");
});
it("03 preserves selection order and reverse relation",()=>{
 const p=previewFictionalRepairSelectedPairs(draft(),[revoke()],[pair("C","A"),pair("A","B"),pair("D","C")]);
 expect(p.selected_pairs.map(x=>x.left_anchor_id)).toEqual(["C","A","D"]);
 expect(p.selected_pairs[0].before.relation).toBe("after");
});
it("04 refuses duplicate and reverse duplicate",()=>{
 for(const rows of [[pair("A","B"),pair("A","B")],[pair("A","B"),pair("B","A")]])
 expect(()=>previewFictionalRepairSelectedPairs(draft(),[revoke()],rows)).toThrow();
});
it("05 refuses empty or nine selections and forged fields",()=>{
 expect(()=>previewFictionalRepairSelectedPairs(draft(),[revoke()],[])).toThrow();
 expect(()=>previewFictionalRepairSelectedPairs(draft(),[revoke()],Array.from({length:9},(_,i)=>pair("A",String(i))))).toThrow();
 expect(()=>previewFictionalRepairSelectedPairs(draft(),[revoke()],
  [{...pair("A","B"),write_to_disk:true} as unknown as FictionalRepairSelectedPair])).toThrow();
});
it("06 refuses unknown, revoked and foreign IDs",()=>{
 for(const id of ["missing","old","foreign:A"])
 expect(()=>previewFictionalRepairSelectedPairs(draft(),[revoke()],[pair("A",id)])).toThrow();
});
it("07 refuses malformed unicode, blank and too-long scalar IDs",()=>{
 for(const id of ["\uD800","", "x".repeat(257)])
 expect(()=>previewFictionalRepairSelectedPairs(draft(),[revoke()],[pair("A",id)])).toThrow();
});
it("08 rejects a global cycle outside selected pair",()=>{
 expect(()=>previewFictionalRepairSelectedPairs(draft(),[replace("B","A")],[pair("C","D")])).toThrow(/cycle/);
});
it("09 refuses non-fictional origin",()=>{
 const d={...draft(),data_origin:"operator_sqlite"};
 expect(()=>previewFictionalRepairSelectedPairs(d as ReturnType<typeof draft>,[revoke()],[pair("A","C")])).toThrow();
});
it("10 preserves source draft even after rejected proposal",()=>{
 const d=draft(),before=JSON.stringify(d);
 previewFictionalRepairSelectedPairs(d,[revoke()],[pair("A","C")]);
 expect(JSON.stringify(d)).toBe(before);
 expect(()=>previewFictionalRepairSelectedPairs(d,[replace("B","A")],[pair("C","D")])).toThrow();
 expect(JSON.stringify(d)).toBe(before);
});
it("11 restricts each witness to synthetic read-only data",()=>{
 const p=previewFictionalRepairSelectedPairs(draft(),[revoke()],[pair("A","C")]);
 expect(p.selected_pairs[0].before.data_origin).toBe("synthetic_in_memory_only");
 expect(p.selected_pairs[0].after.edit_controls_available).toBe(false);
 expect(p).not.toHaveProperty("reader_order");
});
it("12 renders optional selection and no fake save",()=>{
 const html=renderToStaticMarkup(createElement(M32FictionalHumanOrderBatchLab,{initial:scenario(),revisions:[]}));
 expect(html).toContain("Ajouter cette paire aux comparaisons explicites");
 expect(html).toContain("Paires choisies par l&#x27;auteur");
 expect(html).not.toContain("Sauvegarde réussie");
});
});
