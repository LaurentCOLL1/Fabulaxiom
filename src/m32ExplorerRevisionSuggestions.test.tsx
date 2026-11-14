import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import Explorer, { deriveM32Explorer } from "./M32SyntheticEventExplorer";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";

function toy(): M32ChronologyProjection {
  const universe_id = "invented-revision-choices";
  const anchor = (id: string, status: "current" | "revoked" | "superseded",
    source_revision_id: string | null) => ({
    id, universe_id, status, source_revision_id, time_kind: "unknown" as const,
    calendar_name: null, fictional_label: null, precision_text: null,
  });
  return {
    universe_id, reader_reveal_status: "not_authored",
    anchors: [
      anchor("A", "current", "shared"),
      anchor("B", "revoked", "shared"),
      anchor("C", "superseded", "\uE000"),
      anchor("D", "current", "💠"),
      anchor("E", "current", null),
      anchor("F", "current", "shared"),
    ],
    precedences: [{
      id: "human-AD", universe_id, before_anchor_id: "A",
      after_anchor_id: "D", status: "current", reason: "Fictional human order",
    }],
    narration: [],
  };
}
const empty = { leftAnchorId: null, rightAnchorId: null };
function derive(source: M32ChronologyProjection = toy(), revision = "",
  query = "", status: "all" | "current" | "historical" = "all",
  page = 0, selection = empty) {
  return deriveM32Explorer(source, source.universe_id, selection,
    query, status, page, revision);
}
function html(source: M32ChronologyProjection = toy()) {
  return renderToStaticMarkup(createElement(Explorer, {
    scenarioKey: "invented", expectedUniverseId: source.universe_id, snapshot: source,
  }));
}
describe("M3.2 P3ab fictional revision source suggestions", () => {
  it("lists distinct nonnull IDs with truthful counts and scalar ordering", () => {
    expect(derive().revision_choices).toEqual([
      { id: "shared", anchor_count: 3, historical_count: 1 },
      { id: "\uE000", anchor_count: 1, historical_count: 1 },
      { id: "💠", anchor_count: 1, historical_count: 0 },
    ]);
  });
  it("does not change with insertion order, filters, or pagination", () => {
    const s = toy();
    const expected = derive(s).revision_choices;
    expect(derive({ ...s, anchors: [...s.anchors].reverse() }).revision_choices)
      .toEqual(expected);
    expect(derive(s, "shared", "no match", "historical", 17).revision_choices)
      .toEqual(expected);
    expect(derive(s, "shared", "", "historical").count).toBe(1);
    expect(derive(s, "shared", "", "current").count).toBe(2);
  });
  it("preserves case-sensitive exact IDs rather than promoting text matches", () => {
    expect(derive(toy(), "Shared").count).toBe(0);
    expect(derive(toy(), "shar").count).toBe(0);
    expect(derive(toy(), "shared").count).toBe(3);
  });
  it("keeps NFC and NFD identities separate", () => {
    const s = toy();
    s.anchors[2].source_revision_id = "e\u0301";
    s.anchors[3].source_revision_id = "é";
    expect(derive(s, "é").count).toBe(1);
    expect(derive(s, "e\u0301").count).toBe(1);
    expect(derive(s).revision_choices.map(v => v.id)).toEqual(["e\u0301", "shared", "é"]);
  });
  it("does not suggest a source ID too long for the input", () => {
    const s = toy();
    s.anchors[3].source_revision_id = "z".repeat(257);
    expect(derive(s).revision_choices.map(v => v.id)).toEqual(["shared", "\uE000"]);
    expect(derive(s).count).toBe(6);
  });
  it("preserves explicit witness selection even when only history is visible", () => {
    const selection = { leftAnchorId: "A", rightAnchorId: "D" };
    const v = derive(toy(), "\uE000", "", "historical", 0, selection);
    expect(v.rows.map(r => r.id)).toEqual(["C"]);
    expect(v.comparison?.relation).toBe("before");
    expect(v.comparison?.witness.map(w => w.precedence_id)).toEqual(["human-AD"]);
  });
  it("fails closed before suggestions for mixed Universe", () => {
    const s = toy(); s.anchors[0].universe_id = "foreign";
    expect(() => derive(s)).toThrow();
    expect(html(s)).toContain("Exploration refusée");
    expect(html(s)).not.toContain("<datalist");
  });
  it("fails closed for a surrogate in an historical source ID", () => {
    const s = toy(); s.anchors[1].source_revision_id = "bad-\uD800";
    expect(() => derive(s)).toThrow();
    expect(html(s)).not.toContain("<datalist");
  });
  it("escapes hostile source IDs in a datalist without mutating input", () => {
    const s = toy();
    s.anchors[3].source_revision_id = "<script>unsafe()</script>";
    const before = JSON.stringify(s), markup = html(s);
    expect(markup).toContain("<datalist");
    expect(markup).toContain("revision-suggestions");
    expect(markup).toContain("&lt;script&gt;");
    expect(markup).not.toContain("<script>");
    expect(JSON.stringify(s)).toBe(before);
  });
  it("disclaims provenance and exposes no persistence controls", () => {
    const v = derive();
    expect(v.source_kind).toBe("invented_only");
    expect(v.can_write).toBe(false);
    const markup = html();
    expect(markup).toContain("aucune preuve d’appartenance à un roman ou une scène");
    expect(markup).not.toMatch(/<(form|textarea)\b/);
    expect(markup).not.toContain("Sauvegarde réussie");
  });
});
