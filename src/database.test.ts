import { describe, expect, it } from "vitest";
import {
  formatDatabaseSummary,
  type DatabaseStatus,
} from "./database";

describe("formatDatabaseSummary", () => {
  it("formats a qualified local database", () => {
    const status: DatabaseStatus = {
      available: true,
      path: "C:\\Users\\test\\AppData\\Local\\com.fabulaxiom.desktop\\database\\fabulaxiom.sqlite3",
      schema_version: 1,
      foreign_keys: true,
      error: null,
    };

    expect(formatDatabaseSummary(status)).toContain(
      "SQLite schema v1 · clés étrangères ON",
    );
    expect(formatDatabaseSummary(status)).toContain("fabulaxiom.sqlite3");
  });

  it("keeps a database diagnostic error", () => {
    const status: DatabaseStatus = {
      available: false,
      path: null,
      schema_version: null,
      foreign_keys: false,
      error: "chemin indisponible",
    };

    expect(formatDatabaseSummary(status)).toBe(
      "Base locale indisponible : chemin indisponible",
    );
  });
});
