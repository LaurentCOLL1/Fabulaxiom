/**
 * P3a: typed COMMAND CONTRACT REHEARSAL only, mirroring the fixture-only Rust
 * P2b vocabulary without invoking Rust, Tauri, the network or disk.
 * This pure reducer operates ONLY on synthetic React memory drafts.
 * It is NOT an IPC adapter, production admission or SQLite persistence.
 */
import {
  createFictionalAnchor, createFictionalPrecedence, inspectFictionalDraft,
  startFictionalDraft,
  type FictionalDraft, type FictionalRevision, type FictionalTimeInput,
} from "./m32FictionalManualChronology";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";

export const P3_NEW_ANCHOR = "$new" as const;
export type P3Relation = Readonly<{
  before_anchor_id: string;
  after_anchor_id: string;
  reason: string;
}>;
export type P3Command =
  | Readonly<{
      kind: "create_anchor_with_optional_relation";
      universe_id: string;
      time: FictionalTimeInput;
      relation: P3Relation | null;
    }>
  | Readonly<{
      kind: "create_precedence";
      universe_id: string;
      relation: P3Relation;
    }>;
export type P3State = Readonly<{
  draft: FictionalDraft;
  data_origin: "fictional_browser_memory_only";
  real_g3_authorized: false;
  commands_committed: number;
}>;
function refuse(message: string): never {
  throw new Error("P3 fictif : " + message);
}
function verified(state: P3State, universe: string): FictionalDraft {
  if (state?.data_origin !== "fictional_browser_memory_only" ||
      state.real_g3_authorized !== false ||
      !Number.isSafeInteger(state.commands_committed) ||
      state.commands_committed < 0 || state.commands_committed > 4096)
    return refuse("origine ou autorisation invalide");
  const draft = inspectFictionalDraft(state.draft);
  if (draft.snapshot.universe_id !== universe || !universe.startsWith("fiction-"))
    return refuse("Univers étranger ou réel");
  return draft;
}
export function startP3FictionalState(
  snapshot: M32ChronologyProjection, revisions: readonly FictionalRevision[] = [],
): P3State {
  const draft = startFictionalDraft(snapshot, revisions);
  return { draft, data_origin: "fictional_browser_memory_only",
    real_g3_authorized: false, commands_committed: 0 };
}
export function readP3FictionalSnapshot(
  state: P3State, universe_id: string,
): M32ChronologyProjection {
  return verified(state, universe_id).snapshot;
}
function checkRelation(relation: P3Relation): void {
  if (!relation || typeof relation.before_anchor_id !== "string" ||
      typeof relation.after_anchor_id !== "string" ||
      typeof relation.reason !== "string" ||
      relation.reason.trim() === "" || relation.reason.length > 160)
    refuse("raison et identifiants explicites obligatoires");
}
/** One immutable transaction-like transition: if an edge fails, the new
 * anchor exists only in a discarded intermediate JS object.
 */
export function applyP3FictionalCommand(state: P3State, command: P3Command): P3State {
  if (!command || typeof command.universe_id !== "string")
    return refuse("commande invalide");
  const prior = verified(state, command.universe_id);
  let draft: FictionalDraft;
  switch (command.kind) {
    case "create_anchor_with_optional_relation": {
      draft = createFictionalAnchor(prior, command.time);
      if (command.relation !== null) {
        checkRelation(command.relation);
        const created = draft.snapshot.anchors[draft.snapshot.anchors.length - 1];
        const resolve = (id: string) => id === P3_NEW_ANCHOR ? created.id : id;
        const before = resolve(command.relation.before_anchor_id);
        const after = resolve(command.relation.after_anchor_id);
        if (before === after ||
            (command.relation.before_anchor_id !== P3_NEW_ANCHOR &&
             command.relation.after_anchor_id !== P3_NEW_ANCHOR))
          return refuse("la relation doit contenir exactement la nouvelle ancre");
        draft = createFictionalPrecedence(draft, before, after, command.relation.reason);
      }
      break;
    }
    case "create_precedence":
      checkRelation(command.relation);
      if ([command.relation.before_anchor_id, command.relation.after_anchor_id].includes(P3_NEW_ANCHOR))
        return refuse("marqueur de nouvelle ancre interdit sans création");
      draft = createFictionalPrecedence(prior,
        command.relation.before_anchor_id, command.relation.after_anchor_id,
        command.relation.reason);
      break;
    default:
      return refuse("commande inconnue");
  }
  return { ...state, draft, commands_committed: state.commands_committed + 1 };
}
