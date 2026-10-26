import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { formatHierarchyError } from "./hierarchy";
import {
  formatBytes,
  formatCounts,
  isRestorableSelection,
  type BackupResult,
  type BackupStatus,
  type RestoreResult,
} from "./backup";

export default function BackupWorkspace() {
  const [status, setStatus] = useState<BackupStatus | null>(null);
  const [selectedBackup, setSelectedBackup] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function refresh(): Promise<void> {
    const updated = await invoke<BackupStatus>("backup_status");
    setStatus(updated);
    setSelectedBackup((previous) =>
      updated.backups.some((entry) => entry.file_name === previous)
        ? previous
        : (updated.backups[0]?.file_name ?? ""),
    );
  }

  useEffect(() => {
    void (async () => {
      setBusy(true);
      try {
        await refresh();
      } catch (reason) {
        setError(formatHierarchyError(reason));
      } finally {
        setBusy(false);
      }
    })();
  }, []);

  async function createBackup() {
    setBusy(true);
    setMessage(null);
    setError(null);
    try {
      const result = await invoke<BackupResult>("create_database_backup");
      await refresh();
      setSelectedBackup(result.backup.file_name);
      setMessage(
        "Sauvegarde validée (schéma v" +
        result.schema_version +
        ") : " + result.backup.path +
        " · " + formatCounts(result.counts),
      );
    } catch (reason) {
      setError(formatHierarchyError(reason));
    } finally {
      setBusy(false);
    }
  }

  async function restoreBackup() {
    if (!isRestorableSelection(status, selectedBackup)) return;
    const selected = status!.backups.find((entry) => entry.file_name === selectedBackup);
    if (!selected) return;

    const confirmed = window.confirm(
      "Restaurer la sauvegarde " + selected.file_name + " ?\n\n" +
      "Le profil de l'application restera le même. " +
      "Un NOUVEAU fichier SQLite sera créé et activé dans ce profil. " +
      "La base actuelle et les anciens fichiers de sauvegarde seront conservés. " +
      "Les changements réalisés depuis cette sauvegarde resteront dans l'ancien fichier, " +
      "mais ne seront pas affichés dans la base restaurée.",
    );
    if (!confirmed) return;

    const phrase = window.prompt(
      "Confirmez l'activation en saisissant exactement RESTAURER :",
      "",
    );
    if (phrase !== "RESTAURER") return;

    setBusy(true);
    setError(null);
    setMessage(null);
    try {
      const result = await invoke<RestoreResult>("restore_database_backup", {
        input: { file_name: selectedBackup, confirmation: phrase },
      });
      setMessage(
        "Restauration vérifiée : " + result.active_database_path +
        " · " + formatCounts(result.counts),
      );
      // Reload every hierarchy/revision reader onto the new, persistently active database.
      window.location.reload();
    } catch (reason) {
      setError(formatHierarchyError(reason));
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="backup-workspace" aria-labelledby="backup-title">
      <div className="workspace-heading">
        <div>
          <p className="card-kicker">M1.5 · Sauvegarde et restauration locale</p>
          <h2 id="backup-title">Protection de la base Fabulaxiom</h2>
          <p>
            Les sauvegardes sont des instantanés SQLite vérifiés. Une restauration
            conserve le même profil, crée un nouveau fichier et change la base active
            seulement après validation, sans écraser la précédente.
          </p>
        </div>
        <button className="secondary" type="button" disabled={busy}
          onClick={() => void refresh().catch((reason) => setError(formatHierarchyError(reason)))}>
          Actualiser
        </button>
      </div>

      {error && <div className="result failure" role="alert">
        <strong>OPÉRATION REFUSÉE</strong><span>{error}</span>
      </div>}
      {message && <div className="result success" role="status">
        <strong>PASS</strong><span>{message}</span>
      </div>}

      <div className="backup-grid">
        <div className="backup-pane">
          <h3>Créer une sauvegarde</h3>
          <p>La base active reste utilisable. Le fichier de sortie reçoit un nouveau nom et
            ses données sont contrôlées avant d'être proposé à la restauration.</p>
          <button type="button" disabled={busy} onClick={() => void createBackup()}>
            {busy ? "Opération en cours…" : "Créer une sauvegarde vérifiée"}
          </button>
          <p className="context-line">Base active : <code>{status?.active_database_path ?? "Chargement…"}</code></p>
          <p className="context-line">Dossier : <code>{status?.backup_directory ?? "Chargement…"}</code></p>
        </div>
        <div className="backup-pane">
          <h3>Restaurer une sauvegarde</h3>
          <p>Choisissez une sauvegarde créée par l'application.
            Deux confirmations explicites sont nécessaires ; l'ancienne base est conservée
            dans ce même profil.</p>
          <label className="backup-label" htmlFor="backup-choice">Sauvegarde disponible</label>
          <select id="backup-choice" value={selectedBackup}
            onChange={(event) => setSelectedBackup(event.currentTarget.value)}
            disabled={busy || !status || status.backups.length === 0}>
            {status?.backups.length === 0 && <option value="">Aucune sauvegarde</option>}
            {status?.backups.map((entry) => (
              <option key={entry.file_name} value={entry.file_name}>
                {entry.file_name} · {formatBytes(entry.bytes)}
              </option>
            ))}
          </select>
          <button className="secondary" type="button"
            disabled={busy || !isRestorableSelection(status, selectedBackup)}
            onClick={() => void restoreBackup()}>
            Restaurer dans une nouvelle base et activer
          </button>
        </div>
      </div>
      <p className="workspace-note">
        Les sauvegardes historiques créées manuellement pour M1.2 et M1.4 ne sont ni
        supprimées ni modifiées. Aucun appel à Ollama n'est nécessaire.
      </p>
    </section>
  );
}
