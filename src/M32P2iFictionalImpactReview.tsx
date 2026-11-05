import type { ReactElement } from "react";

/**
 * P2i FICTION-ONLY author review of the typed P2h before/after concept.
 * No Rust/IPC bridge exists. The caller MUST provide invented in-memory values.
 * Never imported by App.tsx; no confirmation, persistence or operator access.
 */
export type P2iFictionalEdge = Readonly<{
  id: string;
  universe_id: string;
  before_anchor_id: string;
  after_anchor_id: string;
  origin: "original" | "restatement";
}>;

export type P2iFictionalInput = Readonly<{
  data_origin: "fictional_browser_memory_only";
  production_writer_admitted: false;
  real_g3_authorized: false;
  universe_id: string;
  active_before: readonly P2iFictionalEdge[];
  active_after: readonly P2iFictionalEdge[];
}>;

export type P2iFictionalImpact = Readonly<{
  removed: readonly P2iFictionalEdge[];
  added: readonly P2iFictionalEdge[];
  unchanged: readonly P2iFictionalEdge[];
  data_origin: "fictional_browser_memory_only";
  production_writer_admitted: false;
  real_g3_authorized: false;
}>;

function reject(): never {
  throw new Error("P2i : provenance ou chronologie fictive refusée");
}
function nonblank(s: unknown): s is string {
  return typeof s === "string" && s.trim().length > 0;
}
function signature(edge: P2iFictionalEdge): string {
  // Mirrors P2h full edge-value comparison, NOT a same-ID comparison.
  return JSON.stringify([
    edge.id, edge.before_anchor_id, edge.after_anchor_id, edge.origin,
  ]);
}
function validateGraph(edges: readonly P2iFictionalEdge[], universe: string): void {
  if (!Array.isArray(edges)) reject();
  const seen = new Set<string>();
  const arrows = new Map<string, string[]>();
  for (const edge of edges) {
    if (!edge || !nonblank(edge.id) || !nonblank(edge.universe_id) ||
        edge.universe_id !== universe ||
        !nonblank(edge.before_anchor_id) || !nonblank(edge.after_anchor_id) ||
        edge.before_anchor_id === edge.after_anchor_id ||
        (edge.origin !== "original" && edge.origin !== "restatement"))
      reject();
    const key = signature(edge);
    if (seen.has(key)) reject();
    seen.add(key);
    const neighbors = arrows.get(edge.before_anchor_id) ?? [];
    neighbors.push(edge.after_anchor_id);
    arrows.set(edge.before_anchor_id, neighbors);
  }
  // A partial order can leave anchors incomparable, but cannot contain cycles.
  const active = new Set<string>();
  const finished = new Set<string>();
  function visit(id: string): void {
    if (active.has(id)) reject();
    if (finished.has(id)) return;
    active.add(id);
    for (const child of arrows.get(id) ?? []) visit(child);
    active.delete(id);
    finished.add(id);
  }
  for (const id of arrows.keys()) visit(id);
}

/** Pure projection: no command, no hidden date inference, no authorization token. */
export function previewP2iFictionalImpact(
  input: P2iFictionalInput,
  expectedUniverse: string,
): P2iFictionalImpact {
  if (!input || input.data_origin !== "fictional_browser_memory_only" ||
      input.production_writer_admitted !== false || input.real_g3_authorized !== false ||
      !nonblank(expectedUniverse) || !nonblank(input.universe_id) ||
      input.universe_id !== expectedUniverse) reject();
  validateGraph(input.active_before, expectedUniverse);
  validateGraph(input.active_after, expectedUniverse);
  const before = new Set(input.active_before.map(signature));
  const after = new Set(input.active_after.map(signature));
  return {
    removed: input.active_before.filter(edge => !after.has(signature(edge))),
    added: input.active_after.filter(edge => !before.has(signature(edge))),
    unchanged: input.active_after.filter(edge => before.has(signature(edge))),
    data_origin: "fictional_browser_memory_only",
    production_writer_admitted: false,
    real_g3_authorized: false,
  };
}

export default function M32P2iFictionalImpactReview({
  input, expectedUniverse,
}: { input: P2iFictionalInput; expectedUniverse: string }): ReactElement {
  let impact: P2iFictionalImpact;
  try {
    impact = previewP2iFictionalImpact(input, expectedUniverse);
  } catch {
    return <section role="alert" aria-label="Aperçu chronologique fictif refusé">
      <h2>Aperçu fictif refusé</h2>
      <p>Univers, ordre partiel ou provenance non valides. Aucune commande exécutée.</p>
    </section>;
  }
  const groups = [
    { label: "Relations retirées", edges: impact.removed },
    { label: "Relations ajoutées", edges: impact.added },
    { label: "Relations inchangées", edges: impact.unchanged },
  ] as const;
  return <section aria-label="Impact fictif d’une correction chronologique">
    <h2>Impact fictif de la correction — avant / après</h2>
    <p>Exercice d’auteur sur données inventées en mémoire uniquement.</p>
    <p>L’ordre du monde est partiel : aucune date ni priorité narrative déduite.</p>
    {groups.map(group => <section key={group.label} aria-label={group.label}>
      <h3>{group.label} ({group.edges.length})</h3>
      {group.edges.length === 0
        ? <p>Aucune.</p>
        : <ul>{group.edges.map((edge, index) => <li key={signature(edge) + index}>
          <code>{edge.id}</code> : {edge.before_anchor_id} avant {edge.after_anchor_id}
          {" — "}{edge.origin === "restatement" ? "reformulation" : "assertion initiale"}
        </li>)}</ul>}
    </section>)}
    <p>Prévisualisation uniquement : aucune écriture, aucune confirmation,
      aucun accès SQLite, aucune commande Tauri, G3 STOP_UNAVAILABLE.</p>
  </section>;
}
