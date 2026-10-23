import type { ReactElement } from "react";
import { inspectFictionalDraft, type FictionalDraft } from "./m32FictionalManualChronology";

/**
 * M3.2 two-Universe visual rehearsal ONLY. Not registered in App.tsx.
 * No Tauri invoke, storage, network, local file, SQLite or operator data.
 * Never form an inter-Universe chronology or infer reader revelation.
 */
export default function M32TwoUniverseSafetyPreview({ left, right }: {
  left: FictionalDraft; right: FictionalDraft;
}): ReactElement {
  inspectFictionalDraft(left);
  inspectFictionalDraft(right);
  if (left.snapshot.universe_id === right.snapshot.universe_id) {
    throw new Error("Comparaison M3.2 refusée : deux univers fictifs distincts sont obligatoires.");
  }
  return <section aria-label="Comparaison de deux univers fictifs isolés">
    <h2>Deux univers fictifs — aucune chronologie commune</h2>
    <p role="note">Simulation en mémoire seulement. Aucun accès Windows, SQLite,
      aucune sauvegarde et aucune connaissance du lecteur déduite.</p>
    {[left, right].map((draft) => <section key={draft.snapshot.universe_id}
      aria-label={"Univers fictif " + draft.snapshot.universe_id}>
      <h3>{draft.snapshot.universe_id}</h3>
      <p>Ancres courantes : {draft.snapshot.anchors.filter(a => a.status === "current").length}</p>
      <p>Relations humaines courantes : {draft.snapshot.precedences.filter(e => e.status === "current").length}</p>
      <p>Romans distincts : {new Set(draft.snapshot.narration.map(s => s.novel_id)).size}</p>
      <p>Révélation au lecteur : non renseignée (lecture seule).</p>
    </section>)}
    <p>Les positions de narration et les dates de ces univers ne sont jamais comparées entre elles.</p>
  </section>;
}
