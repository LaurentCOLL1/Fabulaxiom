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
/** P3i: explicitly INVENTED character/fact notes tied to historical novel sources. */
export type P3iFictionalCanonClaim = Readonly<{
  assertion_id: string;
  universe_id: string;
  novel_id: string;
  scene_id: string;
  source_revision_id: string;
  entity_id: string;
  property_key: string;
  literal_value: string;
}>;
export type P3iFictionalCanonPair = Readonly<{
  first: P3iFictionalCanonClaim;
  second: P3iFictionalCanonClaim;
}>;

export type P3fFictionalNovelInput = Readonly<{
  data_origin: "fictional_browser_memory_only";
  production_writer_admitted: false;
  real_g3_authorized: false;
  universe_id: string;
  novels: readonly [P3fFictionalNovelSource, P3fFictionalNovelSource];
  revision_witnesses: readonly P3gFictionalRevisionWitness[];
  impact: P2iFictionalInput;
  /** Optional only for earlier P3f fixtures: absence is NOT a coherence proof. */
  canon_claims?: readonly P3iFictionalCanonClaim[];
}>;

const nonblank = (v: unknown): v is string =>
  typeof v === "string" && v.trim().length > 0;

/** Compare ONLY matching explicit keys across the two invented historical sources.
 * A difference is a review prompt, never an inferred contradiction or date.
 */
export function compareP3iFictionalCanonClaims(input: P3fFictionalNovelInput) {
  const claims = input.canon_claims === undefined ? [] : input.canon_claims;
  if (!Array.isArray(claims) || claims.length > 64) {
    throw new Error("P3i : catalogue de fiches fictives refusé");
  }
  const ids = new Set<string>();
  const keys = new Set<string>();
  for (const claim of claims) {
    if (!claim || claim.universe_id !== input.universe_id ||
        !nonblank(claim.assertion_id) || !nonblank(claim.novel_id) ||
        !nonblank(claim.scene_id) || !nonblank(claim.source_revision_id) ||
        !nonblank(claim.entity_id) || !nonblank(claim.property_key) ||
        !nonblank(claim.literal_value) || claim.literal_value.length > 256) {
      throw new Error("P3i : provenance de fiche fictive refusée");
    }
    const declaredOwner = input.novels.find(novel =>
      novel.novel_id === claim.novel_id &&
      novel.scene_id === claim.scene_id &&
      novel.source_revision_id === claim.source_revision_id);
    const subjectKey = JSON.stringify([
      claim.novel_id, claim.entity_id, claim.property_key,
    ]);
    if (!declaredOwner || ids.has(claim.assertion_id) || keys.has(subjectKey)) {
      throw new Error("P3i : fiche étrangère ou attribution ambiguë");
    }
    ids.add(claim.assertion_id);
    keys.add(subjectKey);
  }
  const [first, second] = input.novels;
  const left = claims.filter(claim => claim.novel_id === first.novel_id);
  const right = claims.filter(claim => claim.novel_id === second.novel_id);
  const agreements: P3iFictionalCanonPair[] = [];
  const differences: P3iFictionalCanonPair[] = [];
  // P3j: absence in the other novel is NOT an agreement or contradiction.
  const first_only: P3iFictionalCanonClaim[] = [];
  const second_only: P3iFictionalCanonClaim[] = [];
  const factKey = (claim: P3iFictionalCanonClaim) =>
    JSON.stringify([claim.entity_id, claim.property_key]);
  const firstKeys = new Set(left.map(factKey));
  const secondKeys = new Set(right.map(factKey));
  for (const claim of left) if (!secondKeys.has(factKey(claim))) first_only.push(claim);
  for (const claim of right) if (!firstKeys.has(factKey(claim))) second_only.push(claim);
  for (const a of left) {
    for (const b of right) {
      if (a.entity_id !== b.entity_id || a.property_key !== b.property_key) continue;
      const pair = { first: a, second: b };
      if (a.literal_value === b.literal_value) agreements.push(pair);
      else differences.push(pair);
    }
  }
  return {
    total_claims: claims.length,
    agreements,
    differences,
    first_only,
    second_only,
    /** Fictional labels are never canon, truth or SQL provenance claims. */
    data_origin: "fictional_browser_memory_only" as const,
    production_writer_admitted: false as const,
    real_g3_authorized: false as const,
  };
}

/** P3k: select a single invented character only AFTER full source validation. */
export function previewP3kFictionalCharacterFocus(
  input: P3fFictionalNovelInput, entityId: string,
) {
  const full = previewP3fTwoNovelFictionalReview(input).canon_comparison;
  const hasEntity = [
    ...full.agreements.map(pair => pair.first.entity_id),
    ...full.differences.map(pair => pair.first.entity_id),
    ...full.first_only.map(claim => claim.entity_id),
    ...full.second_only.map(claim => claim.entity_id),
  ].includes(entityId);
  if (!nonblank(entityId) || !hasEntity) {
    throw new Error("P3k : personnage fictif inconnu ou ambigu");
  }
  const agreements = full.agreements.filter(pair => pair.first.entity_id === entityId);
  const differences = full.differences.filter(pair => pair.first.entity_id === entityId);
  const first_only = full.first_only.filter(claim => claim.entity_id === entityId);
  const second_only = full.second_only.filter(claim => claim.entity_id === entityId);
  return {
    ...full,
    total_claims: 2 * (agreements.length + differences.length) +
      first_only.length + second_only.length,
    agreements, differences, first_only, second_only,
    selected_entity_id: entityId,
  };
}

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
    canon_comparison: compareP3iFictionalCanonClaims(input),
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
  const [characterFocus, setCharacterFocus] = useState("");
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

  const characterIds = [...new Set([
    ...review.canon_comparison.agreements.map(pair => pair.first.entity_id),
    ...review.canon_comparison.differences.map(pair => pair.first.entity_id),
    ...review.canon_comparison.first_only.map(claim => claim.entity_id),
    ...review.canon_comparison.second_only.map(claim => claim.entity_id),
  ])].sort();
  const selectedCharacter = characterIds.includes(characterFocus) ? characterFocus : "";
  const displayedClaims = selectedCharacter === ""
    ? review.canon_comparison
    : previewP3kFictionalCharacterFocus(input, selectedCharacter);
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
    <section aria-label="Revue de cohérence de fiches fictives">
      <h3>Fiches de personnages — comparaison de deux romans fictifs</h3>
      <p>Comparaison des seules déclarations inventées reliées aux révisions
        historiques indiquées ; aucune vérité, date ou priorité narrative inférée.</p>
      {review.canon_comparison.total_claims === 0
        ? <p>Aucune fiche fictive fournie : cohérence non évaluée.</p>
        : <>
          <label htmlFor="m32-p3k-fictional-character">Consulter un personnage fictif</label>
          <select id="m32-p3k-fictional-character" value={selectedCharacter}
            onChange={event => setCharacterFocus(event.target.value)}>
            <option value="">Tous les personnages déclarés</option>
            {characterIds.map(id => <option key={id} value={id}>{id}</option>)}
          </select>
          <p>Filtre de lecture seule : aucun choix canonique, aucune écriture ou
            nouvelle preuve de propriété SQLite.</p>
          <p>{displayedClaims.total_claims} assertions littérales déclarées ;
            {" "}{displayedClaims.differences.length} écarts à examiner ;
            {" "}{displayedClaims.agreements.length} accords déclarés ;
            {" "}{displayedClaims.first_only.length} faits du premier roman sans correspondant ;
            {" "}{displayedClaims.second_only.length} faits du second roman sans correspondant.</p>
          <p>Un fait absent dans l'autre roman signifie uniquement « non comparable » :
            ce n'est ni un accord, ni un écart établi, ni une erreur de canon.</p>
          <ul aria-label="Faits fictifs non comparables entre romans">
            {[...displayedClaims.first_only, ...displayedClaims.second_only]
              .map(claim => <li key={claim.assertion_id}>
                <code>{claim.entity_id}</code> / <code>{claim.property_key}</code> :
                {" "}<code>{claim.literal_value}</code> (source
                {" "}<code>{claim.source_revision_id}</code>) —
                {" "}{claim.novel_id === review.first.novel_id
                  ? "premier roman uniquement" : "second roman uniquement"}
              </li>)}
          </ul>
          <ul aria-label="Écarts de fiches entre romans fictifs">
            {displayedClaims.differences.map(pair =>
              <li key={pair.first.assertion_id + ":" + pair.second.assertion_id}>
                <code>{pair.first.entity_id}</code> /
                <code>{pair.first.property_key}</code> :
                {" "}<code>{pair.first.literal_value}</code> (source
                {" "}<code>{pair.first.source_revision_id}</code>) contre
                {" "}<code>{pair.second.literal_value}</code> (source
                {" "}<code>{pair.second.source_revision_id}</code>)
                {" "}— à examiner par l'auteur, sans résolution automatique
              </li>,
            )}
          </ul>
          <p>Les accords sont uniquement des valeurs littérales identiques ;
            ils ne prouvent ni un canon universel ni une cohérence générale.</p>
        </>}
    </section>
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
