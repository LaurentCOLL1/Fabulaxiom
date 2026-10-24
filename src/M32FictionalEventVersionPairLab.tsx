import { useState, type ReactElement } from "react";
import {
  auditedFictionalEventHistory, inspectFictionalEventNotebook,
  type FictionalEventNotebook,
} from "./m32FictionalEventNotebook";
import M32FictionalEventNotebookPreview, {
  type FictionalVersionPreviewSelection,
} from "./M32FictionalEventNotebookPreview";

/** Browser-fixture-only selector. No user database, app mount, persistence or IPC. */
export default function M32FictionalEventVersionPairLab({ notebook }: {
  notebook: FictionalEventNotebook;
}): ReactElement {
  inspectFictionalEventNotebook(notebook);
  const [eventId, setEventId] = useState("");
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const created = notebook.events.filter(e => e.version === 1);
  const versions = eventId
    ? auditedFictionalEventHistory(notebook, eventId).map(item => item.event.version)
    : [];
  const start = from === "" ? null : Number(from);
  const end = to === "" ? null : Number(to);
  const selection: FictionalVersionPreviewSelection | undefined =
    start !== null && end !== null && Number.isSafeInteger(start) &&
    Number.isSafeInteger(end) && start < end &&
    versions.includes(start) && versions.includes(end)
      ? { event_id: eventId, from_version: start, to_version: end }
      : undefined;
  return <section aria-label="Laboratoire de sélection de versions fictives">
    <h2>Sélection manuelle — versions d'un même événement inventé</h2>
    <p role="note">Laboratoire navigateur isolé, données inventées en RAM :
      sans persistance, commande Tauri, SQLite ou date inférée.</p>
    <label>Événement fictif à comparer
      <select value={eventId} onChange={e => {
        setEventId(e.target.value); setFrom(""); setTo("");
      }}>
        <option value="">Choisir un événement inventé</option>
        {created.map(item => <option key={item.event_id} value={item.event_id}>
          {item.event_id} — {item.title}
        </option>)}
      </select>
    </label>
    <label>Version fictive de départ
      <select value={from} disabled={!eventId} onChange={e => {
        setFrom(e.target.value); setTo("");
      }}>
        <option value="">Choisir la version de départ</option>
        {versions.slice(0, -1).map(v => <option key={v} value={String(v)}>
          Version {v}
        </option>)}
      </select>
    </label>
    <label>Version fictive d'arrivée
      <select value={to} disabled={!from} onChange={e => setTo(e.target.value)}>
        <option value="">Choisir la version d'arrivée</option>
        {versions.filter(v => start !== null && v > start).map(v =>
          <option key={v} value={String(v)}>Version {v}</option>)}
      </select>
    </label>
    <p role="status" aria-live="polite">
      {selection ? "Paire explicite de versions fictives validée." :
        "Sélectionnez un événement et deux versions strictement croissantes."}
    </p>
    <M32FictionalEventNotebookPreview notebook={notebook} selection={selection} />
  </section>;
}
