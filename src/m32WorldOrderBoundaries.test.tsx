import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32WorldOrderComparison, { compareM32WorldOrder } from "./M32WorldOrderComparison";
import type {
  M32ChronologyProjection, M32PrecedenceProjection,
} from "./M32ChronologyPreview";

// Synthetic stress envelope only. Does not mount App.tsx, open SQLite,
// contact a server, touch a Windows profile or authorize writer semantics.
const universe = "fictional-bounded-universe";
const anchors = Array.from({ length: 512 }, (_, i) => ({
  id: "node-" + i, universe_id: universe, time_kind: "unknown" as const,
  status: "current" as const, calendar_name: null, fictional_label: null,
  precision_text: null, source_revision_id: null,
}));
function edgesAtCap(): M32PrecedenceProjection[] {
  const result: M32PrecedenceProjection[] = [];
  for (let i = 0; i < 512 && result.length < 2048; i += 1) {
    for (let j = i + 1; j < 512 && result.length < 2048; j += 1) {
      result.push({
        id: `edge-${i}-${j}`, universe_id: universe,
        before_anchor_id: "node-" + i, after_anchor_id: "node-" + j,
        status: "current", reason: "Human reason " + i + " -> " + j,
      });
    }
  }
  return result;
}
function snapshot(
  precedences: M32PrecedenceProjection[] = edgesAtCap(),
): M32ChronologyProjection {
  return { universe_id: universe, anchors, precedences,
    narration: [], reader_reveal_status: "not_authored" };
}
function read(v: M32ChronologyProjection, a = "node-0", b = "node-511") {
  return compareM32WorldOrder(v, universe, a, b);
}
function html(v: M32ChronologyProjection, a = "node-0", b = "node-511") {
  return renderToStaticMarkup(createElement(M32WorldOrderComparison, {
    expectedUniverseId: universe, snapshot: v, leftAnchorId: a,
    rightAnchorId: b,
  }));
}

describe("M3.2 P3w bounded fictional graph and global refusal contracts", () => {
  it("accepts the exact 512-anchor/2048-edge limit and stable shortest witness", () => {
    const edges = edgesAtCap();
    expect(anchors).toHaveLength(512);
    expect(edges).toHaveLength(2048);
    const cases = [snapshot(edges), snapshot([...edges].reverse())];
    for (const v of cases) {
      const before = JSON.stringify(v);
      const result = read(v);
      expect(result).toMatchObject({
        relation: "before", data_origin: "synthetic_in_memory_only",
        edit_controls_available: false,
        witness_selection_policy: "shortest_active_chain_then_edge_id",
      });
      expect(result.witness.map(step => step.precedence_id)).toEqual(["edge-0-511"]);
      expect(result.witness[0].human_reason).toBe("Human reason 0 -> 511");
      expect(read(v, "node-511", "node-0").relation).toBe("after");
      expect(read(v, "node-511", "node-511")).toMatchObject({
        relation: "same", witness: [],
      });
      expect(JSON.stringify(v)).toBe(before);
    }
  });

  it("refuses 2049 relations even when overflow is only historical", () => {
    const edges = edgesAtCap();
    const historical: M32PrecedenceProjection = {
      id: "history-overflow", universe_id: universe,
      before_anchor_id: "node-511", after_anchor_id: "node-0",
      status: "revoked", reason: "SECRET HISTORICAL OVERFLOW",
    };
    const v = snapshot([...edges, historical]);
    const before = JSON.stringify(v);
    expect(v.precedences).toHaveLength(2049);
    expect(() => read(v)).toThrow(/volume synthétique excessif/);
    const markup = html(v);
    expect(markup).toContain("Comparaison refusée");
    expect(markup).not.toContain("SECRET HISTORICAL OVERFLOW");
    expect(markup).not.toContain("Human reason");
    expect(markup).not.toMatch(/<(button|input|textarea|form)\b/);
    expect(JSON.stringify(v)).toBe(before);
  });

  it("refuses 513 anchors or 2049 narration entries with no partial display", () => {
    const scenes = Array.from({ length: 2049 }, (_, i) => ({
      scene_id: "scene-" + i, universe_id: universe, novel_id: "novel-" + (i % 2),
      novel_title: "Fictional novel", chapter_id: "chapter-" + (i % 4),
      chapter_title: "Fictional chapter", chapter_order: i,
      scene_order: 0, scene_title: "PRIVATE SCENE " + i,
    }));
    const overAnchors = { ...snapshot([]), anchors: [
      ...anchors, { ...anchors[0], id: "node-512" },
    ] };
    const overNarration = { ...snapshot([]), narration: scenes };
    for (const v of [overAnchors, overNarration]) {
      const before = JSON.stringify(v);
      expect(() => read(v, "node-0", "node-0")).toThrow(/volume synthétique excessif/);
      const markup = html(v);
      expect(markup).toContain("Comparaison refusée");
      expect(markup).not.toContain("PRIVATE SCENE");
      expect(markup).not.toMatch(/<(button|input|textarea|form)\b/);
      expect(JSON.stringify(v)).toBe(before);
    }
  });

  it("fails closed on a cycle anywhere in the full allowed graph, even for same-ID", () => {
    const edges = edgesAtCap();
    // edge-0-511 already exists; swapping one valid edge creates a back-edge.
    const cycleEdge: M32PrecedenceProjection = {
      id: "cycle-back", universe_id: universe,
      before_anchor_id: "node-511", after_anchor_id: "node-0",
      status: "current", reason: "SECRET CYCLE",
    };
    const v = snapshot([...edges.slice(0, -1), cycleEdge]);
    const before = JSON.stringify(v);
    expect(v.precedences).toHaveLength(2048);
    expect(() => read(v)).toThrow(/cycle/);
    expect(() => read(v, "node-250", "node-250")).toThrow(/cycle/);
    const markup = html(v);
    expect(markup).toContain("Comparaison refusée");
    expect(markup).not.toContain("SECRET CYCLE");
    expect(markup).not.toContain("Human reason");
    expect(JSON.stringify(v)).toBe(before);
  });

  it("ignores a revoked back-edge at the exact relation cap without changing history", () => {
    const edges = edgesAtCap();
    const revoked: M32PrecedenceProjection = {
      id: "retired-back", universe_id: universe,
      before_anchor_id: "node-511", after_anchor_id: "node-0",
      status: "revoked", reason: "HISTORICAL ONLY",
    };
    const v = snapshot([...edges.slice(0, -1), revoked]);
    const before = JSON.stringify(v);
    expect(read(v).relation).toBe("before");
    expect(read(v).witness.map(step => step.precedence_id)).toEqual(["edge-0-511"]);
    expect(read(v, "node-511", "node-0").relation).toBe("after");
    expect(read(v).witness.map(step => step.precedence_id)).not.toContain("retired-back");
    expect(JSON.stringify(v)).toBe(before);
  });
});
