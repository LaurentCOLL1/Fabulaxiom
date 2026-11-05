import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import M32P2iFictionalImpactReview, {
  previewP2iFictionalImpact,
  type P2iFictionalInput,
  type P2iFictionalEdge,
} from "./M32P2iFictionalImpactReview";

const world = "fiction-p2i-world";
function edge(id: string, from: string, to: string,
              origin: P2iFictionalEdge["origin"] = "original"): P2iFictionalEdge {
  return { id, universe_id: world, before_anchor_id: from, after_anchor_id: to, origin };
}
const initial: P2iFictionalInput = {
  data_origin: "fictional_browser_memory_only",
  production_writer_admitted: false,
  real_g3_authorized: false,
  universe_id: world,
  active_before: [edge("old12", "A", "B"), edge("edge13", "A", "C")],
  active_after: [edge("edge13", "A", "C"), edge("new21", "B", "A", "restatement")],
};
describe("M3.2 P2i fictional author-facing impact panel (test-only)", () => {
  it("01 groups removed, added and unchanged without modifying either list", () => {
    const before = JSON.stringify(initial);
    const impact = previewP2iFictionalImpact(initial, world);
    expect(impact.removed.map(x => x.id)).toEqual(["old12"]);
    expect(impact.added.map(x => x.id)).toEqual(["new21"]);
    expect(impact.unchanged.map(x => x.id)).toEqual(["edge13"]);
    expect(impact.production_writer_admitted).toBe(false);
    expect(impact.real_g3_authorized).toBe(false);
    expect(JSON.stringify(initial)).toBe(before);
  });
  it("02 full edge comparison treats reused ID with reversed endpoints as changed", () => {
    const changed = {
      ...initial,
      active_before: [edge("same", "A", "B")],
      active_after: [edge("same", "B", "A", "restatement")],
    };
    const impact = previewP2iFictionalImpact(changed, world);
    expect(impact.removed).toHaveLength(1);
    expect(impact.added).toHaveLength(1);
    expect(impact.unchanged).toEqual([]);
  });
  it("03 refuses foreign universe and forged provenance or writer authorization", () => {
    expect(() => previewP2iFictionalImpact(initial, "foreign")).toThrow();
    expect(() => previewP2iFictionalImpact({
      ...initial, active_after: [edge("foreign", "A", "B"), {
        ...edge("x", "B", "C"), universe_id: "foreign",
      }],
    }, world)).toThrow();
    expect(() => previewP2iFictionalImpact({
      ...initial, production_writer_admitted: true,
    } as unknown as P2iFictionalInput, world)).toThrow();
    expect(() => previewP2iFictionalImpact({
      ...initial, data_origin: "operator_disk",
    } as unknown as P2iFictionalInput, world)).toThrow();
  });
  it("04 fails closed on cycles, self-links and duplicated assertions", () => {
    expect(() => previewP2iFictionalImpact({
      ...initial, active_after: [edge("x", "A", "B"), edge("y", "B", "A")],
    }, world)).toThrow();
    expect(() => previewP2iFictionalImpact({
      ...initial, active_after: [edge("x", "A", "A")],
    }, world)).toThrow();
    expect(() => previewP2iFictionalImpact({
      ...initial, active_after: [edge("x", "A", "B"), edge("x", "A", "B")],
    }, world)).toThrow();
  });
  it("05 renders three separate read-only groups without any real action", () => {
    const html = renderToStaticMarkup(createElement(M32P2iFictionalImpactReview, {
      input: initial, expectedUniverse: world,
    }));
    expect(html).toContain("Impact fictif de la correction");
    expect(html).toContain("Relations retirées (1)");
    expect(html).toContain("Relations ajoutées (1)");
    expect(html).toContain("Relations inchangées (1)");
    expect(html).toContain("new21");
    expect(html).toContain("aucune commande Tauri");
    expect(html).toContain("STOP_UNAVAILABLE");
    expect(html).not.toContain("<button");
    expect(html).not.toContain("<input");
  });
  it("06 rejects tampering visibly without leaking purported operator data", () => {
    const html = renderToStaticMarkup(createElement(M32P2iFictionalImpactReview, {
      input: { ...initial, real_g3_authorized: true } as unknown as P2iFictionalInput,
      expectedUniverse: world,
    }));
    expect(html).toContain("Aperçu fictif refusé");
    expect(html).not.toContain("new21");
    expect(html).not.toContain("<button");
  });
  it("07 escapes user-supplied invented labels and never parses HTML", () => {
    const malicious = {
      ...initial,
      active_before: [edge("<img src=x onerror=alert(1)>", "A", "B")],
      active_after: [],
    };
    const html = renderToStaticMarkup(createElement(M32P2iFictionalImpactReview, {
      input: malicious, expectedUniverse: world,
    }));
    expect(html).toContain("&lt;img");
    expect(html).not.toContain("<img");
    expect(html).not.toContain("<button");
  });
});
