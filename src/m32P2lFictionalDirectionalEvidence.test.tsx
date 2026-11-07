import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32P2lFictionalDirectionalEvidence, {
  previewP2lFictionalDirectionalEvidence,
} from "./M32P2lFictionalDirectionalEvidence";
import type { P2iFictionalEdge, P2iFictionalInput } from "./M32P2iFictionalImpactReview";
const world = "p2l-fiction-only";
function edge(id: string, from: string, to: string,
  origin: P2iFictionalEdge["origin"] = "original"): P2iFictionalEdge {
  return { id, universe_id: world, before_anchor_id: from, after_anchor_id: to, origin };
}
const input: P2iFictionalInput = {
  data_origin: "fictional_browser_memory_only",
  production_writer_admitted: false, real_g3_authorized: false, universe_id: world,
  active_before: [edge("rm-in", "A", "B"), edge("rm-out", "B", "C"),
    edge("same", "A", "D"), edge("remote", "X", "Y")],
  active_after: [edge("same", "A", "D"), edge("remote", "X", "Y"),
    edge("add-in", "E", "B", "restatement"), edge("add-out", "B", "F")],
};
describe("M3.2 P2l direct fictional anchor directions", () => {
  it("01 separates four direct groups and never mutates input", () => {
    const before = JSON.stringify(input);
    const r = previewP2lFictionalDirectionalEvidence(input, world, "B");
    expect(r.removed_incoming.map(e => e.id)).toEqual(["rm-in"]);
    expect(r.removed_outgoing.map(e => e.id)).toEqual(["rm-out"]);
    expect(r.added_incoming.map(e => e.id)).toEqual(["add-in"]);
    expect(r.added_outgoing.map(e => e.id)).toEqual(["add-out"]);
    expect(r.data_origin).toBe("fictional_browser_memory_only");
    expect(r.production_writer_admitted).toBe(false);
    expect(r.real_g3_authorized).toBe(false);
    expect(JSON.stringify(input)).toBe(before);
  });
  it("02 excludes unchanged/unrelated anchors and rejects non-touched selections", () => {
    const r = previewP2lFictionalDirectionalEvidence(input, world, "A");
    expect(r.removed_outgoing.map(e => e.id)).toEqual(["rm-in"]);
    expect(r.removed_incoming).toEqual([]);
    expect(r.added_incoming).toEqual([]);
    expect(r.added_outgoing).toEqual([]);
    for (const a of ["D", "X", "unknown", ""]) {
      expect(() => previewP2lFictionalDirectionalEvidence(input, world, a)).toThrow();
    }
  });
  it("03 preserves lexical full-value order within directions only", () => {
    const unsorted = { ...input,
      active_before: [edge("z", "A", "B"), edge("a", "C", "B"), edge("q", "B", "D")],
      active_after: [edge("v", "E", "B"), edge("b", "F", "B")],
    };
    const r = previewP2lFictionalDirectionalEvidence(unsorted, world, "B");
    expect(r.removed_incoming.map(e => e.id)).toEqual(["a", "z"]);
    expect(r.removed_outgoing.map(e => e.id)).toEqual(["q"]);
    expect(r.added_incoming.map(e => e.id)).toEqual(["b", "v"]);
    expect(r.added_outgoing).toEqual([]);
  });
  it("04 does not equate reused IDs with unchanged assertions", () => {
    const moved = { ...input,
      active_before: [edge("reuse", "A", "B")],
      active_after: [edge("reuse", "B", "C", "restatement")],
    };
    const r = previewP2lFictionalDirectionalEvidence(moved, world, "B");
    expect(r.removed_incoming[0].origin).toBe("original");
    expect(r.added_outgoing[0].origin).toBe("restatement");
    expect(r.removed_outgoing).toEqual([]);
    expect(r.added_incoming).toEqual([]);
  });
  it("05 refuses forged writer, G3, source and foreign universe", () => {
    expect(() => previewP2lFictionalDirectionalEvidence(input, "foreign", "B")).toThrow();
    for (const patch of [{ data_origin: "operator_disk" },
      { production_writer_admitted: true }, { real_g3_authorized: true }]) {
      expect(() => previewP2lFictionalDirectionalEvidence({
        ...input, ...patch,
      } as unknown as P2iFictionalInput, world, "B")).toThrow();
    }
  });
  it("06 refuses cycles, self-links and exact duplicates", () => {
    for (const changed of [
      { active_after: [edge("x", "A", "B"), edge("y", "B", "A")] },
      { active_before: [edge("x", "B", "B")] },
      { active_before: [edge("x", "A", "B"), edge("x", "A", "B")] },
    ]) {
      expect(() => previewP2lFictionalDirectionalEvidence({
        ...input, ...changed,
      }, world, "B")).toThrow();
    }
  });
  it("07 renders four accessible read-only groups and no narrative inference", () => {
    const html = renderToStaticMarkup(createElement(M32P2lFictionalDirectionalEvidence,
      { input, expectedUniverse: world, selectedAnchor: "B" }));
    for (const label of ["Retirées vers l’ancre (1)", "Retirées depuis l’ancre (1)",
      "Ajoutées vers l’ancre (1)", "Ajoutées depuis l’ancre (1)"]) {
      expect(html).toContain(label);
    }
    expect(html).toContain("Aucune transitivité, date");
    expect(html).toContain("G3 STOP_UNAVAILABLE");
    expect(html).not.toContain("<button");
    expect(html).not.toContain("<input");
  });
  it("08 escapes hostile invented IDs and refuses without leaking assertions", () => {
    const evil = "<img src=x onerror=alert(1)>";
    const fake = { ...input,
      active_before: [edge(evil, evil, "B")], active_after: [],
    };
    const ok = renderToStaticMarkup(createElement(M32P2lFictionalDirectionalEvidence,
      { input: fake, expectedUniverse: world, selectedAnchor: evil }));
    expect(ok).toContain("&lt;img");
    expect(ok).not.toContain("<img");
    const denied = renderToStaticMarkup(createElement(M32P2lFictionalDirectionalEvidence, {
      input: { ...fake, real_g3_authorized: true } as unknown as P2iFictionalInput,
      expectedUniverse: world, selectedAnchor: evil,
    }));
    expect(denied).toContain("Directions fictives refusées");
    expect(denied).not.toContain(evil);
    expect(denied).not.toContain("<li");
  });
});
