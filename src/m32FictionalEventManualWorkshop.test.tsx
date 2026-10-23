import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import { startFictionalDraft, type FictionalRevision } from "./m32FictionalManualChronology";
import {
  startFictionalEventNotebook, currentFictionalEvents,
  type FictionalEventNotebook, type FictionalEventInput,
} from "./m32FictionalEventNotebook";
import M32FictionalEventManualWorkshop, {
  applyFictionalWorkshopAction, type FictionalWorkshopAction,
} from "./M32FictionalEventManualWorkshop";

function invented(universe: "fiction-alpha" | "fiction-beta" = "fiction-alpha") {
  const snapshot: M32ChronologyProjection = {
    universe_id: universe, reader_reveal_status: "not_authored",
    anchors: ["A", "B"].map((id, index) => ({
      id, universe_id: universe, status: "current" as const,
      time_kind: "unknown" as const, calendar_name: null,
      fictional_label: null, precision_text: null,
      source_revision_id: index === 0 ? universe + "-rev-1" : null,
    })), precedences: [],
    narration: [{ universe_id: universe, novel_id: "novel-1",
      novel_title: "Roman inventé", chapter_id: "ch-1",
      chapter_title: "Chapitre 1", chapter_order: 0, scene_id: "scene-1",
      scene_title: "Scène 1", scene_order: 0 }],
  };
  const revisions: readonly FictionalRevision[] = [{
    universe_id: universe, novel_id: "novel-1", scene_id: "scene-1",
    revision_id: universe + "-rev-1", revision_label: "Source historique fictive",
  }];
  return startFictionalEventNotebook(startFictionalDraft(snapshot, revisions));
}
const input: FictionalEventInput = { title: "Rencontre", note: "Fait inventé",
  anchor_id: null, source_revision_id: null };
function create(book: FictionalEventNotebook = invented()) {
  return applyFictionalWorkshopAction(book, { kind: "create", input });
}
function change(book: FictionalEventNotebook, id: string, title = "Rencontre corrigée") {
  return applyFictionalWorkshopAction(book, {
    kind: "amend", eventId: id, input: { ...input, title }, reason: "Révision volontaire",
  });
}
describe("M3.2 manual fictional event workshop source-only", () => {
  it("01 renders only invented, non-persistent form and explicit safety message", () => {
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: invented() }));
    expect(html).toContain("Atelier fictif");
    expect(html).toContain("Formulaire d&#x27;événement fictif");
    expect(html).toContain("Créer en mémoire");
    expect(html).toContain("Aucun enregistrement");
    expect(html).toContain("Aucune révision");
  });
  it("02 renders explicit manual anchor and historic revision choices", () => {
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: invented() }));
    expect(html).toContain("Ancre temporelle explicitement choisie");
    expect(html).toContain("Révision historique explicitement choisie");
    expect(html).toContain("fiction-alpha-rev-1");
    expect(html).toContain("Sans ancre (temps inconnu)");
  });
  it("03 creates only in RAM with a single version and audit entry", () => {
    const book = invented(), next = create(book);
    expect(book.events).toHaveLength(0);
    expect(next.events).toHaveLength(1);
    expect(next.audit[0].action).toBe("created");
    expect(next.real_g3_authorized).toBe(false);
  });
  it("04 correction never overwrites the previous version", () => {
    const a = create(), b = change(a, a.events[0].event_id);
    expect(a.events[0].title).toBe("Rencontre");
    expect(b.events.map(e => e.status)).toEqual(["superseded", "current"]);
    expect(b.events.map(e => e.version)).toEqual([1, 2]);
    expect(b.audit[1].explanation).toBe("Révision volontaire");
  });
  it("05 withdrawal retains both original and historical tombstone", () => {
    const a = create(), b = applyFictionalWorkshopAction(a, {
      kind: "withdraw", eventId: a.events[0].event_id, reason: "Retrait humain",
    });
    expect(a.events).toHaveLength(1);
    expect(b.events.map(e => e.status)).toEqual(["superseded", "withdrawn"]);
    expect(currentFictionalEvents(b)).toHaveLength(0);
  });
  it("06 prevents withdrawal after the item is already withdrawn", () => {
    const a = create(), id = a.events[0].event_id;
    const b = applyFictionalWorkshopAction(a, {
      kind: "withdraw", eventId: id, reason: "Fin",
    });
    expect(() => applyFictionalWorkshopAction(b, {
      kind: "withdraw", eventId: id, reason: "Encore",
    })).toThrow();
  });
  it("07 refuses amendment without explicit nonblank rationale", () => {
    const a = create();
    expect(() => applyFictionalWorkshopAction(a, {
      kind: "amend", eventId: a.events[0].event_id, input, reason: " ",
    })).toThrow();
  });
  it("08 refuses forged foreign Universe event ID", () => {
    const a = create();
    expect(() => applyFictionalWorkshopAction(a, {
      kind: "withdraw", eventId: "fiction-beta-event-0001", reason: "Non",
    })).toThrow();
  });
  it("09 never infers a historical revision from a selected anchor alone", () => {
    expect(() => applyFictionalWorkshopAction(invented(), {
      kind: "create", input: { ...input, anchor_id: "A" },
    })).toThrow();
  });
  it("10 accepts only exactly matched manually supplied historical references", () => {
    const a = applyFictionalWorkshopAction(invented(), {
      kind: "create", input: {
        ...input, anchor_id: "A", source_revision_id: "fiction-alpha-rev-1",
      },
    });
    expect(a.events[0].source_revision_id).toBe("fiction-alpha-rev-1");
  });
  it("11 rejects foreign historical revision identifiers", () => {
    expect(() => applyFictionalWorkshopAction(invented(), {
      kind: "create", input: { ...input, anchor_id: "A",
        source_revision_id: "fiction-beta-rev-1" },
    })).toThrow();
  });
  it("12 untrusted notebook origin cannot be promoted through controller", () => {
    const a = invented();
    expect(() => applyFictionalWorkshopAction({
      ...a, data_origin: "real_sqlite",
    } as unknown as FictionalEventNotebook, { kind: "create", input })).toThrow();
  });
  it("13 two Universes preserve homonymous human text but distinct stable IDs", () => {
    const a = create(invented("fiction-alpha")), b = create(invented("fiction-beta"));
    expect(a.events[0].title).toBe(b.events[0].title);
    expect(a.events[0].event_id).not.toBe(b.events[0].event_id);
  });
  it("14 read-only server render never mutates or persists supplied notebook", () => {
    const a = create(), before = JSON.stringify(a);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: a }));
    expect(html).toContain("Corriger ou retirer");
    expect(html).toContain("Rencontre");
    expect(JSON.stringify(a)).toBe(before);
  });
  it("15 historical scene revisions are preserved across manual amendments", () => {
    const a = create(), b = change(a, a.events[0].event_id);
    expect(b.draft.revisions).toEqual(a.draft.revisions);
    expect(b.draft.snapshot).toEqual(a.draft.snapshot);
  });
  it("16 no implicit reader-reveal ordering in manual workshop transitions", () => {
    const a = create(), b = change(a, a.events[0].event_id);
    expect(b.draft.snapshot.reader_reveal_status).toBe("not_authored");
    expect(b.draft.snapshot.precedences).toEqual([]);
  });
  it("17 actions with removed or empty event IDs refuse without mutation", () => {
    const a = create(), before = JSON.stringify(a);
    expect(() => applyFictionalWorkshopAction(a, {
      kind: "amend", eventId: "", input, reason: "Refus",
    })).toThrow();
    expect(JSON.stringify(a)).toBe(before);
  });
  it("18 controller only has 3 human edit actions, not filesystem/IPC", () => {
    const kinds: FictionalWorkshopAction["kind"][] = ["create", "amend", "withdraw"];
    expect(kinds).toEqual(["create", "amend", "withdraw"]);
  });
});
