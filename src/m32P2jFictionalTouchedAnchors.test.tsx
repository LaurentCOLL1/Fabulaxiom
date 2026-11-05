import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32P2jFictionalTouchedAnchors, {
  previewP2jFictionalTouchedAnchors,
} from "./M32P2jFictionalTouchedAnchors";
import type { P2iFictionalEdge, P2iFictionalInput } from "./M32P2iFictionalImpactReview";

const universe = "fiction-p2j-world";
function edge(id: string, from: string, to: string): P2iFictionalEdge {
  return { id, universe_id: universe, before_anchor_id: from, after_anchor_id: to, origin: "original" };
}
const input: P2iFictionalInput = {
  data_origin: "fictional_browser_memory_only",
  production_writer_admitted: false,
  real_g3_authorized: false,
  universe_id: universe,
  active_before: [edge("removed", "A", "B"), edge("same", "A", "C")],
  active_after: [edge("same", "A", "C"), edge("added", "B", "D")],
};
describe("M3.2 P2j fictional touched-anchor projection (isolated and read-only)", () => {
  it("01 lists only endpoints of changed assertions with direct before/after flags", () => {
    const before = JSON.stringify(input);
    const result = previewP2jFictionalTouchedAnchors(input, universe);
    expect(result.anchors).toEqual([
      { anchor_id: "A", in_removed: true, in_added: false },
      { anchor_id: "B", in_removed: true, in_added: true },
      { anchor_id: "D", in_removed: false, in_added: true },
    ]);
    expect(result.production_writer_admitted).toBe(false);
    expect(result.real_g3_authorized).toBe(false);
    expect(JSON.stringify(input)).toBe(before);
  });
  it("02 unchanged edges do not create touched anchors; identical snapshots give empty result", () => {
    const same = { ...input, active_after: input.active_before };
    expect(previewP2jFictionalTouchedAnchors(same, universe).anchors).toEqual([]);
  });
  it("03 a reused assertion ID with changed endpoints affects both old and new anchors", () => {
    const changed = {
      ...input,
      active_before: [edge("reused", "A", "B")],
      active_after: [edge("reused", "B", "C")],
    };
    expect(previewP2jFictionalTouchedAnchors(changed, universe).anchors).toEqual([
      { anchor_id: "A", in_removed: true, in_added: false },
      { anchor_id: "B", in_removed: true, in_added: true },
      { anchor_id: "C", in_removed: false, in_added: true },
    ]);
  });
  it("04 fails closed on forged source or foreign universe and does not display anchor IDs", () => {
    expect(() => previewP2jFictionalTouchedAnchors(input, "other-world")).toThrow();
    const forged = { ...input, production_writer_admitted: true } as unknown as P2iFictionalInput;
    expect(() => previewP2jFictionalTouchedAnchors(forged, universe)).toThrow();
    const html = renderToStaticMarkup(createElement(M32P2jFictionalTouchedAnchors, {
      input: forged, expectedUniverse: universe,
    }));
    expect(html).toContain("Ancres fictives refusées");
    expect(html).not.toContain("<li");
  });
  it("05 fails closed on cycles and self-links inherited from P2i", () => {
    const cyclic = { ...input, active_after: [edge("x", "A", "B"), edge("y", "B", "A")] };
    const self = { ...input, active_after: [edge("x", "A", "A")] };
    expect(() => previewP2jFictionalTouchedAnchors(cyclic, universe)).toThrow();
    expect(() => previewP2jFictionalTouchedAnchors(self, universe)).toThrow();
  });
  it("06 renders three accessible read-only categories and escapes fictional labels", () => {
    const html = renderToStaticMarkup(createElement(M32P2jFictionalTouchedAnchors, {
      input, expectedUniverse: universe,
    }));
    expect(html).toContain("Relations retirées uniquement (1)");
    expect(html).toContain("Relations ajoutées uniquement (1)");
    expect(html).toContain("Relations retirées et ajoutées (1)");
    expect(html).toContain("sans déduction de date");
    expect(html).toContain("STOP_UNAVAILABLE");
    expect(html).not.toContain("<button");
    expect(html).not.toContain("<input");
    const malicious = { ...input, active_before: [edge("<img src=x onerror=alert(1)>", "A", "B")], active_after: [] };
    const escaped = renderToStaticMarkup(createElement(M32P2jFictionalTouchedAnchors, {
      input: malicious, expectedUniverse: universe,
    }));
    expect(escaped).toContain("&lt;img");
    expect(escaped).not.toContain("<img");
  });
});
