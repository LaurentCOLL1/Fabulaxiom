import { useId, useState, type ReactElement } from "react";
import type { M32ChronologyProjection, M32TimeKind } from "./M32ChronologyPreview";
import M32ChronologyPreview from "./M32ChronologyPreview";
import {
  startFictionalDraft, createFictionalAnchor, supersedeFictionalAnchor,
  createFictionalPrecedence, revokeFictionalPrecedence,
  previewFictionalPrecedence, previewFictionalCorrection,
  type FictionalDraft, type FictionalTimeInput, type FictionalRevision,
} from "./m32FictionalManualChronology";

/** Isolated browser-only fictional UX lab. No App.tsx, Tauri invoke, storage or network. */
function Lab({ initial, revisions }: {
  initial: M32ChronologyProjection;
  revisions: readonly FictionalRevision[];
}): ReactElement {
  const id = useId();
  const [draft, setDraft] = useState<FictionalDraft>(() => startFictionalDraft(initial, revisions));
  const [kind, setKind] = useState<M32TimeKind>("unknown");
  const [calendar, setCalendar] = useState("");
  const [label, setLabel] = useState("");
  const [precision, setPrecision] = useState("");
  const [sceneId, setSceneId] = useState("");
  const [revisionId, setRevisionId] = useState("");
  const [replace, setReplace] = useState("");
  const [before, setBefore] = useState("");
  const [after, setAfter] = useState("");
  const [reason, setReason] = useState("");
  const [revoke, setRevoke] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const active = draft.snapshot.anchors.filter(a => a.status === "current");
  const edges = draft.snapshot.precedences.filter(e => e.status === "current");
  const conflict = previewFictionalPrecedence(draft, before, after);
  const correctionPreview = previewFictionalCorrection(draft, replace);
  const scenes = draft.revisions.filter((r, index, all) =>
    all.findIndex(first => first.scene_id === r.scene_id) === index);
  const availableRevisions = draft.revisions.filter(r => r.scene_id === sceneId);
  const input: FictionalTimeInput = {
    kind, calendar, label, precision,
    source_scene_id: sceneId || undefined,
    source_revision_id: sceneId ? revisionId : undefined,
  };
  function apply(action: () => FictionalDraft, message: string) {
    try {
      setDraft(action());
      setError(null);
      setNotice(message);
    } catch (err) {
      setError(String(err));
      setNotice(null);
    }
  }
  return <section aria-label="Atelier manuel M3.2 exclusivement fictif">
    <h2>Atelier de chronologie — simulation sans sauvegarde</h2>
    <p role="note">Toutes les modifications restent en mémoire dans ce navigateur de test.
      Aucun univers réel, fichier SQLite, commande Tauri, migration ou canon n'est modifié.</p>
    <p><strong>Univers imaginaire :</strong> {draft.snapshot.universe_id}</p>
    <fieldset>
      <legend>Créer ou remplacer une ancre temporelle</legend>
      <label htmlFor={id + "-kind"}>Type de date</label>
      <select id={id + "-kind"} value={kind}
        onChange={e => setKind(e.currentTarget.value as M32TimeKind)}>
        <option value="unknown">Inconnue</option>
        <option value="relative">Relative</option>
        <option value="exact">Exacte dans un calendrier fictif</option>
        <option value="approximate">Approximative dans un calendrier fictif</option>
      </select>
      {(kind === "exact" || kind === "approximate") && <>
        <label htmlFor={id + "-calendar"}>Calendrier fictif</label>
        <input id={id + "-calendar"} value={calendar} maxLength={160}
          onChange={e => setCalendar(e.currentTarget.value)} />
      </>}
      {kind === "exact" && <>
        <label htmlFor={id + "-label"}>Date exprimée dans ce calendrier</label>
        <input id={id + "-label"} value={label} maxLength={160}
          onChange={e => setLabel(e.currentTarget.value)} />
      </>}
      {kind === "approximate" && <>
        <label htmlFor={id + "-precision"}>Intervalle ou incertitude</label>
        <input id={id + "-precision"} value={precision} maxLength={160}
          onChange={e => setPrecision(e.currentTarget.value)} />
      </>}
      <label htmlFor={id + "-scene"}>Scène inventée à citer (facultatif)</label>
      <select id={id + "-scene"} value={sceneId} onChange={e => {
        setSceneId(e.currentTarget.value);
        setRevisionId("");
      }}>
        <option value="">Sans nouvelle référence de scène</option>
        {scenes.map(r => <option key={r.scene_id} value={r.scene_id}>
          {draft.snapshot.narration.find(n => n.scene_id === r.scene_id)?.scene_title}
          {" — "}{r.novel_id} / {r.scene_id}
        </option>)}
      </select>
      {sceneId && <>
        <label htmlFor={id + "-revision"}>Révision exacte et immuable de cette scène</label>
        <select id={id + "-revision"} value={revisionId}
          onChange={e => setRevisionId(e.currentTarget.value)}>
          <option value="">Choisir la révision exacte</option>
          {availableRevisions.map(r => <option key={r.revision_id} value={r.revision_id}>
            {r.revision_label} — {r.revision_id}
          </option>)}
        </select>
      </>}
      <p>Aucun titre de scène ne sert d'identifiant ; aucune révision courante n'est déduite.</p>
      <button type="button" onClick={() => apply(
        () => createFictionalAnchor(draft, input), "Ancre fictive créée")}>
        Ajouter l'ancre
      </button>
      <label htmlFor={id + "-replace"}>Correction : remplacer une ancre active</label>
      <select id={id + "-replace"} value={replace}
        onChange={e => setReplace(e.currentTarget.value)}>
        <option value="">Sélectionner une ancre</option>
        {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
      </select>
      <section aria-label="Vérification de correction fictive" role="status">
        <p>{correctionPreview.reason}</p>
        {correctionPreview.historical_revision_id && <p>
          Révision historique conservée : {correctionPreview.historical_revision_id}
        </p>}
      </section>
      <button type="button" onClick={() => apply(
        () => supersedeFictionalAnchor(draft, replace, input),
        "Correction fictive enregistrée, ancienne ancre conservée")}>
        Remplacer sans effacer l'historique
      </button>
    </fieldset>
    <fieldset>
      <legend>Déclarer une relation manuelle avant/après</legend>
      <label htmlFor={id + "-before"}>Événement antérieur</label>
      <select id={id + "-before"} value={before} onChange={e => setBefore(e.currentTarget.value)}>
        <option value="">Choisir</option>
        {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
      </select>
      <label htmlFor={id + "-after"}>Événement postérieur</label>
      <select id={id + "-after"} value={after} onChange={e => setAfter(e.currentTarget.value)}>
        <option value="">Choisir</option>
        {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
      </select>
      <section aria-label="Vérification avant/après fictive" role="status">
        <p>{conflict.reason}</p>
        {conflict.witness_edge_ids.length > 0 && <p>
          Témoins historiques : {conflict.witness_edge_ids.join(", ")}
        </p>}
      </section>
      <label htmlFor={id + "-reason"}>Justification humaine fictive</label>
      <input id={id + "-reason"} value={reason} maxLength={160}
        onChange={e => setReason(e.currentTarget.value)} />
      <button type="button" onClick={() => apply(
        () => createFictionalPrecedence(draft, before, after, reason),
        "Relation fictive créée")}>
        Ajouter avant/après
      </button>
      <label htmlFor={id + "-revoke"}>Relation à révoquer (historique conservé)</label>
      <select id={id + "-revoke"} value={revoke}
        onChange={e => setRevoke(e.currentTarget.value)}>
        <option value="">Choisir</option>
        {edges.map(e => <option key={e.id} value={e.id}>
          {e.before_anchor_id} avant {e.after_anchor_id}
        </option>)}
      </select>
      <button type="button" onClick={() => apply(
        () => revokeFictionalPrecedence(draft, revoke, reason),
        "Relation fictive révoquée, historique conservé")}>
        Révoquer explicitement
      </button>
    </fieldset>
    {error && <p role="alert">Refus : {error}</p>}
    {notice && <p role="status">{notice}</p>}
    <section aria-label="Journal des modifications fictives">
      <h3>Historique inaltérable dans cette session fictive</h3>
      <ol>{draft.audit.map((entry, i) => <li key={i}>
        {entry.action} : {entry.id} — {entry.explanation}
      </li>)}</ol>
    </section>
    <M32ChronologyPreview
      expectedUniverseId={draft.snapshot.universe_id}
      snapshot={draft.snapshot} />
    <p>Ordre de narration indépendant, ordre de révélation non renseigné.
      Aucune chronologie totale inventée.</p>
  </section>;
}
export default function M32ManualChronologyLab({
  initial, revisions = [],
}: { initial: M32ChronologyProjection; revisions?: readonly FictionalRevision[] }): ReactElement {
  try {
    startFictionalDraft(initial, revisions);
  } catch {
    return <section role="alert"><h2>Atelier fictif refusé</h2>
      <p>Univers ou graphe initial incohérent. Aucune saisie autorisée.</p></section>;
  }
  return <Lab initial={initial} revisions={revisions} />;
}
