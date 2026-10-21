import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import M32ManualChronologyLab from "./M32ManualChronologyLab";
import {
  startFictionalDraft as startDraft, createFictionalAnchor, supersedeFictionalAnchor,
  createFictionalPrecedence, revokeFictionalPrecedence,
  previewFictionalPrecedence, previewFictionalCorrection,
  type FictionalRevision,
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
const history: readonly FictionalRevision[] = [
  { universe_id: "fiction-one", novel_id: "novel-one", scene_id: "s-one",
    revision_id: "fiction-revision-A", revision_label: "Texte initial" },
  { universe_id: "fiction-one", novel_id: "novel-one", scene_id: "s-one",
    revision_id: "fiction-revision-B", revision_label: "Texte de travail plus tardif" },
  { universe_id: "fiction-one", novel_id: "novel-two", scene_id: "s-two",
    revision_id: "fiction-revision-C", revision_label: "Deuxième roman" },
];
function startFictionalDraft(snapshot: M32ChronologyProjection) {
  return startDraft(snapshot, history);
}
const unknown = { kind: "unknown" as const, calendar: "", label: "", precision: "" };
const exact = { kind: "exact" as const, calendar: "Marées inventées",
  label: "Cloche XII", precision: "" };
const approximate = { kind: "approximate" as const, calendar: "Lunes fictives",
  label: "", precision: "entre le quatrième et le cinquième cycle" };
describe("M3.2 manually authored fictional-only chronology laboratory", () => {
  it("01 creates unknown and relative dates without inventing Gregorian values", () => {
    const a = createFictionalAnchor(startFictionalDraft(invented), unknown);
    const b = createFictionalAnchor(a, { ...unknown, kind: "relative" });
    expect(b.snapshot.anchors[b.snapshot.anchors.length - 1]?.time_kind).toBe("relative");
    expect(b.snapshot.anchors[b.snapshot.anchors.length - 2]?.fictional_label).toBeNull();
    expect(b.snapshot.anchors).toHaveLength(5);
    expect(b.real_g3_authorized).toBe(false);
  });
  it("02 creates exact and approximate fictional dates, no time conversion", () => {
    const a = createFictionalAnchor(startFictionalDraft(invented), exact);
    const b = createFictionalAnchor(a, approximate);
    expect(a.snapshot.anchors[a.snapshot.anchors.length - 1]?.calendar_name).toBe("Marées inventées");
    expect(b.snapshot.anchors[b.snapshot.anchors.length - 1]?.precision_text).toContain("cinquième");
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
    expect(corrected.snapshot.anchors[corrected.snapshot.anchors.length - 1]?.status).toBe("current");
    expect(d.snapshot.anchors.find(a => a.id === "A")?.status).toBe("current");
  });
  it("07 requires explicit link revocation before anchor correction", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "reason");
    expect(() => supersedeFictionalAnchor(d, "A", exact)).toThrow(/révoquer/);
    const r = revokeFictionalPrecedence(d, d.snapshot.precedences[0].id, "historique corrigé");
    expect(supersedeFictionalAnchor(r, "A", exact).snapshot.anchors.slice(-1)[0]?.status).toBe("current");
  });
  it("08 keeps revoked relation and its separate audit reason", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ordre originel");
    const r = revokeFictionalPrecedence(d, d.snapshot.precedences[0].id, "correction humaine");
    expect(r.snapshot.precedences[0].status).toBe("revoked");
    expect(r.snapshot.precedences[0].reason).toBe("ordre originel");
    expect(r.audit[r.audit.length - 1]?.explanation).toBe("correction humaine");
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
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab, { initial: cyclic, revisions: history }));
    expect(html).toContain("Atelier fictif refusé");
    expect(html).not.toContain("<fieldset");
  });
  it("11 rejects non-fictional universe and unbounded values", () => {
    expect(() => startFictionalDraft({ ...invented, universe_id: "u1" })).toThrow();
    expect(() => createFictionalAnchor(startFictionalDraft(invented),
      { ...exact, label: "X".repeat(161) })).toThrow();
  });
  it("12 static form exposes manual actions only in fictional mode", () => {
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab, { initial: invented, revisions: history }));
    for (const word of ["Ajouter l'ancre", "Remplacer sans effacer", "Ajouter avant/après",
      "Révoquer explicitement", "Ordre de narration", "Ordre de révélation"]) {
      expect(html).toContain(word.replace(/'/g, "&#x27;"));
    }
    expect(html).not.toContain("invoke(");
    expect(html).not.toContain("Date.parse");
    expect(html).not.toContain("fetch(");
  });
  it("14 selects exact historical revision by immutable identifier, not latest scene head", () => {
    const d = createFictionalAnchor(startFictionalDraft(invented),
      { ...exact, source_scene_id: "s-one", source_revision_id: "fiction-revision-A" });
    expect(d.snapshot.anchors.slice(-1)[0].source_revision_id).toBe("fiction-revision-A");
    expect(d.snapshot.narration[0].scene_id).toBe("s-one");
    expect(d.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("15 rejects source scene paired with a revision belonging to another scene", () => {
    expect(() => createFictionalAnchor(startFictionalDraft(invented),
      { ...exact, source_scene_id: "s-two", source_revision_id: "fiction-revision-A" })).toThrow(/révision/);
  });
  it("16 refuses unlisted revision, guessed head or orphan scene", () => {
    const d = startFictionalDraft(invented);
    expect(() => createFictionalAnchor(d,
      { ...unknown, source_scene_id: "s-one", source_revision_id: "fiction-current-head" })).toThrow();
    expect(() => createFictionalAnchor(d,
      { ...unknown, source_scene_id: "orphan", source_revision_id: "fiction-revision-A" })).toThrow();
    expect(() => createFictionalAnchor(d,
      { ...unknown, source_scene_id: "s-one", source_revision_id: "" })).toThrow();
  });
  it("17 rejects duplicate revision IDs even if display labels differ", () => {
    expect(() => startDraft(invented, [...history, { ...history[0], revision_label: "Changed name" }])).toThrow();
  });
  it("18 rejects foreign universe, novel mismatch and scene missing from narration", () => {
    for (const catalog of [
      [{ ...history[0], universe_id: "fiction-two" }],
      [{ ...history[0], novel_id: "novel-two" }],
      [{ ...history[0], scene_id: "ghost" }],
    ]) {
      expect(() => startDraft(invented, catalog)).toThrow();
    }
  });
  it("19 prior source revision survives supersession and next version inherits it", () => {
    const d = startFictionalDraft(invented);
    const next = supersedeFictionalAnchor(d, "A", unknown);
    expect(next.snapshot.anchors.find(a => a.id === "A")?.source_revision_id).toBe("fiction-revision-A");
    expect(next.snapshot.anchors.slice(-1)[0].source_revision_id).toBe("fiction-revision-A");
    expect(next.revisions.find(r => r.revision_id === "fiction-revision-A")?.scene_id).toBe("s-one");
  });
  it("20 an explicit correction can choose a different historical revision", () => {
    const d = supersedeFictionalAnchor(startFictionalDraft(invented), "A",
      { ...unknown, source_scene_id: "s-one", source_revision_id: "fiction-revision-B" });
    expect(d.snapshot.anchors.find(a => a.id === "A")?.source_revision_id).toBe("fiction-revision-A");
    expect(d.snapshot.anchors.slice(-1)[0].source_revision_id).toBe("fiction-revision-B");
  });
  it("21 source arrays remain detached from caller-owned invented objects", () => {
    const revisions = history.map(r => ({ ...r }));
    const draft = startDraft(invented, revisions);
    revisions[0].revision_label = "Tampered by caller";
    expect(draft.revisions[0].revision_label).toBe("Texte initial");
    expect(draft.snapshot.anchors[0].source_revision_id).toBe("fiction-revision-A");
    expect(draft.real_g3_authorized).toBe(false);
  });
  it("22 view shows historical revision choices and cannot acquire real data", () => {
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab,
      { initial: invented, revisions: history }));
    expect(html).toContain("Scène inventée à citer");
    expect(html).toContain("s-one");
    expect(html).toContain("Sans nouvelle référence de scène");
    expect(html).not.toContain("invoke(");
  });
  it("23 refuses proposed C-before-A cycle with a deterministic A-B-C witness", () => {
    const d = createFictionalPrecedence(
      createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab"),
      "B", "C", "bc");
    const p = previewFictionalPrecedence(d, "C", "A");
    expect(p.verdict).toBe("blocked");
    expect(p.reason).toContain("cycle temporel");
    expect(p.witness_anchor_ids).toEqual(["C", "A", "B", "C"]);
    expect(p.witness_edge_ids).toEqual(["fiction-draft-0001", "fiction-draft-0002"]);
    expect(() => createFictionalPrecedence(d, "C", "A", "not allowed"))
      .toThrow(/cycle temporel/);
    expect(d.snapshot.precedences).toHaveLength(2);
  });
  it("24 treats blank selections as unselected with no fabricated order", () => {
    expect(previewFictionalPrecedence(startFictionalDraft(invented), "", "B").verdict)
      .toBe("unselected");
  });
  it("25 distinguishes missing, historical, and self references", () => {
    const d = startFictionalDraft(invented);
    expect(previewFictionalPrecedence(d, "unknown", "B").verdict).toBe("blocked");
    expect(previewFictionalPrecedence(d, "A", "A").reason).toMatch(/réflexive/);
  });
  it("26 reports the matching already declared direct-edge ID", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "once");
    expect(previewFictionalPrecedence(d, "A", "B").witness_edge_ids)
      .toEqual(["fiction-draft-0001"]);
    expect(() => createFictionalPrecedence(d, "A", "B", "duplicate")).toThrow();
  });
  it("27 does not invent chronology between unrelated active anchors", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab");
    expect(previewFictionalPrecedence(d, "A", "C")).toMatchObject({
      verdict: "allowed", witness_anchor_ids: [], witness_edge_ids: [],
    });
    expect(d.snapshot.precedences).toHaveLength(1);
  });
  it("28 resolves conflict after explicit revocation while keeping previous proof", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab");
    const e = createFictionalPrecedence(d, "B", "C", "bc");
    const r = revokeFictionalPrecedence(e, "fiction-draft-0001", "user corrected historical claim");
    expect(previewFictionalPrecedence(r, "C", "A").verdict).toBe("allowed");
    expect(r.snapshot.precedences[0].status).toBe("revoked");
    expect(e.snapshot.precedences[0].status).toBe("current");
  });
  it("29 previews the exact dependency ID before an anchor supersession", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab");
    expect(previewFictionalCorrection(d, "A")).toMatchObject({
      verdict: "blocked", active_edge_ids: ["fiction-draft-0001"],
      historical_revision_id: "fiction-revision-A",
    });
    expect(() => supersedeFictionalAnchor(d, "A", exact)).toThrow(/fiction-draft-0001/);
  });
  it("30 retains historic revision ID once dependency is explicitly revoked", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab");
    const r = revokeFictionalPrecedence(d, "fiction-draft-0001", "correct");
    expect(previewFictionalCorrection(r, "A")).toMatchObject({
      verdict: "allowed", active_edge_ids: [], historical_revision_id: "fiction-revision-A",
    });
    const next = supersedeFictionalAnchor(r, "A", exact);
    expect(next.snapshot.anchors.find(a => a.id === "A")?.source_revision_id)
      .toBe("fiction-revision-A");
  });
  it("31 never previews missing anchor as eligible to correct", () => {
    expect(previewFictionalCorrection(startFictionalDraft(invented), "").verdict).toBe("unselected");
    expect(previewFictionalCorrection(startFictionalDraft(invented), "foreign").verdict).toBe("blocked");
  });
  it("32 displays witness controls without changing source, narration or reveal", () => {
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab,
      { initial: invented, revisions: history }));
    expect(html).toContain("Vérification avant/après fictive");
    expect(html).toContain("Vérification de correction fictive");
    expect(html).toContain("Révision historique");
    const d = startFictionalDraft(invented);
    previewFictionalPrecedence(d, "A", "C");
    previewFictionalCorrection(d, "A");
    expect(d.snapshot.narration).toEqual(invented.narration);
    expect(d.snapshot.reader_reveal_status).toBe("not_authored");
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
