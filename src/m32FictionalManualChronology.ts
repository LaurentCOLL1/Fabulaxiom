import { compareM32WorldOrder } from "./M32WorldOrderComparison";
import { decodeM32ChronologyProjection, type M32AnchorProjection,
  type M32ChronologyProjection, type M32TimeKind } from "./M32ChronologyPreview";

/** Fiction-only draft reducer. NEVER persisted, no original DB or Tauri IPC. */
export type FictionalTimeInput = Readonly<{
  kind: M32TimeKind; calendar: string; label: string; precision: string;
  /** Undefined preserves the old link on supersession. Null intentionally clears it. */
  source_revision_id?: string | null;
  source_scene_id?: string | null;
}>;
/** Explicit immutable IDs only; titles are UI labels, never selectors/foreign keys. */
export type FictionalRevision = Readonly<{
  universe_id: string;
  novel_id: string;
  scene_id: string;
  revision_id: string;
  revision_label: string;
}>;
export type FictionalAudit = Readonly<{
  action: "anchor_created" | "anchor_superseded" | "precedence_created" | "precedence_revoked";
  id: string; explanation: string;
}>;
export type FictionalDraft = Readonly<{
  snapshot: M32ChronologyProjection;
  revisions: readonly FictionalRevision[];
  nextId: number;
  audit: readonly FictionalAudit[];
  data_origin: "fictional_browser_memory_only";
  real_g3_authorized: false;
}>;
function veto(reason: string): never { throw new Error("Atelier fictif M3.2 refusé : " + reason); }
function nonblank(s: string): string {
  if (typeof s !== "string" || s.length > 160 || s.trim().length === 0) {
    return veto("texte obligatoire (160 caractères maximum)");
  }
  return s.trim();
}
function name(d: FictionalDraft): string {
  if (!Number.isSafeInteger(d.nextId) || d.nextId < 1 || d.nextId > 4096)
    return veto("nombre de modifications dépassé");
  const id = "fiction-draft-" + String(d.nextId).padStart(4, "0");
  if (d.snapshot.anchors.some(a => a.id === id) ||
      d.snapshot.precedences.some(e => e.id === id)) return veto("identifiant déjà utilisé");
  return id;
}
function activeGraph(snapshot: M32ChronologyProjection): Map<string, string[]> {
  const active = new Set(snapshot.anchors.filter(a => a.status === "current").map(a => a.id));
  const graph = new Map<string, string[]>([...active].map(a => [a, []]));
  const seen = new Set<string>();
  for (const edge of snapshot.precedences.filter(e => e.status === "current")) {
    if (!active.has(edge.before_anchor_id) || !active.has(edge.after_anchor_id))
      return veto("lien actif vers une ancre historique");
    const key = edge.before_anchor_id + "\u0000" + edge.after_anchor_id;
    if (seen.has(key)) return veto("lien actif en double");
    seen.add(key);
    graph.get(edge.before_anchor_id)!.push(edge.after_anchor_id);
  }
  const visited = new Set<string>(), visiting = new Set<string>();
  function visit(node: string): void {
    if (visiting.has(node)) return veto("cycle temporel");
    if (visited.has(node)) return;
    visiting.add(node);
    for (const next of graph.get(node) ?? []) visit(next);
    visiting.delete(node);
    visited.add(node);
  }
  for (const node of graph.keys()) visit(node);
  return graph;
}
export function inspectFictionalDraft(d: FictionalDraft): FictionalDraft {
  if (d?.data_origin !== "fictional_browser_memory_only" || d.real_g3_authorized !== false)
    return veto("origine fictive non établie");
  const universe = d.snapshot?.universe_id;
  if (typeof universe !== "string" || !universe.startsWith("fiction-"))
    return veto("un univers inventé est obligatoire");
  decodeM32ChronologyProjection(d.snapshot, universe);
  if (!Array.isArray(d.revisions) || d.revisions.length > 128)
    return veto("catalogue de révisions inventées invalide");
  const available = new Map<string, FictionalRevision>();
  for (const rev of d.revisions) {
    if (rev.universe_id !== universe ||
        !rev.revision_id || rev.revision_id.length > 160 ||
        !rev.scene_id || !rev.novel_id || !rev.revision_label ||
        rev.revision_label.length > 160 ||
        available.has(rev.revision_id) ||
        !d.snapshot.narration.some(n =>
          n.universe_id === universe && n.scene_id === rev.scene_id &&
          n.novel_id === rev.novel_id)) {
      return veto("révision inventée inconnue, dupliquée ou étrangère");
    }
    available.set(rev.revision_id, rev);
  }
  for (const a of d.snapshot.anchors) {
    if (a.source_revision_id !== null && !available.has(a.source_revision_id))
      return veto("référence historique de scène sans révision inventée vérifiée");
  }
  activeGraph(d.snapshot);
  return d;
}
export function startFictionalDraft(
  snapshot: M32ChronologyProjection, revisions: readonly FictionalRevision[] = [],
): FictionalDraft {
  // Clone all data, never mutate caller-owned previews and never import any real source.
  const cloned: M32ChronologyProjection = {
    universe_id: snapshot.universe_id,
    reader_reveal_status: snapshot.reader_reveal_status,
    anchors: snapshot.anchors.map(a => ({ ...a })),
    precedences: snapshot.precedences.map(e => ({ ...e })),
    narration: snapshot.narration.map(n => ({ ...n })),
  };
  return inspectFictionalDraft({
    snapshot: cloned, revisions: revisions.map(r => ({ ...r })), nextId: 1, audit: [],
    data_origin: "fictional_browser_memory_only", real_g3_authorized: false,
  });
}
function makeAnchor(
  d: FictionalDraft, input: FictionalTimeInput, old?: M32AnchorProjection,
): M32AnchorProjection {
  const kind = input?.kind;
  if (!["exact", "approximate", "relative", "unknown"].includes(kind))
    return veto("type temporel non reconnu");
  const calendar = kind === "exact" || kind === "approximate" ? nonblank(input.calendar) : null;
  const label = kind === "exact" ? nonblank(input.label) : null;
  const precision = kind === "approximate" ? nonblank(input.precision) : null;
  const ref = input.source_revision_id === undefined
    ? old?.source_revision_id ?? null : input.source_revision_id;
  const scene = input.source_scene_id === undefined
    ? (ref === null ? null : d.revisions.find(r => r.revision_id === ref)?.scene_id ?? null)
    : input.source_scene_id;
  if ((ref === null && scene !== null) ||
      (ref !== null && (typeof ref !== "string" || typeof scene !== "string" ||
        !d.revisions.some(r => r.revision_id === ref && r.scene_id === scene &&
          r.universe_id === d.snapshot.universe_id)))) {
    return veto("la scène et la révision immuable exacte doivent correspondre");
  }
  return {
    id: name(d), universe_id: d.snapshot.universe_id, time_kind: kind,
    status: "current", calendar_name: calendar, fictional_label: label,
    precision_text: precision, source_revision_id: ref,
  };
}
export function createFictionalAnchor(d: FictionalDraft, input: FictionalTimeInput): FictionalDraft {
  inspectFictionalDraft(d);
  const anchor = makeAnchor(d, input);
  return inspectFictionalDraft({
    ...d, nextId: d.nextId + 1,
    snapshot: { ...d.snapshot, anchors: [...d.snapshot.anchors, anchor] },
    audit: [...d.audit, { action: "anchor_created", id: anchor.id, explanation: "Ajout manuel fictif" }],
  });
}
export function supersedeFictionalAnchor(
  d: FictionalDraft, oldId: string, input: FictionalTimeInput,
): FictionalDraft {
  inspectFictionalDraft(d);
  const old = d.snapshot.anchors.find(a => a.id === oldId && a.status === "current");
  if (!old) return veto("ancre absente ou historique");
  const correction = previewFictionalCorrection(d, oldId);
  if (correction.verdict !== "allowed") return veto(correction.reason);
  const replacement = makeAnchor(d, input, old);
  return inspectFictionalDraft({
    ...d, nextId: d.nextId + 1,
    snapshot: { ...d.snapshot, anchors: [
      ...d.snapshot.anchors.map(a => a.id === oldId ? { ...a, status: "superseded" as const } : a),
      replacement,
    ] },
    audit: [...d.audit, { action: "anchor_superseded", id: oldId,
      explanation: "Remplacée par " + replacement.id + " (historique conservé)" }],
  });
}
/** Non-authoritative visual explanation for a proposed edge on fictional active IDs only.
 * A partial order remains partial: no inferred calendar value, canon or world ordering.
 */
export type FictionalPrecedencePreview = Readonly<{
  verdict: "unselected" | "allowed" | "blocked";
  reason: string;
  witness_anchor_ids: readonly string[];
  witness_edge_ids: readonly string[];
}>;
export function previewFictionalPrecedence(
  d: FictionalDraft, before: string, after: string,
): FictionalPrecedencePreview {
  inspectFictionalDraft(d);
  const noWitness = { witness_anchor_ids: [], witness_edge_ids: [] };
  if (!before || !after) return {
    verdict: "unselected", reason: "Choisir deux ancres fictives actives.", ...noWitness,
  };
  const active = new Set(d.snapshot.anchors.filter(a => a.status === "current").map(a => a.id));
  if (!active.has(before) || !active.has(after)) return {
    verdict: "blocked", reason: "Référence étrangère, absente ou historique.", ...noWitness,
  };
  if (before === after) return {
    verdict: "blocked", reason: "Relation réflexive interdite.", witness_anchor_ids: [before], witness_edge_ids: [],
  };
  const direct = d.snapshot.precedences.find(e => e.status === "current" &&
    e.before_anchor_id === before && e.after_anchor_id === after);
  if (direct) return {
    verdict: "blocked", reason: "Relation directe déjà déclarée.",
    witness_anchor_ids: [before, after], witness_edge_ids: [direct.id],
  };
  // BFS returns a deterministic shortest witness for after -> ... -> before.
  // A human proposed before -> after would close exactly this existing path into a cycle.
  const queue: { node: string; nodes: string[]; edges: string[] }[] = [
    { node: after, nodes: [after], edges: [] },
  ];
  const seen = new Set([after]);
  let cursor = 0;
  while (cursor < queue.length) {
    const current = queue[cursor++];
    if (current.node === before) {
      return {
        verdict: "blocked",
        reason: "cycle temporel : " + [before, ...current.nodes].join(" → "),
        witness_anchor_ids: [before, ...current.nodes],
        witness_edge_ids: current.edges,
      };
    }
    const outbound = d.snapshot.precedences
      .filter(e => e.status === "current" && e.before_anchor_id === current.node)
      .sort((a, b) => a.after_anchor_id.localeCompare(b.after_anchor_id) ||
        a.id.localeCompare(b.id));
    for (const edge of outbound) {
      if (!seen.has(edge.after_anchor_id)) {
        seen.add(edge.after_anchor_id);
        queue.push({
          node: edge.after_anchor_id,
          nodes: [...current.nodes, edge.after_anchor_id],
          edges: [...current.edges, edge.id],
        });
      }
    }
  }
  return { verdict: "allowed", reason: "Relation explicite possible, sans ordre total déduit.", ...noWitness };
}

/** Pure preflight. Never automatically revoke another assertion to permit correction. */
export type FictionalCorrectionPreview = Readonly<{
  verdict: "unselected" | "allowed" | "blocked";
  reason: string;
  active_edge_ids: readonly string[];
  historical_revision_id: string | null;
}>;
export function previewFictionalCorrection(
  d: FictionalDraft, oldId: string,
): FictionalCorrectionPreview {
  inspectFictionalDraft(d);
  const old = d.snapshot.anchors.find(a => a.id === oldId && a.status === "current");
  if (!old) return {
    verdict: oldId ? "blocked" : "unselected",
    reason: oldId ? "Ancre étrangère, absente ou déjà historique." : "Choisir une ancre à corriger.",
    active_edge_ids: [], historical_revision_id: null,
  };
  const dependencies = d.snapshot.precedences
    .filter(e => e.status === "current" &&
      (e.before_anchor_id === oldId || e.after_anchor_id === oldId))
    .map(e => e.id).sort();
  return {
    verdict: dependencies.length ? "blocked" : "allowed",
    reason: dependencies.length
      ? "Il faut révoquer explicitement les liens actifs avant correction : " + dependencies.join(", ")
      : "Correction possible en conservant la version et sa révision historique.",
    active_edge_ids: dependencies,
    historical_revision_id: old.source_revision_id,
  };
}

export function createFictionalPrecedence(
  d: FictionalDraft, before: string, after: string, explanation: string,
): FictionalDraft {
  inspectFictionalDraft(d);
  const reason = nonblank(explanation);
  const preview = previewFictionalPrecedence(d, before, after);
  if (preview.verdict !== "allowed") return veto(preview.reason);
  const edge = {
    id: name(d), universe_id: d.snapshot.universe_id,
    before_anchor_id: before, after_anchor_id: after,
    status: "current" as const, reason,
  };
  return inspectFictionalDraft({
    ...d, nextId: d.nextId + 1,
    snapshot: { ...d.snapshot, precedences: [...d.snapshot.precedences, edge] },
    audit: [...d.audit, { action: "precedence_created", id: edge.id,
      explanation: reason }],
  });
}
export function revokeFictionalPrecedence(
  d: FictionalDraft, edgeId: string, explanation: string,
): FictionalDraft {
  inspectFictionalDraft(d);
  const why = nonblank(explanation);
  if (!d.snapshot.precedences.some(e => e.id === edgeId && e.status === "current"))
    return veto("relation absente ou déjà historique");
  return inspectFictionalDraft({
    ...d, snapshot: { ...d.snapshot, precedences: d.snapshot.precedences.map(e =>
      e.id === edgeId ? { ...e, status: "revoked" as const } : e) },
    audit: [...d.audit, { action: "precedence_revoked", id: edgeId, explanation: why }],
  });
}

/** Read-only explanation of three independent coordinates in an invented manuscript.
 * Chapter/scene position is comparable only within the SAME novel.
 * It never proves an event's world time, calendar conversion or reader reveal.
 */
export type FictionalThreeOrdersPreview = Readonly<{
  verdict: "unselected" | "blocked" | "allowed";
  narration: "unselected" | "same_scene" | "before" | "after" |
    "separate_novels" | "indeterminate";
  narration_reason: string;
  world_reason: string;
  reader_reason: string;
}>;
export function previewFictionalThreeOrders(
  d: FictionalDraft, firstId: string, secondId: string,
): FictionalThreeOrdersPreview {
  inspectFictionalDraft(d);
  const common = {
    world_reason: "Chronologie du monde : indéterminée par ces positions de manuscrit.",
    reader_reason: "Révélation au lecteur : non renseignée (lecture seule).",
  };
  if (!firstId || !secondId) return {
    ...common, verdict: "unselected", narration: "unselected",
    narration_reason: "Choisir deux scènes fictives.",
  };
  const first = d.snapshot.narration.find(s => s.scene_id === firstId);
  const second = d.snapshot.narration.find(s => s.scene_id === secondId);
  if (!first || !second) return {
    ...common, verdict: "blocked", narration: "indeterminate",
    narration_reason: "Scène inconnue ou étrangère : comparaison refusée.",
  };
  if (first.scene_id === second.scene_id) return {
    ...common, verdict: "allowed", narration: "same_scene",
    narration_reason: "Même scène du manuscrit, aucun événement différent déduit.",
  };
  if (first.novel_id !== second.novel_id) return {
    ...common, verdict: "allowed", narration: "separate_novels",
    narration_reason: "Ordre de narration indéterminé entre romans distincts.",
  };
  const a = [first.chapter_order, first.scene_order];
  const b = [second.chapter_order, second.scene_order];
  const comparison = a[0] === b[0] ? a[1] - b[1] : a[0] - b[0];
  return comparison === 0 ? {
    ...common, verdict: "allowed", narration: "indeterminate",
    narration_reason: "Même position déclarée pour deux scènes distinctes : ordre indéterminé.",
  } : {
    ...common, verdict: "allowed", narration: comparison < 0 ? "before" : "after",
    narration_reason: comparison < 0
      ? "La première scène précède la seconde dans ce roman."
      : "La première scène suit la seconde dans ce roman.",
  };
}

/** Fictitious read-only bridge from exact immutable revisions to explicit human world time. */
export type FictionalSceneWorldProof = Readonly<{
  verdict: "unselected" | "blocked" | "indeterminate" | "proven";
  relation: "before" | "after" | null;
  witness_edge_ids: readonly string[];
  reason: string;
  data_origin: "fictional_browser_memory_only";
  writes: false;
}>;
export function previewFictionalSceneRevisionWorldOrder(
  d: FictionalDraft, firstSceneId: string, firstRevisionId: string,
  secondSceneId: string, secondRevisionId: string,
): FictionalSceneWorldProof {
  inspectFictionalDraft(d);
  const common = {
    data_origin: "fictional_browser_memory_only" as const,
    writes: false as const, relation: null, witness_edge_ids: [] as readonly string[],
  };
  if (!firstSceneId || !firstRevisionId || !secondSceneId || !secondRevisionId)
    return { ...common, verdict: "unselected",
      reason: "Choisir deux scènes et leurs révisions exactes avant toute preuve du monde." };
  const first = d.revisions.find(r => r.scene_id === firstSceneId &&
    r.revision_id === firstRevisionId && r.universe_id === d.snapshot.universe_id);
  const second = d.revisions.find(r => r.scene_id === secondSceneId &&
    r.revision_id === secondRevisionId && r.universe_id === d.snapshot.universe_id);
  if (!first || !second)
    return { ...common, verdict: "blocked",
      reason: "Révision étrangère, inconnue ou associée à une autre scène : preuve refusée." };
  if (firstSceneId === secondSceneId)
    return { ...common, verdict: "indeterminate",
      reason: "Deux révisions d'une scène ne prouvent pas deux événements distincts." };
  const leftAnchors = d.snapshot.anchors.filter(a =>
    a.status === "current" && a.source_revision_id === firstRevisionId);
  const rightAnchors = d.snapshot.anchors.filter(a =>
    a.status === "current" && a.source_revision_id === secondRevisionId);
  if (leftAnchors.length !== 1 || rightAnchors.length !== 1)
    return { ...common, verdict: "indeterminate",
      reason: "Aucune ancre courante unique pour chaque révision : temps du monde indéterminé." };
  const comparison = compareM32WorldOrder(d.snapshot, d.snapshot.universe_id,
    leftAnchors[0].id, rightAnchors[0].id);
  if (comparison.relation !== "before" && comparison.relation !== "after")
    return { ...common, verdict: "indeterminate",
      reason: "Aucune chaîne de précédences humaines actives entre ces ancres." };
  return {
    ...common, verdict: "proven", relation: comparison.relation,
    witness_edge_ids: comparison.witness.map(w => w.precedence_id),
    reason: comparison.relation === "before"
      ? "Temps du monde établi : première ancre avant la seconde (preuves humaines)."
      : "Temps du monde établi : première ancre après la seconde (preuves humaines).",
  };
}
