import { useState, type ReactElement } from "react";
import { startFictionalDraft, type FictionalDraft, type FictionalRevision } from "./m32FictionalManualChronology";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import {
  previewFictionalHumanOrderBatch, confirmFictionalHumanOrderBatch,
  previewFictionalCreatedBatchSelectedPairs,
  type FictionalHumanOrder, type FictionalHumanOrderBatchPreview,
  previewFictionalHumanOrderRepair, confirmFictionalHumanOrderRepair,
  type FictionalHumanOrderRepair, type FictionalHumanOrderRepairPreview,
  previewFictionalRepairPairImpact, type FictionalRepairPairImpact,
  previewFictionalRepairSelectedPairs, type FictionalRepairSelectedPair,
  type FictionalRepairSelectedPairsImpact,
} from "./m32FictionalHumanOrderBatch";

/** Unmounted synthetic browser workflow: staged, reviewed and explicitly confirmed. */
export default function M32FictionalHumanOrderBatchLab({
  initial, revisions,
}: {
  initial: M32ChronologyProjection;
  revisions: readonly FictionalRevision[];
}): ReactElement {
  const [draft, setDraft] = useState<FictionalDraft>(() => startFictionalDraft(initial, revisions));
  const [before, setBefore] = useState("");
  const [after, setAfter] = useState("");
  const [reason, setReason] = useState("");
  const [staged, setStaged] = useState<readonly FictionalHumanOrder[]>([]);
  const [preview, setPreview] = useState<FictionalHumanOrderBatchPreview | null>(null);
  const [batchCompareLeft, setBatchCompareLeft] = useState("");
  const [batchCompareRight, setBatchCompareRight] = useState("");
  const [batchSelectedPairs, setBatchSelectedPairs] = useState<readonly FictionalRepairSelectedPair[]>([]);
  const [batchImpact, setBatchImpact] = useState<FictionalRepairSelectedPairsImpact | null>(null);
  const [feedback, setFeedback] = useState("");
  const [failed, setFailed] = useState(false);
  const [repairEdge, setRepairEdge] = useState("");
  const [repairMode, setRepairMode] = useState<"revoke" | "replace">("revoke");
  const [repairBefore, setRepairBefore] = useState("");
  const [repairAfter, setRepairAfter] = useState("");
  const [repairWhy, setRepairWhy] = useState("");
  const [replacementWhy, setReplacementWhy] = useState("");
  const [repairs, setRepairs] = useState<readonly FictionalHumanOrderRepair[]>([]);
  const [repairPreview, setRepairPreview] = useState<FictionalHumanOrderRepairPreview | null>(null);
  const [impactLeft, setImpactLeft] = useState("");
  const [impactRight, setImpactRight] = useState("");
  const [repairImpact, setRepairImpact] = useState<FictionalRepairPairImpact | null>(null);
  const [selectedImpactPairs, setSelectedImpactPairs] = useState<readonly FictionalRepairSelectedPair[]>([]);
  const [selectedPairsImpact, setSelectedPairsImpact] = useState<FictionalRepairSelectedPairsImpact | null>(null);
  const activeEdges = draft.snapshot.precedences.filter(e => e.status === "current");
  const active = draft.snapshot.anchors.filter(a => a.status === "current");

  function invalidate() { setPreview(null); setBatchImpact(null); setRepairPreview(null); setRepairImpact(null); setSelectedPairsImpact(null); setFeedback(""); setFailed(false); }
  function stage() {
    if (staged.length >= 16 || repairs.length > 0) {
      setFeedback("Maximum 16 propositions fictives."); setFailed(true); return;
    }
    setStaged(old => [...old, { before_anchor_id: before, after_anchor_id: after, reason }]);
    setBefore(""); setAfter(""); setReason(""); invalidate();
  }
  function stageBatchPair() {
    if (!batchCompareLeft || !batchCompareRight || batchSelectedPairs.length >= 8 ||
      batchSelectedPairs.some(pair =>
        (pair.left_anchor_id===batchCompareLeft && pair.right_anchor_id===batchCompareRight) ||
        (pair.left_anchor_id===batchCompareRight && pair.right_anchor_id===batchCompareLeft))) {
      setFeedback("Paire du lot fictif absente, doublonnée ou limite dépassée.");
      setFailed(true);return;
    }
    setBatchSelectedPairs(old=>[...old,{
      left_anchor_id:batchCompareLeft,right_anchor_id:batchCompareRight}]);
    setBatchCompareLeft("");setBatchCompareRight("");invalidate();
  }
  function prepare() {
    try {
      const candidate = previewFictionalHumanOrderBatch(draft, staged);
      const impact = batchSelectedPairs.length ?
        previewFictionalCreatedBatchSelectedPairs(draft,staged,batchSelectedPairs) : null;
      setPreview(candidate);setBatchImpact(impact);
      setFeedback("Lot fictif cohérent ; aucune modification appliquée.");
      setFailed(false);
    } catch (error) {
      setPreview(null);setBatchImpact(null);
      setFeedback(error instanceof Error ? error.message : "Lot refusé.");
      setFailed(true);
    }
  }
  function confirm() {
    if (!preview) return;
    try {
      const updated = confirmFictionalHumanOrderBatch(draft, staged, preview, true);
      setDraft(updated); setStaged([]); setRepairs([]); setPreview(null);setBatchImpact(null);
      setBatchSelectedPairs([]);setBatchCompareLeft("");setBatchCompareRight("");
      setRepairPreview(null);
      setFeedback("Lot fictif appliqué en mémoire seulement. Aucune sauvegarde.");
      setFailed(false);
    } catch (error) {
      setPreview(null); setFeedback(error instanceof Error ? error.message : "Lot refusé.");
      setFailed(true);
    }
  }

  function stageRepair() {
    if (!repairEdge || !repairWhy.trim() || repairs.length >= 16 || staged.length > 0 ||
        (repairMode === "replace" && (!repairBefore || !repairAfter || !replacementWhy.trim()))) {
      setFeedback("Choix explicites obligatoires : correction fictive refusée.");
      setFailed(true); return;
    }
    const replacement = repairMode === "replace" ?
      { before_anchor_id: repairBefore, after_anchor_id: repairAfter, reason: replacementWhy } : null;
    setRepairs(old => [...old, { precedence_id: repairEdge, revoke_reason: repairWhy, replacement }]);
    setRepairEdge(""); setRepairBefore(""); setRepairAfter("");
    setRepairWhy(""); setReplacementWhy(""); invalidate();
  }
  function stageImpactPair() {
    if (!impactLeft || !impactRight || selectedImpactPairs.length >= 8 ||
      selectedImpactPairs.some(pair =>
        (pair.left_anchor_id === impactLeft && pair.right_anchor_id === impactRight) ||
        (pair.left_anchor_id === impactRight && pair.right_anchor_id === impactLeft))) {
      setFeedback("Paire fictive absente, doublonnée ou limite dépassée."); setFailed(true); return;
    }
    setSelectedImpactPairs(old => [...old,{left_anchor_id:impactLeft,right_anchor_id:impactRight}]);
    setImpactLeft("");setImpactRight("");invalidate();
  }
  function prepareRepair() {
    try {
      const candidate = previewFictionalHumanOrderRepair(draft, repairs);
      if (Boolean(impactLeft) !== Boolean(impactRight)) {
        throw new Error("Choisir les deux ancres à comparer, ou aucune.");
      }
      const compared = impactLeft && impactRight
        ? previewFictionalRepairPairImpact(draft, repairs, impactLeft, impactRight)
        : null;
      const multiple = selectedImpactPairs.length
        ? previewFictionalRepairSelectedPairs(draft,repairs,selectedImpactPairs) : null;
      setRepairPreview(candidate);setRepairImpact(compared);setSelectedPairsImpact(multiple);setPreview(null);
      setFeedback("Révocation/correction fictive cohérente ; rien appliqué."); setFailed(false);
    } catch (error) {
      setRepairPreview(null); setRepairImpact(null); setSelectedPairsImpact(null);
      setFeedback(error instanceof Error ? error.message : "Correction fictive refusée."); setFailed(true);
    }
  }
  function confirmRepair() {
    if (!repairPreview) return;
    try {
      const updated = confirmFictionalHumanOrderRepair(draft, repairs, repairPreview, true);
      setDraft(updated); setRepairs([]); setStaged([]); setRepairPreview(null);
      setRepairImpact(null); setSelectedPairsImpact(null);setSelectedImpactPairs([]);setPreview(null);
      setRepairEdge(""); setFeedback("Historique conservé : appliqué en RAM. Aucune sauvegarde.");
      setFailed(false);
    } catch (error) {
      setRepairPreview(null); setRepairImpact(null);
      setFeedback(error instanceof Error ? error.message : "Correction fictive refusée."); setFailed(true);
    }
  }
  return <section aria-label="Lot de précédences humaines fictives M3.2">
    <h2>Déclarer plusieurs relations avant/après — laboratoire fictif</h2>
    <p role="note">Propositions explicites, simulation globale puis confirmation humaine.
      Aucun fichier, aucune persistance SQLite, aucun writer, aucune commande Tauri.
      L'ordre du monde, celui du récit et celui des révélations restent distincts.</p>
    <p>Univers inventé : <code>{draft.snapshot.universe_id}</code></p>
    <label>Événement antérieur
      <select value={before} onChange={e => setBefore(e.currentTarget.value)}>
        <option value="">Choisir explicitement</option>
        {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
      </select>
    </label>
    <label>Événement postérieur
      <select value={after} onChange={e => setAfter(e.currentTarget.value)}>
        <option value="">Choisir explicitement</option>
        {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
      </select>
    </label>
    <label>Justification de l'ordre humain
      <input value={reason} maxLength={160} onChange={e => setReason(e.currentTarget.value)} />
    </label>
    <button type="button" disabled={!before || !after || !reason.trim() || staged.length >= 16 || repairs.length > 0}
      onClick={stage}>Ajouter au lot fictif</button>
    <h3>Propositions non appliquées ({staged.length}/16)</h3>
    <ol>{staged.map((row, index) => <li key={index}>
      {row.before_anchor_id} avant {row.after_anchor_id} — {row.reason}
      <button type="button" onClick={() => {
        setStaged(old => old.filter((_, i) => i !== index)); invalidate();
      }}>Retirer cette proposition</button>
    </li>)}</ol>
    <section aria-label="Paires choisies pour le lot de créations fictives">
      <h3>Impact des nouvelles relations — paires choisies par l'auteur</h3>
      <p>Jusqu'à huit comparaisons explicites ; ni ordre global ni sauvegarde.</p>
      <label>Première ancre du lot à comparer
        <select value={batchCompareLeft} onChange={e=>{
          setBatchCompareLeft(e.currentTarget.value);invalidate();
        }}>
          <option value="">Choisir une ancre fictive</option>
          {active.map(a=><option key={a.id} value={a.id}>{a.id}</option>)}
        </select>
      </label>
      <label>Seconde ancre du lot à comparer
        <select value={batchCompareRight} onChange={e=>{
          setBatchCompareRight(e.currentTarget.value);invalidate();
        }}>
          <option value="">Choisir une ancre fictive</option>
          {active.map(a=><option key={a.id} value={a.id}>{a.id}</option>)}
        </select>
      </label>
      <button type="button" disabled={!batchCompareLeft || !batchCompareRight ||
        batchSelectedPairs.length>=8} onClick={stageBatchPair}>
        Ajouter cette paire au lot de créations fictives
      </button>
      <p>Paires du lot choisies ({batchSelectedPairs.length}/8)</p>
      <ol>{batchSelectedPairs.map((pair,index)=><li key={index}>
        <code>{pair.left_anchor_id}</code> / <code>{pair.right_anchor_id}</code>
        <button type="button" onClick={()=>{
          setBatchSelectedPairs(old=>old.filter((_,i)=>i!==index));invalidate();
        }}>Retirer la paire du lot</button>
      </li>)}</ol>
    </section>
    <button type="button" disabled={staged.length === 0 || repairs.length > 0} onClick={prepare}>
      Vérifier le lot complet sans l'appliquer
    </button>
    {preview && <section aria-label="Prévisualisation atomique fictive" role="status">
      <p>{preview.proposed_edge_ids.length} relations cohérentes proposées,
        aucun succès de persistance.</p>
      <p>Identifiants fictifs prévus : {preview.proposed_edge_ids.join(", ")}</p>
      {batchImpact && <section aria-label="Impact avant après des nouvelles relations fictives">
        <h4>Impacts ciblés des nouvelles précédences humaines</h4>
        <p>{batchImpact.changed_relation_count} relations modifiées et
          {batchImpact.changed_witness_count} témoins modifiés parmi les paires choisies.</p>
        <ol>{batchImpact.selected_pairs.map((pair,index)=><li key={index}>
          <code>{pair.left_anchor_id}</code> / <code>{pair.right_anchor_id}</code> :
          avant {pair.before.relation}, après {pair.after.relation}.
          Témoin avant : {pair.before.witness.map(w=>w.precedence_id).join(", ")||"aucun"} ;
          témoin après : {pair.after.witness.map(w=>w.precedence_id).join(", ")||"aucun"}.
        </li>)}</ol>
        <p>Lecture seule ; aucun ordre total, aucune persistance, aucun writer.</p>
      </section>}
      <button type="button" onClick={confirm}>
        Confirmer explicitement tout le lot en mémoire
      </button>
    </section>}
    <section aria-label="Révoquer ou corriger les précédences fictives">
      <h3>Révoquer ou corriger une relation humaine — historique conservé</h3>
      <p role="note">Chaque relation est choisie explicitement. L'ancienne décision reste
        consultable ; aucune relation de remplacement n'est inférée automatiquement.
        Aucune persistance, aucun writer.</p>
      <label>Relation courante à révoquer
        <select value={repairEdge} onChange={e => { setRepairEdge(e.currentTarget.value); invalidate(); }}>
          <option value="">Choisir une relation fictive</option>
          {activeEdges.map(e => <option key={e.id} value={e.id}>
            {e.id} : {e.before_anchor_id} avant {e.after_anchor_id}
          </option>)}
        </select>
      </label>
      <label>Décision humaine
        <select value={repairMode} onChange={e => {
          setRepairMode(e.currentTarget.value as "revoke" | "replace"); invalidate();
        }}>
          <option value="revoke">Révoquer sans remplacement</option>
          <option value="replace">Révoquer et déclarer une nouvelle relation</option>
        </select>
      </label>
      <label>Motif humain de révocation
        <input value={repairWhy} maxLength={160} onChange={e => { setRepairWhy(e.currentTarget.value); invalidate(); }}/>
      </label>
      {repairMode === "replace" && <>
        <label>Nouvelle ancre antérieure
          <select value={repairBefore} onChange={e => { setRepairBefore(e.currentTarget.value); invalidate(); }}>
            <option value="">Choisir explicitement</option>
            {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
          </select>
        </label>
        <label>Nouvelle ancre postérieure
          <select value={repairAfter} onChange={e => { setRepairAfter(e.currentTarget.value); invalidate(); }}>
            <option value="">Choisir explicitement</option>
            {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
          </select>
        </label>
        <label>Motif humain du nouveau lien
          <input value={replacementWhy} maxLength={160}
            onChange={e => { setReplacementWhy(e.currentTarget.value); invalidate(); }}/>
        </label>
      </>}
      <button type="button"
        disabled={!repairEdge || !repairWhy.trim() || repairs.length >= 16 || staged.length > 0 ||
          (repairMode === "replace" && (!repairBefore || !repairAfter || !replacementWhy.trim()))}
        onClick={stageRepair}>Préparer cette révocation ou correction fictive</button>
      <h4>Décisions en attente ({repairs.length}/16)</h4>
      <ol>{repairs.map((action, index) => <li key={index}>
        {action.precedence_id} — {action.revoke_reason}
        {action.replacement ? " ; nouvelle relation " +
          action.replacement.before_anchor_id + " avant " + action.replacement.after_anchor_id : ""}
        <button type="button" onClick={() => {
          setRepairs(old => old.filter((_, i) => i !== index)); invalidate();
        }}>Retirer cette décision</button>
      </li>)}</ol>
      <h4>Comparaison ciblée facultative avant/après (lecture seule)</h4>
      <p>Deux ancres sélectionnées explicitement : aucune chronologie globale n'est déduite.
        Les témoins concernent cette paire seulement, pas l'intégralité des événements.</p>
      <label>Première ancre à comparer
        <select value={impactLeft} onChange={e => {
          setImpactLeft(e.currentTarget.value); invalidate();
        }}>
          <option value="">Aucune comparaison ciblée</option>
          {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
        </select>
      </label>
      <label>Seconde ancre à comparer
        <select value={impactRight} onChange={e => {
          setImpactRight(e.currentTarget.value); invalidate();
        }}>
          <option value="">Aucune comparaison ciblée</option>
          {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
        </select>
      </label>
      <button type="button" disabled={!impactLeft || !impactRight || selectedImpactPairs.length >= 8}
        onClick={stageImpactPair}>Ajouter cette paire aux comparaisons explicites (8 maximum)</button>
      <p>Paires choisies par l'auteur ({selectedImpactPairs.length}/8) : aucune exploration globale.</p>
      <ol>{selectedImpactPairs.map((pair,index)=><li key={index}>
        <code>{pair.left_anchor_id}</code> / <code>{pair.right_anchor_id}</code>
        <button type="button" onClick={()=>{setSelectedImpactPairs(old=>old.filter((_,i)=>i!==index));invalidate();}}>
          Retirer cette paire</button>
      </li>)}</ol>
      <button type="button" disabled={repairs.length === 0 || staged.length > 0}
        onClick={prepareRepair}>Vérifier toute la correction sans l'appliquer</button>
      {repairPreview && <section aria-label="Prévisualisation de correction fictive" role="status">
        <p>{repairPreview.revoked_edge_ids.length} relations révoquées prévues,
          {repairPreview.created_edge_ids.length} nouveaux liens prévus ;
          aucune suppression historique, aucun succès de persistance.</p>
        {selectedPairsImpact && <section aria-label="Impacts sur les paires choisies explicitement">
          <h4>Comparaisons humaines ciblées — huit paires au maximum</h4>
          <p>{selectedPairsImpact.changed_relation_count} relations modifiées,
            {selectedPairsImpact.changed_witness_count} témoins modifiés ;
            aucune chronologie totale ni écriture.</p>
          <ol>{selectedPairsImpact.selected_pairs.map((pair,index)=><li key={index}>
            <code>{pair.left_anchor_id}</code> / <code>{pair.right_anchor_id}</code> :
            avant {pair.before.relation}, après {pair.after.relation} ;
            lien modifié {pair.relation_changed ? "oui":"non"},
            témoin modifié {pair.witness_changed ? "oui":"non"}.
            <p>Témoin avant : {pair.before.witness.map(w=>w.precedence_id).join(", ")||"aucun"} ;
              témoin après : {pair.after.witness.map(w=>w.precedence_id).join(", ")||"aucun"}.</p>
          </li>)}</ol>
        </section>}
        {repairImpact && <section aria-label="Impact temporel sur deux ancres fictives">
          <h4>Impact avant/après sur la paire explicitement choisie</h4>
          <p>Ancres : <code>{repairImpact.left_anchor_id}</code> /
            <code>{repairImpact.right_anchor_id}</code></p>
          <p>Avant : {repairImpact.before.relation} ;
            après : {repairImpact.after.relation}.
            Relation modifiée : {repairImpact.relation_changed ? "oui" : "non"}.
            Témoins modifiés : {repairImpact.witness_changed ? "oui" : "non"}.</p>
          <p>Aucun ordre total, aucun calendrier converti, aucune écriture ou preuve de
            persistance. Les témoins historiques ne valent pas preuve courante.</p>
          <h5>Témoins humains avant le projet</h5>
          {repairImpact.before.witness.length ? <ol>{repairImpact.before.witness.map(w =>
            <li key={w.precedence_id}><code>{w.precedence_id}</code> :
              {w.before_anchor_id} avant {w.after_anchor_id} — {w.human_reason}</li>
          )}</ol> : <p>Aucune chaîne justificative courante avant.</p>}
          <h5>Témoins humains après le projet</h5>
          {repairImpact.after.witness.length ? <ol>{repairImpact.after.witness.map(w =>
            <li key={w.precedence_id}><code>{w.precedence_id}</code> :
              {w.before_anchor_id} avant {w.after_anchor_id} — {w.human_reason}</li>
          )}</ol> : <p>Aucune chaîne justificative courante après.</p>}
        </section>}
        <button type="button" onClick={confirmRepair}>
          Confirmer explicitement toute la correction en mémoire
        </button>
      </section>}
    </section>
    {feedback && <p role={failed ? "alert" : "status"}>{feedback}</p>}
    <p>Relations actuellement simulées : {draft.snapshot.precedences.length}.
      Historique de modifications fictives : {draft.audit.length}.</p>
  </section>;
}
