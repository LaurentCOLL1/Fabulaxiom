import type { ReactElement } from "react";

/**
 * M3.2 standalone synthetic read-only preview, NOT mounted by App.tsx.
 * Only invented fixture data; NO operator data, Tauri IPC or editing.
 * A sorted identity list is NOT interpreted as historical chronology.
 */
export type M32TimeKind = "exact" | "approximate" | "relative" | "unknown";
export type M32AssertionStatus = "current" | "revoked" | "superseded";

export type M32AnchorProjection = {
  id: string;
  universe_id: string;
  time_kind: M32TimeKind;
  status: M32AssertionStatus;
  calendar_name: string | null;
  fictional_label: string | null;
  precision_text: string | null;
  source_revision_id: string | null;
};

export type M32PrecedenceProjection = {
  id: string;
  universe_id: string;
  before_anchor_id: string;
  after_anchor_id: string;
  status: M32AssertionStatus;
  reason: string;
};

export type M32SceneNarration = {
  scene_id: string;
  universe_id: string;
  novel_id: string;
  novel_title: string;
  chapter_id: string;
  chapter_title: string;
  chapter_order: number;
  scene_order: number;
  scene_title: string;
};

export type M32ChronologyProjection = {
  universe_id: string;
  anchors: M32AnchorProjection[];
  precedences: M32PrecedenceProjection[];
  narration: M32SceneNarration[];
  reader_reveal_status: "not_authored";
};

const kinds: Record<M32TimeKind, string> = {
  exact: "Date fictive exacte",
  approximate: "Période approximative",
  relative: "Position relative",
  unknown: "Date inconnue",
};

const statuses: Record<M32AssertionStatus, string> = {
  current: "En vigueur",
  revoked: "Révoquée (historique)",
  superseded: "Remplacée (historique)",
};

function validNonblank(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}
function isKind(value: unknown): value is M32TimeKind {
  return typeof value === "string" && Object.prototype.hasOwnProperty.call(kinds, value);
}
function isStatus(value: unknown): value is M32AssertionStatus {
  return typeof value === "string" && Object.prototype.hasOwnProperty.call(statuses, value);
}

// Validate boundaries even for candidate read-only data. Never reveal an
// unverified mixed-Universe projection or silently promote old assertions.
export function decodeM32ChronologyProjection(
  input: M32ChronologyProjection,
  expectedUniverseId: string,
): M32ChronologyProjection {
  if (!validNonblank(expectedUniverseId) ||
      input?.universe_id !== expectedUniverseId ||
      !Array.isArray(input.anchors) ||
      !Array.isArray(input.precedences) ||
      !Array.isArray(input.narration) ||
      input.reader_reveal_status !== "not_authored") {
    throw new Error("Projection M3.2 : Univers ou structure invalide");
  }
  if (input.anchors.length > 512 || input.precedences.length > 2048 ||
      input.narration.length > 2048) {
    throw new Error("Projection M3.2 : volume synthétique excessif");
  }
  const ids = new Set<string>();
  for (const a of input.anchors) {
    if (a.universe_id !== expectedUniverseId || !validNonblank(a.id) ||
        ids.has(a.id) || !isKind(a.time_kind) ||
        !isStatus(a.status) ||
        (a.time_kind === "exact" &&
          (!validNonblank(a.fictional_label) || !validNonblank(a.calendar_name))) ||
        (a.time_kind === "approximate" &&
          (!validNonblank(a.precision_text) || !validNonblank(a.calendar_name))) ||
        ((a.time_kind === "unknown" || a.time_kind === "relative") &&
          (a.fictional_label !== null || a.calendar_name !== null ||
           a.precision_text !== null)) ||
        (a.source_revision_id !== null && !validNonblank(a.source_revision_id))) {
      throw new Error("Projection M3.2 : ancre invalide ou étrangère");
    }
    ids.add(a.id);
  }
  const edgeIds = new Set<string>();
  for (const edge of input.precedences) {
    if (edge.universe_id !== expectedUniverseId ||
        !validNonblank(edge.id) || edgeIds.has(edge.id) ||
        !ids.has(edge.before_anchor_id) || !ids.has(edge.after_anchor_id) ||
        edge.before_anchor_id === edge.after_anchor_id ||
        !isStatus(edge.status) || !validNonblank(edge.reason)) {
      throw new Error("Projection M3.2 : relation invalide ou étrangère");
    }
    edgeIds.add(edge.id);
  }
  const scenes = new Set<string>();
  for (const scene of input.narration) {
    if (scene.universe_id !== expectedUniverseId ||
        !validNonblank(scene.scene_id) || scenes.has(scene.scene_id) ||
        !validNonblank(scene.novel_id) || !validNonblank(scene.novel_title) ||
        !validNonblank(scene.chapter_id) || !validNonblank(scene.chapter_title) ||
        !validNonblank(scene.scene_title) ||
        !Number.isSafeInteger(scene.chapter_order) || scene.chapter_order < 0 ||
        !Number.isSafeInteger(scene.scene_order) || scene.scene_order < 0) {
      throw new Error("Projection M3.2 : scène de narration invalide");
    }
    scenes.add(scene.scene_id);
  }
  return input;
}

export default function M32ChronologyPreview({
  expectedUniverseId,
  snapshot,
}: {
  expectedUniverseId: string;
  snapshot: M32ChronologyProjection | null;
}): ReactElement {
  if (!snapshot) {
    return (
      <section aria-label="Chronologie M3.2 isolée" role="status">
        <h2>Chronologie manuelle — aucune donnée vérifiée</h2>
        <p>Aucune commande IPC de modification n’est disponible dans cette projection.</p>
      </section>
    );
  }
  let checked: M32ChronologyProjection;
  try {
    checked = decodeM32ChronologyProjection(snapshot, expectedUniverseId);
  } catch {
    return (
      <section role="alert" aria-label="Projection M3.2 refusée">
        <h2>Projection de chronologie refusée</h2>
        <p>Univers, références ou états incohérents. Aucune donnée n’est affichée.</p>
      </section>
    );
  }
  const anchors = [...checked.anchors].sort((a, b) => a.id.localeCompare(b.id));
  const precedences = [...checked.precedences].sort((a, b) => a.id.localeCompare(b.id));
  // Keep manuscript ordering *inside a novel*; cross-novel ordering is unknown.
  const narration = [...checked.narration].sort((a, b) =>
    a.novel_id.localeCompare(b.novel_id) ||
    a.chapter_order - b.chapter_order ||
    a.scene_order - b.scene_order ||
    a.scene_id.localeCompare(b.scene_id),
  );
  return (
    <section aria-label="Chronologie M3.2 isolée">
      <h2>Chronologie manuelle — projection en lecture seule</h2>
      <p>Univers : <code>{checked.universe_id}</code></p>
      <p>Les identifiants sont triés pour l’affichage seulement, sans inventer une chronologie.</p>
      <section aria-label="Chronologie du monde">
        <h3>Chronologie du monde</h3>
        {anchors.length === 0 ? <p>Aucune ancre temporelle déclarée.</p> : (
          <ul>{anchors.map((anchor) => (
            <li key={anchor.id}>
              <strong>{anchor.id}</strong> — {kinds[anchor.time_kind]} — {statuses[anchor.status]}
              {anchor.fictional_label && <span> — {anchor.fictional_label}</span>}
              {anchor.calendar_name && <span> ({anchor.calendar_name})</span>}
              {anchor.precision_text && <span> — précision : {anchor.precision_text}</span>}
              {anchor.source_revision_id && <span> — révision : {anchor.source_revision_id}</span>}
            </li>
          ))}</ul>
        )}
        <h4>Avant / après — assertions humaines</h4>
        {precedences.length === 0 ? <p>Aucune relation explicitement déclarée.</p> : (
          <ul>{precedences.map((edge) => (
            <li key={edge.id}>
              <strong>{edge.before_anchor_id}</strong> avant <strong>{edge.after_anchor_id}</strong>
              {" — "}{statuses[edge.status]} — motif : {edge.reason}
            </li>
          ))}</ul>
        )}
      </section>
      <section aria-label="Ordre de narration">
        <h3>Ordre de narration</h3>
        <p>Ordre par roman, chapitre et scène. Aucun ordre global entre romans n’est déduit.</p>
        {narration.length === 0 ? <p>Aucune scène liée au manuscrit.</p> : (
          <ol>{narration.map((scene) => (
            <li key={scene.scene_id}>
              {scene.novel_title} / {scene.chapter_title} / {scene.scene_title}
              {" — "}position : {scene.chapter_order + 1}.{scene.scene_order + 1}
            </li>
          ))}</ol>
        )}
      </section>
      <section aria-label="Ordre de révélation au lecteur">
        <h3>Ordre de révélation au lecteur</h3>
        <p>Non renseigné : aucune révélation ne peut être inférée du texte, des scènes ou du temps du monde.</p>
      </section>
      <p>Prototype sans commandes IPC, sans sauvegarde et sans modification de SQLite.</p>
    </section>
  );
}
