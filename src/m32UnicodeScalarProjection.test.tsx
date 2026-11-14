import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32ChronologyPreview, {
  decodeM32ChronologyProjection, type M32ChronologyProjection,
} from "./M32ChronologyPreview";
import M32ChronologyConsultation, {
  EMPTY_M32_CONSULTATION_SELECTION, inspectM32Consultation,
} from "./M32ChronologyConsultation";
import { compareM32WorldOrder } from "./M32WorldOrderComparison";

// P3y synthetic fixture only; no mounted app, storage, network, Tauri, SQLite,
// IPC, writer, Windows profile, original v6/v7 or recovery.
function toy(): M32ChronologyProjection {
  const u = "universe-fiction";
  return {
    universe_id: u, reader_reveal_status: "not_authored",
    anchors: [
      { id: "A", universe_id: u, time_kind: "unknown", status: "revoked",
        calendar_name: null, fictional_label: null, precision_text: null,
        source_revision_id: "fictional-old-revision" },
    ],
    precedences: [],
    narration: [],
  };
}
function preview(snapshot: M32ChronologyProjection): string {
  return renderToStaticMarkup(createElement(M32ChronologyPreview, {
    expectedUniverseId: snapshot.universe_id, snapshot,
  }));
}
function consult(snapshot: M32ChronologyProjection): string {
  return renderToStaticMarkup(createElement(M32ChronologyConsultation, {
    expectedUniverseId: snapshot.universe_id, snapshot,
    selection: EMPTY_M32_CONSULTATION_SELECTION, onSelectionChange: () => {},
  }));
}
function refuseEverywhere(snapshot: M32ChronologyProjection): void {
  const before = JSON.stringify(snapshot);
  expect(() => decodeM32ChronologyProjection(snapshot, snapshot.universe_id))
    .toThrow(/Unicode non scalaire/);
  expect(() => inspectM32Consultation(snapshot, snapshot.universe_id,
    EMPTY_M32_CONSULTATION_SELECTION)).toThrow(/Unicode non scalaire/);
  for (const html of [preview(snapshot), consult(snapshot)]) {
    expect(html).toContain("refusée");
    expect(html).not.toContain("fictional-old-revision");
    expect(html).not.toContain("PRIVATE_FICTIONAL_REASON");
    expect(html).not.toMatch(/<(button|input|form|textarea|select)\b/i);
  }
  expect(JSON.stringify(snapshot)).toBe(before);
}
describe("M3.2 P3y shared scalar identity preflight on unmounted read-only views", () => {
  it("keeps a valid all-historical fixture with zero current assertions inspectable", () => {
    const s = toy(), original = JSON.stringify(s);
    expect(decodeM32ChronologyProjection(s, s.universe_id)).toBe(s);
    const model = inspectM32Consultation(s, s.universe_id,
      EMPTY_M32_CONSULTATION_SELECTION);
    expect(model.stage).toBe("no_active_anchors");
    expect(model.editing_authorized).toBe(false);
    expect(preview(s)).toContain("fictional-old-revision");
    expect(consult(s)).toContain("Aucune assertion en vigueur");
    expect(JSON.stringify(s)).toBe(original);
  });
  it("refuses an isolated high surrogate in Universe ID without a selectable anchor", () => {
    const s = toy(), bad = "universe-\uD800";
    s.universe_id = bad;
    s.anchors[0].universe_id = bad;
    refuseEverywhere(s);
  });
  it("refuses an isolated low surrogate in historical anchor ID before showing history", () => {
    const s = toy(); s.anchors[0].id = "old-\uDC00";
    refuseEverywhere(s);
  });
  it("refuses a malformed retired relation ID with zero current anchors", () => {
    const s = toy();
    s.precedences.push({ id: "revoked-\uD800", universe_id: s.universe_id,
      before_anchor_id: "A", after_anchor_id: "B", status: "revoked",
      reason: "PRIVATE_FICTIONAL_REASON" });
    s.anchors.push({ ...s.anchors[0], id: "B" });
    refuseEverywhere(s);
  });
  it("refuses malformed source revision ID in historical anchor", () => {
    const s = toy(); s.anchors[0].source_revision_id = "old-\uDC00";
    refuseEverywhere(s);
  });
  it("refuses malformed scene ID without current chronology", () => {
    const s = toy();
    s.narration.push({
      scene_id: "scene-\uD800", universe_id: s.universe_id,
      novel_id: "novel", novel_title: "Invented novel",
      chapter_id: "chapter", chapter_title: "Invented chapter",
      chapter_order: 0, scene_order: 0, scene_title: "Invented scene",
    });
    refuseEverywhere(s);
  });
  it("refuses malformed novel and chapter IDs without partial narration", () => {
    for (const key of ["novel_id", "chapter_id"] as const) {
      const s = toy();
      s.narration.push({
        scene_id: "scene", universe_id: s.universe_id,
        novel_id: "novel", novel_title: "Invented novel",
        chapter_id: "chapter", chapter_title: "Invented chapter",
        chapter_order: 0, scene_order: 0, scene_title: "Invented scene",
      });
      s.narration[0][key] = "broken-\uDC00";
      refuseEverywhere(s);
    }
  });
  it("keeps a valid astral ID and escaped HTML harmless, without claiming persistence", () => {
    const s = toy();
    s.anchors[0].id = "A💠";
    s.anchors[0].source_revision_id = "revision💠";
    s.anchors[0].time_kind = "exact";
    s.anchors[0].calendar_name = "Invented calendar";
    s.anchors[0].fictional_label = "<img src=x onerror=alert(1)>";
    const before = JSON.stringify(s);
    const model = inspectM32Consultation(s, s.universe_id,
      EMPTY_M32_CONSULTATION_SELECTION);
    expect(model.stage).toBe("no_active_anchors");
    expect(preview(s)).toContain("revision💠");
    expect(preview(s)).toContain("&lt;img");
    expect(preview(s)).not.toContain("<img ");
    expect(preview(s)).not.toMatch(/<(button|input|form|textarea)\b/i);
    expect(JSON.stringify(s)).toBe(before);
  });
  it("preserves P3x refusal for malformed selected IDs at comparison boundary", () => {
    const s = toy();
    s.anchors[0].status = "current";
    s.anchors[0].id = "A\uD800";
    expect(() => compareM32WorldOrder(s, s.universe_id, "A\uD800", "A\uD800"))
      .toThrow(/Unicode non scalaire/);
  });
});
