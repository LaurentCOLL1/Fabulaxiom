import { compareM32WorldOrder, type M32WorldComparison } from "./M32WorldOrderComparison";
import {
  createFictionalPrecedence, revokeFictionalPrecedence, inspectFictionalDraft, previewFictionalPrecedence, type FictionalDraft,
} from "./m32FictionalManualChronology";

/** Only a local, invented transaction. This is NOT SQLite atomicity or writer admission. */
export type FictionalHumanOrder = Readonly<{
  before_anchor_id: string;
  after_anchor_id: string;
  reason: string;
}>;
export type FictionalHumanOrderBatchPreview = Readonly<{
  baseline: string;
  actions: readonly FictionalHumanOrder[];
  proposed_edge_ids: readonly string[];
  candidate: FictionalDraft;
  preview_only: true;
  can_write: false;
  world_order_inferred: false;
}>;

function refuse(): never {
  throw new Error("Lot M3.2 fictif refusé (aucune écriture)");
}

/** Validate all actions as ONE unit. An invalid late action never returns a partial draft. */
export function previewFictionalHumanOrderBatch(
  baseline: FictionalDraft, actions: readonly FictionalHumanOrder[],
): FictionalHumanOrderBatchPreview {
  inspectFictionalDraft(baseline);
  if (!Array.isArray(actions) || actions.length === 0 || actions.length > 16)
    return refuse();
  let candidate = baseline;
  const rows: FictionalHumanOrder[] = [];
  for (const action of actions) {
    if (!action || typeof action !== "object" ||
        Object.keys(action).sort().join(",") !== "after_anchor_id,before_anchor_id,reason" ||
        typeof action.before_anchor_id !== "string" ||
        typeof action.after_anchor_id !== "string" ||
        typeof action.reason !== "string") return refuse();
    const row = {
      before_anchor_id: action.before_anchor_id,
      after_anchor_id: action.after_anchor_id,
      reason: action.reason,
    };
    const check = previewFictionalPrecedence(candidate, row.before_anchor_id, row.after_anchor_id);
    if (check.verdict !== "allowed") {
      const witness = check.witness_edge_ids.length
        ? " ; témoins du lot fictif : " + check.witness_edge_ids.join(", ") : "";
      throw new Error("Proposition " + (rows.length + 1) + " refusée : " + check.reason +
        witness + " ; aucune modification appliquée.");
    }
    candidate = createFictionalPrecedence(candidate,
      row.before_anchor_id, row.after_anchor_id, row.reason);
    rows.push(row);
  }
  inspectFictionalDraft(candidate);
  if (candidate.audit.length !== baseline.audit.length + rows.length)
    return refuse();
  return {
    baseline: JSON.stringify(baseline),
    actions: rows,
    proposed_edge_ids: candidate.audit.slice(baseline.audit.length).map(x => x.id),
    candidate,
    preview_only: true,
    can_write: false,
    world_order_inferred: false,
  };
}

/** Explicit human confirmation revalidates the FULL current draft and entire batch.
 * A stale, modified or substituted preview MUST fail closed.
 */
export function confirmFictionalHumanOrderBatch(
  baseline: FictionalDraft, actions: readonly FictionalHumanOrder[],
  preview: FictionalHumanOrderBatchPreview, explicitConfirmation: boolean,
): FictionalDraft {
  if (explicitConfirmation !== true || !preview ||
      preview.preview_only !== true || preview.can_write !== false ||
      preview.world_order_inferred !== false) return refuse();
  const checked = previewFictionalHumanOrderBatch(baseline, actions);
  if (preview.baseline !== checked.baseline ||
      JSON.stringify(preview.actions) !== JSON.stringify(checked.actions) ||
      JSON.stringify(preview.proposed_edge_ids) !== JSON.stringify(checked.proposed_edge_ids) ||
      JSON.stringify(preview.candidate) !== JSON.stringify(checked.candidate))
    return refuse();
  return checked.candidate;
}

/** Explicit, reversible correction or revocation of ONE active invented relation.
 * No historical record is deleted and no replacement is inferred automatically.
 */
export type FictionalHumanOrderRepair = Readonly<{
  precedence_id: string;
  revoke_reason: string;
  replacement: FictionalHumanOrder | null;
}>;
export type FictionalHumanOrderRepairPreview = Readonly<{
  baseline: string;
  actions: readonly FictionalHumanOrderRepair[];
  revoked_edge_ids: readonly string[];
  created_edge_ids: readonly string[];
  candidate: FictionalDraft;
  preview_only: true;
  can_write: false;
  world_order_inferred: false;
}>;

/** Entire repair is a pure RAM preview, never a SQLite transaction or real writer. */
export function previewFictionalHumanOrderRepair(
  baseline: FictionalDraft, actions: readonly FictionalHumanOrderRepair[],
): FictionalHumanOrderRepairPreview {
  inspectFictionalDraft(baseline);
  if (!Array.isArray(actions) || actions.length < 1 || actions.length > 16)
    return refuse();
  let candidate = baseline;
  const rows: FictionalHumanOrderRepair[] = [];
  const revoked: string[] = [];
  const created: string[] = [];
  for (const action of actions) {
    if (!action || typeof action !== "object" ||
        Object.keys(action).sort().join(",") !== "precedence_id,replacement,revoke_reason" ||
        typeof action.precedence_id !== "string" ||
        typeof action.revoke_reason !== "string") return refuse();
    const input = action.replacement;
    if (input !== null && (!input || typeof input !== "object" ||
        Object.keys(input).sort().join(",") !== "after_anchor_id,before_anchor_id,reason" ||
        typeof input.before_anchor_id !== "string" ||
        typeof input.after_anchor_id !== "string" ||
        typeof input.reason !== "string")) return refuse();
    const replacement = input === null ? null : {
      before_anchor_id: input.before_anchor_id,
      after_anchor_id: input.after_anchor_id,
      reason: input.reason,
    };
    candidate = revokeFictionalPrecedence(candidate, action.precedence_id, action.revoke_reason);
    revoked.push(action.precedence_id);
    if (replacement !== null) {
      const prior = candidate.audit.length;
      candidate = createFictionalPrecedence(candidate, replacement.before_anchor_id,
        replacement.after_anchor_id, replacement.reason);
      created.push(candidate.audit[prior].id);
    }
    rows.push({ precedence_id: action.precedence_id,
      revoke_reason: action.revoke_reason, replacement });
  }
  inspectFictionalDraft(candidate);
  if (candidate.audit.length !== baseline.audit.length + revoked.length + created.length)
    return refuse();
  return {
    baseline: JSON.stringify(baseline),
    actions: rows,
    revoked_edge_ids: revoked,
    created_edge_ids: created,
    candidate, preview_only: true, can_write: false, world_order_inferred: false,
  };
}

/** Confirmation is separate, explicitly human and rejects stale/tampered proposals. */
export function confirmFictionalHumanOrderRepair(
  baseline: FictionalDraft, actions: readonly FictionalHumanOrderRepair[],
  preview: FictionalHumanOrderRepairPreview, explicitConfirmation: boolean,
): FictionalDraft {
  if (explicitConfirmation !== true || !preview ||
      preview.preview_only !== true || preview.can_write !== false ||
      preview.world_order_inferred !== false) return refuse();
  const checked = previewFictionalHumanOrderRepair(baseline, actions);
  if (preview.baseline !== checked.baseline ||
      JSON.stringify(preview.actions) !== JSON.stringify(checked.actions) ||
      JSON.stringify(preview.revoked_edge_ids) !== JSON.stringify(checked.revoked_edge_ids) ||
      JSON.stringify(preview.created_edge_ids) !== JSON.stringify(checked.created_edge_ids) ||
      JSON.stringify(preview.candidate) !== JSON.stringify(checked.candidate))
    return refuse();
  return checked.candidate;
}

/** Source-only readout of ONE explicitly selected active anchor pair.
 * A changed relation or witness is not a claim about every possible world order.
 * This toy is never linked to an operator source, Tauri IPC, SQLite, or writer.
 */
export type FictionalRepairPairImpact = Readonly<{
  left_anchor_id: string;
  right_anchor_id: string;
  before: M32WorldComparison;
  after: M32WorldComparison;
  relation_changed: boolean;
  witness_changed: boolean;
  preview_only: true;
  can_write: false;
  world_order_inferred: false;
}>;

/** Rebuilds the entire candidate from the checked fictional baseline before comparing
 * precisely the two human-selected active anchors; no implicit global timeline.
 */
export function previewFictionalRepairPairImpact(
  baseline: FictionalDraft, actions: readonly FictionalHumanOrderRepair[],
  leftAnchorId: string, rightAnchorId: string,
): FictionalRepairPairImpact {
  const proposal = previewFictionalHumanOrderRepair(baseline, actions);
  const universe = baseline.snapshot.universe_id;
  const before = compareM32WorldOrder(baseline.snapshot, universe, leftAnchorId, rightAnchorId);
  const after = compareM32WorldOrder(proposal.candidate.snapshot, universe,
    leftAnchorId, rightAnchorId);
  return {
    left_anchor_id: leftAnchorId,
    right_anchor_id: rightAnchorId,
    before, after,
    relation_changed: before.relation !== after.relation,
    witness_changed: JSON.stringify(before.witness) !== JSON.stringify(after.witness),
    preview_only: true, can_write: false, world_order_inferred: false,
  };
}

/** P3af: up to eight individually selected pairs in invented RAM, never an inferred total order. */
export type FictionalRepairSelectedPair = Readonly<{ left_anchor_id: string; right_anchor_id: string }>;
export type FictionalRepairSelectedPairsImpact = Readonly<{
  selected_pairs: readonly FictionalRepairPairImpact[];
  changed_relation_count: number;
  changed_witness_count: number;
  preview_only: true; can_write: false; world_order_inferred: false;
}>;
/** Single checked whole-batch repair; only author-specified active endpoint pairs are compared. */
export function previewFictionalRepairSelectedPairs(
  baseline: FictionalDraft, actions: readonly FictionalHumanOrderRepair[],
  pairs: readonly FictionalRepairSelectedPair[],
): FictionalRepairSelectedPairsImpact {
  if (!Array.isArray(pairs) || pairs.length < 1 || pairs.length > 8) return refuse();
  const seen = new Set<string>();
  for (const pair of pairs) {
    if (!pair || typeof pair !== "object" ||
      Object.keys(pair).sort().join(",") !== "left_anchor_id,right_anchor_id" ||
      typeof pair.left_anchor_id !== "string" || typeof pair.right_anchor_id !== "string") return refuse();
    const forward=JSON.stringify([pair.left_anchor_id,pair.right_anchor_id]);
    const reverse=JSON.stringify([pair.right_anchor_id,pair.left_anchor_id]);
    if (seen.has(forward) || seen.has(reverse)) return refuse();
    seen.add(forward);
  }
  const proposal=previewFictionalHumanOrderRepair(baseline,actions);
  const universe=baseline.snapshot.universe_id;
  const selected=pairs.map(pair=>{
    const before=compareM32WorldOrder(baseline.snapshot,universe,pair.left_anchor_id,pair.right_anchor_id);
    const after=compareM32WorldOrder(proposal.candidate.snapshot,universe,pair.left_anchor_id,pair.right_anchor_id);
    return {
      left_anchor_id:pair.left_anchor_id,right_anchor_id:pair.right_anchor_id,
      before,after,relation_changed:before.relation!==after.relation,
      witness_changed:JSON.stringify(before.witness)!==JSON.stringify(after.witness),
      preview_only:true as const,can_write:false as const,world_order_inferred:false as const,
    };
  });
  return {selected_pairs:selected,
    changed_relation_count:selected.filter(p=>p.relation_changed).length,
    changed_witness_count:selected.filter(p=>p.witness_changed).length,
    preview_only:true,can_write:false,world_order_inferred:false};
}

/** P3ah — preview effects of new author-declared relations, NOT only revocations.
 * Never select pairs automatically or infer complete world/narration/reveal order.
 * Exactly one checked synthetic draft is used for all comparisons.
 */
export function previewFictionalCreatedBatchSelectedPairs(
  baseline: FictionalDraft,
  actions: readonly FictionalHumanOrder[],
  pairs: readonly FictionalRepairSelectedPair[],
): FictionalRepairSelectedPairsImpact {
  if (!Array.isArray(pairs) || pairs.length < 1 || pairs.length > 8) return refuse();
  const seen=new Set<string>();
  for (const pair of pairs) {
    if (!pair || typeof pair !== "object" ||
        Object.keys(pair).sort().join(",") !== "left_anchor_id,right_anchor_id" ||
        typeof pair.left_anchor_id !== "string" ||
        typeof pair.right_anchor_id !== "string") return refuse();
    const direct=JSON.stringify([pair.left_anchor_id,pair.right_anchor_id]);
    const reverse=JSON.stringify([pair.right_anchor_id,pair.left_anchor_id]);
    if (seen.has(direct) || seen.has(reverse)) return refuse();
    seen.add(direct);
  }
  const proposal=previewFictionalHumanOrderBatch(baseline,actions);
  const universe=baseline.snapshot.universe_id;
  const compared=pairs.map(pair=>{
    const before=compareM32WorldOrder(baseline.snapshot,universe,
      pair.left_anchor_id,pair.right_anchor_id);
    const after=compareM32WorldOrder(proposal.candidate.snapshot,universe,
      pair.left_anchor_id,pair.right_anchor_id);
    return {
      left_anchor_id:pair.left_anchor_id,
      right_anchor_id:pair.right_anchor_id,
      before,after,
      relation_changed:before.relation!==after.relation,
      witness_changed:JSON.stringify(before.witness)!==JSON.stringify(after.witness),
      preview_only:true as const,can_write:false as const,world_order_inferred:false as const,
    };
  });
  return {
    selected_pairs:compared,
    changed_relation_count:compared.filter(p=>p.relation_changed).length,
    changed_witness_count:compared.filter(p=>p.witness_changed).length,
    preview_only:true,can_write:false,world_order_inferred:false,
  };
}
