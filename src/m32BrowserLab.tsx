import { useState } from "react";
import "./m32BrowserLab.css";
import { createRoot } from "react-dom/client";
import { M32SyntheticConsultationLab } from "./M32ChronologyConsultation";
import M32SyntheticEventExplorer from "./M32SyntheticEventExplorer";
import M32ManualChronologyLab from "./M32ManualChronologyLab";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import { startFictionalDraft, type FictionalRevision } from "./m32FictionalManualChronology";
import { startFictionalEventNotebook } from "./m32FictionalEventNotebook";
import M32FictionalEventManualWorkshop from "./M32FictionalEventManualWorkshop";
import M32FictionalCorrectionHistory, { type M32FictionalCorrectionRow } from "./M32FictionalCorrectionHistory";

/** DISPOSABLE FICTITIOUS BROWSER TEST PAGE. NOT an App.tsx import or Tauri route.
 * No original user data, IPC, storage, fetch or filesystem reads.
 */
const first: M32ChronologyProjection = {
  universe_id: "fiction-world-one",
  reader_reveal_status: "not_authored",
  anchors: [
    { id: "A", universe_id: "fiction-world-one", time_kind: "exact",
      status: "current", calendar_name: "Calendrier des marées",
      fictional_label: "Troisième cloche", precision_text: null,
      source_revision_id: "invented-rev-A" },
    ...["B", "C", "D", ...Array.from({ length: 19 }, (_, i) => "N" + String(i + 1).padStart(2, "0"))].map(id => ({
      id, universe_id: "fiction-world-one", time_kind: "unknown" as const,
      status: "current" as const, calendar_name: null, fictional_label: null,
      precision_text: null, source_revision_id: null,
    })),
    { id: "retired", universe_id: "fiction-world-one", time_kind: "unknown",
      status: "revoked", calendar_name: null, fictional_label: null,
      precision_text: null, source_revision_id: null },
    { id: "escape-demo", universe_id: "fiction-world-one", time_kind: "exact",
      status: "superseded", calendar_name: "Marées",
      fictional_label: "<script>not executable()</script>", precision_text: null,
      source_revision_id: null },
  ],
  precedences: [
    { id: "human-ab", universe_id: "fiction-world-one",
      before_anchor_id: "A", after_anchor_id: "B", status: "current",
      reason: "Le messager arrive" },
    { id: "human-bc", universe_id: "fiction-world-one",
      before_anchor_id: "B", after_anchor_id: "C", status: "current",
      reason: "La porte s'ouvre" },
    { id: "retired-ad", universe_id: "fiction-world-one",
      before_anchor_id: "A", after_anchor_id: "D", status: "revoked",
      reason: "Ancien ordre retiré" },
  ],
  narration: [
    { universe_id: "fiction-world-one", scene_id: "s1",
      novel_id: "novel-1", novel_title: "Roman imaginaire",
      chapter_id: "chapter-1", chapter_title: "Premier chapitre",
      chapter_order: 0, scene_order: 0, scene_title: "L'ouverture" },
    { universe_id: "fiction-world-one", scene_id: "s3",
      novel_id: "novel-1", novel_title: "Roman imaginaire",
      chapter_id: "chapter-1", chapter_title: "Premier chapitre",
      chapter_order: 0, scene_order: 2, scene_title: "Le phare éteint" },
    { universe_id: "fiction-world-one", scene_id: "s2",
      novel_id: "novel-2", novel_title: "Deuxième roman imaginaire",
      chapter_id: "chapter-2", chapter_title: "Autre chapitre",
      chapter_order: 0, scene_order: 0, scene_title: "Le retour du messager" },
  ],
};

/** Literal historical IDs; neither display text nor a mutable scene HEAD. */
const fictionalRevisions: readonly FictionalRevision[] = [
  { universe_id: "fiction-world-one", novel_id: "novel-1", scene_id: "s1",
    revision_id: "invented-rev-A", revision_label: "Ancienne rédaction A" },
  { universe_id: "fiction-world-one", novel_id: "novel-1", scene_id: "s1",
    revision_id: "invented-rev-B", revision_label: "Autre rédaction B" },
  { universe_id: "fiction-world-one", novel_id: "novel-2", scene_id: "s2",
    revision_id: "invented-rev-C", revision_label: "Deuxième roman - texte historique" },
];

const second: M32ChronologyProjection = {
  universe_id: "fiction-world-two",
  reader_reveal_status: "not_authored",
  anchors: ["K", "L"].map(id => ({
    id, universe_id: "fiction-world-two", time_kind: "unknown" as const,
    status: "current" as const, calendar_name: null,
    fictional_label: null, precision_text: null, source_revision_id: null,
  })),
  precedences: [],
  narration: [],
};

const cyclic: M32ChronologyProjection = {
  ...first,
  precedences: [...first.precedences, {
    id: "fiction-cycle", universe_id: "fiction-world-one",
    before_anchor_id: "C", after_anchor_id: "A",
    status: "current", reason: "Contradiction fictive",
  }],
};

/** Invented immutable descendants only, not a real SQLite history. */
const inventedCorrections: readonly M32FictionalCorrectionRow[] = [
  {
    id: "fiction-successor", universe_id: "fiction-world-one", kind: "successor",
    prior_successor_id: null, prior_chain_id: null,
    before_anchor_id: "A", after_anchor_id: "B", reason: "Reformulation humaine fictive",
    revocation_id: "fiction-withdraw-1", revocation_reason: "Auteur a retiré l'assertion",
  },
  {
    id: "fiction-chain-1", universe_id: "fiction-world-one", kind: "chain",
    prior_successor_id: "fiction-successor", prior_chain_id: null,
    before_anchor_id: "B", after_anchor_id: "C", reason: "Correction explicite",
    revocation_id: "fiction-withdraw-2", revocation_reason: "Auteur a révisé son ordre",
  },
  {
    id: "fiction-chain-2", universe_id: "fiction-world-one", kind: "chain",
    prior_successor_id: null, prior_chain_id: "fiction-chain-1",
    before_anchor_id: "C", after_anchor_id: "D", reason: "Dernier ordre humain fictif",
    revocation_id: null, revocation_reason: null,
  },
];
const invalidCorrectionCycle: readonly M32FictionalCorrectionRow[] = [
  inventedCorrections[0],
  { ...inventedCorrections[1], prior_successor_id: null, prior_chain_id: "fiction-chain-1" },
  inventedCorrections[2],
];

type Scenario = "one" | "two" | "cyclic";
function BrowserFixture() {
  const [scenario, setScenario] = useState<Scenario>("one");
  const [mode, setMode] = useState<"consultation" | "explorer" | "editor" | "history" | "event-form">("consultation");
  const snapshot = scenario === "two" ? second : scenario === "cyclic" ? cyclic : first;
  return <main aria-label="Laboratoire navigateur M3.2 exclusivement fictif">
    <h1>Tests navigateur — données imaginaires exclusivement</h1>
    <section aria-label="Commutateurs de scénarios fictifs">
      <button type="button" onClick={() => setScenario("two")}>
        Charger un autre univers fictif
      </button>
      <button type="button" onClick={() => setScenario("one")}>
        Revenir au premier univers fictif
      </button>
      <button type="button" onClick={() => setScenario("cyclic")}>
        Charger un cycle fictif invalide
      </button>
    </section>
    <section aria-label="Choix des interfaces fictives">
      <button type="button" onClick={() => setMode("explorer")}>
        Afficher l'explorateur fictif
      </button>
      <button type="button" onClick={() => setMode("consultation")}>
        Afficher le parcours de consultation fictif
      </button>
      <button type="button" onClick={() => setMode("editor")}>
        Ouvrir l'atelier manuel fictif
      </button>
      <button type="button" onClick={() => setMode("history")}>
        Afficher l'historique fictif des corrections
      </button>
      <button type="button" onClick={() => setMode("event-form")}>
        Ouvrir le carnet d'événements fictifs
      </button>
    </section>
    {mode === "event-form" ? scenario === "cyclic"
      ? <p role="alert">Cycle fictif refusé pour le carnet manuel.</p>
      : <M32FictionalEventManualWorkshop key={scenario}
          initial={startFictionalEventNotebook(startFictionalDraft(snapshot,
            scenario === "two" ? [] : fictionalRevisions))} />
      : mode === "history"
      ? <M32FictionalCorrectionHistory expectedUniverseId={snapshot.universe_id}
          records={scenario === "two" ? [] : scenario === "cyclic"
            ? invalidCorrectionCycle : inventedCorrections} />
      : mode === "editor"
      ? <M32ManualChronologyLab key={scenario} initial={snapshot}
          revisions={scenario === "two" ? [] : fictionalRevisions} />
      : mode === "consultation" ? <M32SyntheticConsultationLab
        scenarioKey={scenario}
        expectedUniverseId={snapshot.universe_id}
        snapshot={snapshot}
      /> : <M32SyntheticEventExplorer
        scenarioKey={scenario}
        expectedUniverseId={snapshot.universe_id}
        snapshot={snapshot}
      />}
    <p>Aucun événement dans cette page ne provient d'une base opérateur.</p>
  </main>;
}
const mount = document.getElementById("m32-browser-lab-root");
if (!mount) throw new Error("No isolated synthetic browser root");
createRoot(mount).render(<BrowserFixture />);
