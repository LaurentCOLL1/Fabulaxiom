import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32WorldOrderComparison, {
  compareM32WorldOrder,
} from "./M32WorldOrderComparison";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";

const original: M32ChronologyProjection = {
  universe_id: "world-a",
  reader_reveal_status: "not_authored",
  anchors: ["A", "B", "C", "D", "E"].map(id => ({
    id, universe_id: "world-a", time_kind: "unknown" as const,
    status: "current" as const, calendar_name: null,
    fictional_label: null, precision_text: null, source_revision_id: null,
  })).concat([
    { id: "past", universe_id: "world-a", time_kind: "unknown" as const,
      status: "revoked" as const, calendar_name: null,
      fictional_label: null, precision_text: null, source_revision_id: null },
  ]),
  precedences: [
    { id: "human-1", universe_id: "world-a", before_anchor_id: "A",
      after_anchor_id: "B", status: "current", reason: "Raison 1" },
    { id: "human-2", universe_id: "world-a", before_anchor_id: "B",
      after_anchor_id: "C", status: "current", reason: "Raison 2" },
    { id: "history-only", universe_id: "world-a", before_anchor_id: "A",
      after_anchor_id: "D", status: "revoked", reason: "Ancienne raison" },
  ],
  narration: [],
};
function read(snapshot: M32ChronologyProjection = original, left="A", right="C") {
  return compareM32WorldOrder(snapshot, "world-a", left, right);
}
function view(snapshot: M32ChronologyProjection | null = original, left="A",
  right="C", universe="world-a"): string {
  return renderToStaticMarkup(createElement(M32WorldOrderComparison, {
    expectedUniverseId: universe, snapshot,
    leftAnchorId: left, rightAnchorId: right,
  }));
}
const addedEdge = (before: string, after: string, id: string) => ({
  id, universe_id: "world-a", before_anchor_id: before, after_anchor_id: after,
  status: "current" as const, reason: "Motif inventé",
});

describe("M3.2 invented world-order comparison, no production source", () => {
  it("proves direct before with exact authored edge identity", () => {
    const v = read(original, "A", "B");
    expect(v.relation).toBe("before");
    expect(v.witness.map(x => x.precedence_id)).toEqual(["human-1"]);
  });
  it("proves transitive before with a human edge-by-edge witness", () => {
    const v = read();
    expect(v.relation).toBe("before");
    expect(v.witness.map(x => x.precedence_id)).toEqual(["human-1", "human-2"]);
    expect(v.witness.map(x => x.human_reason)).toEqual(["Raison 1", "Raison 2"]);
  });
  it("returns after with the witness still oriented before to after", () => {
    const v = read(original, "C", "A");
    expect(v.relation).toBe("after");
    expect(v.witness[0].before_anchor_id).toBe("A");
    expect(v.witness[1].after_anchor_id).toBe("C");
  });
  it("identical current ID returns same without invented precedence", () => {
    expect(read(original, "B", "B")).toMatchObject({ relation: "same", witness: [] });
  });
  it("declares disconnected events incomparable, never false calendar order", () => {
    expect(read(original, "C", "E")).toMatchObject({
      relation: "incomparable", witness: [],
    });
  });
  it("never promotes a revoked old edge into the current graph", () => {
    expect(read(original, "A", "D").relation).toBe("incomparable");
  });
  it("never compares a revoked source ID, including with itself", () => {
    expect(() => read(original, "past", "past")).toThrow();
    expect(() => read(original, "A", "past")).toThrow();
  });
  it("refuses a relation labeled current that points at historical source", () => {
    const bad = { ...original, precedences: [...original.precedences,
      addedEdge("past", "A", "broken")],
    };
    expect(() => read(bad)).toThrow();
  });
  it("refuses a cycle involving the selected pair", () => {
    const bad = { ...original, precedences: [...original.precedences,
      addedEdge("C", "A", "cycle")],
    };
    expect(() => read(bad)).toThrow(/cycle/);
  });
  it("refuses an unrelated active cycle, rather than exposing partial proof", () => {
    const bad = { ...original, precedences: [...original.precedences,
      addedEdge("D", "E", "de"), addedEdge("E", "D", "ed")],
    };
    expect(() => read(bad)).toThrow(/cycle/);
  });
  it("refuses duplicated active endpoint pairs with different edge IDs", () => {
    const bad = { ...original, precedences: [...original.precedences,
      addedEdge("A", "B", "another-id")],
    };
    expect(() => read(bad)).toThrow(/doublonnée/);
  });
  it("refuses dangling, foreign Universe and self edges through base decoder", () => {
    for (const edge of [
      { ...original.precedences[0], after_anchor_id: "absent" },
      { ...original.precedences[0], universe_id: "world-b" },
      { ...original.precedences[0], after_anchor_id: "A" },
    ]) {
      expect(() => read({ ...original, precedences: [edge] })).toThrow();
    }
  });
  it("refuses a selection not present, blank, or from another Universe", () => {
    expect(() => read(original, "absent", "B")).toThrow();
    expect(() => read(original, "", "B")).toThrow();
    expect(() => compareM32WorldOrder(original, "world-b", "A", "B")).toThrow();
  });
  it("does not treat fictional labels, identity sort or narration as order", () => {
    const altered: M32ChronologyProjection = {
      ...original,
      anchors: original.anchors.map(a => a.id === "D" ? {
        ...a, time_kind: "exact", fictional_label: "Première cloche",
        calendar_name: "Une année inventée",
      } : a),
      narration: [{ scene_id: "scene-1", universe_id: "world-a", novel_id: "novel",
        novel_title: "Livre", chapter_id: "chapter", chapter_title: "Chapitre",
        chapter_order: 0, scene_order: 0, scene_title: "Scène A" }],
    };
    expect(read(altered, "D", "C").relation).toBe("incomparable");
  });
  it("chooses the shortest stable witness rather than inferred complete ranking", () => {
    const extra = { ...original, precedences: [
      ...original.precedences,
      addedEdge("A", "C", "human-direct"),
    ] };
    expect(read(extra).witness.map(x => x.precedence_id)).toEqual(["human-direct"]);
  });
  it("uses stable edge IDs for equal-length alternative witnesses", () => {
    const extra = { ...original, precedences: [
      addedEdge("A", "D", "z-edge"), addedEdge("D", "C", "z-end"),
      addedEdge("A", "B", "a-edge"), addedEdge("B", "C", "a-end"),
    ] };
    expect(read(extra).witness.map(x => x.precedence_id)).toEqual(["a-edge", "a-end"]);
  });
  it("displays the authored justification chain and read-only status", () => {
    const html = view();
    expect(html).toContain("Avant : précédence humaine");
    expect(html).toContain("human-1");
    expect(html).toContain("human-2");
    expect(html).toContain("Raison 1");
    expect(html).toContain("Raison 2");
    expect(html).not.toMatch(/<(button|input|form|textarea)\b/);
  });
  it("displays explicit incomparable state with no fictional witness", () => {
    const html = view(original, "D", "E");
    expect(html).toContain("Ordre indéterminé");
    expect(html).toContain("Aucune chaîne de précédences");
    expect(html).not.toContain("Raison 1");
  });
  it("empty view never tries an application fallback", () => {
    expect(view(null)).toContain("aucune donnée synthétique fournie");
  });
  it("invalid view refuses without leaking historical reasons", () => {
    const v = view(original, "past", "B");
    expect(v).toContain("Comparaison refusée");
    expect(v).not.toContain("Raison 1");
  });
  it("escapes script-like human authored reason text", () => {
    const bad = { ...original, precedences: original.precedences.map(e => ({
      ...e, reason: "<script>bad()</script>",
    })) };
    const html = view(bad);
    expect(html).not.toContain("<script>");
    expect(html).toContain("&lt;script&gt;");
  });
  it("never mutates the submitted synthetic snapshot or its arrays", () => {
    const before = JSON.stringify(original);
    read();
    view();
    expect(JSON.stringify(original)).toBe(before);
  });
  it("explicitly denies edit controls and real-data provenance on outputs", () => {
    const v = read();
    expect(v.edit_controls_available).toBe(false);
    expect(v.data_origin).toBe("synthetic_in_memory_only");
  });
  it("can compare 512 invented anchors with no invented edge ordering", () => {
    const fixture = {
      ...original,
      anchors: Array.from({ length: 512 }, (_, i) => ({
        ...original.anchors[0], id: "fiction-" + String(i),
      })),
      precedences: [],
    };
    expect(read(fixture, "fiction-0", "fiction-511").relation).toBe("incomparable");
  });
});
