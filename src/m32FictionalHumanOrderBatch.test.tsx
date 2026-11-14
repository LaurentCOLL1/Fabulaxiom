import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32FictionalHumanOrderBatchLab from "./M32FictionalHumanOrderBatchLab";
import {
  previewFictionalHumanOrderBatch, confirmFictionalHumanOrderBatch,
  type FictionalHumanOrder,
} from "./m32FictionalHumanOrderBatch";
import {
  startFictionalDraft, createFictionalPrecedence,
} from "./m32FictionalManualChronology";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";

const universe_id = "fiction-order-batch";
const time = (id: string, status: "current" | "revoked" = "current") => ({
  id, universe_id, status, time_kind: "unknown" as const, calendar_name: null,
  fictional_label: null, precision_text: null, source_revision_id: null,
});
function sample(): M32ChronologyProjection {
  return {
    universe_id, reader_reveal_status: "not_authored",
    anchors: [time("A"), time("B"), time("C"), time("D"), time("retired", "revoked")],
    precedences: [], narration: [],
  };
}
function draft() { return startFictionalDraft(sample()); }
const row = (before_anchor_id: string, after_anchor_id: string, reason = "Choix humain") => ({
  before_anchor_id, after_anchor_id, reason,
});
const plan: readonly FictionalHumanOrder[] = [row("A", "B"), row("B", "C")];

describe("M3.2 P3ac fictional batch of explicit human world-order relations", () => {
  it("01 previews a two-step human plan without modifying its baseline", () => {
    const before = draft(), bytes = JSON.stringify(before);
    const preview = previewFictionalHumanOrderBatch(before, plan);
    expect(JSON.stringify(before)).toBe(bytes);
    expect(preview.preview_only).toBe(true);
    expect(preview.can_write).toBe(false);
    expect(preview.world_order_inferred).toBe(false);
    expect(preview.candidate.snapshot.precedences).toHaveLength(2);
    expect(preview.proposed_edge_ids).toEqual(["fiction-draft-0001", "fiction-draft-0002"]);
  });
  it("02 refuses an unconfirmed batch even when its preview passes", () => {
    const d = draft(), p = previewFictionalHumanOrderBatch(d, plan);
    expect(() => confirmFictionalHumanOrderBatch(d, plan, p, false)).toThrow();
    expect(d.snapshot.precedences).toHaveLength(0);
  });
  it("03 applies all valid rows only after explicit confirmation in RAM", () => {
    const d = draft(), p = previewFictionalHumanOrderBatch(d, plan);
    const result = confirmFictionalHumanOrderBatch(d, plan, p, true);
    expect(result.snapshot.precedences.map(x => [x.before_anchor_id, x.after_anchor_id]))
      .toEqual([["A", "B"], ["B", "C"]]);
    expect(result.audit).toHaveLength(2);
    expect(result.real_g3_authorized).toBe(false);
    expect(result.data_origin).toBe("fictional_browser_memory_only");
    expect(d.audit).toHaveLength(0);
  });
  it("04 rejects the entire plan if its LAST action creates a cycle", () => {
    const d = draft(), bytes = JSON.stringify(d);
    expect(() => previewFictionalHumanOrderBatch(d,
      [...plan, row("C", "A", "a forbidden cycle")])).toThrow(/cycle/);
    expect(JSON.stringify(d)).toBe(bytes);
  });
  it("05 rejects a duplicate relation within the same batch", () => {
    expect(() => previewFictionalHumanOrderBatch(draft(),
      [row("A", "D"), row("A", "D")])).toThrow();
  });
  it("06 rejects a cycle with an existing original active relation", () => {
    const d = createFictionalPrecedence(draft(), "C", "A", "Original declaration");
    expect(() => previewFictionalHumanOrderBatch(d, plan)).toThrow(/cycle/);
    expect(d.snapshot.precedences).toHaveLength(1);
  });
  it("07 rejects unknown, retired and cross-Universe anchor IDs", () => {
    const d = draft();
    for (const id of ["missing", "retired", "foreign-world:A"]) {
      expect(() => previewFictionalHumanOrderBatch(d, [row("A", id)])).toThrow();
    }
  });
  it("08 refuses missing or blank human rationales", () => {
    expect(() => previewFictionalHumanOrderBatch(draft(), [row("A", "B", " ")])).toThrow();
    expect(() => previewFictionalHumanOrderBatch(draft(), [row("A", "B", "")])).toThrow();
  });
  it("09 refuses empty plans, 17 rows and forged action fields", () => {
    expect(() => previewFictionalHumanOrderBatch(draft(), [])).toThrow();
    expect(() => previewFictionalHumanOrderBatch(draft(),
      Array.from({ length: 17 }, () => row("A", "B")))).toThrow();
    expect(() => previewFictionalHumanOrderBatch(draft(),
      [{ ...row("A", "B"), write_to_disk: true } as unknown as FictionalHumanOrder])).toThrow();
  });
  it("10 refuses a preview from an earlier unrelated draft state", () => {
    const a = draft(), p = previewFictionalHumanOrderBatch(a, plan);
    const b = createFictionalPrecedence(a, "A", "D", "Independent action");
    expect(() => confirmFictionalHumanOrderBatch(b, plan, p, true)).toThrow();
  });
  it("11 refuses a preview after its staged content changes", () => {
    const a = draft(), p = previewFictionalHumanOrderBatch(a, plan);
    expect(() => confirmFictionalHumanOrderBatch(a, [row("A", "D")], p, true)).toThrow();
  });
  it("12 refuses tampering with expected candidates or advertised provenance", () => {
    const a = draft(), p = previewFictionalHumanOrderBatch(a, plan);
    expect(() => confirmFictionalHumanOrderBatch(a, plan,
      { ...p, candidate: a }, true)).toThrow();
    expect(() => confirmFictionalHumanOrderBatch(a, plan,
      { ...p, can_write: true } as unknown as typeof p, true)).toThrow();
  });
  it("13 produces identical invented IDs for repeat plans", () => {
    expect(previewFictionalHumanOrderBatch(draft(), plan).proposed_edge_ids)
      .toEqual(previewFictionalHumanOrderBatch(draft(), plan).proposed_edge_ids);
  });
  it("14 does not infer story order, narrator chronology or a reading reveal", () => {
    const d = draft(), next = confirmFictionalHumanOrderBatch(
      d, plan, previewFictionalHumanOrderBatch(d, plan), true);
    expect(next.snapshot.narration).toEqual([]);
    expect(next.snapshot.reader_reveal_status).toBe("not_authored");
    expect(next.snapshot.anchors).toEqual(d.snapshot.anchors);
  });
  it("15 rejects forged non-fictional origins before any proposal", () => {
    const d = { ...draft(), data_origin: "real_db" };
    expect(() => previewFictionalHumanOrderBatch(
      d as unknown as ReturnType<typeof draft>, plan)).toThrow();
  });
  it("16 only renders human confirmation after an explicit in-memory preview", () => {
    const html = renderToStaticMarkup(createElement(M32FictionalHumanOrderBatchLab,
      { initial: sample(), revisions: [] }));
    expect(html).toContain("Déclarer plusieurs relations avant/après");
    expect(html).toContain("Vérifier le lot complet");
    expect(html).not.toContain("Confirmer explicitement tout le lot");
    expect(html).toContain("Aucun fichier");
    expect(html).not.toContain("Sauvegarde réussie");
  });
  it("17 never evaluates untrusted ID markup as HTML in initial controls", () => {
    const base = sample();
    const x = { ...base, anchors: base.anchors.map((a, i) =>
      i === 0 ? { ...a, id: "<script>unsafe()</script>" } : a) };
    const markup = renderToStaticMarkup(createElement(M32FictionalHumanOrderBatchLab,
      { initial: x, revisions: [] }));
    expect(markup).not.toContain("<script>");
    expect(markup).toContain("&lt;script&gt;");
  });
  it("18 action ordering is not silently sorted or reversed", () => {
    const d = draft(), p = previewFictionalHumanOrderBatch(d,
      [row("C", "D"), row("A", "B")]);
    expect(p.candidate.snapshot.precedences.map(x => x.before_anchor_id))
      .toEqual(["C", "A"]);
  });
});
