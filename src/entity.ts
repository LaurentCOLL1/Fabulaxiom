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
