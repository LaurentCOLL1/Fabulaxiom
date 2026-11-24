import { readFileSync } from "node:fs";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
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
  it("06 refusal messages cannot overwrite real state or imply writer admission", () => {
    const old = Object.freeze({data_origin:"fictional_browser_memory_only", writer_admitted:false,
      version:1, saved:false});
    const next = describeM32FictionalPersistence("action_refused");
    expect(old.saved).toBe(false);
    expect(old.version).toBe(1);
    expect(next.persisted).toBe(false);
    expect(next.writer_authorized).toBe(false);
  });
});
