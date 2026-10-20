import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import M32ManualChronologyLab from "./M32ManualChronologyLab";
import {
  startFictionalDraft, createFictionalAnchor, supersedeFictionalAnchor,
  createFictionalPrecedence, revokeFictionalPrecedence,
} from "./m32FictionalManualChronology";

const invented: M32ChronologyProjection = {
  universe_id: "fiction-one", reader_reveal_status: "not_authored",
  anchors: ["A", "B", "C"].map(id => ({
    id, universe_id: "fiction-one", status: "current" as const,
    time_kind: "unknown" as const, calendar_name: null,
    fictional_label: null, precision_text: null, source_revision_id: id === "A" ? "fiction-revision-A" : null,
  })),
  precedences: [],
  narration: [
    { universe_id: "fiction-one", novel_id: "novel-one", novel_title: "Roman imaginaire 1",
      chapter_id: "ch-one", chapter_title: "Chapitre 1", chapter_order: 0,
      scene_id: "s-one", scene_title: "Scène inventée 1", scene_order: 0 },
    { universe_id: "fiction-one", novel_id: "novel-two", novel_title: "Roman imaginaire 2",
      chapter_id: "ch-two", chapter_title: "Chapitre 2", chapter_order: 1,
      scene_id: "s-two", scene_title: "Scène inventée 2", scene_order: 0 },
  ],
};
const unknown = { kind: "unknown" as const, calendar: "", label: "", precision: "" };
const exact = { kind: "exact" as const, calendar: "Marées inventées",
  label: "Cloche XII", precision: "" };
const approximate = { kind: "approximate" as const, calendar: "Lunes fictives",
  label: "", precision: "entre le quatrième et le cinquième cycle" };
describe("M3.2 manually authored fictional-only chronology laboratory", () => {
  it("01 creates unknown and relative dates without inventing Gregorian values", () => {
    const a = createFictionalAnchor(startFictionalDraft(invented), unknown);
    const b = createFictionalAnchor(a, { ...unknown, kind: "relative" });
    expect(b.snapshot.anchors.at(-1)?.time_kind).toBe("relative");
    expect(b.snapshot.anchors.at(-2)?.fictional_label).toBeNull();
    expect(b.snapshot.anchors).toHaveLength(5);
    expect(b.real_g3_authorized).toBe(false);
  });
  it("02 creates exact and approximate fictional dates, no time conversion", () => {
    const a = createFictionalAnchor(startFictionalDraft(invented), exact);
    const b = createFictionalAnchor(a, approximate);
    expect(a.snapshot.anchors.at(-1)?.calendar_name).toBe("Marées inventées");
    expect(b.snapshot.anchors.at(-1)?.precision_text).toContain("cinquième");
  });
  it("03 fails closed on absent exact calendar or approximate precision", () => {
    expect(() => createFictionalAnchor(startFictionalDraft(invented), { ...exact, calendar: "" })).toThrow();
    expect(() => createFictionalAnchor(startFictionalDraft(invented), { ...approximate, precision: "" })).toThrow();
  });
  it("04 refuses cycle and leaves previous immutable state intact", () => {
    const a = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "A vient avant B");
    const b = createFictionalPrecedence(a, "B", "C", "B avant C");
    expect(() => createFictionalPrecedence(b, "C", "A", "Cycle interdit")).toThrow(/cycle/);
    expect(b.snapshot.precedences).toHaveLength(2);
    expect(invented.precedences).toHaveLength(0);
  });
  it("05 refuses self, duplicate and unknown anchor links", () => {
    const d = startFictionalDraft(invented);
    expect(() => createFictionalPrecedence(d, "A", "A", "soi-même")).toThrow();
    expect(() => createFictionalPrecedence(d, "A", "foreign", "autre univers")).toThrow();
    const a = createFictionalPrecedence(d, "A", "B", "preuve imaginée");
    expect(() => createFictionalPrecedence(a, "A", "B", "doublon")).toThrow();
  });
  it("06 corrects by supersession without mutating immutable revision", () => {
    const d = startFictionalDraft(invented);
    const corrected = supersedeFictionalAnchor(d, "A", exact);
    expect(corrected.snapshot.anchors.find(a => a.id === "A")?.status).toBe("superseded");
    expect(corrected.snapshot.anchors.find(a => a.id === "A")?.source_revision_id).toBe("fiction-revision-A");
    expect(corrected.snapshot.anchors.at(-1)?.status).toBe("current");
    expect(d.snapshot.anchors.find(a => a.id === "A")?.status).toBe("current");
  });
  it("07 requires explicit link revocation before anchor correction", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "reason");
    expect(() => supersedeFictionalAnchor(d, "A", exact)).toThrow(/révoquer/);
    const r = revokeFictionalPrecedence(d, d.snapshot.precedences[0].id, "historique corrigé");
    expect(supersedeFictionalAnchor(r, "A", exact).snapshot.anchors.at(-1)?.status).toBe("current");
  });
  it("08 keeps revoked relation and its separate audit reason", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ordre originel");
    const r = revokeFictionalPrecedence(d, d.snapshot.precedences[0].id, "correction humaine");
    expect(r.snapshot.precedences[0].status).toBe("revoked");
    expect(r.snapshot.precedences[0].reason).toBe("ordre originel");
    expect(r.audit.at(-1)?.explanation).toBe("correction humaine");
    expect(d.snapshot.precedences[0].status).toBe("current");
  });
  it("09 preserves narration from both novels and reader reveal unknown", () => {
    const d = createFictionalAnchor(startFictionalDraft(invented), exact);
    expect(d.snapshot.narration.map(n => n.novel_id)).toEqual(["novel-one", "novel-two"]);
    expect(d.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("10 mixed universe and invalid original cycle refuse all forms", () => {
    const foreign = { ...invented, anchors: [ { ...invented.anchors[0], universe_id: "fiction-two" }, ...invented.anchors.slice(1) ] };
    expect(() => startFictionalDraft(foreign)).toThrow();
    const cyclic = { ...invented, precedences: [
      { id: "ab", universe_id: "fiction-one", before_anchor_id: "A",
        after_anchor_id: "B", status: "current" as const, reason: "A B" },
      { id: "ba", universe_id: "fiction-one", before_anchor_id: "B",
        after_anchor_id: "A", status: "current" as const, reason: "B A" },
    ] };
    expect(() => startFictionalDraft(cyclic)).toThrow();
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab, { initial: cyclic }));
    expect(html).toContain("Atelier fictif refusé");
    expect(html).not.toContain("<fieldset");
  });
  it("11 rejects non-fictional universe and unbounded values", () => {
    expect(() => startFictionalDraft({ ...invented, universe_id: "u1" })).toThrow();
    expect(() => createFictionalAnchor(startFictionalDraft(invented),
      { ...exact, label: "X".repeat(161) })).toThrow();
  });
  it("12 static form exposes manual actions only in fictional mode", () => {
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab, { initial: invented }));
    for (const word of ["Ajouter l'ancre", "Remplacer sans effacer", "Ajouter avant/après",
      "Révoquer explicitement", "Ordre de narration", "Ordre de révélation"]) {
      expect(html).toContain(word);
    }
    expect(html).not.toContain("invoke(");
    expect(html).not.toContain("Date.parse");
    expect(html).not.toContain("fetch(");
  });
  it("13 refuses malformed legacy edge and forbids promotion to G3", () => {
    const d = startFictionalDraft(invented);
    expect(d.real_g3_authorized).toBe(false);
    expect(d.data_origin).toBe("fictional_browser_memory_only");
    const old = { ...invented, precedences: [
      { id: "ab", universe_id: "fiction-one", before_anchor_id: "A",
        after_anchor_id: "missing", status: "current" as const, reason: "wrong" },
    ] };
    expect(() => startFictionalDraft(old)).toThrow();
  });
});
