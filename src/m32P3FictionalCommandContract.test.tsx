import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import type { FictionalRevision } from "./m32FictionalManualChronology";
import M32P3FictionalCommandWorkshop from "./M32P3FictionalCommandWorkshop";
import {
  P3_NEW_ANCHOR, applyP3FictionalCommand,
  readP3FictionalSnapshot, startP3FictionalState,
  type P3Command,
} from "./m32P3FictionalCommandContract";

const first: M32ChronologyProjection = {
  universe_id: "fiction-one", reader_reveal_status: "not_authored",
  anchors: ["A","B"].map((id,index) => ({
    id, universe_id: "fiction-one", time_kind: "unknown" as const,
    status: "current" as const, calendar_name: null, fictional_label: null,
    precision_text: null, source_revision_id: index === 0 ? "r2" : null,
  })),
  precedences: [], narration: [
    { universe_id: "fiction-one", novel_id: "n1", novel_title: "Roman un",
      chapter_id: "c1", chapter_title: "Chapitre un", chapter_order: 0,
      scene_id: "s1", scene_title: "Scène fictive", scene_order: 0 },
    { universe_id: "fiction-one", novel_id: "n2", novel_title: "Roman deux",
      chapter_id: "c2", chapter_title: "Chapitre deux", chapter_order: 0,
      scene_id: "s2", scene_title: "Autre scène fictive", scene_order: 0 },
  ],
};
const revisions: readonly FictionalRevision[] = [
  { universe_id:"fiction-one", novel_id:"n1", scene_id:"s1",
    revision_id:"r2", revision_label:"Ancienne rédaction" },
  { universe_id:"fiction-one", novel_id:"n1", scene_id:"s1",
    revision_id:"r3", revision_label:"Nouvelle rédaction" },
  { universe_id:"fiction-one", novel_id:"n2", scene_id:"s2",
    revision_id:"r4", revision_label:"Autre roman" },
];
const start = () => startP3FictionalState(first,revisions);
const unknown = { kind:"unknown" as const, calendar:"", label:"", precision:"" };
function anchor(
  universe_id = "fiction-one", relation: null | {
    before_anchor_id:string;after_anchor_id:string;reason:string
  } = null,
): P3Command {
  return { kind:"create_anchor_with_optional_relation", universe_id,
    time:unknown, relation };
}
function edge(before:string,after:string): P3Command {
  return {kind:"create_precedence",universe_id:"fiction-one",relation:{
    before_anchor_id:before,after_anchor_id:after,reason:"Précédence humaine explicite",
  }};
}
describe("M3.2 P3a browser-only typed chronology command contract",()=>{
  it("01 is strictly invented, does not authorize a real writer",()=>{
    const s=start();
    expect(s.data_origin).toBe("fictional_browser_memory_only");
    expect(s.real_g3_authorized).toBe(false);
    expect(s.commands_committed).toBe(0);
    expect(readP3FictionalSnapshot(s,"fiction-one").reader_reveal_status).toBe("not_authored");
  });
  it("02 accepts an unknown-time anchor without inventing an order",()=>{
    const s=start(), next=applyP3FictionalCommand(s,anchor());
    expect(next.commands_committed).toBe(1);
    expect(next.draft.snapshot.anchors.at(-1)?.time_kind).toBe("unknown");
    expect(next.draft.snapshot.precedences).toHaveLength(0);
    expect(s.draft.snapshot.anchors).toHaveLength(2);
  });
  it("03 atomically creates an anchor and a human-authorized relation",()=>{
    const next=applyP3FictionalCommand(start(),anchor("fiction-one",{
      before_anchor_id:"A",after_anchor_id:P3_NEW_ANCHOR,reason:"A précède la nouvelle date",
    }));
    expect(next.draft.snapshot.anchors.at(-1)?.id).toBe("fiction-draft-0001");
    expect(next.draft.snapshot.precedences.at(-1)?.after_anchor_id).toBe("fiction-draft-0001");
    expect(next.draft.audit.map(a=>a.action)).toEqual(["anchor_created","precedence_created"]);
    expect(next.commands_committed).toBe(1);
  });
  it("04 invalid relation causes complete rollback of the invented state",()=>{
    const prior=start();
    expect(()=>applyP3FictionalCommand(prior,anchor("fiction-one",{
      before_anchor_id:"not-found",after_anchor_id:P3_NEW_ANCHOR,reason:"Erreur fictive",
    }))).toThrow();
    expect(prior.draft.snapshot.anchors).toHaveLength(2);
    expect(prior.draft.snapshot.precedences).toHaveLength(0);
    expect(prior.commands_committed).toBe(0);
  });
  it("05 rejects cycles, duplicates and inaccessible historical anchors",()=>{
    const one=applyP3FictionalCommand(start(),edge("A","B"));
    expect(()=>applyP3FictionalCommand(one,edge("B","A"))).toThrow(/cycle/);
    expect(()=>applyP3FictionalCommand(one,edge("A","B"))).toThrow();
    expect(()=>applyP3FictionalCommand(one,edge("A","historical-id"))).toThrow();
    expect(one.draft.snapshot.precedences).toHaveLength(1);
  });
  it("06 refuses other universes, real-looking profile and malformed origin",()=>{
    const s=start();
    expect(()=>applyP3FictionalCommand(s,anchor("fiction-two"))).toThrow();
    expect(()=>readP3FictionalSnapshot(s,"u1")).toThrow();
    expect(()=>readP3FictionalSnapshot({...s,data_origin:"sqlite"} as never,"fiction-one")).toThrow();
    expect(()=>applyP3FictionalCommand({...s,real_g3_authorized:true} as never,anchor())).toThrow();
  });
  it("07 exact historical revision is selected by immutable r2, not guessed r3",()=>{
    const next=applyP3FictionalCommand(start(),{
      kind:"create_anchor_with_optional_relation",universe_id:"fiction-one",
      time:{kind:"exact",calendar:"Calendrier des marées",
        label:"Quatrième cloche",precision:"",
        source_revision_id:"r2",source_scene_id:"s1"},
      relation:null,
    });
    expect(next.draft.snapshot.anchors.at(-1)?.source_revision_id).toBe("r2");
    expect(next.draft.snapshot.narration.map(x=>x.novel_id)).toEqual(["n1","n2"]);
    expect(next.draft.snapshot.reader_reveal_status).toBe("not_authored");
    expect(()=>applyP3FictionalCommand(start(),{
      kind:"create_anchor_with_optional_relation",universe_id:"fiction-one",
      time:{kind:"relative",calendar:"",label:"",precision:"",
        source_revision_id:"r2",source_scene_id:"s2"},
      relation:null,
    })).toThrow();
  });
  it("08 never accepts the new anchor placeholder in a standalone precedence",()=>{
    expect(()=>applyP3FictionalCommand(start(),edge("A",P3_NEW_ANCHOR))).toThrow();
    expect(()=>applyP3FictionalCommand(start(),anchor("fiction-one",{
      before_anchor_id:"A",after_anchor_id:"B",reason:"Both existing",
    }))).toThrow();
  });
  it("09 renders explicit fictional-only UI with accessible native fields",()=>{
    const html=renderToStaticMarkup(createElement(M32P3FictionalCommandWorkshop,{
      initial:first,revisions,
    }));
    expect(html).toContain("Simulation navigateur exclusivement");
    expect(html).toContain("ne communique pas avec Rust");
    expect(html).toContain("Exécuter la commande fictive en mémoire");
    expect(html).toContain("Révision narrative historique");
    expect(html).toContain("r2");
    expect(html).toContain("Aucun");
    expect(html).toContain('role="status"');
    expect(html).not.toContain("invoke(");
  });
  it("10 refuses mixed-world forged fixture without rendering its contents",()=>{
    const mixed={...first,anchors:[{...first.anchors[0],universe_id:"foreign"},...first.anchors.slice(1)]};
    const html=renderToStaticMarkup(createElement(M32P3FictionalCommandWorkshop,{
      initial:mixed,revisions,
    }));
    expect(html).toContain("Atelier P3a refusé");
    expect(html).not.toContain("Révision narrative historique");
  });
  it("11 preserves script-shaped invented labels as inert escaped content",()=>{
    const hostile={...first,narration:first.narration.map((n,i)=>i===0?{...n,scene_title:"<script>inert()</script>"}:n)};
    const html=renderToStaticMarkup(createElement(M32P3FictionalCommandWorkshop,{
      initial:hostile,revisions,
    }));
    expect(html).not.toContain("<script>inert()");
    expect(html).toContain("Simulation navigateur");
  });
});
