import type { ReactElement } from "react";
import {
  previewP2iFictionalImpact,
  type P2iFictionalEdge,
  type P2iFictionalInput,
} from "./M32P2iFictionalImpactReview";

/**
 * P2j: read-only, fiction-only list of anchors directly mentioned by changed
 * precedence assertions. An anchor is NOT a dated event, narrative order,
 * inferred transitive consequence, or authorization for a writer.
 * No production import from App.tsx; never reads storage or invokes Tauri.
 */
export type P2jFictionalTouchedAnchor = Readonly<{
  anchor_id: string;
  in_removed: boolean;
  in_added: boolean;
}>;

export type P2jFictionalTouchedResult = Readonly<{
  anchors: readonly P2jFictionalTouchedAnchor[];
  data_origin: "fictional_browser_memory_only";
  production_writer_admitted: false;
  real_g3_authorized: false;
}>;

/** Reuses all P2i guards; only the endpoints of changed assertions count. */
export function previewP2jFictionalTouchedAnchors(
  input: P2iFictionalInput,
  expectedUniverse: string,
): P2jFictionalTouchedResult {
  const impact = previewP2iFictionalImpact(input, expectedUniverse);
  const touched = new Map<string, { in_removed: boolean; in_added: boolean }>();
  const include = (edges: readonly P2iFictionalEdge[], kind: "in_removed" | "in_added") => {
    for (const edge of edges) {
      for (const anchor_id of [edge.before_anchor_id, edge.after_anchor_id]) {
        const flags = touched.get(anchor_id) ?? { in_removed: false, in_added: false };
        flags[kind] = true;
        touched.set(anchor_id, flags);
      }
    }
  };
  include(impact.removed, "in_removed");
  include(impact.added, "in_added");
  // Display sorting is lexical by identifier, never a fictional chronology.
  const anchors = [...touched.entries()]
    .sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)
    .map(([anchor_id, flags]) => ({ anchor_id, ...flags }));
  return {
    anchors,
    data_origin: "fictional_browser_memory_only",
    production_writer_admitted: false,
    real_g3_authorized: false,
  };
}

export default function M32P2jFictionalTouchedAnchors({
  input, expectedUniverse,
}: { input: P2iFictionalInput; expectedUniverse: string }): ReactElement {
  let result: P2jFictionalTouchedResult;
  try {
    result = previewP2jFictionalTouchedAnchors(input, expectedUniverse);
  } catch {
    return <section role="alert" aria-label="Ancres fictives refusées">
      <h2>Ancres fictives refusées</h2>
      <p>Provenance ou relations non valides. Aucune commande exécutée.</p>
    </section>;
  }
  const categories = [
    { title: "Relations retirées uniquement", matches: (a: P2jFictionalTouchedAnchor) => a.in_removed && !a.in_added },
    { title: "Relations ajoutées uniquement", matches: (a: P2jFictionalTouchedAnchor) => a.in_added && !a.in_removed },
    { title: "Relations retirées et ajoutées", matches: (a: P2jFictionalTouchedAnchor) => a.in_added && a.in_removed },
  ];
  return <section aria-label="Ancres touchées par la correction fictive">
    <h2>Ancres touchées par des relations modifiées — fiction uniquement</h2>
    <p>Une ancre est listée si une relation retirée ou ajoutée la mentionne directement.</p>
    <p>Tri alphabétique des identifiants, sans déduction de date, d’ordre du monde total,
      de narration ou de révélation.</p>
    {categories.map(category => {
      const anchors = result.anchors.filter(category.matches);
      return <section key={category.title} aria-label={category.title}>
        <h3>{category.title} ({anchors.length})</h3>
        {anchors.length ? <ul>{anchors.map(anchor =>
          <li key={anchor.anchor_id}><code>{anchor.anchor_id}</code></li>,
        )}</ul> : <p>Aucune.</p>}
      </section>;
    })}
    <p>Lecture seule : aucune confirmation, aucun writer, aucune commande Tauri,
      aucune donnée opérateur. G3 STOP_UNAVAILABLE.</p>
  </section>;
}
