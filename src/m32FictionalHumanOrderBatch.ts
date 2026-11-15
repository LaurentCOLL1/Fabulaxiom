import { compareM32WorldOrder, type M32WorldComparison } from "./M32WorldOrderComparison";
import {
  createFictionalPrecedence, revokeFictionalPrecedence, inspectFictionalDraft, type FictionalDraft,
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
