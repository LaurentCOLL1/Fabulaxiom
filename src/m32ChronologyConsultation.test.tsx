import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32ChronologyConsultation, {
  EMPTY_M32_CONSULTATION_SELECTION,
  M32SyntheticConsultationLab,
  chooseM32ConsultationAnchor,
  inspectM32Consultation,
  type M32ConsultationSelection,
} from "./M32ChronologyConsultation";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";

const invented: M32ChronologyProjection = {
  universe_id: "invented-u",
  reader_reveal_status: "not_authored",
  anchors: [
    { id: "A", universe_id: "invented-u", time_kind: "exact",
      status: "current", calendar_name: "Calendrier inventé",
      fictional_label: "Troisième cloche", precision_text: null, source_revision_id: "old-rev" },
    ...["B", "C", "D"].map(id => ({
      id, universe_id: "invented-u", time_kind: "unknown" as const,
      status: "current" as const, calendar_name: null, fictional_label: null,
      precision_text: null, source_revision_id: null,
    })),
    { id: "retired", universe_id: "invented-u", time_kind: "unknown",
      status: "revoked", calendar_name: null, fictional_label: null,
      precision_text: null, source_revision_id: null },
  ],
  precedences: [
    { id: "ab", universe_id: "invented-u", before_anchor_id: "A",
      after_anchor_id: "B", status: "current", reason: "Le messager arrive" },
    { id: "bc", universe_id: "invented-u", before_anchor_id: "B",
      after_anchor_id: "C", status: "current", reason: "La porte s'ouvre" },
    { id: "historic-ad", universe_id: "invented-u", before_anchor_id: "A",
      after_anchor_id: "D", status: "revoked", reason: "Retiré" },
  ],
  narration: [
    { scene_id: "s1", universe_id: "invented-u", novel_id: "novel-1",
      novel_title: "Livre inventé", chapter_id: "c1", chapter_title: "Chapitre 1",
      chapter_order: 0, scene_order: 0, scene_title: "Ouverture" },
  ],
};

const empty = EMPTY_M32_CONSULTATION_SELECTION;
function selected(left: string | null, right: string | null): M32ConsultationSelection {
  return { leftAnchorId: left, rightAnchorId: right };
}
function inspect(selection: M32ConsultationSelection = empty,
  data: M32ChronologyProjection | null = invented, universe = "invented-u") {
  return inspectM32Consultation(data, universe, selection);
}
function view(selection: M32ConsultationSelection = empty,
  data: M32ChronologyProjection | null = invented, universe = "invented-u") {
  return renderToStaticMarkup(createElement(M32ChronologyConsultation, {
    expectedUniverseId: universe, snapshot: data, selection,
    onSelectionChange: (_next: M32ConsultationSelection) => {},
  }));
}

describe("M3.2 connected synthetic read-only consultation workflow", () => {
  it("displays world-time, narration and reader reveal independently", () => {
    const html = view();
    expect(html).toContain("Chronologie du monde");
    expect(html).toContain("Ordre de narration");
    expect(html).toContain("Ordre de révélation au lecteur");
    expect(html).toContain("aucune révélation ne peut être inférée");
  });
  it("uses two native selects with explicit associated labels", () => {
    const html = view();
    expect((html.match(/<select\b/g) ?? []).length).toBe(2);
    expect(html).toContain("Premier événement");
    expect(html).toContain("Deuxième événement");
    expect((html.match(/<label htmlFor=/g) ?? []).length).toBe(0);
    expect((html.match(/<label for=/g) ?? []).length).toBe(2);
  });
  it("does not silently choose a default pair or show a witness", () => {
    const html = view();
    expect(html).toContain("Choisissez les deux événements");
    expect(html).not.toContain("Relations humaines justificatives");
    expect(inspect().comparison).toBeNull();
  });
  it("includes only current assertions as selectable options", () => {
    const opts = inspect().options.map(x => x.id);
    expect(opts).toEqual(["A", "B", "C", "D"]);
    const html = view();
    expect(html).not.toContain('<option value="retired"');
    expect(html).toContain("Troisième cloche");
    expect(html).toContain("old-rev");
  });
  it("selects the first ID using an explicit pure transition", () => {
    const one = chooseM32ConsultationAnchor(invented, "invented-u", empty, "left", "A");
    expect(one).toEqual(selected("A", null));
    expect(inspect(one).stage).toBe("choose_pair");
  });
  it("selects the second ID and obtains a transitive before witness", () => {
    const first = chooseM32ConsultationAnchor(invented, "invented-u", empty, "left", "A");
    const both = chooseM32ConsultationAnchor(invented, "invented-u", first, "right", "C");
    expect(inspect(both).comparison?.relation).toBe("before");
    expect(inspect(both).comparison?.witness.map(x => x.precedence_id)).toEqual(["ab", "bc"]);
    const html = view(both);
    expect(html).toContain("Relations humaines justificatives");
    expect(html).toContain("Le messager arrive");
    expect(html).toContain("La porte s");
  });
  it("reversing the explicitly chosen IDs changes before to after", () => {
    expect(inspect(selected("C", "A")).comparison?.relation).toBe("after");
    expect(view(selected("C", "A"))).toContain("Après :");
  });
  it("permits same selected identity without fabricated edges", () => {
    const model = inspect(selected("B", "B"));
    expect(model.comparison?.relation).toBe("same");
    expect(model.comparison?.witness).toEqual([]);
  });
  it("displays incomparable when no human precedence exists", () => {
    const model = inspect(selected("A", "D"));
    expect(model.comparison?.relation).toBe("incomparable");
    expect(model.comparison?.witness).toEqual([]);
    expect(view(selected("A", "D"))).toContain("Ordre indéterminé");
    expect(view(selected("A", "D"))).not.toContain("Relations humaines justificatives");
  });
  it("clearing a selection explicitly removes the comparison", () => {
    const next = chooseM32ConsultationAnchor(invented, "invented-u",
      selected("A", "C"), "right", "");
    expect(next).toEqual(selected("A", null));
    expect(inspect(next).comparison).toBeNull();
  });
  it("never auto-replaces a historical selection with the first valid ID", () => {
    expect(() => inspect(selected("retired", "A"))).toThrow();
    const html = view(selected("retired", "A"));
    expect(html).toContain("Consultation refusée");
    expect(html).not.toContain("Le messager arrive");
  });
  it("refuses a foreign or absent selected anchor, including at transition", () => {
    expect(() => inspect(selected("other-u", "B"))).toThrow();
    expect(() => chooseM32ConsultationAnchor(invented, "invented-u",
      empty, "left", "unknown")).toThrow();
    expect(() => chooseM32ConsultationAnchor(invented, "invented-u",
      empty, "right", "retired")).toThrow();
  });
  it("refuses invalid selection side, types and missing members", () => {
    expect(() => chooseM32ConsultationAnchor(invented, "invented-u",
      empty, "middle" as never, "A")).toThrow();
    expect(() => chooseM32ConsultationAnchor(invented, "invented-u",
      empty, "left", null as never)).toThrow();
    expect(() => inspect({ leftAnchorId: "A" } as never)).toThrow();
  });
  it("refuses cross-Universe snapshots without leaking any assertions", () => {
    const html = view(empty, invented, "foreign-universe");
    expect(html).toContain("Consultation refusée");
    expect(html).not.toContain("Troisième cloche");
  });
  it("checks cycles even before two events are selected", () => {
    const cyclic = { ...invented, precedences: [...invented.precedences,
      { id: "ca", universe_id: "invented-u", before_anchor_id: "C",
        after_anchor_id: "A", status: "current" as const, reason: "cycle" }] };
    expect(() => inspect(empty, cyclic)).toThrow(/cycle/);
    expect(view(empty, cyclic)).toContain("Consultation refusée");
  });
  it("refuses active edges from revoked source even before selection", () => {
    const bad = { ...invented, precedences: [...invented.precedences,
      { id: "past-edge", universe_id: "invented-u", before_anchor_id: "retired",
        after_anchor_id: "A", status: "current" as const, reason: "invalid" }] };
    expect(() => inspect(empty, bad)).toThrow();
  });
  it("refuses active edges with no current source anchors", () => {
    const bad = { ...invented,
      anchors: invented.anchors.map(a => ({ ...a, status: "revoked" as const })),
      precedences: invented.precedences.map(e => ({ ...e, status: "current" as const })),
    };
    expect(() => inspect(empty, bad)).toThrow();
  });
  it("handles wholly empty synthetic chronology with no selectable pair", () => {
    const noEvents = { ...invented, anchors: [], precedences: [], narration: [] };
    expect(inspect(empty, noEvents).stage).toBe("no_active_anchors");
    const html = view(empty, noEvents);
    expect(html).toContain("Aucune assertion en vigueur");
    expect(html).not.toContain("<select");
  });
  it("without a snapshot it never tries to query a production database", () => {
    const html = view(empty, null);
    expect(html).toContain("aucun jeu de données fourni");
    expect(html).not.toContain("<select");
    expect(() => inspect(selected("A", "B"), null)).toThrow();
  });
  it("renders a standalone lab harness with empty local selection", () => {
    const html = renderToStaticMarkup(createElement(M32SyntheticConsultationLab, {
      scenarioKey: "fiction-v1", expectedUniverseId: "invented-u", snapshot: invented,
    }));
    expect(html).toContain("Choisissez les deux événements");
    expect(html).toContain("Premier événement");
  });
  it("does not expose write buttons, network links or forms", () => {
    const html = view(selected("A", "C"));
    expect(html).not.toMatch(/<(button|form|textarea|input)\b/);
    expect(html).not.toContain("invoke(");
    expect(html).not.toContain("fetch(");
  });
  it("escapes invented script-like labels and justification reasons", () => {
    const modified = { ...invented, anchors: invented.anchors.map(a =>
      a.id === "A" ? { ...a, fictional_label: "<script>evil()</script>" } : a),
      precedences: invented.precedences.map(e =>
        e.id === "ab" ? { ...e, reason: "<script>danger()</script>" } : e),
    };
    const html = view(selected("A", "C"), modified);
    expect(html).not.toContain("<script>");
    expect(html).toContain("&lt;script&gt;");
  });
  it("preserves synthetic input arrays and selection object unchanged", () => {
    const before = JSON.stringify(invented);
    const selection = selected("A", "C");
    const beforeSelection = JSON.stringify(selection);
    view(selection);
    chooseM32ConsultationAnchor(invented, "invented-u", selection, "right", "B");
    expect(JSON.stringify(invented)).toBe(before);
    expect(JSON.stringify(selection)).toBe(beforeSelection);
  });
  it("provides non-authorizing output provenance and no editing rights", () => {
    const model = inspect(selected("A", "C"));
    expect(model.data_origin).toBe("synthetic_in_memory_only");
    expect(model.editing_authorized).toBe(false);
    expect(model.comparison?.edit_controls_available).toBe(false);
  });
});
