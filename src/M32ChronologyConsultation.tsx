import { useId, useState, type ReactElement } from "react";
import M32ChronologyPreview, {
  decodeM32ChronologyProjection,
  type M32ChronologyProjection,
} from "./M32ChronologyPreview";
import M32WorldOrderComparison, {
  compareM32WorldOrder,
  type M32WorldComparison,
} from "./M32WorldOrderComparison";

/** Test-only composition of two already-qualified read-only React views.
 * NOT mounted by App.tsx. No service, Tauri IPC, storage or operator data.
 */
export type M32ConsultationSelection = Readonly<{
  leftAnchorId: string | null;
  rightAnchorId: string | null;
}>;
export type M32ConsultationSide = "left" | "right";
export const EMPTY_M32_CONSULTATION_SELECTION: M32ConsultationSelection = Object.freeze({
  leftAnchorId: null, rightAnchorId: null,
});
export type M32ConsultationOption = Readonly<{ id: string; label: string }>;
export type M32ConsultationModel = Readonly<{
  snapshot: M32ChronologyProjection | null;
  options: readonly M32ConsultationOption[];
  comparison: M32WorldComparison | null;
  stage: "no_fixture" | "no_active_anchors" | "choose_pair" | "compared";
  data_origin: "synthetic_in_memory_only";
  editing_authorized: false;
}>;

function refuse(): never {
  throw new Error("Consultation M3.2 fictive refusée");
}
function validId(id: unknown): id is string {
  return typeof id === "string" && id.trim().length > 0;
}

/** Validate the entire fictional graph even before any anchor is selected.
 * A bad edge/cycle may not remain hidden behind an empty selection.
 */
export function inspectM32Consultation(
  snapshot: M32ChronologyProjection | null,
  expectedUniverseId: string,
  selection: M32ConsultationSelection,
): M32ConsultationModel {
  if (!selection || typeof selection !== "object" ||
      !Object.prototype.hasOwnProperty.call(selection, "leftAnchorId") ||
      !Object.prototype.hasOwnProperty.call(selection, "rightAnchorId")) {
    return refuse();
  }
  if (!validId(expectedUniverseId)) return refuse();
  if (selection.leftAnchorId !== null && !validId(selection.leftAnchorId)) return refuse();
  if (selection.rightAnchorId !== null && !validId(selection.rightAnchorId)) return refuse();
  if (snapshot === null) {
    if (selection.leftAnchorId !== null || selection.rightAnchorId !== null) return refuse();
    return { snapshot: null, options: [], comparison: null,
      stage: "no_fixture", data_origin: "synthetic_in_memory_only",
      editing_authorized: false };
  }
  const checked = decodeM32ChronologyProjection(snapshot, expectedUniverseId);
  const current = checked.anchors
    .filter(a => a.status === "current")
    .sort((a, b) => a.id.localeCompare(b.id));
  const valid = new Set(current.map(a => a.id));
  // An active relation has to be attached to at least one current anchor.
  if (current.length === 0 && checked.precedences.some(e => e.status === "current")) {
    return refuse();
  }
  if (current.length !== 0) {
    // compare(same, same) still validates ALL current graph edges and cycles.
    compareM32WorldOrder(checked, expectedUniverseId, current[0].id, current[0].id);
  }
  if ((selection.leftAnchorId !== null && !valid.has(selection.leftAnchorId)) ||
      (selection.rightAnchorId !== null && !valid.has(selection.rightAnchorId))) {
    return refuse(); // Never replace a historical/stale selection with a new ID.
  }
  const options = current.map(a => ({
    id: a.id,
    label: a.fictional_label === null ? "Date fictive non précisée" : a.fictional_label,
  }));
  const complete = selection.leftAnchorId !== null && selection.rightAnchorId !== null;
  const comparison = complete
    ? compareM32WorldOrder(checked, expectedUniverseId,
        selection.leftAnchorId!, selection.rightAnchorId!)
    : null;
  return { snapshot: checked, options, comparison,
    stage: current.length === 0 ? "no_active_anchors" : complete ? "compared" : "choose_pair",
    data_origin: "synthetic_in_memory_only", editing_authorized: false };
}

/** A select-only transition: an empty option explicitly clears a choice.
 * No hidden default, ID coercion, automatic ranking, or persistence.
 */
export function chooseM32ConsultationAnchor(
  snapshot: M32ChronologyProjection | null,
  expectedUniverseId: string,
  selection: M32ConsultationSelection,
  side: M32ConsultationSide,
  selectedId: string,
): M32ConsultationSelection {
  if (side !== "left" && side !== "right") return refuse();
  if (typeof selectedId !== "string") return refuse();
  const model = inspectM32Consultation(snapshot, expectedUniverseId, selection);
  if (model.snapshot === null) return refuse();
  if (selectedId !== "" && !model.options.some(x => x.id === selectedId)) return refuse();
  const next = selectedId === "" ? null : selectedId;
  return side === "left"
    ? { leftAnchorId: next, rightAnchorId: selection.rightAnchorId }
    : { leftAnchorId: selection.leftAnchorId, rightAnchorId: next };
}

/** Controlled, unmounted inspection UI. Native labelled select elements
 * provide keyboard access; select changes are UI-only, not domain writes.
 */
export default function M32ChronologyConsultation({
  expectedUniverseId, snapshot, selection, onSelectionChange,
}: {
  expectedUniverseId: string;
  snapshot: M32ChronologyProjection | null;
  selection: M32ConsultationSelection;
  onSelectionChange: (next: M32ConsultationSelection) => void;
}): ReactElement {
  const labelId = useId();
  let model: M32ConsultationModel;
  try {
    model = inspectM32Consultation(snapshot, expectedUniverseId, selection);
  } catch {
    return <section role="alert" aria-label="Consultation M3.2 refusée">
      <h2>Consultation refusée</h2>
      <p>Univers, source, graphe ou sélection incompatible. Aucun événement affiché.</p>
    </section>;
  }
  if (model.stage === "no_fixture") {
    return <section role="status" aria-label="Consultation M3.2 sans données">
      <h2>Chronologie fictive — aucun jeu de données fourni</h2>
      <p>Aucune recherche automatique de base n’est effectuée.</p>
    </section>;
  }
  return <section aria-label="Parcours M3.2 fictif en lecture seule">
    <h2>Parcours de consultation chronologique fictif</h2>
    <p>Univers : <code>{expectedUniverseId}</code> — expérience sans base opérateur.</p>
    <M32ChronologyPreview expectedUniverseId={expectedUniverseId} snapshot={model.snapshot} />
    <section aria-label="Sélection explicite de deux événements">
      <h3>Comparer deux assertions en vigueur</h3>
      {model.stage === "no_active_anchors" ? <p>Aucune assertion en vigueur à sélectionner.</p> : <>
        <label htmlFor={labelId + "-left"}>Premier événement</label>
        <select id={labelId + "-left"} value={selection.leftAnchorId ?? ""}
          onChange={event => onSelectionChange(chooseM32ConsultationAnchor(
            model.snapshot, expectedUniverseId, selection, "left", event.currentTarget.value))}>
          <option value="">Choisir explicitement un événement</option>
          {model.options.map(o => <option key={o.id} value={o.id}>{o.id} — {o.label}</option>)}
        </select>
        <label htmlFor={labelId + "-right"}>Deuxième événement</label>
        <select id={labelId + "-right"} value={selection.rightAnchorId ?? ""}
          onChange={event => onSelectionChange(chooseM32ConsultationAnchor(
            model.snapshot, expectedUniverseId, selection, "right", event.currentTarget.value))}>
          <option value="">Choisir explicitement un événement</option>
          {model.options.map(o => <option key={o.id} value={o.id}>{o.id} — {o.label}</option>)}
        </select>
      </>}
      {model.stage === "choose_pair" && <p role="status">
        Choisissez les deux événements ; aucun ordre n’est déduit par défaut.
      </p>}
    </section>
    {model.comparison !== null && <M32WorldOrderComparison
      expectedUniverseId={expectedUniverseId}
      snapshot={model.snapshot}
      leftAnchorId={model.comparison.left_anchor_id}
      rightAnchorId={model.comparison.right_anchor_id} />}
    <p>Choix purement locaux à cette prévisualisation. Ni sauvegarde ni écriture.</p>
  </section>;
}

/** Deliberately unmounted lab harness. The fictional scenario key forces React
 * to create a fresh selection state when the caller replaces the toy scenario.
 * It is NOT a fingerprint, source authentication, or permission.
 */
function SyntheticScenario({
  expectedUniverseId, snapshot,
}: {
  expectedUniverseId: string;
  snapshot: M32ChronologyProjection | null;
}): ReactElement {
  const [selection, setSelection] = useState<M32ConsultationSelection>(
    EMPTY_M32_CONSULTATION_SELECTION,
  );
  return <M32ChronologyConsultation expectedUniverseId={expectedUniverseId}
    snapshot={snapshot} selection={selection} onSelectionChange={setSelection} />;
}
export function M32SyntheticConsultationLab({
  scenarioKey, expectedUniverseId, snapshot,
}: {
  scenarioKey: string;
  expectedUniverseId: string;
  snapshot: M32ChronologyProjection | null;
}): ReactElement {
  return <SyntheticScenario key={scenarioKey} expectedUniverseId={expectedUniverseId}
    snapshot={snapshot} />;
}
