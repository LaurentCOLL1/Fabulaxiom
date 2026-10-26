import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { formatHierarchyError, newHierarchyId } from "./hierarchy";
import {announceWorkspaceChange,WORKSPACE_REVISION_CHANGED} from "./workspaceSync";
import {
  currentSceneRevision,
  hiddenSceneRevisionCount,
  revisionSummary,
  visibleSceneRevisions,
  type SceneRevisionHistory,
  type SceneTextRevision,
} from "./revisions";

type RevisionWorkspaceProps = {
  scene: {
    id: string;
    title: string;
  } | null;
};

const EMPTY_HISTORY: SceneRevisionHistory = {
  scene_id: "",
  current_revision_id: null,
  revisions: [],
};

export default function RevisionWorkspace({
  scene,
}: RevisionWorkspaceProps) {
  const [history, setHistory] = useState<SceneRevisionHistory>(EMPTY_HISTORY);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [archiveEnabled, setArchiveEnabled] = useState<boolean | null>(null);
  const [archivedIds, setArchivedIds] = useState<string[]>([]);
  const [showArchived, setShowArchived] = useState(false);

  useEffect(() => {
    let active = true;
    // The identity-only command does not open any database.
    void invoke<boolean>("greenfield_revision_archive_enabled")
      .then((enabled) => { if (active) setArchiveEnabled(enabled); })
      .catch(() => { if (active) setArchiveEnabled(false); });
    return () => { active = false; };
  }, []);

  async function loadHistory(sceneId: string) {
    const result = await invoke<SceneRevisionHistory>(
      "scene_revision_history",
      { input: { scene_id: sceneId } },
    );
    const archived = archiveEnabled
      ? await invoke<string[]>("scene_archived_revision_ids", {
          input: { scene_id: sceneId },
        })
      : [];
    setHistory(result);
    setArchivedIds(archived);
    const current = currentSceneRevision(result);
    setDraft(current?.content ?? "");
    return result;
  }

  useEffect(() => {
    if (!scene) {
      setHistory(EMPTY_HISTORY);
      setDraft("");
      setArchivedIds([]);
      setShowArchived(false);
      setError(null);
      return;
    }

    if (archiveEnabled === null) return;

    void (async () => {
      setBusy(true);
      setHistory(EMPTY_HISTORY);
      setArchivedIds([]);
      setShowArchived(false);
      setError(null);
      try {
        await loadHistory(scene.id);
      } catch (reason) {
        setError(formatHierarchyError(reason));
      } finally {
        setBusy(false);
      }
    })();
  }, [scene?.id, archiveEnabled]);

  async function saveRevision() {
    if (!scene) return;

    setBusy(true);
    setError(null);
    try {
      await invoke<SceneTextRevision>("create_scene_text_revision", {
        input: {
          id: newHierarchyId("revision"),
          scene_id: scene.id,
          content: draft,
        },
      });
      announceWorkspaceChange(WORKSPACE_REVISION_CHANGED);
      await loadHistory(scene.id);
    } catch (reason) {
      setError(formatHierarchyError(reason));
    } finally {
      setBusy(false);
    }
  }

  async function restoreRevision(revision: SceneTextRevision) {
    if (!scene) return;

    setBusy(true);
    setError(null);
    try {
      await invoke<SceneTextRevision>("set_current_scene_revision", {
        input: {
          scene_id: scene.id,
          revision_id: revision.id,
        },
      });
      announceWorkspaceChange(WORKSPACE_REVISION_CHANGED);
      await loadHistory(scene.id);
    } catch (reason) {
      setError(formatHierarchyError(reason));
    } finally {
      setBusy(false);
    }
  }

  async function setArchived(revision: SceneTextRevision, archived: boolean) {
    if (!scene || !archiveEnabled || busy) return;
    setBusy(true);
    setError(null);
    try {
      const ids = await invoke<string[]>("set_scene_revision_archived", {
        input: { scene_id: scene.id, revision_id: revision.id, archived },
      });
      setArchivedIds(ids);
    } catch (reason) {
      setError(formatHierarchyError(reason));
    } finally {
      setBusy(false);
    }
  }

  const current = currentSceneRevision(history);
  const visibleRevisions = visibleSceneRevisions(history, archivedIds, showArchived);
  const hiddenCount = hiddenSceneRevisionCount(history, archivedIds);

  return (
    <section className="revision-workspace" aria-labelledby="revision-title">
      <div className="workspace-heading">
        <div>
          <p className="card-kicker">M1.4 · texte versionné</p>
          <h3 id="revision-title">Révisions de scène</h3>
          <p>
            {scene
              ? "Scène : " + scene.title
              : "Sélectionnez une scène pour éditer son texte."}
          </p>
        </div>
        {scene && (
          <button
            type="button"
            className="secondary"
            disabled={busy}
            onClick={() =>
              void loadHistory(scene.id).catch((reason) =>
                setError(formatHierarchyError(reason)),
              )
            }
          >
            Actualiser l'historique
          </button>
        )}
      </div>

      {error && (
        <div className="result failure revision-error" role="alert">
          <strong>RÉVISION REFUSÉE</strong>
          <span>{error}</span>
        </div>
      )}

      {scene ? (
        <div className="revision-grid">
          <div className="revision-editor">
            <label htmlFor="scene-text">Texte de la scène</label>
            <textarea
              id="scene-text"
              value={draft}
              onChange={(event) => setDraft(event.currentTarget.value)}
              disabled={busy}
              rows={16}
              placeholder="Écrivez le texte de cette scène…"
            />
            <div className="revision-editor-actions">
              <span className="context-line">
                {current
                  ? "Courante : v" + current.revision_number
                  : "Aucune révision enregistrée."}
              </span>
              <button type="button" disabled={busy} onClick={() => void saveRevision()}>
                Enregistrer une nouvelle révision
              </button>
            </div>
          </div>

          <div className="revision-history">
            <h4>Historique</h4>
            {archiveEnabled && (
              <div className="revision-editor-actions">
                <span className="context-line">{hiddenCount} révision(s) archivée(s)</span>
                <button
                  type="button"
                  className="secondary"
                  disabled={busy}
                  aria-pressed={showArchived}
                  onClick={() => setShowArchived((value) => !value)}
                >
                  {showArchived ? "Masquer les archivées" : "Afficher les archivées"}
                </button>
              </div>
            )}
            {history.revisions.length === 0 && (
              <p className="empty-state">
                L'historique est vide. La première sauvegarde créera v1.
              </p>
            )}

            {history.revisions.length > 0 && visibleRevisions.length === 0 && (
              <p className="empty-state">Toutes les révisions non courantes sont archivées.</p>
            )}
            {visibleRevisions.map((revision) => {
              const isCurrent = revision.id === history.current_revision_id;
              const isArchived = archivedIds.includes(revision.id);
              return (
                <article
                  key={revision.id}
                  className={
                    "revision-card" + (isCurrent ? " revision-current" : "")
                  }
                >
                  <div>
                    <strong>
                      v{revision.revision_number}
                      {isCurrent ? " · COURANTE" : ""}
                      {isArchived ? " · ARCHIVÉE" : ""}
                    </strong>
                    <p>{revisionSummary(revision)}</p>
                    <code>{revision.id}</code>
                  </div>
                  <p className="revision-preview">
                    {revision.content.length > 180
                      ? revision.content.slice(0, 180) + "…"
                      : revision.content || "(texte vide)"}
                  </p>
                  <div className="entity-actions">
                    {!isCurrent && !isArchived && (
                      <button
                        type="button"
                        className="secondary"
                        disabled={busy}
                        onClick={() => void restoreRevision(revision)}
                      >
                        Restaurer comme courante
                      </button>
                    )}
                    <button
                      type="button"
                      className="secondary"
                      disabled={busy}
                      onClick={() => setDraft(revision.content)}
                    >
                      Charger dans l'éditeur
                    </button>
                    {archiveEnabled && (!isCurrent || isArchived) && (
                      <button
                        type="button"
                        className="secondary"
                        disabled={busy}
                        onClick={() => void setArchived(revision, !isArchived)}
                      >
                        {isArchived ? "Désarchiver" : "Archiver (masquer)"}
                      </button>
                    )}
                  </div>
                </article>
              );
            })}
          </div>
        </div>
      ) : (
        <p className="empty-state">
          Ouvrez d'abord une scène dans le panneau Scenes.
        </p>
      )}

      <p className="workspace-note">
        Chaque sauvegarde crée une révision immuable. Restaurer une ancienne
        version ne supprime aucune révision : seul le pointeur courant change.
        {archiveEnabled && (
          <> L'archivage Greenfield masque seulement l'affichage et peut être annulé ;
          le texte, les citations et la provenance restent dans la base v6.</>
        )}
      </p>
    </section>
  );
}
