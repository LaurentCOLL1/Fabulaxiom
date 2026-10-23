import type { ReactElement } from "react";
import {
  currentFictionalEvents, inspectFictionalEventNotebook,
  type FictionalEventNotebook,
} from "./m32FictionalEventNotebook";

/** Read-only notebook inspection; not mounted by App.tsx or connected to Tauri. */
export default function M32FictionalEventNotebookPreview({ notebook }: {
  notebook: FictionalEventNotebook;
}): ReactElement {
  inspectFictionalEventNotebook(notebook);
  const current = currentFictionalEvents(notebook);
  const withdrawn = notebook.events.filter(e => e.status === "withdrawn").length;
  return <section aria-label="Carnet d'événements fictifs sans sauvegarde">
    <h2>Carnet manuel fictif — {notebook.draft.snapshot.universe_id}</h2>
    <p role="note">Mémoire de démonstration seulement : aucune écriture SQLite,
      aucun ordre mondial calculé, aucune révélation du lecteur déduite.</p>
    <p>Événements courants : {current.length} ; retraits historiques : {withdrawn}</p>
    <ul>{current.map(event => <li key={event.event_id}>
      {event.title} — version {event.version}
      {event.anchor_id === null ? " (date non liée)" :
        " (ancre explicite : " + event.anchor_id + ")"}
    </li>)}</ul>
  </section>;
}
