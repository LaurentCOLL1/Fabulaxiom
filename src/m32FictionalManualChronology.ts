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
      ? "Révoquer explicitement les liens actifs avant correction : " + dependencies.join(", ")
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
