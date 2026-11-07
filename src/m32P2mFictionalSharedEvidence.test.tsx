import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32P2mFictionalSharedEvidence, {
  previewP2mFictionalSharedEvidence,
} from "./M32P2mFictionalSharedEvidence";
import type {
  P2iFictionalEdge, P2iFictionalInput,
} from "./M32P2iFictionalImpactReview";

const universe = "p2m-invented-world";
function edge(
  id: string, before: string, after: string,
  origin: P2iFictionalEdge["origin"] = "original",
): P2iFictionalEdge {
  return { id, universe_id: universe,
    before_anchor_id: before, after_anchor_id: after, origin };
}
const input: P2iFictionalInput = {
  data_origin: "fictional_browser_memory_only",
  production_writer_admitted: false,
  real_g3_authorized: false,
  universe_id: universe,
  active_before: [
    edge("shared-removed", "A", "B"), edge("first-removed", "A", "C"),
    edge("second-removed", "D", "B"), edge("stable", "E", "F"),
  ],
  active_after: [
    edge("shared-added", "B", "A", "restatement"), edge("first-added", "G", "A"),
    edge("second-added", "B", "H"), edge("stable", "E", "F"),
  ],
};

describe("M3.2 P2m two fictional anchor shared direct-only witnesses", () => {
  it("01 returns the shared changed assertions once and preserves input", () => {
    const unchanged = JSON.stringify(input);
    const result = previewP2mFictionalSharedEvidence(input, universe, "A", "B");
    expect(result.shared.map(w => w.edge.id).sort()).toEqual(["shared-added", "shared-removed"]);
    expect(result.shared.every(w => w.touches_first && w.touches_second)).toBe(true);
    expect(result.shared.length).toBe(2);
    expect(result.data_origin).toBe("fictional_browser_memory_only");
    expect(result.production_writer_admitted).toBe(false);
    expect(result.real_g3_authorized).toBe(false);
    expect(JSON.stringify(input)).toBe(unchanged);
  });
  it("02 partitions only direct changes, never stable or remote assertions", () => {
    const result = previewP2mFictionalSharedEvidence(input, universe, "A", "B");
    expect(result.first_only.map(w => w.edge.id).sort()).toEqual([
      "first-added", "first-removed",
    ]);
    expect(result.second_only.map(w => w.edge.id).sort()).toEqual([
      "second-added", "second-removed",
    ]);
    const all = [...result.shared, ...result.first_only, ...result.second_only];
    expect(all).toHaveLength(6);
    expect(all.some(w => w.edge.id === "stable")).toBe(false);
    expect(new Set(all.map(w => JSON.stringify([
      w.change, w.edge.id, w.edge.before_anchor_id, w.edge.after_anchor_id, w.edge.origin,
    ]))).size).toBe(6);
  });
  it("03 preserves removal/addition distinctions even with reused assertion IDs", () => {
    const changed = {
      ...input,
      active_before: [edge("reuse", "A", "B")],
      active_after: [edge("reuse", "B", "A", "restatement")],
    };
    const result = previewP2mFictionalSharedEvidence(changed, universe, "A", "B");
    expect(result.shared.map(w => w.change)).toEqual(["added", "removed"]);
    expect(result.shared.every(w => w.edge.id === "reuse")).toBe(true);
  });
  it("04 allows shared or exclusive empty categories without fabricating an edge", () => {
    const changed = {
      ...input,
      active_before: [edge("left", "A", "C"), edge("right", "B", "D")],
      active_after: [],
    };
    const result = previewP2mFictionalSharedEvidence(changed, universe, "A", "B");
    expect(result.shared).toEqual([]);
    expect(result.first_only.map(w => w.edge.id)).toEqual(["left"]);
    expect(result.second_only.map(w => w.edge.id)).toEqual(["right"]);
  });
  it("05 refuses equal, blank, unchanged-only or unknown selections", () => {
    for (const [first, second] of [
      ["A", "A"], ["A", ""], ["", "B"], ["A", "E"], ["B", "unknown"],
    ]) {
      expect(() => previewP2mFictionalSharedEvidence(
        input, universe, first, second,
      )).toThrow();
    }
  });
  it("06 inherits origin, permission, universe and graph validation refusals", () => {
    expect(() => previewP2mFictionalSharedEvidence(input, "foreign", "A", "B")).toThrow();
    for (const patch of [
      { data_origin: "operator_disk" }, { production_writer_admitted: true },
      { real_g3_authorized: true },
      { active_after: [edge("cycle1", "A", "B"), edge("cycle2", "B", "A")] },
      { active_before: [edge("self", "A", "A")] },
      { active_before: [edge("dup", "A", "B"), edge("dup", "A", "B")] },
    ]) {
      expect(() => previewP2mFictionalSharedEvidence({
        ...input, ...patch,
      } as unknown as P2iFictionalInput, universe, "A", "B")).toThrow();
    }
  });
  it("07 renders three accessible groups, one shared entry per assertion, no actions", () => {
    const html = renderToStaticMarkup(createElement(M32P2mFictionalSharedEvidence,
      { input, expectedUniverse: universe, firstAnchor: "A", secondAnchor: "B" }));
    expect(html).toContain("Assertions communes aux deux ancres (2)");
    expect(html).toContain("Assertions propres à la première ancre (2)");
    expect(html).toContain("Assertions propres à la seconde ancre (2)");
    expect(html).toContain("aucune transitivité, date");
    expect(html).toContain("G3 STOP_UNAVAILABLE");
    expect(html).not.toContain("<button");
    expect(html).not.toContain("<input");
    expect((html.match(/shared-removed/g) ?? []).length).toBe(1);
  });
  it("08 HTML-escapes invented malicious labels and fails closed with no leak", () => {
    const evil = "<img src=x onerror=alert(1)>";
    const invented = { ...input,
      active_before: [edge(evil, evil, "B")], active_after: [],
    };
    const escaped = renderToStaticMarkup(createElement(M32P2mFictionalSharedEvidence,
      { input: invented, expectedUniverse: universe, firstAnchor: evil, secondAnchor: "B" }));
    expect(escaped).toContain("&lt;img");
    expect(escaped).not.toContain("<img");
    const bad = { ...invented,
      production_writer_admitted: true,
    } as unknown as P2iFictionalInput;
    const refused = renderToStaticMarkup(createElement(M32P2mFictionalSharedEvidence,
      { input: bad, expectedUniverse: universe, firstAnchor: evil, secondAnchor: "B" }));
    expect(refused).toContain("Comparaison fictive refusée");
    expect(refused).not.toContain(evil);
    expect(refused).not.toContain("<li");
  });
});
