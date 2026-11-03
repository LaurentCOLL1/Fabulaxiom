import { useState, type FormEvent, type ReactElement } from "react";
import type { P3Command, P3State } from "./m32P3FictionalCommandContract";
import {
  confirmP4aFictionalPlan, stageP4aFictionalPlan,
  type P4aFictionalPlan,
} from "./m32P4aFictionalReview";

/** Standalone P4a fiction-only UX. Intentionally NOT mounted by App.tsx. */
export default function M32P4aFictionalReview({
  initial, command,
}: { initial: P3State; command: P3Command }): ReactElement {
  const [state, setState] = useState(initial);
  const [proposal, setProposal] = useState<P4aFictionalPlan | null>(null);
  const [reason, setReason] = useState("");
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
  function confirm(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      if (!proposal) throw new Error("Aucune proposition fictive à confirmer");
      setState(confirmP4aFictionalPlan(state, proposal, reason));
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
      </form>
    </section>}
    <p role="status">{message}</p>
    <p>Admission du writer de production : STOP_UNAVAILABLE.</p>
  </section>;
}
