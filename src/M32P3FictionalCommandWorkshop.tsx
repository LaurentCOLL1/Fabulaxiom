import { useId, useState, type FormEvent, type ReactElement } from "react";
import M32ChronologyPreview from "./M32ChronologyPreview";
import type { M32ChronologyProjection, M32TimeKind } from "./M32ChronologyPreview";
import type { FictionalRevision } from "./m32FictionalManualChronology";
import {
  P3_NEW_ANCHOR, applyP3FictionalCommand,
  readP3FictionalSnapshot, startP3FictionalState,
  type P3Command,
} from "./m32P3FictionalCommandContract";

/** P3a: browser-only rehearsal of the P2b command vocabulary.
 * NOT a Rust bridge or production application route. No IPC, fetch,
 * storage, SQLite, real user data, persistence or inferred chronology.
 */
function FictionalPanel({ initial, revisions }: {
  initial: M32ChronologyProjection;
  revisions: readonly FictionalRevision[];
}): ReactElement {
  const id = useId();
  const [state, setState] = useState(() => startP3FictionalState(initial, revisions));
  const [kind, setKind] = useState<M32TimeKind>("unknown");
  const [calendar, setCalendar] = useState("");
  const [label, setLabel] = useState("");
  const [precision, setPrecision] = useState("");
  const [revision, setRevision] = useState("");
  const [relativeTo, setRelativeTo] = useState("");
  const [direction, setDirection] = useState<"none" | "existing_before_new" | "new_before_existing">("none");
  const [reason, setReason] = useState("");
  const [firstAnchor, setFirstAnchor] = useState("");
  const [secondAnchor, setSecondAnchor] = useState("");
  const [standaloneReason, setStandaloneReason] = useState("");
  const [message, setMessage] = useState("Aucune commande lancée.");
  const [error, setError] = useState(false);
  const snapshot = readP3FictionalSnapshot(state, initial.universe_id);
  const active = snapshot.anchors.filter(a => a.status === "current");
  function execute(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      const historical = revisions.find(r => r.revision_id === revision);
      if (revision && !historical) throw new Error("Révision historique inconnue");
      if (direction !== "none" && !relativeTo) throw new Error("Choisir une ancre existante");
      const relation = direction === "none" ? null : {
        before_anchor_id: direction === "existing_before_new" ? relativeTo : P3_NEW_ANCHOR,
        after_anchor_id: direction === "existing_before_new" ? P3_NEW_ANCHOR : relativeTo,
        reason,
      };
      const command: P3Command = {
        kind: "create_anchor_with_optional_relation",
        universe_id: initial.universe_id,
        time: {
          kind, calendar, label, precision,
          source_revision_id: historical?.revision_id ?? null,
          source_scene_id: historical?.scene_id ?? null,
        },
        relation,
      };
      const next = applyP3FictionalCommand(state, command);
      setState(next);
      setError(false);
      setMessage("Commande fictive acceptée en mémoire : aucune écriture SQLite.");
    } catch (cause) {
      setError(true);
      setMessage(cause instanceof Error ? cause.message : "Commande fictive refusée");
    }
  }
  function executeStandalone(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      if (!firstAnchor || !secondAnchor || firstAnchor === secondAnchor) {
        throw new Error("Choisir deux ancres distinctes du même Univers fictif");
      }
      const next = applyP3FictionalCommand(state, {
        kind: "create_precedence",
        universe_id: initial.universe_id,
        relation: {
          before_anchor_id: firstAnchor,
          after_anchor_id: secondAnchor,
          reason: standaloneReason,
        },
      });
      setState(next);
      setError(false);
      setMessage("Lien fictif accepté en mémoire ; aucune sauvegarde ni déduction automatique.");
      setStandaloneReason("");
    } catch (cause) {
      setError(true);
      setMessage(cause instanceof Error ? cause.message : "Lien fictif refusé");
    }
  }
  return <section aria-label="P3c atelier de commandes de chronologie fictive">
    <h2>Créer une date dans le monde fictif — contrat P3a</h2>
    <p><strong>Simulation navigateur exclusivement.</strong> Cette interface
      ne communique pas avec Rust et ne sauvegarde aucune modification.</p>
    <p>Univers explicite : <code>{snapshot.universe_id}</code>.
      Temps du monde, narration et révélation au lecteur restent distincts.</p>
    <form aria-label="Commande temporelle fictive" onSubmit={execute}>
      <label htmlFor={id + "-kind"}>Nature du temps dans le monde</label>
      <select id={id + "-kind"} value={kind}
        onChange={e => setKind(e.currentTarget.value as M32TimeKind)}>
        <option value="unknown">Inconnue</option>
        <option value="relative">Relative</option>
        <option value="approximate">Approximative</option>
        <option value="exact">Exacte dans le calendrier fictif</option>
      </select>
      {(kind === "exact" || kind === "approximate") && <>
        <label htmlFor={id + "-calendar"}>Calendrier inventé</label>
        <input id={id + "-calendar"} value={calendar}
          maxLength={160} onChange={e => setCalendar(e.currentTarget.value)} />
      </>}
      {kind === "exact" && <>
        <label htmlFor={id + "-label"}>Étiquette du temps exact fictif</label>
        <input id={id + "-label"} value={label}
          maxLength={160} onChange={e => setLabel(e.currentTarget.value)} />
      </>}
      {kind === "approximate" && <>
        <label htmlFor={id + "-precision"}>Précision fictive</label>
        <input id={id + "-precision"} value={precision}
          maxLength={160} onChange={e => setPrecision(e.currentTarget.value)} />
      </>}
      <label htmlFor={id + "-revision"}>Révision narrative historique (choix manuel)</label>
      <select id={id + "-revision"} value={revision}
        onChange={e => setRevision(e.currentTarget.value)}>
        <option value="">Aucune révision liée</option>
        {revisions.filter(r => r.universe_id === snapshot.universe_id)
          .map(r => <option key={r.revision_id} value={r.revision_id}>
            {r.revision_label} — {r.revision_id}
          </option>)}
      </select>
      <label htmlFor={id + "-direction"}>Lien temporel facultatif avec l'ancre créée</label>
      <select id={id + "-direction"} value={direction}
        onChange={e => setDirection(e.currentTarget.value as typeof direction)}>
        <option value="none">Sans lien : ordre indéterminé</option>
        <option value="existing_before_new">Une ancre existante précède la nouvelle</option>
        <option value="new_before_existing">La nouvelle précède une ancre existante</option>
      </select>
      {direction !== "none" && <>
        <label htmlFor={id + "-relative"}>Ancre existante explicitement choisie</label>
        <select id={id + "-relative"} value={relativeTo}
          onChange={e => setRelativeTo(e.currentTarget.value)}>
          <option value="">Choisir une ancre</option>
          {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
        </select>
        <label htmlFor={id + "-reason"}>Justification humaine du lien</label>
        <input id={id + "-reason"} value={reason} maxLength={160}
          onChange={e => setReason(e.currentTarget.value)} />
      </>}
      <button type="submit">Exécuter la commande fictive en mémoire</button>
      <button type="button" onClick={() => {
        setState(startP3FictionalState(initial, revisions));
        setError(false); setMessage("Données fictives réinitialisées.");
        setRelativeTo(""); setDirection("none"); setReason(""); setRevision("");
        setFirstAnchor(""); setSecondAnchor(""); setStandaloneReason("");
      }}>Réinitialiser les données fictives</button>
    </form>
    <section aria-label="P3c lien temporel entre deux ancres existantes">
      <h3>Relier deux dates déjà créées</h3>
      <p>Le lien avant / après est une décision humaine. Sans lien, leur ordre
        reste inconnu ; la disposition de la liste ne signifie pas un ordre temporel.</p>
      <form aria-label="Relation autonome entre ancres fictives" onSubmit={executeStandalone}>
        <label htmlFor={id + "-before"}>Ancre précédant l'autre</label>
        <select id={id + "-before"} value={firstAnchor}
          onChange={e => setFirstAnchor(e.currentTarget.value)}>
          <option value="">Choisir une ancre</option>
          {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
        </select>
        <label htmlFor={id + "-after"}>Ancre suivante</label>
        <select id={id + "-after"} value={secondAnchor}
          onChange={e => setSecondAnchor(e.currentTarget.value)}>
          <option value="">Choisir une ancre</option>
          {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
        </select>
        <label htmlFor={id + "-why"}>Raison humaine explicite</label>
        <input id={id + "-why"} value={standaloneReason} maxLength={160}
          onChange={e => setStandaloneReason(e.currentTarget.value)} />
        <button type="submit">Créer le lien fictif sans nouvelle date</button>
      </form>
    </section>
    <p role={error ? "alert" : "status"}>{message}</p>
    <section aria-label="Résultat des commandes fictives">
      <h3>État local non enregistré</h3>
      <p>{state.commands_committed} commande(s), {active.length} ancre(s) en vigueur,
        {snapshot.precedences.filter(e => e.status === "current").length} relation(s) explicites.</p>
      <ul>{active.slice(-8).map(a => <li key={a.id}>
        <code>{a.id}</code> — {a.time_kind} —
        révision source : <code>{a.source_revision_id ?? "aucune"}</code>
      </li>)}</ul>
      <ol>{snapshot.precedences.filter(e => e.status === "current")
        .slice(-8).map(e => <li key={e.id}>
          <code>{e.before_anchor_id}</code> avant <code>{e.after_anchor_id}</code> :
          {" "}{e.reason}
        </li>)}</ol>
    </section>
    <M32ChronologyPreview expectedUniverseId={snapshot.universe_id} snapshot={snapshot} />
    <p>Les commandes de cette page sont simulées par un réducteur TypeScript.
      L'acteur Rust P2b reste un test isolé, non raccordé à cette interface.</p>
  </section>;
}
export default function M32P3FictionalCommandWorkshop({
  initial, revisions,
}: {
  initial: M32ChronologyProjection;
  revisions: readonly FictionalRevision[];
}): ReactElement {
  try {
    startP3FictionalState(initial, revisions);
  } catch {
    return <section role="alert" aria-label="Atelier P3a refusé">
      Données fictives invalides ou Univers incompatible. Aucune commande possible.
    </section>;
  }
  return <FictionalPanel initial={initial} revisions={revisions} />;
}
