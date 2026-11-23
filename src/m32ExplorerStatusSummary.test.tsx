import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import Explorer, { deriveM32Explorer } from "./M32SyntheticEventExplorer";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import type { M32ConsultationSelection } from "./M32ChronologyConsultation";

/** P3bt fictional-only distribution; never runtime admission or source read. */
const selection: M32ConsultationSelection = {
  leftAnchorId: null, rightAnchorId: null,
};
function fixture(): M32ChronologyProjection {
  const universe_id = "fiction-p3bt";
  const anchor = (id: string, status: "current" | "revoked" | "superseded",
                  source_revision_id: string | null, fictional_label: string) => ({
    id, universe_id, status, source_revision_id, fictional_label,
    time_kind: "exact" as const, calendar_name: "Calendrier fictif",
    precision_text: null,
  });
  return {
    universe_id, reader_reveal_status: "not_authored",
    anchors: [
      anchor("A", "current", "r2", "Départ"),
      anchor("B", "current", "r2", "Arrivée"),
      anchor("old-rev", "revoked", "r1", "Ancien départ"),
      anchor("old-rev-2", "revoked", null, "<script>fake()</script>"),
      anchor("old-sup", "superseded", "r1", "Arrivée précédente"),
    ],
    precedences: [{
      id: "human-AB", universe_id, before_anchor_id: "A",
      after_anchor_id: "B", status: "current", reason: "Décision humaine",
    }],
    narration: [],
  };
}
function derive(source: M32ChronologyProjection, query = "",
                status: "all" | "current" | "historical" | "revoked" | "superseded" = "all",
                page = 0, revision = "") {
  return deriveM32Explorer(source, source.universe_id, selection, query, status,
                           page, revision);
}
describe("M3.2 P3bt fictional status summary", () => {
  it("counts every validated anchor once in its distinct status", () => {
    const view = derive(fixture());
    expect(view.status_counts).toEqual({
      current: 2, revoked: 2, superseded: 1, total: 5,
    });
    expect(view.count).toBe(5);
    expect(view.source_kind).toBe("invented_only");
    expect(view.can_write).toBe(false);
  });
  it("keeps global counts independent of status, query, revision and pagination", () => {
    const f = fixture(), baseline = derive(f).status_counts;
    expect(derive(f, "", "revoked").count).toBe(2);
    expect(derive(f, "", "superseded").count).toBe(1);
    expect(derive(f, "", "current").count).toBe(2);
    expect(derive(f, "old", "revoked", 17, "r1").count).toBe(1);
    expect(derive(f, "old", "revoked", 17, "r1").page).toBe(0);
    for (const view of [derive(f, "", "current"), derive(f, "old", "revoked", 17, "r1"),
                        derive(f, "none", "superseded"), derive(f, "", "historical")])
      expect(view.status_counts).toEqual(baseline);
  });
  it("rejects a hidden active cycle before exposing even global counters", () => {
    const f = fixture();
    f.precedences.push({
      id: "cycle", universe_id: f.universe_id, before_anchor_id: "B",
      after_anchor_id: "A", status: "current", reason: "Contradiction",
    });
    expect(() => derive(f, "", "revoked")).toThrow();
    const html = renderToStaticMarkup(createElement(Explorer, {
      scenarioKey: "p3bt-cycle", expectedUniverseId: f.universe_id, snapshot: f,
    }));
    expect(html).toContain("Exploration refusée");
    expect(html).not.toContain("assertions fictives validées");
  });
  it("does not count an anchor from a foreign universe", () => {
    const f = fixture(); f.anchors[0].universe_id = "other-universe";
    expect(() => derive(f, "", "historical")).toThrow();
  });
  it("renders accessible status counts with escaped labels, no write or mutation", () => {
    const f = fixture(), before = JSON.stringify(f);
    const html = renderToStaticMarkup(createElement(Explorer, {
      scenarioKey: "p3bt-fictive", expectedUniverseId: f.universe_id, snapshot: f,
    }));
    expect(html).toContain('aria-label="Répartition des statuts de l’univers fictif"');
    expect(html).toContain("5 assertions fictives validées");
    expect(html).toContain("2 en vigueur");
    expect(html).toContain("2 révoquées");
    expect(html).toContain("1 remplacées");
    expect(html).toContain("&lt;script&gt;fake()");
    expect(html).not.toContain("<script>fake()</script>");
    expect(html).not.toContain("Sauvegarde réussie");
    expect(JSON.stringify(f)).toBe(before);
  });
});
