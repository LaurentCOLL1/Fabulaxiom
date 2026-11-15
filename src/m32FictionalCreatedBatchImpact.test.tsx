import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32FictionalHumanOrderBatchLab from "./M32FictionalHumanOrderBatchLab";
import { previewFictionalCreatedBatchSelectedPairs, type FictionalRepairSelectedPair,
 type FictionalHumanOrder } from "./m32FictionalHumanOrderBatch";
import { startFictionalDraft, createFictionalPrecedence } from "./m32FictionalManualChronology";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
const universe_id="fiction-batch-impact";
const anchor=(id:string,status:"current"|"revoked"="current")=>({id,universe_id,status,
 time_kind:"unknown" as const,calendar_name:null,fictional_label:null,
 precision_text:null,source_revision_id:null});
const scene=():M32ChronologyProjection=>({universe_id,reader_reveal_status:"not_authored",
 anchors:[anchor("A"),anchor("B"),anchor("C"),anchor("D"),anchor("old","revoked")],
 precedences:[],narration:[]});
const draft=()=>createFictionalPrecedence(startFictionalDraft(scene()),"A","B","Author A-B");
const add=(before_anchor_id:string,after_anchor_id:string):FictionalHumanOrder=>({
 before_anchor_id,after_anchor_id,reason:"Explicit author relation"});
const pair=(left_anchor_id:string,right_anchor_id:string):FictionalRepairSelectedPair=>({
 left_anchor_id,right_anchor_id});
describe("P3ah selective before-after for newly staged fictional batch",()=>{
 it("01 reports a new A-C path through staged B-C",()=>{
  const p=previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],[pair("A","C")]);
  expect(p.selected_pairs[0].before.relation).toBe("incomparable");
  expect(p.selected_pairs[0].after.relation).toBe("before");
  expect(p.selected_pairs[0].after.witness.map(x=>x.precedence_id))
   .toEqual(["fiction-draft-0001","fiction-draft-0002"]);
  expect(p.changed_relation_count).toBe(1);
  expect(p.changed_witness_count).toBe(1);
  expect(p.can_write).toBe(false);expect(p.world_order_inferred).toBe(false);
 });
 it("02 retains independent unchanged pair after proposal",()=>{
  const p=previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],
   [pair("A","C"),pair("A","B"),pair("D","C")]);
  expect(p.selected_pairs.map(x=>x.relation_changed)).toEqual([true,false,false]);
  expect(p.changed_relation_count).toBe(1);
 });
 it("03 reverses a selected direction, not the authored precedence",()=>{
  const p=previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],[pair("C","A")]);
  expect(p.selected_pairs[0].after.relation).toBe("after");
 });
 it("04 refuses repeated selections including reversed duplicate",()=>{
  for(const pairs of [[pair("A","C"),pair("A","C")],[pair("A","C"),pair("C","A")]])
   expect(()=>previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],pairs)).toThrow();
 });
 it("05 refuses zero selections, >8 and extra writable fields",()=>{
  expect(()=>previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],[])).toThrow();
  expect(()=>previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],
   Array.from({length:9},(_,i)=>pair("A",String(i))))).toThrow();
  expect(()=>previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],
   [{...pair("A","C"),save:true} as unknown as FictionalRepairSelectedPair])).toThrow();
 });
 it("06 rejects historical or foreign selected anchors",()=>{
  for(const id of ["old","missing","foreign:A"])
   expect(()=>previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],[pair("A",id)])).toThrow();
 });
 it("07 rejects malformed unicode scalar and blank IDs",()=>{
  for(const id of ["\uD800","", "x".repeat(257)])
   expect(()=>previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],[pair("A",id)])).toThrow();
 });
 it("08 refuses a cycle even for a selected pair outside the cycle",()=>{
  expect(()=>previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","A")],
   [pair("C","D")])).toThrow(/cycle/);
 });
 it("09 rejects data claiming to originate from operator SQLite",()=>{
  const bad={...draft(),data_origin:"operator_sqlite"};
  expect(()=>previewFictionalCreatedBatchSelectedPairs(bad as ReturnType<typeof draft>,
   [add("B","C")],[pair("A","C")])).toThrow();
 });
 it("10 preserves source bytes on valid or rejected batch",()=>{
  const initial=draft(),bytes=JSON.stringify(initial);
  previewFictionalCreatedBatchSelectedPairs(initial,[add("B","C")],[pair("A","C")]);
  expect(JSON.stringify(initial)).toBe(bytes);
  expect(()=>previewFictionalCreatedBatchSelectedPairs(initial,[add("B","A")],
   [pair("A","B")])).toThrow();
  expect(JSON.stringify(initial)).toBe(bytes);
 });
 it("11 exposes no story/reveal inference nor writable controls",()=>{
  const p=previewFictionalCreatedBatchSelectedPairs(draft(),[add("B","C")],[pair("A","C")]);
  expect(p.selected_pairs[0].before.data_origin).toBe("synthetic_in_memory_only");
  expect(p.selected_pairs[0].after.edit_controls_available).toBe(false);
  expect(p).not.toHaveProperty("reader_order");
  expect(p).not.toHaveProperty("novel_time");
 });
 it("12 shows explicit batch pair selectors but no fake persistence",()=>{
  const html=renderToStaticMarkup(createElement(M32FictionalHumanOrderBatchLab,
   {initial:scene(),revisions:[]}));
  expect(html).toContain("Ajouter cette paire au lot de créations fictives");
  expect(html).toContain("Paires du lot choisies");
  expect(html).not.toContain("Sauvegarde réussie");
 });
});
