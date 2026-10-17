import type { ReactElement } from "react";
import {
  decodeM32ChronologyProjection,
  type M32ChronologyProjection,
  type M32PrecedenceProjection,
} from "./M32ChronologyPreview";

/**
 * M3.2 synthetic-only, unmouted world-time pair inspection.
 * No Tauri command, live DB, user identity, filesystem, network or write.
 * A human-authored active precedence graph is NOT a global time axis.
 */
export type M32WorldRelation = "same" | "before" | "after" | "incomparable";
export type M32WitnessStep = Readonly<{
  precedence_id: string;
  before_anchor_id: string;
  after_anchor_id: string;
  human_reason: string;
}>;
export type M32WorldComparison = Readonly<{
  left_anchor_id: string;
  right_anchor_id: string;
  relation: M32WorldRelation;
  witness: readonly M32WitnessStep[];
  data_origin: "synthetic_in_memory_only";
  edit_controls_available: false;
}>;

function nonblank(v: unknown): v is string {
  return typeof v === "string" && v.trim().length > 0;
}
function refused(message: string): never {
  throw new Error("Comparaison M3.2 refusée : " + message);
}
function witnessStep(edge: M32PrecedenceProjection): M32WitnessStep {
  return {
    precedence_id: edge.id,
    before_anchor_id: edge.before_anchor_id,
    after_anchor_id: edge.after_anchor_id,
    human_reason: edge.reason,
  };
}

/** A bounded breadth-first proof over ONLY currently active declared edges.
 * Sorted by immutable edge ID so the choice among multiple witnesses is stable.
 * A returned witness is an illustrative authored chain, not an audit signature.
 */
function findWitness(
  adjacency: ReadonlyMap<string, readonly M32PrecedenceProjection[]>,
  start: string,
  goal: string,
): readonly M32WitnessStep[] | null {
  const visited = new Set<string>([start]);
  const pending: { id: string; witness: readonly M32WitnessStep[] }[] = [
    { id: start, witness: [] },
  ];
  for (let i = 0; i < pending.length; i += 1) {
    const item = pending[i];
    for (const edge of adjacency.get(item.id) ?? []) {
      if (visited.has(edge.after_anchor_id)) continue;
      const path = [...item.witness, witnessStep(edge)];
      if (edge.after_anchor_id === goal) return path;
      visited.add(edge.after_anchor_id);
      pending.push({ id: edge.after_anchor_id, witness: path });
    }
  }
  return null;
}

export function compareM32WorldOrder(
  snapshot: M32ChronologyProjection,
  expectedUniverseId: string,
  leftAnchorId: string,
  rightAnchorId: string,
): M32WorldComparison {
  const checked = decodeM32ChronologyProjection(snapshot, expectedUniverseId);
  if (!nonblank(leftAnchorId) || !nonblank(rightAnchorId)) {
    return refused("deux identifiants explicites sont requis");
  }
  const byId = new Map(checked.anchors.map(anchor => [anchor.id, anchor]));
  const left = byId.get(leftAnchorId);
  const right = byId.get(rightAnchorId);
  if (!left || !right || left.status !== "current" || right.status !== "current") {
    return refused("identifiant étranger, absent ou historique");
  }

  const activeEdges = checked.precedences.filter(edge => edge.status === "current");
  const endpointPairs = new Set<string>();
  const adjacency = new Map<string, M32PrecedenceProjection[]>();
  const degrees = new Map<string, number>();
  for (const anchor of checked.anchors) {
    if (anchor.status === "current") {
      adjacency.set(anchor.id, []);
      degrees.set(anchor.id, 0);
    }
  }

  for (const edge of activeEdges) {
    if (!adjacency.has(edge.before_anchor_id) || !adjacency.has(edge.after_anchor_id)) {
      return refused("relation active vers une assertion historique");
    }
    // Pair serialization is internal to the toy and cannot confuse e.g. a:b / ab:c.
    const pair = JSON.stringify([edge.before_anchor_id, edge.after_anchor_id]);
    if (endpointPairs.has(pair)) return refused("relation active doublonnée");
    endpointPairs.add(pair);
    adjacency.get(edge.before_anchor_id)!.push(edge);
    degrees.set(edge.after_anchor_id, degrees.get(edge.after_anchor_id)! + 1);
  }
  for (const outgoing of adjacency.values()) {
    outgoing.sort((a, b) => a.id.localeCompare(b.id));
  }

  // Fail closed on a cycle anywhere in the current graph, even if the
  // selected endpoints are not directly involved.
  const zeroDegree = [...degrees.keys()].filter(id => degrees.get(id) === 0);
  let traversed = 0;
  for (let i = 0; i < zeroDegree.length; i += 1) {
    const current = zeroDegree[i];
    traversed += 1;
    for (const edge of adjacency.get(current) ?? []) {
      const newDegree = degrees.get(edge.after_anchor_id)! - 1;
      degrees.set(edge.after_anchor_id, newDegree);
      if (newDegree === 0) zeroDegree.push(edge.after_anchor_id);
    }
  }
  if (traversed !== degrees.size) return refused("cycle de précédence active");

  if (leftAnchorId === rightAnchorId) {
    return {
      left_anchor_id: leftAnchorId, right_anchor_id: rightAnchorId,
      relation: "same", witness: [], data_origin: "synthetic_in_memory_only",
      edit_controls_available: false,
    };
  }
  const forward = findWitness(adjacency, leftAnchorId, rightAnchorId);
  const reverse = forward ? null : findWitness(adjacency, rightAnchorId, leftAnchorId);
  return {
    left_anchor_id: leftAnchorId,
    right_anchor_id: rightAnchorId,
    relation: forward ? "before" : reverse ? "after" : "incomparable",
    witness: forward ?? reverse ?? [],
    data_origin: "synthetic_in_memory_only",
    edit_controls_available: false,
  };
}

const descriptions: Record<M32WorldRelation, string> = {
  same: "Même assertion : identité exacte, sans relation inventée",
  before: "Avant : précédence humaine explicite ou transitive",
  after: "Après : précédence humaine explicite ou transitive",
  incomparable: "Ordre indéterminé : aucune précédence humaine ne relie ces assertions",
};

/** Unmounted React preview. No text inference and no editing controls. */
export default function M32WorldOrderComparison({
  expectedUniverseId, snapshot, leftAnchorId, rightAnchorId,
}: {
  expectedUniverseId: string;
  snapshot: M32ChronologyProjection | null;
  leftAnchorId: string;
  rightAnchorId: string;
}): ReactElement {
  if (!snapshot) {
    return <section role="status" aria-label="Comparaison M3.2 isolée">
      <h2>Comparaison chronologique — aucune donnée synthétique fournie</h2>
    </section>;
  }
  let value: M32WorldComparison;
  try {
    value = compareM32WorldOrder(
      snapshot, expectedUniverseId, leftAnchorId, rightAnchorId,
    );
  } catch {
    return <section role="alert" aria-label="Comparaison M3.2 refusée">
      <h2>Comparaison refusée</h2>
      <p>Univers, sources ou précédences non qualifiés. Aucune conclusion affichée.</p>
    </section>;
  }
  return <section aria-label="Comparaison M3.2 isolée">
    <h2>Comparaison de chronologie fictive — lecture seule</h2>
    <p>Univers : <code>{expectedUniverseId}</code></p>
    <p>Deux assertions explicitement sélectionnées :
      {" "}<code>{value.left_anchor_id}</code> / <code>{value.right_anchor_id}</code>
    </p>
    <p role="status">{descriptions[value.relation]}</p>
    {value.witness.length ? <section aria-label="Justification des précédences">
      <h3>Relations humaines justificatives</h3>
      <ol>{value.witness.map(step => <li key={step.precedence_id}>
        <code>{step.before_anchor_id}</code> avant <code>{step.after_anchor_id}</code>
        {" — "}<code>{step.precedence_id}</code>
        {" — motif : "}{step.human_reason}
      </li>)}</ol>
    </section> : <p>Aucune chaîne de précédences n’est inventée.</p>}
    <p>La liste n’établit aucun ordre total ni calendrier grégorien.</p>
    <p>Les anciennes assertions sont consultables ailleurs mais ne servent pas
      de preuve d’ordre courant. Aucune modification ni commande IPC disponible.</p>
  </section>;
}
