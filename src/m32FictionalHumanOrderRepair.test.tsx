import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32FictionalHumanOrderBatchLab from "./M32FictionalHumanOrderBatchLab";
import { previewFictionalHumanOrderRepair, confirmFictionalHumanOrderRepair,
  type FictionalHumanOrderRepair } from "./m32FictionalHumanOrderBatch";
import { startFictionalDraft, createFictionalPrecedence, revokeFictionalPrecedence } from "./m32FictionalManualChronology";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";

const universe_id = "fiction-repair";
function scenario(): M32ChronologyProjection {
  const anchor = (id: string, status: "current" | "revoked" = "current") => ({
    id, universe_id, status, time_kind: "unknown" as const, calendar_name: null,
    fictional_label: null, precision_text: null, source_revision_id: null,
  });
  return { universe_id, reader_reveal_status: "not_authored",
    anchors: [anchor("A"),anchor("B"),anchor("C"),anchor("D"),anchor("retired","revoked")],
    precedences: [], narration: [] };
}
function draft() {
  return createFictionalPrecedence(
    createFictionalPrecedence(startFictionalDraft(scenario()), "A","B","Human first"),
    "B","C","Human second");
}
const revoke = (id: string): FictionalHumanOrderRepair =>
  ({ precedence_id: id, revoke_reason: "Human revocation", replacement: null });
const replace = (id: string, before = "A", after = "D"): FictionalHumanOrderRepair =>
  ({ precedence_id: id, revoke_reason: "Human correction",
     replacement: { before_anchor_id: before, after_anchor_id: after, reason: "Explicit replacement" } });

describe("M3.2 P3ad fictional reversible precedence correction batch", () => {
  it("01 previews a revocation without touching baseline or authorizing writes", () => {
    const d = draft(), old = JSON.stringify(d);
    const p = previewFictionalHumanOrderRepair(d, [revoke("fiction-draft-0001")]);
    expect(JSON.stringify(d)).toBe(old);
    expect(p.preview_only).toBe(true); expect(p.can_write).toBe(false);
    expect(p.world_order_inferred).toBe(false);
    expect(p.revoked_edge_ids).toEqual(["fiction-draft-0001"]);
    expect(p.candidate.snapshot.precedences.map(e => e.status)).toEqual(["revoked","current"]);
  });
  it("02 rejects missing explicit human confirmation", () => {
    const d = draft(), actions = [revoke("fiction-draft-0001")];
    expect(() => confirmFictionalHumanOrderRepair(d, actions,
      previewFictionalHumanOrderRepair(d,actions),false)).toThrow();
  });
  it("03 confirms replacement preserving old history and separate new identity", () => {
    const d = draft(), actions = [replace("fiction-draft-0001")];
    const result = confirmFictionalHumanOrderRepair(d, actions,
      previewFictionalHumanOrderRepair(d,actions),true);
    expect(result.snapshot.precedences.map(e=>e.status)).toEqual(["revoked","current","current"]);
    expect(result.snapshot.precedences[2].id).toBe("fiction-draft-0003");
    expect(result.audit.slice(-2).map(a=>a.action)).toEqual(["precedence_revoked","precedence_created"]);
    expect(result.real_g3_authorized).toBe(false);
    expect(d.snapshot.precedences[0].status).toBe("current");
  });
  it("04 rejects a cyclic replacement atomically", () => {
    const d = draft(), old = JSON.stringify(d);
    expect(()=>previewFictionalHumanOrderRepair(d,
      [replace("fiction-draft-0001","C","B")])).toThrow(/cycle/);
    expect(JSON.stringify(d)).toBe(old);
  });
  it("05 rejects duplicate or already historical revocations", () => {
    const d = draft(), row = revoke("fiction-draft-0001");
    expect(()=>previewFictionalHumanOrderRepair(d,[row,row])).toThrow();
    const old = revokeFictionalPrecedence(d,row.precedence_id,"Earlier human choice");
    expect(()=>previewFictionalHumanOrderRepair(old,[row])).toThrow();
  });
  it("06 refuses foreign, missing, retired and self-referential identifiers", () => {
    for (const id of ["missing","foreign:A"]) {
      expect(()=>previewFictionalHumanOrderRepair(draft(),[revoke(id)])).toThrow();
    }
    for (const after of ["retired","missing","A"]) {
      expect(()=>previewFictionalHumanOrderRepair(draft(),
        [replace("fiction-draft-0001","A",after)])).toThrow();
    }
  });
  it("07 refuses empty, oversized, forged and overlimit proposed actions", () => {
    const d = draft(), row = revoke("fiction-draft-0001");
    expect(()=>previewFictionalHumanOrderRepair(d,[])).toThrow();
    expect(()=>previewFictionalHumanOrderRepair(d,Array(17).fill(row))).toThrow();
    expect(()=>previewFictionalHumanOrderRepair(d,
      [{...row,revoke_reason:"  "}])).toThrow();
    expect(()=>previewFictionalHumanOrderRepair(d,
      [{...row,revoke_reason:"x".repeat(161)}])).toThrow();
    expect(()=>previewFictionalHumanOrderRepair(d,
      [{...row,write_to_disk:true} as unknown as FictionalHumanOrderRepair])).toThrow();
  });
  it("08 refuses stale baseline and edited staged actions at confirmation", () => {
    const d = draft(), row = revoke("fiction-draft-0001");
    const p = previewFictionalHumanOrderRepair(d,[row]);
    const changed = createFictionalPrecedence(d,"A","D","Other human choice");
    expect(()=>confirmFictionalHumanOrderRepair(changed,[row],p,true)).toThrow();
    expect(()=>confirmFictionalHumanOrderRepair(d,[replace(row.precedence_id)],p,true)).toThrow();
  });
  it("09 refuses forged preview contents and false writer claims", () => {
    const d = draft(), rows = [revoke("fiction-draft-0001")];
    const p = previewFictionalHumanOrderRepair(d,rows);
    expect(()=>confirmFictionalHumanOrderRepair(d,rows,{...p,candidate:d},true)).toThrow();
    expect(()=>confirmFictionalHumanOrderRepair(d,rows,
      {...p,can_write:true} as unknown as typeof p,true)).toThrow();
  });
  it("10 preserves both old IDs, audit order, narration and reader reveal", () => {
    const d = draft(), rows = [revoke("fiction-draft-0002"),revoke("fiction-draft-0001")];
    const p = previewFictionalHumanOrderRepair(d,rows);
    expect(p.candidate.snapshot.precedences.map(e=>e.id)).toEqual(["fiction-draft-0001","fiction-draft-0002"]);
    expect(p.candidate.snapshot.precedences.every(e=>e.status==="revoked")).toBe(true);
    expect(p.candidate.audit.slice(-2).map(a=>a.id)).toEqual(["fiction-draft-0002","fiction-draft-0001"]);
    expect(p.candidate.snapshot.narration).toEqual(d.snapshot.narration);
    expect(p.candidate.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("11 can redeclare the identical before/after pair with a new human explanation", () => {
    const d = draft(), p = previewFictionalHumanOrderRepair(d,
      [replace("fiction-draft-0001","A","B")]);
    expect(p.created_edge_ids).toEqual(["fiction-draft-0003"]);
    expect(p.candidate.snapshot.precedences[0].status).toBe("revoked");
    expect(p.candidate.snapshot.precedences[2].status).toBe("current");
  });
  it("12 rejects an origin pretending to be an operator database", () => {
    const d = {...draft(),data_origin:"real_db"};
    expect(()=>previewFictionalHumanOrderRepair(
      d as unknown as ReturnType<typeof draft>,[revoke("fiction-draft-0001")])).toThrow();
  });
  it("13 renders explicit correction options without fake persistence success", () => {
    const html = renderToStaticMarkup(createElement(M32FictionalHumanOrderBatchLab,
      {initial:scenario(),revisions:[]}));
    expect(html).toContain("Révoquer ou corriger une relation humaine");
    expect(html).toContain("Motif humain de révocation");
    expect(html).not.toContain("Confirmer explicitement toute la correction en mémoire");
    expect(html).not.toContain("Sauvegarde réussie");
  });
  it("14 escapes untrusted markup from invented active relation IDs", () => {
    const e = {id:"<script>bad()</script>",universe_id,status:"current" as const,
      before_anchor_id:"A",after_anchor_id:"B",reason:"Fiction"};
    const html = renderToStaticMarkup(createElement(M32FictionalHumanOrderBatchLab,
      {initial:{...scenario(),precedences:[e]},revisions:[]}));
    expect(html).not.toContain("<script>");
    expect(html).toContain("&lt;script&gt;");
  });
});
