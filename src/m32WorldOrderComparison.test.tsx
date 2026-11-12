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
  anchors: [
    ...["A", "B", "C", "D", "E"].map(id => ({
      id, universe_id: "world-a", time_kind: "unknown" as const,
      status: "current" as const, calendar_name: null,
      fictional_label: null, precision_text: null, source_revision_id: null,
    })),
    { id: "past", universe_id: "world-a", time_kind: "unknown" as const,
      status: "revoked" as const, calendar_name: null,
      fictional_label: null, precision_text: null, source_revision_id: null },
  ],
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
  it("rejects 257-character selected IDs but permits exactly 256 in fictional data", () => {
    const limit = "x".repeat(256);
    const tooLong = limit + "x";
    const astral = "💠".repeat(256); // 256 code points, 512 UTF-16 units.
    const astralTooLong = astral + "💠";
    const withBoundary = { ...original, anchors: [
      ...original.anchors,
      { ...original.anchors[0], id: limit },
      { ...original.anchors[0], id: tooLong },
      { ...original.anchors[0], id: astral },
      { ...original.anchors[0], id: astralTooLong },
    ] };
    for (const valid of [limit, astral]) {
      expect(read(withBoundary, valid, "B")).toMatchObject({
        relation: "incomparable", witness: [],
      });
    }
    for (const [left, right] of [
      [tooLong, "B"], ["B", tooLong], [tooLong, tooLong],
      [astralTooLong, "B"], ["B", astralTooLong],
    ]) {
      expect(() => read(withBoundary, left, right))
        .toThrow("256 caractères maximum");
      const html = view(withBoundary, left, right);
      expect(html).toContain("Comparaison refusée");
      expect(html).not.toContain("Raison 1");
      expect(html).not.toContain(tooLong);
    }
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
  it("documents the stable ID tie-break despite insertion order and revoked shortcuts", () => {
    const edges = [
      addedEdge("A", "D", "z-route"), addedEdge("D", "C", "z-tail"),
      addedEdge("A", "B", "a-route"), addedEdge("B", "C", "a-tail"),
      { ...addedEdge("A", "C", "0-old-direct"), status: "revoked" as const },
    ];
    const first = { ...original, precedences: edges };
    const reversed = { ...first, precedences: [...edges].reverse() };
    const originalBytes = JSON.stringify(first);
    for (const fixture of [first, reversed]) {
      expect(read(fixture).witness.map(step => step.precedence_id))
        .toEqual(["a-route", "a-tail"]);
      expect(read(fixture).witness_selection_policy)
        .toBe("shortest_active_chain_then_edge_id");
      expect(view(fixture)).toContain("pas par ordre de saisie");
      expect(view(fixture)).not.toContain("0-old-direct");
      expect(view(fixture)).not.toMatch(/<(button|input|form|textarea)\b/);
    }
    expect(JSON.stringify(first)).toBe(originalBytes);
    const shorter = { ...first, precedences: [
      ...edges, addedEdge("A", "C", "zz-new-direct"),
    ] };
    expect(read(shorter).witness.map(step => step.precedence_id))
      .toEqual(["zz-new-direct"]);
    expect(read(original, "B", "B")).toMatchObject({
      relation: "same", witness: [],
      witness_selection_policy: "shortest_active_chain_then_edge_id",
    });
    expect(read(original, "D", "E")).toMatchObject({
      relation: "incomparable", witness: [],
      witness_selection_policy: "shortest_active_chain_then_edge_id",
    });
  });
  it("uses Unicode scalar order for equal-length synthetic witnesses", () => {
    const ascii = { ...original, precedences: [
      addedEdge("A", "D", "a-start"), addedEdge("D", "C", "a-end"),
      addedEdge("A", "B", "Z-start"), addedEdge("B", "C", "Z-end"),
    ] };
    // U+005A ('Z') precedes U+0061 ('a'), regardless of locale.
    for (const edges of [ascii.precedences, [...ascii.precedences].reverse()]) {
      expect(read({ ...ascii, precedences: edges }).witness.map(x => x.precedence_id))
        .toEqual(["Z-start", "Z-end"]);
    }
    const astral = { ...original, precedences: [
      addedEdge("A", "D", "💠-start"), addedEdge("D", "C", "💠-end"),
      addedEdge("A", "B", "\uE000-start"), addedEdge("B", "C", "\uE000-end"),
    ] };
    // U+E000 precedes U+1F4A0, unlike UTF-16 code-unit order.
    const revoked = { ...addedEdge("A", "C", "0-old-direct"), status: "revoked" as const };
    const fixture = { ...astral, precedences: [revoked, ...astral.precedences] };
    for (const edges of [fixture.precedences, [...fixture.precedences].reverse()]) {
      const result = read({ ...fixture, precedences: edges });
      expect(result.witness.map(x => x.precedence_id))
        .toEqual(["\uE000-start", "\uE000-end"]);
      expect(result.witness_selection_policy).toBe("shortest_active_chain_then_edge_id");
    }
    expect(view(fixture)).not.toContain("0-old-direct");
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
  it("exhaustively checks all five-event active DAGs against an independent path oracle", () => {
    // Five fictional events have ten possible before/after pairs and 2^10
    // acyclic subsets; no operator data, IPC, dates or persistence.
    const ids = ["A", "B", "C", "D", "E"];
    const pairs: { before: string; after: string }[] = [];
    for (let i = 0; i < ids.length; i += 1) {
      for (let j = i + 1; j < ids.length; j += 1) {
        pairs.push({ before: ids[i], after: ids[j] });
      }
    }
    expect(pairs).toHaveLength(10);
    const allEdges = pairs.map(({ before, after }, index) => ({
      ...addedEdge(before, after, "edge-" + String(index).padStart(2, "0")),
      reason: "Motif humain " + String(index),
    }));
    // Historical direct assertions must not become a shortcut.
    const historical = {
      ...addedEdge("A", "E", "historical-direct"),
      status: "revoked" as const,
    };

    // Intentionally independent of breadth-first search or sorting adjacency:
    // enumerate every A->E simple path, then choose fewest edges and
    // lexical edge IDs. The DAG structure makes recursion finite.
    function oracle(edges: typeof allEdges): string[] | null {
      const successors = new Map<string, typeof allEdges>();
      for (const edge of edges) {
        const previous = successors.get(edge.before_anchor_id) ?? [];
        successors.set(edge.before_anchor_id, [...previous, edge]);
      }
      const paths: string[][] = [];
      function enumerate(at: string, used: string[]): void {
        if (at === "E") {
          paths.push(used);
          return;
        }
        for (const edge of successors.get(at) ?? []) {
          enumerate(edge.after_anchor_id, [...used, edge.id]);
        }
      }
      enumerate("A", []);
      paths.sort((a, b) => {
        if (a.length !== b.length) return a.length - b.length;
        for (let i = 0; i < a.length; i += 1) {
          if (a[i] !== b[i]) return a[i] < b[i] ? -1 : 1;
        }
        return 0;
      });
      return paths[0] ?? null;
    }

    for (let mask = 0; mask < (1 << pairs.length); mask += 1) {
      const selected = allEdges.filter((_, i) => (mask & (1 << i)) !== 0);
      const expected = oracle(selected);
      for (const arranged of [selected, [...selected].reverse()]) {
        const fixture: M32ChronologyProjection = {
          ...original, precedences: [...arranged, historical],
        };
        const fixtureBytes = JSON.stringify(fixture);
        const forward = read(fixture, "A", "E");
        const backward = read(fixture, "E", "A");
        expect(forward.relation).toBe(expected ? "before" : "incomparable");
        expect(backward.relation).toBe(expected ? "after" : "incomparable");
        expect(forward.witness.map(step => step.precedence_id))
          .toEqual(expected ?? []);
        expect(backward.witness.map(step => step.precedence_id))
          .toEqual(expected ?? []);
        expect(forward.witness.map(step => step.human_reason))
          .toEqual(expected?.map(id => allEdges.find(e => e.id === id)!.reason) ?? []);
        expect(forward.witness_selection_policy)
          .toBe("shortest_active_chain_then_edge_id");
        expect(forward.data_origin).toBe("synthetic_in_memory_only");
        expect(forward.edit_controls_available).toBe(false);
        expect(JSON.stringify(fixture)).toBe(fixtureBytes);
        expect(forward.witness.map(step => step.precedence_id))
          .not.toContain("historical-direct");
      }
    }
  });

  it("exhaustively refuses cyclic four-vertex directed graphs, with no partial conclusion", () => {
    // 4 fictitious current anchors, 12 possible non-self directed arcs,
    // 2^12=4096 finite graphs, including cycles and contradictory directions.
    const names = ["A", "B", "C", "D"];
    const oriented = names.flatMap(before => names
      .filter(after => after !== before)
      .map(after => ({ before, after })));
    expect(oriented).toHaveLength(12);
    const all = oriented.map(({ before, after }) =>
      addedEdge(before, after, "arc-" + before + "-" + after));
    const retired = {
      ...addedEdge("C", "A", "revoked-shortcut"), status: "revoked" as const,
    };

    // Independent DFS oracle: recursion-stack cycle detection and reachability,
    // not the product's in-degree/toposort or breadth-first witness algorithm.
    function graphFrom(edges: typeof all): Map<string, string[]> {
      const graph = new Map<string, string[]>(names.map(n => [n, []]));
      for (const e of edges) graph.get(e.before_anchor_id)!.push(e.after_anchor_id);
      return graph;
    }
    function hasCycle(graph: ReadonlyMap<string, readonly string[]>): boolean {
      const entered = new Set<string>();
      const finished = new Set<string>();
      function visit(node: string): boolean {
        if (entered.has(node)) return true;
        if (finished.has(node)) return false;
        entered.add(node);
        for (const next of graph.get(node) ?? []) {
          if (visit(next)) return true;
        }
        entered.delete(node);
        finished.add(node);
        return false;
      }
      return names.some(name => visit(name));
    }
    function reaches(graph: ReadonlyMap<string, readonly string[]>,
      origin: string, destination: string): boolean {
      const visited = new Set<string>();
      const pending = [origin];
      while (pending.length) {
        const at = pending.pop()!;
        if (at === destination) return true;
        if (visited.has(at)) continue;
        visited.add(at);
        pending.push(...(graph.get(at) ?? []));
      }
      return false;
    }

    let cyclic = 0;
    let acyclic = 0;
    for (let mask = 0; mask < 1 << all.length; mask += 1) {
      const active = all.filter((_, i) => (mask & (1 << i)) !== 0);
      const graph = graphFrom(active);
      const cycle = hasCycle(graph);
      if (cycle) cyclic += 1;
      else acyclic += 1;
      const forward = reaches(graph, "A", "C");
      const backward = reaches(graph, "C", "A");
      for (const ordered of [active, [...active].reverse()]) {
        const fixture: M32ChronologyProjection = {
          ...original, precedences: [retired, ...ordered],
        };
        const before = JSON.stringify(fixture);
        if (cycle) {
          expect(() => read(fixture, "A", "C")).toThrow(/cycle/);
          // Fail closed even if the requested anchors are the same,
          // or an unrelated E is not part of this directed subgraph.
          expect(() => read(fixture, "E", "E")).toThrow(/cycle/);
          const html = view(fixture, "A", "C");
          expect(html).toContain("Comparaison refusée");
          expect(html).not.toContain("revoked-shortcut");
          expect(html).not.toMatch(/<(button|input|form|textarea)\b/);
        } else {
          expect(forward && backward).toBe(false);
          const left = read(fixture, "A", "C");
          const right = read(fixture, "C", "A");
          const relation = forward ? "before" : backward ? "after" : "incomparable";
          expect(left.relation).toBe(relation);
          expect(right.relation).toBe(
            relation === "before" ? "after" :
            relation === "after" ? "before" : "incomparable");
          expect(left.witness.every(step =>
            active.some(edge => edge.id === step.precedence_id))).toBe(true);
          expect(left.witness.map(step => step.precedence_id))
            .not.toContain("revoked-shortcut");
          expect(read(fixture, "E", "E")).toMatchObject({relation: "same", witness: []});
          expect(left.edit_controls_available).toBe(false);
          expect(left.data_origin).toBe("synthetic_in_memory_only");
        }
        expect(JSON.stringify(fixture)).toBe(before);
      }
    }
    expect(cyclic + acyclic).toBe(4096);
    expect(cyclic).toBeGreaterThan(0);
    expect(acyclic).toBeGreaterThan(0);
  }, 30000);

});
