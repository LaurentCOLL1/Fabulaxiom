import M32FictionalPersistenceNotice from "./m32FictionalPersistenceNotice";
import { useId, useState, type ReactElement } from "react";
import type { M32ChronologyProjection, M32TimeKind } from "./M32ChronologyPreview";
import M32ChronologyPreview from "./M32ChronologyPreview";
import M32WorldOrderComparison from "./M32WorldOrderComparison";
import { previewFictionalRevocationImpact } from "./m32FictionalRevocationImpact";
import { previewFictionalAnchorSupersession, confirmFictionalAnchorSupersession,
  type FictionalAnchorSupersessionReview, type FictionalSourceTransition
} from "./m32FictionalAnchorSupersessionPreview";
import {
  startFictionalDraft, createFictionalAnchor,
  createFictionalPrecedence, revokeFictionalPrecedence,
  previewFictionalPrecedence, previewFictionalCorrection, previewFictionalThreeOrders,
  previewFictionalSceneRevisionWorldOrder,
  type FictionalDraft, type FictionalTimeInput, type FictionalRevision,
} from "./m32FictionalManualChronology";

const fictionalSourceTransitionText: Record<FictionalSourceTransition,string> = {
  none: "Aucune source historique ni nouvelle.",
  linked: "Nouvelle source fictive liée à une révision exacte.",
  retained: "Source historique exacte conservée.",
  replaced: "Source historique remplacée explicitement ; ancienne source conservée.",
  detached: "Source proposée détachée ; source historique conservée.",
};
/** Pure, scope-local UI preflight: never treat a corrected historical anchor as current. */
export function fictionalSelectionIsHistorical(
  activeIds: readonly string[], left: string, right: string,
): boolean {
  const available = new Set(activeIds);
  return [left, right].some(id => id !== "" && !available.has(id));
}

/** Separate catalogue of names, local to the invented laboratory only. */
export type FictionalCalendarEntry = Readonly<{ id: string; name: string }>;
export function addFictionalCalendar(catalogue: readonly FictionalCalendarEntry[], raw: string): readonly FictionalCalendarEntry[] {
  const name = raw.trim().normalize("NFC");
  if (!name || name.length > 160 || /[\u0000-\u001f\u007f]/.test(name))
    throw Error("Nom de calendrier fictif invalide.");
  if (catalogue.length >= 128) throw Error("Catalogue fictif complet.");
  if (catalogue.some(entry => entry.name.normalize("NFC").toLowerCase() === name.toLowerCase()))
    throw Error("Calendrier fictif déjà créé.");
  const id = "fiction-calendar-" + String(catalogue.length + 1).padStart(4, "0");
  if (catalogue.some(entry => entry.id === id)) throw Error("Identifiant fictif déjà utilisé.");
  return [...catalogue, { id, name }];
}
export function selectFictionalCalendar(catalogue: readonly FictionalCalendarEntry[], id: string): string {
  const matches = catalogue.filter(entry => entry.id === id);
  if (matches.length !== 1) throw Error("Calendrier fictif absent ou ambigu.");
  return matches[0].name;
}

/** Isolated browser-only fictional UX lab. No App.tsx, Tauri invoke, storage or network. */
function Lab({ initial, revisions }: {
  initial: M32ChronologyProjection;
  revisions: readonly FictionalRevision[];
}): ReactElement {
  const id = useId();
  const [draft, setDraft] = useState<FictionalDraft>(() => startFictionalDraft(initial, revisions));
  const [kind, setKind] = useState<M32TimeKind>("unknown");
  const [calendar, setCalendar] = useState("");
  const [calendarCatalogue, setCalendarCatalogue] = useState<readonly FictionalCalendarEntry[]>([]);
  const [newCalendarName, setNewCalendarName] = useState("");
  const [calendarFeedback, setCalendarFeedback] = useState("");
  const [calendarError, setCalendarError] = useState(false);
  function createCalendar() {
    try {
      setCalendarCatalogue(addFictionalCalendar(calendarCatalogue, newCalendarName));
      setNewCalendarName("");
      setCalendarError(false);
      setCalendarFeedback("Calendrier créé en mémoire ; aucune date ni ancre créée.");
    } catch (err) {
      setCalendarError(true);
      setCalendarFeedback(String(err));
    }
  }
  function chooseCalendar(calendarId: string) {
    try {
      setCalendar(selectFictionalCalendar(calendarCatalogue, calendarId));
      setSupersessionPreview(null);
      setCalendarError(false);
      setCalendarFeedback("Calendrier choisi explicitement pour la prochaine saisie.");
    } catch (err) {
      setCalendarError(true);
      setCalendarFeedback(String(err));
    }
  }
  const [label, setLabel] = useState("");
  const [precision, setPrecision] = useState("");
  const [sceneId, setSceneId] = useState("");
  const [revisionId, setRevisionId] = useState("");
  const [replace, setReplace] = useState("");
  const [detachSource, setDetachSource] = useState(false);
  const [supersessionPreview, setSupersessionPreview] = useState<FictionalAnchorSupersessionReview|null>(null);
  const [before, setBefore] = useState("");
  const [after, setAfter] = useState("");
  const [reason, setReason] = useState("");
  const [revoke, setRevoke] = useState("");
  const [revokeReason, setRevokeReason] = useState("");
  const [firstScene, setFirstScene] = useState("");
  const [secondScene, setSecondScene] = useState("");
  const [firstWorldRevision, setFirstWorldRevision] = useState("");
  const [secondWorldRevision, setSecondWorldRevision] = useState("");
  const [worldLeft, setWorldLeft] = useState("");
  const [worldRight, setWorldRight] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const active = draft.snapshot.anchors.filter(a => a.status === "current");
  const selectionIsHistorical = fictionalSelectionIsHistorical(
    active.map(anchor => anchor.id), worldLeft, worldRight);
  const edges = draft.snapshot.precedences.filter(e => e.status === "current");
  const conflict = previewFictionalPrecedence(draft, before, after);
  const correctionPreview = previewFictionalCorrection(draft, replace);
  const revocationImpact = previewFictionalRevocationImpact(draft, revoke);
  const threeOrders = previewFictionalThreeOrders(draft, firstScene, secondScene);
  const sceneWorld = previewFictionalSceneRevisionWorldOrder(
    draft, firstScene, firstWorldRevision, secondScene, secondWorldRevision);
  const scenes = draft.revisions.filter((r, index, all) =>
    all.findIndex(first => first.scene_id === r.scene_id) === index);
  const availableRevisions = draft.revisions.filter(r => r.scene_id === sceneId);
  const input: FictionalTimeInput = {
    kind, calendar, label, precision,
    source_scene_id: sceneId || undefined,
    source_revision_id: sceneId ? revisionId : undefined,
  };
  // Only the deliberate correction can detach; creating an anchor keeps
  // its independently authored scene/revision selection.
  const correctionInput: FictionalTimeInput = detachSource && replace
    ? {...input, source_scene_id:null, source_revision_id:null}
    : input;
  function apply(action: () => FictionalDraft, message: string, onSuccess?: () => void) {
    try {
      const updated = action();
      setDraft(updated);
      // Reset correction-specific controls only after a successful RAM action.
      onSuccess?.();
      setSupersessionPreview(null);
      setError(null);
      setNotice(message);
    } catch (err) {
      // A refused fictional action must not leave a previous confirmation
      // visually actionable; do not mutate the draft on this failure.
      setSupersessionPreview(null);
      setError(String(err));
      setNotice(null);
    }
  }
  function reviewCorrection() {
    try {
      const candidate = previewFictionalAnchorSupersession(draft,replace,correctionInput);
      setSupersessionPreview(candidate);
      setNotice("Prévisualisation fictive seulement ; aucune correction appliquée.");
      setError(null);
    } catch(err) {
      setSupersessionPreview(null);
      setError(String(err));setNotice(null);
    }
  }
  return <section aria-label="Atelier manuel M3.2 exclusivement fictif">
    <h2>Atelier de chronologie — simulation sans sauvegarde</h2>
    <M32FictionalPersistenceNotice />
    <p role="note">Toutes les modifications restent en mémoire dans ce navigateur de test.
      Aucun univers réel, fichier SQLite, commande Tauri, migration ou canon n'est modifié.</p>
    <p><strong>Univers imaginaire :</strong> {draft.snapshot.universe_id}</p>
    <fieldset>
      <legend>Créer un calendrier fictif</legend>
      <p>Catalogue local de noms, sans conversion de dates ni création automatique d'événement.</p>
      <label htmlFor={id + "-new-calendar"}>Nom du nouveau calendrier</label>
      <input id={id + "-new-calendar"} value={newCalendarName} maxLength={160}
        onChange={e => setNewCalendarName(e.currentTarget.value)} />
      <button type="button" onClick={createCalendar}>Créer le calendrier en mémoire</button>
      {calendarCatalogue.length === 0 && <p>Aucun calendrier créé dans ce catalogue.</p>}
      <ul aria-label="Calendriers fictifs créés">
        {calendarCatalogue.map(entry => <li key={entry.id}>
          {entry.name} — {entry.id}{" "}
          <button type="button" onClick={() => chooseCalendar(entry.id)}>
            Choisir {entry.name} pour la saisie
          </button>
        </li>)}
      </ul>
      {calendarFeedback && <p role={calendarError ? "alert" : "status"}>{calendarFeedback}</p>}
    </fieldset>
    <fieldset>
      <legend>Créer ou remplacer une ancre temporelle</legend>
      <label htmlFor={id + "-kind"}>Type de date</label>
      <select id={id + "-kind"} value={kind}
        onChange={e => {setKind(e.currentTarget.value as M32TimeKind);setSupersessionPreview(null);}}>
        <option value="unknown">Inconnue</option>
        <option value="relative">Relative</option>
        <option value="exact">Exacte dans un calendrier fictif</option>
        <option value="approximate">Approximative dans un calendrier fictif</option>
      </select>
      {(kind === "exact" || kind === "approximate") && <>
        <label htmlFor={id + "-calendar"}>Calendrier fictif</label>
        <input id={id + "-calendar"} value={calendar} maxLength={160}
          onChange={e => {setCalendar(e.currentTarget.value);setSupersessionPreview(null);}} />
      </>}
      {kind === "exact" && <>
        <label htmlFor={id + "-label"}>Date exprimée dans ce calendrier</label>
        <input id={id + "-label"} value={label} maxLength={160}
          onChange={e => {setLabel(e.currentTarget.value);setSupersessionPreview(null);}} />
      </>}
      {kind === "approximate" && <>
        <label htmlFor={id + "-precision"}>Intervalle ou incertitude</label>
        <input id={id + "-precision"} value={precision} maxLength={160}
          onChange={e => {setPrecision(e.currentTarget.value);setSupersessionPreview(null);}} />
      </>}
      <label htmlFor={id + "-scene"}>Scène inventée à citer (facultatif)</label>
      <select id={id + "-scene"} value={sceneId} onChange={e => {
        setSceneId(e.currentTarget.value);
        setRevisionId("");
        setDetachSource(false);
        setSupersessionPreview(null);
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
          onChange={e => {setRevisionId(e.currentTarget.value);setSupersessionPreview(null);}}>
          <option value="">Choisir la révision exacte</option>
          {availableRevisions.map(r => <option key={r.revision_id} value={r.revision_id}>
            {r.revision_label} — {r.revision_id}
          </option>)}
        </select>
      </>}
      <p>Aucun titre de scène ne sert d'identifiant ; aucune révision courante n'est déduite.</p>
      <p>Les scènes peuvent appartenir à des romans différents du même Univers ; leur position de narration ne prouve aucune précédence dans le monde ni révélation au lecteur.</p>
      <button type="button" onClick={() => apply(
        () => createFictionalAnchor(draft, input), "Ancre fictive créée")}>
        Ajouter l'ancre
      </button>
      <label htmlFor={id + "-replace"}>Correction : remplacer une ancre active</label>
      <select id={id + "-replace"} value={replace}
        onChange={e => {
          setReplace(e.currentTarget.value);
          // A new correction target must never inherit a different target's
          // proposed immutable scene/revision source.
          setSceneId("");
          setRevisionId("");
          setDetachSource(false);
          setSupersessionPreview(null);
        }}>
        <option value="">Sélectionner une ancre</option>
        {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
      </select>
      <p>Changer d'ancre à corriger efface la sélection de source proposée
        (scène et révision exactes) et impose une nouvelle prévisualisation.
        Aucune version historique n'est modifiée.</p>
      <p>Après confirmation fictive réussie, la cible et la source proposées
        sont effacées ; la version historique reste consultable.</p>
      <label htmlFor={id + "-detach-source"}>
        <input id={id + "-detach-source"} type="checkbox" checked={detachSource}
          disabled={!replace} onChange={e=>{
            const detach = e.currentTarget.checked;
            setDetachSource(detach);
            if (detach) {
              setSceneId("");
              setRevisionId("");
            }
            setSupersessionPreview(null);
          }} />
        Détacher explicitement la source historique de la version proposée
      </label>
      <p>Ce choix ne modifie pas l'ancre historique. Détacher efface seulement
        la sélection de scène/révision proposée ; sélectionner une nouvelle scène annule
        automatiquement le détachement. Sans choix explicite, la révision initiale est
        conservée.</p>
      <section aria-label="Vérification de correction fictive" role="status">
        <p>{correctionPreview.reason}</p>
        {correctionPreview.active_edge_ids.length > 0 && <section
          role="status" aria-label="Relations humaines actives empêchant la correction">
          <p>Ces liens humains fictifs actifs empêchent la correction de l'ancre.
            Chacun doit être révoqué explicitement, avec justification humaine.
            Cette liste n'effectue aucune révocation automatique.</p>
          <ul>{correctionPreview.active_edge_ids.map(edgeId => {
            const edge = edges.find(e => e.id === edgeId);
            return <li key={edgeId}><code>{edgeId}</code> : {edge
              ? <><code>{edge.before_anchor_id}</code> avant
                   <code>{edge.after_anchor_id}</code> — {edge.reason}
                   <button type="button" onClick={() => {
                     setRevoke(edgeId);
                     setRevokeReason("");
                   }}>Préparer la révocation de {edgeId} (sans l'appliquer)</button></>
              : "relation non retrouvée : correction refusée"}</li>;
          })}</ul>
        </section>}
        {correctionPreview.historical_revision_id && <p>
          Révision historique conservée : {correctionPreview.historical_revision_id}
        </p>}
      </section>
      <button type="button" disabled={!replace} onClick={reviewCorrection}>
        Prévisualiser la correction sans l'appliquer
      </button>
      <p>Une action fictive refusée annule la prévisualisation précédente.
        Une nouvelle vérification est nécessaire avant confirmation.</p>
      {supersessionPreview && <section role="status"
          aria-label="Avant après correction d'ancre fictive">
        <h3>Correction proposée — données fictives non enregistrées</h3>
        <p>Version historique conservée :
          <code>{supersessionPreview.old_anchor.id}</code> —
          {supersessionPreview.old_anchor.time_kind} —
          {supersessionPreview.old_anchor.calendar_name ?? "sans calendrier"}.</p>
        <p>Libellé historique :
          {supersessionPreview.old_anchor.fictional_label ?? "aucun"} ;
          précision historique :
          {supersessionPreview.old_anchor.precision_text ?? "aucune"}.</p>
        <p>Nouvelle version envisagée :
          <code>{supersessionPreview.new_anchor.id}</code> —
          {supersessionPreview.new_anchor.time_kind} —
          {supersessionPreview.new_anchor.calendar_name ?? "sans calendrier"}.</p>
        <p>Libellé proposé :
          {supersessionPreview.new_anchor.fictional_label ?? "aucun"} ;
          précision proposée :
          {supersessionPreview.new_anchor.precision_text ?? "aucune"}.</p>
        <p>Décision de provenance : {fictionalSourceTransitionText[
          supersessionPreview.source_transition]}</p>
        <p>Source historique initiale :
          {supersessionPreview.old_anchor.source_revision_id ?? "aucune"} ;
          source envisagée :
          {supersessionPreview.new_anchor.source_revision_id ?? "aucune"}.</p>
        <p>Roman et scène historiques :
          <code>{supersessionPreview.old_source?.novel_id ?? "aucun"}</code> /
          <code>{supersessionPreview.old_source?.scene_id ?? "aucune"}</code>.</p>
        <p>Roman et scène proposés :
          <code>{supersessionPreview.new_source?.novel_id ?? "aucun"}</code> /
          <code>{supersessionPreview.new_source?.scene_id ?? "aucune"}</code>.</p>
        {supersessionPreview.old_source && !supersessionPreview.new_source && <p>
          Détachement explicite de la source proposée ; la révision historique reste conservée.
        </p>}
        <p>Ni date grégorienne déduite, ni ordre total, ni écriture.</p>
        <button type="button" onClick={() => apply(
          () => confirmFictionalAnchorSupersession(
            draft,replace,correctionInput,supersessionPreview,true),
          "Correction fictive confirmée en mémoire ; aucune sauvegarde.",
          () => {
            setReplace("");
            setSceneId("");
            setRevisionId("");
            setDetachSource(false);
          })}>
          Confirmer la correction fictive en RAM
        </button>
      </section>}
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
        onChange={e => {setRevoke(e.currentTarget.value);setRevokeReason("");}}>
        <option value="">Choisir</option>
        {edges.map(e => <option key={e.id} value={e.id}>
          {e.before_anchor_id} avant {e.after_anchor_id}
        </option>)}
      </select>
      <label htmlFor={id + "-revoke-reason"}>Justification de révocation fictive</label>
      <input id={id + "-revoke-reason"} value={revokeReason} maxLength={160}
        onChange={e => setRevokeReason(e.currentTarget.value)} />
      <p>Une révocation exige une nouvelle justification distincte de celle
        utilisée pour déclarer une relation ; aucune révocation n'est automatique.</p>
      <section role="status" aria-label="Prévisualisation de révocation fictive">
        <p>{revocationImpact.reason}</p>
        {revocationImpact.witness_after.length > 0 && <p>
          Autre chemin humain encore actif : {revocationImpact.witness_after.join(", ")}
        </p>}
        <p>Cette prévisualisation ne révoque rien et n'invente aucune date.</p>
      </section>
      <button type="button" onClick={() => apply(
        () => revokeFictionalPrecedence(draft, revoke, revokeReason),
        "Relation fictive révoquée, historique conservé",
        () => {setRevoke("");setRevokeReason("");})}>
        Révoquer explicitement
      </button>
    </fieldset>
    <fieldset>
      <legend>Comparer les trois ordres — fictif</legend>
      <p>Une scène du manuscrit n'est ni une date du monde ni une révélation au lecteur.</p>
      <label htmlFor={id + "-compare-first"}>Première scène à comparer</label>
      <select id={id + "-compare-first"} value={firstScene}
        onChange={e => { setFirstScene(e.currentTarget.value); setFirstWorldRevision(""); }}>
        <option value="">Choisir la première scène</option>
        {draft.snapshot.narration.map(s => <option key={s.scene_id} value={s.scene_id}>
          {s.novel_title} — {s.scene_title} ({s.scene_id})
        </option>)}
      </select>
      <label htmlFor={id + "-compare-second"}>Deuxième scène à comparer</label>
      <select id={id + "-compare-second"} value={secondScene}
        onChange={e => { setSecondScene(e.currentTarget.value); setSecondWorldRevision(""); }}>
        <option value="">Choisir la deuxième scène</option>
        {draft.snapshot.narration.map(s => <option key={s.scene_id} value={s.scene_id}>
          {s.novel_title} — {s.scene_title} ({s.scene_id})
        </option>)}
      </select>
      <section role="status" aria-label="Comparaison des trois ordres fictifs">
        <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit, minmax(14rem, 1fr))",gap:"0.75rem"}}>
          <section aria-label="Chronologie du monde fictif" style={{border:"1px solid currentColor",padding:"0.75rem",borderRadius:"0.5rem"}}>
            <h4>Temps du monde — décision humaine</h4>
            <p>Modification possible seulement par les actions fictives explicites de création, correction ou révocation.</p>
            <p>{threeOrders.world_reason}</p>
          </section>
          <section aria-label="Ordre de narration fictif" style={{border:"1px solid currentColor",padding:"0.75rem",borderRadius:"0.5rem"}}>
            <h4>Ordre de narration — lecture seule du manuscrit</h4>
            <p>Ordre de narration : {threeOrders.narration_reason}</p>
            <p>La position dans le roman n'est pas une preuve du temps du monde.</p>
          </section>
          <section aria-label="Révélation au lecteur fictive" style={{border:"1px solid currentColor",padding:"0.75rem",borderRadius:"0.5rem"}}>
            <h4>Révélation au lecteur — lecture seule</h4>
            <p>{threeOrders.reader_reason}</p>
            <p>Aucun ordre de révélation calculé ni renseigné par cette comparaison.</p>
          </section>
        </div>
        <p>Aucune conversion silencieuse entre temps du monde, narration et révélation.</p>
      </section>
      <section aria-label="Preuve du temps du monde par révisions exactes">
        <h3>Preuve du temps du monde — révisions explicites</h3>
        <p>Choisissez une version immuable par scène. Une position dans un roman ne prouve aucun temps du monde.</p>
        <label htmlFor={id + "-first-world-rev"}>Révision exacte de la première scène pour le temps du monde</label>
        <select id={id + "-first-world-rev"} value={firstWorldRevision}
          onChange={e => setFirstWorldRevision(e.currentTarget.value)}>
          <option value="">Choisir une version précise</option>
          {draft.revisions.filter(r => r.scene_id === firstScene).map(r =>
            <option key={r.revision_id} value={r.revision_id}>
              {r.revision_label} — {r.revision_id}
            </option>)}
        </select>
        <label htmlFor={id + "-second-world-rev"}>Révision exacte de la deuxième scène pour le temps du monde</label>
        <select id={id + "-second-world-rev"} value={secondWorldRevision}
          onChange={e => setSecondWorldRevision(e.currentTarget.value)}>
          <option value="">Choisir une version précise</option>
          {draft.revisions.filter(r => r.scene_id === secondScene).map(r =>
            <option key={r.revision_id} value={r.revision_id}>
              {r.revision_label} — {r.revision_id}
            </option>)}
        </select>
        <section role="status" aria-label="Résultat du temps du monde lié aux révisions">
          <p>{sceneWorld.reason}</p>
          {sceneWorld.witness_edge_ids.length > 0 && <p>
            Témoins humains actifs : {sceneWorld.witness_edge_ids.join(", ")}
          </p>}
          <p>Révélation au lecteur non renseignée ; aucune date ni ordre narratif inféré.</p>
        </section>
      </section>
    </fieldset>
    <fieldset>
      <legend>Consulter une preuve de précédence humaine — fictive</legend>
      <p>Seules les relations humaines encore en vigueur peuvent justifier un ordre.
        Un tri de scènes ou une date littéraire ne constitue pas une preuve.</p>
      <label htmlFor={id + "-world-left"}>Première ancre à consulter</label>
      <select id={id + "-world-left"} value={worldLeft}
        onChange={e => setWorldLeft(e.currentTarget.value)}>
        <option value="">Choisir la première ancre</option>
        {worldLeft && !active.some(a => a.id === worldLeft) &&
          <option value={worldLeft} disabled>Historique : {worldLeft}</option>}
        {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
      </select>
      <label htmlFor={id + "-world-right"}>Deuxième ancre à consulter</label>
      <select id={id + "-world-right"} value={worldRight}
        onChange={e => setWorldRight(e.currentTarget.value)}>
        <option value="">Choisir la deuxième ancre</option>
        {worldRight && !active.some(a => a.id === worldRight) &&
          <option value={worldRight} disabled>Historique : {worldRight}</option>}
        {active.map(a => <option key={a.id} value={a.id}>{a.id}</option>)}
      </select>
      {selectionIsHistorical
        ? <p role="status">Sélection historique : une ancre remplacée n'est plus une preuve courante.
            Choisissez deux ancres actives ; l'historique est conservé.</p>
        : worldLeft && worldRight
          ? <M32WorldOrderComparison expectedUniverseId={draft.snapshot.universe_id}
              snapshot={draft.snapshot} leftAnchorId={worldLeft} rightAnchorId={worldRight} />
          : <p>Choisir deux ancres actives pour consulter les preuves déclarées.</p>}
      <p>Cette consultation ne crée ni ne révoque de relation, et ne renseigne
        aucune révélation au lecteur.</p>
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
