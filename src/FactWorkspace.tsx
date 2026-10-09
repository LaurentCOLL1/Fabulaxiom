import {useEffect,useMemo,useState,type FormEvent,type SyntheticEvent} from "react";
import {invoke} from "@tauri-apps/api/core";
import type {HierarchySnapshot,Universe} from "./hierarchy";
import type {NarrativeEntity,EntitySnapshot} from "./entity";
import {decodeEntitySnapshot,KIND_LABELS} from "./entity";
import type {SceneRevisionHistory,SceneTextRevision} from "./revisions";
import {
  FACT_STATUSES,STATUS_LABELS,decodeFactSnapshot,decodeReviewSnapshot,
  decodeReviewHistory,quoteFromSelection,verifySourceEvidence,reviewAction,
  newFactId,formatFactError,type FactSnapshot,type ReviewSnapshot,
  type ReviewHistory,type FactRecord,type FactStatus,type SelectedQuote,type SourceEvidence,
} from "./factWorkspace";

const EMPTY_HIERARCHY:HierarchySnapshot={
  universes:[],series:[],novels:[],chapters:[],scenes:[],
};
const EMPTY_FACTS:FactSnapshot={universe_id:"",records:[]};
const EMPTY_REVIEWS:ReviewSnapshot={universe_id:"",reviews:[]};
const VALIDITY=[["","Aucune"],["exact","Exacte"],["approximate","Approximative"],
  ["relative","Relative"],["unknown","Inconnue"]] as const;

export default function FactWorkspace() {
  const [hierarchy,setHierarchy]=useState<HierarchySnapshot>(EMPTY_HIERARCHY);
  const [universeId,setUniverseId]=useState("");
  const [entities,setEntities]=useState<NarrativeEntity[]>([]);
  const [facts,setFacts]=useState<FactSnapshot>(EMPTY_FACTS);
  const [reviews,setReviews]=useState<ReviewSnapshot>(EMPTY_REVIEWS);
  const [busy,setBusy]=useState(false);
  const [error,setError]=useState<string|null>(null);
  const [notice,setNotice]=useState<string|null>(null);
  const [entityId,setEntityId]=useState("");
  const [factKey,setFactKey]=useState("");
  const [factValue,setFactValue]=useState("");
  const [provenance,setProvenance]=useState<"unsourced"|"sourced">("unsourced");
  const [validityKind,setValidityKind]=useState("");
  const [validityText,setValidityText]=useState("");
  const [sceneId,setSceneId]=useState("");
  const [revisionId,setRevisionId]=useState("");
  const [revisionHistory,setRevisionHistory]=useState<SceneRevisionHistory|null>(null);
  const [quote,setQuote]=useState<SelectedQuote|null>(null);
  const [selectedFactId,setSelectedFactId]=useState("");
  const [sourceEvidence,setSourceEvidence]=useState<SourceEvidence|null>(null);
  const [reviewHistory,setReviewHistory]=useState<ReviewHistory|null>(null);
  const [nextStatus,setNextStatus]=useState<FactStatus>("suggestion");
  const [reviewerLabel,setReviewerLabel]=useState("");
  const [reviewReason,setReviewReason]=useState("");
  const [confirmed,setConfirmed]=useState(false);

  const universes:Universe[]=hierarchy.universes;
  const ownNovels=useMemo(()=>hierarchy.novels.filter(n=>n.universe_id===universeId),
    [hierarchy,universeId]);
  const ownChapters=useMemo(()=>hierarchy.chapters.filter(c=>ownNovels.some(n=>n.id===c.novel_id)),
    [hierarchy,ownNovels]);
  const ownScenes=useMemo(()=>hierarchy.scenes.filter(s=>ownChapters.some(c=>c.id===s.chapter_id)),
    [hierarchy,ownChapters]);
  const selectedRecord=facts.records.find(r=>r.fact.id===selectedFactId)??null;
  const selectedStatus=reviews.reviews.find(r=>r.fact_id===selectedFactId)??null;
  const selectedRevision=revisionHistory?.revisions.find(r=>r.id===revisionId)??null;

  useEffect(()=>{
    let active=true;
    void invoke<HierarchySnapshot>("hierarchy_snapshot").then(snapshot=>{
      if(!active)return;
      if(!snapshot || !Array.isArray(snapshot.universes) || !Array.isArray(snapshot.scenes)
        ||!Array.isArray(snapshot.novels)||!Array.isArray(snapshot.chapters))
        throw new Error("Hiérarchie IPC incomplète.");
      setHierarchy(snapshot);
      setUniverseId(snapshot.universes[0]?.id??"");
    }).catch((e:unknown)=>{if(active)setError(formatFactError(e));});
    return ()=>{active=false;};
  },[]);

  async function fetchSnapshots(id:string) {
    const [entitiesValue,factsValue,reviewValue]=await Promise.all([
      invoke<unknown>("entity_snapshot",{input:{universe_id:id}}),
      invoke<unknown>("facts_snapshot",{input:{universe_id:id}}),
      invoke<unknown>("fact_review_snapshot",{input:{universe_id:id}}),
    ]);
    const parsedEntities:EntitySnapshot=decodeEntitySnapshot(entitiesValue);
    if(parsedEntities.entities.some(e=>e.universe_id!==id))
      throw new Error("Une entité appartient à un autre univers.");
    return {
      entities:parsedEntities.entities,
      facts:decodeFactSnapshot(factsValue,id),
      reviews:decodeReviewSnapshot(reviewValue,id),
    };
  }

  useEffect(()=>{
    let active=true;
    setEntities([]);
    setFacts(EMPTY_FACTS);
    setReviews(EMPTY_REVIEWS);
    setEntityId("");setSceneId("");setRevisionId("");
    setRevisionHistory(null);setQuote(null);setSelectedFactId("");
    setSourceEvidence(null);setReviewHistory(null);setConfirmed(false);
    setError(null);setNotice(null);
    if(!universeId)return()=>{active=false;};
    void fetchSnapshots(universeId).then(data=>{
      if(!active)return;
      setEntities(data.entities);setFacts(data.facts);setReviews(data.reviews);
      setEntityId(data.entities[0]?.id??"");
    }).catch((e:unknown)=>{if(active)setError(formatFactError(e));});
    return ()=>{active=false;};
  },[universeId]);

  useEffect(()=>{
    let active=true;
    setRevisionHistory(null);setRevisionId("");setQuote(null);
    if(!sceneId||!ownScenes.some(s=>s.id===sceneId))return()=>{active=false;};
    void invoke<SceneRevisionHistory>("scene_revision_history",{input:{scene_id:sceneId}})
      .then(value=>{
        if(!active)return;
        if(!value||value.scene_id!==sceneId||!Array.isArray(value.revisions))
          throw new Error("Historique de scène IPC invalide.");
        setRevisionHistory(value);
        setRevisionId(value.current_revision_id??value.revisions[value.revisions.length-1]?.id??"");
      }).catch((e:unknown)=>{if(active)setError(formatFactError(e));});
    return ()=>{active=false;};
  },[sceneId,ownScenes]);

  async function refresh(id:string) {
    const data=await fetchSnapshots(id);
    setEntities(data.entities);setFacts(data.facts);setReviews(data.reviews);
    setEntityId(old=>data.entities.some(e=>e.id===old)?old:data.entities[0]?.id??"");
  }

  async function createFact(event:FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if(!universeId||!entities.some(e=>e.id===entityId)||!factKey.trim()||!factValue.trim())
      return;
    if(provenance==="sourced" && (!selectedRevision||quote?.revision_id!==selectedRevision.id)) {
      setError("Sélectionnez un passage exact dans une révision de scène.");
      return;
    }
    if(validityKind && !validityText.trim()) {
      setError("Précisez la validité temporelle ou choisissez Aucune.");
      return;
    }
    setBusy(true);setError(null);setNotice(null);
    try{
      await invoke("create_narrative_fact",{input:{
        id:newFactId("fact"),entity_id:entityId,
        fact_key:factKey.trim(),fact_value:factValue.trim(),
        provenance_kind:provenance,
        validity_kind:validityKind||null,
        validity_text:validityKind?validityText.trim():null,
        source:provenance==="sourced"&&quote?{...quote,id:newFactId("source")}:null,
      }});
      await refresh(universeId);
      setFactKey("");setFactValue("");setQuote(null);
      setNotice("Fait enregistré en brouillon. Aucune promotion automatique au canon.");
    }catch(e){setError(formatFactError(e));}
    finally{setBusy(false);}
  }

  async function openFact(record:FactRecord) {
    setSelectedFactId(record.fact.id);
    setReviewHistory(null);setSourceEvidence(null);
    setNextStatus("suggestion");setConfirmed(false);
    setError(null);setBusy(true);
    try{
      const historyValue=await invoke<unknown>("review_fact_history",{
        input:{fact_id:record.fact.id,universe_id:universeId},
      });
      setReviewHistory(decodeReviewHistory(historyValue,record.fact.id,universeId));
      if(record.source) {
        const evidenceValue=await invoke<unknown>("fact_source_revision",{
          input:{fact_id:record.fact.id,universe_id:universeId},
        });
        setSourceEvidence(verifySourceEvidence(evidenceValue,universeId,record.source));
      }
    }catch(e){setError(formatFactError(e));}
    finally{setBusy(false);}
  }

  async function saveReview(event:FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if(!selectedRecord||!reviewHistory||!selectedStatus || !reviewerLabel.trim()||!reviewReason.trim())
      return;
    setBusy(true);setError(null);setNotice(null);
    try{
      if(selectedStatus.revision_number!==reviewHistory.state.revision_number)
        throw new Error("Version de revue désynchronisée : actualisez.");
      const choice=reviewAction(reviewHistory.state.status,nextStatus,confirmed);
      if(choice.action_kind!=="set_status" && !window.confirm(
        choice.action_kind==="approve_canon"
          ?"Confirmer explicitement la promotion de ce fait au canon ?"
          :"Confirmer explicitement le retrait de ce fait du canon ?"))
        return;
      const result=await invoke<unknown>("review_narrative_fact",{input:{
        id:newFactId("review"),fact_id:selectedRecord.fact.id,universe_id:universeId,
        expected_revision:reviewHistory.state.revision_number,next_status:nextStatus,
        action_kind:choice.action_kind,confirmation_phrase:choice.confirmation_phrase,
        reviewer_label:reviewerLabel.trim(),reason:reviewReason.trim(),
      }});
      setReviewHistory(decodeReviewHistory(result,selectedRecord.fact.id,universeId));
      await refresh(universeId);
      setConfirmed(false);setReviewReason("");
      setNotice("Décision ajoutée à l'historique immuable.");
    }catch(e){setError(formatFactError(e));}
    finally{setBusy(false);}
  }

  function selectQuote(event:SyntheticEvent<HTMLTextAreaElement>) {
    const start=event.currentTarget.selectionStart,end=event.currentTarget.selectionEnd;
    if(!selectedRevision){setQuote(null);return;}
    try{
      setQuote(quoteFromSelection(selectedRevision,start,end));
      setError(null);
    }catch{setQuote(null);}
  }

  return <section className="workspace" aria-labelledby="fact-workspace-title">
    <div className="workspace-heading">
      <div>
        <p className="card-kicker">M2.5 · faits et revue humaine sans IA</p>
        <h2 id="fact-workspace-title">Faits narratifs et canon</h2>
        <p>Sources immuables, statuts explicites et décisions tracées. Un fait nouveau est toujours un brouillon.</p>
      </div>
      <button type="button" className="secondary" disabled={busy||!universeId}
        onClick={()=>void refresh(universeId).then(()=>setNotice("Données actualisées."))
          .catch((e:unknown)=>setError(formatFactError(e)))}>Actualiser</button>
    </div>
    {error&&<div className="result failure workspace-error" role="alert">{error}</div>}
    {notice&&<div className="result success" role="status">{notice}</div>}
    <div className="workspace-panel">
      <label htmlFor="fact-universe">Univers</label>
      <select id="fact-universe" value={universeId} disabled={busy}
        onChange={e=>setUniverseId(e.currentTarget.value)}>
        {!universes.length&&<option value="">Aucun univers</option>}
        {universes.map(u=><option key={u.id} value={u.id}>{u.name}</option>)}
      </select>
    </div>
    {universeId&&<div className="workspace-grid">
      <form className="workspace-panel stack-form" onSubmit={e=>void createFact(e)}>
        <h3>Créer un fait</h3>
        <label htmlFor="fact-entity">Entité concernée</label>
        <select id="fact-entity" value={entityId} disabled={busy}
          onChange={e=>setEntityId(e.currentTarget.value)}>
          {!entities.length&&<option value="">Aucune entité</option>}
          {entities.map(e=><option value={e.id} key={e.id}>{KIND_LABELS[e.kind]} · {e.name}</option>)}
        </select>
        <label htmlFor="fact-key">Attribut / relation</label>
        <input id="fact-key" value={factKey} disabled={busy}
          onChange={e=>setFactKey(e.currentTarget.value)} placeholder="ex. couleur des yeux"/>
        <label htmlFor="fact-value">Valeur</label>
        <textarea id="fact-value" value={factValue} disabled={busy} rows={3}
          onChange={e=>setFactValue(e.currentTarget.value)} placeholder="Énoncé factuel précis"/>
        <label htmlFor="fact-validity">Validité temporelle (facultatif)</label>
        <select id="fact-validity" value={validityKind} disabled={busy}
          onChange={e=>{const value=e.currentTarget.value;setValidityKind(value);if(!value)setValidityText("");}}>
          {VALIDITY.map(([id,label])=><option key={id} value={id}>{label}</option>)}
        </select>
        {validityKind&&<input aria-label="Précision temporelle" value={validityText} disabled={busy}
          onChange={e=>setValidityText(e.currentTarget.value)} placeholder="Époque, date ou contexte"/>}
        <label htmlFor="fact-provenance">Provenance</label>
        <select id="fact-provenance" value={provenance} disabled={busy}
          onChange={e=>{
            const value=e.currentTarget.value as "sourced"|"unsourced";
            setProvenance(value);setQuote(null);
          }}>
          <option value="unsourced">Sans citation — brouillon non sourcé</option>
          <option value="sourced">Citation exacte d'une révision de scène</option>
        </select>
        {provenance==="sourced"&&<div className="workspace-panel">
          <label htmlFor="fact-scene">Scène dans cet univers</label>
          <select id="fact-scene" value={sceneId} disabled={busy} onChange={e=>setSceneId(e.currentTarget.value)}>
            <option value="">Choisir une scène</option>
            {ownScenes.map(s=><option key={s.id} value={s.id}>
              {ownNovels.find(n=>ownChapters.some(c=>c.id===s.chapter_id&&c.novel_id===n.id))?.title ?? "Roman"} · {s.title}
            </option>)}
          </select>
          <label htmlFor="fact-revision">Révision immuable (pas nécessairement courante)</label>
          <select id="fact-revision" disabled={busy||!revisionHistory} value={revisionId}
            onChange={e=>{setRevisionId(e.currentTarget.value);setQuote(null);}}>
            {!revisionHistory?.revisions.length&&<option value="">Aucune révision</option>}
            {revisionHistory?.revisions.map(r=><option key={r.id} value={r.id}>
              v{r.revision_number}{revisionHistory.current_revision_id===r.id?" · Courante":""} · {r.id}
            </option>)}
          </select>
          {selectedRevision&&<div>
            <label htmlFor="fact-revision-text">Sélectionner à la souris le passage exact ci-dessous</label>
            <textarea id="fact-revision-text" readOnly rows={7} value={selectedRevision.content}
              onSelect={selectQuote} aria-describedby="fact-selection-description"/>
            <p id="fact-selection-description" className="workspace-note">
              La citation mémorise les bornes en octets UTF-8 de cette révision historique.
            </p>
            {quote&&<div className="result success" role="status">
              Passage : « {quote.quoted_text} » · octets {quote.start_byte}–{quote.end_byte}
            </div>}
          </div>}
        </div>}
        <button type="submit" disabled={busy||!entityId||!factKey.trim()||!factValue.trim()
          ||(!!validityKind&&!validityText.trim())
          ||(provenance==="sourced"&&(!quote||quote.revision_id!==revisionId))}>
          Enregistrer comme brouillon
        </button>
      </form>

      <div className="workspace-panel">
        <h3>Faits de l'univers ({facts.records.length})</h3>
        {!facts.records.length&&<p className="empty-state">Aucun fait. Les entités restent inchangées.</p>}
        <div className="entity-list">
          {facts.records.map(row=>{
            const state=reviews.reviews.find(s=>s.fact_id===row.fact.id);
            return <article key={row.fact.id} className="entity-row">
              <div>
                <strong>{row.fact.fact_key} : {row.fact.fact_value}</strong>
                <p className="context-line">{entities.find(e=>e.id===row.fact.entity_id)?.name??row.fact.entity_id}</p>
                <p>{STATUS_LABELS[state?.status??"draft"]} · {row.source?"Source citée":"Sans source"}</p>
                {row.fact.validity_kind&&<p className="context-line">
                  Temps : {row.fact.validity_kind} · {row.fact.validity_text}
                </p>}
                <code>{row.fact.id}</code>
              </div>
              <button type="button" className="secondary" disabled={busy}
                onClick={()=>void openFact(row)}>Sources et revue</button>
            </article>;
          })}
        </div>
      </div>
    </div>}
    {selectedRecord&&<div className="workspace-panel">
      <h3>Provenance et décisions : {selectedRecord.fact.fact_key}</h3>
      <p>{selectedRecord.fact.fact_value}</p>
      {selectedRecord.source?
        <div>
          <p>Révision immuable : <code>{selectedRecord.source.revision_id}</code></p>
          <blockquote>« {selectedRecord.source.quoted_text} »</blockquote>
          {sourceEvidence&&<details>
            <summary>Voir le texte intégral de la révision citée · v{sourceEvidence.revision_number}</summary>
            <p className="context-line">Scène {sourceEvidence.scene_id}</p>
            <pre className="fact-evidence-text">{sourceEvidence.content}</pre>
            <p>Passage vérifié, octets {sourceEvidence.start_byte}–{sourceEvidence.end_byte}</p>
          </details>}
        </div>:
        <p className="workspace-note">Aucune citation. Ne pas interpréter ce fait comme prouvé.</p>}
      {reviewHistory&&<div>
        <p><strong>Statut actuel : {STATUS_LABELS[reviewHistory.state.status]}</strong>
          {" · "}révision de revue {reviewHistory.state.revision_number}</p>
        <h4>Historique immuable</h4>
        {!reviewHistory.events.length&&<p>Aucune revue humaine enregistrée.</p>}
        <ol>
          {reviewHistory.events.map(event=><li key={event.id}>
            {STATUS_LABELS[event.previous_status]} → {STATUS_LABELS[event.next_status]}
            {" · "}{event.recorded_at_utc} · {event.reviewer_label}
            <p>{event.reason}</p>
          </li>)}
        </ol>
        <form className="stack-form" onSubmit={e=>void saveReview(e)}>
          <h4>Décision humaine explicite</h4>
          <label htmlFor="fact-next-status">Nouveau statut</label>
          <select id="fact-next-status" value={nextStatus} disabled={busy}
            onChange={e=>{setNextStatus(e.currentTarget.value as FactStatus);setConfirmed(false);}}>
            {FACT_STATUSES.map(s=><option value={s} key={s}>{STATUS_LABELS[s]}</option>)}
          </select>
          <p className="workspace-note">
            Inconnu = information absente ; ambigu = interprétations multiples ;
            contradictoire = assertions incompatibles ; variante = autre possibilité narrative.
            Aucune de ces catégories n'est canonique par défaut.
          </p>
          <label htmlFor="fact-reviewer">Nom déclaré de la personne qui décide</label>
          <input id="fact-reviewer" value={reviewerLabel} disabled={busy}
            onChange={e=>setReviewerLabel(e.currentTarget.value)}
            placeholder="Nom libre, non authentifié"/>
          <label htmlFor="fact-reason">Motif de la décision</label>
          <textarea id="fact-reason" rows={3} value={reviewReason} disabled={busy}
            onChange={e=>setReviewReason(e.currentTarget.value)} placeholder="Pourquoi ce changement ?"/>
          {(nextStatus==="canon"||reviewHistory.state.status==="canon")&&
            <label className="fact-confirmation">
              <input type="checkbox" checked={confirmed} disabled={busy}
                onChange={e=>setConfirmed(e.currentTarget.checked)}/>
              {nextStatus==="canon"?"Je confirme personnellement l'approbation canonique.":
                "Je confirme personnellement le retrait de ce fait du canon."}
            </label>}
          <button type="submit" disabled={busy||!reviewerLabel.trim()||!reviewReason.trim()
            ||nextStatus===reviewHistory.state.status
            ||((nextStatus==="canon"||reviewHistory.state.status==="canon")&&!confirmed)}>
            {nextStatus==="canon"?"Approuver explicitement le canon":
              reviewHistory.state.status==="canon"?"Révoquer explicitement le canon":"Enregistrer la revue"}
          </button>
        </form>
      </div>}
    </div>}
    <p className="workspace-note">
      Aucune extraction IA ni validation canonique automatique. L'identité du réviseur est déclarée,
      pas authentifiée. Les décisions sont conservées ; les textes de scènes historiques ne sont jamais modifiés.
    </p>
  </section>;
}
