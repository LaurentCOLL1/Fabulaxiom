import { useId, useState, type ReactElement } from "react";
import { type M32ChronologyProjection } from "./M32ChronologyPreview";
import M32ChronologyConsultation, {
  EMPTY_M32_CONSULTATION_SELECTION,
  chooseM32ConsultationAnchor,
  inspectM32Consultation,
  type M32ConsultationSelection,
  type M32ConsultationSide,
} from "./M32ChronologyConsultation";

/** Unmounted synthetic laboratory explorer, NEVER a source reader or Tauri IPC. */
export type M32ExplorerFilter = "all" | "current" | "historical";
export const M32_EXPLORER_PAGE_SIZE = 8;
export type M32ExplorerRow = Readonly<{
  id: string;
  label: string;
  status: "current" | "revoked" | "superseded";
  revision: string | null;
}>;
export type M32ExplorerView = Readonly<{
  rows: readonly M32ExplorerRow[];
  count: number;
  page: number;
  pageCount: number;
  comparison: ReturnType<typeof inspectM32Consultation>["comparison"];
  source_kind: "invented_only";
  can_write: false;
}>;

function refused(): never {
  throw new Error("Explorateur M3.2 fictif refusé");
}

/** Filters only the EXPLORER list, never removes source nodes from the graph.
 * The complete active-graph veto and current-ID admission run before filtering.
 * Paging never silently clears/replaces an existing comparison.
 */
export function deriveM32Explorer(
  snapshot: M32ChronologyProjection | null,
  universeId: string,
  selection: M32ConsultationSelection,
  query: string,
  status: M32ExplorerFilter,
  requestedPage: number,
): M32ExplorerView {
  if (typeof query !== "string" || query.length > 160 ||
      (status !== "all" && status !== "current" && status !== "historical") ||
      !Number.isSafeInteger(requestedPage) || requestedPage < 0) {
    return refused();
  }
  const approved = inspectM32Consultation(snapshot, universeId, selection);
  const normalized = query.trim().toLocaleLowerCase("fr");
  const anchors = approved.snapshot?.anchors ?? [];
  const filtered = anchors.filter(a => {
    const statusMatch = status === "all" ||
      (status === "current" ? a.status === "current" : a.status !== "current");
    const textMatch = !normalized ||
      a.id.toLocaleLowerCase("fr").includes(normalized) ||
      (a.fictional_label ?? "").toLocaleLowerCase("fr").includes(normalized);
    return statusMatch && textMatch;
  }).sort((a, b) => a.id.localeCompare(b.id));
  const pageCount = Math.max(1, Math.ceil(filtered.length / M32_EXPLORER_PAGE_SIZE));
  const page = Math.min(requestedPage, pageCount - 1);
  return {
    rows: filtered.slice(page * M32_EXPLORER_PAGE_SIZE,
      (page + 1) * M32_EXPLORER_PAGE_SIZE).map(a => ({
        id: a.id,
        label: a.fictional_label ?? "Date non précisée",
        status: a.status,
        revision: a.source_revision_id,
      })),
    count: filtered.length, page, pageCount,
    comparison: approved.comparison,
    source_kind: "invented_only", can_write: false,
  };
}

function SyntheticExplorerScenario({
  snapshot, expectedUniverseId,
}: {
  snapshot: M32ChronologyProjection | null;
  expectedUniverseId: string;
}): ReactElement {
  const id = useId();
  const [selection, setSelection] = useState<M32ConsultationSelection>(
    EMPTY_M32_CONSULTATION_SELECTION,
  );
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<M32ExplorerFilter>("all");
  const [page, setPage] = useState(0);
  let model: M32ExplorerView;
  try {
    model = deriveM32Explorer(snapshot, expectedUniverseId, selection,
      query, status, page);
  } catch {
    return <section role="alert" aria-label="Explorateur M3.2 refusé">
      <h2>Exploration refusée</h2>
      <p>Univers, graphe ou sélection incompatibles. Aucune assertion exposée.</p>
    </section>;
  }
  if (snapshot === null) {
    return <section role="status" aria-label="Explorateur M3.2 sans source">
      <h2>Explorateur fictif — aucune donnée fournie</h2>
    </section>;
  }
  const choose = (side: M32ConsultationSide, candidate: string) => {
    setSelection(chooseM32ConsultationAnchor(
      snapshot, expectedUniverseId, selection, side, candidate));
  };
  return <section className="m32-explorer" aria-label="Explorateur M3.2 fictif filtrable">
    <h2>Explorer les assertions fictives</h2>
    <p>Filtrer cette liste ne modifie pas les relations ni les sélections courantes.</p>
    <section role="search" aria-label="Recherche dans la chronologie fictive" className="m32-search-controls">
      <label htmlFor={id + "-query"}>Filtrer les événements</label>
    <input id={id + "-query"} type="search" value={query} maxLength={160}
      onChange={event => { setQuery(event.currentTarget.value); setPage(0); }} />
    <label htmlFor={id + "-status"}>Filtre de statut</label>
    <select id={id + "-status"} value={status}
      onChange={event => {
        const value = event.currentTarget.value;
        if (value !== "all" && value !== "current" && value !== "historical") {
          return refused();
        }
        setStatus(value);
        setPage(0);
      }}>
      <option value="all">Tous les événements</option>
      <option value="current">En vigueur seulement</option>
      <option value="historical">Historique seulement</option>
    </select>
    </section>
    <p role="status" aria-label="Résultat du filtrage" aria-atomic="true">
      {model.count} assertions correspondantes — Page {model.page + 1} sur {model.pageCount}
    </p>
    <p role="status" aria-label="Événements choisis" aria-atomic="true">
      Premier : {selection.leftAnchorId ?? "non sélectionné"} ;
      deuxième : {selection.rightAnchorId ?? "non sélectionné"}.
    </p>
    <ol className="m32-event-list" aria-label="Événements filtrés">{model.rows.map(row => <li
      className="m32-event-row" key={row.id}>
      <code>{row.id}</code> — {row.label} — {row.status === "current"
        ? "En vigueur" : row.status === "revoked" ? "Révoquée (historique)"
          : "Remplacée (historique)"}
      {row.revision && <span> — révision : <code>{row.revision}</code></span>}
      {row.status === "current" && <>
        {" "}<button type="button" onClick={() => choose("left", row.id)}
          aria-label={"Choisir " + row.id + " comme premier événement"}
          aria-pressed={selection.leftAnchorId === row.id}>
          Premier
        </button>
        {" "}<button type="button" onClick={() => choose("right", row.id)}
          aria-label={"Choisir " + row.id + " comme deuxième événement"}
          aria-pressed={selection.rightAnchorId === row.id}>
          Deuxième
        </button>
      </>}
    </li>)}</ol>
    {model.count === 0 && <p>Aucun événement fictif ne correspond au filtre.</p>}
    <nav className="m32-pagination" aria-label="Pagination des événements fictifs">
      <button type="button" disabled={model.page === 0}
        onClick={() => setPage(model.page - 1)}>Page précédente</button>
      <button type="button" disabled={model.page + 1 >= model.pageCount}
        onClick={() => setPage(model.page + 1)}>Page suivante</button>
    </nav>
    {model.comparison !== null && <section className="m32-proof" aria-label="Résumé de justification de comparaison">
      <h3>Justification des événements sélectionnés</h3>
      <p>Relation : {model.comparison.relation === "before" ? "Avant"
        : model.comparison.relation === "after" ? "Après"
          : model.comparison.relation === "same" ? "Identique" : "Indéterminée"}</p>
      {model.comparison.witness.length > 0
        ? <ol className="m32-proof-steps" aria-label="Chaîne de précédence sélectionnée">
          {model.comparison.witness.map((w, idx) => <li key={w.precedence_id}>
            Étape {idx + 1} : <code>{w.before_anchor_id}</code> vers
            {" "}<code>{w.after_anchor_id}</code> —
            {" "}<code>{w.precedence_id}</code> — motif : {w.human_reason}
          </li>)}
        </ol>
        : <p>Aucune chaîne de précédences humaines justificatives.</p>}
    </section>}
    <M32ChronologyConsultation
      expectedUniverseId={expectedUniverseId}
      snapshot={snapshot}
      selection={selection}
      onSelectionChange={setSelection}
    />
    <p>Exploration uniquement en mémoire fictive. Aucune modification du monde.</p>
  </section>;
}

/** React key drops ALL explorer-local state when the caller changes toy scenarios.
 * The key is not a source hash or an authorization token.
 */
export default function M32SyntheticEventExplorer({
  scenarioKey, expectedUniverseId, snapshot,
}: {
  scenarioKey: string;
  expectedUniverseId: string;
  snapshot: M32ChronologyProjection | null;
}): ReactElement {
  return <SyntheticExplorerScenario key={scenarioKey}
    snapshot={snapshot} expectedUniverseId={expectedUniverseId} />;
}
