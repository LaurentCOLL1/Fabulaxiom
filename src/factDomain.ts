import type {SceneTextRevision} from "./revisions";

export const FACT_STATUSES = [
  "draft", "suggestion", "canon", "variant", "unknown", "ambiguous", "contradictory",
] as const;
export type FactStatus = (typeof FACT_STATUSES)[number];
export const STATUS_LABELS: Record<FactStatus,string> = {
  draft:"Brouillon", suggestion:"Suggestion", canon:"Canon confirmé",
  variant:"Variante", unknown:"Inconnu", ambiguous:"Ambigu", contradictory:"Contradictoire",
};
export type FactSource = {
  id:string; fact_id:string; universe_id:string; revision_id:string;
  start_byte:number; end_byte:number; quoted_text:string;
};
export type FactRecord = {
  fact: {
    id:string; entity_id:string; universe_id:string; fact_key:string; fact_value:string;
    provenance_kind:"sourced"|"unsourced"; validity_kind:string|null;
    validity_text:string|null; created_at_utc:string;
  };
  source:FactSource|null;
};
export type FactSnapshot = {universe_id:string;records:FactRecord[]};
export type ReviewState = {
  fact_id:string;universe_id:string;status:FactStatus;revision_number:number;
};
export type ReviewSnapshot = {universe_id:string;reviews:ReviewState[]};
export type ReviewEvent = {
  id:string;fact_id:string;universe_id:string;revision_number:number;
  previous_status:FactStatus;next_status:FactStatus;action_kind:string;
  reviewer_label:string;reason:string;recorded_at_utc:string;
};
export type ReviewHistory = {state:ReviewState;events:ReviewEvent[]};
export type SelectedQuote = {revision_id:string;start_byte:number;end_byte:number;quoted_text:string};
export type SourceEvidence = {
  fact_id:string;universe_id:string;revision_id:string;scene_id:string;
  revision_number:number;content:string;quoted_text:string;start_byte:number;end_byte:number;
};
const isObject=(v:unknown):v is Record<string,unknown> =>
  !!v && typeof v==="object" && !Array.isArray(v);
const isString=(v:unknown):v is string=>typeof v==="string";
const isOptionalText=(v:unknown):v is string|null=>v===null||isString(v);
const isInteger=(v:unknown):v is number=>Number.isSafeInteger(v);
const isStatus=(v:unknown):v is FactStatus =>
  typeof v==="string" && (FACT_STATUSES as readonly string[]).includes(v);
const fail=(detail:string):never=>{throw new Error("Réponse IPC des faits invalide : "+detail);};

export function decodeFactSnapshot(value:unknown,universeId:string):FactSnapshot {
  if(!isObject(value)||value.universe_id!==universeId||!Array.isArray(value.records))
    return fail("univers ou liste de faits incorrecte.");
  for(const row of value.records) {
    if(!isObject(row)||!isObject(row.fact))return fail("fait malformé.");
    const f=row.fact;
    if(![f.id,f.entity_id,f.universe_id,f.fact_key,f.fact_value,f.created_at_utc].every(isString)
      ||f.universe_id!==universeId || !["sourced","unsourced"].includes(String(f.provenance_kind))
      ||!isOptionalText(f.validity_kind)||!isOptionalText(f.validity_text))
      return fail("identité ou provenance de fait incohérente.");
    if(f.provenance_kind==="sourced") {
      if(!isObject(row.source))return fail("citation manquante.");
      const s=row.source;
      if(![s.id,s.fact_id,s.universe_id,s.revision_id,s.quoted_text].every(isString)
        ||s.fact_id!==f.id||s.universe_id!==universeId
        ||!isInteger(s.start_byte)||!isInteger(s.end_byte)
        ||(s.start_byte as number)<0||(s.end_byte as number)<=(s.start_byte as number))
        return fail("citation incohérente.");
    } else if(row.source!==null) return fail("un fait sans source possède une citation.");
  }
  return value as FactSnapshot;
}
export function decodeReviewSnapshot(value:unknown,universeId:string):ReviewSnapshot {
  if(!isObject(value)||value.universe_id!==universeId||!Array.isArray(value.reviews))
    return fail("registre des statuts incomplet.");
  for(const s of value.reviews) {
    if(!isObject(s)||!isString(s.fact_id)||s.universe_id!==universeId
      ||!isStatus(s.status)||!isInteger(s.revision_number)||(s.revision_number as number)<0)
      return fail("statut ou version invalide.");
  }
  return value as ReviewSnapshot;
}
export function decodeReviewHistory(value:unknown,factId:string,universeId:string):ReviewHistory {
  if(!isObject(value)||!isObject(value.state)||!Array.isArray(value.events))
    return fail("historique absent.");
  const s=value.state;
  if(s.fact_id!==factId||s.universe_id!==universeId||!isStatus(s.status)||
    !isInteger(s.revision_number)||(s.revision_number as number)<0)
    return fail("historique d'un autre fait.");
  let previous:"draft"|FactStatus="draft";
  for(let i=0;i<value.events.length;i++){
    const e=value.events[i];
    if(!isObject(e)||e.fact_id!==factId||e.universe_id!==universeId
      ||!isString(e.id)||!isString(e.action_kind)||!isString(e.reviewer_label)
      ||!isString(e.reason)||!isString(e.recorded_at_utc)
      ||!isStatus(e.previous_status)||!isStatus(e.next_status)
      ||e.previous_status!==previous||e.revision_number!==i+1)
      return fail("chaîne de revue incorrecte.");
    previous=e.next_status;
  }
  if(s.revision_number!==value.events.length ||s.status!==previous)
    return fail("état courant sans événement correspondant.");
  return value as ReviewHistory;
}
export function quoteFromSelection(
  revision:Pick<SceneTextRevision,"id"|"content">,
  startUtf16:number,endUtf16:number,
):SelectedQuote {
  const {content}=revision;
  if(!Number.isSafeInteger(startUtf16)||!Number.isSafeInteger(endUtf16)
    ||startUtf16<0||startUtf16>=endUtf16||endUtf16>content.length)
    throw new Error("Sélectionnez un passage non vide dans la révision.");
  // A browser selection uses UTF-16. Refuse positions inside a surrogate pair.
  for(const point of [startUtf16,endUtf16]) {
    if(point>0 && point<content.length
      && content.charCodeAt(point-1)>=0xD800 && content.charCodeAt(point-1)<=0xDBFF
      && content.charCodeAt(point)>=0xDC00 && content.charCodeAt(point)<=0xDFFF)
      throw new Error("La sélection coupe un caractère Unicode.");
  }
  const byteEncoder=new TextEncoder();
  const start=byteEncoder.encode(content.slice(0,startUtf16)).length;
  const end=byteEncoder.encode(content.slice(0,endUtf16)).length;
  const bytes=byteEncoder.encode(content);
  const extracted=new TextDecoder("utf-8",{fatal:true}).decode(bytes.subarray(start,end));
  if(extracted!==content.slice(startUtf16,endUtf16))
    throw new Error("La sélection coupe un caractère Unicode : sélectionnez un passage complet.");
  return {revision_id:revision.id,start_byte:start,end_byte:end,quoted_text:extracted};
}
export function verifySourceEvidence(value:unknown,universeId:string,source:FactSource):SourceEvidence {
  if(!isObject(value)||value.universe_id!==universeId||value.revision_id!==source.revision_id
    ||value.fact_id!==source.fact_id||!isString(value.scene_id)||!isInteger(value.revision_number)
    ||!isString(value.content)||value.quoted_text!==source.quoted_text
    ||value.start_byte!==source.start_byte||value.end_byte!==source.end_byte)
    return fail("révision de citation incohérente.");
  const bytes=new TextEncoder().encode(value.content as string);
  const start=source.start_byte,end=source.end_byte;
  if(start<0||end>bytes.length||start>=end) return fail("bornes de citation invalides.");
  let decoded:string;
  try{decoded=new TextDecoder("utf-8",{fatal:true}).decode(bytes.subarray(start,end));}
  catch{return fail("la citation coupe un caractère UTF-8.");}
  if(decoded!==source.quoted_text)return fail("texte cité différent de la révision.");
  return value as SourceEvidence;
}
export function reviewAction(
  current:FactStatus,next:FactStatus,confirmed:boolean
):{action_kind:"set_status"|"approve_canon"|"revoke_canon";confirmation_phrase:string|null} {
  if(current===next)throw new Error("Choisissez un état différent.");
  if(next==="canon"){
    if(!confirmed)throw new Error("Confirmation humaine explicite obligatoire pour approuver le canon.");
    return {action_kind:"approve_canon",confirmation_phrase:"APPROVE_CANON"};
  }
  if(current==="canon"){
    if(!confirmed)throw new Error("Confirmation humaine explicite obligatoire pour retirer le canon.");
    return {action_kind:"revoke_canon",confirmation_phrase:"REVOKE_CANON"};
  }
  return {action_kind:"set_status",confirmation_phrase:null};
}
export const newFactId=(prefix:"fact"|"source"|"review"):string =>
  prefix+"-"+crypto.randomUUID();
export function formatFactError(reason:unknown):string {
  if(isObject(reason)&&isString(reason.code)&&isString(reason.message))
    return "["+reason.code+"] "+reason.message;
  if(typeof reason==="string") {
    try{return formatFactError(JSON.parse(reason) as unknown);}
    catch{return reason;}
  }
  return reason instanceof Error?reason.message:String(reason);
}
