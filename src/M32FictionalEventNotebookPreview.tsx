import type { ReactElement } from "react";
import {
  auditedFictionalEventHistory, currentFictionalEvents, inspectFictionalEventNotebook,
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
    <section aria-label="Historique des versions fictives">
      <h3>Historique manuel des versions et justifications</h3>
      <p role="note">Audit structurel inventé et non authentifié :
        aucune reconstitution de source réelle, aucune date déduite.</p>
      <ul>{notebook.events.filter(e => e.version === 1).map(created => {
        const history = auditedFictionalEventHistory(notebook, created.event_id);
        const latest = history[history.length - 1].event;
        return <li key={created.event_id}>
          <details>
            <summary>{latest.title} — {latest.status === "withdrawn" ? "retiré" : "courant"}
              {" — " + history.length + " version(s)"}</summary>
            <ol>{history.map(({ event, audit, changed_fields }) => <li key={event.version}>
              Version {event.version} — {audit.action} — {event.status}
              {" ; justification : " + audit.explanation}
              {" ; modifications de contenu : " + (changed_fields.length
                ? changed_fields.map(field => ({
                  title: "titre", note: "note", anchor_id: "ancre",
                  source_revision_id: "révision",
                }[field])).join(", ")
                : "aucune")}
              {" ; titre : " + event.title}
              {event.note ? " ; note : " + event.note : ""}
              {event.anchor_id === null ? " ; sans date liée" :
                " ; ancre explicite : " + event.anchor_id}
              {event.source_revision_id === null ? "" :
                " ; révision source exacte : " + event.source_revision_id}
            </li>)}</ol>
          </details>
        </li>;
      })}</ul>
    </section>
  </section>;
}
