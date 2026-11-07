import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import M32P3fTwoNovelFictionalReview, {
  previewP3fTwoNovelFictionalReview, type P3fFictionalNovelInput,
} from "./M32P3fTwoNovelFictionalReview";
import type { P2iFictionalInput } from "./M32P2iFictionalImpactReview";

const world = "fiction-p3f-two-novels";
const edge = (id: string, from: string, to: string) =>
  ({ id, universe_id: world, before_anchor_id: from, after_anchor_id: to,
    origin: "original" as const });
const data: P3fFictionalNovelInput = {
  data_origin: "fictional_browser_memory_only",
  production_writer_admitted: false,
  real_g3_authorized: false,
  universe_id: world,
  novels: [
    { universe_id: world, novel_id: "book-1", novel_title: "Premier roman inventé",
      scene_id: "scene-1", anchor_id: "A", source_revision_id: "r2",
      current_head_revision_id: "r3" },
    { universe_id: world, novel_id: "book-2", novel_title: "Second roman inventé",
      scene_id: "scene-2", anchor_id: "B", source_revision_id: "r4",
      current_head_revision_id: "r5" },
  ],
  impact: {
    data_origin: "fictional_browser_memory_only",
    production_writer_admitted: false,
    real_g3_authorized: false,
    universe_id: world,
    active_before: [edge("old", "A", "B"), edge("stable", "C", "D")],
    active_after: [edge("new", "B", "A"), edge("stable", "C", "D")],
  },
};

describe("P3f browser-only author evidence for two invented novels", () => {
  it("01 returns only directly changed cross-novel assertions, without mutating input", () => {
    const old = JSON.stringify(data);
    const view = previewP3fTwoNovelFictionalReview(data);
    expect(view.first.source_revision_id).toBe("r2");
    expect(view.second.source_revision_id).toBe("r4");
    expect(view.first.current_head_revision_id).toBe("r3");
    expect(view.second.current_head_revision_id).toBe("r5");
    expect(view.direct.shared.map(x => x.edge.id)).toEqual(["new", "old"]);
    expect(view.direct.first_only).toEqual([]);
    expect(view.direct.second_only).toEqual([]);
    expect(view.data_origin).toBe("fictional_browser_memory_only");
    expect(view.production_writer_admitted).toBe(false);
    expect(view.real_g3_authorized).toBe(false);
    expect(JSON.stringify(data)).toBe(old);
  });
  it("02 rejects forged writer, G3 or source provenance and refuses foreign worlds", () => {
    for (const patch of [
      { production_writer_admitted: true }, { real_g3_authorized: true },
      { data_origin: "operator_disk" }, { universe_id: "foreign-world" },
    ]) {
      expect(() => previewP3fTwoNovelFictionalReview(
        { ...data, ...patch } as unknown as P3fFictionalNovelInput,
      )).toThrow();
    }
  });
  it("03 rejects mismatched novel, scene, source, head, anchor and missing metadata", () => {
    const first = data.novels[0], second = data.novels[1];
    for (const changed of [
      { universe_id: "other" }, { novel_id: first.novel_id },
      { scene_id: first.scene_id }, { source_revision_id: first.source_revision_id },
      { current_head_revision_id: second.source_revision_id },
      { anchor_id: first.anchor_id }, { novel_title: "" },
    ]) {
      expect(() => previewP3fTwoNovelFictionalReview(
        { ...data, novels: [first, { ...second, ...changed }] },
      )).toThrow();
    }
    expect(() => previewP3fTwoNovelFictionalReview(
      { ...data, novels: [first] } as unknown as P3fFictionalNovelInput,
    )).toThrow();
  });
  it("04 inherits full graph validation, rejects cycles and unchanged-only anchors", () => {
    for (const impact of [
      { ...data.impact, active_after: [edge("c1", "A", "B"), edge("c2", "B", "A")] },
      { ...data.impact, active_before: [edge("self", "A", "A")] },
      { ...data.impact, active_before: [edge("dup", "A", "B"), edge("dup", "A", "B")] },
      { ...data.impact, active_before: [edge("stable", "C", "D")],
        active_after: [edge("stable", "C", "D")] },
      { ...data.impact, real_g3_authorized: true } as unknown as P2iFictionalInput,
    ]) {
      expect(() => previewP3fTwoNovelFictionalReview({ ...data, impact })).toThrow();
    }
  });
  it("05 SSR displays two novel historical sources and a read-only comparison", () => {
    const html = renderToStaticMarkup(
      createElement(M32P3fTwoNovelFictionalReview, { input: data }),
    );
    for (const required of [
      "Revue chronologique de deux romans fictifs",
      "Premier roman inventé", "Second roman inventé", "r2", "r3", "r4", "r5",
      "Assertions communes aux deux ancres (2)", "new", "old",
      "sans liaison Rust", "STOP_UNAVAILABLE",
    ]) expect(html).toContain(required);
    expect(html).not.toContain("stable</code>");
    expect(html).not.toContain("Confirmer en mémoire");
    expect(html).not.toContain("fetch(");
    expect(html).toContain('aria-pressed="true"');
  });
  it("06 JSX escapes hostile fictional labels and refuses without leaking sources", () => {
    const evil = "<img src=x onerror=alert(1)>";
    const invented: P3fFictionalNovelInput = {
      ...data, novels: [
        { ...data.novels[0], novel_title: evil }, data.novels[1],
      ],
    };
    const html = renderToStaticMarkup(createElement(
      M32P3fTwoNovelFictionalReview, { input: invented },
    ));
    expect(html).toContain("&lt;img");
    expect(html).not.toContain("<img");
    const forged = { ...invented, production_writer_admitted: true } as unknown as P3fFictionalNovelInput;
    const denied = renderToStaticMarkup(createElement(
      M32P3fTwoNovelFictionalReview, { input: forged },
    ));
    expect(denied).toContain("Revue fictive refusée");
    expect(denied).not.toContain(evil);
    expect(denied).not.toContain("Premier roman inventé");
    expect(denied).not.toContain("<li");
  });
});
