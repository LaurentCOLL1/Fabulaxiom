import { inspectFictionalDraft, supersedeFictionalAnchor,
 type FictionalDraft, type FictionalTimeInput, type FictionalRevision } from "./m32FictionalManualChronology";
import type { M32AnchorProjection } from "./M32ChronologyPreview";

/** P3aj — human-reviewed correction of an invented RAM anchor.
 * No SQLite, Tauri writer, saved state, calendar conversion or implicit old edge revocation.
 */
export type FictionalAnchorSupersessionReview = Readonly<{
  baseline: string;
  old_anchor: M32AnchorProjection;
  new_anchor: M32AnchorProjection;
  /** Exact, explicitly recorded fictional revision identity; never inferred from a title. */
  old_source: FictionalRevision | null;
  new_source: FictionalRevision | null;
  candidate: FictionalDraft;
  preview_only: true;
  can_write: false;
  total_world_order_inferred: false;
}>;

function stop(): never {
  throw new Error("Prévisualisation fictive refusée : aucune sauvegarde.");
}

/** Bind a source to an exact invented revision and its owning scene/novel.
 * Missing/foreign identity fails closed; source-free anchors remain source-free.
 */
function sourceIdentity(d:FictionalDraft,a:M32AnchorProjection):FictionalRevision|null {
  if(a.source_revision_id===null) return null;
  const rev=d.revisions.find(r=>r.revision_id===a.source_revision_id);
  if(!rev || rev.universe_id!==d.snapshot.universe_id ||
      !d.snapshot.narration.some(n=>n.universe_id===rev.universe_id &&
        n.novel_id===rev.novel_id && n.scene_id===rev.scene_id)) return stop();
  return {...rev};
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
    old_source:sourceIdentity(baseline,old),
    new_source:sourceIdentity(candidate,added[0]),
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
