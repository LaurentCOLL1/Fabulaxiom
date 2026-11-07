import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32P2kFictionalAnchorEvidence, {
  previewP2kFictionalAnchorEvidence,
} from "./M32P2kFictionalAnchorEvidence";
import type { P2iFictionalEdge, P2iFictionalInput } from "./M32P2iFictionalImpactReview";

const world = "fiction-p2k-direct";
function edge(id: string, from: string, to: string,
  origin: P2iFictionalEdge["origin"] = "original"): P2iFictionalEdge {
  return { id, universe_id: world, before_anchor_id: from, after_anchor_id: to, origin };
}
const input: P2iFictionalInput = {
  data_origin: "fictional_browser_memory_only",
  production_writer_admitted: false,
  real_g3_authorized: false,
  universe_id: world,
  active_before: [edge("removed", "A", "B"), edge("same", "A", "C"),
                  edge("remote", "X", "Y")],
  active_after: [edge("same", "A", "C"), edge("remote", "X", "Y"),
                 edge("added", "B", "D", "restatement")],
};

describe("M3.2 P2k fictional direct evidence per touched anchor", () => {
  it("01 shows only direct removed and added assertions for one touched anchor", () => {
    const unchanged = JSON.stringify(input);
    const result = previewP2kFictionalAnchorEvidence(input, world, "B");
    expect(result.anchor_id).toBe("B");
    expect(result.removed.map(e => e.id)).toEqual(["removed"]);
    expect(result.added.map(e => e.id)).toEqual(["added"]);
    expect(result.production_writer_admitted).toBe(false);
    expect(result.real_g3_authorized).toBe(false);
    expect(JSON.stringify(input)).toBe(unchanged);
  });
  it("02 excludes unchanged-only and unknown anchors rather than disclosing them", () => {
    expect(() => previewP2kFictionalAnchorEvidence(input, world, "C")).toThrow();
    expect(() => previewP2kFictionalAnchorEvidence(input, world, "X")).toThrow();
    expect(() => previewP2kFictionalAnchorEvidence(input, world, "missing")).toThrow();
    expect(() => previewP2kFictionalAnchorEvidence(input, world, "")).toThrow();
  });
  it("03 treats an assertion ID reused with different endpoints as two direct changes", () => {
    const changed = { ...input,
      active_before: [edge("reuse", "A", "B")],
      active_after: [edge("reuse", "B", "C", "restatement")],
    };
    const result = previewP2kFictionalAnchorEvidence(changed, world, "B");
    expect(result.removed.map(e => e.before_anchor_id)).toEqual(["A"]);
    expect(result.added.map(e => e.after_anchor_id)).toEqual(["C"]);
  });
  it("04 lexically sorts full direct evidence without implying transitive impact", () => {
    const unsorted = { ...input,
      active_before: [edge("z", "A", "B"), edge("a", "A", "B")],
      active_after: [edge("added", "B", "C")],
    };
    const result = previewP2kFictionalAnchorEvidence(unsorted, world, "B");
    expect(result.removed.map(e => e.id)).toEqual(["a", "z"]);
    expect(result.added.map(e => e.id)).toEqual(["added"]);
    expect(result.removed.every(e => e.after_anchor_id === "B")).toBe(true);
  });
  it("05 rejects forged origin, operator writer flag, or a foreign universe", () => {
    expect(() => previewP2kFictionalAnchorEvidence(input, "foreign", "B")).toThrow();
    expect(() => previewP2kFictionalAnchorEvidence({
      ...input, data_origin: "operator_disk",
    } as unknown as P2iFictionalInput, world, "B")).toThrow();
    expect(() => previewP2kFictionalAnchorEvidence({
      ...input, production_writer_admitted: true,
    } as unknown as P2iFictionalInput, world, "B")).toThrow();
  });
  it("06 inherits cycle, self-link and duplicated-assertion refusal", () => {
    expect(() => previewP2kFictionalAnchorEvidence({
      ...input, active_after: [edge("a", "A", "B"), edge("b", "B", "A")],
    }, world, "B")).toThrow();
    expect(() => previewP2kFictionalAnchorEvidence({
      ...input, active_before: [edge("a", "A", "A")],
    }, world, "A")).toThrow();
    expect(() => previewP2kFictionalAnchorEvidence({
      ...input, active_before: [edge("a", "A", "B"), edge("a", "A", "B")],
    }, world, "B")).toThrow();
  });
  it("07 renders accessible escaped, read-only evidence and fails closed without leaking IDs", () => {
    const html = renderToStaticMarkup(createElement(M32P2kFictionalAnchorEvidence,
      { input, expectedUniverse: world, selectedAnchor: "B" }));
    expect(html).toContain("Relations directement retirées (1)");
    expect(html).toContain("Relations directement ajoutées (1)");
    expect(html).toContain("sans"); // No authority to derive a total world order
    expect(html).toContain("G3 STOP_UNAVAILABLE");
    expect(html).not.toContain("<button");
    expect(html).not.toContain("<input");
    const malicious = "<img src=x onerror=alert(1)>";
    const invented = { ...input,
      active_before: [edge("evil", malicious, "B")],
      active_after: [],
    };
    const escaped = renderToStaticMarkup(createElement(M32P2kFictionalAnchorEvidence,
      { input: invented, expectedUniverse: world, selectedAnchor: malicious }));
    expect(escaped).toContain("&lt;img");
    expect(escaped).not.toContain("<img");
    const forged = { ...input, real_g3_authorized: true } as unknown as P2iFictionalInput;
    const denied = renderToStaticMarkup(createElement(M32P2kFictionalAnchorEvidence,
      { input: forged, expectedUniverse: world, selectedAnchor: "B" }));
    expect(denied).toContain("Preuves fictives refusées");
    expect(denied).not.toContain("removed");
    expect(denied).not.toContain("<li");
  });
});
