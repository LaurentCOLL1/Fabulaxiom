import { useState, type ReactElement } from "react";
import { startFictionalDraft, type FictionalDraft, type FictionalRevision } from "./m32FictionalManualChronology";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import {
  previewFictionalHumanOrderBatch, confirmFictionalHumanOrderBatch,
  type FictionalHumanOrder, type FictionalHumanOrderBatchPreview,
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
  const active = draft.snapshot.anchors.filter(a => a.status === "current");

  function invalidate() { setPreview(null); setFeedback(""); setFailed(false); }
  function stage() {
    if (staged.length >= 16) {
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
      setDraft(updated); setStaged([]); setPreview(null);
      setFeedback("Lot fictif appliqué en mémoire seulement. Aucune sauvegarde.");
      setFailed(false);
    } catch (error) {
      setPreview(null); setFeedback(error instanceof Error ? error.message : "Lot refusé.");
      setFailed(true);
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
    <button type="button" disabled={!before || !after || !reason.trim() || staged.length >= 16}
      onClick={stage}>Ajouter au lot fictif</button>
    <h3>Propositions non appliquées ({staged.length}/16)</h3>
    <ol>{staged.map((row, index) => <li key={index}>
      {row.before_anchor_id} avant {row.after_anchor_id} — {row.reason}
      <button type="button" onClick={() => {
        setStaged(old => old.filter((_, i) => i !== index)); invalidate();
      }}>Retirer cette proposition</button>
    </li>)}</ol>
    <button type="button" disabled={staged.length === 0} onClick={prepare}>
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
    {feedback && <p role={failed ? "alert" : "status"}>{feedback}</p>}
    <p>Relations actuellement simulées : {draft.snapshot.precedences.length}.
      Historique de modifications fictives : {draft.audit.length}.</p>
  </section>;
}
