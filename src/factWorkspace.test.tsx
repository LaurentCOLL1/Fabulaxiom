import {describe,it,expect} from "vitest";
import {renderToStaticMarkup} from "react-dom/server";
import {createElement} from "react";
import {
  decodeFactSnapshot,decodeReviewSnapshot,decodeReviewHistory,
  quoteFromSelection,verifySourceEvidence,reviewAction,formatFactError,
  STATUS_LABELS,
} from "./factWorkspace";
import FactWorkspace from "./FactWorkspace";

const f={id:"f1",entity_id:"e1",universe_id:"u1",fact_key:"lieu",
  fact_value:"Place",provenance_kind:"sourced" as const,validity_kind:"relative",
  validity_text:"après",created_at_utc:"2026-10-09"};
const src={id:"s1",fact_id:"f1",universe_id:"u1",revision_id:"r1",
  start_byte:6,end_byte:11,quoted_text:"🐈 "};
const facts={universe_id:"u1",records:[{fact:f,source:src}]};
const reviews={universe_id:"u1",reviews:[{fact_id:"f1",universe_id:"u1",status:"draft",revision_number:0}]};
const history={state:reviews.reviews[0],events:[]};

describe("M2.5 user-visible narrative fact governance",()=>{
  it("renders a dedicated workspace even before IPC data is loaded",()=>{
    const html=renderToStaticMarkup(createElement(FactWorkspace));
    expect(html).toContain("Faits narratifs et canon");
    expect(html).toContain("Aucune promotion automatique");
    expect(html).toContain("fact-universe");
  });
  it("rejects absent, cross-universe and malformed fact snapshots",()=>{
    expect(decodeFactSnapshot(facts,"u1").records[0].source?.quoted_text).toBe("🐈 ");
    expect(()=>decodeFactSnapshot(facts,"u2")).toThrow(/invalide/);
    expect(()=>decodeFactSnapshot({...facts,records:[{fact:f,source:null}]},"u1"))
      .toThrow(/citation manquante/);
    expect(()=>decodeFactSnapshot({...facts,records:[{fact:f,source:{...src,universe_id:"u2"}}]},"u1"))
      .toThrow(/citation incohérente/);
    expect(()=>decodeFactSnapshot({...facts,records:[{fact:{...f,provenance_kind:"unsourced"},source:src}]},"u1"))
      .toThrow(/sans source/);
  });
  it("rejects malformed statuses and cross-universe review rows",()=>{
    expect(decodeReviewSnapshot(reviews,"u1").reviews[0].status).toBe("draft");
    expect(()=>decodeReviewSnapshot({...reviews,reviews:[{...reviews.reviews[0],status:"promoted"}]},"u1"))
      .toThrow(/statut/);
    expect(()=>decodeReviewSnapshot({...reviews,reviews:[{...reviews.reviews[0],universe_id:"u2"}]},"u1"))
      .toThrow(/statut/);
  });
  it("validates append-only review chain before rendering history",()=>{
    expect(decodeReviewHistory(history,"f1","u1").events).toHaveLength(0);
    const event={id:"review1",fact_id:"f1",universe_id:"u1",revision_number:1,
      previous_status:"draft",next_status:"suggestion",action_kind:"set_status",
      reviewer_label:"Label déclaré",reason:"Motif",recorded_at_utc:"2026-10-09"};
    const good={state:{...history.state,status:"suggestion",revision_number:1},events:[event]};
    expect(decodeReviewHistory(good,"f1","u1").state.status).toBe("suggestion");
    expect(()=>decodeReviewHistory({...good,events:[{...event,previous_status:"canon"}]},"f1","u1"))
      .toThrow(/chaîne/);
    expect(()=>decodeReviewHistory(good,"f2","u1")).toThrow(/autre fait/);
    expect(()=>decodeReviewHistory({...good,state:{...good.state,revision_number:2}},"f1","u1"))
      .toThrow(/état courant/);
  });
  it("maps selection UTF-16 to exact UTF-8 byte offsets",()=>{
    const rev={id:"r1",content:"Été 🐈 magique"};
    const q=quoteFromSelection(rev,0,6);
    expect(q).toEqual({revision_id:"r1",start_byte:0,end_byte:10,quoted_text:"Été 🐈"});
    expect(quoteFromSelection(rev,4,6)).toMatchObject({start_byte:6,end_byte:10,quoted_text:"🐈"});
    expect(()=>quoteFromSelection(rev,4,5)).toThrow(/Unicode/);
    expect(()=>quoteFromSelection(rev,2,2)).toThrow(/non vide/);
  });
  it("verifies exact historical revision content, not just the claimed quote",()=>{
    const evidence={fact_id:"f1",universe_id:"u1",revision_id:"r1",scene_id:"scene1",
      revision_number:1,content:"Été 🐈 magique",quoted_text:"🐈 ",
      start_byte:5,end_byte:10};
    expect(verifySourceEvidence(evidence,"u1",src).scene_id).toBe("scene1");
    expect(()=>verifySourceEvidence({...evidence,content:"Été ! magique"},"u1",src))
      .toThrow(/texte cité/);
    expect(()=>verifySourceEvidence({...evidence,universe_id:"u2"},"u1",src))
      .toThrow(/incohérente/);
    expect(()=>verifySourceEvidence({...evidence,start_byte:4},"u1",src))
      .toThrow(/incohérente/);
  });
  it("never promotes suggestions silently; explicit canon approval and revocation only",()=>{
    expect(reviewAction("draft","suggestion",false))
      .toEqual({action_kind:"set_status",confirmation_phrase:null});
    expect(reviewAction("ambiguous","contradictory",false).action_kind).toBe("set_status");
    expect(()=>reviewAction("suggestion","canon",false)).toThrow(/humaine explicite/);
    expect(reviewAction("suggestion","canon",true))
      .toEqual({action_kind:"approve_canon",confirmation_phrase:"APPROVE_CANON"});
    expect(()=>reviewAction("canon","draft",false)).toThrow(/humaine explicite/);
    expect(reviewAction("canon","variant",true))
      .toEqual({action_kind:"revoke_canon",confirmation_phrase:"REVOKE_CANON"});
    expect(()=>reviewAction("canon","canon",true)).toThrow(/différent/);
  });
  it("distinguishes each uncertain state and exposes deterministic IPC errors",()=>{
    expect(new Set(["unknown","ambiguous","contradictory","variant"].map(
      s=>STATUS_LABELS[s as "unknown"|"ambiguous"|"contradictory"|"variant"]
    )).size).toBe(4);
    expect(formatFactError({code:"stale_revision",message:"Version périmée."}))
      .toBe("[stale_revision] Version périmée.");
    expect(formatFactError('{"code":"cross_universe","message":"Refus."}'))
      .toBe("[cross_universe] Refus.");
    expect(formatFactError(new Error("IPC hors service"))).toBe("IPC hors service");
  });
});
