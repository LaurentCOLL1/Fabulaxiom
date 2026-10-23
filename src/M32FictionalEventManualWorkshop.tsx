import { useState, type FormEvent, type ReactElement } from "react";
import {
  amendFictionalEvent, createFictionalEvent, currentFictionalEvents,
  inspectFictionalEventNotebook, withdrawFictionalEvent,
  type FictionalEventInput, type FictionalEventNotebook,
} from "./m32FictionalEventNotebook";

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

  const activeAnchors = book.draft.snapshot.anchors.filter(a => a.status === "current");
  const currentEvents = currentFictionalEvents(book);
  function clearSelection() {
    setSelectedId(""); setTitle(""); setNote("");
    setAnchor(""); setRevision(""); setReason("");
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
    setFeedback("");
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
        <select value={revision} onChange={e => setRevision(e.target.value)}>
          <option value="">Aucune révision</option>
          {book.draft.revisions.map(r =>
            <option key={r.revision_id} value={r.revision_id}>
              {r.revision_label} ({r.revision_id})
            </option>)}
        </select>
      </label>
      <label>Justification de correction ou de retrait
        <input value={reason} onChange={e => setReason(e.target.value)}
          maxLength={240} required={Boolean(selectedId)} />
      </label>
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
    <p>Historique préservé : {book.events.length} versions ;
      {book.audit.length} opérations fictives.</p>
  </section>;
}
