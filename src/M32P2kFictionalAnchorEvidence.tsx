import type { ReactElement } from "react";
import {
  previewP2iFictionalImpact,
  type P2iFictionalEdge,
  type P2iFictionalInput,
} from "./M32P2iFictionalImpactReview";
import { previewP2jFictionalTouchedAnchors } from "./M32P2jFictionalTouchedAnchors";

/**
 * P2k: show only the directly changed assertions incident to one fictional
 * touched anchor. This is NOT transitive impact, chronology, provenance from
 * operator data, a production writer, or an App.tsx-integrated feature.
 */
export type P2kFictionalDirectEvidence = Readonly<{
  anchor_id: string;
  removed: readonly P2iFictionalEdge[];
  added: readonly P2iFictionalEdge[];
  data_origin: "fictional_browser_memory_only";
  production_writer_admitted: false;
  real_g3_authorized: false;
}>;

function signature(edge: P2iFictionalEdge): string {
  return JSON.stringify([
    edge.id, edge.before_anchor_id, edge.after_anchor_id, edge.origin,
  ]);
}

export function previewP2kFictionalAnchorEvidence(
  input: P2iFictionalInput,
  expectedUniverse: string,
  selectedAnchor: string,
): P2kFictionalDirectEvidence {
  // P2j applies the complete P2i provenance, universe, cycle, self-link and
  // duplicate checks. A selection absent from changed edges fails closed.
  const touched = previewP2jFictionalTouchedAnchors(input, expectedUniverse);
  if (typeof selectedAnchor !== "string" || !selectedAnchor.trim() ||
      !touched.anchors.some(anchor => anchor.anchor_id === selectedAnchor)) {
    throw new Error("P2k : ancre fictive non touchée ou sélection refusée");
  }
  const impact = previewP2iFictionalImpact(input, expectedUniverse);
  const direct = (edges: readonly P2iFictionalEdge[]) => edges
    .filter(edge => edge.before_anchor_id === selectedAnchor ||
                    edge.after_anchor_id === selectedAnchor)
    .sort((a, b) => {
      const x = signature(a), y = signature(b);
      return x < y ? -1 : x > y ? 1 : 0;
    });
  return {
    anchor_id: selectedAnchor,
    removed: direct(impact.removed),
    added: direct(impact.added),
    data_origin: "fictional_browser_memory_only",
    production_writer_admitted: false,
    real_g3_authorized: false,
  };
}

export default function M32P2kFictionalAnchorEvidence({
  input, expectedUniverse, selectedAnchor,
}: {
  input: P2iFictionalInput;
  expectedUniverse: string;
  selectedAnchor: string;
}): ReactElement {
  let evidence: P2kFictionalDirectEvidence;
  try {
    evidence = previewP2kFictionalAnchorEvidence(input, expectedUniverse, selectedAnchor);
  } catch {
    return <section role="alert" aria-label="Preuves fictives refusées">
      <h2>Preuves fictives refusées</h2>
      <p>Ancre, univers ou relations non valides. Aucune commande exécutée.</p>
    </section>;
  }
  const groups = [
    { label: "Relations directement retirées", edges: evidence.removed },
    { label: "Relations directement ajoutées", edges: evidence.added },
  ] as const;
  return <section aria-label="Relations directes pour une ancre fictive">
    <h2>Preuves directes de correction — fiction uniquement</h2>
    <p>Ancre touchée : <code>{evidence.anchor_id}</code></p>
    <p>Seules les assertions modifiées mentionnant directement cette ancre
      sont affichées, sans déduction de date, transitivité, chronologie totale,
      ordre narratif ou révélation ne sont déduits.</p>
    {groups.map(group => <section key={group.label} aria-label={group.label}>
      <h3>{group.label} ({group.edges.length})</h3>
      {group.edges.length === 0
        ? <p>Aucune.</p>
        : <ul>{group.edges.map(edge => <li key={signature(edge)}>
          <code>{edge.id}</code> : <code>{edge.before_anchor_id}</code> avant
          {" "}<code>{edge.after_anchor_id}</code>
          {" — "}{edge.origin === "restatement" ? "reformulation" : "assertion initiale"}
        </li>)}</ul>}
    </section>)}
    <p>Lecture seule en mémoire fictive : aucun writer, aucun Tauri IPC,
      aucune donnée opérateur. G3 STOP_UNAVAILABLE.</p>
  </section>;
}
