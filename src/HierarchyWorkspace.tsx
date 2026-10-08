import {
  useEffect,
  useMemo,
  useState,
  type FormEvent,
  type ReactNode,
} from "react";
import { invoke } from "@tauri-apps/api/core";
import RevisionWorkspace from "./RevisionWorkspace";
import {
  formatHierarchyError,
  newHierarchyId,
  optionalId,
  type Chapter,
  type HierarchySnapshot,
  type Novel,
  type Scene,
  type Series,
  type Universe,
} from "./hierarchy";

const EMPTY_SNAPSHOT: HierarchySnapshot = {
  universes: [],
  series: [],
  novels: [],
  chapters: [],
  scenes: [],
};

type EntityRowProps = {
  id: string;
  label: string;
  selected?: boolean;
  busy: boolean;
  onOpen?: () => void;
  onRename: (value: string) => Promise<void>;
  onDelete: () => Promise<void>;
  onMoveUp?: () => Promise<void>;
  onMoveDown?: () => Promise<void>;
  extra?: ReactNode;
};

function EntityRow({
  id,
  label,
  selected = false,
  busy,
  onOpen,
  onRename,
  onDelete,
  onMoveUp,
  onMoveDown,
  extra,
}: EntityRowProps) {
  const [draft, setDraft] = useState(label);

  useEffect(() => {
    setDraft(label);
  }, [label]);

  return (
    <div className={"entity-row" + (selected ? " entity-row-selected" : "")}>
      <div className="entity-main">
        <input
          value={draft}
          onChange={(event) => setDraft(event.currentTarget.value)}
          disabled={busy}
          aria-label={"Nom de " + label}
        />
        <code>{id}</code>
      </div>

      {extra}

      <div className="entity-actions">
        {onOpen && (
          <button
            type="button"
            className="secondary"
            onClick={onOpen}
            disabled={busy}
          >
            Ouvrir
          </button>
        )}
        <button
          type="button"
          className="secondary"
          onClick={() => void onRename(draft)}
          disabled={busy || draft.trim().length === 0 || draft === label}
        >
          Renommer
        </button>
        {onMoveUp && (
          <button
            type="button"
            className="secondary compact"
            onClick={() => void onMoveUp()}
            disabled={busy}
            aria-label={"Monter " + label}
          >
            ↑
          </button>
        )}
        {onMoveDown && (
          <button
            type="button"
            className="secondary compact"
            onClick={() => void onMoveDown()}
            disabled={busy}
            aria-label={"Descendre " + label}
          >
            ↓
          </button>
        )}
        <button
          type="button"
          className="danger"
          onClick={() => {
            if (window.confirm("Supprimer « " + label + " » ?")) {
              void onDelete();
            }
          }}
          disabled={busy}
        >
          Supprimer
        </button>
      </div>
    </div>
  );
}

function sortByOrder<T extends { sort_order: number; id: string }>(items: T[]) {
  return [...items].sort(
    (left, right) =>
      left.sort_order - right.sort_order || left.id.localeCompare(right.id),
  );
}

export default function HierarchyWorkspace() {
  const [snapshot, setSnapshot] = useState<HierarchySnapshot>(EMPTY_SNAPSHOT);
  const [selectedUniverseId, setSelectedUniverseId] = useState("");
  const [selectedNovelId, setSelectedNovelId] = useState("");
  const [selectedChapterId, setSelectedChapterId] = useState("");
  const [selectedSceneId, setSelectedSceneId] = useState("");
  const [universeName, setUniverseName] = useState("");
  const [seriesName, setSeriesName] = useState("");
  const [novelTitle, setNovelTitle] = useState("");
  const [novelSeriesId, setNovelSeriesId] = useState("");
  const [chapterTitle, setChapterTitle] = useState("");
  const [sceneTitle, setSceneTitle] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    const result = await invoke<HierarchySnapshot>("hierarchy_snapshot");
    setSnapshot(result);
    return result;
  }

  useEffect(() => {
    void (async () => {
      setBusy(true);
      setError(null);
      try {
        await refresh();
      } catch (reason) {
        setError(formatHierarchyError(reason));
      } finally {
        setBusy(false);
      }
    })();
  }, []);

  const universeSeries = useMemo(
    () =>
      sortByOrder(
        snapshot.series.filter(
          (item) => item.universe_id === selectedUniverseId,
        ),
      ),
    [snapshot.series, selectedUniverseId],
  );

  const universeNovels = useMemo(
    () =>
      snapshot.novels.filter(
        (item) => item.universe_id === selectedUniverseId,
      ),
    [snapshot.novels, selectedUniverseId],
  );

  const selectedNovelChapters = useMemo(
    () =>
      sortByOrder(
        snapshot.chapters.filter(
          (item) => item.novel_id === selectedNovelId,
        ),
      ),
    [snapshot.chapters, selectedNovelId],
  );

  const selectedChapterScenes = useMemo(
    () =>
      sortByOrder(
        snapshot.scenes.filter(
          (item) => item.chapter_id === selectedChapterId,
        ),
      ),
    [snapshot.scenes, selectedChapterId],
  );

  useEffect(() => {
    if (
      selectedUniverseId &&
      snapshot.universes.some((item) => item.id === selectedUniverseId)
    ) {
      return;
    }
    setSelectedUniverseId(snapshot.universes[0]?.id ?? "");
  }, [snapshot.universes, selectedUniverseId]);

  useEffect(() => {
    if (
      selectedNovelId &&
      universeNovels.some((item) => item.id === selectedNovelId)
    ) {
      return;
    }
    setSelectedNovelId(universeNovels[0]?.id ?? "");
  }, [universeNovels, selectedNovelId]);

  useEffect(() => {
    if (
      selectedChapterId &&
      selectedNovelChapters.some((item) => item.id === selectedChapterId)
    ) {
      return;
    }
    setSelectedChapterId(selectedNovelChapters[0]?.id ?? "");
  }, [selectedNovelChapters, selectedChapterId]);

  useEffect(() => {
    if (
      selectedSceneId &&
      selectedChapterScenes.some((item) => item.id === selectedSceneId)
    ) {
      return;
    }
    setSelectedSceneId(selectedChapterScenes[0]?.id ?? "");
  }, [selectedChapterScenes, selectedSceneId]);

  useEffect(() => {
    if (
      novelSeriesId &&
      !universeSeries.some((item) => item.id === novelSeriesId)
    ) {
      setNovelSeriesId("");
    }
  }, [universeSeries, novelSeriesId]);

  async function mutate(command: string, input: unknown) {
    setBusy(true);
    setError(null);
    try {
      await invoke(command, { input });
      await refresh();
    } catch (reason) {
      setError(formatHierarchyError(reason));
    } finally {
      setBusy(false);
    }
  }

  async function createUniverse(event: FormEvent) {
    event.preventDefault();
    const name = universeName.trim();
    if (!name) return;
    await mutate("create_universe", {
      id: newHierarchyId("universe"),
      name,
    });
    setUniverseName("");
  }

  async function createSeries(event: FormEvent) {
    event.preventDefault();
    const name = seriesName.trim();
    if (!selectedUniverseId || !name) return;
    await mutate("create_series", {
      id: newHierarchyId("series"),
      universe_id: selectedUniverseId,
      name,
    });
    setSeriesName("");
  }

  async function createNovel(event: FormEvent) {
    event.preventDefault();
    const title = novelTitle.trim();
    if (!selectedUniverseId || !title) return;
    await mutate("create_novel", {
      id: newHierarchyId("novel"),
      universe_id: selectedUniverseId,
      series_id: optionalId(novelSeriesId),
      title,
    });
    setNovelTitle("");
  }

  async function createChapter(event: FormEvent) {
    event.preventDefault();
    const title = chapterTitle.trim();
    if (!selectedNovelId || !title) return;
    await mutate("create_chapter", {
      id: newHierarchyId("chapter"),
      novel_id: selectedNovelId,
      title,
    });
    setChapterTitle("");
  }

  async function createScene(event: FormEvent) {
    event.preventDefault();
    const title = sceneTitle.trim();
    if (!selectedChapterId || !title) return;
    await mutate("create_scene", {
      id: newHierarchyId("scene"),
      chapter_id: selectedChapterId,
      title,
    });
    setSceneTitle("");
  }

  const selectedUniverse = snapshot.universes.find(
    (item) => item.id === selectedUniverseId,
  );
  const selectedNovel = snapshot.novels.find(
    (item) => item.id === selectedNovelId,
  );
  const selectedChapter = snapshot.chapters.find(
    (item) => item.id === selectedChapterId,
  );
  const selectedScene = snapshot.scenes.find(
    (item) => item.id === selectedSceneId,
  );

  return (
    <section className="workspace" aria-labelledby="workspace-title">
      <div className="workspace-heading">
        <div>
          <p className="card-kicker">M1.3 · CRUD sans IA</p>
          <h2 id="workspace-title">Hiérarchie du projet</h2>
          <p>
            Gérez Universe → Series optionnelle → Novel → Chapter → Scene.
            Aucune de ces opérations n'appelle Ollama.
          </p>
        </div>
        <button
          type="button"
          className="secondary"
          onClick={() => void refresh().catch((reason) => setError(formatHierarchyError(reason)))}
          disabled={busy}
        >
          Actualiser
        </button>
      </div>

      {error && (
        <div className="result failure workspace-error" role="alert">
          <strong>OPÉRATION REFUSÉE</strong>
          <span>{error}</span>
        </div>
      )}

      <div className="workspace-grid">
        <section className="workspace-panel">
          <h3>Universes</h3>
          <form className="inline-form" onSubmit={(event) => void createUniverse(event)}>
            <input
              value={universeName}
              onChange={(event) => setUniverseName(event.currentTarget.value)}
              placeholder="Nom du nouvel univers"
              disabled={busy}
            />
            <button type="submit" disabled={busy || !universeName.trim()}>
              Créer
            </button>
          </form>

          <div className="entity-list">
            {snapshot.universes.map((item: Universe) => (
              <EntityRow
                key={item.id}
                id={item.id}
                label={item.name}
                selected={item.id === selectedUniverseId}
                busy={busy}
                onOpen={() => setSelectedUniverseId(item.id)}
                onRename={(value) =>
                  mutate("rename_universe", { id: item.id, value })
                }
                onDelete={() => mutate("delete_universe", { id: item.id })}
              />
            ))}
            {snapshot.universes.length === 0 && (
              <p className="empty-state">Créez d'abord un univers.</p>
            )}
          </div>
        </section>

        <section className="workspace-panel">
          <h3>Series</h3>
          <p className="context-line">
            {selectedUniverse
              ? "Univers : " + selectedUniverse.name
              : "Sélectionnez un univers."}
          </p>
          <form className="inline-form" onSubmit={(event) => void createSeries(event)}>
            <input
              value={seriesName}
              onChange={(event) => setSeriesName(event.currentTarget.value)}
              placeholder="Nom de la nouvelle série"
              disabled={busy || !selectedUniverseId}
            />
            <button
              type="submit"
              disabled={busy || !selectedUniverseId || !seriesName.trim()}
            >
              Créer
            </button>
          </form>

          <div className="entity-list">
            {universeSeries.map((item: Series, index) => (
              <EntityRow
                key={item.id}
                id={item.id}
                label={item.name}
                busy={busy}
                onRename={(value) =>
                  mutate("rename_series", { id: item.id, value })
                }
                onDelete={() => mutate("delete_series", { id: item.id })}
                onMoveUp={
                  index > 0
                    ? () =>
                        mutate("reorder_series", {
                          id: item.id,
                          new_index: index - 1,
                        })
                    : undefined
                }
                onMoveDown={
                  index < universeSeries.length - 1
                    ? () =>
                        mutate("reorder_series", {
                          id: item.id,
                          new_index: index + 1,
                        })
                    : undefined
                }
              />
            ))}
            {selectedUniverseId && universeSeries.length === 0 && (
              <p className="empty-state">Aucune série. Elles sont optionnelles.</p>
            )}
          </div>
        </section>

        <section className="workspace-panel">
          <h3>Novels</h3>
          <p className="context-line">
            {selectedUniverse
              ? "Univers : " + selectedUniverse.name
              : "Sélectionnez un univers."}
          </p>
          <form className="stack-form" onSubmit={(event) => void createNovel(event)}>
            <input
              value={novelTitle}
              onChange={(event) => setNovelTitle(event.currentTarget.value)}
              placeholder="Titre du nouveau roman"
              disabled={busy || !selectedUniverseId}
            />
            <select
              value={novelSeriesId}
              onChange={(event) => setNovelSeriesId(event.currentTarget.value)}
              disabled={busy || !selectedUniverseId}
            >
              <option value="">Sans série</option>
              {universeSeries.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.name}
                </option>
              ))}
            </select>
            <button
              type="submit"
              disabled={busy || !selectedUniverseId || !novelTitle.trim()}
            >
              Créer le roman
            </button>
          </form>

          <div className="entity-list">
            {universeNovels.map((item: Novel) => {
              const scope = sortByOrder(
                universeNovels.filter(
                  (candidate) => candidate.series_id === item.series_id,
                ),
              );
              const index = scope.findIndex((candidate) => candidate.id === item.id);

              return (
                <EntityRow
                  key={item.id}
                  id={item.id}
                  label={item.title}
                  selected={item.id === selectedNovelId}
                  busy={busy}
                  onOpen={() => setSelectedNovelId(item.id)}
                  onRename={(value) =>
                    mutate("rename_novel", { id: item.id, value })
                  }
                  onDelete={() => mutate("delete_novel", { id: item.id })}
                  onMoveUp={
                    index > 0
                      ? () =>
                          mutate("reorder_novel", {
                            id: item.id,
                            new_index: index - 1,
                          })
                      : undefined
                  }
                  onMoveDown={
                    index >= 0 && index < scope.length - 1
                      ? () =>
                          mutate("reorder_novel", {
                            id: item.id,
                            new_index: index + 1,
                          })
                      : undefined
                  }
                  extra={
                    <label className="series-picker">
                      Série
                      <select
                        value={item.series_id ?? ""}
                        onChange={(event) =>
                          void mutate("set_novel_series", {
                            id: item.id,
                            series_id: optionalId(event.currentTarget.value),
                          })
                        }
                        disabled={busy}
                      >
                        <option value="">Sans série</option>
                        {universeSeries.map((seriesItem) => (
                          <option key={seriesItem.id} value={seriesItem.id}>
                            {seriesItem.name}
                          </option>
                        ))}
                      </select>
                    </label>
                  }
                />
              );
            })}
            {selectedUniverseId && universeNovels.length === 0 && (
              <p className="empty-state">Aucun roman dans cet univers.</p>
            )}
          </div>
        </section>

        <section className="workspace-panel">
          <h3>Chapters</h3>
          <p className="context-line">
            {selectedNovel
              ? "Roman : " + selectedNovel.title
              : "Sélectionnez un roman."}
          </p>
          <form className="inline-form" onSubmit={(event) => void createChapter(event)}>
            <input
              value={chapterTitle}
              onChange={(event) => setChapterTitle(event.currentTarget.value)}
              placeholder="Titre du chapitre"
              disabled={busy || !selectedNovelId}
            />
            <button
              type="submit"
              disabled={busy || !selectedNovelId || !chapterTitle.trim()}
            >
              Créer
            </button>
          </form>

          <div className="entity-list">
            {selectedNovelChapters.map((item: Chapter, index) => (
              <EntityRow
                key={item.id}
                id={item.id}
                label={item.title}
                selected={item.id === selectedChapterId}
                busy={busy}
                onOpen={() => setSelectedChapterId(item.id)}
                onRename={(value) =>
                  mutate("rename_chapter", { id: item.id, value })
                }
                onDelete={() => mutate("delete_chapter", { id: item.id })}
                onMoveUp={
                  index > 0
                    ? () =>
                        mutate("reorder_chapter", {
                          id: item.id,
                          new_index: index - 1,
                        })
                    : undefined
                }
                onMoveDown={
                  index < selectedNovelChapters.length - 1
                    ? () =>
                        mutate("reorder_chapter", {
                          id: item.id,
                          new_index: index + 1,
                        })
                    : undefined
                }
              />
            ))}
            {selectedNovelId && selectedNovelChapters.length === 0 && (
              <p className="empty-state">Aucun chapitre.</p>
            )}
          </div>
        </section>

        <section className="workspace-panel">
          <h3>Scenes</h3>
          <p className="context-line">
            {selectedChapter
              ? "Chapitre : " + selectedChapter.title
              : "Sélectionnez un chapitre."}
          </p>
          <form className="inline-form" onSubmit={(event) => void createScene(event)}>
            <input
              value={sceneTitle}
              onChange={(event) => setSceneTitle(event.currentTarget.value)}
              placeholder="Titre de la scène"
              disabled={busy || !selectedChapterId}
            />
            <button
              type="submit"
              disabled={busy || !selectedChapterId || !sceneTitle.trim()}
            >
              Créer
            </button>
          </form>

          <div className="entity-list">
            {selectedChapterScenes.map((item: Scene, index) => (
              <EntityRow
                key={item.id}
                id={item.id}
                label={item.title}
                selected={item.id === selectedSceneId}
                busy={busy}
                onOpen={() => setSelectedSceneId(item.id)}
                onRename={(value) =>
                  mutate("rename_scene", { id: item.id, value })
                }
                onDelete={() => mutate("delete_scene", { id: item.id })}
                onMoveUp={
                  index > 0
                    ? () =>
                        mutate("reorder_scene", {
                          id: item.id,
                          new_index: index - 1,
                        })
                    : undefined
                }
                onMoveDown={
                  index < selectedChapterScenes.length - 1
                    ? () =>
                        mutate("reorder_scene", {
                          id: item.id,
                          new_index: index + 1,
                        })
                    : undefined
                }
              />
            ))}
            {selectedChapterId && selectedChapterScenes.length === 0 && (
              <p className="empty-state">Aucune scène.</p>
            )}
          </div>
        </section>
      </div>

      <RevisionWorkspace
        scene={
          selectedScene
            ? { id: selectedScene.id, title: selectedScene.title }
            : null
        }
      />

      <p className="workspace-note">
        Les suppressions suivent les contraintes SQLite RESTRICT : un parent
        contenant encore des enfants est refusé avec une erreur déterministe.
        Une scène possédant des révisions est également protégée.
      </p>
    </section>
  );
}
