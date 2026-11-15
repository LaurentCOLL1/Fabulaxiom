import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32FictionalHumanOrderBatchLab from "./M32FictionalHumanOrderBatchLab";
import { previewFictionalRepairPairImpact, type FictionalHumanOrderRepair,
} from "./m32FictionalHumanOrderBatch";
import { createFictionalPrecedence, startFictionalDraft, revokeFictionalPrecedence,
} from "./m32FictionalManualChronology";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";

const universe_id = "fiction-impact";
const time = (id: string, status: "current" | "revoked" = "current") =>
  ({ id, universe_id, status, time_kind: "unknown" as const, calendar_name: null,
    fictional_label: null, precision_text: null, source_revision_id: null });
function scenario(): M32ChronologyProjection {
  return { universe_id, reader_reveal_status: "not_authored",
    anchors: [time("A"),time("B"),time("C"),time("D"),time("historical","revoked")],
    precedences: [], narration: [] };
}
function draft() {
  const d = startFictionalDraft(scenario());
  return createFictionalPrecedence(createFictionalPrecedence(d,
    "A","B","Human A before B"),"B","C","Human B before C");
}
const revoke = (id = "fiction-draft-0002"): FictionalHumanOrderRepair =>
  ({ precedence_id:id, revoke_reason:"Human correction", replacement:null });
const replace = (before: string, after: string): FictionalHumanOrderRepair =>
  ({ precedence_id:"fiction-draft-0002", revoke_reason:"Correct this relation",
    replacement:{ before_anchor_id:before, after_anchor_id:after,
      reason:"Author explicitly declares new order" } });

describe("M3.2 P3ae read-only before/after impact for one selected fictional pair", () => {
  it("01 computes changed A/C relation after a witness is explicitly revoked", () => {
    const result=previewFictionalRepairPairImpact(draft(),[revoke()],"A","C");
    expect(result.before.relation).toBe("before");
    expect(result.before.witness.map(x=>x.precedence_id))
      .toEqual(["fiction-draft-0001","fiction-draft-0002"]);
    expect(result.after.relation).toBe("incomparable");
    expect(result.after.witness).toEqual([]);
    expect(result.relation_changed).toBe(true);
    expect(result.witness_changed).toBe(true);
    expect(result.preview_only).toBe(true);
    expect(result.can_write).toBe(false);
    expect(result.world_order_inferred).toBe(false);
  });
  it("02 reports an unaffected selected pair as unchanged", () => {
    const result=previewFictionalRepairPairImpact(draft(),[revoke()],"A","B");
    expect(result.before.relation).toBe("before");
    expect(result.after.relation).toBe("before");
    expect(result.relation_changed).toBe(false);
    expect(result.witness_changed).toBe(false);
  });
  it("03 reports a newly established human witness after replacement", () => {
    const result=previewFictionalRepairPairImpact(draft(),[replace("B","D")],"A","D");
    expect(result.before.relation).toBe("incomparable");
    expect(result.after.relation).toBe("before");
    expect(result.after.witness.map(x=>x.precedence_id))
      .toEqual(["fiction-draft-0001","fiction-draft-0003"]);
    expect(result.relation_changed).toBe(true);
  });
  it("04 distinguishes unchanged relation from changed human proof", () => {
    const result=previewFictionalRepairPairImpact(draft(),[replace("B","C")],"A","C");
    expect(result.before.relation).toBe("before");
    expect(result.after.relation).toBe("before");
    expect(result.relation_changed).toBe(false);
    expect(result.witness_changed).toBe(true);
    expect(result.after.witness[1].precedence_id).toBe("fiction-draft-0003");
  });
  it("05 reverses the user-selected comparison consistently", () => {
    const result=previewFictionalRepairPairImpact(draft(),[revoke()],"C","A");
    expect(result.before.relation).toBe("after");
    expect(result.after.relation).toBe("incomparable");
  });
  it("06 rejects historical and unrecognized selected anchor IDs", () => {
    for (const id of ["historical","missing","foreign:A"]) {
      expect(()=>previewFictionalRepairPairImpact(draft(),[revoke()],"A",id)).toThrow();
    }
  });
  it("07 rejects malformed Unicode scalar IDs before showing a pair", () => {
    expect(()=>previewFictionalRepairPairImpact(draft(),[revoke()],"A","\uD800")).toThrow();
    expect(()=>previewFictionalRepairPairImpact(draft(),[revoke()],"A","")).toThrow();
  });
  it("08 rejects a globally cyclic replacement even for an unrelated selected pair", () => {
    expect(()=>previewFictionalRepairPairImpact(draft(),[replace("C","B")],"A","A"))
      .toThrow(/cycle/);
  });
  it("09 never mutates the original fictional draft on successful or refused preview", () => {
    const d=draft(), original=JSON.stringify(d);
    previewFictionalRepairPairImpact(d,[revoke()],"A","C");
    expect(JSON.stringify(d)).toBe(original);
    expect(()=>previewFictionalRepairPairImpact(d,[replace("C","B")],"A","C"))
      .toThrow();
    expect(JSON.stringify(d)).toBe(original);
  });
  it("10 refuses a non-fictional origin and stale already-historical relation", () => {
    const d=draft();
    expect(()=>previewFictionalRepairPairImpact(
      {...d,data_origin:"operator_sqlite"} as unknown as typeof d,[revoke()],"A","B"))
      .toThrow();
    const changed=revokeFictionalPrecedence(d,"fiction-draft-0002","Already revoked");
    expect(()=>previewFictionalRepairPairImpact(changed,[revoke()],"A","B")).toThrow();
  });
  it("11 avoids projecting any novel narration or reader reveal inference", () => {
    const result=previewFictionalRepairPairImpact(draft(),[revoke()],"A","C");
    expect(result.before.data_origin).toBe("synthetic_in_memory_only");
    expect(result.after.edit_controls_available).toBe(false);
    expect(result.world_order_inferred).toBe(false);
    expect(result).not.toHaveProperty("reader_order");
    expect(result).not.toHaveProperty("novel_time");
  });
  it("12 handles exact same-identity pair without inventing a chain", () => {
    const result=previewFictionalRepairPairImpact(draft(),[revoke()],"A","A");
    expect(result.before.relation).toBe("same");
    expect(result.after.relation).toBe("same");
    expect(result.before.witness).toEqual([]);
    expect(result.after.witness).toEqual([]);
  });
  it("13 exposes two optional selection controls but no false persistence success", () => {
    const html=renderToStaticMarkup(createElement(M32FictionalHumanOrderBatchLab,
      {initial:scenario(),revisions:[]}));
    expect(html).toContain("Comparaison ciblée facultative avant/après");
    expect(html).toContain("Première ancre à comparer");
    expect(html).toContain("Seconde ancre à comparer");
    expect(html).not.toContain("Sauvegarde réussie");
  });
  it("14 escapes suspicious fictional source anchor labels in the UI", () => {
    const x=scenario();
    const html=renderToStaticMarkup(createElement(M32FictionalHumanOrderBatchLab,
      {initial:{...x,anchors:x.anchors.map((a,i)=>i===0?
        {...a,id:"<script>unsafe()</script>"}:a)},revisions:[]}));
    expect(html).not.toContain("<script>");
    expect(html).toContain("&lt;script&gt;");
  });
});
