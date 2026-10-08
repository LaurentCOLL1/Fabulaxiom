export const NARRATIVE_KINDS = ["character", "place", "organization", "object", "event", "world_rule"] as const;
export type NarrativeKind = (typeof NARRATIVE_KINDS)[number];
export const KIND_LABELS: Record<NarrativeKind, string> = {
  character:"Personnage", place:"Lieu", organization:"Organisation",
  object:"Objet", event:"Événement", world_rule:"Règle du monde",
};
export type NarrativeEntity = {
  id:string; universe_id:string; kind:NarrativeKind; name:string; created_at_utc:string;
};
export type EntityAlias = {id:string; entity_id:string; universe_id:string; alias:string};
export type EntitySnapshot = {entities:NarrativeEntity[]; aliases:EntityAlias[]};
/** Accept a captured string, never a React event whose currentTarget may be cleared. */
export function updateAliasDraft(
  current: Readonly<Record<string,string>>, entityId:string, capturedValue:string
):Record<string,string> {
  return {...current,[entityId]:capturedValue};
}
export function newEntityId(prefix:"entity" | "alias"):string {
  return prefix + "-" + crypto.randomUUID();
}
export function isNarrativeKind(value:string):value is NarrativeKind {
  return (NARRATIVE_KINDS as readonly string[]).includes(value);
}
export function formatEntityError(reason:unknown):string {
  if (reason && typeof reason === "object") {
    const r=reason as {code?:unknown; message?:unknown};
    if(typeof r.code==="string" && typeof r.message==="string") {
      return "[" + r.code + "] " + r.message;
    }
  }
  if(typeof reason==="string") {
    try {return formatEntityError(JSON.parse(reason) as unknown);} catch{return reason;}
  }
  if(reason instanceof Error) return reason.message;
  return String(reason);
}

/** Reject malformed IPC snapshots before React tries to render alias records. */
export function decodeEntitySnapshot(value: unknown): EntitySnapshot {
  if (!value || typeof value !== "object") {
    throw new Error("Réponse du registre narratif invalide.");
  }
  const snapshot = value as {entities?:unknown; aliases?:unknown};
  if (!Array.isArray(snapshot.entities) || !Array.isArray(snapshot.aliases)) {
    throw new Error("Réponse du registre narratif incomplète (entités ou alias).");
  }
  for (const entity of snapshot.entities) {
    if (!entity || typeof entity !== "object" ||
        typeof entity.id !== "string" ||
        typeof entity.universe_id !== "string" ||
        typeof entity.name !== "string" ||
        typeof entity.created_at_utc !== "string" ||
        typeof entity.kind !== "string" || !isNarrativeKind(entity.kind)) {
      throw new Error("Enregistrement d'entité invalide reçu depuis Rust.");
    }
  }
  for (const alias of snapshot.aliases) {
    if (!alias || typeof alias !== "object" ||
        typeof alias.id !== "string" ||
        typeof alias.entity_id !== "string" ||
        typeof alias.universe_id !== "string" ||
        typeof alias.alias !== "string") {
      throw new Error("Enregistrement d'alias invalide reçu depuis Rust.");
    }
  }
  return value as EntitySnapshot;
}
