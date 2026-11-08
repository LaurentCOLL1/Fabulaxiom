import { useState, type ReactElement } from "react";
import M32P2mFictionalSharedEvidence, {
  previewP2mFictionalSharedEvidence,
} from "./M32P2mFictionalSharedEvidence";
import M32P2lFictionalDirectionalEvidence from "./M32P2lFictionalDirectionalEvidence";
import type { P2iFictionalInput } from "./M32P2iFictionalImpactReview";

/** P3f: invented two-novel author review; NOT a Rust-v7 bridge or operator UI. */
export type P3fFictionalNovelSource = Readonly<{
  universe_id: string;
  novel_id: string;
  novel_title: string;
  scene_id: string;
  anchor_id: string;
  source_revision_id: string;
  current_head_revision_id: string;
}>;
/** P3g: invented declared revision witnesses, never SQL identity. */
export type P3gFictionalRevisionWitness = Readonly<{
  universe_id: string;
  novel_id: string;
  scene_id: string;
  revision_id: string;
  role: "historical_source" | "current_head";
  anchor_id: string | null;
}>;
export type P3fFictionalNovelInput = Readonly<{
  data_origin: "fictional_browser_memory_only";
  production_writer_admitted: false;
  real_g3_authorized: false;
  universe_id: string;
  novels: readonly [P3fFictionalNovelSource, P3fFictionalNovelSource];
  revision_witnesses: readonly P3gFictionalRevisionWitness[];
  impact: P2iFictionalInput;
}>;

const nonblank = (v: unknown): v is string =>
  typeof v === "string" && v.trim().length > 0;

/** Validate a declared FICTIONAL provenance pairing, never a database identity. */
export function previewP3fTwoNovelFictionalReview(input: P3fFictionalNovelInput) {
  if (!input || input.data_origin !== "fictional_browser_memory_only" ||
      input.production_writer_admitted !== false ||
      input.real_g3_authorized !== false || !nonblank(input.universe_id) ||
      !Array.isArray(input.novels) || input.novels.length !== 2) {
    throw new Error("P3f : revue inter-romans fictive refusée");
  }
  const [first, second] = input.novels;
  for (const source of [first, second]) {
    if (!source || source.universe_id !== input.universe_id ||
        !nonblank(source.novel_id) || !nonblank(source.novel_title) ||
        !nonblank(source.scene_id) || !nonblank(source.anchor_id) ||
        !nonblank(source.source_revision_id) ||
        !nonblank(source.current_head_revision_id) ||
        source.source_revision_id === source.current_head_revision_id) {
      throw new Error("P3f : métadonnées fictives insuffisantes");
    }
  }
  if (first.novel_id === second.novel_id ||
      first.scene_id === second.scene_id ||
      first.anchor_id === second.anchor_id ||
      first.source_revision_id === second.source_revision_id ||
      !input.impact || input.impact.universe_id !== input.universe_id) {
    throw new Error("P3f : deux sources de romans distincts sont requises");
  }
  // Self-contained declared witnesses only: no revision is read from SQLite.
  const witnesses = input.revision_witnesses;
  if (!Array.isArray(witnesses) || witnesses.length !== 4) {
    throw new Error("P3g : quatre témoins de révision fictifs requis");
  }
  const revisions = new Set<string>();
  for (const witness of witnesses) {
    if (!witness || witness.universe_id !== input.universe_id ||
        !nonblank(witness.novel_id) || !nonblank(witness.scene_id) ||
        !nonblank(witness.revision_id)) {
      throw new Error("P3g : provenance fictive étrangère refusée");
    }
    const source = [first, second].find(novel =>
      novel.novel_id === witness.novel_id && novel.scene_id === witness.scene_id);
    const expectedRevision = witness.role === "historical_source"
      ? source?.source_revision_id : witness.role === "current_head"
        ? source?.current_head_revision_id : null;
    const expectedAnchor = witness.role === "historical_source" ? source?.anchor_id : null;
    if (!source || !expectedRevision || witness.revision_id !== expectedRevision ||
        witness.anchor_id !== expectedAnchor || revisions.has(witness.revision_id)) {
      throw new Error("P3g : attribution de révision fictive refusée");
    }
    revisions.add(witness.revision_id);
  }
  const direct = previewP2mFictionalSharedEvidence(
    input.impact, input.universe_id, first.anchor_id, second.anchor_id,
  );
  return {
    first,
    second,
    direct,
    declared_revision_witnesses: revisions.size,
    data_origin: "fictional_browser_memory_only" as const,
    production_writer_admitted: false as const,
    real_g3_authorized: false as const,
  };
}

type ReviewMode = "joint" | "first" | "second";
export default function M32P3fTwoNovelFictionalReview({
  input,
}: { input: P3fFictionalNovelInput }): ReactElement {
  const [mode, setMode] = useState<ReviewMode>("joint");
  let review: ReturnType<typeof previewP3fTwoNovelFictionalReview>;
  try {
    review = previewP3fTwoNovelFictionalReview(input);
  } catch {
    // Never reveal labels or historical revisions of invalid/foreign input.
    return <section role="alert" aria-label="Revue inter-romans fictive refusée">
      <h2>Revue fictive refusée</h2>
      <p>Sources, Univers ou assertions invalides. Aucune commande exécutée.</p>
    </section>;
  }
  return <section aria-label="Revue chronologique de deux romans fictifs">
    <h2>Deux romans — sources historiques et relations directes</h2>
    <p>Laboratoire navigateur : métadonnées et assertions inventées, sans liaison Rust,
      SQLite, Tauri IPC ni profil opérateur. Aucun ordre total ni date inventés.</p>
    <ul aria-label="Sources historiques fictives des romans">
      {[review.first, review.second].map((source, index) =>
        <li key={source.novel_id}>
          <strong>{index === 0 ? "Premier roman" : "Second roman"}</strong>
          {" — "}{source.novel_title} (<code>{source.novel_id}</code>)
          {" — ancre "}<code>{source.anchor_id}</code>
          {" — révision historique "}<code>{source.source_revision_id}</code>
          {" — HEAD fictive distincte "}<code>{source.current_head_revision_id}</code>
        </li>,
      )}
    </ul>
    <p>Catalogue fictif déclaré : {review.declared_revision_witnesses} attributions de
      révision contrôlées entre romans, scènes et ancres. Aucune preuve SQLite.</p>
    <nav aria-label="Choisir une preuve fictive inter-romans">
      <button type="button" aria-pressed={mode === "joint"}
        onClick={() => setMode("joint")}>Comparer les assertions communes</button>
      <button type="button" aria-pressed={mode === "first"}
        onClick={() => setMode("first")}>Directions du premier roman</button>
      <button type="button" aria-pressed={mode === "second"}
        onClick={() => setMode("second")}>Directions du second roman</button>
    </nav>
    {mode === "joint" ?
      <M32P2mFictionalSharedEvidence input={input.impact}
        expectedUniverse={input.universe_id}
        firstAnchor={review.first.anchor_id} secondAnchor={review.second.anchor_id} />
      : <M32P2lFictionalDirectionalEvidence input={input.impact}
        expectedUniverse={input.universe_id}
        selectedAnchor={mode === "first" ? review.first.anchor_id : review.second.anchor_id} />}
    <p>Aucune confirmation ni mutation : P4 réel et writer STOP_UNAVAILABLE.
      Ces révisions ne sont pas des preuves de propriété SQLite ou d'admission.</p>
  </section>;
}
