import {
  createFictionalPrecedence, inspectFictionalDraft, type FictionalDraft,
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
