import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import M32P3FictionalCommandWorkshop from "./M32P3FictionalCommandWorkshop";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import type { FictionalRevision } from "./m32FictionalManualChronology";
import {
  applyP3FictionalCommand, startP3FictionalState,
} from "./m32P3FictionalCommandContract";

/** P3d: invented browser-memory contract; no Tauri, IPC, disk or operator data. */
const snapshot: M32ChronologyProjection = {
  universe_id: "fiction-reversible-world", reader_reveal_status: "not_authored",
  anchors: [
    { id:"A", universe_id:"fiction-reversible-world", status:"current",
      time_kind:"exact", calendar_name:"Calendrier inventé",
      fictional_label:"Troisième cloche", precision_text:null,
      source_revision_id:"fiction-r2" },
    { id:"B", universe_id:"fiction-reversible-world", status:"current",
      time_kind:"unknown", calendar_name:null, fictional_label:null,
      precision_text:null, source_revision_id:null },
  ],
  precedences: [
    { id:"edge-ab", universe_id:"fiction-reversible-world",
      before_anchor_id:"A", after_anchor_id:"B", status:"current",
      reason:"Décision humaine fictive" },
  ],
  narration: [{
    universe_id:"fiction-reversible-world", novel_id:"fiction-novel",
    novel_title:"Roman fictif", chapter_id:"fiction-chapter",
    chapter_title:"Chapitre fictif", chapter_order:0,
    scene_id:"fiction-scene", scene_title:"Scène fictive", scene_order:0,
  }],
};
const revisions: readonly FictionalRevision[] = [{
  universe_id:"fiction-reversible-world", novel_id:"fiction-novel",
  scene_id:"fiction-scene", revision_id:"fiction-r2",
  revision_label:"Version historique inventée",
}];
const start = () => startP3FictionalState(snapshot,revisions);
const revoke = (reason = "Révocation humaine explicite", universe_id = snapshot.universe_id) => ({
  kind:"revoke_precedence" as const, universe_id, precedence_id:"edge-ab",reason,
});
const correction = (anchor_id = "A", universe_id = snapshot.universe_id) => ({
  kind:"supersede_anchor" as const,universe_id,anchor_id,
  time:{kind:"relative" as const,calendar:"",label:"",precision:""},
});

describe("M3.2 P3d reversible fictional correction/revocation",()=>{
  it("01 renders separate explicit actions and preflight without persistence claims",()=>{
    const html=renderToStaticMarkup(createElement(M32P3FictionalCommandWorkshop,{
      initial:snapshot,revisions,
    }));
    for(const text of ["P3d révocation explicite fictive",
      "Révoquer explicitement le lien fictif",
      "P3d correction historique fictive",
      "Remplacer l&#x27;ancre fictive et conserver l&#x27;historique",
      "Contrôle avant correction","Simulation navigateur exclusivement",
      "ne communique pas avec Rust","Ordre de révélation au lecteur"]){
      expect(html).toContain(text);
    }
    expect(html).not.toContain("invoke(");
  });
  it("02 revokes the chosen current edge without deleting its historical assertion",()=>{
    const before=start(), after=applyP3FictionalCommand(before,revoke());
    expect(before.draft.snapshot.precedences[0].status).toBe("current");
    expect(after.draft.snapshot.precedences[0].status).toBe("revoked");
    expect(after.draft.snapshot.precedences).toHaveLength(1);
    expect(after.draft.audit.slice(-1)[0]?.action).toBe("precedence_revoked");
    expect(after.commands_committed).toBe(1);
    expect(after.real_g3_authorized).toBe(false);
  });
  it("03 disallows silent revocation and wrong-universe IDs without mutation",()=>{
    const before=start(), original=JSON.stringify(before);
    expect(()=>applyP3FictionalCommand(before,revoke(""))).toThrow();
    expect(()=>applyP3FictionalCommand(before,revoke("Motif","fiction-another"))).toThrow();
    expect(()=>applyP3FictionalCommand(before,{
      ...revoke(),precedence_id:"missing",
    })).toThrow();
    expect(JSON.stringify(before)).toBe(original);
  });
  it("04 refuses correction with active linked edge, then accepts after explicit revocation",()=>{
    const before=start(), original=JSON.stringify(before);
    expect(()=>applyP3FictionalCommand(before,correction())).toThrow(/révoquer/);
    expect(JSON.stringify(before)).toBe(original);
    const removed=applyP3FictionalCommand(before,revoke());
    const after=applyP3FictionalCommand(removed,correction());
    const old=after.draft.snapshot.anchors.find(a=>a.id==="A");
    const newer=after.draft.snapshot.anchors.find(a=>a.id==="fiction-draft-0001");
    expect(old?.status).toBe("superseded");
    expect(newer?.status).toBe("current");
    expect(newer?.source_revision_id).toBe("fiction-r2");
    expect(after.draft.snapshot.anchors).toHaveLength(3);
    expect(after.draft.snapshot.narration).toEqual(before.draft.snapshot.narration);
    expect(after.draft.snapshot.reader_reveal_status).toBe("not_authored");
    expect(after.draft.audit.map(a=>a.action)).toEqual([
      "precedence_revoked","anchor_superseded",
    ]);
    expect(after.commands_committed).toBe(2);
    expect(removed.draft.snapshot.anchors[0].status).toBe("current");
  });
  it("05 fails closed for historical or foreign anchors and malformed corrected date",()=>{
    const after=applyP3FictionalCommand(start(),revoke());
    const original=JSON.stringify(after);
    expect(()=>applyP3FictionalCommand(after,correction("missing"))).toThrow();
    expect(()=>applyP3FictionalCommand(after,correction("A","fiction-foreign"))).toThrow();
    expect(()=>applyP3FictionalCommand(after,{
      ...correction(),time:{kind:"exact" as const,calendar:"",label:"",precision:""},
    })).toThrow();
    expect(JSON.stringify(after)).toBe(original);
  });
  it("06 cannot revoke twice, correct twice or silently rewrite the old anchor",()=>{
    const first=applyP3FictionalCommand(start(),revoke());
    expect(()=>applyP3FictionalCommand(first,revoke())).toThrow();
    const after=applyP3FictionalCommand(first,correction());
    expect(()=>applyP3FictionalCommand(after,correction())).toThrow();
    expect(after.draft.snapshot.anchors.find(a=>a.id==="A")?.status).toBe("superseded");
    expect(after.draft.snapshot.precedences[0].status).toBe("revoked");
  });
});
