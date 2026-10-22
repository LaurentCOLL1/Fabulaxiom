import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import M32FictionalCorrectionHistory, {
  auditM32FictionalCorrectionChain,
  type M32FictionalCorrectionRow,
} from "./M32FictionalCorrectionHistory";

const world = "fabricated-one";
const successor: M32FictionalCorrectionRow = {
  id: "s1", universe_id: world, kind: "successor",
  prior_successor_id: null, prior_chain_id: null,
  before_anchor_id: "A", after_anchor_id: "B",
  reason: "human authored", revocation_id: "r1", revocation_reason: "withdrawn",
};
const chain1: M32FictionalCorrectionRow = {
  id: "c1", universe_id: world, kind: "chain",
  prior_successor_id: "s1", prior_chain_id: null,
  before_anchor_id: "B", after_anchor_id: "C",
  reason: "explicit edit", revocation_id: "r2", revocation_reason: "withdrawn again",
};
const chain2: M32FictionalCorrectionRow = {
  id: "c2", universe_id: world, kind: "chain",
  prior_successor_id: null, prior_chain_id: "c1",
  before_anchor_id: "C", after_anchor_id: "D",
  reason: "current edit", revocation_id: null, revocation_reason: null,
};
describe("M3.2 browser-only fictional correction history", () => {
  it("01 retains every authored correction and one currently active one", () => {
    const result = auditM32FictionalCorrectionChain(world, [chain2, successor, chain1]);
    expect(result.ordered_history.map(x => x.id)).toEqual(["s1", "c1", "c2"]);
    expect(result.active_id).toBe("c2");
    expect(result.editing_authorized).toBe(false);
    expect(result.real_g3_authorized).toBe(false);
    expect(result.data_origin).toBe("fictional_browser_memory_only");
  });
  it("02 allows explicitly withdrawn terminal with no remaining active correction", () => {
    const result = auditM32FictionalCorrectionChain(world, [
      successor, { ...chain1, revocation_id: "r2", revocation_reason: "human" },
    ]);
    expect(result.active_id).toBeNull();
    expect(result.ordered_history).toHaveLength(2);
  });
  it("03 rejects missing predecessor or non-retired predecessor", () => {
    expect(() => auditM32FictionalCorrectionChain(world, [
      successor, { ...chain1, prior_successor_id: "missing" },
    ])).toThrow();
    expect(() => auditM32FictionalCorrectionChain(world, [
      { ...successor, revocation_id: null, revocation_reason: null }, chain1,
    ])).toThrow();
  });
  it("04 rejects forks, duplicate IDs and missing root", () => {
    expect(() => auditM32FictionalCorrectionChain(world, [
      successor, chain1, { ...chain1, id: "c-branch", prior_successor_id: "s1" },
    ])).toThrow();
    expect(() => auditM32FictionalCorrectionChain(world, [successor, successor])).toThrow();
    expect(() => auditM32FictionalCorrectionChain(world, [chain1])).toThrow();
  });
  it("05 rejects cross-Universe, blank ID and unmatched revocation reason", () => {
    expect(() => auditM32FictionalCorrectionChain(world, [
      successor, { ...chain1, universe_id: "fabricated-two" },
    ])).toThrow();
    expect(() => auditM32FictionalCorrectionChain(world, [
      { ...successor, id: "  " },
    ])).toThrow();
    expect(() => auditM32FictionalCorrectionChain(world, [
      { ...successor, revocation_reason: null },
    ])).toThrow();
  });
  it("06 rejects wrong parent type, both parents, self-cycle", () => {
    expect(() => auditM32FictionalCorrectionChain(world, [
      successor, { ...chain1, prior_chain_id: "s1", prior_successor_id: null },
    ])).toThrow();
    expect(() => auditM32FictionalCorrectionChain(world, [
      successor, { ...chain1, prior_chain_id: "c1" },
    ])).toThrow();
    expect(() => auditM32FictionalCorrectionChain(world, [
      successor, { ...chain1, prior_successor_id: null, prior_chain_id: "c1" },
    ])).toThrow();
  });
  it("07 displays only synthetic immutable history in read-only markup", () => {
    const html = renderToStaticMarkup(createElement(M32FictionalCorrectionHistory, {
      expectedUniverseId: world, records: [successor, chain1, chain2],
    }));
    expect(html).toContain("Historique fictif des corrections chronologiques");
    expect(html).toContain("correction active");
    expect(html).toContain("correction retirée");
    expect(html).toContain("Corrige explicitement");
    expect(html).toContain("ancienne assertion");
    expect(html).toContain("Aucun ordre global déduit");
    expect(html).toContain("Aucun accès SQLite ni commande Tauri");
    expect(html).not.toContain("<button");
    expect(html).not.toContain("<input");
  });
  it("08 fails closed on invalid imported history and isolates empty world", () => {
    const bad = renderToStaticMarkup(createElement(M32FictionalCorrectionHistory, {
      expectedUniverseId: world,
      records: [successor, { ...chain1, universe_id: "foreign" }],
    }));
    expect(bad).toContain("Historique de corrections refusé");
    expect(bad).not.toContain("s1");
    expect(bad).not.toContain("ancienne assertion");
    expect(auditM32FictionalCorrectionChain("fabricated-two", []).active_id).toBeNull();
  });
});
