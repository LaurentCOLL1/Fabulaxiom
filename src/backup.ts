export type DataCounts = {
  universes: number;
  series: number;
  novels: number;
  chapters: number;
  scenes: number;
  revisions: number;
  current_heads: number;
  entities: number;
  aliases: number;
  facts: number;
  fact_sources: number;
  review_events: number;
};

export type BackupEntry = {
  file_name: string;
  path: string;
  bytes: number;
};

export type BackupStatus = {
  active_database_path: string;
  default_database_path: string;
  backup_directory: string;
  backups: BackupEntry[];
};

export type BackupResult = {
  backup: BackupEntry;
  schema_version: number;
  counts: DataCounts;
};

export type RestoreResult = {
  previous_database_path: string;
  active_database_path: string;
  source_backup: string;
  schema_version: number;
  counts: DataCounts;
};

export function formatCounts(counts: DataCounts): string {
  return (
    counts.universes +
    " univers · " +
    counts.novels +
    " romans · " +
    counts.scenes +
    " scènes · " +
    counts.revisions +
    " révisions · " +
    counts.current_heads +
    " pointeurs courants · " +
    counts.entities +
    " entités · " +
    counts.aliases +
    " alias · " +
    counts.facts + " faits · " +
    counts.fact_sources + " citations · " +
    counts.review_events + " revues"
  );
}

export function formatBytes(bytes: number): string {
  if (!Number.isFinite(bytes) || bytes < 0) {
    return "Taille inconnue";
  }
  if (bytes < 1024) return bytes + " o";
  return (bytes / 1024 / 1024).toFixed(2) + " Mio";
}

export function isRestorableSelection(status: BackupStatus | null, fileName: string): boolean {
  return status !== null && status.backups.some((entry) => entry.file_name === fileName);
}
