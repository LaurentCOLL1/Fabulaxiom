import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32ChronologyPreview, {
  type M32AnchorProjection,
  type M32ChronologyProjection,
  type M32TimeKind,
} from "./M32ChronologyPreview";
import M32WorldOrderComparison, {
  compareM32WorldOrder,
} from "./M32WorldOrderComparison";

// P3v: separate synthetic Universes may legitimately reuse the same IDs.
// These snapshots never come from App.tsx, Tauri, SQLite or an operator profile.
function fixture(universe: string): M32ChronologyProjection {
  const anchor = (
    id: string, time_kind: M32TimeKind, status: "current" | "revoked",
    calendar_name: string | null = null,
    fictional_label: string | null = null,
    precision_text: string | null = null,
  ): M32AnchorProjection => ({
    id, universe_id: universe, time_kind, status, calendar_name,
    fictional_label, precision_text, source_revision_id: "revision-" + universe,
  });
  return {
    universe_id: universe,
    reader_reveal_status: "not_authored",
    anchors: [
      anchor("A", "exact", "current", "Calendrier " + universe, "Jour 2"),
      anchor("B", "approximate", "current", "Calendrier " + universe, null, "Saison"),
      anchor("C", "relative", "current"),
      anchor("D", "unknown", "current"),
      anchor("OLD", "unknown", "revoked"),
    ],
    precedences: [
      { id: "edge-1", universe_id: universe, before_anchor_id: "A",
        after_anchor_id: "B", status: "current", reason: "Cause " + universe },
      { id: "edge-2", universe_id: universe, before_anchor_id: "B",
        after_anchor_id: "C", status: "current", reason: "Suite " + universe },
      { id: "edge-old", universe_id: universe, before_anchor_id: "A",
        after_anchor_id: "C", status: "revoked", reason: "Historique " + universe },
    ],
    narration: [
      { scene_id: "scene-1", universe_id: universe, novel_id: "novel-1",
        novel_title: "Premier roman " + universe, chapter_id: "chapter-1",
        chapter_title: "Début", chapter_order: 0, scene_order: 0,
        scene_title: "Flashback" },
      { scene_id: "scene-2", universe_id: universe, novel_id: "novel-2",
        novel_title: "Second roman " + universe, chapter_id: "chapter-2",
        chapter_title: "Autre temps", chapter_order: 0, scene_order: 0,
        scene_title: "Révélation différée" },
    ],
  };
}
function compare(snapshot: M32ChronologyProjection, universe: string, left = "A", right = "C") {
  return compareM32WorldOrder(snapshot, universe, left, right);
}
function comparisonHtml(snapshot: M32ChronologyProjection, universe: string): string {
  return renderToStaticMarkup(createElement(M32WorldOrderComparison, {
    expectedUniverseId: universe, snapshot, leftAnchorId: "A", rightAnchorId: "C",
  }));
}
function overviewHtml(snapshot: M32ChronologyProjection, universe: string): string {
  return renderToStaticMarkup(createElement(M32ChronologyPreview, {
    expectedUniverseId: universe, snapshot,
  }));
}

describe("M3.2 P3v fiction-only independent Universe identity and chronology boundaries", () => {
  it("accepts homonymous anchors, precedence IDs and scene IDs in SEPARATE Universes", () => {
    const first = fixture("universe-one");
    const second = fixture("universe-two");
    const bytes = [JSON.stringify(first), JSON.stringify(second)];
    for (const [universe, snapshot] of [
      ["universe-one", first], ["universe-two", second],
    ] as const) {
      const forward = compare(snapshot, universe);
      const backward = compare(snapshot, universe, "C", "A");
      expect(forward.relation).toBe("before");
      expect(backward.relation).toBe("after");
      expect(forward.witness.map(step => step.precedence_id)).toEqual(["edge-1", "edge-2"]);
      expect(forward.witness.map(step => step.human_reason))
        .toEqual(["Cause " + universe, "Suite " + universe]);
      expect(compare(snapshot, universe, "C", "D")).toMatchObject({
        relation: "incomparable", witness: [], data_origin: "synthetic_in_memory_only",
        edit_controls_available: false,
      });
      expect(comparisonHtml(snapshot, universe)).toContain("Cause " + universe);
      const html = overviewHtml(snapshot, universe);
      expect(html).toContain("Premier roman " + universe);
      expect(html).toContain("Second roman " + universe);
      expect(html).toContain("Ordre de révélation au lecteur");
      expect(html).toContain("Non renseigné");
      expect(html).not.toMatch(/<(button|input|form|textarea)\b/);
    }
    expect(comparisonHtml(first, "universe-one")).not.toContain("Cause universe-two");
    expect(comparisonHtml(second, "universe-two")).not.toContain("Cause universe-one");
    expect(JSON.stringify(first)).toBe(bytes[0]);
    expect(JSON.stringify(second)).toBe(bytes[1]);
  });

  it("refuses the other Universe selection before any partial proof or history leaks", () => {
    const first = fixture("universe-one");
    expect(() => compare(first, "universe-two")).toThrow();
    const html = comparisonHtml(first, "universe-two");
    expect(html).toContain("Comparaison refusée");
    expect(html).not.toContain("Cause universe-one");
    expect(html).not.toContain("edge-1");
    expect(overviewHtml(first, "universe-two")).toContain("Projection de chronologie refusée");
  });

  it("refuses injected foreign anchor, edge or novel scene even with identical local IDs", () => {
    const local = fixture("universe-one");
    const foreign = fixture("universe-two");
    const injected: M32ChronologyProjection[] = [
      { ...local, anchors: [foreign.anchors[0], ...local.anchors.slice(1)] },
      { ...local, precedences: [
        { ...foreign.precedences[0], reason: "PRIVATE FOREIGN EDGE" },
        ...local.precedences.slice(1),
      ] },
      { ...local, narration: [
        { ...foreign.narration[0], scene_title: "PRIVATE FOREIGN SCENE" },
        ...local.narration.slice(1),
      ] },
    ];
    for (const bad of injected) {
      const before = JSON.stringify(bad);
      expect(() => compare(bad, "universe-one")).toThrow();
      const html = comparisonHtml(bad, "universe-one");
      expect(html).toContain("Comparaison refusée");
      expect(html).not.toContain("Cause universe-one");
      expect(html).not.toContain("PRIVATE FOREIGN EDGE");
      expect(html).not.toContain("PRIVATE FOREIGN SCENE");
      expect(overviewHtml(bad, "universe-one")).toContain("Projection de chronologie refusée");
      expect(JSON.stringify(bad)).toBe(before);
    }
  });

  it("refuses same-Universe duplicate identities instead of accepting homonyms as aliases", () => {
    const base = fixture("universe-one");
    const invalid: M32ChronologyProjection[] = [
      { ...base, anchors: [...base.anchors, { ...base.anchors[0] }] },
      { ...base, precedences: [...base.precedences, { ...base.precedences[0] }] },
      { ...base, narration: [...base.narration, { ...base.narration[0] }] },
      { ...base, precedences: [...base.precedences, {
        ...base.precedences[0], id: "second-id-same-live-endpoints",
      }] },
    ];
    for (const snapshot of invalid) {
      expect(() => compare(snapshot, "universe-one")).toThrow();
      expect(comparisonHtml(snapshot, "universe-one")).toContain("Comparaison refusée");
    }
  });

  it("does not infer chronology from four time kinds, cross-novel narration or source revision", () => {
    const original = fixture("universe-one");
    const originalBytes = JSON.stringify(original);
    for (const mode of ["exact", "approximate", "relative", "unknown"] as const) {
      const temporal: M32AnchorProjection = {
        ...original.anchors[0], time_kind: mode,
        calendar_name: mode === "exact" || mode === "approximate" ? "Autre calendrier" : null,
        fictional_label: mode === "exact" ? "Date inventée" : null,
        precision_text: mode === "approximate" ? "Période incertaine" : null,
        source_revision_id: "ancienne-revision-" + mode,
      };
      const snapshot: M32ChronologyProjection = {
        ...original,
        anchors: [temporal, ...original.anchors.slice(1)],
        narration: [...original.narration].reverse().map(scene => ({
          ...scene, chapter_order: 999, scene_order: 20,
          scene_title: "Après dans le livre, avant dans le récit",
        })),
      };
      const start = JSON.stringify(snapshot);
      expect(compare(snapshot, "universe-one")).toMatchObject({ relation: "before" });
      expect(compare(snapshot, "universe-one", "A", "D")).toMatchObject({
        relation: "incomparable", witness: [],
      });
      expect(compare(snapshot, "universe-one", "D", "D")).toMatchObject({
        relation: "same", witness: [],
      });
      expect(overviewHtml(snapshot, "universe-one")).toContain("Non renseigné");
      expect(JSON.stringify(snapshot)).toBe(start);
    }
    expect(JSON.stringify(original)).toBe(originalBytes);
  });

  it("does not turn an unauthored reader reveal into any invented chronological order", () => {
    const base = fixture("universe-one");
    const denied: M32ChronologyProjection = {
      ...base, reader_reveal_status: "published" as M32ChronologyProjection["reader_reveal_status"],
    };
    expect(() => compare(denied, "universe-one")).toThrow();
    expect(comparisonHtml(denied, "universe-one")).toContain("Comparaison refusée");
    expect(overviewHtml(denied, "universe-one")).toContain("Projection de chronologie refusée");
    expect(compare(base, "universe-one", "A", "D").relation).toBe("incomparable");
  });
});
