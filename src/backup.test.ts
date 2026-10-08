import { describe, expect, it } from "vitest";
import { formatBytes, formatCounts, isRestorableSelection, type BackupStatus } from "./backup";

describe("backup UI helpers", () => {
  const status: BackupStatus = {
    active_database_path: "C:/Fabulaxiom/fabulaxiom.sqlite3",
    default_database_path: "C:/Fabulaxiom/fabulaxiom.sqlite3",
    backup_directory: "C:/Fabulaxiom/backups",
    backups: [{ file_name: "a.sqlite3", path: "C:/Fabulaxiom/backups/a.sqlite3", bytes: 4096 }],
  };

  it("allows restoring only a listed application backup", () => {
    expect(isRestorableSelection(status, "a.sqlite3")).toBe(true);
    expect(isRestorableSelection(status, "../a.sqlite3")).toBe(false);
    expect(isRestorableSelection(null, "a.sqlite3")).toBe(false);
  });

  it("renders SQLite content counters without Ollama dependency", () => {
    expect(formatCounts({
      universes: 1, series: 0, novels: 2, chapters: 3,
      scenes: 4, revisions: 5, current_heads: 2,
    })).toContain("5 révisions");
  });

  it("handles valid and invalid file sizes", () => {
    expect(formatBytes(1024 * 1024)).toBe("1.00 Mio");
    expect(formatBytes(-1)).toBe("Taille inconnue");
  });
});
