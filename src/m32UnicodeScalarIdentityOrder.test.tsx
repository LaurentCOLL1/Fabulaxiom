import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32ChronologyPreview, {
  compareM32IdentityScalars, decodeM32ChronologyProjection,
  type M32ChronologyProjection,
} from "./M32ChronologyPreview";
import M32ChronologyConsultation, {
  EMPTY_M32_CONSULTATION_SELECTION, inspectM32Consultation,
} from "./M32ChronologyConsultation";
import { compareM32WorldOrder } from "./M32WorldOrderComparison";

// All fixtures are invented; no App.tsx, IPC, local files, SQLite, or writer.
function toy(): M32ChronologyProjection {
  const universe_id = "fiction-scalar";
  const anchor = (id: string) => ({
    id, universe_id, time_kind: "unknown" as const,
    status: "current" as const, calendar_name: null, fictional_label: null,
    precision_text: null, source_revision_id: null,
  });
  const edge = (id: string, target: string) => ({
    id, universe_id, before_anchor_id: "A", after_anchor_id: target,
    status: "revoked" as const, reason: "invented retired reason",
  });
  const scene = (scene_id: string, novel_id: string, scene_title: string) => ({
    scene_id, universe_id, novel_id, novel_title: "Invented novel",
    chapter_id: "chapter", chapter_title: "Invented chapter",
    chapter_order: 0, scene_order: 0, scene_title,
  });
  return { universe_id, reader_reveal_status: "not_authored",
    anchors: [anchor("💠"), anchor("\uE000"), anchor("A")],
    precedences: [edge("💠", "💠"), edge("\uE000", "\uE000")],
    narration: [
      scene("💠", "💠", "ASTRAL_NOVEL"),
      scene("\uE000", "\uE000", "BMP_NOVEL"),
      scene("same💠", "same", "ASTRAL_SCENE"),
      scene("same\uE000", "same", "BMP_SCENE"),
    ] };
}
function preview(s: M32ChronologyProjection): string {
  return renderToStaticMarkup(createElement(M32ChronologyPreview, {
    expectedUniverseId: s.universe_id, snapshot: s,
  }));
}
function consultation(s: M32ChronologyProjection): string {
  return renderToStaticMarkup(createElement(M32ChronologyConsultation, {
    expectedUniverseId: s.universe_id, snapshot: s,
    selection: EMPTY_M32_CONSULTATION_SELECTION, onSelectionChange: () => {},
  }));
}
describe("M3.2 P3z fictional deterministic Unicode scalar display IDs", () => {
  it("orders U+E000 before astral U+1F4A0 without locale collation", () => {
    expect(compareM32IdentityScalars("\uE000", "💠")).toBe(-1);
    expect(compareM32IdentityScalars("💠", "\uE000")).toBe(1);
    expect(compareM32IdentityScalars("💠", "💠")).toBe(0);
  });
  it("orders prefixes and refuses to equate distinct NFC and NFD identifiers", () => {
    expect(compareM32IdentityScalars("A", "A💠")).toBe(-1);
    expect(compareM32IdentityScalars("A\uE000", "A💠")).toBe(-1);
    expect(compareM32IdentityScalars("e\u0301", "\u00E9")).toBe(-1);
    expect(compareM32IdentityScalars("\u00E9", "e\u0301")).toBe(1);
  });
  it("sorts fictional anchor identity without implying world time", () => {
    const html = preview(toy());
    expect(html.indexOf("<strong>A</strong>"))
      .toBeLessThan(html.indexOf("<strong>\uE000</strong>"));
    expect(html.indexOf("<strong>\uE000</strong>"))
      .toBeLessThan(html.indexOf("<strong>💠</strong>"));
    expect(html).toContain("sans inventer une chronologie");
  });
  it("sorts read-only consultation selection by the same scalar rule", () => {
    const s = toy(), m = inspectM32Consultation(s, s.universe_id,
      EMPTY_M32_CONSULTATION_SELECTION);
    expect(m.options.map(x => x.id)).toEqual(["A", "\uE000", "💠"]);
    expect(m.comparison).toBeNull();
    const html = consultation(s);
    expect(html.indexOf('value="A"')).toBeLessThan(html.indexOf('value="\uE000"'));
    expect(html.indexOf('value="\uE000"')).toBeLessThan(html.indexOf('value="💠"'));
  });
  it("sorts revoked precedence identity without making it active", () => {
    const html = preview(toy());
    const first = html.indexOf("<strong>A</strong> avant <strong>\uE000</strong>");
    const second = html.indexOf("<strong>A</strong> avant <strong>💠</strong>");
    expect(first).toBeGreaterThan(-1);
    expect(second).toBeGreaterThan(first);
    expect(html).toContain("Révoquée (historique)");
  });
  it("sorts novels and tied within-novel scene IDs by scalars", () => {
    const html = preview(toy());
    expect(html.indexOf("BMP_NOVEL")).toBeLessThan(html.indexOf("ASTRAL_NOVEL"));
    expect(html.indexOf("BMP_SCENE")).toBeLessThan(html.indexOf("ASTRAL_SCENE"));
    expect(html).toContain("Aucun ordre global entre romans");
    expect(html).toContain("Ordre de révélation au lecteur");
  });
  it("makes read-only rendering independent of source array insertion order", () => {
    const s = toy(), before = JSON.stringify(s);
    const other = { ...s, anchors: [...s.anchors].reverse(),
      precedences: [...s.precedences].reverse(), narration: [...s.narration].reverse() };
    expect(preview(s)).toBe(preview(other));
    expect(consultation(s)).toBe(consultation(other));
    expect(JSON.stringify(s)).toBe(before);
  });
  it("preserves directed human witness instead of identity-derived chronology", () => {
    const s = toy();
    s.precedences = [{
      ...s.precedences[0], status: "current",
      before_anchor_id: "A", after_anchor_id: "💠",
    }];
    const v = compareM32WorldOrder(s, s.universe_id, "A", "💠");
    expect(v.relation).toBe("before");
    expect(v.witness.map(x => x.precedence_id)).toEqual(["💠"]);
    expect(v.data_origin).toBe("synthetic_in_memory_only");
    expect(v.edit_controls_available).toBe(false);
  });
  it("refuses a malformed historical ID before any identity ordering appears", () => {
    const s = toy();
    s.anchors.push({ ...s.anchors[0], id: "bad-\uD800", status: "revoked" });
    expect(() => decodeM32ChronologyProjection(s, s.universe_id))
      .toThrow(/Unicode non scalaire/);
    expect(preview(s)).toContain("Projection de chronologie refusée");
    expect(consultation(s)).toContain("Consultation refusée");
    expect(preview(s)).not.toContain("invented retired reason");
  });
});
