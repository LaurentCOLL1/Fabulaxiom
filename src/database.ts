export type DatabaseStatus = {
  available: boolean;
  path: string | null;
  schema_version: number | null;
  foreign_keys: boolean;
  error: string | null;
};

export function formatDatabaseSummary(status: DatabaseStatus): string {
  if (
    status.available &&
    status.path &&
    status.schema_version !== null &&
    status.foreign_keys
  ) {
    return `SQLite schema v${status.schema_version} · clés étrangères ON · ${status.path}`;
  }

  return status.error
    ? `Base locale indisponible : ${status.error}`
    : "Base locale indisponible.";
}
