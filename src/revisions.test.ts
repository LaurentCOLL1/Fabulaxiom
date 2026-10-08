import { describe, expect, it } from "vitest";
import {
  currentSceneRevision,
  revisionSummary,
  type SceneRevisionHistory,
} from "./revisions";

describe("revision helpers", () => {
  const history: SceneRevisionHistory = {
    scene_id: "scene-1",
    current_revision_id: "revision-1",
    revisions: [
      {
        id: "revision-2",
        scene_id: "scene-1",
        revision_number: 2,
        content: "Second",
        created_at_utc: "2026-10-07 21:00:01",
        parent_revision_id: "revision-1",
      },
      {
        id: "revision-1",
        scene_id: "scene-1",
        revision_number: 1,
        content: "First",
        created_at_utc: "2026-10-07 21:00:00",
        parent_revision_id: null,
      },
    ],
  };

  it("resolves the explicit current revision rather than the newest one", () => {
    expect(currentSceneRevision(history)?.id).toBe("revision-1");
    expect(currentSceneRevision(history)?.content).toBe("First");
  });

  it("formats revision lineage", () => {
    expect(revisionSummary(history.revisions[0])).toContain("v2");
    expect(revisionSummary(history.revisions[0])).toContain(
      "parent revision-1",
    );
    expect(revisionSummary(history.revisions[1])).toContain("origine");
  });
});
