import { describe, expect, it } from "vitest";
import {
  formatHierarchyError,
  newHierarchyId,
  optionalId,
} from "./hierarchy";

describe("hierarchy helpers", () => {
  it("formats a structured Tauri service error", () => {
    expect(
      formatHierarchyError({
        code: "has_children",
        message: "Suppression refusée.",
      }),
    ).toBe("[has_children] Suppression refusée.");
  });

  it("formats a serialized Tauri service error", () => {
    expect(
      formatHierarchyError(
        JSON.stringify({
          code: "cross_universe_series",
          message: "Série incompatible.",
        }),
      ),
    ).toBe("[cross_universe_series] Série incompatible.");
  });

  it("normalizes an optional series id", () => {
    expect(optionalId("  series-1  ")).toBe("series-1");
    expect(optionalId("   ")).toBeNull();
  });

  it("creates prefixed stable ids with the platform UUID primitive", () => {
    const id = newHierarchyId("novel");
    expect(id.startsWith("novel-")).toBe(true);
    expect(id.length).toBeGreaterThan("novel-".length);
  });
});
