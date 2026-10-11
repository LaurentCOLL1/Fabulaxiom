import { describe, expect, it } from "vitest";
import { selectM31PreviewRoute } from "./m31PreviewRoute";

describe("M3.1 isolated preview UI gate", () => {
  it("blocks M2 workspaces if the explicitly requested preview IPC is missing", () => {
    expect(selectM31PreviewRoute("unavailable", true)).toBe("blocked");
  });
  it("never mounts normal modules while an explicit preview is pending", () => {
    expect(selectM31PreviewRoute("pending", true)).toBe("waiting");
    expect(selectM31PreviewRoute("available", true)).toBe("preview");
  });
  it("preserves the normal v6 application when no preview was requested", () => {
    expect(selectM31PreviewRoute("unavailable", false)).toBe("normal");
    expect(selectM31PreviewRoute("available", false)).toBe("preview");
  });
});
