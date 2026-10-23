import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import { compareM32WorldOrder } from "./M32WorldOrderComparison";
import M32TwoUniverseSafetyPreview from "./M32TwoUniverseSafetyPreview";
import {
  startFictionalDraft, createFictionalAnchor, createFictionalPrecedence,
  revokeFictionalPrecedence, supersedeFictionalAnchor,
  previewFictionalPrecedence, previewFictionalThreeOrders,
  previewFictionalSceneRevisionWorldOrder, type FictionalRevision,
} from "./m32FictionalManualChronology";

/** All identifiers and text are invented. Identical anchor/novel names across
 * two Universes must NOT establish identity across their separate namespaces.
 */
function fixture(universe: "fiction-alpha" | "fiction-beta") {
  const snapshot: M32ChronologyProjection = {
    universe_id: universe, reader_reveal_status: "not_authored",
    anchors: ["A", "B", "C"].map((id, i) => ({
      id, universe_id: universe, time_kind: "unknown" as const,
      status: "current" as const, calendar_name: null, fictional_label: null,
      precision_text: null, source_revision_id: i < 2 ? universe + "-rev-" + (i + 1) : null,
    })),
    precedences: [],
    narration: [
      { universe_id: universe, novel_id: "novel-one", novel_title: "Roman homonyme",
        chapter_id: "chapter-one", chapter_title: "Chapitre inventé", chapter_order: 0,
        scene_id: "scene-one", scene_title: "Scène homonyme", scene_order: 0 },
      { universe_id: universe, novel_id: "novel-two", novel_title: "Roman homonyme",
        chapter_id: "chapter-two", chapter_title: "Chapitre inventé", chapter_order: 0,
        scene_id: "scene-two", scene_title: "Scène homonyme", scene_order: 0 },
    ],
  };
  const revisions: readonly FictionalRevision[] = [
    { universe_id: universe, novel_id: "novel-one", scene_id: "scene-one",
      revision_id: universe + "-rev-1", revision_label: "Révision inventée" },
    { universe_id: universe, novel_id: "novel-two", scene_id: "scene-two",
      revision_id: universe + "-rev-2", revision_label: "Révision inventée" },
  ];
  return { snapshot, revisions };
}
function alpha() { const f = fixture("fiction-alpha"); return startFictionalDraft(f.snapshot, f.revisions); }
function beta() { const f = fixture("fiction-beta"); return startFictionalDraft(f.snapshot, f.revisions); }
const unknown = { kind: "unknown" as const, calendar: "", label: "", precision: "" };

describe("M3.2 two-Universe / two-Novel invented-only acceptance rehearsal", () => {
  it("01 creates two distinct independent in-memory drafts", () => {
    const a = alpha(), b = beta();
    expect(a.snapshot.universe_id).toBe("fiction-alpha");
    expect(b.snapshot.universe_id).toBe("fiction-beta");
    expect(a.snapshot.anchors.map(x => x.id)).toEqual(b.snapshot.anchors.map(x => x.id));
    expect(a.snapshot.anchors).not.toBe(b.snapshot.anchors);
    expect(a.real_g3_authorized).toBe(false);
    expect(b.real_g3_authorized).toBe(false);
  });
  it("02 retains the two fictional novels separately within each Universe", () => {
    for (const d of [alpha(), beta()]) {
      expect(new Set(d.snapshot.narration.map(s => s.novel_id)).size).toBe(2);
      expect(previewFictionalThreeOrders(d, "scene-one", "scene-two").narration)
        .toBe("separate_novels");
      expect(d.snapshot.reader_reveal_status).toBe("not_authored");
    }
  });
  it("03 one Universe exact manual date never changes the other Universe", () => {
    const a = alpha(), b = beta();
    const updated = createFictionalAnchor(a, {
      kind: "exact", calendar: "Cycle Alpha", label: "Marée XII", precision: "",
    });
    expect(updated.snapshot.anchors[updated.snapshot.anchors.length - 1]?.calendar_name).toBe("Cycle Alpha");
    expect(b.snapshot.anchors).toHaveLength(3);
    expect(a.snapshot.anchors).toHaveLength(3);
    expect(updated.snapshot.universe_id).toBe("fiction-alpha");
  });
  it("04 unknown relative and approximate time do not invent a common calendar", () => {
    const a = createFictionalAnchor(alpha(), unknown);
    const b = createFictionalAnchor(beta(), {
      kind: "approximate", calendar: "Lunes Bêta", label: "",
      precision: "phase inconnue",
    });
    const c = createFictionalAnchor(a, { ...unknown, kind: "relative" });
    expect(c.snapshot.anchors[c.snapshot.anchors.length - 1]?.time_kind).toBe("relative");
    expect(c.snapshot.anchors[c.snapshot.anchors.length - 1]?.calendar_name).toBeNull();
    expect(b.snapshot.anchors[b.snapshot.anchors.length - 1]?.precision_text).toBe("phase inconnue");
    expect(b.snapshot.anchors[b.snapshot.anchors.length - 1]?.calendar_name).toBe("Lunes Bêta");
  });
  it("05 identically named anchors can have opposite human order in distinct Universes", () => {
    const a = createFictionalPrecedence(alpha(), "A", "B", "Alpha avant B");
    const b = createFictionalPrecedence(beta(), "B", "A", "Bêta avant A");
    expect(compareM32WorldOrder(a.snapshot, "fiction-alpha", "A", "B").relation).toBe("before");
    expect(compareM32WorldOrder(b.snapshot, "fiction-beta", "A", "B").relation).toBe("after");
    expect(a.snapshot.precedences[0].universe_id).toBe("fiction-alpha");
    expect(b.snapshot.precedences[0].universe_id).toBe("fiction-beta");
  });
  it("06 cyclic declaration in Alpha is rejected without mutating Bêta", () => {
    const a = createFictionalPrecedence(
      createFictionalPrecedence(alpha(), "A", "B", "A-B"), "B", "C", "B-C");
    const b = beta(), previous = JSON.stringify(b);
    expect(() => createFictionalPrecedence(a, "C", "A", "Cycle interdit")).toThrow(/cycle/);
    expect(JSON.stringify(b)).toBe(previous);
    expect(a.snapshot.precedences).toHaveLength(2);
  });
  it("07 foreign-Universe revisions cannot be injected into the initial catalogue", () => {
    const a = fixture("fiction-alpha"), b = fixture("fiction-beta");
    expect(() => startFictionalDraft(a.snapshot, [...a.revisions, ...b.revisions])).toThrow();
  });
  it("08 foreign source revision cannot be bound to a local scene", () => {
    expect(() => createFictionalAnchor(alpha(), {
      ...unknown, source_scene_id: "scene-one",
      source_revision_id: "fiction-beta-rev-1",
    })).toThrow();
  });
  it("09 projection decoder refuses a foreign narration row", () => {
    const a = fixture("fiction-alpha"), b = fixture("fiction-beta");
    const mixed = { ...a.snapshot, narration: [...a.snapshot.narration, b.snapshot.narration[0]] };
    expect(() => startFictionalDraft(mixed, a.revisions)).toThrow();
  });
  it("10 source revision proof remains Universe-scoped, never inferred by manuscript label", () => {
    const a = createFictionalPrecedence(alpha(), "A", "B", "A avant B");
    expect(previewFictionalSceneRevisionWorldOrder(a, "scene-one",
      "fiction-alpha-rev-1", "scene-two", "fiction-alpha-rev-2").verdict).toBe("proven");
    expect(previewFictionalSceneRevisionWorldOrder(beta(), "scene-one",
      "fiction-beta-rev-1", "scene-two", "fiction-beta-rev-2").verdict).toBe("indeterminate");
    expect(previewFictionalSceneRevisionWorldOrder(a, "scene-one",
      "fiction-beta-rev-1", "scene-two", "fiction-beta-rev-2").verdict).toBe("blocked");
  });
  it("11 correction and revocation in Alpha do not silently rewrite Bêta", () => {
    const b = createFictionalPrecedence(beta(), "A", "B", "Bêta A-B");
    let a = createFictionalPrecedence(alpha(), "A", "B", "Alpha A-B");
    a = revokeFictionalPrecedence(a, a.snapshot.precedences[0].id, "Révocation humaine");
    a = supersedeFictionalAnchor(a, "A", unknown);
    expect(a.snapshot.anchors.find(x => x.id === "A")?.status).toBe("superseded");
    expect(b.snapshot.anchors.find(x => x.id === "A")?.status).toBe("current");
    expect(b.snapshot.precedences[0].status).toBe("current");
  });
  it("12 cross-Universe projection comparison refuses the wrong explicit scope", () => {
    expect(() => compareM32WorldOrder(alpha().snapshot, "fiction-beta", "A", "B")).toThrow();
    expect(previewFictionalPrecedence(alpha(), "A", "foreign-anchor").verdict).toBe("blocked");
  });
  it("13 read-only side-by-side preview labels the Universes without enabling persistence", () => {
    const markup = renderToStaticMarkup(createElement(M32TwoUniverseSafetyPreview,
      { left: alpha(), right: beta() }));
    expect(markup).toContain("fiction-alpha");
    expect(markup).toContain("fiction-beta");
    expect(markup).toContain("aucune chronologie commune");
    expect(markup).toContain("Simulation en mémoire seulement");
    expect(markup).toContain("lecture seule");
  });
  it("14 read-only preview rejects an identical or forged same-Universe pair", () => {
    expect(() => renderToStaticMarkup(createElement(M32TwoUniverseSafetyPreview,
      { left: alpha(), right: alpha() }))).toThrow(/deux univers fictifs distincts/);
  });
});
