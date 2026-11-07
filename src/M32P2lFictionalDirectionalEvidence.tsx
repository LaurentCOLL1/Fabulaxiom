import type { ReactElement } from "react";
import { previewP2kFictionalAnchorEvidence } from "./M32P2kFictionalAnchorEvidence";
import type { P2iFictionalInput, P2iFictionalEdge } from "./M32P2iFictionalImpactReview";

/** P2l: direct changed-assertion directions, fictional browser memory only.
 * No transitive impact, total world order, narrative, disk, IPC or writer.
 */
export type P2lFictionalDirectionalEvidence = Readonly<{
  anchor_id: string;
  removed_incoming: readonly P2iFictionalEdge[];
  removed_outgoing: readonly P2iFictionalEdge[];
  added_incoming: readonly P2iFictionalEdge[];
  added_outgoing: readonly P2iFictionalEdge[];
  data_origin: "fictional_browser_memory_only";
  production_writer_admitted: false;
  real_g3_authorized: false;
}>;
function signature(e: P2iFictionalEdge): string {
  return JSON.stringify([e.id, e.before_anchor_id, e.after_anchor_id, e.origin]);
}
export function previewP2lFictionalDirectionalEvidence(
  input: P2iFictionalInput, expectedUniverse: string, selectedAnchor: string,
): P2lFictionalDirectionalEvidence {
  // Inherits P2i/P2j/P2k source, universe, DAG, and touched-selection vetoes.
  const direct = previewP2kFictionalAnchorEvidence(input, expectedUniverse, selectedAnchor);
  const incoming = (edges: readonly P2iFictionalEdge[]) =>
    edges.filter(edge => edge.after_anchor_id === direct.anchor_id);
  const outgoing = (edges: readonly P2iFictionalEdge[]) =>
    edges.filter(edge => edge.before_anchor_id === direct.anchor_id);
  return {
    anchor_id: direct.anchor_id,
    removed_incoming: incoming(direct.removed),
    removed_outgoing: outgoing(direct.removed),
    added_incoming: incoming(direct.added),
    added_outgoing: outgoing(direct.added),
    data_origin: "fictional_browser_memory_only",
    production_writer_admitted: false, real_g3_authorized: false,
  };
}
export default function M32P2lFictionalDirectionalEvidence({
  input, expectedUniverse, selectedAnchor,
}: {
  input: P2iFictionalInput; expectedUniverse: string; selectedAnchor: string;
}): ReactElement {
  let result: P2lFictionalDirectionalEvidence;
  try {
    result = previewP2lFictionalDirectionalEvidence(input, expectedUniverse, selectedAnchor);
  } catch {
    return <section role="alert" aria-label="Directions fictives refusées">
      <h2>Directions fictives refusées</h2>
      <p>Sélection, provenance ou relations invalides. Aucune commande exécutée.</p>
    </section>;
  }
  const groups = [
    { title: "Retirées vers l’ancre", edges: result.removed_incoming },
    { title: "Retirées depuis l’ancre", edges: result.removed_outgoing },
    { title: "Ajoutées vers l’ancre", edges: result.added_incoming },
    { title: "Ajoutées depuis l’ancre", edges: result.added_outgoing },
  ] as const;
  return <section aria-label="Directions des assertions fictives directement modifiées">
    <h2>Directions des corrections directes — fiction uniquement</h2>
    <p>Ancre sélectionnée : <code>{result.anchor_id}</code></p>
    <p>« Vers » et « depuis » désignent uniquement les extrémités des assertions
      directement modifiées. Aucune transitivité, date, chronologie totale
      ni priorité narrative n’est déduite.</p>
    {groups.map(group => <section key={group.title} aria-label={group.title}>
      <h3>{group.title} ({group.edges.length})</h3>
      {group.edges.length === 0 ? <p>Aucune.</p> :
        <ul>{group.edges.map(edge => <li key={signature(edge)}>
          <code>{edge.id}</code> : <code>{edge.before_anchor_id}</code> avant
          {" "}<code>{edge.after_anchor_id}</code>
          {" — "}{edge.origin === "restatement" ? "reformulation" : "assertion initiale"}
        </li>)}</ul>}
    </section>)}
    <p>Lecture seule, mémoire fictive uniquement. Aucun writer, aucune commande
      Tauri ni donnée opérateur. G3 STOP_UNAVAILABLE.</p>
  </section>;
}
