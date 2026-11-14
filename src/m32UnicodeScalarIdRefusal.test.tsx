import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32WorldOrderComparison, { compareM32WorldOrder } from "./M32WorldOrderComparison";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";

// P3x: invented fixture only, not App.tsx, real SQLite, Windows profile, IPC or writer.
function toy(universe = "invented-universe"): M32ChronologyProjection {
  const anchor = (id: string) => ({
    id, universe_id: universe, status: "current" as const,
    time_kind: "unknown" as const, calendar_name: null, fictional_label: null,
    precision_text: null, source_revision_id: null as string | null,
  });
  return { universe_id: universe, anchors: [anchor("A"), anchor("B")],
    precedences: [{ id: "edge", universe_id: universe,
      before_anchor_id: "A", after_anchor_id: "B", status: "current",
      reason: "SECRET_FICTIONAL_REASON" }], narration: [],
    reader_reveal_status: "not_authored" };
}
function assertRefused(snapshot: M32ChronologyProjection,
  left = "A", right = "B"): void {
  const before = JSON.stringify(snapshot);
  expect(() => compareM32WorldOrder(snapshot, snapshot.universe_id, left, right))
    .toThrow(/Unicode non scalaire/);
  const html = renderToStaticMarkup(createElement(M32WorldOrderComparison, {
    expectedUniverseId: snapshot.universe_id, snapshot,
    leftAnchorId: left, rightAnchorId: right,
  }));
  expect(html).toContain("Comparaison refusée");
  expect(html).toContain("Aucune conclusion affichée");
  expect(html).not.toContain("SECRET_FICTIONAL_REASON");
  expect(html).not.toMatch(/<(button|input|form|textarea)\b/i);
  expect(JSON.stringify(snapshot)).toBe(before);
}
describe("M3.2 P3x Unicode scalar IDs on invented unmounted comparison", () => {
  it("refuses a lone high surrogate in a selected anchor", () => {
    const s = toy(), bad = "A\uD800";
    s.anchors[0].id = bad; s.precedences[0].before_anchor_id = bad;
    assertRefused(s, bad, "B");
  });
  it("refuses a lone low surrogate in a selected anchor", () => {
    const s = toy(), bad = "B\uDC00";
    s.anchors[1].id = bad; s.precedences[0].after_anchor_id = bad;
    assertRefused(s, "A", bad);
  });
  it("refuses malformed active precedence identity", () => {
    const s = toy(); s.precedences[0].id = "edge-\uD800"; assertRefused(s);
  });
  it("refuses malformed historic precedence identity even with valid current proof", () => {
    const s = toy();
    s.precedences.push({ ...s.precedences[0], id: "historic-\uDC00", status: "revoked" });
    assertRefused(s);
  });
  it("refuses malformed source revision identity without leaking current justification", () => {
    const s = toy(); s.anchors[0].source_revision_id = "revision-\uD800";
    assertRefused(s);
  });
  it("refuses malformed narration scene identity without creating a timeline", () => {
    const s = toy();
    s.narration.push({ scene_id: "scene-\uDC00", universe_id: s.universe_id,
      novel_id: "novel", novel_title: "Imaginary novel",
      chapter_id: "chapter", chapter_title: "Imaginary chapter",
      scene_title: "Imaginary scene", chapter_order: 0, scene_order: 0 });
    assertRefused(s);
  });
  it("refuses a malformed Universe identifier", () => {
    const s = toy("universe-\uD800"); assertRefused(s);
  });
  it("accepts astral Unicode pair and escapes hostile authored HTML reason", () => {
    const s = toy(), valid = "A💠";
    s.anchors[0].id = valid; s.precedences[0].before_anchor_id = valid;
    s.precedences[0].reason = "<img src=x onerror=alert(1)>";
    const before = JSON.stringify(s);
    const value = compareM32WorldOrder(s, s.universe_id, valid, "B");
    expect(value.relation).toBe("before");
    expect(value.witness.map(e => e.precedence_id)).toEqual(["edge"]);
    expect(value.data_origin).toBe("synthetic_in_memory_only");
    expect(value.edit_controls_available).toBe(false);
    const html = renderToStaticMarkup(createElement(M32WorldOrderComparison, {
      expectedUniverseId: s.universe_id, snapshot: s, leftAnchorId: valid,
      rightAnchorId: "B",
    }));
    expect(html).toContain("&lt;img");
    expect(html).not.toContain("<img ");
    expect(html).not.toMatch(/<(button|input|form|textarea)\b/i);
    expect(JSON.stringify(s)).toBe(before);
  });
  it("allows 256 well-formed astral scalars and refuses 257", () => {
    const s = toy(), valid = "💠".repeat(256);
    s.anchors[0].id = valid; s.precedences[0].before_anchor_id = valid;
    expect(compareM32WorldOrder(s, s.universe_id, valid, "B").relation).toBe("before");
    expect(() => compareM32WorldOrder(s, s.universe_id, "💠".repeat(257), "B"))
      .toThrow(/256 caractères maximum/);
  });
});
