import {useEffect,useState,type FormEvent} from "react";
import {invoke} from "@tauri-apps/api/core";
import {KIND_LABELS,NARRATIVE_KINDS,formatEntityError,newEntityId,
  type EntitySnapshot,type NarrativeKind} from "./entity";
import type {HierarchySnapshot,Universe} from "./hierarchy";

const EMPTY:EntitySnapshot={entities:[],aliases:[]};

export default function EntityWorkspace() {
  const [universes,setUniverses]=useState<Universe[]>([]);
  const [universeId,setUniverseId]=useState("");
  const [data,setData]=useState<EntitySnapshot>(EMPTY);
  const [kind,setKind]=useState<NarrativeKind>("character");
  const [name,setName]=useState("");
  const [aliasInputs,setAliasInputs]=useState<Record<string,string>>({});
  const [busy,setBusy]=useState(false);
  const [error,setError]=useState<string|null>(null);

  async function loadUniverses() {
    const hierarchy=await invoke<HierarchySnapshot>("hierarchy_snapshot");
    setUniverses(hierarchy.universes);
    setUniverseId(current=>
      hierarchy.universes.some(u=>u.id===current) ? current : hierarchy.universes[0]?.id ?? "");
  }
  async function reload(id:string) {
    if(!id){setData(EMPTY);return;}
    setData(await invoke<EntitySnapshot>("entity_snapshot",{input:{universe_id:id}}));
  }
  useEffect(()=>{
    void loadUniverses().catch((e:unknown)=>setError(formatEntityError(e)));
  },[]);
  useEffect(()=>{
    let active=true;
    if(!universeId){setData(EMPTY);return;}
    void invoke<EntitySnapshot>("entity_snapshot",{input:{universe_id:universeId}})
      .then(result=>{if(active)setData(result);})
      .catch((e:unknown)=>{if(active)setError(formatEntityError(e));});
    return ()=>{active=false;};
  },[universeId]);

  async function mutate(command:string,input:unknown) {
    setBusy(true);setError(null);
    try {
      await invoke(command,{input});
      await reload(universeId);
      return true;
    } catch(e) {
      setError(formatEntityError(e));
      return false;
    } finally {setBusy(false);}
  }
  async function add(event:FormEvent) {
    event.preventDefault();
    if(!universeId||!name.trim())return;
    if(await mutate("create_narrative_entity",{
      id:newEntityId("entity"),universe_id:universeId,kind,name:name.trim()
    }))setName("");
  }
  async function addAlias(event:FormEvent,id:string) {
    event.preventDefault();
    const alias=(aliasInputs[id]??"").trim();
    if(!alias)return;
    if(await mutate("create_entity_alias",{
      id:newEntityId("alias"),entity_id:id,alias
    }))setAliasInputs(prev=>({...prev,[id]:""}));
  }
  return <section className="workspace" aria-labelledby="narrative-entities-title">
    <div className="workspace-heading">
      <div>
        <p className="card-kicker">M2.2 · Entités narratives sans IA</p>
        <h2 id="narrative-entities-title">Personnages, lieux et événements</h2>
        <p>Six types d'entités et leurs alias, identifiants permanents, sans Ollama.</p>
      </div>
      <button type="button" className="secondary" disabled={busy}
        onClick={()=>void loadUniverses().then(()=>reload(universeId))
          .catch((e:unknown)=>setError(formatEntityError(e)))}>Actualiser</button>
    </div>
    {error&&<div className="result failure workspace-error" role="alert">{error}</div>}
    <div className="workspace-panel">
      <label htmlFor="entity-universe">Univers</label>
      <select id="entity-universe" value={universeId}
        onChange={e=>setUniverseId(e.currentTarget.value)} disabled={busy}>
        {!universes.length&&<option value="">Aucun univers</option>}
        {universes.map(u=><option key={u.id} value={u.id}>{u.name}</option>)}
      </select>
      {universeId&&<form onSubmit={e=>void add(e)} className="stack-form">
        <label htmlFor="entity-kind">Type</label>
        <select id="entity-kind" value={kind} disabled={busy}
          onChange={e=>setKind(e.currentTarget.value as NarrativeKind)}>
          {NARRATIVE_KINDS.map(k=><option key={k} value={k}>{KIND_LABELS[k]}</option>)}
        </select>
        <label htmlFor="entity-name">Nom</label>
        <input id="entity-name" value={name} disabled={busy}
          onChange={e=>setName(e.currentTarget.value)} placeholder="Nom de l'entité"/>
        <button type="submit" disabled={busy||!name.trim()}>Créer l'entité</button>
      </form>}
    </div>
    <p className="workspace-note">{data.entities.length} entités dans cet univers.</p>
    <div className="workspace-grid">
      {data.entities.map(entity=><div className="workspace-panel" key={entity.id}>
        <p className="card-kicker">{KIND_LABELS[entity.kind]}</p>
        <h3>{entity.name}</h3><p className="context-line">{entity.id}</p>
        <div className="entity-actions">
          <button type="button" className="secondary" disabled={busy}
            onClick={()=>{
              const proposed=window.prompt("Renommer l'entité :",entity.name);
              if(proposed!==null&&proposed.trim()&&proposed.trim()!==entity.name)
                void mutate("rename_narrative_entity",{id:entity.id,name:proposed.trim()});
            }}>Renommer</button>
          <button type="button" className="danger" disabled={busy}
            onClick={()=>{
              if(window.confirm("Supprimer cette entité ?"))
                void mutate("delete_narrative_entity",{id:entity.id});
            }}>Supprimer</button>
        </div>
        <h4>Alias</h4>
        <div className="entity-list">
          {data.aliases.filter(a=>a.entity_id===entity.id).map(a=>
            <div className="entity-row" key={a.id}>
              <span>{a.alias}</span><code>{a.id}</code>
              <div className="entity-actions">
                <button className="secondary" type="button" disabled={busy}
                  onClick={()=>{
                    const value=window.prompt("Renommer l'alias :",a.alias);
                    if(value!==null&&value.trim()&&value.trim()!==a.alias)
                      void mutate("rename_entity_alias",{id:a.id,alias:value.trim()});
                  }}>Renommer</button>
                <button className="danger" type="button" disabled={busy}
                  onClick={()=>{
                    if(window.confirm("Supprimer l'alias ?"))
                      void mutate("delete_entity_alias",{id:a.id});
                  }}>Supprimer</button>
              </div>
            </div>)}
        </div>
        <form className="inline-form" onSubmit={e=>void addAlias(e,entity.id)}>
          <input aria-label={"Nouvel alias de "+entity.name} disabled={busy}
            value={aliasInputs[entity.id]??""} placeholder="Nouvel alias"
            onChange={e=>setAliasInputs(prev=>({...prev,[entity.id]:e.currentTarget.value}))}/>
          <button type="submit" disabled={busy||!(aliasInputs[entity.id]??"").trim()}>
            Ajouter
          </button>
        </form>
      </div>)}
    </div>
  </section>;
}
