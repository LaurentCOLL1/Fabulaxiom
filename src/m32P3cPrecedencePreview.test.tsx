import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import M32P3FictionalCommandWorkshop from "./M32P3FictionalCommandWorkshop";
import { previewFictionalPrecedence } from "./m32FictionalManualChronology";
import {
  applyP3FictionalCommand, startP3FictionalState,
} from "./m32P3FictionalCommandContract";

const snapshot: M32ChronologyProjection = {
  universe_id:"fiction-one",reader_reveal_status:"not_authored",
  anchors:["A","B","C","D"].map(id=>({
    id,universe_id:"fiction-one",time_kind:"unknown" as const,
    status:"current" as const,calendar_name:null,fictional_label:null,
    precision_text:null,source_revision_id:null,
  })),
  precedences:[
    {id:"ab",universe_id:"fiction-one",before_anchor_id:"A",
      after_anchor_id:"B",status:"current",reason:"A avant B"},
    {id:"bc",universe_id:"fiction-one",before_anchor_id:"B",
      after_anchor_id:"C",status:"current",reason:"B avant C"},
  ],
  narration:[],
};
const state=()=>startP3FictionalState(snapshot);
describe("M3.2 P3c standalone fictional precedence preflight",()=>{
  it("01 renders two labelled explicit selectors and refuses empty submission",()=>{
    const html=renderToStaticMarkup(createElement(M32P3FictionalCommandWorkshop,{
      initial:snapshot,revisions:[],
    }));
    expect(html).toContain("P3c proposition de précédence fictive");
    expect(html).toContain("Première ancre : avant");
    expect(html).toContain("Deuxième ancre : après");
    expect(html).toContain("Justification humaine de la précédence");
    expect(html).toContain("Choisir deux ancres distinctes");
    expect(html).toContain("Valider le lien fictif après contrôle");
    expect(html).toContain("disabled");
    expect(html).toContain("ne communique pas avec Rust");
  });
  it("02 human-declared new edge is explicitly allowed and never infers revelation",()=>{
    const original=state();
    const allowed=previewFictionalPrecedence(original.draft,"C","D");
    expect(allowed.verdict).toBe("allowed");
    const next=applyP3FictionalCommand(original,{
      kind:"create_precedence",universe_id:"fiction-one",relation:{
        before_anchor_id:"C",after_anchor_id:"D",reason:"Auteur déclare C avant D",
      },
    });
    expect(next.draft.snapshot.precedences).toHaveLength(3);
    expect(next.draft.snapshot.precedences.slice(-1)[0].reason).toContain("Auteur");
    expect(next.draft.snapshot.reader_reveal_status).toBe("not_authored");
    expect(original.draft.snapshot.precedences).toHaveLength(2);
  });
  it("03 preflight explains cycles and duplicates without mutating the state",()=>{
    const prior=state(),fingerprint=JSON.stringify(prior);
    const cycle=previewFictionalPrecedence(prior.draft,"C","A");
    expect(cycle.verdict).toBe("blocked");
    expect(cycle.reason).toMatch(/cycle/);
    expect(cycle.witness_anchor_ids).toEqual(["C","A","B","C"]);
    expect(previewFictionalPrecedence(prior.draft,"A","B").verdict).toBe("blocked");
    expect(()=>applyP3FictionalCommand(prior,{
      kind:"create_precedence",universe_id:"fiction-one",
      relation:{before_anchor_id:"C",after_anchor_id:"A",reason:"Cycle illégitime"},
    })).toThrow();
    expect(JSON.stringify(prior)).toBe(fingerprint);
  });
  it("04 rejects absent/foreign anchors and retains incomparable pair",()=>{
    const prior=state();
    expect(previewFictionalPrecedence(prior.draft,"A","missing").verdict).toBe("blocked");
    expect(previewFictionalPrecedence(prior.draft,"","D").verdict).toBe("unselected");
    expect(previewFictionalPrecedence(prior.draft,"D","A").verdict).toBe("allowed");
    expect(prior.draft.snapshot.precedences.some(e=>e.after_anchor_id==="D")).toBe(false);
  });
});
