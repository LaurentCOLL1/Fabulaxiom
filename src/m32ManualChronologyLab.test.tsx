import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import M32ManualChronologyLab from "./M32ManualChronologyLab";
import { fictionalSelectionIsHistorical } from "./M32ManualChronologyLab";
import { compareM32WorldOrder } from "./M32WorldOrderComparison";
import { previewFictionalRevocationImpact } from "./m32FictionalRevocationImpact";
import {
  startFictionalDraft as startDraft, createFictionalAnchor, supersedeFictionalAnchor,
  createFictionalPrecedence, revokeFictionalPrecedence,
  previewFictionalPrecedence, previewFictionalCorrection, previewFictionalThreeOrders,
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
    expect(html).toContain("Choisir une ancre à corriger.");
    expect(html).toContain("Choisir deux ancres fictives actives.");
    const d = startFictionalDraft(invented);
    previewFictionalPrecedence(d, "A", "C");
    previewFictionalCorrection(d, "A");
    expect(d.snapshot.narration).toEqual(invented.narration);
    expect(d.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("33 explicitly binds the historical revision of a second fictional novel", () => {
    const d = createFictionalAnchor(startFictionalDraft(invented), {
      ...unknown, source_scene_id: "s-two", source_revision_id: "fiction-revision-C",
    });
    expect(d.snapshot.anchors.slice(-1)[0]?.source_revision_id).toBe("fiction-revision-C");
    expect(d.snapshot.narration.map(s => s.novel_id)).toEqual(["novel-one", "novel-two"]);
    expect(d.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("34 refuses crossing revision IDs between two novels", () => {
    const d = startFictionalDraft(invented);
    expect(() => createFictionalAnchor(d, { ...unknown, source_scene_id: "s-two",
      source_revision_id: "fiction-revision-A" })).toThrow(/révision/);
    expect(() => createFictionalAnchor(d, { ...unknown, source_scene_id: "s-one",
      source_revision_id: "fiction-revision-C" })).toThrow(/révision/);
    expect(d.audit).toHaveLength(0);
  });
  it("35 a second-novel correction preserves the exact immutable historical source", () => {
    const first = createFictionalAnchor(startFictionalDraft(invented), {
      ...unknown, source_scene_id: "s-two", source_revision_id: "fiction-revision-C",
    });
    const lastId = first.snapshot.anchors.slice(-1)[0]!.id;
    const next = supersedeFictionalAnchor(first, lastId, exact);
    expect(next.snapshot.anchors.find(a => a.id === lastId)?.source_revision_id)
      .toBe("fiction-revision-C");
    expect(next.snapshot.anchors.slice(-1)[0]?.source_revision_id).toBe("fiction-revision-C");
    expect(next.snapshot.narration).toEqual(invented.narration);
  });
  it("36 distinguishes manuscript order from world and read-only reveal across novels", () => {
    const d = startFictionalDraft(invented);
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab,
      { initial: invented, revisions: history }));
    expect(html).toContain("romans différents du même Univers");
    expect(html).toContain("Ordre de narration");
    expect(html).toContain("Ordre de révélation au lecteur");
    expect(d.snapshot.precedences).toHaveLength(0);
    expect(d.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("37 compares scene position only within an invented single novel", () => {
    const first = invented.narration[0];
    const added = { ...first, scene_id: "s-three", scene_title: "Troisième scène",
      scene_order: first.scene_order + 2 };
    const draft = startDraft({ ...invented, narration: [...invented.narration, added] }, history);
    const forward = previewFictionalThreeOrders(draft, first.scene_id, added.scene_id);
    const reverse = previewFictionalThreeOrders(draft, added.scene_id, first.scene_id);
    expect(forward.narration).toBe("before");
    expect(reverse.narration).toBe("after");
    expect(forward.world_reason).toContain("indéterminée");
    expect(forward.reader_reason).toContain("non renseignée");
  });
  it("38 rejects inferred global manuscript order between fictional novels", () => {
    const d = startFictionalDraft(invented);
    const p = previewFictionalThreeOrders(d, "s-one", "s-two");
    expect(p.verdict).toBe("allowed");
    expect(p.narration).toBe("separate_novels");
    expect(p.narration_reason).toContain("indéterminé entre romans");
  });
  it("39 treats the same scene as identity not two world events", () => {
    const p = previewFictionalThreeOrders(startFictionalDraft(invented), "s-one", "s-one");
    expect(p.narration).toBe("same_scene");
    expect(p.world_reason).toContain("indéterminée");
  });
  it("40 does not compare empty or foreign scene IDs", () => {
    const d = startFictionalDraft(invented);
    expect(previewFictionalThreeOrders(d, "", "s-one").verdict).toBe("unselected");
    expect(previewFictionalThreeOrders(d, "missing", "s-one").verdict).toBe("blocked");
    expect(d.audit).toHaveLength(0);
  });
  it("41 does not invent ordering for same-position scenes in one novel", () => {
    const other = { ...invented.narration[0], scene_id: "same-slot" };
    const draft = startDraft({ ...invented,
      narration: [...invented.narration, other] }, history);
    expect(previewFictionalThreeOrders(draft, "s-one", "same-slot").narration)
      .toBe("indeterminate");
  });
  it("42 three-order comparison is read-only even with active temporal edges", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "fiction only");
    const before = JSON.stringify(d);
    const x = previewFictionalThreeOrders(d, "s-one", "s-two");
    expect(x.world_reason).toContain("indéterminée");
    expect(JSON.stringify(d)).toBe(before);
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab,
      { initial: invented, revisions: history }));
    expect(html).toContain("Comparaison des trois ordres fictifs");
    expect(html).toContain("Première scène à comparer");
    expect(html).toContain("Deuxième scène à comparer");
    expect(html).not.toContain("invoke(");
  });
  it("43 reuses exact human edges, not manuscript placements, for active proof", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "human A-B");
    const x = compareM32WorldOrder(d.snapshot, "fiction-one", "A", "B");
    expect(x.relation).toBe("before");
    expect(x.witness.map(e => e.precedence_id)).toEqual(["fiction-draft-0001"]);
    expect(x.witness[0].human_reason).toBe("human A-B");
    expect(d.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("44 shows a two-link human witness without authoring an extra relation", () => {
    const d = createFictionalPrecedence(
      createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab"), "B", "C", "bc");
    const before = JSON.stringify(d);
    const x = compareM32WorldOrder(d.snapshot, "fiction-one", "A", "C");
    expect(x.relation).toBe("before");
    expect(x.witness.map(e => e.precedence_id))
      .toEqual(["fiction-draft-0001", "fiction-draft-0002"]);
    expect(JSON.stringify(d)).toBe(before);
  });
  it("45 gives reverse relation without reversing the human witness", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab");
    const x = compareM32WorldOrder(d.snapshot, "fiction-one", "B", "A");
    expect(x.relation).toBe("after");
    expect(x.witness[0]).toMatchObject({ before_anchor_id: "A", after_anchor_id: "B" });
  });
  it("46 refuses to use revoked links as current time evidence", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "human");
    const r = revokeFictionalPrecedence(d, "fiction-draft-0001", "not current");
    expect(compareM32WorldOrder(r.snapshot, "fiction-one", "A", "B").relation)
      .toBe("incomparable");
    expect(r.snapshot.precedences[0].reason).toBe("human");
  });
  it("47 refuses unknown and historical anchors without touching the draft", () => {
    const d = startFictionalDraft(invented);
    expect(() => compareM32WorldOrder(d.snapshot, "fiction-one", "A", "outsider")).toThrow();
    expect(() => compareM32WorldOrder(d.snapshot, "fiction-two", "A", "B")).toThrow();
    expect(compareM32WorldOrder(d.snapshot, "fiction-one", "C", "C").relation)
      .toBe("same");
    expect(d.audit).toHaveLength(0);
  });
  it("48 renders the independent read-only proof selectors in manual lab", () => {
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab,
      { initial: invented, revisions: history }));
    expect(html).toContain("Consulter une preuve de précédence humaine");
    expect(html).toContain("Première ancre à consulter");
    expect(html).toContain("Deuxième ancre à consulter");
    expect(html).toContain("Choisir deux ancres actives");
    expect(html).not.toContain("invoke(");
  });
  it("49 after supersession the old fictional anchor cannot prove current time", () => {
    const d = startFictionalDraft(invented);
    const corrected = supersedeFictionalAnchor(d, "C", unknown);
    expect(corrected.snapshot.anchors.find(a => a.id === "C")?.status).toBe("superseded");
    expect(() => compareM32WorldOrder(corrected.snapshot, "fiction-one", "A", "C"))
      .toThrow(/historique/);
    expect(d.snapshot.anchors.find(a => a.id === "C")?.status).toBe("current");
  });
  it("50 the corrected anchor retains source history without promoting reader reveal", () => {
    const corrected = supersedeFictionalAnchor(startFictionalDraft(invented), "A", exact);
    const old = corrected.snapshot.anchors.find(a => a.id === "A");
    expect(old?.source_revision_id).toBe("fiction-revision-A");
    expect(old?.status).toBe("superseded");
    expect(corrected.snapshot.reader_reveal_status).toBe("not_authored");
    expect(corrected.audit).toHaveLength(1);
  });
  it("51 prevents showing a stale world proof for a corrected ID", () => {
    expect(fictionalSelectionIsHistorical(["A", "B"], "A", "B")).toBe(false);
    expect(fictionalSelectionIsHistorical(["A", "B"], "A", "C")).toBe(true);
    expect(fictionalSelectionIsHistorical(["A", "B"], "C", "A")).toBe(true);
    expect(fictionalSelectionIsHistorical(["A", "B"], "", "A")).toBe(false);
    expect(fictionalSelectionIsHistorical(["K", "L"], "A", "K")).toBe(true);
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab,
      { initial: invented, revisions: history }));
    expect(html).toContain("Consulter une preuve de précédence humaine");
    expect(html).not.toContain("invoke(");
  });
  it("52 simulation without an explicitly chosen active edge remains unselected", () => {
    const draft = startFictionalDraft(invented);
    expect(previewFictionalRevocationImpact(draft, "").verdict).toBe("unselected");
    expect(previewFictionalRevocationImpact(draft, "foreign").verdict).toBe("blocked");
    expect(draft.audit).toHaveLength(0);
  });
  it("53 simulation of a sole human edge withdraws its proof, never the real draft", () => {
    const draft = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab");
    const before = JSON.stringify(draft);
    const preview = previewFictionalRevocationImpact(draft, "fiction-draft-0001");
    expect(preview.verdict).toBe("allowed");
    expect(preview.relation_after).toBe("incomparable");
    expect(preview.writes).toBe(false);
    expect(JSON.stringify(draft)).toEqual(before);
    expect(compareM32WorldOrder(draft.snapshot, "fiction-one", "A", "B").relation)
      .toBe("before");
  });
  it("54 if a second authored route remains, it is named as the only surviving proof", () => {
    const first = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab");
    const second = createFictionalPrecedence(first, "B", "C", "bc");
    const all = createFictionalPrecedence(second, "A", "C", "ac");
    const preview = previewFictionalRevocationImpact(all, "fiction-draft-0003");
    expect(preview.relation_after).toBe("before");
    expect(preview.witness_after).toEqual(["fiction-draft-0001", "fiction-draft-0002"]);
    expect(all.snapshot.precedences).toHaveLength(3);
    expect(all.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("55 a revoked or foreign relation cannot be re-simulated as current", () => {
    const d = createFictionalPrecedence(startFictionalDraft(invented), "A", "B", "ab");
    const gone = revokeFictionalPrecedence(d, "fiction-draft-0001", "human corrected");
    expect(previewFictionalRevocationImpact(gone, "fiction-draft-0001").verdict)
      .toBe("blocked");
    expect(gone.snapshot.precedences[0].reason).toBe("ab");
    const html = renderToStaticMarkup(createElement(M32ManualChronologyLab,
      { initial: invented, revisions: history }));
    expect(html).toContain("Prévisualisation de révocation fictive");
    expect(html).toContain("Cette prévisualisation ne révoque rien");
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
