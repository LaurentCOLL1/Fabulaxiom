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
  applyFictionalWorkshopAction, eligibleFictionalEventRevisions,
  matchingFictionalEventHistoryIds, pageFictionalEventHistoryIds,
  orderFictionalEventHistoryIds, appendFictionalCalendarAnchor,
  type FictionalWorkshopAction,
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

function inventedTwoNovels(): FictionalEventNotebook {
  const base = invented();
  const snapshot: M32ChronologyProjection = {
    ...base.draft.snapshot,
    anchors: [...base.draft.snapshot.anchors, {
      ...base.draft.snapshot.anchors[1], id: "C",
      source_revision_id: "fiction-alpha-rev-2",
    }],
    narration: [...base.draft.snapshot.narration, {
      ...base.draft.snapshot.narration[0], novel_id: "novel-2",
      novel_title: "Autre roman fictif", scene_id: "scene-2",
      scene_title: "Scène 2", chapter_id: "ch-2", chapter_title: "Chapitre 2",
      chapter_order: 1,
    }],
  };
  const revisions: readonly FictionalRevision[] = [...base.draft.revisions, {
    universe_id: "fiction-alpha", novel_id: "novel-2",
    scene_id: "scene-2", revision_id: "fiction-alpha-rev-2",
    revision_label: "Deuxième révision fictive",
  }];
  return startFictionalEventNotebook(startFictionalDraft(snapshot, revisions));
}

function inventedTwoScenesSameNovel(): FictionalEventNotebook {
  const two = inventedTwoNovels();
  const snapshot: M32ChronologyProjection = {
    ...two.draft.snapshot,
    narration: two.draft.snapshot.narration.map(n => n.scene_id === "scene-2"
      ? { ...n, novel_id: "novel-1", novel_title: "Roman inventé" } : n),
  };
  const revisions: readonly FictionalRevision[] = two.draft.revisions.map(r =>
    r.scene_id === "scene-2" ? { ...r, novel_id: "novel-1" } : r);
  return startFictionalEventNotebook(startFictionalDraft(snapshot, revisions));
}

function inventedTwoExactDates(): FictionalEventNotebook {
  const two = inventedTwoScenesSameNovel();
  const snapshot: M32ChronologyProjection = {
    ...two.draft.snapshot,
    anchors: two.draft.snapshot.anchors.map(a =>
      a.id === "A" || a.id === "C"
        ? { ...a, time_kind: "exact", calendar_name: "calendrier-invente",
            fictional_label: a.id === "A" ? "Jour inventé 1" : "Jour inventé 2",
            precision_text: null }
        : a),
  };
  return startFictionalEventNotebook(startFictionalDraft(snapshot, two.draft.revisions));
}
function inventedTwoCalendars(): FictionalEventNotebook {
  const two = inventedTwoExactDates();
  const snapshot: M32ChronologyProjection = {
    ...two.draft.snapshot,
    anchors: two.draft.snapshot.anchors.map(a =>
      a.id === "C" ? { ...a, calendar_name: "calendrier-invente-b" } : a),
  };
  return startFictionalEventNotebook(startFictionalDraft(snapshot, two.draft.revisions));
}

function inventedFourTimeKinds(): FictionalEventNotebook {
  const base = invented();
  const original = base.draft.snapshot.anchors;
  const universe_id = base.draft.snapshot.universe_id;
  const snapshot: M32ChronologyProjection = {
    ...base.draft.snapshot,
    anchors: [
      { ...original[0], time_kind: "exact", calendar_name: "cycle-invente",
        fictional_label: "Jour inventé 1", precision_text: null },
      { ...original[1], time_kind: "approximate", calendar_name: "cycle-invente",
        fictional_label: null, precision_text: "Autour du solstice fictif" },
      { ...original[1], id: "C", universe_id, time_kind: "relative",
        calendar_name: null, fictional_label: null, precision_text: null },
      { ...original[1], id: "D", universe_id, time_kind: "unknown",
        calendar_name: null, fictional_label: null, precision_text: null },
    ],
  };
  return startFictionalEventNotebook(startFictionalDraft(snapshot, base.draft.revisions));
}


/** P3bn: independent fictional universes, two novels, four temporal anchor kinds. */
function inventedFourKindsTwoNovels(
  universe: "fiction-alpha" | "fiction-beta",
): FictionalEventNotebook {
  const base=invented(universe);
  const a=base.draft.snapshot.anchors;
  const revisionTwo: FictionalRevision={
    universe_id:universe,novel_id:"novel-2",scene_id:"scene-2",
    revision_id:universe+"-rev-2",revision_label:"Deuxième roman inventé",
  };
  const snapshot: M32ChronologyProjection={
    ...base.draft.snapshot,
    anchors:[
      {...a[0],time_kind:"exact" as const,calendar_name:"cycle-fictif",
        fictional_label:"Jour inventé 1",precision_text:null},
      {...a[1],time_kind:"approximate" as const,calendar_name:"cycle-fictif",
        fictional_label:null,precision_text:"Vers la saison fictive"},
      {...a[1],id:"C",time_kind:"relative" as const,calendar_name:null,
        fictional_label:null,precision_text:null,
        source_revision_id:revisionTwo.revision_id},
      {...a[1],id:"D",time_kind:"unknown" as const,calendar_name:null,
        fictional_label:null,precision_text:null},
    ],
    narration:[...base.draft.snapshot.narration,{
      ...base.draft.snapshot.narration[0],novel_id:"novel-2",
      novel_title:"Deuxième roman inventé",chapter_id:"ch-2",
      chapter_title:"Chapitre 2",chapter_order:1,
      scene_id:"scene-2",scene_title:"Scène 2",
    }],
  };
  return startFictionalEventNotebook(startFictionalDraft(snapshot,
    [...base.draft.revisions,revisionTwo]));
}

import { addFictionalCalendar } from "./M32ManualChronologyLab";

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
    expect(html).not.toContain("value=\"fiction-alpha-rev-1\"");
    expect(html).toContain("Aucune source historique n’est sélectionnée automatiquement.");
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
  it("19 offers only the exact current anchor revision, without implicit selection", () => {
    const book = invented();
    const unrelated = { ...book.draft.revisions[0],
      revision_id: "fiction-alpha-rev-unused", revision_label: "Autre source inventée" };
    const withUnrelated: FictionalEventNotebook = {
      ...book, draft: { ...book.draft,
        revisions: [...book.draft.revisions, unrelated] },
    };
    const before = JSON.stringify(withUnrelated);
    expect(eligibleFictionalEventRevisions(withUnrelated, "")).toEqual([]);
    expect(eligibleFictionalEventRevisions(withUnrelated, "B")).toEqual([]);
    expect(eligibleFictionalEventRevisions(withUnrelated, "missing")).toEqual([]);
    expect(eligibleFictionalEventRevisions(withUnrelated, "A")
      .map(revision => revision.revision_id)).toEqual(["fiction-alpha-rev-1"]);
    expect(JSON.stringify(withUnrelated)).toBe(before);
  });


  it("20 exposes an explicit read-only history picker without implicit inspection", () => {
    const book = create(), before = JSON.stringify(book);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: book }));
    expect(html).toContain("Historique détaillé des événements fictifs");
    expect(html).toContain("Événement fictif à examiner");
    expect(html).toContain(book.events[0].event_id);
    expect(html).toContain("aucune restauration");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("21 keeps a withdrawn event selectable as history without restoring it", () => {
    const first = create(), id = first.events[0].event_id;
    const withdrawn = applyFictionalWorkshopAction(first, {
      kind: "withdraw", eventId: id, reason: "Motif humain de retrait inventé",
    });
    expect(currentFictionalEvents(withdrawn)).toHaveLength(0);
    const before = JSON.stringify(withdrawn);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: withdrawn }));
    expect(html).toContain("Événements courants (0)");
    expect(html).toContain(`value="${id}"`);
    expect(html).not.toContain("Versions historiques fictives");
    expect(html).not.toContain("Restaurer en production");
    expect(JSON.stringify(withdrawn)).toBe(before);
  });

  it("22 filters invented event IDs by latest status, retaining withdrawn tombstones", () => {
    const first = create(), withdrawnId = first.events[0].event_id;
    const withdrawn = applyFictionalWorkshopAction(first, {
      kind: "withdraw", eventId: withdrawnId, reason: "Retrait fictif choisi",
    });
    const mixed = create(withdrawn), activeId = mixed.events[mixed.events.length - 1].event_id;
    const before = JSON.stringify(mixed);
    expect(matchingFictionalEventHistoryIds(mixed, "", "all"))
      .toEqual([withdrawnId, activeId]);
    expect(matchingFictionalEventHistoryIds(mixed, "", "withdrawn"))
      .toEqual([withdrawnId]);
    expect(matchingFictionalEventHistoryIds(mixed, "", "current"))
      .toEqual([activeId]);
    expect(matchingFictionalEventHistoryIds(mixed, "EVENT-0001", "withdrawn"))
      .toEqual([withdrawnId]);
    expect(matchingFictionalEventHistoryIds(mixed, "non-existent", "all"))
      .toEqual([]);
    expect(JSON.stringify(mixed)).toBe(before);
  });
  it("23 renders the search/status controls without implicit historical inspection", () => {
    const created = create(), id = created.events[0].event_id;
    const withdrawn = applyFictionalWorkshopAction(created, {
      kind: "withdraw", eventId: id, reason: "Retrait pour témoin inventé",
    });
    const before = JSON.stringify(withdrawn);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: withdrawn }));
    expect(html).toContain("Rechercher un identifiant d&#x27;événement fictif");
    expect(html).toContain("Filtrer l&#x27;historique par statut");
    expect(html).toContain("Événements retirés seulement");
    expect(html).toContain(`value="${id}"`);
    expect(html).not.toContain("Versions historiques fictives");
    expect(html).not.toContain("Motif humain historique :");
    expect(html).not.toContain("Retrait pour témoin inventé");
    expect(JSON.stringify(withdrawn)).toBe(before);
  });

  it("24 pages 12 fictional IDs and retains withdrawn history without mutation", () => {
    let book = invented();
    for (let i = 0; i < 12; i++) book = create(book);
    const withdrawnId = book.events[0].event_id;
    book = applyFictionalWorkshopAction(book, {
      kind: "withdraw", eventId: withdrawnId, reason: "Retrait conservé",
    });
    const before = JSON.stringify(book);
    const ids = matchingFictionalEventHistoryIds(book, "", "all");
    expect(ids).toHaveLength(12);
    expect(pageFictionalEventHistoryIds(ids, 0).ids).toEqual(ids.slice(0, 10));
    expect(pageFictionalEventHistoryIds(ids, 1).ids).toEqual(ids.slice(10));
    expect(pageFictionalEventHistoryIds(ids, 30).index).toBe(1);
    expect(pageFictionalEventHistoryIds(ids, 1).pages).toBe(2);
    expect(pageFictionalEventHistoryIds(
      matchingFictionalEventHistoryIds(book, "", "withdrawn"), 0).ids)
      .toEqual([withdrawnId]);
    expect(pageFictionalEventHistoryIds([], 10))
      .toEqual({ ids: [], index: 0, pages: 1, total: 0 });
    expect(() => pageFictionalEventHistoryIds(ids, -1)).toThrow();
    expect(() => pageFictionalEventHistoryIds(ids, 1.5)).toThrow();
    expect(JSON.stringify(book)).toBe(before);
  });
  it("25 SSR shows first ID page only and no history contents before selection", () => {
    let book = invented();
    for (let i = 0; i < 12; i++) book = create(book);
    const before = JSON.stringify(book);
    const ids = matchingFictionalEventHistoryIds(book, "", "all");
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: book }));
    expect(html).toContain("Page 1 sur 2");
    expect(html).toContain('role="note" aria-live="polite"');
    expect(html).not.toContain('role="status">Page');
    expect(html).toContain("12 identifiants fictifs trouvés");
    expect(html).toContain(`value="${ids[9]}"`);
    expect(html).not.toContain(`value="${ids[10]}"`);
    expect(html).toContain("Page précédente");
    expect(html).toContain("Page suivante");
    expect(html).not.toContain("Versions historiques fictives");
    expect(html).not.toContain("Motif humain historique :");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("26 exact source ID filter finds superseded source and withdrawn tombstone", () => {
    const a = applyFictionalWorkshopAction(invented(), {
      kind: "create", input: { ...input, anchor_id: "A",
        source_revision_id: "fiction-alpha-rev-1" },
    }), id = a.events[0].event_id;
    const b = change(a, id);
    const c = applyFictionalWorkshopAction(b, {
      kind: "withdraw", eventId: id, reason: "Retrait fictif",
    }), mixed = create(c), before = JSON.stringify(mixed);
    expect(matchingFictionalEventHistoryIds(mixed, "", "all", "fiction-alpha-rev-1"))
      .toEqual([id]);
    expect(matchingFictionalEventHistoryIds(mixed, "", "withdrawn",
      " fiction-alpha-rev-1 ")).toEqual([id]);
    expect(matchingFictionalEventHistoryIds(mixed, "", "current", "fiction-alpha-rev-1"))
      .toEqual([]);
    expect(matchingFictionalEventHistoryIds(mixed, "", "all", "fiction-alpha-rev"))
      .toEqual([]);
    expect(matchingFictionalEventHistoryIds(mixed, "", "all", "FICTION-ALPHA-REV-1"))
      .toEqual([]);
    expect(matchingFictionalEventHistoryIds(mixed, "", "all", "")).toHaveLength(2);
    expect(JSON.stringify(mixed)).toBe(before);
  });
  it("27 SSR source filter does not inspect unselected historical data", () => {
    const b = applyFictionalWorkshopAction(invented(), {
      kind: "create", input: { ...input, note: "NOTE-CACHEE-SOURCE",
        anchor_id: "A", source_revision_id: "fiction-alpha-rev-1" },
    }), before = JSON.stringify(b);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: b }));
    expect(html).toContain("Filtrer par ID exact de révision source fictive");
    expect(html).not.toContain("NOTE-CACHEE-SOURCE");
    expect(html).not.toContain("Versions historiques fictives");
    expect(html).not.toContain("Motif humain historique :");
    expect(html).toContain("Page 1 sur 1");
    expect(JSON.stringify(b)).toBe(before);
  });

  it("28 filters fiction-only source novel and requires same historical version", () => {
    const first = applyFictionalWorkshopAction(inventedTwoNovels(), {
      kind: "create", input: { ...input, anchor_id: "A",
        source_revision_id: "fiction-alpha-rev-1" },
    }), oldId = first.events[0].event_id;
    const second = applyFictionalWorkshopAction(first, {
      kind: "create", input: { ...input, anchor_id: "C",
        source_revision_id: "fiction-alpha-rev-2" },
    }), newId = second.events[second.events.length - 1].event_id;
    const amended = applyFictionalWorkshopAction(second, {
      kind: "amend", eventId: oldId, reason: "Changement de roman fictif",
      input: { ...input, title: "Déplacement volontaire",
        anchor_id: "C", source_revision_id: "fiction-alpha-rev-2" },
    });
    const withdrawn = applyFictionalWorkshopAction(amended, {
      kind: "withdraw", eventId: oldId, reason: "Retrait fictif volontaire",
    });
    const book = create(withdrawn), before = JSON.stringify(book);
    const ids = (source: string, novel: string,
      status: "all" | "current" | "withdrawn" = "all") =>
      matchingFictionalEventHistoryIds(book, "", status, source, novel);
    expect(ids("", "novel-1")).toEqual([oldId]);
    expect(ids("", "novel-2")).toEqual([oldId, newId]);
    expect(ids("", "novel-2", "current")).toEqual([newId]);
    expect(ids("", "novel-1", "withdrawn")).toEqual([oldId]);
    expect(ids("fiction-alpha-rev-1", "novel-2")).toEqual([]);
    expect(ids("fiction-alpha-rev-2", "novel-1")).toEqual([]);
    expect(ids("fiction-alpha-rev-2", "novel-2")).toEqual([oldId, newId]);
    expect(ids("", "NOVEL-2")).toEqual([]);
    expect(ids("", "unknown-novel")).toEqual([]);
    expect(ids("", "")).toHaveLength(3);
    expect(JSON.stringify(book)).toBe(before);
  });
  it("29 SSR exposes novel ID options but not unselected historic notes", () => {
    const a = applyFictionalWorkshopAction(inventedTwoNovels(), {
      kind: "create", input: { ...input, note: "DONNEE-HISTORIQUE-PRIVEE",
        anchor_id: "C", source_revision_id: "fiction-alpha-rev-2" },
    });
    const before = JSON.stringify(a);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: a }));
    expect(html).toContain("Filtrer par roman de révision source fictive");
    expect(html).toContain('value="novel-1"');
    expect(html).toContain('value="novel-2"');
    expect(html).not.toContain("DONNEE-HISTORIQUE-PRIVEE");
    expect(html).not.toContain("Versions historiques fictives");
    expect(html).not.toContain("Motif humain historique :");
    expect(JSON.stringify(a)).toBe(before);
  });

  it("30 filters source scenes within one novel without cross-version pairing", () => {
    const first = applyFictionalWorkshopAction(inventedTwoScenesSameNovel(), {
      kind: "create", input: { ...input,
        anchor_id: "A", source_revision_id: "fiction-alpha-rev-1" },
    }), oldId = first.events[0].event_id;
    const second = applyFictionalWorkshopAction(first, {
      kind: "create", input: { ...input,
        anchor_id: "C", source_revision_id: "fiction-alpha-rev-2" },
    }), newId = second.events[second.events.length - 1].event_id;
    const amended = applyFictionalWorkshopAction(second, {
      kind: "amend", eventId: oldId, reason: "Changement de scène fictive",
      input: { ...input, title: "Scène corrigée",
        anchor_id: "C", source_revision_id: "fiction-alpha-rev-2" },
    });
    const withdrawn = applyFictionalWorkshopAction(amended, {
      kind: "withdraw", eventId: oldId, reason: "Retrait fictif",
    }), book = create(withdrawn), before = JSON.stringify(book);
    const ids = (source: string, novel: string, scene: string,
      status: "all" | "current" | "withdrawn" = "all") =>
      matchingFictionalEventHistoryIds(book, "", status, source, novel, scene);
    expect(ids("", "novel-1", "scene-1")).toEqual([oldId]);
    expect(ids("", "novel-1", "scene-2")).toEqual([oldId, newId]);
    expect(ids("", "novel-1", "scene-2", "current")).toEqual([newId]);
    expect(ids("", "novel-1", "scene-1", "withdrawn")).toEqual([oldId]);
    expect(ids("fiction-alpha-rev-1", "novel-1", "scene-2")).toEqual([]);
    expect(ids("fiction-alpha-rev-2", "novel-1", "scene-1")).toEqual([]);
    expect(ids("fiction-alpha-rev-2", "novel-1", "scene-2")).toEqual([oldId, newId]);
    expect(ids("", "", "SCENE-2")).toEqual([]);
    expect(ids("", "", "nonexistent-scene")).toEqual([]);
    expect(ids("", "", "")).toHaveLength(3);
    expect(JSON.stringify(book)).toBe(before);
  });
  it("31 SSR shows only opaque source-scene IDs before historical inspection", () => {
    const book = applyFictionalWorkshopAction(inventedTwoScenesSameNovel(), {
      kind: "create", input: { ...input, note: "SECRET-SCENE-HISTORIQUE",
        anchor_id: "C", source_revision_id: "fiction-alpha-rev-2" },
    }), before = JSON.stringify(book);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: book }));
    expect(html).toContain("Filtrer par scène de révision source fictive");
    expect(html).toContain('value="scene-1"');
    expect(html).toContain('value="scene-2"');
    expect(html).not.toContain("SECRET-SCENE-HISTORIQUE");
    expect(html).not.toContain("Versions historiques fictives");
    expect(html).not.toContain("Motif humain historique :");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("32 rejects a novel-scene tuple absent from the same fictional source revision", () => {
    const a = applyFictionalWorkshopAction(inventedTwoNovels(), {
      kind: "create", input: { ...input, anchor_id: "A",
        source_revision_id: "fiction-alpha-rev-1" },
    }), oldId = a.events[0].event_id;
    const b = applyFictionalWorkshopAction(a, {
      kind: "amend", eventId: oldId, reason: "Roman fictif modifié",
      input: { ...input, anchor_id: "C", source_revision_id: "fiction-alpha-rev-2" },
    });
    const before = JSON.stringify(b);
    expect(matchingFictionalEventHistoryIds(b, "", "all", "", "novel-1", "scene-2"))
      .toEqual([]);
    expect(matchingFictionalEventHistoryIds(b, "", "all", "", "novel-2", "scene-1"))
      .toEqual([]);
    expect(matchingFictionalEventHistoryIds(b, "", "all",
      "fiction-alpha-rev-1", "novel-1", "scene-1")).toEqual([oldId]);
    expect(matchingFictionalEventHistoryIds(b, "", "all",
      "fiction-alpha-rev-2", "novel-2", "scene-2")).toEqual([oldId]);
    expect(JSON.stringify(b)).toBe(before);
  });

  it("33 filters exact fictional historical anchor and date label, same version", () => {
    const a = applyFictionalWorkshopAction(inventedTwoExactDates(), {
      kind: "create", input: { ...input, anchor_id: "A",
        source_revision_id: "fiction-alpha-rev-1" },
    }), id = a.events[0].event_id;
    const b = applyFictionalWorkshopAction(a, {
      kind: "amend", eventId: id, reason: "Date fictive corrigée",
      input: { ...input, anchor_id: "C", source_revision_id: "fiction-alpha-rev-2" },
    });
    const withdrawn = applyFictionalWorkshopAction(b, {
      kind: "withdraw", eventId: id, reason: "Retrait inventé",
    }), before = JSON.stringify(withdrawn);
    const ids = (source: string, novel: string, scene: string,
      anchor: string, date: string, status: "all" | "current" | "withdrawn" = "all") =>
      matchingFictionalEventHistoryIds(withdrawn, "", status,
        source, novel, scene, anchor, date);
    expect(ids("", "", "", "A", "Jour inventé 1")).toEqual([id]);
    expect(ids("", "", "", "C", "Jour inventé 2", "withdrawn")).toEqual([id]);
    expect(ids("", "", "", "A", "Jour inventé 2")).toEqual([]);
    expect(ids("", "", "", "C", "Jour inventé 1")).toEqual([]);
    expect(ids("fiction-alpha-rev-1", "novel-1", "scene-1",
      "C", "Jour inventé 2")).toEqual([]);
    expect(ids("fiction-alpha-rev-2", "novel-1", "scene-2",
      "C", "Jour inventé 2")).toEqual([id]);
    expect(ids("", "", "", "A", "jour inventé 1")).toEqual([]);
    expect(ids("", "", "", "unknown", "")).toEqual([]);
    expect(ids("", "", "", "", "Jour inventé 1", "current")).toEqual([]);
    expect(JSON.stringify(withdrawn)).toBe(before);
  });
  it("34 keeps unknown and source-less versions out of exact-date filters", () => {
    const book = create(inventedTwoExactDates());
    const before = JSON.stringify(book);
    expect(matchingFictionalEventHistoryIds(book, "", "all",
      "", "", "", "", "Jour inventé 1")).toEqual([]);
    expect(matchingFictionalEventHistoryIds(book, "", "all",
      "", "", "", "B", "")).toEqual([]);
    expect(matchingFictionalEventHistoryIds(book, "", "all")).toHaveLength(1);
    expect(JSON.stringify(book)).toBe(before);
  });
  it("35 SSR source anchor/date selectors do not expose unselected history", () => {
    const book = applyFictionalWorkshopAction(inventedTwoExactDates(), {
      kind: "create", input: { ...input, note: "NOTE-HISTORIQUE-INVISIBLE",
        anchor_id: "A", source_revision_id: "fiction-alpha-rev-1" },
    });
    const before = JSON.stringify(book);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: book }));
    expect(html).toContain("Filtrer par ID exact d&#x27;ancre historique fictive");
    expect(html).toContain("Filtrer par libellé exact de date fictive");
    expect(html).toContain('value="A"');
    expect(html).toContain('value="Jour inventé 1"');
    expect(html).not.toContain("NOTE-HISTORIQUE-INVISIBLE");
    expect(html).not.toContain("Motif humain historique :");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });

  it("36 filters exact calendar of the same fictional historical version", () => {
    const a = applyFictionalWorkshopAction(inventedTwoCalendars(), {
      kind: "create", input: { ...input, anchor_id: "A",
        source_revision_id: "fiction-alpha-rev-1" },
    }), id = a.events[0].event_id;
    const b = applyFictionalWorkshopAction(a, {
      kind: "amend", eventId: id, reason: "Calendrier fictif corrigé",
      input: { ...input, anchor_id: "C", source_revision_id: "fiction-alpha-rev-2" },
    });
    const book = applyFictionalWorkshopAction(b, {
      kind: "withdraw", eventId: id, reason: "Retrait fictif",
    }), before = JSON.stringify(book);
    const ids = (source: string, anchor: string, date: string, calendar: string) =>
      matchingFictionalEventHistoryIds(book, "", "withdrawn",
        source, "novel-1", "", anchor, date, calendar);
    expect(ids("fiction-alpha-rev-1","A","Jour inventé 1","calendrier-invente")).toEqual([id]);
    expect(ids("fiction-alpha-rev-2","C","Jour inventé 2","calendrier-invente-b")).toEqual([id]);
    expect(ids("fiction-alpha-rev-1","C","Jour inventé 2","calendrier-invente-b")).toEqual([]);
    expect(ids("","A","Jour inventé 1","calendrier-invente-b")).toEqual([]);
    expect(ids("","A","Jour inventé 2","calendrier-invente")).toEqual([]);
    expect(ids("","","","CALENDRIER-INVENTE")).toEqual([]);
    expect(JSON.stringify(book)).toBe(before);
  });

  it("37 SSR calendar choices never expose unselected history notes", () => {
    const book = applyFictionalWorkshopAction(inventedTwoCalendars(), {
      kind: "create", input: { ...input, note: "SECRET-CALENDRIER",
        anchor_id: "A", source_revision_id: "fiction-alpha-rev-1" },
    }), before = JSON.stringify(book);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: book }));
    expect(html).toContain("Filtrer par nom exact de calendrier historique fictif");
    expect(html).toContain('value="calendrier-invente"');
    expect(html).toContain('value="calendrier-invente-b"');
    expect(html).not.toContain("SECRET-CALENDRIER");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });

  it("38 shows an explicit reset button without inspecting fictional history", () => {
    const book=applyFictionalWorkshopAction(inventedTwoCalendars(), {
      kind:"create",input:{...input, note:"SECRET-HISTORY-RESET",
        anchor_id:"A",source_revision_id:"fiction-alpha-rev-1"},
    }), before=JSON.stringify(book);
    const html=renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      {initial:book}));
    expect(html).toContain('type="button"');
    expect(html).toContain("Réinitialiser les filtres historiques fictifs");
    expect(html).not.toContain("SECRET-HISTORY-RESET");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });

  it("39 only permits bounded 5 10 20 fictional IDs per page", () => {
    let book = invented();
    for (let i = 0; i < 12; i++) book = create(book);
    const before = JSON.stringify(book);
    const ids = matchingFictionalEventHistoryIds(book, "", "all");
    const first = pageFictionalEventHistoryIds(ids, 0, 5);
    expect(first).toEqual({ ids: ids.slice(0, 5), index: 0, pages: 3, total: 12 });
    expect(pageFictionalEventHistoryIds(ids, 1, 5).ids).toEqual(ids.slice(5, 10));
    expect(pageFictionalEventHistoryIds(ids, 99, 5).ids).toEqual(ids.slice(10));
    expect(pageFictionalEventHistoryIds(ids, 0, 10).ids).toEqual(ids.slice(0, 10));
    expect(pageFictionalEventHistoryIds(ids, 0, 20)).toEqual({
      ids, index: 0, pages: 1, total: 12,
    });
    expect(pageFictionalEventHistoryIds([], 1, 20))
      .toEqual({ ids: [], index: 0, pages: 1, total: 0 });
    for (const size of [-1, 0, 4, 6, 11, 64, 5.5, Number.NaN, Infinity]) {
      expect(() => pageFictionalEventHistoryIds(ids, 0, size)).toThrow(
        "Taille de page fictive invalide");
    }
    expect(() => pageFictionalEventHistoryIds(ids, -1, 5)).toThrow();
    expect(JSON.stringify(book)).toBe(before);
  });

  it("40 SSR exposes only bounded page sizes and hides unselected notes", () => {
    let book = invented();
    for (let i = 0; i < 12; i++) book = create(book);
    const secret = applyFictionalWorkshopAction(book, {
      kind: "amend", eventId: book.events[0].event_id,
      reason: "MOTIF-SECRET-PAGINATION",
      input: { ...input, note: "NOTE-SECRET-PAGINATION" },
    });
    const before = JSON.stringify(secret);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: secret }));
    expect(html).toContain("Identifiants fictifs par page");
    expect(html).toContain('value="5"');
    expect(html).toContain('value="10"');
    expect(html).toContain('value="20"');
    expect(html).toContain("Page 1 sur 2");
    expect(html).not.toContain("NOTE-SECRET-PAGINATION");
    expect(html).not.toContain("MOTIF-SECRET-PAGINATION");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(secret)).toBe(before);
  });

  it("41 reverses fictional ID display, including withdrawal, without mutation", () => {
    let book = invented();
    for (let i = 0; i < 12; i++) book = create(book);
    const withdrawn = book.events[0].event_id;
    book = applyFictionalWorkshopAction(book, {
      kind: "withdraw", eventId: withdrawn, reason: "Retrait inventé",
    });
    const before = JSON.stringify(book);
    const ids = matchingFictionalEventHistoryIds(book, "", "all");
    expect(ids).toHaveLength(12);
    expect(ids).toContain(withdrawn);
    expect(orderFictionalEventHistoryIds(ids, "insertion")).toEqual(ids);
    const inverted = orderFictionalEventHistoryIds(ids, "reverse-insertion");
    expect(inverted).toEqual([...ids].reverse());
    expect(pageFictionalEventHistoryIds(inverted, 0, 5).ids).toEqual(
      [...ids].reverse().slice(0, 5));
    expect(() => orderFictionalEventHistoryIds(ids, "world" as never))
      .toThrow("Ordre de consultation fictif invalide");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("42 SSR shows only order choices, no unselected historical notes", () => {
    const first = create(invented());
    const book = applyFictionalWorkshopAction(first, {
      kind: "amend", eventId: first.events[0].event_id,
      reason: "MOTIF-SECRET-ORDRE",
      input: { ...input, note: "NOTE-SECRET-ORDRE" },
    });
    const before = JSON.stringify(book);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: book }));
    expect(html).toContain("Ordre d&#x27;ajout des identifiants fictifs");
    expect(html).toContain('value="reverse-insertion"');
    expect(html).toContain("jamais l&#x27;ordre du monde");
    expect(html).not.toContain("NOTE-SECRET-ORDRE");
    expect(html).not.toContain("MOTIF-SECRET-ORDRE");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("43 historical time-kind filter covers four explicit anchor kinds, one version at a time", () => {
    let book = inventedFourTimeKinds();
    const make = (anchor_id: string | null, source_revision_id: string | null) => {
      book = applyFictionalWorkshopAction(book, {
        kind: "create", input: { ...input, anchor_id, source_revision_id },
      });
      return book.events[book.events.length - 1].event_id;
    };
    const e1 = make("A", "fiction-alpha-rev-1");
    const e2 = make("B", null);
    const e3 = make("C", null);
    const e4 = make("D", null);
    make(null, null);
    book = applyFictionalWorkshopAction(book, {
      kind: "amend", eventId: e1, reason: "Correction fictive du type",
      input: { ...input, anchor_id: "B", source_revision_id: null },
    });
    book = applyFictionalWorkshopAction(book, {
      kind: "withdraw", eventId: e3, reason: "Retrait fictif conservé",
    });
    const before = JSON.stringify(book);
    const ids = (kind: "exact"|"approximate"|"relative"|"unknown",
      source = "", status: "all"|"withdrawn" = "all") =>
      matchingFictionalEventHistoryIds(book, "", status,
        source, "", "", "", "", "", kind);
    expect(ids("exact")).toEqual([e1]);
    expect(ids("approximate")).toEqual([e1, e2]);
    expect(ids("relative")).toEqual([e3]);
    expect(ids("unknown")).toEqual([e4]);
    expect(ids("relative", "", "withdrawn")).toEqual([e3]);
    expect(ids("approximate", "fiction-alpha-rev-1")).toEqual([]);
    expect(ids("exact", "fiction-alpha-rev-1")).toEqual([e1]);
    expect(() => matchingFictionalEventHistoryIds(book, "", "all",
      "", "", "", "", "", "", "invalid" as never))
      .toThrow("Type temporel fictif invalide");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("44 SSR temporal-kind controls hide all unselected historical reasons", () => {
    const initial = inventedFourTimeKinds();
    const created = applyFictionalWorkshopAction(initial, {
      kind: "create", input: { ...input, anchor_id: "A",
        source_revision_id: "fiction-alpha-rev-1", note: "NOTE-SECRET-TEMPS" },
    });
    const book = applyFictionalWorkshopAction(created, {
      kind: "amend", eventId: created.events[0].event_id,
      reason: "MOTIF-SECRET-TEMPS",
      input: { ...input, anchor_id: "B", source_revision_id: null },
    });
    const before = JSON.stringify(book);
    const html = renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      { initial: book }));
    expect(html).toContain("Filtrer par type temporel historique fictif");
    for (const kind of ["exact", "approximate", "relative", "unknown"]) {
      expect(html).toContain('value="' + kind + '"');
    }
    expect(html).toContain("Sans ancre ne signifie pas temps inconnu attesté.");
    expect(html).not.toContain("NOTE-SECRET-TEMPS");
    expect(html).not.toContain("MOTIF-SECRET-TEMPS");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("45 anchor linkage filters per historical version without conflating unknown time", () => {
    let book = inventedFourTimeKinds();
    book = applyFictionalWorkshopAction(book, {
      kind: "create", input: { ...input, anchor_id: "D", source_revision_id: null },
    });
    const firstId=book.events[0].event_id;
    book = applyFictionalWorkshopAction(book, {
      kind: "amend", eventId: firstId, reason: "Détachement fictif volontaire",
      input: { ...input, anchor_id: null, source_revision_id: null },
    });
    book = applyFictionalWorkshopAction(book, {
      kind: "create", input: { ...input, anchor_id: null, source_revision_id: null },
    });
    const secondId=book.events[book.events.length-1].event_id;
    book=applyFictionalWorkshopAction(book, {
      kind: "withdraw", eventId: secondId, reason: "Retrait fictif historique",
    });
    const snapshot=JSON.stringify(book);
    const filter=(kind: ""|"unknown",link: ""|"linked"|"unlinked",
      anchor="")=>matchingFictionalEventHistoryIds(book,"","all",
        "","","",anchor,"","",kind,link);
    expect(filter("unknown","linked")).toEqual([firstId]);
    expect(filter("unknown","unlinked")).toEqual([]);
    expect(filter("","unlinked")).toEqual([firstId,secondId]);
    expect(filter("","linked")).toEqual([firstId]);
    expect(filter("","unlinked","D")).toEqual([]);
    expect(filter("unknown","linked","D")).toEqual([firstId]);
    expect(matchingFictionalEventHistoryIds(book,"","withdrawn",
      "","","","","","","","unlinked")).toEqual([secondId]);
    expect(()=>matchingFictionalEventHistoryIds(book,"","all",
      "","","","","","","","bogus" as never))
      .toThrow("Lien d'ancre fictive invalide");
    expect(JSON.stringify(book)).toBe(snapshot);
  });
  it("46 SSR anchor linkage choice remains opaque until user selects a history", () => {
    const first = applyFictionalWorkshopAction(inventedFourTimeKinds(), {
      kind: "create", input: { ...input, anchor_id: "D", source_revision_id: null,
        note: "NOTE-SECRET-LIAISON" },
    });
    const book = applyFictionalWorkshopAction(first, {
      kind: "amend", eventId: first.events[0].event_id,
      reason: "MOTIF-SECRET-LIAISON",
      input: { ...input, anchor_id: null, source_revision_id: null },
    });
    const before=JSON.stringify(book);
    const html=renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,
      {initial:book}));
    expect(html).toContain("Filtrer par présence d&#x27;ancre historique fictive");
    expect(html).toContain('value="linked"');
    expect(html).toContain('value="unlinked"');
    expect(html).toContain("Sans ancre ne vaut jamais");
    expect(html).not.toContain("NOTE-SECRET-LIAISON");
    expect(html).not.toContain("MOTIF-SECRET-LIAISON");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });

  it("47 source-link filter remains scoped to one version and separated from anchors",()=>{
    let book=applyFictionalWorkshopAction(invented(),{kind:"create",input:{
      ...input,anchor_id:"A",source_revision_id:"fiction-alpha-rev-1"}});
    const id=book.events[0].event_id;
    book=applyFictionalWorkshopAction(book,{kind:"amend",eventId:id,
      reason:"Découplage inventé",input:{...input,anchor_id:"B",source_revision_id:null}});
    book=applyFictionalWorkshopAction(book,{kind:"create",input});
    const other=book.events[book.events.length-1].event_id;
    book=applyFictionalWorkshopAction(book,{kind:"withdraw",eventId:other,
      reason:"Retrait inventé"});
    const before=JSON.stringify(book);
    const filter=(source:string,link:""|"linked"|"unlinked",
      anchor="",anchorLink:""|"linked"|"unlinked"="")=>
      matchingFictionalEventHistoryIds(book,"","all",source,"","",anchor,
        "","","",anchorLink,link);
    expect(filter("","linked")).toEqual([id]);
    expect(filter("","unlinked")).toEqual([id,other]);
    expect(filter("fiction-alpha-rev-1","unlinked")).toEqual([]);
    expect(filter("fiction-alpha-rev-1","linked")).toEqual([id]);
    expect(filter("","unlinked","B","linked")).toEqual([id]);
    expect(filter("","linked","","unlinked")).toEqual([]);
    expect(matchingFictionalEventHistoryIds(book,"","withdrawn",
      "","","","","","","","","unlinked")).toEqual([other]);
    expect(()=>matchingFictionalEventHistoryIds(book,"","all",
      "","","","","","","","","invalid" as never))
      .toThrow("Lien de révision source fictive invalide");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("48 SSR exposes source link options but hides private unselected past",()=>{
    const first=applyFictionalWorkshopAction(invented(),{kind:"create",
      input:{...input,anchor_id:"A",source_revision_id:"fiction-alpha-rev-1",
        note:"NOTE-SECRET-SOURCE"}});
    const book=applyFictionalWorkshopAction(first,{kind:"amend",
      eventId:first.events[0].event_id,reason:"MOTIF-SECRET-SOURCE",
      input:{...input,anchor_id:"B",source_revision_id:null}});
    const before=JSON.stringify(book);
    const html=renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,{initial:book}));
    expect(html).toContain("Filtrer par présence de révision source historique fictive");
    expect(html).toContain("Avec révision source explicite");
    expect(html).toContain("Sans révision source explicite");
    expect(html).not.toContain("NOTE-SECRET-SOURCE");
    expect(html).not.toContain("MOTIF-SECRET-SOURCE");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });

  it("49 tests four historical temporal kinds in each of two isolated fictional universes and novels",()=>{
    for(const universe of ["fiction-alpha","fiction-beta"] as const){
      let book=inventedFourKindsTwoNovels(universe);
      const inputs:[string,string|null,string][]=[
        ["A",universe+"-rev-1","exact"],
        ["B",null,"approximate"],
        ["C",universe+"-rev-2","relative"],
        ["D",null,"unknown"],
      ];
      const ids:string[]=[];
      for(const [anchor,source] of inputs){
        book=applyFictionalWorkshopAction(book,{kind:"create",
          input:{...input,anchor_id:anchor,source_revision_id:source}});
        ids.push(book.events[book.events.length-1].event_id);
      }
      const before=JSON.stringify(book);
      for(let i=0;i<inputs.length;i++){
        const kind=inputs[i][2] as "exact"|"approximate"|"relative"|"unknown";
        const found=matchingFictionalEventHistoryIds(book,"","all",
          "","","","","","",kind);
        expect(found).toEqual([ids[i]]);
      }
      expect(matchingFictionalEventHistoryIds(book,"","all",
        "","novel-1","","","","","relative")).toEqual([]);
      expect(matchingFictionalEventHistoryIds(book,"","all",
        "","novel-2","","","","","relative")).toEqual([ids[2]]);
      expect(matchingFictionalEventHistoryIds(book,"","all",
        "","novel-2","","","","","exact")).toEqual([]);
      expect(matchingFictionalEventHistoryIds(book,"","all",
        universe+"-rev-1","novel-2","","","","","")).toEqual([]);
      expect(JSON.stringify(book)).toBe(before);
    }
  });
  it("50 rejects cross-universe source IDs and preserves withdrawn history without restoration",()=>{
    const alphaBase=inventedFourKindsTwoNovels("fiction-alpha");
    const betaBase=inventedFourKindsTwoNovels("fiction-beta");
    const alpha=applyFictionalWorkshopAction(alphaBase,{kind:"create",input:{
      ...input,anchor_id:"C",source_revision_id:"fiction-alpha-rev-2",
      note:"NOTE-FICTIVE-ALPHA"}});
    const betaCreated=applyFictionalWorkshopAction(betaBase,{kind:"create",input:{
      ...input,anchor_id:"C",source_revision_id:"fiction-beta-rev-2",
      note:"NOTE-FICTIVE-BETA"}});
    const alphaId=alpha.events[0].event_id;
    const betaId=betaCreated.events[0].event_id;
    const beta=applyFictionalWorkshopAction(betaCreated,{
      kind:"withdraw",eventId:betaId,reason:"Retrait beta fictif"});
    expect(alphaId).not.toBe(betaId);
    const beforeAlpha=JSON.stringify(alpha),beforeBeta=JSON.stringify(beta);
    expect(matchingFictionalEventHistoryIds(alpha,"","all",
      "fiction-beta-rev-2")).toEqual([]);
    expect(matchingFictionalEventHistoryIds(beta,"","all",
      "fiction-alpha-rev-2")).toEqual([]);
    expect(matchingFictionalEventHistoryIds(beta,alphaId)).toEqual([]);
    expect(matchingFictionalEventHistoryIds(beta,"","withdrawn",
      "fiction-beta-rev-2","novel-2","","C","","","relative")).toEqual([betaId]);
    expect(matchingFictionalEventHistoryIds(beta,"","current")).toEqual([]);
    expect(matchingFictionalEventHistoryIds(alpha,"","current")).toEqual([alphaId]);
    expect(JSON.stringify(alpha)).toBe(beforeAlpha);
    expect(JSON.stringify(beta)).toBe(beforeBeta);
  });

  it("51 changed-field history filter only matches the same historical amended version",()=>{
    const first=applyFictionalWorkshopAction(invented(),{
      kind:"create",input:{...input,anchor_id:"A",
        source_revision_id:"fiction-alpha-rev-1"}});
    const id=first.events[0].event_id;
    let book=applyFictionalWorkshopAction(first,{
      kind:"amend",eventId:id,reason:"Révision 2 fictive",
      input:{...input,title:"Titre modifié",anchor_id:"B",source_revision_id:null}});
    book=applyFictionalWorkshopAction(book,{
      kind:"amend",eventId:id,reason:"Révision 3 fictive",
      input:{...input,title:"Titre modifié",note:"Note modifiée",
        anchor_id:"B",source_revision_id:null}});
    const other=applyFictionalWorkshopAction(book,{kind:"create",input});
    book=applyFictionalWorkshopAction(other,{
      kind:"withdraw",eventId:other.events[other.events.length-1].event_id,
      reason:"Retrait seul sans changement de contenu"});
    const before=JSON.stringify(book);
    const filter=(field:""|"title"|"note"|"anchor_id"|"source_revision_id",
      anchor="",source="",status:"all"|"withdrawn"="all")=>
      matchingFictionalEventHistoryIds(book,"",status,source,"","",anchor,
        "","","","","",field);
    for(const field of ["title","note","anchor_id","source_revision_id"] as const)
      expect(filter(field)).toEqual([id]);
    expect(filter("title","B")).toEqual([id]);
    expect(filter("title","A")).toEqual([]);
    expect(filter("note","B")).toEqual([id]);
    expect(filter("note","","fiction-alpha-rev-1")).toEqual([]);
    expect(filter("title","","","withdrawn")).toEqual([]);
    expect(filter("")).toHaveLength(2);
    expect(()=>matchingFictionalEventHistoryIds(book,"","all",
      "","","","","","","","","","bad" as never))
      .toThrow("Champ historique fictif invalide");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("52 SSR changed-field filter hides old text, audit reasons and corrected contents",()=>{
    const first=applyFictionalWorkshopAction(invented(),{
      kind:"create",input:{...input,anchor_id:"A",source_revision_id:"fiction-alpha-rev-1",
        note:"NOTE-PRIVÉE-V1"}});
    const book=applyFictionalWorkshopAction(first,{
      kind:"amend",eventId:first.events[0].event_id,
      reason:"JUSTIFICATION-PRIVÉE-V2",
      input:{...input,title:"Titre public inventé",anchor_id:"B",
        source_revision_id:null,note:"NOTE-PRIVÉE-V2"}});
    const before=JSON.stringify(book);
    const html=renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,{initial:book}));
    expect(html).toContain("Filtrer par champ modifié entre versions historiques fictives");
    for(const key of ["title","note","anchor_id","source_revision_id"])
      expect(html).toContain('value="'+key+'"');
    expect(html).not.toContain("NOTE-PRIVÉE-V1");
    expect(html).not.toContain("NOTE-PRIVÉE-V2");
    expect(html).not.toContain("JUSTIFICATION-PRIVÉE-V2");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("53 filters exact historical version with same-version corrected fields",()=>{
    const first=applyFictionalWorkshopAction(invented(),{kind:"create",
      input:{...input,anchor_id:"A",source_revision_id:"fiction-alpha-rev-1"}});
    const id=first.events[0].event_id;
    const second=applyFictionalWorkshopAction(first,{kind:"amend",eventId:id,
      reason:"Passage fictif à la version deux",
      input:{...input,note:"Note fictive modifiée",anchor_id:"B",source_revision_id:null}});
    const book=applyFictionalWorkshopAction(second,{kind:"amend",eventId:id,
      reason:"Passage fictif à la version trois",
      input:{...input,title:"Titre version trois",note:"Note fictive modifiée",
        anchor_id:"B",source_revision_id:null}});
    const before=JSON.stringify(book);
    const find=(version:number,
      field:""|"title"|"note"|"anchor_id"|"source_revision_id"="",anchor="")=>
      matchingFictionalEventHistoryIds(book,"","all","","","",anchor,
        "","","","","",field,version);
    expect(find(0)).toEqual([id]);
    expect(find(1,"","A")).toEqual([id]);
    expect(find(1,"title")).toEqual([]);
    expect(find(2,"note","B")).toEqual([id]);
    expect(find(2,"note","A")).toEqual([]);
    expect(find(2,"source_revision_id")).toEqual([id]);
    expect(find(2,"title")).toEqual([]);
    expect(find(3,"title","B")).toEqual([id]);
    expect(find(3,"source_revision_id")).toEqual([]);
    expect(find(4)).toEqual([]);
    for(const bad of [-1,1.5,NaN,Infinity])
      expect(()=>find(bad)).toThrow("Version historique fictive invalide");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("54 SSR shows only version numbers before historical inspection",()=>{
    const first=applyFictionalWorkshopAction(invented(),{kind:"create",
      input:{...input,note:"NOTE-PRIVÉE-VERSION-1"}});
    const book=applyFictionalWorkshopAction(first,{kind:"amend",
      eventId:first.events[0].event_id,reason:"MOTIF-PRIVÉ-VERSION-2",
      input:{...input,note:"NOTE-PRIVÉE-VERSION-2"}});
    const before=JSON.stringify(book);
    const html=renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,{initial:book}));
    expect(html).toContain("Filtrer par numéro exact de version historique fictive");
    expect(html).toContain('value="1"');
    expect(html).toContain('value="2"');
    expect(html).toContain("Toutes les versions fictives");
    expect(html).not.toContain("NOTE-PRIVÉE-VERSION-1");
    expect(html).not.toContain("NOTE-PRIVÉE-VERSION-2");
    expect(html).not.toContain("MOTIF-PRIVÉ-VERSION-2");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("55 filters created amended withdrawn actions on the same version",()=>{
    const first=applyFictionalWorkshopAction(invented(),{kind:"create",
      input:{...input,note:"Début inventé"}});
    const id=first.events[0].event_id;
    const second=applyFictionalWorkshopAction(first,{kind:"amend",eventId:id,
      reason:"Correction humaine fictive",
      input:{...input,note:"Note de correction inventée"}});
    const book=applyFictionalWorkshopAction(second,{kind:"withdraw",eventId:id,
      reason:"Retrait humain fictif"});
    const before=JSON.stringify(book);
    const find=(action:""|"created"|"amended"|"withdrawn",version=0,
      field:""|"title"|"note"|"anchor_id"|"source_revision_id"="")=>
      matchingFictionalEventHistoryIds(book,"","withdrawn","","","","",
        "","","","","",field,version,action);
    expect(find("created",1)).toEqual([id]);
    expect(find("created",2)).toEqual([]);
    expect(find("amended",2,"note")).toEqual([id]);
    expect(find("amended",1)).toEqual([]);
    expect(find("withdrawn",3)).toEqual([id]);
    expect(find("withdrawn",2)).toEqual([]);
    expect(find("withdrawn",3,"note")).toEqual([]);
    expect(find("",0)).toEqual([id]);
    expect(()=>matchingFictionalEventHistoryIds(book,"","all","","","","",
      "","","","","","",0,"removed" as never))
      .toThrow("Action historique fictive invalide");
    expect(JSON.stringify(book)).toBe(before);
  });
  it("56 historical action filter SSR never leaks uninspected notes or reasons",()=>{
    const first=applyFictionalWorkshopAction(invented(),{kind:"create",
      input:{...input,note:"NOTE_ACTION_PRIVÉE_1"}});
    const book=applyFictionalWorkshopAction(first,{kind:"amend",
      eventId:first.events[0].event_id,reason:"MOTIF_ACTION_PRIVÉ",
      input:{...input,note:"NOTE_ACTION_PRIVÉE_2"}});
    const before=JSON.stringify(book);
    const html=renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,{initial:book}));
    expect(html).toContain("Filtrer par action de version historique fictive");
    for(const action of ["created","amended","withdrawn"])
      expect(html).toContain('value="'+action+'"');
    expect(html).not.toContain("NOTE_ACTION_PRIVÉE_1");
    expect(html).not.toContain("NOTE_ACTION_PRIVÉE_2");
    expect(html).not.toContain("MOTIF_ACTION_PRIVÉ");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(before);
  });

});

describe("M32-070 calendar anchor event manual pathway candidate", () => {
  it("57 creates calendar then exact sourced anchor then explicit event and correction", () => {
    const book = invented(), bytes = JSON.stringify(book);
    const catalogue = addFictionalCalendar([], "Marées");
    const dated = appendFictionalCalendarAnchor(book,catalogue,catalogue[0].id,"exact","Jour XII","fiction-alpha-rev-1");
    const a = dated.draft.snapshot.anchors[dated.draft.snapshot.anchors.length-1];
    expect(a).toMatchObject({calendar_name:"Marées",fictional_label:"Jour XII",source_revision_id:"fiction-alpha-rev-1"});
    expect(dated.events).toHaveLength(0);
    const created = applyFictionalWorkshopAction(dated,{kind:"create",input:{...input,anchor_id:a.id,source_revision_id:a.source_revision_id}});
    const revised = applyFictionalWorkshopAction(created,{kind:"amend",eventId:created.events[0].event_id,reason:"Correction humaine",input:{...input,title:"Rencontre corrigée",anchor_id:a.id,source_revision_id:a.source_revision_id}});
    expect(revised.events.map(e=>[e.version,e.status,e.anchor_id,e.source_revision_id])).toEqual([[1,"superseded",a.id,a.source_revision_id],[2,"current",a.id,a.source_revision_id]]);
    expect(JSON.stringify(book)).toBe(bytes);
    expect(revised.real_g3_authorized).toBe(false);
  });
  it("58 preserves estimation and optional absence of source without deriving a date", () => {
    const book = invented(), catalogue = addFictionalCalendar([], "Lunes");
    const dated = appendFictionalCalendarAnchor(book,catalogue,catalogue[0].id,"approximate","Vers le solstice","");
    const a = dated.draft.snapshot.anchors[dated.draft.snapshot.anchors.length-1];
    expect(a).toMatchObject({calendar_name:"Lunes",time_kind:"approximate",precision_text:"Vers le solstice",fictional_label:null,source_revision_id:null});
    expect(applyFictionalWorkshopAction(dated,{kind:"create",input:{...input,anchor_id:a.id}}).events).toHaveLength(1);
  });
  it("59 rejects missing calendar, blank estimation and foreign revision without mutation", () => {
    const book=invented(), bytes=JSON.stringify(book), catalogue=addFictionalCalendar([],"Lunes");
    expect(()=>appendFictionalCalendarAnchor(book,catalogue,"foreign","exact","Jour","")).toThrow();
    expect(()=>appendFictionalCalendarAnchor(book,catalogue,catalogue[0].id,"approximate"," ","")).toThrow();
    expect(()=>appendFictionalCalendarAnchor(book,catalogue,catalogue[0].id,"exact","Jour","fiction-beta-rev-1")).toThrow();
    expect(JSON.stringify(book)).toBe(bytes);
  });
  it("60 requires explicit event source even after creation of a sourced anchor", () => {
    const catalogue=addFictionalCalendar([],"Lunes");
    const dated=appendFictionalCalendarAnchor(invented(),catalogue,catalogue[0].id,"exact","Jour","fiction-alpha-rev-1");
    const a=dated.draft.snapshot.anchors[dated.draft.snapshot.anchors.length-1];
    expect(()=>applyFictionalWorkshopAction(dated,{kind:"create",input:{...input,anchor_id:a.id}})).toThrow(/révision/);
    expect(dated.events).toHaveLength(0);
  });
  it("61 presents a distinct opt-in preparation before the event form", () => {
    const html=renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,{initial:invented()}));
    expect(html).toContain("Préparer un calendrier et une ancre fictifs");
    expect(html).toContain('aria-expanded="false"');
    expect(html.indexOf("Préparer un calendrier et une ancre fictifs")).toBeLessThan(html.indexOf("Créer un événement"));
  });
});

describe("M32-071 explicit historical source character candidate", () => {
  function withCharacters() {
    const base = inventedTwoNovels();
    const revisions = base.draft.revisions.map((r, i) => ({
      ...r, fictional_character_ids: [i === 0 ? "fiction-character-A" : "fiction-character-B"],
    }));
    return startFictionalEventNotebook(startFictionalDraft(base.draft.snapshot, revisions));
  }
  it("62 matches character and all other filters on one historical version only", () => {
    const first = applyFictionalWorkshopAction(withCharacters(), {kind:"create",
      input:{...input,anchor_id:"A",source_revision_id:"fiction-alpha-rev-1"}});
    const id = first.events[0].event_id;
    const amended = applyFictionalWorkshopAction(first, {kind:"amend",eventId:id,
      reason:"Correction inventée",input:{...input,anchor_id:"C",source_revision_id:"fiction-alpha-rev-2"}});
    const withdrawn = applyFictionalWorkshopAction(amended, {kind:"withdraw",eventId:id,
      reason:"Retrait inventé"});
    const book = create(withdrawn), bytes = JSON.stringify(book);
    const find = (character: string, novel = "", source = "", version = 0) =>
      matchingFictionalEventHistoryIds(book,"","all",source,novel,"","","","","","","","",version,"",character);
    expect(find("fiction-character-A","novel-1","fiction-alpha-rev-1",1)).toEqual([id]);
    expect(find("fiction-character-B","novel-2","fiction-alpha-rev-2",2)).toEqual([id]);
    expect(find("fiction-character-A","novel-2")).toEqual([]);
    expect(find("fiction-character-B","","fiction-alpha-rev-1")).toEqual([]);
    expect(find("fiction-character-A","","",2)).toEqual([]);
    expect(find("fiction-character-missing")).toEqual([]);
    expect(find("")).toHaveLength(2);
    expect(()=>find("not-fictional")).toThrow("Identifiant de personnage fictif invalide");
    expect(JSON.stringify(book)).toBe(bytes);
  });
  it("63 rejects invalid, duplicate, or overlong catalogues and clones explicit IDs", () => {
    const base = invented(), ids = ["fiction-character-A"];
    const draft = startFictionalDraft(base.draft.snapshot, [{...base.draft.revisions[0],fictional_character_ids:ids}]);
    ids.push("fiction-character-B");
    expect(draft.revisions[0].fictional_character_ids).toEqual(["fiction-character-A"]);
    for (const bad of [["invalid"],["fiction-character-A","fiction-character-A"],
      Array.from({length:33},(_,i)=>"fiction-character-"+i), ["fiction-character-"+"x".repeat(81)]]) {
      expect(()=>startFictionalDraft(base.draft.snapshot,[{...base.draft.revisions[0],fictional_character_ids:bad}])).toThrow(/personnages/);
    }
    const foreign = invented("fiction-beta");
    expect(()=>startFictionalDraft(foreign.draft.snapshot,draft.revisions)).toThrow(/étrangère/);
  });
  it("64 renders only explicit source IDs and not historical text before selection", () => {
    const first = applyFictionalWorkshopAction(withCharacters(),{kind:"create",
      input:{...input,note:"NOTE_PERSONNAGE_NON_INSPECTEE",anchor_id:"A",source_revision_id:"fiction-alpha-rev-1"}});
    const book = applyFictionalWorkshopAction(first,{kind:"amend",eventId:first.events[0].event_id,
      reason:"Correction inventée",input:{...input,anchor_id:"A",source_revision_id:"fiction-alpha-rev-1"}});
    const bytes=JSON.stringify(book);
    const html=renderToStaticMarkup(createElement(M32FictionalEventManualWorkshop,{initial:book}));
    expect(html).toContain("Filtrer par personnage de révision source fictive");
    expect(html).toContain('value="fiction-character-A"');
    expect(html).toContain('value="fiction-character-B"');
    expect(html).not.toContain("NOTE_PERSONNAGE_NON_INSPECTEE");
    expect(html).not.toContain("Versions historiques fictives");
    expect(JSON.stringify(book)).toBe(bytes);
  });
});
