import { useState, type ReactElement } from "react";
import { startFictionalDraft, type FictionalDraft, type FictionalRevision } from "./m32FictionalManualChronology";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import {
  previewFictionalHumanOrderBatch, confirmFictionalHumanOrderBatch,
  type FictionalHumanOrder, type FictionalHumanOrderBatchPreview,
  previewFictionalHumanOrderRepair, confirmFictionalHumanOrderRepair,
  type FictionalHumanOrderRepair, type FictionalHumanOrderRepairPreview,
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
  const activeEdges = draft.snapshot.precedences.filter(e => e.status === "current");
  const active = draft.snapshot.anchors.filter(a => a.status === "current");

  function invalidate() { setPreview(null); setRepairPreview(null); setFeedback(""); setFailed(false); }
  function stage() {
    if (staged.length >= 16 || repairs.length > 0) {
      setFeedback("Maximum 16 propositions fictives."); setFailed(true); return;
    }
    setStaged(old => [...old, { before_anchor_id: before, after_anchor_id: after, reason }]);
    setBefore(""); setAfter(""); setReason(""); invalidate();
  }
  function prepare() {
    try {
      const candidate = previewFictionalHumanOrderBatch(draft, staged);
      setPreview(candidate); setFeedback("Lot fictif cohérent ; aucune modification appliquée.");
      setFailed(false);
    } catch (error) {
      setPreview(null); setFeedback(error instanceof Error ? error.message : "Lot refusé.");
      setFailed(true);
    }
  }
  function confirm() {
    if (!preview) return;
    try {
      const updated = confirmFictionalHumanOrderBatch(draft, staged, preview, true);
      setDraft(updated); setStaged([]); setRepairs([]); setPreview(null); setRepairPreview(null);
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
  function prepareRepair() {
    try {
      const candidate = previewFictionalHumanOrderRepair(draft, repairs);
      setRepairPreview(candidate); setPreview(null);
      setFeedback("Révocation/correction fictive cohérente ; rien appliqué."); setFailed(false);
    } catch (error) {
      setRepairPreview(null);
      setFeedback(error instanceof Error ? error.message : "Correction fictive refusée."); setFailed(true);
    }
  }
  function confirmRepair() {
    if (!repairPreview) return;
    try {
      const updated = confirmFictionalHumanOrderRepair(draft, repairs, repairPreview, true);
      setDraft(updated); setRepairs([]); setStaged([]); setRepairPreview(null); setPreview(null);
      setRepairEdge(""); setFeedback("Historique conservé : appliqué en RAM. Aucune sauvegarde.");
      setFailed(false);
    } catch (error) {
      setRepairPreview(null);
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
    <button type="button" disabled={staged.length === 0 || repairs.length > 0} onClick={prepare}>
      Vérifier le lot complet sans l'appliquer
    </button>
    {preview && <section aria-label="Prévisualisation atomique fictive" role="status">
      <p>{preview.proposed_edge_ids.length} relations cohérentes proposées,
        aucun succès de persistance.</p>
      <p>Identifiants fictifs prévus : {preview.proposed_edge_ids.join(", ")}</p>
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
      <button type="button" disabled={repairs.length === 0 || staged.length > 0}
        onClick={prepareRepair}>Vérifier toute la correction sans l'appliquer</button>
      {repairPreview && <section aria-label="Prévisualisation de correction fictive" role="status">
        <p>{repairPreview.revoked_edge_ids.length} relations révoquées prévues,
          {repairPreview.created_edge_ids.length} nouveaux liens prévus ;
          aucune suppression historique, aucun succès de persistance.</p>
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
