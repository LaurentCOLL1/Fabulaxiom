import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import Explorer, {
  deriveM32Explorer, M32_EXPLORER_PAGE_SIZE,
} from "./M32SyntheticEventExplorer";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import type { M32ConsultationSelection } from "./M32ChronologyConsultation";

const invented: M32ChronologyProjection = {
  universe_id: "fiction",
  reader_reveal_status: "not_authored",
  anchors: [
    ...Array.from({ length: 21 }, (_, i) => ({
      id: "N" + String(i + 1).padStart(2, "0"), universe_id: "fiction",
      time_kind: "unknown" as const, status: "current" as const,
      calendar_name: null, fictional_label: null, precision_text: null,
      source_revision_id: null,
    })),
    { id: "old", universe_id: "fiction", time_kind: "exact",
      status: "superseded", calendar_name: "Fiction",
      fictional_label: "La Vague", precision_text: null, source_revision_id: "fiction-r1" },
    { id: "same-name", universe_id: "fiction", time_kind: "exact",
      status: "current", calendar_name: "Fiction",
      fictional_label: "La Vague", precision_text: null, source_revision_id: "fiction-r2" },
  ],
  precedences: [
    { id: "e1", universe_id: "fiction", before_anchor_id: "N01",
      after_anchor_id: "N02", status: "current", reason: "L'auteur l'a indiqué" },
    { id: "e2", universe_id: "fiction", before_anchor_id: "N02",
      after_anchor_id: "N03", status: "current", reason: "La scène continue" },
    { id: "old-edge", universe_id: "fiction", before_anchor_id: "N01",
      after_anchor_id: "old", status: "revoked", reason: "Correction ancienne" },
  ],
  narration: [],
};
const empty: M32ConsultationSelection = { leftAnchorId: null, rightAnchorId: null };
function derive(query = "", status: "all" | "current" | "historical" = "all",
  page = 0, selection = empty, data: M32ChronologyProjection | null = invented) {
  return deriveM32Explorer(data, "fiction", selection, query, status, page);
}
function html(data: M32ChronologyProjection | null = invented) {
  return renderToStaticMarkup(createElement(Explorer, {
    scenarioKey: "toy", expectedUniverseId: "fiction", snapshot: data,
  }));
}

describe("M3.2 bounded fictional event explorer, isolated read-only", () => {
  it("sets the visible page size to eight", () => {
    expect(M32_EXPLORER_PAGE_SIZE).toBe(8);
    expect(derive().rows).toHaveLength(8);
  });
  it("counts all original events without rewriting world ordering", () => {
    expect(derive().count).toBe(23);
    expect(derive().pageCount).toBe(3);
    expect(derive().rows[0].id).toBe("N01");
  });
  it("paginates deterministically over stable IDs", () => {
    expect(derive("", "all", 1).rows[0].id).toBe("N09");
    expect(derive("", "all", 2).rows.at(-1)?.id).toBe("same-name");
  });
  it("clamps the presentation page without discarding selected sources", () => {
    const a = derive("N02", "all", 2, { leftAnchorId: "N01", rightAnchorId: "N03" });
    expect(a.page).toBe(0);
    expect(a.comparison?.relation).toBe("before");
    expect(a.comparison?.witness.map(w => w.precedence_id)).toEqual(["e1", "e2"]);
  });
  it("filters case-insensitively by ID with whitespace normalization", () => {
    expect(derive("  n03  ").rows.map(r => r.id)).toEqual(["N03"]);
  });
  it("searches fictional labels without attempting a calendar sort", () => {
    expect(derive(" vague ").rows.map(r => r.id)).toEqual(["old", "same-name"]);
  });
  it("distinguishes historical from current versions sharing one title", () => {
    expect(derive("vague", "current").rows.map(r => r.id)).toEqual(["same-name"]);
    expect(derive("vague", "historical").rows.map(r => r.id)).toEqual(["old"]);
  });
  it("never returns retired rows in the current-only filter", () => {
    expect(derive("", "current").count).toBe(22);
  });
  it("never returns active rows in historical filter", () => {
    expect(derive("", "historical").count).toBe(1);
  });
  it("reports no match without silently selecting another source", () => {
    expect(derive("missing").count).toBe(0);
    expect(derive("missing").pageCount).toBe(1);
    expect(derive("missing").rows).toEqual([]);
  });
  it("rejects invalid search, enum and page values", () => {
    expect(() => deriveM32Explorer(invented, "fiction", empty, "x".repeat(161), "all", 0)).toThrow();
    expect(() => deriveM32Explorer(invented, "fiction", empty, "", "__proto__" as never, 0)).toThrow();
    expect(() => derive("", "all", -1)).toThrow();
    expect(() => derive("", "all", 0.5)).toThrow();
  });
  it("validates full-world graph before applying a hiding filter", () => {
    const bad = { ...invented, precedences: [...invented.precedences,
      { id: "cycle", universe_id: "fiction", before_anchor_id: "N03",
        after_anchor_id: "N01", status: "current" as const, reason: "contradiction" }],
    };
    expect(() => derive("same-name", "historical", 0, empty, bad)).toThrow();
    expect(html(bad)).toContain("Exploration refusée");
    expect(html(bad)).not.toContain("La Vague");
  });
  it("rejects stale historical selected IDs even when filtered out", () => {
    expect(() => derive("", "current", 0,
      { leftAnchorId: "old", rightAnchorId: null })).toThrow();
  });
  it("preserves original graph/array identities, including retired edges", () => {
    const before = JSON.stringify(invented);
    derive("N03");
    html();
    expect(JSON.stringify(invented)).toBe(before);
  });
  it("renders accessible native search and status select", () => {
    const markup = html();
    expect(markup).toContain('type="search"');
    expect(markup).toContain("Filtrer les événements");
    expect(markup).toContain("Filtre de statut");
    expect(markup).toContain('aria-label="Pagination des événements fictifs"');
  });
  it("distinguishes browsing controls from underlying domain writes", () => {
    const markup = html();
    expect(markup).toContain("Choisir N01 comme premier événement");
    expect(markup).toContain("Choisir N01 comme deuxième événement");
    expect(markup).not.toContain("invoke(");
  });
  it("does not allow choosing a historical row", () => {
    const markup = html();
    expect(markup).not.toContain("Choisir old comme premier événement");
    expect(markup).not.toContain("Choisir old comme deuxième événement");
  });
  it("holds no hidden comparison or fabricated witness until explicit selection", () => {
    expect(derive().comparison).toBeNull();
    const markup = html();
    expect(markup).not.toContain("Chaîne de précédence sélectionnée");
  });
  it("escapes script-like fictional titles in the browser output", () => {
    const bad = { ...invented, anchors: invented.anchors.map(a =>
      a.id === "same-name" ? { ...a, fictional_label: "<script>fake()</script>" } : a),
    };
    const output = html(bad);
    expect(output).not.toContain("<script>fake()");
    expect(output).toContain("&lt;script&gt;fake()");
  });
  it("refuses foreign Universes before rendering filtered assertions", () => {
    expect(() => deriveM32Explorer(invented, "foreign", empty, "", "all", 0)).toThrow();
  });
  it("does not claim an authenticated source or write permission", () => {
    expect(derive().source_kind).toBe("invented_only");
    expect(derive().can_write).toBe(false);
  });
  it("returns no current/event data for explicitly absent snapshot", () => {
    expect(derive("", "all", 0, empty, null).count).toBe(0);
    expect(html(null)).toContain("aucune donnée fournie");
  });
});
