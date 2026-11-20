import { useState, type FormEvent, type ReactElement } from "react";
import {
  amendFictionalEvent, createFictionalEvent, currentFictionalEvents,
  inspectFictionalEventNotebook, prepareFictionalEventHistoricalDraft,
  auditedFictionalEventHistory, withdrawFictionalEvent,
  type FictionalEventInput, type FictionalEventNotebook,
} from "./m32FictionalEventNotebook";
import M32FictionalEventVersionPairLab from "./M32FictionalEventVersionPairLab";
import type { FictionalRevision } from "./m32FictionalManualChronology";

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
): readonly string[] {
  inspectFictionalEventNotebook(notebook);
  const query = searchId.trim().toLocaleLowerCase();
  // Opaque source IDs use exact matching, including superseded versions.
  const sourceId = exactSourceRevisionId.trim();
  const novelId = exactSourceNovelId.trim();
  const sceneId = exactSourceSceneId.trim();
  const sourceRevisionById = new Map(
    notebook.draft.revisions.map(r => [r.revision_id, r]));
  return notebook.events.filter(e => e.version === 1).map(e => e.event_id)
    .filter(id => {
      const versions = notebook.events.filter(e => e.event_id === id);
      const latest = versions[versions.length - 1];
      return Boolean(latest && (status === "all" || latest.status === status) &&
        id.toLocaleLowerCase().includes(query) &&
        ((!sourceId && !novelId && !sceneId) || versions.some(v => {
          // All source selectors must match one historical event version.
          const revision = v.source_revision_id === null ? undefined :
            sourceRevisionById.get(v.source_revision_id);
          return (!sourceId || v.source_revision_id === sourceId) &&
            (!novelId || revision?.novel_id === novelId) &&
            (!sceneId || revision?.scene_id === sceneId);
        })));
    });
}

/** Paged IDs only; never implicitly inspect or mutate a fictional event. */
export const FICTIONAL_HISTORY_PAGE_SIZE = 10;
export function pageFictionalEventHistoryIds(ids: readonly string[], page: number):
  Readonly<{ ids: readonly string[]; index: number; pages: number; total: number }> {
  if (!Number.isSafeInteger(page) || page < 0) throw Error("Page fictive invalide");
  const pages = Math.max(1, Math.ceil(ids.length / FICTIONAL_HISTORY_PAGE_SIZE));
  const index = Math.min(page, pages - 1);
  return { ids: ids.slice(index * FICTIONAL_HISTORY_PAGE_SIZE,
    (index + 1) * FICTIONAL_HISTORY_PAGE_SIZE), index, pages, total: ids.length };
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
  const [historySceneId, setHistorySceneId] = useState("");
  const [historyPage, setHistoryPage] = useState(0);
  const [historyStatus, setHistoryStatus] =
    useState<"all" | "current" | "withdrawn">("all");

  const activeAnchors = book.draft.snapshot.anchors.filter(a => a.status === "current");
  const eligibleRevisions = eligibleFictionalEventRevisions(book, anchor);
  const currentEvents = currentFictionalEvents(book);
  // Creation IDs remain available after a withdrawal; a tombstone is history,
  // not permission to restore a past event or change the current manuscript.
  const sourceNovelIds = [...new Set(book.draft.revisions.map(r => r.novel_id))];
  const sourceSceneIds = [...new Set(book.draft.revisions.map(r => r.scene_id))];
  const historyEventIds = matchingFictionalEventHistoryIds(
    book, historyIdQuery, historyStatus, historySourceIdQuery, historyNovelId,
    historySceneId);
  const historyView = pageFictionalEventHistoryIds(historyEventIds, historyPage);
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
    <p role="note">Démonstration exclusivement en mémoire du navigateur.
      Aucun enregistrement, aucun accès SQLite, aucune commande Tauri,
      aucune chronologie ou révélation du lecteur calculée automatiquement.</p>
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
      <button type="submit">{selectedId ? "Enregistrer une nouvelle version" :
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
      <label>Filtrer par scène de révision source fictive
        <select value={historySceneId} onChange={e => {
          setHistorySceneId(e.currentTarget.value);
          setHistoryEventId(""); setHistoryPage(0);
        }}>
          <option value="">Toutes les scènes sources fictives</option>
          {sourceSceneIds.map(id => <option key={id} value={id}>{id}</option>)}
        </select>
      </label>
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
      <p role="note">Le filtrage n'affiche aucune version ni motif historique.
        Choisissez un identifiant pour consulter les versions en lecture seule.</p>
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
