import M32FictionalPersistenceNotice from "./m32FictionalPersistenceNotice";
import { useState, type FormEvent, type ReactElement } from "react";
import {
  amendFictionalEvent, createFictionalEvent, currentFictionalEvents,
  inspectFictionalEventNotebook, prepareFictionalEventHistoricalDraft,
  auditedFictionalEventHistory, withdrawFictionalEvent,
  type FictionalEventInput, type FictionalEventNotebook,
} from "./m32FictionalEventNotebook";
import M32FictionalEventVersionPairLab from "./M32FictionalEventVersionPairLab";
import { createFictionalAnchor, isFictionalCharacterId, type FictionalRevision } from "./m32FictionalManualChronology";
import { addFictionalCalendar, selectFictionalCalendar, type FictionalCalendarEntry } from "./M32ManualChronologyLab";

/** Append a human-dated anchor without creating or changing any event. RAM only. */
export function appendFictionalCalendarAnchor(
  book: FictionalEventNotebook, catalogue: readonly FictionalCalendarEntry[],
  calendarId: string, kind: "exact" | "approximate", dateText: string, revisionId: string,
): FictionalEventNotebook {
  inspectFictionalEventNotebook(book);
  if (kind !== "exact" && kind !== "approximate") throw Error("Type de date fictive invalide.");
  const calendar = selectFictionalCalendar(catalogue, calendarId);
  const rev = book.draft.revisions.find(r => r.revision_id === revisionId);
  if (revisionId && !rev) throw Error("Révision fictive absente ou étrangère.");
  const draft = createFictionalAnchor(book.draft, {
    kind, calendar, label: kind === "exact" ? dateText : "",
    precision: kind === "approximate" ? dateText : "",
    source_revision_id: rev?.revision_id ?? null, source_scene_id: rev?.scene_id ?? null,
  });
  return inspectFictionalEventNotebook({...book, draft});
}

/** Offer only an active anchor's exact historical source, without choosing it.
 * Fictional browser memory only; neither a source authority nor a persistence gate.
 */
export function eligibleFictionalEventRevisions(
  notebook: FictionalEventNotebook, selectedAnchorId: string,
): readonly FictionalRevision[] {
  inspectFictionalEventNotebook(notebook);
  const universe = notebook.draft.snapshot.universe_id;
  const anchor = notebook.draft.snapshot.anchors.find(a =>
    a.id === selectedAnchorId && a.universe_id === universe && a.status === "current");
  if (!anchor?.source_revision_id) return [];
  return notebook.draft.revisions.filter(revision =>
    revision.universe_id === universe && revision.revision_id === anchor.source_revision_id);
}

/** Only list event IDs, never historical titles/reasons, until explicit inspection.
 * Last status includes withdrawn tombstones and cannot restore a past event.
 */
export function matchingFictionalEventHistoryIds(
  notebook: FictionalEventNotebook, searchId: string,
  status: "all" | "current" | "withdrawn" = "all",
  exactSourceRevisionId = "",
  exactSourceNovelId = "",
  exactSourceSceneId = "",
  exactAnchorId = "",
  exactFictionalDateLabel = "",
  exactCalendarName = "",
  exactTimeKind: "" | "exact" | "approximate" | "relative" | "unknown" = "",
  anchorLink: "" | "linked" | "unlinked" = "",
  sourceLink: "" | "linked" | "unlinked" = "",
  changedField: "" | "title" | "note" | "anchor_id" | "source_revision_id" = "",
  exactVersion = 0,
  historicalAction: "" | "created" | "amended" | "withdrawn" = "",
  exactCharacterId = "",
): readonly string[] {
  inspectFictionalEventNotebook(notebook);
  if (exactCharacterId !== "" && !isFictionalCharacterId(exactCharacterId))
    throw Error("Identifiant de personnage fictif invalide");
  const query = searchId.trim().toLocaleLowerCase();
  // Opaque source IDs use exact matching, including superseded versions.
  const sourceId = exactSourceRevisionId.trim();
  const novelId = exactSourceNovelId.trim();
  const sceneId = exactSourceSceneId.trim();
  const anchorId = exactAnchorId.trim();
  const dateLabel = exactFictionalDateLabel.trim();
  const calendarName = exactCalendarName.trim();
  if (!Number.isSafeInteger(exactVersion) || exactVersion < 0)
    throw Error("Version historique fictive invalide");
  if (!["", "created", "amended", "withdrawn"].includes(historicalAction))
    throw Error("Action historique fictive invalide");
  if (!["", "exact", "approximate", "relative", "unknown"].includes(exactTimeKind))
    throw Error("Type temporel fictif invalide");
  const timeKind = exactTimeKind;
  if (!["", "linked", "unlinked"].includes(anchorLink))
    throw Error("Lien d'ancre fictive invalide");
  if (!["", "linked", "unlinked"].includes(sourceLink))
    throw Error("Lien de révision source fictive invalide");
  if (!["", "title", "note", "anchor_id", "source_revision_id"].includes(changedField))
    throw Error("Champ historique fictif invalide");
  const anchorById = new Map(notebook.draft.snapshot.anchors.map(a => [a.id, a]));
  const sourceRevisionById = new Map(
    notebook.draft.revisions.map(r => [r.revision_id, r]));
  return notebook.events.filter(e => e.version === 1).map(e => e.event_id)
    .filter(id => {
      const versions = notebook.events.filter(e => e.event_id === id);
      const latest = versions[versions.length - 1];
      return Boolean(latest && (status === "all" || latest.status === status) &&
        id.toLocaleLowerCase().includes(query) &&
        ((!sourceId && !novelId && !sceneId && !anchorId && !dateLabel && !calendarName &&
          !timeKind && !anchorLink && !sourceLink && !changedField && !exactVersion &&
          !historicalAction && !exactCharacterId) ||
          versions.some((v, index) => {
            // All selectors must match one event version, not a union of history.
            const revision = v.source_revision_id === null ? undefined :
              sourceRevisionById.get(v.source_revision_id);
            const anchor = v.anchor_id === null ? undefined :
              anchorById.get(v.anchor_id);
            return (!sourceId || v.source_revision_id === sourceId) &&
              (!novelId || revision?.novel_id === novelId) &&
              (!exactCharacterId || revision?.fictional_character_ids?.includes(exactCharacterId)) &&
              (!sceneId || revision?.scene_id === sceneId) &&
              (!anchorId || v.anchor_id === anchorId) &&
              (!dateLabel || (anchor?.time_kind === "exact" &&
                anchor.fictional_label === dateLabel)) &&
              (!calendarName || (anchor?.time_kind === "exact" &&
                anchor.calendar_name === calendarName)) &&
              (!timeKind || anchor?.time_kind === timeKind) &&
              (!anchorLink || (anchorLink === "linked" ?
                v.anchor_id !== null : v.anchor_id === null)) &&
              (!sourceLink || (sourceLink === "linked" ?
                v.source_revision_id !== null : v.source_revision_id === null)) &&
              (!changedField || (index > 0 &&
                v[changedField] !== versions[index - 1][changedField])) &&
              (!exactVersion || v.version === exactVersion) &&
              (!historicalAction || notebook.audit.some(a =>
                a.event_id === id && a.version === v.version &&
                a.action === historicalAction));
          })));
    });
}

/** Paged IDs only; never implicitly inspect or mutate a fictional event. */
export const FICTIONAL_HISTORY_PAGE_SIZE = 10;
export const FICTIONAL_HISTORY_PAGE_SIZES = [5, 10, 20] as const;
export type FictionalHistoryIdOrder = "insertion" | "reverse-insertion";
/** Only opaque ID display ordering, never world/narration/revelation chronology. */
export function orderFictionalEventHistoryIds(ids: readonly string[],
  order: FictionalHistoryIdOrder): readonly string[] {
  if (order !== "insertion" && order !== "reverse-insertion")
    throw Error("Ordre de consultation fictif invalide");
  return order === "insertion" ? [...ids] : [...ids].reverse();
}
export function pageFictionalEventHistoryIds(
  ids: readonly string[], page: number, pageSize: number = FICTIONAL_HISTORY_PAGE_SIZE,
):
  Readonly<{ ids: readonly string[]; index: number; pages: number; total: number }> {
  if (!Number.isSafeInteger(page) || page < 0) throw Error("Page fictive invalide");
  if (!FICTIONAL_HISTORY_PAGE_SIZES.some(size => size === pageSize))
    throw Error("Taille de page fictive invalide");
  const pages = Math.max(1, Math.ceil(ids.length / pageSize));
  const index = Math.min(page, pages - 1);
  return { ids: ids.slice(index * pageSize, (index + 1) * pageSize),
    index, pages, total: ids.length };
}

/** One action, one invented in-memory state transition; never persisted. */
export type FictionalWorkshopAction =
  | Readonly<{ kind: "create"; input: FictionalEventInput }>
  | Readonly<{ kind: "amend"; eventId: string; input: FictionalEventInput; reason: string }>
  | Readonly<{ kind: "withdraw"; eventId: string; reason: string }>;

export function applyFictionalWorkshopAction(
  notebook: FictionalEventNotebook, action: FictionalWorkshopAction,
): FictionalEventNotebook {
  inspectFictionalEventNotebook(notebook);
  switch (action.kind) {
    case "create": return createFictionalEvent(notebook, action.input);
    case "amend": return amendFictionalEvent(notebook, action.eventId, action.input, action.reason);
    case "withdraw": return withdrawFictionalEvent(notebook, action.eventId, action.reason);
  }
}

/**
 * Unmounted manual UX rehearsal. Never import into App.tsx or invoke Tauri.
 * No localStorage, fetch, files, production source, SQLite or automatic ordering.
 */
export default function M32FictionalEventManualWorkshop({ initial }: {
  initial: FictionalEventNotebook;
}): ReactElement {
  inspectFictionalEventNotebook(initial);
  const [book, setBook] = useState(initial);
  const [calendarOpen, setCalendarOpen] = useState(false);
  const [calendars, setCalendars] = useState<readonly FictionalCalendarEntry[]>([]);
  const [calendarName, setCalendarName] = useState("");
  const [calendarId, setCalendarId] = useState("");
  const [dateKind, setDateKind] = useState<"exact" | "approximate">("exact");
  const [dateText, setDateText] = useState("");
  const [dateRevision, setDateRevision] = useState("");
  const [dateFeedback, setDateFeedback] = useState("");
  const [dateError, setDateError] = useState(false);
  function createCalendar() {
    try {
      setCalendars(addFictionalCalendar(calendars, calendarName));
      setCalendarName(""); setDateError(false);
      setDateFeedback("Calendrier créé ; aucune ancre ni aucun événement créé.");
    } catch (error) {
      setDateError(true); setDateFeedback(String(error));
    }
  }
  function createDateAnchor() {
    try {
      const next = appendFictionalCalendarAnchor(book, calendars, calendarId, dateKind, dateText, dateRevision);
      setBook(next); setDateText(""); setDateError(false);
      setDateFeedback("Ancre créée : " + next.draft.snapshot.anchors[next.draft.snapshot.anchors.length - 1].id +
        ". Choisissez-la explicitement dans le formulaire événement.");
    } catch (error) {
      setDateError(true); setDateFeedback(String(error));
    }
  }
  const [selectedId, setSelectedId] = useState("");
  const [title, setTitle] = useState("");
  const [note, setNote] = useState("");
  const [anchor, setAnchor] = useState("");
  const [revision, setRevision] = useState("");
  const [reason, setReason] = useState("");
  const [feedback, setFeedback] = useState("");
  const [isError, setIsError] = useState(false);
  const [compareOpen, setCompareOpen] = useState(false);
  const [historicalVersion, setHistoricalVersion] = useState("");
  const [historyEventId, setHistoryEventId] = useState("");
  const [historyIdQuery, setHistoryIdQuery] = useState("");
  const [historySourceIdQuery, setHistorySourceIdQuery] = useState("");
  const [historyNovelId, setHistoryNovelId] = useState("");
  const [historyCharacterId, setHistoryCharacterId] = useState("");
  const [historySceneId, setHistorySceneId] = useState("");
  const [historyAnchorId, setHistoryAnchorId] = useState("");
  const [historyFictionalDateLabel, setHistoryFictionalDateLabel] = useState("");
  const [historyCalendarName, setHistoryCalendarName] = useState("");
  const [historyTimeKind, setHistoryTimeKind] =
    useState<"" | "exact" | "approximate" | "relative" | "unknown">("");
  const [historyAnchorLink, setHistoryAnchorLink] =
    useState<"" | "linked" | "unlinked">("");
  const [historySourceLink, setHistorySourceLink] =
    useState<"" | "linked" | "unlinked">("");
  const [historyChangedField, setHistoryChangedField] =
    useState<"" | "title" | "note" | "anchor_id" | "source_revision_id">("");
  const [historyExactVersion, setHistoryExactVersion] = useState(0);
  const [historyAction, setHistoryAction] =
    useState<"" | "created" | "amended" | "withdrawn">("");
  const [historyPage, setHistoryPage] = useState(0);
  const [historyPageSize, setHistoryPageSize] = useState<number>(FICTIONAL_HISTORY_PAGE_SIZE);
  const [historyIdOrder, setHistoryIdOrder] = useState<FictionalHistoryIdOrder>("insertion");
  const [historyStatus, setHistoryStatus] =
    useState<"all" | "current" | "withdrawn">("all");

  const activeAnchors = book.draft.snapshot.anchors.filter(a => a.status === "current");
  const eligibleRevisions = eligibleFictionalEventRevisions(book, anchor);
  const currentEvents = currentFictionalEvents(book);
  // Creation IDs remain available after a withdrawal; a tombstone is history,
  // not permission to restore a past event or change the current manuscript.
  const sourceNovelIds = [...new Set(book.draft.revisions.map(r => r.novel_id))];
  const sourceCharacterIds = [...new Set(book.draft.revisions.flatMap(r => r.fictional_character_ids ?? []))].sort();
  const sourceSceneIds = [...new Set(book.draft.revisions.map(r => r.scene_id))];
  const historyAnchorIds = book.draft.snapshot.anchors.map(a => a.id);
  const historyVersionNumbers = [...new Set(book.events.map(e => e.version))]
    .sort((a, b) => a - b);
  const historyDateLabels = [...new Set(book.draft.snapshot.anchors
    .filter(a => a.time_kind === "exact" && a.fictional_label !== null)
    .map(a => a.fictional_label!))];
  const historyCalendarNames = [...new Set(book.draft.snapshot.anchors
    .filter(a => a.time_kind === "exact" && a.calendar_name !== null)
    .map(a => a.calendar_name!))];
  const historyEventIds = matchingFictionalEventHistoryIds(
    book, historyIdQuery, historyStatus, historySourceIdQuery, historyNovelId,
    historySceneId, historyAnchorId, historyFictionalDateLabel, historyCalendarName,
    historyTimeKind, historyAnchorLink, historySourceLink, historyChangedField,
    historyExactVersion, historyAction, historyCharacterId);
  const orderedHistoryIds = orderFictionalEventHistoryIds(historyEventIds, historyIdOrder);
  const historyView = pageFictionalEventHistoryIds(orderedHistoryIds, historyPage, historyPageSize);
  const inspectedHistory = historyEventId
    ? auditedFictionalEventHistory(book, historyEventId) : [];
  const editableEvent = currentEvents.find(e => e.event_id === selectedId);
  const olderVersions = editableEvent && editableEvent.version > 1
    ? auditedFictionalEventHistory(book, selectedId).filter(
      entry => entry.event.version < editableEvent.version)
    : [];
  function clearSelection() {
    setSelectedId(""); setTitle(""); setNote("");
    setAnchor(""); setRevision(""); setReason(""); setHistoricalVersion("");
  }
  function apply(action: FictionalWorkshopAction) {
    try {
      const updated = applyFictionalWorkshopAction(book, action);
      setBook(updated);
      clearSelection();
      setIsError(false);
      setFeedback("Modification fictive en mémoire uniquement. Aucune sauvegarde.");
    } catch (error) {
      setIsError(true);
      setFeedback(error instanceof Error ? error.message : "Action fictive refusée.");
    }
  }
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const input: FictionalEventInput = {
      title, note, anchor_id: anchor || null,
      source_revision_id: revision || null,
    };
    if (selectedId) {
      apply({ kind: "amend", eventId: selectedId, input, reason });
    } else {
      apply({ kind: "create", input });
    }
  }
  function resetHistoryFilters() {
    setHistoryIdQuery(""); setHistorySourceIdQuery("");
    setHistoryNovelId(""); setHistorySceneId(""); setHistoryCharacterId("");
    setHistoryAnchorId(""); setHistoryFictionalDateLabel("");
    setHistoryCalendarName(""); setHistoryTimeKind(""); setHistoryAnchorLink("");
    setHistorySourceLink(""); setHistoryChangedField("");
    setHistoryExactVersion(0); setHistoryAction("");
    setHistoryStatus("all");
    setHistoryPage(0); setHistoryEventId("");
    setHistoryPageSize(FICTIONAL_HISTORY_PAGE_SIZE);
    setHistoryIdOrder("insertion");
  }
  function chooseEvent(eventId: string) {
    const selected = currentEvents.find(e => e.event_id === eventId);
    if (!selected) return;
    setSelectedId(selected.event_id);
    setTitle(selected.title);
    setNote(selected.note);
    setAnchor(selected.anchor_id ?? "");
    setRevision(selected.source_revision_id ?? "");
    setReason("");
    setHistoricalVersion("");
    setFeedback("");
  }
  function prepareOlderVersion() {
    try {
      const data = prepareFictionalEventHistoricalDraft(book, selectedId,
        Number(historicalVersion));
      setTitle(data.title); setNote(data.note);
      setAnchor(data.anchor_id ?? ""); setRevision(data.source_revision_id ?? "");
      setReason("");
      setIsError(false);
      setFeedback("Version historique copiée dans le formulaire seulement : " +
        "la correction attend votre justification et votre validation explicite.");
    } catch (error) {
      setIsError(true);
      setFeedback(error instanceof Error ? error.message : "Copie fictive refusée.");
    }
  }
  return <section aria-label="Atelier manuel fictif d'événements M3.2">
    <h2>Atelier fictif — événements de {book.draft.snapshot.universe_id}</h2>
    <M32FictionalPersistenceNotice />
    <p role="note">Démonstration exclusivement en mémoire du navigateur.
      Aucun enregistrement, aucun accès SQLite, aucune commande Tauri,
      aucune chronologie ou révélation du lecteur calculée automatiquement.</p>
    <button type="button" aria-expanded={calendarOpen} onClick={() => setCalendarOpen(!calendarOpen)}>
      {calendarOpen ? "Masquer la préparation temporelle" : "Préparer un calendrier et une ancre fictifs"}
    </button>
    {calendarOpen && <fieldset>
      <legend>Préparation temporelle manuelle sans IA</legend>
      <label>Nom du calendrier à créer
        <input value={calendarName} maxLength={160} onChange={e => setCalendarName(e.target.value)} />
      </label>
      <button type="button" onClick={createCalendar}>Créer le calendrier fictif</button>
      <label>Calendrier créé explicitement choisi
        <select value={calendarId} onChange={e => setCalendarId(e.target.value)}>
          <option value="">Choisir un calendrier</option>
          {calendars.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </label>
      <label>Validité temporelle de l'ancre
        <select value={dateKind} onChange={e => {setDateKind(e.target.value as "exact" | "approximate");setDateText("");}}>
          <option value="exact">Date exacte</option>
          <option value="approximate">Date estimée</option>
        </select>
      </label>
      <label>{dateKind === "exact" ? "Date fictive exacte" : "Précision ou intervalle estimé"}
        <input value={dateText} maxLength={160} onChange={e => setDateText(e.target.value)} />
      </label>
      <label>Révision source de la nouvelle ancre
        <select value={dateRevision} onChange={e => setDateRevision(e.target.value)}>
          <option value="">Sans source explicite</option>
          {book.draft.revisions.map(r => <option key={r.revision_id} value={r.revision_id}>
            {r.revision_label} — {r.revision_id}
          </option>)}
        </select>
      </label>
      <button type="button" onClick={createDateAnchor}>Créer l'ancre datée en mémoire</button>
      {dateFeedback && <p role={dateError ? "alert" : "status"}>{dateFeedback}</p>}
    </fieldset>}
    <form onSubmit={submit} aria-label="Formulaire d'événement fictif">
      <h3>{selectedId ? "Corriger un événement" : "Créer un événement"}</h3>
      <label>Titre de l'événement (obligatoire)
        <input value={title} onChange={e => setTitle(e.target.value)}
          maxLength={120} required />
      </label>
      <label>Note facultative
        <textarea value={note} onChange={e => setNote(e.target.value)}
          maxLength={400} />
      </label>
      <label>Ancre temporelle explicitement choisie
        <select value={anchor} onChange={e => { setAnchor(e.target.value); setRevision(""); }}>
          <option value="">Sans ancre (temps inconnu)</option>
          {activeAnchors.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
        </select>
      </label>
      <label>Révision historique explicitement choisie
        <select value={revision} disabled={eligibleRevisions.length === 0}
          onChange={e => setRevision(e.target.value)}>
          <option value="">Aucune révision</option>
          {eligibleRevisions.map(r =>
            <option key={r.revision_id} value={r.revision_id}>
              {r.revision_label} ({r.revision_id})
            </option>)}
        </select>
      </label>
      <small role="note">Seule la révision associée à l’ancre active est proposée.
        Aucune source historique n’est sélectionnée automatiquement.</small>
      <label>Justification de correction ou de retrait
        <input value={reason} onChange={e => setReason(e.target.value)}
          maxLength={240} required={Boolean(selectedId)} />
      </label>
      {selectedId && olderVersions.length > 0 && <fieldset>
        <legend>Reprendre manuellement le texte d'une version historique fictive</legend>
        <label>Version passée à reprendre
          <select value={historicalVersion}
            onChange={e => setHistoricalVersion(e.target.value)}>
            <option value="">Choisir une ancienne version</option>
            {olderVersions.map(entry =>
              <option key={entry.event.version} value={String(entry.event.version)}>
                Version {entry.event.version}
              </option>)}
          </select>
        </label>
        <button type="button" disabled={!historicalVersion}
          onClick={prepareOlderVersion}>
          Préparer la correction depuis cette version
        </button>
        <p role="note">Copie seulement les champs dans le formulaire :
          aucune modification enregistrée avant justification et validation.
          Aucun événement retiré ne peut être réactivé ainsi.</p>
      </fieldset>}
      <button type="submit">{selectedId ? "Créer une nouvelle version fictive en mémoire" :
        "Créer en mémoire"}</button>
      {selectedId && <button type="button" onClick={() =>
        apply({ kind: "withdraw", eventId: selectedId, reason })}>
        Retirer en conservant l'historique
      </button>}
      <button type="button" onClick={clearSelection}>Effacer la sélection</button>
    </form>
    {feedback && <p role={isError ? "alert" : "status"}>{feedback}</p>}
    <h3>Événements courants ({currentEvents.length})</h3>
    <ul>{currentEvents.map(e => <li key={e.event_id}>
      {e.title} — version {e.version}
      <button type="button" onClick={() => chooseEvent(e.event_id)}>
        Corriger ou retirer {e.event_id}
      </button>
    </li>)}</ul>
    <section aria-label="Historique détaillé des événements fictifs">
      <h3>Consulter le passé d’un événement fictif</h3>
      <p>Historique en lecture seule : aucune restauration, aucune écriture,
        aucune décision sur le canon ou l’ordre du monde.</p>
      <label>Rechercher un identifiant d'événement fictif
        <input type="search" value={historyIdQuery} maxLength={120}
          onChange={e => {
            setHistoryIdQuery(e.currentTarget.value); setHistoryEventId(""); setHistoryPage(0);
          }} />
      </label>
      <label>Filtrer par ID exact de révision source fictive
        <input type="search" value={historySourceIdQuery} maxLength={256}
          onChange={e => {
            setHistorySourceIdQuery(e.currentTarget.value);
            setHistoryEventId(""); setHistoryPage(0);
          }} />
      </label>
      <label>Filtrer par roman de révision source fictive
        <select value={historyNovelId} onChange={e => {
          setHistoryNovelId(e.currentTarget.value);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Tous les romans sources fictifs</option>
          {sourceNovelIds.map(id => <option key={id} value={id}>{id}</option>)}
        </select>
      </label>
      <label>Filtrer par personnage de révision source fictive
        <select value={historyCharacterId} onChange={e => {
          setHistoryCharacterId(e.currentTarget.value);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Tous les personnages sources fictifs</option>
          {sourceCharacterIds.map(id => <option key={id} value={id}>{id}</option>)}
        </select>
      </label>
      <small role="note">Association explicite à la révision source inventée exacte ; aucune inférence depuis le texte.</small>
      <label>Filtrer par scène de révision source fictive
        <select value={historySceneId} onChange={e => {
          setHistorySceneId(e.currentTarget.value);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Toutes les scènes sources fictives</option>
          {sourceSceneIds.map(id => <option key={id} value={id}>{id}</option>)}
        </select>
      </label>
      <label>Filtrer par ID exact d'ancre historique fictive
        <select value={historyAnchorId} onChange={e => {
          setHistoryAnchorId(e.currentTarget.value);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Toutes les ancres fictives</option>
          {historyAnchorIds.map(id => <option key={id} value={id}>{id}</option>)}
        </select>
      </label>
      <label>Filtrer par libellé exact de date fictive
        <select value={historyFictionalDateLabel} onChange={e => {
          setHistoryFictionalDateLabel(e.currentTarget.value);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Toutes les dates fictives exactes</option>
          {historyDateLabels.map(label => <option key={label} value={label}>{label}</option>)}
        </select>
      </label>
      <label>Filtrer par nom exact de calendrier historique fictif
        <select value={historyCalendarName} onChange={e => {
          setHistoryCalendarName(e.currentTarget.value);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Tous les calendriers fictifs exacts</option>
          {historyCalendarNames.map(name =>
            <option key={name} value={name}>{name}</option>)}
        </select>
      </label>
      <label>Filtrer par type temporel historique fictif
        <select value={historyTimeKind} onChange={e => {
          setHistoryTimeKind(e.currentTarget.value as typeof historyTimeKind);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Tous les types temporels fictifs</option>
          <option value="exact">Date fictive exacte</option>
          <option value="approximate">Période fictive approximative</option>
          <option value="relative">Position fictive relative</option>
          <option value="unknown">Ancre fictive à temps inconnu</option>
        </select>
      </label>
      <small role="note">Type de l'ancre citée par une même version historique,
        sans inférence de date. Sans ancre ne signifie pas temps inconnu attesté.</small>
      <label>Filtrer par présence d'ancre historique fictive
        <select value={historyAnchorLink} onChange={e => {
          setHistoryAnchorLink(e.currentTarget.value as typeof historyAnchorLink);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Toutes les liaisons d'ancres fictives</option>
          <option value="linked">Avec ancre historique explicite</option>
          <option value="unlinked">Sans ancre historique explicite</option>
        </select>
      </label>
      <small role="note">Sans ancre ne vaut jamais « ancre au temps inconnu ».
        Les filtres doivent correspondre à une même version.</small>
      <label>Filtrer par présence de révision source historique fictive
        <select value={historySourceLink} onChange={e => {
          setHistorySourceLink(e.currentTarget.value as typeof historySourceLink);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Toutes les liaisons sources fictives</option>
          <option value="linked">Avec révision source explicite</option>
          <option value="unlinked">Sans révision source explicite</option>
        </select>
      </label>
      <small role="note">Sans source ne signifie ni sans ancre ni temps inconnu.
        Tous les filtres portent sur une même version historique.</small>
      <label>Filtrer par numéro exact de version historique fictive
        <select value={historyExactVersion} onChange={e => {
          setHistoryExactVersion(Number(e.currentTarget.value));
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value={0}>Toutes les versions fictives</option>
          {historyVersionNumbers.map(version =>
            <option key={version} value={version}>Version {version}</option>)}
        </select>
      </label>
      <small role="note">Sélection d’un numéro de version, sans lecture des
        titres, notes ou motifs historiques avant inspection explicite.</small>
      <label>Filtrer par action de version historique fictive
        <select value={historyAction} onChange={e => {
          setHistoryAction(e.currentTarget.value as typeof historyAction);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Toutes les actions historiques fictives</option>
          <option value="created">Création fictive</option>
          <option value="amended">Correction fictive</option>
          <option value="withdrawn">Retrait fictif</option>
        </select>
      </label>
      <small role="note">L'action appartient à une version historique précise ;
        elle n'est ni le statut de l'événement actuel ni un droit de restauration.</small>
      <label>Filtrer par champ modifié entre versions historiques fictives
        <select value={historyChangedField} onChange={e => {
          setHistoryChangedField(e.currentTarget.value as typeof historyChangedField);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Toutes les corrections historiques fictives</option>
          <option value="title">Titre modifié</option>
          <option value="note">Note modifiée</option>
          <option value="anchor_id">Ancre modifiée</option>
          <option value="source_revision_id">Révision source modifiée</option>
        </select>
      </label>
      <small role="note">Seules les versions corrigées sont prises en compte,
        sans afficher le texte passé avant une inspection explicite.
        Le retrait seul ne constitue pas une correction.</small>
      <label>Filtrer l'historique par statut
        <select value={historyStatus} onChange={e => {
          setHistoryStatus(e.currentTarget.value as "all" | "current" | "withdrawn");
          setHistoryEventId("");
          setHistoryPage(0);
        }}>
          <option value="all">Tous, actifs et retirés</option>
          <option value="current">Événements actifs seulement</option>
          <option value="withdrawn">Événements retirés seulement</option>
        </select>
      </label>
      <button type="button" onClick={resetHistoryFilters}>
        Réinitialiser les filtres historiques fictifs
      </button>
      <p role="note">Le filtrage n'affiche aucune version ni motif historique.
        Choisissez un identifiant pour consulter les versions en lecture seule.</p>
      <label>Ordre d'ajout des identifiants fictifs
        <select value={historyIdOrder} onChange={e => {
          setHistoryIdOrder(e.currentTarget.value as FictionalHistoryIdOrder);
          setHistoryPage(0); setHistoryEventId("");
        }}>
          <option value="insertion">Premiers ajouts d'abord</option>
          <option value="reverse-insertion">Derniers ajouts d'abord</option>
        </select>
      </label>
      <small role="note">Ordre d'ajout uniquement, jamais l'ordre du monde,
        de narration ou de révélation.</small>
      <label>Identifiants fictifs par page
        <select value={historyPageSize} onChange={e => {
          setHistoryPageSize(Number(e.currentTarget.value));
          setHistoryPage(0); setHistoryEventId("");
        }}>
          {FICTIONAL_HISTORY_PAGE_SIZES.map(size =>
            <option key={size} value={size}>{size} identifiants</option>)}
        </select>
      </label>
      <p role="note" aria-live="polite">Page {historyView.index + 1} sur {historyView.pages}
        {" — "}{historyView.total} identifiants fictifs trouvés.</p>
      <button type="button" disabled={historyView.index === 0}
        onClick={() => { setHistoryEventId(""); setHistoryPage(historyView.index - 1); }}>
        Page précédente
      </button>
      <button type="button" disabled={historyView.index + 1 >= historyView.pages}
        onClick={() => { setHistoryEventId(""); setHistoryPage(historyView.index + 1); }}>
        Page suivante
      </button>
      <label>Événement fictif à examiner
        <select value={historyEventId}
          onChange={e => setHistoryEventId(e.currentTarget.value)}>
          <option value="">Choisir un événement historique</option>
          {historyView.ids.map(id => <option key={id} value={id}>{id}</option>)}
        </select>
      </label>
      {inspectedHistory.length > 0 && <ol aria-label="Versions historiques fictives">
        {inspectedHistory.map(entry => <li key={entry.event.version}>
          <strong>Version {entry.event.version} — {entry.event.status}</strong>
          <p>Titre historique : {entry.event.title}</p>
          <p>Note historique : {entry.event.note || "aucune"}</p>
          <p>Ancre historique : {entry.event.anchor_id ?? "aucune"}</p>
          <p>Révision source historique : {entry.event.source_revision_id ?? "aucune"}</p>
          <p>Personnages de la révision source fictive : {book.draft.revisions
            .find(r => r.revision_id === entry.event.source_revision_id)
            ?.fictional_character_ids?.join(", ") || "aucune association explicite"}</p>
          <p>Action fictive : {entry.audit.action}</p>
          <p>Motif humain historique : {entry.audit.explanation}</p>
          <p>Champs modifiés : {entry.changed_fields.join(", ") || "aucun (création)"}</p>
          {entry.field_differences.map(diff => <dl key={diff.field}>
            <dt>Écart : {diff.field}</dt>
            <dd>Avant : {diff.before ?? "aucun"} ; après : {diff.after ?? "aucun"}</dd>
          </dl>)}
        </li>)}
      </ol>}
    </section>
    <button type="button" aria-expanded={compareOpen}
      aria-controls="m32-fictional-live-comparison"
      onClick={() => setCompareOpen(open => !open)}>
      {compareOpen ? "Masquer la comparaison des versions fictives" :
        "Comparer les versions créées dans cet atelier fictif"}
    </button>
    {compareOpen && <div id="m32-fictional-live-comparison">
      <M32FictionalEventVersionPairLab notebook={book} />
    </div>}
    <p>Historique préservé : {book.events.length} versions ;
      {book.audit.length} opérations fictives.</p>
  </section>;
}
