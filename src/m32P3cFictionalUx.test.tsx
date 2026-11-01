import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import M32P3FictionalCommandWorkshop from "./M32P3FictionalCommandWorkshop";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import {
  applyP3FictionalCommand, startP3FictionalState,
} from "./m32P3FictionalCommandContract";

const invented: M32ChronologyProjection = {
  universe_id:"fiction-p3c", reader_reveal_status:"not_authored",
  anchors:["A","B"].map(id=>({
    id, universe_id:"fiction-p3c", time_kind:"unknown" as const,
    status:"current" as const, calendar_name:null, fictional_label:null,
    precision_text:null, source_revision_id:null,
  })),
  precedences:[],
  narration:[{
    universe_id:"fiction-p3c", novel_id:"fiction-novel",
    novel_title:"Roman fictif", chapter_id:"fiction-chapter",
    chapter_title:"Chapitre fictif", chapter_order:0,
    scene_id:"fiction-scene", scene_title:"Scène fictive", scene_order:0,
  }],
};
const begin=()=>startP3FictionalState(invented,[]);
const link=(before_anchor_id:string,after_anchor_id:string,reason="Raison humaine")=>({
  kind:"create_precedence" as const, universe_id:"fiction-p3c",
  relation:{before_anchor_id,after_anchor_id,reason},
});
describe("M3.2 P3c isolated fictional chronology UX",()=>{
  it("01 exposes independent relation form and three separate order views",()=>{
    const html=renderToStaticMarkup(createElement(M32P3FictionalCommandWorkshop,{
      initial:invented,revisions:[],
    }));
    expect(html).toContain("Relation autonome entre ancres fictives");
    expect(html).toContain("Créer le lien fictif sans nouvelle date");
    expect(html).toContain("Chronologie du monde");
    expect(html).toContain("Ordre de narration");
    expect(html).toContain("Ordre de révélation au lecteur");
    expect(html).toContain("Non renseigné");
    expect(html).toContain("sans sauvegarde");
  });
  it("02 creates standalone link without inventing an anchor or reader reveal",()=>{
    const before=begin(),after=applyP3FictionalCommand(before,link("A","B"));
    expect(after.commands_committed).toBe(1);
    expect(after.draft.snapshot.anchors).toEqual(before.draft.snapshot.anchors);
    expect(after.draft.snapshot.precedences).toHaveLength(1);
    expect(after.draft.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("03 refuses cycle, self-link and empty human reason without changing state",()=>{
    const state=applyP3FictionalCommand(begin(),link("A","B"));
    const prior=JSON.stringify(state);
    expect(()=>applyP3FictionalCommand(state,link("B","A"))).toThrow(/cycle/);
    expect(()=>applyP3FictionalCommand(state,link("A","A"))).toThrow();
    expect(()=>applyP3FictionalCommand(state,link("A","B",""))).toThrow();
    expect(JSON.stringify(state)).toBe(prior);
  });
});
