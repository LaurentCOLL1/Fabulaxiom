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

  it("refuses inherited enum property names rather than accepting prototype names", () => {
    const badKind = { ...fixture, anchors: [
      { ...fixture.anchors[0], time_kind: "toString" as never }, fixture.anchors[1],
    ] };
    const badStatus = { ...fixture, anchors: [
      { ...fixture.anchors[0], status: "__proto__" as never }, fixture.anchors[1],
    ] };
    for (const item of [badKind, badStatus]) {
      expect(() => decodeM32ChronologyProjection(item, "u1")).toThrow();
    }
  });

  it("refuses fabricated calendars, labels and precision on unknown or relative dates", () => {
    for (const kind of ["unknown", "relative"] as const) {
      const a = { ...fixture.anchors[0], time_kind: kind };
      for (const metadata of [
        { fictional_label: "made-up" }, { calendar_name: "made-up" },
        { precision_text: "made-up" },
      ]) {
        expect(() => decodeM32ChronologyProjection({
          ...fixture, anchors: [{ ...a, ...metadata }, fixture.anchors[1]],
        }, "u1")).toThrow();
      }
    }
  });

  it("refuses approximate dates without both calendar and explicit precision", () => {
    const approx = {
      ...fixture.anchors[0], time_kind: "approximate" as const,
      calendar_name: "Fiction", precision_text: "short period",
    };
    for (const details of [{ calendar_name: null }, { precision_text: null }]) {
      expect(() => decodeM32ChronologyProjection({
        ...fixture, anchors: [{ ...approx, ...details }, fixture.anchors[1]],
      }, "u1")).toThrow();
    }
  });

  it("refuses wrong-Universe edges and manuscript scenes", () => {
    const edge = { ...fixture, precedences: [
      { ...fixture.precedences[0], universe_id: "u2" },
    ] };
    const scene = { ...fixture, narration: [
      { ...fixture.narration[0], universe_id: "u2" },
    ] };
    for (const input of [edge, scene]) {
      expect(() => decodeM32ChronologyProjection(input, "u1")).toThrow();
    }
  });

  it("refuses same-anchor links and repeated edge IDs", () => {
    const selfEdge = { ...fixture, precedences: [{
      ...fixture.precedences[0], before_anchor_id: "z", after_anchor_id: "z",
    }] };
    const repeated = { ...fixture, precedences: [
      fixture.precedences[0], fixture.precedences[0],
    ] };
    for (const input of [selfEdge, repeated]) {
      expect(() => decodeM32ChronologyProjection(input, "u1")).toThrow();
    }
  });

  it("refuses duplicate scene IDs, invalid scene coordinates and empty source revision", () => {
    const repeated = { ...fixture, narration: [
      fixture.narration[0], fixture.narration[0],
    ] };
    const negative = { ...fixture, narration: [
      { ...fixture.narration[0], scene_order: -1 },
    ] };
    const fractional = { ...fixture, narration: [
      { ...fixture.narration[0], chapter_order: 0.5 },
    ] };
    const emptySource = { ...fixture, anchors: [
      fixture.anchors[0], { ...fixture.anchors[1], source_revision_id: "" },
    ] };
    for (const input of [repeated, negative, fractional, emptySource]) {
      expect(() => decodeM32ChronologyProjection(input, "u1")).toThrow();
    }
  });

  it("refuses an oversized invented Universe", () => {
    const many = Array.from({ length: 513 }, (_, i) => ({
      ...fixture.anchors[0], id: "invented-" + String(i),
    }));
    expect(() => decodeM32ChronologyProjection({
      ...fixture, anchors: many, precedences: [],
    }, "u1")).toThrow();
  });

  it("renders an empty synthetic projection but never invents missing scene data", () => {
    const output = render({ ...fixture, anchors: [], precedences: [], narration: [] });
    expect(output).toContain("Aucune ancre temporelle");
    expect(output).toContain("Aucune scène liée");
    expect(output).toContain("Non renseigné");
  });

  it("displays raw fictional calendars and historical revisions without Gregorian conversion", () => {
    const html = render(fixture);
    expect(html).toContain("Marées");
    expect(html).toContain("Cycle XII");
    expect(html).toContain("r-old");
    expect(html).not.toContain("1970");
  });

  it("never renders interactive write inputs, forms or controls", () => {
    const html = render(fixture);
    expect(html).not.toMatch(/<(button|input|textarea|form)\b/);
  });

  it("never mutates input arrays when ordering the read-only presentation", () => {
    const originalAnchors = fixture.anchors.map(a => a.id);
    const originalScenes = fixture.narration.map(s => s.scene_id);
    render(fixture);
    expect(fixture.anchors.map(a => a.id)).toEqual(originalAnchors);
    expect(fixture.narration.map(s => s.scene_id)).toEqual(originalScenes);
  });

  it("does not silently merge two same-title scenes with distinct identities", () => {
    const html = render({ ...fixture, narration: fixture.narration.map(s =>
      ({ ...s, scene_title: "Même nom" })) });
    expect((html.match(/Même nom/g) ?? []).length).toBe(2);
  });

  it("rejects mixed-view snapshots with an invalid reader-reveal status", () => {
    const changed = { ...fixture, reader_reveal_status: "inferred" as never };
    expect(() => decodeM32ChronologyProjection(changed, "u1")).toThrow();
    expect(render(changed)).toContain("Projection de chronologie refusée");
  });

  it("rejects unverified fixture shapes rather than trusting TypeScript annotations", () => {
    const broken = { ...fixture, narration: null } as unknown as M32ChronologyProjection;
    expect(() => decodeM32ChronologyProjection(broken, "u1")).toThrow();
    expect(render(broken)).toContain("Projection de chronologie refusée");
  });

});
