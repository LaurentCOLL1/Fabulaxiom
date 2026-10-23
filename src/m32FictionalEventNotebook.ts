import { inspectFictionalDraft, type FictionalDraft } from "./m32FictionalManualChronology";

/** Manual event CRUD rehearsal, on INVENTED browser-memory data only.
 * Does not create a SQLite table, Tauri IPC, canonical event or reader reveal.
 */
export type FictionalEventVersion = Readonly<{
  event_id: string; universe_id: string; version: number;
  title: string; note: string;
  anchor_id: string | null; source_revision_id: string | null;
  status: "current" | "superseded" | "withdrawn";
}>;
export type FictionalEventInput = Readonly<{
  title: string; note: string;
  anchor_id: string | null; source_revision_id: string | null;
}>;
export type FictionalEventAudit = Readonly<{
  action: "created" | "amended" | "withdrawn";
  event_id: string; version: number; explanation: string;
}>;
export type FictionalEventNotebook = Readonly<{
  draft: FictionalDraft;
  events: readonly FictionalEventVersion[];
  audit: readonly FictionalEventAudit[];
  nextId: number;
  data_origin: "fictional_browser_memory_only";
  real_g3_authorized: false;
}>;

function stop(reason: string): never { throw new Error("Carnet M3.2 fictif refusé : " + reason); }
function nonblank(input: string, maximum: number): string {
  if (typeof input !== "string" || !input.trim() || input.length > maximum)
    return stop("texte vide ou trop long");
  return input.trim();
}
function checkInput(draft: FictionalDraft, data: FictionalEventInput): FictionalEventInput {
  const title = nonblank(data?.title, 120);
  if (typeof data.note !== "string" || data.note.length > 400)
    return stop("note fictive trop longue");
  const anchorId = data.anchor_id;
  const revisionId = data.source_revision_id;
  if (anchorId === null && revisionId !== null)
    return stop("révision sans ancre temporelle explicite");
  if (anchorId !== null) {
    if (typeof anchorId !== "string")
      return stop("identifiant d'ancre fictive invalide");
    const anchor = draft.snapshot.anchors.find(a =>
      a.id === anchorId && a.universe_id === draft.snapshot.universe_id && a.status === "current");
    if (!anchor) return stop("ancre absente, étrangère ou historique");
    if (anchor.source_revision_id !== revisionId)
      return stop("identifiant de révision historique incompatible avec l'ancre");
    if (revisionId !== null && !draft.revisions.some(r =>
      r.revision_id === revisionId && r.universe_id === draft.snapshot.universe_id))
      return stop("révision historique inventée inconnue");
  }
  return { title, note: data.note.trim(), anchor_id: anchorId, source_revision_id: revisionId };
}
export function inspectFictionalEventNotebook(book: FictionalEventNotebook): FictionalEventNotebook {
  if (!book || book.data_origin !== "fictional_browser_memory_only" ||
      book.real_g3_authorized !== false || !Array.isArray(book.events) ||
      !Array.isArray(book.audit) || book.events.length > 512 ||
      book.audit.length > 512 || !Number.isSafeInteger(book.nextId) ||
      book.nextId < 1 || book.nextId > 513) {
    return stop("origine fictive ou taille non prouvée");
  }
  inspectFictionalDraft(book.draft);
  const universe = book.draft.snapshot.universe_id;
  const grouped = new Map<string, FictionalEventVersion[]>();
  for (const event of book.events) {
    if (event.universe_id !== universe ||
        !event.event_id.startsWith(universe + "-event-") ||
        !Number.isSafeInteger(event.version) || event.version < 1 ||
        !["current", "superseded", "withdrawn"].includes(event.status)) {
      return stop("événement étranger ou version incorrecte");
    }
    checkInput(book.draft, event);
    grouped.set(event.event_id, [...(grouped.get(event.event_id) ?? []), event]);
  }
  for (const versions of grouped.values()) {
    for (let i = 0; i < versions.length; i += 1) {
      if (versions[i].version !== i + 1 ||
          (i !== versions.length - 1 && versions[i].status !== "superseded") ||
          (i === versions.length - 1 && versions[i].status === "superseded"))
        return stop("historique de correction non monotone");
    }
  }
  // One appended version per human operation: preserve exact audit alignment.
  // This is a structural sanity check, not an authentication of historical bytes.
  if (book.audit.length !== book.events.length)
    return stop("audit incomplet ou surnuméraire");
  let createdCount = 0;
  for (let index = 0; index < book.events.length; index += 1) {
    const event = book.events[index];
    const audit = book.audit[index];
    if (event.version === 1) {
      createdCount += 1;
      if (event.event_id !== universe + "-event-" + String(createdCount).padStart(4, "0"))
        return stop("identifiant événementiel non monotone");
    }
    const expectedAction = event.version === 1 ? "created" :
      event.status === "withdrawn" ? "withdrawn" : "amended";
    if (!audit || audit.event_id !== event.event_id ||
        audit.version !== event.version || audit.action !== expectedAction ||
        typeof audit.explanation !== "string" || !audit.explanation.trim() ||
        audit.explanation.length > 240)
      return stop("audit fictif absent, désordonné ou incompatible");
  }
  if (book.nextId !== createdCount + 1)
    return stop("compteur d'événements incohérent");
  return book;
}
export function startFictionalEventNotebook(draft: FictionalDraft): FictionalEventNotebook {
  inspectFictionalDraft(draft);
  return inspectFictionalEventNotebook({
    draft, events: [], audit: [], nextId: 1,
    data_origin: "fictional_browser_memory_only", real_g3_authorized: false,
  });
}
export function currentFictionalEvents(book: FictionalEventNotebook): readonly FictionalEventVersion[] {
  inspectFictionalEventNotebook(book);
  return book.events.filter(e => e.status === "current");
}
export function createFictionalEvent(
  book: FictionalEventNotebook, input: FictionalEventInput,
): FictionalEventNotebook {
  inspectFictionalEventNotebook(book);
  const data = checkInput(book.draft, input);
  const event_id = book.draft.snapshot.universe_id + "-event-" + String(book.nextId).padStart(4, "0");
  if (book.events.some(e => e.event_id === event_id)) return stop("identifiant fictif déjà utilisé");
  const event: FictionalEventVersion = {
    ...data, universe_id: book.draft.snapshot.universe_id,
    event_id, version: 1, status: "current",
  };
  return inspectFictionalEventNotebook({
    ...book, nextId: book.nextId + 1,
    events: [...book.events, event],
    audit: [...book.audit, { action: "created", event_id, version: 1,
      explanation: "Événement créé manuellement en mémoire inventée" }],
  });
}
export function amendFictionalEvent(
  book: FictionalEventNotebook, eventId: string, input: FictionalEventInput,
  explanation: string,
): FictionalEventNotebook {
  inspectFictionalEventNotebook(book);
  const reason = nonblank(explanation, 240);
  const data = checkInput(book.draft, input);
  const old = book.events.find(e => e.event_id === eventId && e.status === "current");
  if (!old) return stop("événement absent, historique ou retiré");
  const next: FictionalEventVersion = { ...old, ...data, version: old.version + 1, status: "current" };
  return inspectFictionalEventNotebook({
    ...book,
    events: [...book.events.map(e => e === old ? { ...e, status: "superseded" as const } : e), next],
    audit: [...book.audit, { action: "amended", event_id: eventId,
      version: next.version, explanation: reason }],
  });
}
export function withdrawFictionalEvent(
  book: FictionalEventNotebook, eventId: string, explanation: string,
): FictionalEventNotebook {
  inspectFictionalEventNotebook(book);
  const reason = nonblank(explanation, 240);
  const old = book.events.find(e => e.event_id === eventId && e.status === "current");
  if (!old) return stop("événement absent, historique ou déjà retiré");
  const tombstone: FictionalEventVersion = {
    ...old, version: old.version + 1, status: "withdrawn",
  };
  return inspectFictionalEventNotebook({
    ...book,
    events: [...book.events.map(e => e === old ? { ...e, status: "superseded" as const } : e),
      tombstone],
    audit: [...book.audit, { action: "withdrawn", event_id: eventId,
      version: tombstone.version, explanation: reason }],
  });
}
