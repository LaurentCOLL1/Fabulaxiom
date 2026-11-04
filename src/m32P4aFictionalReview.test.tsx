import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import M32P4aFictionalReview from "./M32P4aStageReviewPanel";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import {
  applyP3FictionalCommand, startP3FictionalState,
  type P3Command,
} from "./m32P3FictionalCommandContract";
import { confirmP4aFictionalPlan, confirmP4cFictionalPlanWithReceipt, stageP4aFictionalPlan } from "./m32P4aFictionalReview";

const fixture: M32ChronologyProjection = {
  universe_id: "fiction-p4a-preview", reader_reveal_status: "not_authored",
  anchors: [
    { id:"A",universe_id:"fiction-p4a-preview",status:"current",time_kind:"unknown",
      calendar_name:null,fictional_label:null,precision_text:null,source_revision_id:null },
    { id:"B",universe_id:"fiction-p4a-preview",status:"current",time_kind:"unknown",
      calendar_name:null,fictional_label:null,precision_text:null,source_revision_id:null },
  ], precedences:[], narration:[],
};
const initial = () => startP3FictionalState(fixture,[]);
const edge: P3Command = {kind:"create_precedence",universe_id:"fiction-p4a-preview",
  relation:{before_anchor_id:"A",after_anchor_id:"B",reason:"Lien humain inventé"}};

describe("M3.2 P4a staged human review (fiction only)",()=>{
  it("01 previews before/after without mutation or production admission",()=>{
    const state=initial(),before=JSON.stringify(state);
    const plan=stageP4aFictionalPlan(state,edge);
    expect(JSON.stringify(state)).toBe(before);
    expect(plan.changes.created_precedence_ids).toEqual(["fiction-draft-0001"]);
    expect(plan.changes.created_anchor_ids).toEqual([]);
    expect(plan.changes.narration_unchanged).toBe(true);
    expect(plan.production_writer_admitted).toBe(false);
    expect(plan.real_g3_authorized).toBe(false);
    expect(state.commands_committed).toBe(0);
  });
  it("02 requires a human reason and commits only into a NEW fictional state",()=>{
    const state=initial(),plan=stageP4aFictionalPlan(state,edge);
    expect(()=>confirmP4aFictionalPlan(state,plan,"")).toThrow();
    expect(()=>confirmP4aFictionalPlan(state,plan,"x".repeat(161))).toThrow();
    const after=confirmP4aFictionalPlan(state,plan,"Choix de l'auteur");
    expect(after.commands_committed).toBe(1);
    expect(after.draft.snapshot.precedences).toHaveLength(1);
    expect(state.draft.snapshot.precedences).toHaveLength(0);
    expect(after.real_g3_authorized).toBe(false);
    const { state: documented, receipt } = confirmP4cFictionalPlanWithReceipt(
      state, plan, "  Motif personnel inventé  ",
    );
    expect(documented).toEqual(after);
    expect(receipt.human_reason).toBe("Motif personnel inventé");
    expect(receipt.before_commands).toBe(0);
    expect(receipt.after_commands).toBe(1);
    expect(receipt.created_precedence_ids).toEqual(["fiction-draft-0001"]);
    expect(receipt.data_origin).toBe("fictional_browser_memory_only");
    expect(receipt.real_g3_authorized).toBe(false);
    expect(receipt.production_writer_admitted).toBe(false);
  });
  it("03 rejects stale baseline even when a candidate looked valid earlier",()=>{
    const state=initial(),plan=stageP4aFictionalPlan(state,edge);
    const changed=applyP3FictionalCommand(state,{
      kind:"create_anchor_with_optional_relation",universe_id:fixture.universe_id,
      time:{kind:"unknown",calendar:"",label:"",precision:""},relation:null,
    });
    expect(()=>confirmP4aFictionalPlan(changed,plan,"Je confirme")).toThrow(/périmée/);
    expect(changed.draft.snapshot.precedences).toHaveLength(0);
  });
  it("04 rejects a forged after-state, and leaves caller input unchanged",()=>{
    const before=initial(),plan=stageP4aFictionalPlan(before,edge);
    const fake={...plan,after_json:"{}",changes:{...plan.changes,created_precedence_ids:["fake"]}};
    const record=JSON.stringify(before);
    expect(()=>confirmP4aFictionalPlan(before,fake,"Motif")).toThrow(/modifiée/);
    expect(JSON.stringify(before)).toBe(record);
    expect(()=>confirmP4cFictionalPlanWithReceipt(before,fake,"Motif")).toThrow(/modifiée/);
  });
  it("05 refuses foreign universes, cycles and nonexistent IDs at staging",()=>{
    const before=initial(),original=JSON.stringify(before);
    expect(()=>stageP4aFictionalPlan(before,{...edge,universe_id:"fiction-foreign"})).toThrow();
    expect(()=>stageP4aFictionalPlan(before,{
      ...edge,relation:{...edge.relation,before_anchor_id:"missing"},
    } as P3Command)).toThrow();
    const added=applyP3FictionalCommand(before,edge);
    expect(()=>stageP4aFictionalPlan(added,{
      kind:"create_precedence",universe_id:fixture.universe_id,
      relation:{before_anchor_id:"B",after_anchor_id:"A",reason:"Cycle"},
    })).toThrow(/cycle/);
    expect(JSON.stringify(before)).toBe(original);
  });
  it("06 renders an isolated, escaped, visibly non-production human review",()=>{
    const html=renderToStaticMarkup(createElement(M32P4aFictionalReview,{
      initial:initial(),command:edge,
    }));
    expect(html).toContain("P4a — vérifier avant de confirmer");
    expect(html).toContain("Prévisualiser sans modifier");
    expect(html).toContain("Journal des confirmations fictives en mémoire");
    expect(html).toContain("ni signature, ni sauvegarde");
    expect(html).not.toContain("Annuler la prévisualisation fictive");
    expect(html).toContain("Aucune commande Tauri");
    expect(html).toContain("STOP_UNAVAILABLE");
    expect(html).not.toContain("invoke(");
  });
});
