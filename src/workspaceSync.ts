/** Sibling workspaces receive a local notification only after successful Rust IPC writes. */
export const WORKSPACE_HIERARCHY_CHANGED = "fabulaxiom:hierarchy-changed";
export const WORKSPACE_ENTITY_CHANGED = "fabulaxiom:entity-changed";
export const WORKSPACE_REVISION_CHANGED = "fabulaxiom:revision-changed";

export type WorkspaceChange =
  | typeof WORKSPACE_HIERARCHY_CHANGED
  | typeof WORKSPACE_ENTITY_CHANGED
  | typeof WORKSPACE_REVISION_CHANGED;

/** Observable only in the current Tauri window; never writes to SQLite. */
export function announceWorkspaceChange(event: WorkspaceChange, target: EventTarget = window): void {
  target.dispatchEvent(new Event(event));
}

export function preferredUniverseId(
  ids: ReadonlyArray<{id:string}>,
  currentlySelected: string,
): string {
  return ids.some(item => item.id === currentlySelected)
    ? currentlySelected
    : (ids[0]?.id ?? "");
}
