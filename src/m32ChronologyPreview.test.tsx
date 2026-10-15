import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import M32ChronologyPreview, {
  decodeM32ChronologyProjection,
  type M32ChronologyProjection,
} from "./M32ChronologyPreview";

const fixture: M32ChronologyProjection = {
  universe_id: "u1",
  reader_reveal_status: "not_authored",
  anchors: [
    { id: "z", universe_id: "u1", time_kind: "unknown", status: "current",
      calendar_name: null, fictional_label: null, precision_text: null, source_revision_id: null },
    { id: "a", universe_id: "u1", time_kind: "exact", status: "superseded",
      calendar_name: "Marées", fictional_label: "Cycle XII", precision_text: "jour", source_revision_id: "r-old" },
  ],
  precedences: [
    { id: "ab", universe_id: "u1", before_anchor_id: "a",
      after_anchor_id: "z", status: "revoked", reason: "Version corrigée" },
  ],
  narration: [
    { universe_id: "u1", scene_id: "scene-b", novel_id: "n1", novel_title: "Livre 1",
      chapter_id: "c1", chapter_title: "Chapitre 1", chapter_order: 0,
      scene_order: 1, scene_title: "Scène tardive" },
    { universe_id: "u1", scene_id: "scene-a", novel_id: "n1", novel_title: "Livre 1",
      chapter_id: "c1", chapter_title: "Chapitre 1", chapter_order: 0,
      scene_order: 0, scene_title: "Scène initiale" },
  ],
};

function render(snapshot: M32ChronologyProjection | null, universe="u1"): string {
  return renderToStaticMarkup(createElement(M32ChronologyPreview, {
    expectedUniverseId: universe, snapshot,
  }));
}

describe("M3.2 read-only separated narrative coordinates", () => {
  it("renders world, narration and reader reveal in three distinct sections", () => {
    const html = render(fixture);
    for (const label of ["Chronologie du monde", "Ordre de narration",
      "Ordre de révélation au lecteur", "Cycle XII", "Date fictive exacte",
      "Date inconnue", "Révoquée (historique)"]) {
      expect(html).toContain(label);
    }
    expect(html.indexOf("Scène initiale")).toBeLessThan(html.indexOf("Scène tardive"));
    expect(html).toContain("aucune révélation ne peut être inférée");
    expect(html).not.toContain("<button");
    expect(html).not.toContain("invoke(");
    expect(html).not.toContain("Date.parse");
  });

  it("does not represent a stable anchor identity sort as chronological inference", () => {
    const html = render(fixture);
    expect(html.indexOf("<strong>a</strong>")).toBeLessThan(html.indexOf("<strong>z</strong>"));
    expect(html).toContain("sans inventer une chronologie");
    expect(html).toContain("Aucun ordre global entre romans");
  });

  it("fails closed on mixed Universe, invalid reference and repeated identities", () => {
    const cross = { ...fixture, anchors: [
      { ...fixture.anchors[0], universe_id: "u2" }, fixture.anchors[1],
    ] };
    const brokenEdge = { ...fixture, precedences: [
      { ...fixture.precedences[0], after_anchor_id: "missing" },
    ] };
    const repeated = { ...fixture, anchors: [
      fixture.anchors[0], fixture.anchors[0],
    ] };
    for (const data of [cross, brokenEdge, repeated]) {
      expect(() => decodeM32ChronologyProjection(data, "u1")).toThrow();
      const html = render(data);
      expect(html).toContain("Projection de chronologie refusée");
      expect(html).not.toContain("Cycle XII");
    }
    expect(render(fixture,"u2")).toContain("Projection de chronologie refusée");
  });

  it("does not invent missing evidence or interpolate fictional calendar coordinates", () => {
    const html = render(null);
    expect(html).toContain("aucune donnée vérifiée");
    expect(html).not.toContain("<button");
    const injection = { ...fixture, anchors: [
      { ...fixture.anchors[0], id: "<script>alert(1)</script>" },
      fixture.anchors[1],
    ], precedences: [] };
    const safe = render(injection);
    expect(safe).not.toContain("<script>");
    expect(safe).toContain("&lt;script&gt;");
  });
});
