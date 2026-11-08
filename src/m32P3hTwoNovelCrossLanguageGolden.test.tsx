import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import golden from "../fixtures/m32_p3h_two_novel_historical_contract_v1.json";
import M32P3fTwoNovelFictionalReview, {
  previewP3fTwoNovelFictionalReview, type P3fFictionalNovelInput,
} from "./M32P3fTwoNovelFictionalReview";

/** Same immutable Git JSON as cfg(test)-only Rust P2n actor; no transport or SQL bridge. */
function input(): P3fFictionalNovelInput {
  const [first, second] = golden.novels;
  const source = (novel: typeof first) => ({
    universe_id: novel.universe_id, novel_id: novel.novel_id,
    novel_title: novel.novel_title, scene_id: novel.scene_id,
    anchor_id: novel.anchor_id,
    source_revision_id: novel.historical_revision_id,
    current_head_revision_id: novel.current_head_revision_id,
  });
  return {
    data_origin: "fictional_browser_memory_only",
    production_writer_admitted: false, real_g3_authorized: false,
    universe_id: golden.universe_id,
    novels: [source(first), source(second)],
    revision_witnesses: [first, second].flatMap(novel => [
      { universe_id: novel.universe_id, novel_id: novel.novel_id,
        scene_id: novel.scene_id, revision_id: novel.historical_revision_id,
        role: "historical_source" as const, anchor_id: novel.anchor_id },
      { universe_id: novel.universe_id, novel_id: novel.novel_id,
        scene_id: novel.scene_id, revision_id: novel.current_head_revision_id,
        role: "current_head" as const, anchor_id: null },
    ]),
    impact: {
      data_origin: "fictional_browser_memory_only",
      production_writer_admitted: false, real_g3_authorized: false,
      universe_id: golden.universe_id,
      active_before: [{
        id: golden.precedence.id, universe_id: golden.universe_id,
        before_anchor_id: golden.precedence.before_anchor_id,
        after_anchor_id: golden.precedence.after_anchor_id,
        origin: "original",
      }],
      active_after: [{
        id: "fictional-reversed-correction", universe_id: golden.universe_id,
        before_anchor_id: golden.precedence.after_anchor_id,
        after_anchor_id: golden.precedence.before_anchor_id,
        origin: "restatement",
      }],
    },
  };
}
describe("P3h one shared invented two-novel Git golden read by Rust and TypeScript", () => {
  it("01 pins test-only origin, no writer admission and two distinct historical sources", () => {
    expect(golden.contract_version).toBe(1);
    expect(golden.data_origin).toBe("fictional_two_novel_cross_language_test_only");
    expect(golden.operator_data_authorized).toBe(false);
    expect(golden.production_writer_admitted).toBe(false);
    expect(golden.real_g3_authorized).toBe(false);
    expect(golden.novels).toHaveLength(2);
    for (const novel of golden.novels) {
      expect(novel.universe_id).toBe(golden.universe_id);
      expect(novel.historical_revision_id).not.toBe(novel.current_head_revision_id);
    }
    expect(golden.novels[0].historical_revision_id)
      .not.toBe(golden.novels[1].historical_revision_id);
  });
  it("02 reproduces the direct inter-novel evidence, not an inferred total order", () => {
    const value = input(), before = JSON.stringify(value);
    const review = previewP3fTwoNovelFictionalReview(value);
    expect(review.declared_revision_witnesses).toBe(4);
    expect([review.first.anchor_id, review.second.anchor_id])
      .toEqual(golden.novels.map(n => n.anchor_id));
    expect(review.direct.shared.map(w => w.edge.id).sort())
      .toEqual(["cross-novel-before", "fictional-reversed-correction"].sort());
    expect(review.direct.first_only).toEqual([]);
    expect(review.direct.second_only).toEqual([]);
    expect(review.direct.shared.some(w => w.edge.before_anchor_id ===
      golden.incomparable.anchor_id || w.edge.after_anchor_id ===
      golden.incomparable.anchor_id)).toBe(false);
    expect(JSON.stringify(value)).toBe(before);
  });
  it("03 refuses forged novel/scene/revision provenance and foreign universe", () => {
    const value = input(), second = value.novels[1];
    for (const change of [
      { scene_id: "s3" }, { universe_id: golden.foreign.universe_id },
      { source_revision_id: golden.foreign.source_revision_id },
      { source_revision_id: second.current_head_revision_id },
    ]) {
      expect(() => previewP3fTwoNovelFictionalReview({
        ...value, novels: [value.novels[0], { ...second, ...change }],
      })).toThrow();
    }
    expect(() => previewP3fTwoNovelFictionalReview({
      ...value, revision_witnesses: value.revision_witnesses.slice(1),
    })).toThrow();
    expect(golden.forbidden_actions).toContain("cross_world_relation");
  });
  it("04 rejects contradictory partial orders without revealing source labels", () => {
    const value = input();
    const bad = {
      ...value, impact: {
        ...value.impact, active_after: [...value.impact.active_before, ...value.impact.active_after],
      },
    };
    expect(() => previewP3fTwoNovelFictionalReview(bad)).toThrow();
    const html = renderToStaticMarkup(createElement(
      M32P3fTwoNovelFictionalReview, { input: bad },
    ));
    expect(html).toContain("Revue fictive refusée");
    expect(html).not.toContain(golden.novels[0].novel_title);
    expect(html).not.toContain(golden.novels[1].novel_title);
  });
});
