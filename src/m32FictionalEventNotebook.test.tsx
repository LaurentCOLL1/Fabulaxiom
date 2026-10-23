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
  auditedFictionalEventHistory,
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
