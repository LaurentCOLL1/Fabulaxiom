import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import M32P3FictionalCommandWorkshop from "./M32P3FictionalCommandWorkshop";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import { startP3FictionalState } from "./m32P3FictionalCommandContract";

/** No disk, IPC, production sources, real worlds or registered accounts. */
const historical: M32ChronologyProjection = {
  universe_id: "fiction-history-view", reader_reveal_status: "not_authored",
  anchors: [
    { id:"old-a", universe_id:"fiction-history-view", status:"superseded",
      time_kind:"unknown", calendar_name:null, fictional_label:null,
      precision_text:null, source_revision_id:null },
    { id:"old-b", universe_id:"fiction-history-view", status:"revoked",
      time_kind:"unknown", calendar_name:null, fictional_label:null,
      precision_text:null, source_revision_id:null },
    { id:"current-c", universe_id:"fiction-history-view", status:"current",
      time_kind:"unknown", calendar_name:null, fictional_label:null,
      precision_text:null, source_revision_id:null },
  ],
  precedences: [
    { id:"old-link", universe_id:"fiction-history-view",
      before_anchor_id:"old-a", after_anchor_id:"old-b", status:"revoked",
      reason:"<script>fiction only</script>" },
  ],
  narration: [],
};
describe("M3.2 P3e fictitious history inspection",()=>{
  it("01 keeps obsolete anchors and links visible in a separate read-only panel",()=>{
    const html=renderToStaticMarkup(createElement(M32P3FictionalCommandWorkshop,{
      initial:historical,revisions:[],
    }));
    expect(html).toContain("P3e historique consultable des décisions fictives");
    expect(html).toContain("Ancres fictives archivées");
    expect(html).toContain("Relations fictives archivées");
    expect(html).toContain("Journal fictif des actions acceptées");
    expect(html).toContain("old-a");
    expect(html).toContain("old-b");
    expect(html).toContain("old-link");
    expect(html).toContain("statut historique : superseded");
    expect(html).toContain("relation révoquée");
    expect(html).toContain("Aucun historique n");
  });
  it("02 escapes hostile-looking historical reason without treating it as executable markup",()=>{
    const html=renderToStaticMarkup(createElement(M32P3FictionalCommandWorkshop,{
      initial:historical,revisions:[],
    }));
    expect(html).not.toContain("<script>fiction only</script>");
    expect(html).toContain("&lt;script&gt;fiction only&lt;/script&gt;");
    expect(html).not.toContain("invoke(");
  });
  it("03 preserves the input and distinguishes historical rows from active relations",()=>{
    const before=JSON.stringify(historical);
    const state=startP3FictionalState(historical);
    expect(state.draft.snapshot.anchors.filter(a=>a.status==="current"))
      .toHaveLength(1);
    expect(state.draft.snapshot.precedences.filter(e=>e.status==="current"))
      .toHaveLength(0);
    expect(state.draft.snapshot.precedences.filter(e=>e.status==="revoked"))
      .toHaveLength(1);
    expect(state.draft.audit).toHaveLength(0);
    expect(state.real_g3_authorized).toBe(false);
    expect(JSON.stringify(historical)).toBe(before);
  });
});
