export type SceneTextRevision = {
  id: string;
  scene_id: string;
  revision_number: number;
  content: string;
  created_at_utc: string;
  parent_revision_id: string | null;
};

export type SceneRevisionHistory = {
  scene_id: string;
  current_revision_id: string | null;
  revisions: SceneTextRevision[];
};

export function currentSceneRevision(
  history: SceneRevisionHistory,
): SceneTextRevision | null {
  if (!history.current_revision_id) {
    return null;
  }

  return (
    history.revisions.find(
      (revision) => revision.id === history.current_revision_id,
    ) ?? null
  );
}

export function revisionSummary(revision: SceneTextRevision): string {
  const parent = revision.parent_revision_id
    ? " · parent " + revision.parent_revision_id
    : " · origine";

  return (
    "v" +
    revision.revision_number +
    " · " +
    revision.created_at_utc +
    parent
  );
}
