import M32P3FictionalCommandWorkshop from "./M32P3FictionalCommandWorkshop";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import { startP3FictionalState, applyP3FictionalCommand } from "./m32P3FictionalCommandContract";
import M32FictionalPersistenceNotice, {
  describeM32FictionalPersistence,
} from "./m32FictionalPersistenceNotice";

/** Only fictional browser fixtures; real Windows writer refusal is NOT tested. */
describe("M32-076 no false persistence claim in unmounted fictional laboratories", () => {
  it("01 fixture always exposes nonpersistent and unauthorized writer flags", () => {
    expect(describeM32FictionalPersistence("fixture")).toMatchObject({
      state: "fixture", persisted: false, writer_called: false,
      writer_authorized: false, status: "non_persisted",
    });
    expect(describeM32FictionalPersistence("fixture").message).toContain("G3 STOP_UNAVAILABLE");
  });
  it("02 refused fictional action does not imply a real writer attempt", () => {
    const response = describeM32FictionalPersistence("action_refused");
    expect(response.persisted).toBe(false);
    expect(response.writer_called).toBe(false);
    expect(response.writer_authorized).toBe(false);
    expect(response.message).toContain("Action fictive refusée");
    expect(response.message).toContain("Aucun appel au writer réel");
    expect(response.message).toContain("aucun changement des données réelles");
  });
  it("03 invalid status fails closed instead of claiming success", () => {
    expect(() => describeM32FictionalPersistence(
      "saved" as never)).toThrow(/STOP M32-076/);
  });
  it("04 visible default and rejection distinguish status and alert", () => {
    const initial = renderToStaticMarkup(createElement(M32FictionalPersistenceNotice));
    const refused = renderToStaticMarkup(createElement(M32FictionalPersistenceNotice,
      {state: "action_refused"}));
    expect(initial).toContain('role="note"');
    expect(initial).toContain("Simulation fictive non persistée");
    expect(refused).toContain('role="alert"');
    expect(refused).toContain("Action fictive refusée");
    for (const html of [initial, refused]) {
      expect(html.toLowerCase()).toContain("aucune sauvegarde");
      expect(html).toContain('aria-label="Persistance de la simulation chronologique"');
      expect(html).toContain("G3 STOP_UNAVAILABLE");
      expect(html).not.toMatch(/Sauvegarde réussie|Écriture confirmée|persisted.true/i);
    }
  });
  it("05 fictional command UI always presents nonpersistence in SSR", () => {
    const universe_id = "fiction-m32076-ui";
    const initial: M32ChronologyProjection = {
      universe_id, reader_reveal_status: "not_authored",
      anchors: ["A", "B"].map(id => ({
        id, universe_id, time_kind: "unknown" as const, status: "current" as const,
        calendar_name: null, fictional_label: null, precision_text: null,
        source_revision_id: null,
      })),
      precedences: [],
      narration: [{
        universe_id, novel_id: "fiction-novel", novel_title: "Roman fictif",
        chapter_id: "fiction-chapter", chapter_title: "Chapitre fictif",
        chapter_order: 0, scene_id: "fiction-scene",
        scene_title: "Scène fictive", scene_order: 0,
      }],
    };
    const html = renderToStaticMarkup(createElement(M32P3FictionalCommandWorkshop,
      {initial, revisions: []}));
    expect(html).toContain('aria-label="Persistance de la simulation chronologique"');
    expect(html).toContain("Simulation fictive non persistée");
    expect(html).toContain("G3 STOP_UNAVAILABLE");
    expect(html).not.toContain("Sauvegarde réussie");
  });
  it("06 rejected fictional command preserves the actual in-memory reducer state", () => {
    const universe_id = "fiction-m32076";
    const snapshot: M32ChronologyProjection = {
      universe_id, reader_reveal_status: "not_authored",
      anchors: ["A", "B"].map(id => ({
        id, universe_id, time_kind: "unknown" as const, status: "current" as const,
        calendar_name: null, fictional_label: null, precision_text: null,
        source_revision_id: null,
      })),
      precedences: [], narration: [],
    };
    const state = startP3FictionalState(snapshot, []);
    const before = JSON.stringify(state);
    expect(() => applyP3FictionalCommand(state, {
      kind: "create_precedence", universe_id,
      relation: {before_anchor_id: "A", after_anchor_id: "A", reason: "Refus de boucle"},
    })).toThrow();
    expect(JSON.stringify(state)).toBe(before);
    expect(state.draft.real_g3_authorized).toBe(false);
    const feedback = describeM32FictionalPersistence("action_refused");
    expect(feedback.persisted).toBe(false);
    expect(feedback.writer_called).toBe(false);
    expect(feedback.writer_authorized).toBe(false);
  });
});
