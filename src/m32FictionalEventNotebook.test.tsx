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
  auditedFictionalEventHistory, compareFictionalEventVersions,
} from "./m32FictionalEventNotebook";
import M32FictionalEventNotebookPreview from "./M32FictionalEventNotebookPreview";
import M32FictionalEventVersionPairLab from "./M32FictionalEventVersionPairLab";
import M32FictionalEventManualWorkshop from "./M32FictionalEventManualWorkshop";

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


describe("M3.2 fictional event withdrawal tombstone integrity negative cases", () => {
  it("28 rejects a version-one withdrawn event despite a matching created audit", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(() => inspectFictionalEventNotebook({
      ...a, events: [{ ...a.events[0], status: "withdrawn" }],
    })).toThrow("retrait sans version précédente");
  });
  it("29 rejects rewriting the title inside a withdrawal tombstone", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    const b = withdrawFictionalEvent(a, a.events[0].event_id, "Retrait humain");
    expect(() => inspectFictionalEventNotebook({
      ...b, events: [b.events[0], { ...b.events[1], title: "Titre clandestin" }],
    })).toThrow("pierre tombale modifiant la version précédente");
  });
  it("30 rejects rewriting the note inside a withdrawal tombstone", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), plain);
    const b = withdrawFictionalEvent(a, a.events[0].event_id, "Retrait humain");
    expect(() => inspectFictionalEventNotebook({
      ...b, events: [b.events[0], { ...b.events[1], note: "Note clandestine" }],
    })).toThrow("pierre tombale modifiant la version précédente");
  });
  it("31 rejects silently removing an anchor and its exact revision at withdrawal", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), linked);
    const b = withdrawFictionalEvent(a, a.events[0].event_id, "Retrait humain");
    expect(() => inspectFictionalEventNotebook({
      ...b, events: [b.events[0], { ...b.events[1],
        anchor_id: null, source_revision_id: null }],
    })).toThrow("pierre tombale modifiant la version précédente");
  });
  it("32 accepts legitimate amend then withdraw retaining the complete last payload", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), linked);
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...linked, title: "Version ajustée", note: "Précision humaine" }, "Motif humain");
    const c = withdrawFictionalEvent(b, a.events[0].event_id, "Retrait motivé");
    expect(inspectFictionalEventNotebook(c)).toBe(c);
    expect(c.events.map(e => e.status)).toEqual(["superseded", "superseded", "withdrawn"]);
    expect(c.events[2].title).toBe(c.events[1].title);
    expect(c.events[2].note).toBe(c.events[1].note);
    expect(c.events[2].anchor_id).toBe(c.events[1].anchor_id);
    expect(c.events[2].source_revision_id).toBe(c.events[1].source_revision_id);
    expect(c.audit.map(audit => audit.action)).toEqual(["created", "amended", "withdrawn"]);
  });
});

describe("M3.2 invented notebook runtime-shape fail-closed checks", () => {
  function created() {
    return createFictionalEvent(fixture("fiction-alpha"), plain);
  }
  function badEvent(a: ReturnType<typeof created>, value: unknown) {
    return { ...a, events: [value] } as unknown as typeof a;
  }
  it("33 rejects null event with a domain refusal rather than raw TypeError", () => {
    const a = created();
    expect(() => inspectFictionalEventNotebook(badEvent(a, null)))
      .toThrow("Carnet M3.2 fictif refusé");
  });
  it("34 rejects primitive event instead of treating it as a record", () => {
    const a = created();
    expect(() => inspectFictionalEventNotebook(badEvent(a, "fiction-alpha-event-0001")))
      .toThrow("Carnet M3.2 fictif refusé");
  });
  it("35 rejects numeric event ID before attempting a string prefix", () => {
    const a = created();
    expect(() => inspectFictionalEventNotebook(badEvent(a, { ...a.events[0], event_id: 42 })))
      .toThrow("Carnet M3.2 fictif refusé");
  });
  it("36 rejects a missing event ID on a structurally plausible version", () => {
    const a = created();
    const { event_id: _omitted, ...withoutId } = a.events[0];
    expect(() => inspectFictionalEventNotebook(badEvent(a, withoutId)))
      .toThrow("Carnet M3.2 fictif refusé");
  });
  it("37 rejects an array impersonating an invented event record", () => {
    const a = created();
    const forged = Object.assign([], a.events[0]);
    expect(() => inspectFictionalEventNotebook(badEvent(a, forged)))
      .toThrow("Carnet M3.2 fictif refusé");
  });
  it("38 rejects an array impersonating an invented audit record", () => {
    const a = created();
    const forged = Object.assign([], a.audit[0]);
    expect(() => inspectFictionalEventNotebook({
      ...a, audit: [forged],
    } as unknown as typeof a)).toThrow("Carnet M3.2 fictif refusé");
  });
  it("39 rejects mutation from a malformed input notebook without changing the original", () => {
    const a = created();
    const tampered = badEvent(a, { ...a.events[0], event_id: 42 });
    expect(() => createFictionalEvent(tampered, plain))
      .toThrow("Carnet M3.2 fictif refusé");
    expect(a.events).toHaveLength(1);
    expect(a.nextId).toBe(2);
  });
  it("40 rejects a root array impersonating a fictional notebook", () => {
    const a = created();
    const forged = Object.assign([], a);
    expect(() => inspectFictionalEventNotebook(forged as unknown as typeof a))
      .toThrow("Carnet M3.2 fictif refusé");
  });
  it("41 preserves legitimate interleaved create, amend and withdraw histories", () => {
    let a = created();
    a = createFictionalEvent(a, { ...plain, title: "Autre événement" });
    a = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, title: "Événement rectifié" }, "Motif humain");
    a = withdrawFictionalEvent(a, a.events[1].event_id, "Retrait humain");
    expect(inspectFictionalEventNotebook(a)).toBe(a);
    expect(a.events.map(e => e.status)).toEqual([
      "superseded", "superseded", "current", "withdrawn",
    ]);
  });
});

describe("M3.2 invented read-only event history: versions and human explanations", () => {
  function first() {
    return createFictionalEvent(fixture("fiction-alpha"), plain);
  }
  it("42 returns aligned create amend withdraw versions including withdrawn tombstone", () => {
    const a = first();
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, title: "Rectification" }, "Justification manuelle");
    const c = withdrawFictionalEvent(b, a.events[0].event_id, "Retrait motivé");
    const entries = auditedFictionalEventHistory(c, a.events[0].event_id);
    expect(entries.map(x => x.event.version)).toEqual([1, 2, 3]);
    expect(entries.map(x => x.event.status)).toEqual([
      "superseded", "superseded", "withdrawn",
    ]);
    expect(entries.map(x => x.audit.action)).toEqual(["created", "amended", "withdrawn"]);
    expect(entries.map(x => x.audit.explanation)).toEqual([
      "Événement créé manuellement en mémoire inventée",
      "Justification manuelle", "Retrait motivé",
    ]);
  });
  it("43 isolates histories across two event IDs despite interleaved operations", () => {
    let a = first();
    const firstId = a.events[0].event_id;
    a = createFictionalEvent(a, { ...plain, title: "Second" });
    const secondId = a.events[1].event_id;
    a = amendFictionalEvent(a, firstId, { ...plain, title: "Première corrigée" }, "Correction");
    a = withdrawFictionalEvent(a, secondId, "Retrait explicite");
    expect(auditedFictionalEventHistory(a, firstId).map(x => x.audit.action))
      .toEqual(["created", "amended"]);
    expect(auditedFictionalEventHistory(a, secondId).map(x => x.audit.action))
      .toEqual(["created", "withdrawn"]);
  });
  it("44 rejects an unknown invented event ID", () => {
    const a = first();
    expect(() => auditedFictionalEventHistory(a, "fiction-alpha-event-0999"))
      .toThrow("historique d'événement fictif absent ou étranger");
  });
  it("45 refuses cross-universe event history lookup without fallback", () => {
    const a = first();
    expect(() => auditedFictionalEventHistory(a, "fiction-beta-event-0001"))
      .toThrow("historique d'événement fictif absent ou étranger");
  });
  it("46 rejects null and numeric untyped selectors instead of producing empty history", () => {
    const a = first();
    for (const value of [null, 7, ""]) {
      expect(() => auditedFictionalEventHistory(a, value as unknown as string))
        .toThrow("historique d'événement fictif absent ou étranger");
    }
  });
  it("47 rejects tampered notebook audit before exposing historical entries", () => {
    const a = first();
    expect(() => auditedFictionalEventHistory({
      ...a, audit: [{ ...a.audit[0], action: "withdrawn" }],
    } as unknown as typeof a, a.events[0].event_id)).toThrow("audit fictif");
  });
  it("48 detaches and freezes display entries without mutating input notebook", () => {
    const a = first();
    const history = auditedFictionalEventHistory(a, a.events[0].event_id);
    expect(Object.isFrozen(history)).toBe(true);
    expect(Object.isFrozen(history[0])).toBe(true);
    expect(Object.isFrozen(history[0].event)).toBe(true);
    expect(Object.isFrozen(history[0].audit)).toBe(true);
    expect(history[0].event).not.toBe(a.events[0]);
    expect(history[0].audit).not.toBe(a.audit[0]);
    expect(a.audit[0].action).toBe("created");
  });
  it("49 renders a withdrawn event and explanations in collapsed accessible HTML", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), {
      ...plain, note: "<script>not-a-command</script>",
    });
    const b = withdrawFictionalEvent(a, a.events[0].event_id, "Choix de l'auteur");
    const html = renderToStaticMarkup(createElement(M32FictionalEventNotebookPreview,
      { notebook: b }));
    expect(html).toContain("Historique des versions fictives");
    expect(html).toContain("<details>");
    expect(html).toContain("retiré");
    expect(html).toContain("Choix de l&#x27;auteur");
    expect(html).toContain("&lt;script&gt;not-a-command&lt;/script&gt;");
    expect(html).not.toContain("<script>");
    expect(html).toContain("aucune écriture SQLite");
    expect(currentFictionalEvents(b)).toHaveLength(0);
  });
});

describe("M3.2 invented-only event history content differences", () => {
  function starting() {
    return createFictionalEvent(fixture("fiction-alpha"), plain);
  }
  it("50 reports no content changes for the initial creation", () => {
    const a = starting();
    expect(auditedFictionalEventHistory(a, a.events[0].event_id)[0].changed_fields).toEqual([]);
  });
  it("51 reports title-only changes without marking unchanged note or links", () => {
    const a = starting();
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, title: "Titre révisé" }, "Motif humain");
    expect(auditedFictionalEventHistory(b, a.events[0].event_id)[1].changed_fields)
      .toEqual(["title"]);
  });
  it("52 reports note-only changes even when title is unchanged", () => {
    const a = starting();
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, note: "Nouvelle note" }, "Motif humain");
    expect(auditedFictionalEventHistory(b, a.events[0].event_id)[1].changed_fields)
      .toEqual(["note"]);
  });
  it("53 reports explicit anchor and revision changes together", () => {
    const a = starting();
    const b = amendFictionalEvent(a, a.events[0].event_id, linked, "Ancrage explicite");
    expect(auditedFictionalEventHistory(b, a.events[0].event_id)[1].changed_fields)
      .toEqual(["anchor_id", "source_revision_id"]);
  });
  it("54 does not report invented content changes for a withdrawal tombstone", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), linked);
    const b = withdrawFictionalEvent(a, a.events[0].event_id, "Choix humain");
    const last = auditedFictionalEventHistory(b, a.events[0].event_id)[1];
    expect(last.audit.action).toBe("withdrawn");
    expect(last.changed_fields).toEqual([]);
  });
  it("55 compares interleaved amendments against the same event, not a neighbor", () => {
    let a = starting();
    const originalId = a.events[0].event_id;
    a = createFictionalEvent(a, { ...plain, title: "Autre personnage" });
    const secondId = a.events[1].event_id;
    a = amendFictionalEvent(a, secondId,
      { ...plain, title: "Autre personnage modifié" }, "Correction deuxième");
    a = amendFictionalEvent(a, originalId, { ...plain, note: "Première note" }, "Correction première");
    expect(auditedFictionalEventHistory(a, originalId)[1].changed_fields).toEqual(["note"]);
    expect(auditedFictionalEventHistory(a, secondId)[1].changed_fields).toEqual(["title"]);
  });
  it("56 freezes difference arrays as detached display-only values", () => {
    const a = starting();
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, title: "Correction" }, "Justification");
    const history = auditedFictionalEventHistory(b, a.events[0].event_id);
    expect(Object.isFrozen(history[1].changed_fields)).toBe(true);
    expect(Object.isFrozen(history[1])).toBe(true);
    expect(b.events[1].title).toBe("Correction");
  });
  it("57 renders accessible version differences with escaped invented input", () => {
    const a = starting();
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, title: "<b>événement</b>", note: "Une note" }, "Correction");
    const html = renderToStaticMarkup(createElement(M32FictionalEventNotebookPreview,
      { notebook: b }));
    expect(html).toContain("modifications de contenu : titre, note");
    expect(html).toContain("modifications de contenu : aucune");
    expect(html).toContain("&lt;b&gt;événement&lt;/b&gt;");
    expect(html).not.toContain("<b>événement</b>");
    expect(html).toContain("<details>");
    expect(html).not.toContain("open=");
  });
});

describe("M3.2 fictional event exact before-after display differences", () => {
  function created() {
    return createFictionalEvent(fixture("fiction-alpha"), plain);
  }
  it("58 initial creation has no before-after pair", () => {
    const a = created();
    expect(auditedFictionalEventHistory(a, a.events[0].event_id)[0].field_differences)
      .toEqual([]);
  });
  it("59 title correction retains exact before and after invented text", () => {
    const a = created();
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, title: "Rencontre ajustée" }, "Motif explicite");
    expect(auditedFictionalEventHistory(b, a.events[0].event_id)[1].field_differences)
      .toEqual([{ field: "title", before: "Première rencontre", after: "Rencontre ajustée" }]);
  });
  it("60 empty and nonempty notes remain distinguishable in history", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), { ...plain, note: "" });
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, note: "Note ajoutée" }, "Précision");
    expect(auditedFictionalEventHistory(b, a.events[0].event_id)[1].field_differences)
      .toEqual([{ field: "note", before: "", after: "Note ajoutée" }]);
  });
  it("61 explicit anchor and exact revision link show null to bound identifiers", () => {
    const a = created();
    const b = amendFictionalEvent(a, a.events[0].event_id, linked, "Lien humain");
    expect(auditedFictionalEventHistory(b, a.events[0].event_id)[1].field_differences)
      .toEqual([
        { field: "anchor_id", before: null, after: "A" },
        { field: "source_revision_id", before: null, after: "fiction-alpha-revision-1" },
      ]);
  });
  it("62 removed temporal link shows exact explicit values to null", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), linked);
    const b = amendFictionalEvent(a, a.events[0].event_id, plain, "Délier manuellement");
    expect(auditedFictionalEventHistory(b, a.events[0].event_id)[1].field_differences)
      .toEqual([
        { field: "anchor_id", before: "A", after: null },
        { field: "source_revision_id", before: "fiction-alpha-revision-1", after: null },
      ]);
  });
  it("63 withdrawal creates no invented before-after content change", () => {
    const a = createFictionalEvent(fixture("fiction-alpha"), linked);
    const b = withdrawFictionalEvent(a, a.events[0].event_id, "Retrait humain");
    expect(auditedFictionalEventHistory(b, a.events[0].event_id)[1].field_differences)
      .toEqual([]);
  });
  it("64 freezes each detached before-after entry without altering the historical notebook", () => {
    const a = created();
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, title: "Titre corrigé" }, "Motif");
    const x = auditedFictionalEventHistory(b, a.events[0].event_id);
    expect(Object.isFrozen(x[1].field_differences)).toBe(true);
    expect(Object.isFrozen(x[1].field_differences[0])).toBe(true);
    expect(x[1].field_differences[0].before).toBe(a.events[0].title);
    expect(b.events[0].title).toBe("Première rencontre");
  });
  it("65 renders explicit before-after labels and React-escapes malicious invented text", () => {
    const a = created();
    const b = amendFictionalEvent(a, a.events[0].event_id,
      { ...plain, title: "<script>mauvais</script>" }, "Motif");
    const html = renderToStaticMarkup(createElement(M32FictionalEventNotebookPreview,
      { notebook: b }));
    expect(html).toContain("Valeurs avant et après fictives");
    expect(html).toContain("avant = Première rencontre");
    expect(html).toContain("après = &lt;script&gt;mauvais&lt;/script&gt;");
    expect(html).not.toContain("<script>");
    expect(html).toContain("<details>");
    expect(html).not.toContain("open=");
  });
});

describe("M3.2 invented-only explicit nonadjacent event-version comparison", () => {
  function created() {
    return createFictionalEvent(fixture("fiction-alpha"), plain);
  }
  it("66 compares first and third versions cumulatively rather than adjacent only", () => {
    const a = created(), id = a.events[0].event_id;
    const b = amendFictionalEvent(a, id, { ...plain, title: "Titre ajusté" }, "Correction titre");
    const c = amendFictionalEvent(b, id,
      { ...plain, title: "Titre ajusté", note: "Note finale" }, "Correction note");
    const diff = compareFictionalEventVersions(c, id, 1, 3);
    expect(diff.field_differences).toEqual([
      { field: "title", before: "Première rencontre", after: "Titre ajusté" },
      { field: "note", before: "Evénement manuel", after: "Note finale" },
    ]);
    expect(diff.to_status).toBe("current");
    expect(diff.from_version).toBe(1);
    expect(diff.to_version).toBe(3);
  });
  it("67 cancels intermediate changes when the final invented value equals the original", () => {
    const a = created(), id = a.events[0].event_id;
    const b = amendFictionalEvent(a, id, { ...plain, title: "Intermédiaire" }, "Correction");
    const c = amendFictionalEvent(b, id, plain, "Rétablissement");
    expect(compareFictionalEventVersions(c, id, 1, 3).field_differences).toEqual([]);
    expect(compareFictionalEventVersions(c, id, 2, 3).field_differences)
      .toEqual([{ field: "title", before: "Intermédiaire", after: "Première rencontre" }]);
  });
  it("68 retains final withdrawal status without inventing content changes", () => {
    const a = created(), id = a.events[0].event_id;
    const b = withdrawFictionalEvent(a, id, "Retrait humain");
    const diff = compareFictionalEventVersions(b, id, 1, 2);
    expect(diff.to_status).toBe("withdrawn");
    expect(diff.field_differences).toEqual([]);
    expect(currentFictionalEvents(b)).toHaveLength(0);
  });
  it("69 rejects equal reversed fractional and nonsafe version selectors", () => {
    const a = created(), id = a.events[0].event_id;
    for (const pair of [[1,1],[2,1],[1,1.5],[1,Number.MAX_SAFE_INTEGER+1],[0,2]]) {
      expect(() => compareFictionalEventVersions(a,id,pair[0],pair[1]))
        .toThrow("comparaison de versions fictives non croissante");
    }
  });
  it("70 refuses absent versions instead of silently falling back", () => {
    const a = created(), id = a.events[0].event_id;
    expect(() => compareFictionalEventVersions(a,id,1,2))
      .toThrow("version fictive absente ou étrangère");
  });
  it("71 refuses different-universe event IDs and untyped null ID", () => {
    const a = created();
    for (const id of ["fiction-beta-event-0001",null]) {
      expect(() => compareFictionalEventVersions(a,id as string,1,2))
        .toThrow("Carnet M3.2 fictif refusé");
    }
  });
  it("72 never compares interleaved versions of neighboring event IDs", () => {
    let a = created();
    const first = a.events[0].event_id;
    a = createFictionalEvent(a,{...plain,title:"Deuxième"});
    const second = a.events[1].event_id;
    a = amendFictionalEvent(a,second,{...plain,title:"Deuxième corrigé"},"Deuxième correction");
    a = amendFictionalEvent(a,first,{...plain,note:"Première corrigée"},"Première correction");
    expect(compareFictionalEventVersions(a,first,1,2).field_differences)
      .toEqual([{field:"note",before:"Evénement manuel",after:"Première corrigée"}]);
    expect(compareFictionalEventVersions(a,second,1,2).field_differences)
      .toEqual([{field:"title",before:"Deuxième",after:"Deuxième corrigé"}]);
  });
  it("73 freezes the detached cumulative result and each difference entry", () => {
    const a = created(), id = a.events[0].event_id;
    const b = amendFictionalEvent(a,id,{...plain,title:"Autre"},"Correction");
    const diff = compareFictionalEventVersions(b,id,1,2);
    expect(Object.isFrozen(diff)).toBe(true);
    expect(Object.isFrozen(diff.field_differences)).toBe(true);
    expect(Object.isFrozen(diff.field_differences[0])).toBe(true);
    expect(a.events[0].title).toBe("Première rencontre");
  });
  it("74 presents cumulative first-to-last values in escaped collapsed fictional HTML", () => {
    const a = created(), id = a.events[0].event_id;
    const b = amendFictionalEvent(a,id,{...plain,title:"<script>test</script>"},"Correction");
    const html = renderToStaticMarkup(createElement(M32FictionalEventNotebookPreview,{notebook:b}));
    expect(html).toContain("Comparaison cumulative des versions fictives");
    expect(html).toContain("version 1 vers version 2");
    expect(html).toContain("après = &lt;script&gt;test&lt;/script&gt;");
    expect(html).not.toContain("<script>");
    expect(html).not.toContain("open=");
  });
});

describe("M3.2 controlled read-only selected-version fictional preview", () => {
  function created() {
    return createFictionalEvent(fixture("fiction-alpha"), plain);
  }
  function html(
    notebook: ReturnType<typeof created>,
    selection?: { event_id: string; from_version: number; to_version: number },
  ) {
    return renderToStaticMarkup(createElement(M32FictionalEventNotebookPreview,
      { notebook, selection }));
  }
  it("75 keeps existing default historical view when no controlled selection is provided", () => {
    const a = created();
    expect(html(a)).not.toContain("Comparaison fictive demandée explicitement");
    expect(html(a)).toContain("Historique manuel des versions");
  });
  it("76 shows the caller-selected middle-to-final version rather than implicit 1-to-last", () => {
    const a = created(), id = a.events[0].event_id;
    const b = amendFictionalEvent(a,id,{...plain,title:"Deuxième"},"Correction");
    const c = amendFictionalEvent(b,id,{...plain,title:"Troisième"},"Correction");
    const markup = html(c,{event_id:id,from_version:2,to_version:3});
    expect(markup).toContain("Comparaison sélectionnée, version 2 vers version 3");
    expect(markup).toContain("avant = Deuxième");
    expect(markup).toContain("après = Troisième");
    expect(markup).toContain("Comparaison manuelle, version 1 vers version 3");
  });
  it("77 never selects a neighboring event accidentally when revisions interleave", () => {
    let a = created();
    const first = a.events[0].event_id;
    a = createFictionalEvent(a,{...plain,title:"Événement voisin"});
    const neighbor = a.events[1].event_id;
    a = amendFictionalEvent(a,neighbor,{...plain,title:"Voisin corrigé"},"Correction");
    a = amendFictionalEvent(a,first,{...plain,note:"Note précise"},"Correction");
    const markup = html(a,{event_id:first,from_version:1,to_version:2});
    const explicit = markup.split('aria-label="Comparaison fictive demandée explicitement"')[1]
      ?.split("</section>")[0];
    expect(explicit).toContain("après = Note précise");
    expect(explicit).not.toContain("Voisin corrigé");
  });
  it("78 rejects reversed and equal version selectors without rendering fallback", () => {
    const a = created(), id = a.events[0].event_id;
    for (const [from_version,to_version] of [[1,1],[2,1],[0,2],[1,1.5]]) {
      expect(() => html(a,{event_id:id,from_version,to_version}))
        .toThrow("comparaison de versions fictives non croissante");
    }
  });
  it("79 refuses absent versions instead of silently falling back to existing history", () => {
    const a = created(), id = a.events[0].event_id;
    expect(() => html(a,{event_id:id,from_version:1,to_version:2}))
      .toThrow("version fictive absente ou étrangère");
  });
  it("80 rejects cross-universe event IDs from a controlled caller", () => {
    const a = created();
    expect(() => html(a,{event_id:"fiction-beta-event-0001",from_version:1,to_version:2}))
      .toThrow("historique d'événement fictif absent ou étranger");
  });
  it("81 rejects malformed null-controlled selections, not a silent default", () => {
    const a = created();
    expect(() => html(a,null as unknown as {event_id:string;from_version:number;to_version:number}))
      .toThrow("Sélection fictive refusée");
    expect(() => html(a,[] as unknown as {event_id:string;from_version:number;to_version:number}))
      .toThrow("Sélection fictive refusée");
  });
  it("82 escapes HTML in caller-selected content and never emits a script", () => {
    const a = created(),id=a.events[0].event_id;
    const b = amendFictionalEvent(a,id,{...plain,title:"<script>attaque</script>"},"Correction");
    const markup = html(b,{event_id:id,from_version:1,to_version:2});
    expect(markup).toContain("Comparaison fictive demandée explicitement");
    expect(markup).toContain("&lt;script&gt;attaque&lt;/script&gt;");
    expect(markup).not.toContain("<script>");
    expect(markup).not.toContain("open=");
  });
  it("83 compares a withdrawn tombstone without manufacturing a content change", () => {
    const a = created(),id=a.events[0].event_id;
    const b = withdrawFictionalEvent(a,id,"Retrait motivé");
    const markup = html(b,{event_id:id,from_version:1,to_version:2});
    expect(markup).toContain("Aucun écart de contenu entre ces deux versions fictives.");
    expect(markup).toContain("withdrawn");
    expect(currentFictionalEvents(b)).toHaveLength(0);
  });
});

describe("M3.2 browser-only fictional version pair selectors", () => {
  it("84 starts with no selected version or implicit comparison", () => {
    const book = createFictionalEvent(fixture("fiction-alpha"), plain);
    const markup = renderToStaticMarkup(createElement(M32FictionalEventVersionPairLab, { notebook: book }));
    expect(markup).toContain("Laboratoire de sélection de versions fictives");
    expect(markup).toContain("Choisir un événement inventé");
    expect(markup).not.toContain('aria-label="Comparaison fictive demandée explicitement"');
  });
  it("85 keeps stable event identity even with a withdrawn historical version", () => {
    const first = createFictionalEvent(fixture("fiction-alpha"), plain);
    const last = withdrawFictionalEvent(first, first.events[0].event_id, "Retrait motivé");
    const markup = renderToStaticMarkup(createElement(M32FictionalEventVersionPairLab, { notebook: last }));
    expect(markup).toContain(first.events[0].event_id);
    expect(markup).toContain("Première rencontre");
    expect(markup).toContain("Historique manuel des versions");
  });
  it("86 fails closed before rendering a forged real SQLite notebook", () => {
    const book = createFictionalEvent(fixture("fiction-alpha"), plain);
    expect(() => renderToStaticMarkup(createElement(M32FictionalEventVersionPairLab,
      { notebook: { ...book, data_origin: "real_sqlite" } as unknown as typeof book }))).toThrow();
  });
  it("87 escapes hostile-looking event labels within a selector option", () => {
    const book = createFictionalEvent(fixture("fiction-alpha"),
      { ...plain, title: "<script>not-executable</script>" });
    const markup = renderToStaticMarkup(createElement(M32FictionalEventVersionPairLab, { notebook: book }));
    expect(markup).toContain("&lt;script&gt;not-executable&lt;/script&gt;");
    expect(markup).not.toContain("<script>");
  });
});

describe("M3.2 live invented workshop compares only its own in-memory event versions", () => {
  function html(book = fixture("fiction-alpha")) {
    return renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: book }));
  }
  it("88 starts with live comparator unmounted and does not alter empty event counts", () => {
    const markup = html();
    expect(markup).toContain("Comparer les versions créées dans cet atelier fictif");
    expect(markup).toContain("Événements courants (0)");
    expect(markup).not.toContain('aria-label="Laboratoire de sélection de versions fictives"');
    expect(markup).toContain('aria-expanded="false"');
  });
  it("89 preserves the original create/amend/withdraw controller without persistence", () => {
    let book = fixture("fiction-alpha");
    book = createFictionalEvent(book, plain);
    const id = book.events[0].event_id;
    book = amendFictionalEvent(book, id, { ...plain, title: "Révision fictive B" },
      "Correction explicite");
    book = withdrawFictionalEvent(book, id, "Retrait motivé");
    const markup = html(book);
    expect(markup).toContain("Événements courants (0)");
    expect(markup).toContain("Historique préservé : ");
    expect(markup).toContain("3 versions");
    expect(markup).not.toContain('aria-label="Laboratoire de sélection de versions fictives"');
  });
  it("90 refuses forged origin before mounting the live workshop or comparing", () => {
    const book = fixture("fiction-alpha");
    expect(() => html({ ...book, data_origin: "real_sqlite" } as unknown as typeof book))
      .toThrow("Carnet M3.2 fictif refusé");
  });
});
