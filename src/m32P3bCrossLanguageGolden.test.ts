import { describe, expect, it } from "vitest";
import fixture from "../fixtures/m32_p3b_typed_chronology_contract_v1.json";
import type { M32ChronologyProjection } from "./M32ChronologyPreview";
import type { FictionalRevision } from "./m32FictionalManualChronology";
import {
  P3_NEW_ANCHOR, applyP3FictionalCommand,
  startP3FictionalState,
} from "./m32P3FictionalCommandContract";

/**
 * P3b: independent TS reading of the SAME Git blob also included by a
 * cfg(test)-only Rust P2b actor fixture. No cross-runtime calls or IPC.
 */
function synthetic() {
  const snapshot: M32ChronologyProjection = {
    universe_id: fixture.universe_id, reader_reveal_status: "not_authored",
    anchors: [], precedences: [],
    narration: [{
      universe_id: fixture.universe_id, novel_id: fixture.novel_id,
      novel_title: "Roman entièrement inventé", chapter_id: "fiction-c1",
      chapter_title: "Chapitre inventé", chapter_order: 0,
      scene_id: fixture.scene_id, scene_title: "Scène inventée", scene_order: 0,
    }],
  };
  const history: readonly FictionalRevision[] = [
    { universe_id: fixture.universe_id, novel_id: fixture.novel_id,
      scene_id: fixture.scene_id, revision_id: fixture.historical_revision_id,
      revision_label: "Version historique fictive" },
    { universe_id: fixture.universe_id, novel_id: fixture.novel_id,
      scene_id: fixture.scene_id, revision_id: fixture.current_head_revision_id,
      revision_label: "Version fictive courante" },
  ];
  return startP3FictionalState(snapshot, history);
}
function applyGolden() {
  let state = synthetic();
  for (const op of fixture.anchor_commands) {
    const prior = state;
    const relation = op.relation === null ? null : {
      before_anchor_id: op.relation.before_anchor_id,
      after_anchor_id: op.relation.after_anchor_id,
      reason: op.relation.reason,
    };
    state = applyP3FictionalCommand(state, {
      kind: "create_anchor_with_optional_relation",
      universe_id: fixture.universe_id,
      time: {
        kind: "relative", calendar: "", label: "", precision: "",
        source_revision_id: op.source_revision_id,
        source_scene_id: fixture.scene_id,
      },
      relation,
    });
    expect(state.draft.snapshot.anchors.slice(-1)[0]?.id).toBe(op.anchor_id);
    expect(prior.commands_committed + 1).toBe(state.commands_committed);
    expect(prior.draft.snapshot.anchors.length + 1).toBe(state.draft.snapshot.anchors.length);
  }
  return state;
}
describe("P3b shared fixture-only contract in TypeScript", () => {
  it("01 verifies source identity marker and refuses production claims", () => {
    expect(fixture.contract_version).toBe(1);
    expect(fixture.data_origin).toBe("fictional_cross_language_test_only");
    expect(fixture.fixture_name).toBe("invented_isolated_chronology_v1");
    expect(fixture.universe_id.startsWith("fiction-")).toBe(true);
    expect(fixture.production_ipc_authorized).toBe(false);
    expect(fixture.operator_data_authorized).toBe(false);
    expect(fixture.writer_admitted).toBe(false);
    expect(fixture.negative_cases).toEqual([
      "missing_predecessor_rollback", "reverse_cycle_refused",
      "foreign_universe_refused", "wrong_revision_source_refused",
    ]);
  });
  it("02 executes shared goldens without inventing a total temporal order", () => {
    const state = applyGolden();
    expect(state.commands_committed).toBe(3);
    expect(state.real_g3_authorized).toBe(false);
    expect(state.draft.snapshot.anchors.map(a => a.id))
      .toEqual(fixture.expected_current_anchor_ids);
    expect(state.draft.snapshot.anchors.every(a =>
      a.source_revision_id === fixture.historical_revision_id)).toBe(true);
    const edges = state.draft.snapshot.precedences.map(e => ({
      id:e.id,before_anchor_id:e.before_anchor_id,after_anchor_id:e.after_anchor_id,
    }));
    expect(edges).toEqual(fixture.expected_precedences);
    expect(edges.some(e =>
      e.before_anchor_id === fixture.expected_incomparable_anchor_id ||
      e.after_anchor_id === fixture.expected_incomparable_anchor_id)).toBe(false);
    expect(state.draft.snapshot.reader_reveal_status).toBe("not_authored");
  });
  it("03 invalid relation rolls back state, cycle and foreign world refuse", () => {
    const state=applyGolden(), before=JSON.stringify(state);
    expect(() => applyP3FictionalCommand(state, {
      kind:"create_anchor_with_optional_relation",universe_id:fixture.universe_id,
      time:{kind:"relative",calendar:"",label:"",precision:""},
      relation:{before_anchor_id:"missing",after_anchor_id:P3_NEW_ANCHOR,
        reason:"Lien inexistant"},
    })).toThrow();
    expect(() => applyP3FictionalCommand(state, {
      kind:"create_precedence",universe_id:fixture.universe_id,
      relation:{before_anchor_id:fixture.expected_current_anchor_ids[1],
        after_anchor_id:fixture.expected_current_anchor_ids[0],
        reason:"Cycle interdit"},
    })).toThrow(/cycle/);
    expect(() => applyP3FictionalCommand(state, {
      kind:"create_precedence",universe_id:"fiction-foreign",
      relation:{before_anchor_id:fixture.expected_current_anchor_ids[0],
        after_anchor_id:fixture.expected_current_anchor_ids[2],
        reason:"Univers étranger"},
    })).toThrow();
    expect(JSON.stringify(state)).toBe(before);
  });
  it("04 historical source ID is exact, wrong scene or revision refuses", () => {
    const state = applyGolden();
    expect(() => applyP3FictionalCommand(state, {
      kind:"create_anchor_with_optional_relation",universe_id:fixture.universe_id,
      time:{kind:"relative",calendar:"",label:"",precision:"",
        source_scene_id: "invented-foreign-scene",
        source_revision_id:fixture.historical_revision_id},
      relation:null,
    })).toThrow();
    expect(() => applyP3FictionalCommand(state, {
      kind:"create_anchor_with_optional_relation",universe_id:fixture.universe_id,
      time:{kind:"relative",calendar:"",label:"",precision:"",
        source_scene_id: fixture.scene_id,
        source_revision_id:"not-in-invented-history"},
      relation:null,
    })).toThrow();
    expect(state.draft.snapshot.anchors.length).toBe(3);
  });
});
