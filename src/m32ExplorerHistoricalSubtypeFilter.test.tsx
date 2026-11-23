import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import Explorer, {
  deriveM32Explorer, type M32ExplorerFilter,
} from "./M32SyntheticEventExplorer";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import type { M32ConsultationSelection } from "./M32ChronologyConsultation";

/** P3bs: invented-only UI lab; no App.tsx mount, Tauri, SQLite, network or files. */
const empty: M32ConsultationSelection = {
  leftAnchorId: null, rightAnchorId: null,
};
function toy(): M32ChronologyProjection {
  const universe_id = "fiction-p3bs";
  const anchor = (id: string, status: "current" | "revoked" | "superseded",
    revision: string | null, label: string) => ({
    id, universe_id, status, source_revision_id: revision,
    time_kind: "exact" as const, calendar_name: "Calendrier inventé",
    fictional_label: label, precision_text: null,
  });
  return {
    universe_id, reader_reveal_status: "not_authored",
    anchors: [
      anchor("B", "current", "r2", "Porte ouverte"),
      anchor("old-sup", "superseded", "r1", "Même légende"),
      anchor("old-rev", "revoked", "r1", "Même légende"),
      anchor("A", "current", "r2", "Messager"),
      anchor("old-rev2", "revoked", null, "<script>fake()</script>"),
    ],
    precedences: [{
      id: "human-AB", universe_id, before_anchor_id: "A",
      after_anchor_id: "B", status: "current", reason: "Choix humain",
    }],
    narration: [],
  };
}
function derive(status: M32ExplorerFilter, selected = empty,
  revision = "", source: M32ChronologyProjection = toy()) {
  return deriveM32Explorer(source, source.universe_id,
    selected, "", status, 0, revision);
}
function html(source: M32ChronologyProjection = toy()) {
  return renderToStaticMarkup(createElement(Explorer, {
    scenarioKey: "p3bs-toy", expectedUniverseId: source.universe_id,
    snapshot: source,
  }));
}

describe("M3.2 P3bs: fictional historical subtype exploration", () => {
  it("preserves historical union while separating revoked and superseded", () => {
    expect(derive("all").count).toBe(5);
    expect(derive("historical").rows.map(r => r.id))
      .toEqual(["old-rev", "old-rev2", "old-sup"]);
    expect(derive("revoked").rows.map(r => r.id))
      .toEqual(["old-rev", "old-rev2"]);
    expect(derive("superseded").rows.map(r => r.id)).toEqual(["old-sup"]);
    expect(derive("current").rows.map(r => r.id)).toEqual(["A", "B"]);
  });

  it("composes exact source revision and status without invented equivalence", () => {
    expect(derive("revoked", empty, "r1").rows.map(r => r.id)).toEqual(["old-rev"]);
    expect(derive("superseded", empty, "r1").rows.map(r => r.id)).toEqual(["old-sup"]);
    expect(derive("revoked", empty, "R1").count).toBe(0);
    expect(derive("superseded", empty, "r2").count).toBe(0);
    expect(derive("revoked").source_kind).toBe("invented_only");
    expect(derive("superseded").can_write).toBe(false);
  });

  it("preserves an explicit active-pair witness even when both IDs are hidden", () => {
    const selection = { leftAnchorId: "A", rightAnchorId: "B" };
    for (const status of ["revoked", "superseded"] as const) {
      const view = derive(status, selection, "r1");
      expect(view.comparison?.relation).toBe("before");
      expect(view.comparison?.witness.map(w => w.precedence_id)).toEqual(["human-AB"]);
      expect(view.rows.every(r => r.status === status)).toBe(true);
    }
  });

  it("rejects hidden active graph cycles before filtering historical rows", () => {
    const invalid = toy();
    invalid.precedences.push({
      id: "cycle", universe_id: invalid.universe_id,
      before_anchor_id: "B", after_anchor_id: "A",
      status: "current", reason: "Contradiction",
    });
    for (const status of ["revoked", "superseded"] as const)
      expect(() => derive(status, empty, "r1", invalid)).toThrow();
    expect(html(invalid)).toContain("Exploration refusée");
    expect(html(invalid)).not.toContain("Même légende");
  });

  it("rejects foreign-universe nodes, malformed statuses and old selections", () => {
    const foreign = toy(); foreign.anchors[0].universe_id = "outside";
    expect(() => derive("revoked", empty, "r1", foreign)).toThrow();
    expect(() => derive("superseded", empty, "r1", foreign)).toThrow();
    expect(() => deriveM32Explorer(toy(), "fiction-p3bs", empty,
      "", "withdrawn" as M32ExplorerFilter, 0)).toThrow();
    expect(() => derive("revoked", {
      leftAnchorId: "old-rev", rightAnchorId: null,
    })).toThrow();
  });

  it("adds two accessible native choices without a source-write control", () => {
    const markup = html();
    expect(markup).toContain('<option value="historical">Historique seulement</option>');
    expect(markup).toContain('<option value="revoked">Révoqués seulement</option>');
    expect(markup).toContain('<option value="superseded">Remplacés seulement</option>');
    expect(markup).toContain("Filtre de statut");
    expect(markup).toContain('aria-label="Explorateur M3.2 fictif filtrable"');
    expect(markup).not.toContain("Choisir old-rev comme premier événement");
    expect(markup).not.toContain("Choisir old-sup comme deuxième événement");
    expect(markup).not.toContain("Sauvegarde réussie");
  });

  it("escapes hostile historical labels without mutating the original fixture", () => {
    const source = toy(), before = JSON.stringify(source);
    const markup = html(source);
    expect(markup).not.toContain("<script>fake()</script>");
    expect(markup).toContain("&lt;script&gt;fake()");
    expect(JSON.stringify(source)).toBe(before);
    derive("revoked", empty, "", source);
    expect(JSON.stringify(source)).toBe(before);
  });
});
