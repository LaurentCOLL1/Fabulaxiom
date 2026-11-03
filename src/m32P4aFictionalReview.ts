/**
 * P4a FICTION-ONLY two-phase review rehearsal.
 * This does not admit P4, invoke Tauri/Rust, grant G3, open SQLite or persist.
 * String snapshots are stale-proposal guards in a single browser-memory session,
 * NOT cryptographic integrity proofs or security authorization.
 */
import {
  applyP3FictionalCommand, readP3FictionalSnapshot,
  type P3Command, type P3State,
} from "./m32P3FictionalCommandContract";

export type P4aFictionalChangeSummary = Readonly<{
  created_anchor_ids: readonly string[];
  superseded_anchor_ids: readonly string[];
  created_precedence_ids: readonly string[];
  revoked_precedence_ids: readonly string[];
  historical_source_revision_ids: readonly string[];
  narration_unchanged: true;
  reader_reveal_unchanged: true;
}>;

export type P4aFictionalPlan = Readonly<{
  data_origin: "fictional_browser_memory_only";
  real_g3_authorized: false;
  production_writer_admitted: false;
  before_json: string;
  after_json: string;
  command: P3Command;
  changes: P4aFictionalChangeSummary;
}>;

function deny(message: string): never {
  throw new Error("P4a fictif : " + message);
}
function validateSnapshot(state: P3State, universe_id: string): void {
  readP3FictionalSnapshot(state, universe_id);
  if (state.real_g3_authorized !== false ||
      state.data_origin !== "fictional_browser_memory_only") deny("origine réelle interdite");
}
/** Stage a PREVIEW only. The caller's state and revision history are unchanged. */
export function stageP4aFictionalPlan(state: P3State, command: P3Command): P4aFictionalPlan {
  if (!command || typeof command.universe_id !== "string") deny("commande invalide");
  validateSnapshot(state, command.universe_id);
  const before_json = JSON.stringify(state);
  // A detached plain-data command prevents subsequent form changes changing the plan.
  const stagedCommand = JSON.parse(JSON.stringify(command)) as P3Command;
  const after = applyP3FictionalCommand(state, stagedCommand);
  const old = state.draft.snapshot;
  const now = after.draft.snapshot;
  if (JSON.stringify(now.narration) !== JSON.stringify(old.narration) ||
      now.reader_reveal_status !== old.reader_reveal_status)
    deny("la narration ou la révélation ne doivent pas changer");
  const oldAnchors = new Map(old.anchors.map(a => [a.id, a]));
  const oldEdges = new Map(old.precedences.map(e => [e.id, e]));
  return {
    data_origin: "fictional_browser_memory_only",
    real_g3_authorized: false,
    production_writer_admitted: false,
    before_json,
    after_json: JSON.stringify(after),
    command: stagedCommand,
    changes: {
      created_anchor_ids: now.anchors.filter(a => !oldAnchors.has(a.id)).map(a => a.id),
      superseded_anchor_ids: now.anchors.filter(a =>
        a.status === "superseded" && oldAnchors.get(a.id)?.status === "current").map(a => a.id),
      created_precedence_ids: now.precedences.filter(e => !oldEdges.has(e.id)).map(e => e.id),
      revoked_precedence_ids: now.precedences.filter(e =>
        e.status === "revoked" && oldEdges.get(e.id)?.status === "current").map(e => e.id),
      historical_source_revision_ids: [...new Set(now.anchors.map(a =>
        a.source_revision_id).filter((v): v is string => v !== null))].sort(),
      narration_unchanged: true,
      reader_reveal_unchanged: true,
    },
  };
}
/** Human confirmation changes ONLY the returned fictional in-memory state. */
export function confirmP4aFictionalPlan(
  current: P3State, staged: P4aFictionalPlan, human_reason: string,
): P3State {
  if (typeof human_reason !== "string" || !human_reason.trim() ||
      human_reason.length > 160) deny("confirmation humaine motivée obligatoire (160 caractères max)");
  if (!staged || staged.data_origin !== "fictional_browser_memory_only" ||
      staged.real_g3_authorized !== false || staged.production_writer_admitted !== false ||
      typeof staged.before_json !== "string" || typeof staged.after_json !== "string" ||
      !staged.command || typeof staged.command.universe_id !== "string")
    deny("dossier de proposition invalide");
  validateSnapshot(current, staged.command.universe_id);
  if (JSON.stringify(current) !== staged.before_json)
    deny("proposition périmée : refaire la prévisualisation");
  // Recompute rather than trust displayed or caller-supplied after_json.
  const recalculated = stageP4aFictionalPlan(current, staged.command);
  if (recalculated.after_json !== staged.after_json ||
      JSON.stringify(recalculated.changes) !== JSON.stringify(staged.changes))
    deny("prévisualisation modifiée : refus");
  return applyP3FictionalCommand(current, staged.command);
}
