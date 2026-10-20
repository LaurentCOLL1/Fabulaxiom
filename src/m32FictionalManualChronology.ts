import { decodeM32ChronologyProjection, type M32AnchorProjection,
  type M32ChronologyProjection, type M32TimeKind } from "./M32ChronologyPreview";

/** Fiction-only draft reducer. NEVER persisted, no original DB or Tauri IPC. */
export type FictionalTimeInput = Readonly<{
  kind: M32TimeKind; calendar: string; label: string; precision: string;
}>;
export type FictionalAudit = Readonly<{
  action: "anchor_created" | "anchor_superseded" | "precedence_created" | "precedence_revoked";
  id: string; explanation: string;
}>;
export type FictionalDraft = Readonly<{
  snapshot: M32ChronologyProjection;
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
  activeGraph(d.snapshot);
  return d;
}
export function startFictionalDraft(snapshot: M32ChronologyProjection): FictionalDraft {
  // Clone all data, never mutate caller-owned previews and never import any real source.
  const cloned: M32ChronologyProjection = {
    universe_id: snapshot.universe_id,
    reader_reveal_status: snapshot.reader_reveal_status,
    anchors: snapshot.anchors.map(a => ({ ...a })),
    precedences: snapshot.precedences.map(e => ({ ...e })),
    narration: snapshot.narration.map(n => ({ ...n })),
  };
  return inspectFictionalDraft({
    snapshot: cloned, nextId: 1, audit: [],
    data_origin: "fictional_browser_memory_only", real_g3_authorized: false,
  });
}
function makeAnchor(d: FictionalDraft, input: FictionalTimeInput): M32AnchorProjection {
  const kind = input?.kind;
  if (!["exact", "approximate", "relative", "unknown"].includes(kind))
    return veto("type temporel non reconnu");
  const calendar = kind === "exact" || kind === "approximate" ? nonblank(input.calendar) : null;
  const label = kind === "exact" ? nonblank(input.label) : null;
  const precision = kind === "approximate" ? nonblank(input.precision) : null;
  return {
    id: name(d), universe_id: d.snapshot.universe_id, time_kind: kind,
    status: "current", calendar_name: calendar, fictional_label: label,
    precision_text: precision, source_revision_id: null,
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
  if (d.snapshot.precedences.some(e => e.status === "current" &&
      (e.before_anchor_id === oldId || e.after_anchor_id === oldId))) {
    return veto("révoquer explicitement les liens actifs avant correction");
  }
  const replacement = makeAnchor(d, input);
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
export function createFictionalPrecedence(
  d: FictionalDraft, before: string, after: string, explanation: string,
): FictionalDraft {
  inspectFictionalDraft(d);
  const reason = nonblank(explanation);
  if (before === after) return veto("relation réflexive");
  const active = new Set(d.snapshot.anchors.filter(a => a.status === "current").map(a => a.id));
  if (!active.has(before) || !active.has(after)) return veto("les deux ancres doivent être actives");
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
