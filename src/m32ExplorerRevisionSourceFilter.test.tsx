import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import Explorer, {
  deriveM32Explorer, M32_EXPLORER_PAGE_SIZE,
} from "./M32SyntheticEventExplorer";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import type { M32ConsultationSelection } from "./M32ChronologyConsultation";

// P3aa: invented read-only projection; no App.tsx, SQLite, IPC, Tauri,
// network, real revision registry, Windows user profile or operator files.
function toy(): M32ChronologyProjection {
  const universe_id = "fiction-explorer";
  const anchor = (
    id: string, status: "current" | "revoked" | "superseded",
    source_revision_id: string | null, fictional_label: string | null = null,
  ) => ({
    id, universe_id, status, source_revision_id, fictional_label,
    time_kind: fictional_label === null ? "unknown" as const : "exact" as const,
    calendar_name: fictional_label === null ? null : "Invented calendar",
    precision_text: null,
  });
  return {
    universe_id, reader_reveal_status: "not_authored",
    anchors: [
      anchor("💠", "superseded", "shared-revision", "Même légende"),
      anchor("\uE000", "revoked", "shared-revision", "Même légende"),
      anchor("A", "current", "source-A"),
      anchor("B", "current", "source-B"),
      ...Array.from({ length: 10 }, (_, i) =>
        anchor("N" + String(i).padStart(2, "0"), "current", null)),
    ],
    precedences: [{
      id: "human-AB", universe_id, before_anchor_id: "A",
      after_anchor_id: "B", status: "current", reason: "Written by a human",
    }],
    narration: [{
      scene_id: "invented-scene", universe_id, novel_id: "invented-novel",
      novel_title: "Invented novel", chapter_id: "invented-chapter",
      chapter_title: "Invented chapter", chapter_order: 0, scene_order: 0,
      scene_title: "Invented scene",
    }],
  };
}
const empty: M32ConsultationSelection = {
  leftAnchorId: null, rightAnchorId: null,
};
function derive(
  revision = "", status: "all" | "current" | "historical" = "all",
  page = 0, selection = empty, query = "",
  source: M32ChronologyProjection = toy(),
) {
  return deriveM32Explorer(source, source.universe_id, selection,
    query, status, page, revision);
}
function view(s: M32ChronologyProjection = toy()): string {
  return renderToStaticMarkup(createElement(Explorer, {
    scenarioKey: "fiction", expectedUniverseId: s.universe_id, snapshot: s,
  }));
}

describe("M3.2 P3aa explicit fictional revision source filter", () => {
  it("filters two historical anchors only by exact revision source identity", () => {
    const m = derive("shared-revision");
    expect(m.rows.map(r => r.id)).toEqual(["\uE000", "💠"]);
    expect(m.source_revision_filter).toBe("shared-revision");
    expect(m.count).toBe(2);
    expect(m.can_write).toBe(false);
    expect(m.source_kind).toBe("invented_only");
  });
  it("keeps source IDs case-sensitive without inventing cross-revision aliases", () => {
    expect(derive("shared-Revision").count).toBe(0);
    expect(derive("shared-revision ").count).toBe(0);
    expect(derive("shared").count).toBe(0);
  });
  it("applies historical and current filters independently of revision search", () => {
    expect(derive("shared-revision", "historical").count).toBe(2);
    expect(derive("shared-revision", "current").count).toBe(0);
    expect(derive("source-A", "current").rows.map(r => r.id)).toEqual(["A"]);
  });
  it("does not use a fictional label as an exact source revision identity", () => {
    expect(derive("Même légende").count).toBe(0);
    expect(derive("", "historical", 0, empty, "même")).toMatchObject({
      count: 2,
    });
  });
  it("preserves selected witnesses when a separate revision filter hides both anchors", () => {
    const selection = { leftAnchorId: "A", rightAnchorId: "B" };
    const m = derive("shared-revision", "historical", 0, selection);
    expect(m.rows.map(r => r.id)).toEqual(["\uE000", "💠"]);
    expect(m.comparison?.relation).toBe("before");
    expect(m.comparison?.witness.map(w => w.precedence_id)).toEqual(["human-AB"]);
  });
  it("sorts all paginated IDs by Unicode scalar independently of insertion order", () => {
    const a = toy(), b = { ...a, anchors: [...a.anchors].reverse() };
    expect(M32_EXPLORER_PAGE_SIZE).toBe(8);
    expect(derive("", "all", 0, empty, "", a).count).toBe(14);
    const first = derive("", "all", 0, empty, "", a).rows.map(r => r.id);
    const last = derive("", "all", 1, empty, "", a).rows.map(r => r.id);
    expect(first).toEqual(["A", "B", "N00", "N01", "N02", "N03", "N04", "N05"]);
    expect(last).toEqual(["N06", "N07", "N08", "N09", "\uE000", "💠"]);
    expect(derive("", "all", 0, empty, "", b).rows.map(r => r.id)).toEqual(first);
    expect(derive("", "all", 1, empty, "", b).rows.map(r => r.id)).toEqual(last);
  });
  it("does not silently select an anchor or infer world time from ID ordering", () => {
    const result = derive();
    expect(result.comparison).toBeNull();
    const html = view();
    expect(html).toContain("aucun rattachement à une scène");
    expect(html).toContain("Choisissez les deux événements");
  });
  it("rejects malformed source revision query, overlong value or invalid type", () => {
    for (const value of ["bad-\uD800", "bad-\uDC00", "x".repeat(257),
      "   ", null, 23]) {
      expect(() => deriveM32Explorer(toy(), "fiction-explorer", empty,
        "", "all", 0, value as string)).toThrow(/refusé/);
    }
  });
  it("rejects a global cycle even when the exact revision filter would hide it", () => {
    const s = toy();
    s.precedences.push({
      id: "cycle", universe_id: s.universe_id,
      before_anchor_id: "B", after_anchor_id: "A",
      status: "current", reason: "Invalid contradiction",
    });
    expect(() => derive("shared-revision", "historical", 0, empty, "", s))
      .toThrow();
    expect(view(s)).toContain("Exploration refusée");
    expect(view(s)).not.toContain("Même légende");
  });
  it("refuses a foreign-Universe source before applying a hiding filter", () => {
    const s = toy();
    s.anchors[0].universe_id = "other-universe";
    expect(() => derive("source-A", "current", 0, empty, "", s)).toThrow();
    expect(view(s)).not.toContain("Même légende");
  });
  it("renders a labeled exact source filter without persistence controls", () => {
    const html = view();
    expect(html).toContain("Révision source fictive (identifiant exact)");
    expect(html).toContain('type="search"');
    expect(html).toContain("aucun rattachement à une scène");
    expect(html).not.toMatch(/<(form|textarea)\b/);
    expect(html).not.toContain("Sauvegarde réussie");
  });
  it("escapes a hostile fictional label and never mutates the original source", () => {
    const s = toy();
    s.anchors[2].time_kind = "exact";
    s.anchors[2].calendar_name = "Invented calendar";
    s.anchors[2].fictional_label = "<script>unsaved()</script>";
    const before = JSON.stringify(s);
    const html = view(s);
    expect(html).not.toContain("<script>");
    expect(html).toContain("&lt;script&gt;");
    expect(JSON.stringify(s)).toBe(before);
  });
});
