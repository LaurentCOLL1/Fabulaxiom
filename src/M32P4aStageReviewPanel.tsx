import { useState, type FormEvent, type ReactElement } from "react";
import type { P3Command, P3State } from "./m32P3FictionalCommandContract";
import {
  confirmP4cFictionalPlanWithReceipt, stageP4aFictionalPlan,
  type P4aFictionalPlan, type P4cFictionalDecisionReceipt,
} from "./m32P4aFictionalReview";

/** Standalone P4a fiction-only UX. Intentionally NOT mounted by App.tsx. */
export default function M32P4aFictionalReview({
  initial, command,
}: { initial: P3State; command: P3Command }): ReactElement {
  const [state, setState] = useState(initial);
  const [proposal, setProposal] = useState<P4aFictionalPlan | null>(null);
  const [reason, setReason] = useState("");
  const [receipts, setReceipts] = useState<readonly P4cFictionalDecisionReceipt[]>([]);
  const [message, setMessage] = useState("Aucune proposition prévisualisée.");
  function stage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      setProposal(stageP4aFictionalPlan(state, command));
      setMessage("Prévisualisation créée ; aucune modification acceptée.");
    } catch (e) {
      setProposal(null);
      setMessage(e instanceof Error ? e.message : "Proposition fictive refusée.");
    }
  }
  function cancel() {
    setProposal(null);
    setReason("");
    setMessage("Prévisualisation annulée ; aucune décision fictive acceptée.");
  }
  function confirm(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      if (!proposal) throw new Error("Aucune proposition fictive à confirmer");
      const accepted = confirmP4cFictionalPlanWithReceipt(state, proposal, reason);
      setState(accepted.state);
      setReceipts(previous => [...previous, accepted.receipt]);
      setProposal(null);
      setReason("");
      setMessage("Décision fictive confirmée en RAM ; aucune écriture Rust/SQLite.");
    } catch (e) {
      setMessage(e instanceof Error ? e.message : "Confirmation fictive refusée.");
    }
  }
  return <section aria-label="P4a revue humaine fictive isolée">
    <h2>P4a — vérifier avant de confirmer une décision fictive</h2>
    <p>Préparation du parcours produit, sans admission P4 ni écrivain réel.
       Aucune commande Tauri, aucun disque, aucune sauvegarde.</p>
    <p>Univers inventé : <code>{state.draft.snapshot.universe_id}</code></p>
    <p>Décisions fictives confirmées en mémoire : {state.commands_committed}</p>
    <form onSubmit={stage} aria-label="Prévisualiser la proposition fictive">
      <button type="submit">Prévisualiser sans modifier</button>
    </form>
    {proposal && <section aria-label="Différence fictive avant après">
      <h3>Avant / après — prévisualisation uniquement</h3>
      <p>Ancres ajoutées : {proposal.changes.created_anchor_ids.join(", ") || "aucune"}</p>
      <p>Ancres remplacées : {proposal.changes.superseded_anchor_ids.join(", ") || "aucune"}</p>
      <p>Liens ajoutés : {proposal.changes.created_precedence_ids.join(", ") || "aucun"}</p>
      <p>Liens révoqués : {proposal.changes.revoked_precedence_ids.join(", ") || "aucun"}</p>
      <p>Révisions source conservées : {proposal.changes.historical_source_revision_ids.join(", ") || "aucune"}</p>
      <p>Ordre de narration inchangé. Révélation au lecteur non renseignée.</p>
      <form onSubmit={confirm} aria-label="Confirmer la décision fictive">
        <label htmlFor="p4a-human-reason">Motif humain de confirmation</label>
        <input id="p4a-human-reason" maxLength={160} value={reason}
          onChange={e => setReason(e.currentTarget.value)} />
        <button type="submit">Confirmer en mémoire fictive uniquement</button>
        <button type="button" onClick={cancel}>Annuler la prévisualisation fictive</button>
      </form>
    </section>}
    <section aria-label="Journal des confirmations fictives en mémoire">
      <h3>Décisions confirmées dans cette session fictive ({receipts.length})</h3>
      <p>Journal visuel en RAM uniquement : ni identité vérifiée, ni signature, ni sauvegarde.</p>
      <ol>{receipts.map((entry, index) => <li key={index}>
        Décision {entry.after_commands} — {entry.command_kind} — motif humain : {entry.human_reason}
        {" — univers : "}{entry.universe_id}
      </li>)}</ol>
    </section>
    <p role="status">{message}</p>
    <p>Admission du writer de production : STOP_UNAVAILABLE.</p>
  </section>;
}
