import type { ReactElement } from "react";

/**
 * Fictitious, read-only browser audit of an explicitly authored successor chain.
 * Never imported by App.tsx, never connected to Tauri, SQLite, disk or network.
 * Nothing returned here establishes custody, authority or actual user history.
 */
export type M32FictionalCorrectionRow = Readonly<{
  id: string;
  universe_id: string;
  kind: "successor" | "chain";
  prior_successor_id: string | null;
  prior_chain_id: string | null;
  before_anchor_id: string;
  after_anchor_id: string;
  reason: string;
  revocation_id: string | null;
  revocation_reason: string | null;
}>;
export type M32FictionalChainAudit = Readonly<{
  ordered_history: readonly M32FictionalCorrectionRow[];
  active_id: string | null;
  data_origin: "fictional_browser_memory_only";
  editing_authorized: false;
  real_g3_authorized: false;
}>;
function nonblank(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}
function refuse(reason: string): never {
  throw new Error("Historique fictif refusé : " + reason);
}

/** A single immutable lineage, not a global chronological or narration order. */
export function auditM32FictionalCorrectionChain(
  expectedUniverseId: string,
  input: readonly M32FictionalCorrectionRow[],
): M32FictionalChainAudit {
  if (!nonblank(expectedUniverseId) || !Array.isArray(input)) {
    return refuse("univers explicite ou historique invalide");
  }
  if (input.length === 0) return {
    ordered_history: [], active_id: null,
    data_origin: "fictional_browser_memory_only",
    editing_authorized: false, real_g3_authorized: false,
  };
  const byId = new Map<string, M32FictionalCorrectionRow>();
  const revocations = new Set<string>();
  for (const record of input) {
    if (!record || !nonblank(record.id) ||
        !nonblank(record.universe_id) || record.universe_id !== expectedUniverseId ||
        !nonblank(record.before_anchor_id) || !nonblank(record.after_anchor_id) ||
        record.before_anchor_id === record.after_anchor_id ||
        !nonblank(record.reason) ||
        (record.kind !== "successor" && record.kind !== "chain") ||
        byId.has(record.id)) {
      return refuse("identifiant, univers, assertion ou motif invalide");
    }
    const revoked = record.revocation_id !== null;
    if (revoked !== (record.revocation_reason !== null) ||
        (revoked && (!nonblank(record.revocation_id) ||
          !nonblank(record.revocation_reason) ||
          revocations.has(record.revocation_id!)))) {
      return refuse("révocation manquante, incohérente ou dupliquée");
    }
    if (revoked) revocations.add(record.revocation_id!);
    if (record.kind === "successor" &&
        (record.prior_chain_id !== null || record.prior_successor_id !== null)) {
      return refuse("successeur fictif avec parent de chaîne illégal");
    }
    if (record.kind === "chain" &&
        ((record.prior_chain_id === null) === (record.prior_successor_id === null))) {
      return refuse("une seule ascendance explicite est obligatoire");
    }
    byId.set(record.id, record);
  }
  const roots = input.filter(r => r.kind === "successor");
  if (roots.length !== 1) return refuse("une seule racine fictive est attendue");
  const next = new Map<string, string>();
  for (const row of input.filter(r => r.kind === "chain")) {
    const parentId = row.prior_successor_id ?? row.prior_chain_id;
    if (!nonblank(parentId)) return refuse("parent de chaîne manquant");
    const parent = byId.get(parentId);
    const requiredKind = row.prior_successor_id !== null ? "successor" : "chain";
    if (!parent || parent.kind !== requiredKind || parent.revocation_id === null) {
      return refuse("parent absent, du mauvais type ou non révoqué");
    }
    if (next.has(parentId)) return refuse("bifurcation de correction non autorisée");
    next.set(parentId, row.id);
  }
  const ordered: M32FictionalCorrectionRow[] = [];
  const visited = new Set<string>();
  let current: string | undefined = roots[0].id;
  while (current) {
    if (visited.has(current)) return refuse("cycle de corrections fictives");
    visited.add(current);
    const row = byId.get(current)!;
    if (next.has(current) && row.revocation_id === null) {
      return refuse("successeur créé avant révocation du parent");
    }
    ordered.push(row);
    current = next.get(current);
  }
  if (ordered.length !== input.length) return refuse("branche orpheline ou cycle");
  const last = ordered[ordered.length - 1];
  return {
    ordered_history: ordered,
    active_id: last.revocation_id === null ? last.id : null,
    data_origin: "fictional_browser_memory_only",
    editing_authorized: false, real_g3_authorized: false,
  };
}

export default function M32FictionalCorrectionHistory({
  expectedUniverseId, records,
}: { expectedUniverseId: string; records: readonly M32FictionalCorrectionRow[] }): ReactElement {
  let history: M32FictionalChainAudit;
  try {
    history = auditM32FictionalCorrectionChain(expectedUniverseId, records);
  } catch {
    return <section role="alert" aria-label="Historique fictif rejeté">
      <h2>Historique de corrections refusé</h2>
      <p>Ascendance ou univers incohérent. Aucune source opérateur consultée.</p>
    </section>;
  }
  return <section aria-label="Historique fictif des corrections chronologiques">
    <h2>Historique fictif des corrections chronologiques</h2>
    <p>Données inventées en mémoire uniquement. Aucun accès SQLite ni commande Tauri.</p>
    <p>Chaque correction exige le retrait explicite de sa devancière.
      Cet historique ne définit pas un ordre chronologique total.</p>
    {history.ordered_history.length === 0
      ? <p>Aucune correction fictive dans cet univers.</p>
      : <ol aria-label="Corrections explicitement conservées">
        {history.ordered_history.map((row, index) => <li key={row.id}>
          <strong>{row.id}</strong> — {row.before_anchor_id} avant {row.after_anchor_id}
          {" — "}{row.reason} — {row.revocation_id === null
            ? "correction active"
            : "correction retirée : " + row.revocation_reason}
          {index > 0 && <p>
            Corrige explicitement <code>{history.ordered_history[index - 1].id}</code> :
            ancienne assertion <code>{history.ordered_history[index - 1].before_anchor_id}</code>
            {" avant "}<code>{history.ordered_history[index - 1].after_anchor_id}</code>.
            Aucun ordre global déduit.
          </p>}
        </li>)}
      </ol>}
    <p>Correction active : {history.active_id ?? "aucune"}. Aucune écriture autorisée.</p>
  </section>;
}
