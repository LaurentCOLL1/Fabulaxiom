import { readFileSync } from "node:fs";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import { startP3FictionalState, applyP3FictionalCommand } from "./m32P3FictionalCommandContract";
import M32FictionalPersistenceNotice, {
  describeM32FictionalPersistence,
} from "./m32FictionalPersistenceNotice";

/** Source-only fixture guard: a real Windows writer refusal is NOT tested here. */
const files = [
  "M32ManualChronologyLab.tsx",
  "M32FictionalEventManualWorkshop.tsx",
  "M32P3FictionalCommandWorkshop.tsx",
  "M32P4aStageReviewPanel.tsx",
] as const;

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
    expect(initial).toContain('role="status"');
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
  it("05 all four fictional action surfaces show explicit nonpersistence", () => {
    for (const name of files) {
      const source = readFileSync(new URL("./" + name, import.meta.url), "utf8");
      expect(source, name).toContain('from "./m32FictionalPersistenceNotice"');
      expect(source, name).toContain("<M32FictionalPersistenceNotice");
      expect(source, name).not.toMatch(/\binvoke\s*\(|\bfetch\s*\(|localStorage\s*\(|APPROVE_CANON/);
    }
    const eventSource = readFileSync(new URL("./M32FictionalEventManualWorkshop.tsx", import.meta.url), "utf8");
    expect(eventSource).not.toContain("Enregistrer une nouvelle version");
    expect(eventSource).toContain("Créer une nouvelle version fictive en mémoire");
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
