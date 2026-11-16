import { inspectFictionalDraft, supersedeFictionalAnchor,
 type FictionalDraft, type FictionalTimeInput } from "./m32FictionalManualChronology";
import type { M32AnchorProjection } from "./M32ChronologyPreview";

/** P3aj — human-reviewed correction of an invented RAM anchor.
 * No SQLite, Tauri writer, saved state, calendar conversion or implicit old edge revocation.
 */
export type FictionalAnchorSupersessionReview = Readonly<{
  baseline: string;
  old_anchor: M32AnchorProjection;
  new_anchor: M32AnchorProjection;
  candidate: FictionalDraft;
  preview_only: true;
  can_write: false;
  total_world_order_inferred: false;
}>;

function stop(): never {
  throw new Error("Prévisualisation fictive refusée : aucune sauvegarde.");
}

export function previewFictionalAnchorSupersession(
  baseline: FictionalDraft, oldId: string, input: FictionalTimeInput,
): FictionalAnchorSupersessionReview {
  inspectFictionalDraft(baseline);
  const old = baseline.snapshot.anchors.find(a => a.id === oldId && a.status === "current");
  if (!old) return stop();
  const candidate = supersedeFictionalAnchor(baseline,oldId,input);
  const added = candidate.snapshot.anchors.slice(baseline.snapshot.anchors.length);
  const historical = candidate.snapshot.anchors.find(a => a.id === oldId);
  if (added.length !== 1 || !historical || historical.status !== "superseded" ||
    added[0].status !== "current" || added[0].universe_id !== baseline.snapshot.universe_id ||
    candidate.audit.length !== baseline.audit.length+1) return stop();
  if (input.source_revision_id === undefined &&
    old.source_revision_id !== added[0].source_revision_id) return stop();
  return {
    baseline:JSON.stringify(baseline),
    old_anchor:{...old},
    new_anchor:{...added[0]},
    candidate,
    preview_only:true,
    can_write:false,
    total_world_order_inferred:false,
  };
}

/** Rebuild the full candidate on the current RAM baseline, fail closed on stale
 * preview / forged fields / absent explicit author confirmation. */
export function confirmFictionalAnchorSupersession(
  baseline:FictionalDraft,oldId:string,input:FictionalTimeInput,
  preview:FictionalAnchorSupersessionReview,explicit:boolean,
):FictionalDraft {
  if (explicit !== true || !preview || preview.preview_only !== true ||
    preview.can_write !== false || preview.total_world_order_inferred !== false)
    return stop();
  const checked=previewFictionalAnchorSupersession(baseline,oldId,input);
  if (JSON.stringify(preview)!==JSON.stringify(checked)) return stop();
  return checked.candidate;
}
