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

});
