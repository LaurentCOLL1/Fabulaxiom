import { compareM32WorldOrder, type M32WorldRelation } from "./M32WorldOrderComparison";
import { startFictionalDraft, type FictionalDraft } from "./m32FictionalManualChronology";

/** A purely hypothetical projection. Never calls a writer or changes a draft. */
export type FictionalRevocationImpact = Readonly<{
  verdict: "unselected" | "blocked" | "allowed";
  reason: string;
  existing_edge_id: string | null;
  relation_after: M32WorldRelation | null;
  witness_after: readonly string[];
  data_origin: "fictional_browser_memory_only";
  writes: false;
}>;

/** Only tests removal of one explicitly authored current human edge.
 * A second path can continue to prove before/after; there is no inferred date,
 * global time axis or automatic revocation. This is not an audit signature.
 */
export function previewFictionalRevocationImpact(
  draft: FictionalDraft, edgeId: string,
): FictionalRevocationImpact {
  if (draft?.data_origin !== "fictional_browser_memory_only" ||
      draft.real_g3_authorized !== false) {
    throw new Error("Prévisualisation fictive refusée : origine non reconnue");
  }
  // The decoder in startFictionalDraft rejects mixed Universes and invalid graphs.
  // This also creates a detached snapshot, so the input cannot be mutated.
  const safe = startFictionalDraft(draft.snapshot, draft.revisions);
  const base = {
    data_origin: "fictional_browser_memory_only" as const,
    writes: false as const,
  };
  if (edgeId === "") return {
    ...base, verdict: "unselected" as const,
    existing_edge_id: null, relation_after: null, witness_after: [],
    reason: "Choisir une relation humaine active pour vérifier une révocation éventuelle.",
  };
  const edge = safe.snapshot.precedences.find(e => e.id === edgeId && e.status === "current");
  if (!edge) return {
    ...base, verdict: "blocked" as const, existing_edge_id: null,
    relation_after: null, witness_after: [],
    reason: "Relation étrangère, absente ou historique : aucune simulation.",
  };
  const imaginary = {
    ...safe.snapshot,
    precedences: safe.snapshot.precedences.map(e =>
      e.id === edgeId ? { ...e, status: "revoked" as const } : e),
  };
  const after = compareM32WorldOrder(imaginary, imaginary.universe_id,
    edge.before_anchor_id, edge.after_anchor_id);
  return {
    ...base, verdict: "allowed", existing_edge_id: edge.id,
    relation_after: after.relation,
    witness_after: after.witness.map(e => e.precedence_id),
    reason: after.relation === "incomparable"
      ? "Simulation seulement : sans ce lien, ordre indéterminé entre ces deux ancres."
      : "Simulation seulement : un autre chemin humain actif justifie encore cet ordre.",
  };
}
