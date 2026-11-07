import type { ReactElement } from "react";
import {
  previewP2kFictionalAnchorEvidence,
} from "./M32P2kFictionalAnchorEvidence";
import type {
  P2iFictionalEdge, P2iFictionalInput,
} from "./M32P2iFictionalImpactReview";

/**
 * P2m: review the union of DIRECT changed assertions for TWO fictional
 * touched anchors, counting a shared assertion once. This is not an
 * inferred chronology, transitive impact, save operation, or real P4.
 */
export type P2mFictionalWitness = Readonly<{
  edge: P2iFictionalEdge;
  change: "removed" | "added";
  touches_first: boolean;
  touches_second: boolean;
}>;

export type P2mFictionalSharedEvidence = Readonly<{
  first_anchor_id: string;
  second_anchor_id: string;
  shared: readonly P2mFictionalWitness[];
  first_only: readonly P2mFictionalWitness[];
  second_only: readonly P2mFictionalWitness[];
  data_origin: "fictional_browser_memory_only";
  production_writer_admitted: false;
  real_g3_authorized: false;
}>;

function signature(change: "removed" | "added", edge: P2iFictionalEdge): string {
  return JSON.stringify([
    change, edge.id, edge.before_anchor_id, edge.after_anchor_id, edge.origin,
  ]);
}

export function previewP2mFictionalSharedEvidence(
  input: P2iFictionalInput,
  expectedUniverse: string,
  firstAnchor: string,
  secondAnchor: string,
): P2mFictionalSharedEvidence {
  if (typeof firstAnchor !== "string" || typeof secondAnchor !== "string" ||
      !firstAnchor.trim() || !secondAnchor.trim() || firstAnchor === secondAnchor) {
    throw new Error("P2m : deux ancres fictives distinctes sont requises");
  }
  // P2k inherits all P2i/P2j refusals and rejects unchanged-only anchors.
  const first = previewP2kFictionalAnchorEvidence(input, expectedUniverse, firstAnchor);
  const second = previewP2kFictionalAnchorEvidence(input, expectedUniverse, secondAnchor);
  const union = new Map<string, {
    edge: P2iFictionalEdge;
    change: "removed" | "added";
    touches_first: boolean;
    touches_second: boolean;
  }>();
  const include = (
    edges: readonly P2iFictionalEdge[],
    change: "removed" | "added",
    side: "touches_first" | "touches_second",
  ) => {
    for (const edge of edges) {
      const key = signature(change, edge);
      const entry = union.get(key) ?? {
        edge, change, touches_first: false, touches_second: false,
      };
      entry[side] = true;
      union.set(key, entry);
    }
  };
  include(first.removed, "removed", "touches_first");
  include(first.added, "added", "touches_first");
  include(second.removed, "removed", "touches_second");
  include(second.added, "added", "touches_second");

  // Lexical display order is a property of assertion values, never of time.
  const witnesses = [...union.entries()]
    .sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)
    .map(([, witness]) => witness);
  return {
    first_anchor_id: first.anchor_id,
    second_anchor_id: second.anchor_id,
    shared: witnesses.filter(w => w.touches_first && w.touches_second),
    first_only: witnesses.filter(w => w.touches_first && !w.touches_second),
    second_only: witnesses.filter(w => !w.touches_first && w.touches_second),
    data_origin: "fictional_browser_memory_only",
    production_writer_admitted: false,
    real_g3_authorized: false,
  };
}

export default function M32P2mFictionalSharedEvidence({
  input, expectedUniverse, firstAnchor, secondAnchor,
}: {
  input: P2iFictionalInput;
  expectedUniverse: string;
  firstAnchor: string;
  secondAnchor: string;
}): ReactElement {
  let evidence: P2mFictionalSharedEvidence;
  try {
    evidence = previewP2mFictionalSharedEvidence(
      input, expectedUniverse, firstAnchor, secondAnchor,
    );
  } catch {
    return <section role="alert" aria-label="Comparaison fictive refusée">
      <h2>Comparaison fictive refusée</h2>
      <p>Ancres, univers ou assertions invalides. Aucune commande exécutée.</p>
    </section>;
  }
  const groups = [
    { label: "Assertions communes aux deux ancres", edges: evidence.shared },
    { label: "Assertions propres à la première ancre", edges: evidence.first_only },
    { label: "Assertions propres à la seconde ancre", edges: evidence.second_only },
  ] as const;
  return <section aria-label="Comparaison fictive des assertions directement modifiées">
    <h2>Comparaison directe de deux ancres — fiction uniquement</h2>
    <p>Ancres sélectionnées : <code>{evidence.first_anchor_id}</code> et{" "}
      <code>{evidence.second_anchor_id}</code>.</p>
    <p>Chaque assertion directement modifiée apparaît une seule fois.
      Les relations inchangées sont exclues ; aucune transitivité, date,
      ordre total du monde ou priorité narrative ne sont inférés.</p>
    {groups.map(group => <section key={group.label} aria-label={group.label}>
      <h3>{group.label} ({group.edges.length})</h3>
      {group.edges.length === 0 ? <p>Aucune.</p> :
        <ul>{group.edges.map(item =>
          <li key={signature(item.change, item.edge)}>
            <strong>{item.change === "removed" ? "Retirée" : "Ajoutée"}</strong>
            {" — "}<code>{item.edge.id}</code> : <code>{item.edge.before_anchor_id}</code>
            {" avant "}<code>{item.edge.after_anchor_id}</code>
            {" — "}{item.edge.origin === "restatement" ? "reformulation" : "assertion initiale"}
          </li>,
        )}</ul>}
    </section>)}
    <p>Lecture seule en mémoire fictive. Aucun writer, Tauri IPC ni donnée opérateur.
      G3 STOP_UNAVAILABLE.</p>
  </section>;
}
