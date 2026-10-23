import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import {
  startFictionalDraft, supersedeFictionalAnchor, type FictionalRevision,
} from "./m32FictionalManualChronology";
import {
  startFictionalEventNotebook, createFictionalEvent, amendFictionalEvent,
  withdrawFictionalEvent, inspectFictionalEventNotebook, currentFictionalEvents,
} from "./m32FictionalEventNotebook";
import M32FictionalEventNotebookPreview from "./M32FictionalEventNotebookPreview";

function fixture(universe: "fiction-alpha" | "fiction-beta") {
  const snapshot: M32ChronologyProjection = {
    universe_id: universe, reader_reveal_status: "not_authored",
    anchors: ["A", "B"].map((id, i) => ({
      id, universe_id: universe, time_kind: "unknown" as const,
      status: "current" as const, calendar_name: null, fictional_label: null,
      precision_text: null, source_revision_id: i === 0 ? universe + "-revision-1" : null,
    })),
    precedences: [],
    narration: [{ universe_id: universe, novel_id: "novel-one",
      novel_title: "Roman inventé", chapter_id: "chapter-one", chapter_title: "Chapitre 1",
      chapter_order: 0, scene_id: "scene-one", scene_title: "Scène 1", scene_order: 0 }],
  };
  const revisions: readonly FictionalRevision[] = [{
    universe_id: universe, novel_id: "novel-one", scene_id: "scene-one",
    revision_id: universe + "-revision-1", revision_label: "Historique non réécrit",
  }];
  return startFictionalEventNotebook(startFictionalDraft(snapshot, revisions));
}
const plain = { title: "Première rencontre", note: "Evénement manuel", anchor_id: null,
  source_revision_id: null };
const linked = { ...plain, anchor_id: "A", source_revision_id: "fiction-alpha-revision-1" };
describe("M3.2 invented-only manual event CRUD and immutable revision history", () => {
  it("01 creates an unanchored event without inventing a date", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(currentFictionalEvents(a)).toHaveLength(1);
    expect(currentFictionalEvents(a)[0].anchor_id).toBeNull();
    expect(currentFictionalEvents(a)[0].source_revision_id).toBeNull();
    expect(a.real_g3_authorized).toBe(false);
  });
  it("02 binds a manual event to an exact historical revision", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), linked);
    expect(a.events[0].source_revision_id).toBe("fiction-alpha-revision-1");
    expect(a.events[0].anchor_id).toBe("A");
    expect(a.draft.revisions[0].revision_label).toBe("Historique non réécrit");
  });
  it("03 rejects a foreign or missing anchor", () => {
    expect(() => createFictionalEvent(fixture("fiction-alpha"), {
      ...plain, anchor_id: "fiction-beta-A",
    })).toThrow();
    expect(() => createFictionalEvent(fixture("fiction-alpha"), {
      ...plain, anchor_id: "missing",
    })).toThrow();
  });
  it("04 rejects guessed or foreign historical revisions", () => {
    expect(() => createFictionalEvent(fixture("fiction-alpha"), {
      ...linked, source_revision_id: "fiction-beta-revision-1",
    })).toThrow();
    expect(() => createFictionalEvent(fixture("fiction-alpha"), {
      ...linked, source_revision_id: "newest",
    })).toThrow();
  });
  it("05 refuses revision without explicit corresponding anchor", () => {
    expect(() => createFictionalEvent(fixture("fiction-alpha"), {
      ...plain, source_revision_id: "fiction-alpha-revision-1",
    })).toThrow();
    expect(() => createFictionalEvent(fixture("fiction-alpha"), {
      ...plain, anchor_id: "A", source_revision_id: null,
    })).toThrow();
  });
  it("06 amendment retains the former version and audit explanation", () => {
    const first = createFictionalEvent(fixture("fiction-alpha"), linked);
    const id = first.events[0].event_id;
    const changed = amendFictionalEvent(first, id, { ...linked, title: "Rencontre corrigée" },
      "Correction explicite");
    expect(first.events).toHaveLength(1);
    expect(changed.events.map(e => e.status)).toEqual(["superseded", "current"]);
    expect(changed.events.map(e => e.version)).toEqual([1, 2]);
    expect(changed.events[0].title).toBe("Première rencontre");
    expect(changed.audit[1].explanation).toBe("Correction explicite");
  });
  it("07 withdrawal retains tombstone without deleting M2 sources", () => {
    const first = createFictionalEvent(fixture("fiction-alpha"), linked);
    const later = withdrawFictionalEvent(first, first.events[0].event_id, "Retrait humain");
    expect(currentFictionalEvents(later)).toHaveLength(0);
    expect(later.events.map(e => e.status)).toEqual(["superseded", "withdrawn"]);
    expect(later.draft.revisions[0]).toEqual(first.draft.revisions[0]);
    expect(later.audit[1].action).toBe("withdrawn");
  });
  it("08 rejects a double withdrawal or editing a withdrawn event", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    const gone = withdrawFictionalEvent(a, a.events[0].event_id, "Retiré");
    expect(() => withdrawFictionalEvent(gone, a.events[0].event_id, "Encore")).toThrow();
    expect(() => amendFictionalEvent(gone, a.events[0].event_id, plain, "Modifié")).toThrow();
  });
  it("09 two Universe notebooks keep identical human titles separately", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    const b = createFictionalEvent(fixture("fiction-beta"), plain);
    expect(a.events[0].title).toBe(b.events[0].title);
    expect(a.events[0].event_id).not.toBe(b.events[0].event_id);
    expect(b.events[0].universe_id).toBe("fiction-beta");
  });
  it("10 duplicate titles within one Universe retain distinct immutable IDs", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    const b = createFictionalEvent(a, plain);
    expect(b.events[0].event_id).not.toBe(b.events[1].event_id);
    expect(currentFictionalEvents(b)).toHaveLength(2);
  });
  it("11 refuses forging the notebook origin and real G3 permission", () => {
    const a = fixture("fiction-alpha");
    expect(() => inspectFictionalEventNotebook({
      ...a, real_g3_authorized: true,
    } as unknown as typeof a)).toThrow();
    expect(() => inspectFictionalEventNotebook({
      ...a, data_origin: "real_sqlite",
    } as unknown as typeof a)).toThrow();
  });
  it("12 rejects malformed imported event history and mixed universe", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(() => inspectFictionalEventNotebook({
      ...a, events: [{ ...a.events[0], universe_id: "fiction-beta" }],
    })).toThrow();
    expect(() => inspectFictionalEventNotebook({
      ...a, events: [{ ...a.events[0], version: 2 }],
    })).toThrow();
  });
  it("13 rejects empty names, excessive notes and blank amendment reasons", () => {
    const a = fixture("fiction-alpha");
    expect(() => createFictionalEvent(a, { ...plain, title: " " })).toThrow();
    expect(() => createFictionalEvent(a, { ...plain, note: "X".repeat(401) })).toThrow();
    const b = createFictionalEvent(a, plain);
    expect(() => amendFictionalEvent(b, b.events[0].event_id, plain, " ")).toThrow();
  });
  it("14 rejects a historical anchor in the borrowed fictional draft", () => {
    const original = fixture("fiction-alpha");
    const corrected = supersedeFictionalAnchor(original.draft, "B", {
      kind: "unknown", calendar: "", label: "", precision: "",
    });
    const newBook = startFictionalEventNotebook(corrected);
    expect(() => createFictionalEvent(newBook, {
      ...plain, anchor_id: "B",
    })).toThrow();
  });
  it("15 preview remains read-only without persistence or reader reveal", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    const html = renderToStaticMarkup(createElement(M32FictionalEventNotebookPreview,
      { notebook: a }));
    expect(html).toContain("Carnet manuel fictif");
    expect(html).toContain("Première rencontre");
    expect(html).toContain("aucune écriture SQLite");
    expect(html).toContain("aucune révélation du lecteur");
    expect(a.audit).toHaveLength(1);
  });
});

describe("M3.2 fictional event audit lineage adversarial checks", () => {
  function two() {
    const first = createFictionalEvent(fixture("fiction-alpha"), plain);
    return createFictionalEvent(first, { ...plain, title: "Deuxième rencontre" });
  }
  it("16 rejects missing audit for a valid created event", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(() => inspectFictionalEventNotebook({ ...a, audit: [] })).toThrow();
  });
  it("17 rejects extra duplicate audit for a single event", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(() => inspectFictionalEventNotebook({ ...a, audit: [...a.audit, a.audit[0]] })).toThrow();
  });
  it("18 rejects a fabricated audit action without changing versions", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(() => inspectFictionalEventNotebook({
      ...a, audit: [{ ...a.audit[0], action: "amended" }],
    })).toThrow();
  });
  it("19 rejects a changed audit version number even when event is valid", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(() => inspectFictionalEventNotebook({
      ...a, audit: [{ ...a.audit[0], version: 2 }],
    })).toThrow();
  });
  it("20 rejects an audit entry assigned to a different event ID", () => {
    const a = two();
    expect(() => inspectFictionalEventNotebook({
      ...a, audit: [{ ...a.audit[0], event_id: a.events[1].event_id }, a.audit[1]],
    })).toThrow();
  });
  it("21 rejects swapped audit entries between different created events", () => {
    const a = two();
    expect(() => inspectFictionalEventNotebook({
      ...a, audit: [a.audit[1], a.audit[0]],
    })).toThrow();
  });
  it("22 rejects a fabricated creator ID even when the prefix matches", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(() => inspectFictionalEventNotebook({
      ...a, events: [{ ...a.events[0], event_id: "fiction-alpha-event-0042" }],
      audit: [{ ...a.audit[0], event_id: "fiction-alpha-event-0042" }],
    })).toThrow();
  });
  it("23 rejects a forged nextId higher or lower than the creation count", () => {
    const a = two();
    expect(() => inspectFictionalEventNotebook({ ...a, nextId: 4 })).toThrow();
    expect(() => inspectFictionalEventNotebook({ ...a, nextId: 2 })).toThrow();
  });
  it("24 rejects creation history recorded in reversed event order", () => {
    const a = two();
    expect(() => inspectFictionalEventNotebook({
      ...a, events: [a.events[1], a.events[0]],
      audit: [a.audit[1], a.audit[0]],
    })).toThrow();
  });
  it("25 rejects a withdrawn tombstone mislabeled as an amendment", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    const b = withdrawFictionalEvent(a, a.events[0].event_id, "Retrait explicite");
    expect(() => inspectFictionalEventNotebook({
      ...b, audit: [b.audit[0], { ...b.audit[1], action: "amended" }],
    })).toThrow();
  });
  it("26 accepts interleaved creation, amendment and withdrawal as audited lineage", () => {
    let a = two();
    a = amendFictionalEvent(a, a.events[0].event_id, { ...plain, title: "Nouvelle version" },
      "Raison humaine");
    a = withdrawFictionalEvent(a, a.events[1].event_id, "Retrait humain");
    expect(inspectFictionalEventNotebook(a)).toBe(a);
    expect(a.events.map(e => e.version)).toEqual([1, 1, 2, 2]);
    expect(a.audit.map(e => e.action)).toEqual(["created", "created", "amended", "withdrawn"]);
    expect(a.nextId).toBe(3);
  });
  it("27 rejects unexplained audit in otherwise coherent lineage", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(() => inspectFictionalEventNotebook({
      ...a, audit: [{ ...a.audit[0], explanation: " " }],
    })).toThrow();
  });
});
