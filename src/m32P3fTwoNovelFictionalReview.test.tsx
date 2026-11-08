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
  revision_witnesses: [
    { universe_id: world, novel_id: "book-1", scene_id: "scene-1",
      revision_id: "r2", role: "historical_source", anchor_id: "A" },
    { universe_id: world, novel_id: "book-1", scene_id: "scene-1",
      revision_id: "r3", role: "current_head", anchor_id: null },
    { universe_id: world, novel_id: "book-2", scene_id: "scene-2",
      revision_id: "r4", role: "historical_source", anchor_id: "B" },
    { universe_id: world, novel_id: "book-2", scene_id: "scene-2",
      revision_id: "r5", role: "current_head", anchor_id: null },
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
    expect(view.declared_revision_witnesses).toBe(4);
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
    expect(html).toContain("attributions de");
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
  it("07 refuses forged declared revision witnesses and foreign attribution", () => {
    const w = data.revision_witnesses;
    for (const altered of [
      w.slice(0, 3),
      [...w, w[0]],
      [...w.slice(0, 2), { ...w[2], novel_id: "book-1" }, w[3]],
      [{ ...w[0], universe_id: "foreign" }, ...w.slice(1)],
      [{ ...w[0], anchor_id: "B" }, ...w.slice(1)],
      [{ ...w[0], role: "current_head" as const }, ...w.slice(1)],
      [{ ...w[0], revision_id: "r3" }, ...w.slice(1)],
      [{ ...w[0], scene_id: "scene-2" }, ...w.slice(1)],
    ]) {
      expect(() => previewP3fTwoNovelFictionalReview({
        ...data, revision_witnesses: altered,
      })).toThrow();
    }
  });
  it("08 rejects an absent witness before displaying historical source details", () => {
    const invalid = { ...data, revision_witnesses: data.revision_witnesses.slice(1) };
    const html = renderToStaticMarkup(createElement(
      M32P3fTwoNovelFictionalReview, { input: invalid },
    ));
    expect(html).toContain("Revue fictive refusée");
    expect(html).not.toContain("Premier roman inventé");
    expect(html).not.toContain("r2");
  });
});


const p3iClaims: NonNullable<P3fFictionalNovelInput["canon_claims"]> = [
  { assertion_id: "home-one", universe_id: world,
    novel_id: "book-1", scene_id: "scene-1", source_revision_id: "r2",
    entity_id: "hero", property_key: "home", literal_value: "north" },
  { assertion_id: "home-two", universe_id: world,
    novel_id: "book-2", scene_id: "scene-2", source_revision_id: "r4",
    entity_id: "hero", property_key: "home", literal_value: "south" },
  { assertion_id: "role-one", universe_id: world,
    novel_id: "book-1", scene_id: "scene-1", source_revision_id: "r2",
    entity_id: "hero", property_key: "role", literal_value: "guide" },
  { assertion_id: "role-two", universe_id: world,
    novel_id: "book-2", scene_id: "scene-2", source_revision_id: "r4",
    entity_id: "hero", property_key: "role", literal_value: "guide" },
];
describe("P3i fictional two-novel character-sheet comparisons", () => {
  it("09 compares only literal facts tied to the historical source, no mutation", () => {
    const input = { ...data, canon_claims: p3iClaims };
    const before = JSON.stringify(input);
    const result = previewP3fTwoNovelFictionalReview(input);
    expect(result.canon_comparison.total_claims).toBe(4);
    expect(result.canon_comparison.differences).toHaveLength(1);
    expect(result.canon_comparison.agreements).toHaveLength(1);
    expect(result.canon_comparison.differences[0].first.literal_value).toBe("north");
    expect(result.canon_comparison.differences[0].second.literal_value).toBe("south");
    expect(result.canon_comparison.real_g3_authorized).toBe(false);
    expect(JSON.stringify(input)).toBe(before);
    expect(previewP3fTwoNovelFictionalReview(data).canon_comparison.total_claims).toBe(0);
  });
  it("10 rejects foreign universe, scene, novel, current HEAD or fabricated source", () => {
    for (const forged of [
      { universe_id: "foreign-world" }, { novel_id: "unknown" },
      { scene_id: "scene-2" }, { source_revision_id: "r3" },
      { source_revision_id: "made-up" }, { source_revision_id: "r4" },
      { property_key: "" }, { entity_id: "" },
    ]) {
      const broken = [{ ...p3iClaims[0], ...forged }, ...p3iClaims.slice(1)];
      expect(() => previewP3fTwoNovelFictionalReview({
        ...data, canon_claims: broken,
      })).toThrow();
    }
  });
  it("11 rejects duplicate assertion IDs, ambiguous facts and malformed catalogues", () => {
    for (const broken of [
      [...p3iClaims, p3iClaims[0]],
      [...p3iClaims, { ...p3iClaims[0], assertion_id: "different-id" }],
      [{ ...p3iClaims[0], literal_value: "X".repeat(257) }, ...p3iClaims.slice(1)],
      Array.from({ length: 65 }, (_, i) => ({
        ...p3iClaims[0], assertion_id: "extra-" + i,
      })),
    ]) {
      expect(() => previewP3fTwoNovelFictionalReview({
        ...data, canon_claims: broken,
      })).toThrow();
    }
    expect(() => previewP3fTwoNovelFictionalReview({
      ...data, canon_claims: {} as unknown as typeof p3iClaims,
    })).toThrow();
  });
  it("12 shows differences as review prompts, escapes HTML and refuses before disclosure", () => {
    const evil = "<script>fake()</script>";
    const given = { ...data, canon_claims: [
      { ...p3iClaims[0], literal_value: evil }, ...p3iClaims.slice(1),
    ] };
    const html = renderToStaticMarkup(createElement(
      M32P3fTwoNovelFictionalReview, { input: given },
    ));
    expect(html).toContain("Revue de cohérence de fiches fictives");
    expect(html).toContain("écarts à examiner");
    expect(html).toContain("&lt;script&gt;");
    expect(html).not.toContain("<script>");
    expect(html).toContain("sans résolution automatique");
    const invalid = { ...given, canon_claims: [
      { ...given.canon_claims[0], source_revision_id: "r3" },
      ...given.canon_claims.slice(1),
    ] };
    const refused = renderToStaticMarkup(createElement(
      M32P3fTwoNovelFictionalReview, { input: invalid },
    ));
    expect(refused).toContain("Revue fictive refusée");
    expect(refused).not.toContain("fake()");
    expect(refused).not.toContain("Premier roman inventé");
    expect(refused).not.toContain("hero");
  });
});


describe("P3j one-sided fictional character facts are not coherence proof", () => {
  it("13 reports missing counterparts separately, preserving both sources", () => {
    const extra = [
      { ...p3iClaims[0], assertion_id: "one-only", property_key: "scar",
        literal_value: "left-scar" },
      { ...p3iClaims[1], assertion_id: "two-only", property_key: "voice",
        literal_value: "soft" },
    ];
    const input = { ...data, canon_claims: [...p3iClaims, ...extra] };
    const prior = JSON.stringify(input);
    const result = previewP3fTwoNovelFictionalReview(input).canon_comparison;
    expect(result.total_claims).toBe(6);
    expect(result.agreements).toHaveLength(1);
    expect(result.differences).toHaveLength(1);
    expect(result.first_only.map(c => c.assertion_id)).toEqual(["one-only"]);
    expect(result.second_only.map(c => c.assertion_id)).toEqual(["two-only"]);
    expect(JSON.stringify(input)).toBe(prior);
    expect(result.production_writer_admitted).toBe(false);
  });
  it("14 distinguishes a one-sided fact from a falsified historical source", () => {
    const extra = { ...p3iClaims[0], assertion_id: "unique-literal",
      property_key: "eye", literal_value: "amber" };
    const valid = { ...data, canon_claims: [...p3iClaims, extra] };
    const view = previewP3fTwoNovelFictionalReview(valid).canon_comparison;
    expect(view.first_only).toHaveLength(1);
    expect(view.second_only).toHaveLength(0);
    const forged = { ...valid, canon_claims: [...p3iClaims,
      { ...extra, source_revision_id: "r3" }] };
    expect(() => previewP3fTwoNovelFictionalReview(forged)).toThrow();
    const denied = renderToStaticMarkup(createElement(
      M32P3fTwoNovelFictionalReview, { input: forged },
    ));
    expect(denied).toContain("Revue fictive refusée");
    expect(denied).not.toContain("amber");
    expect(denied).not.toContain("Premier roman inventé");
  });
  it("15 labels unmatched facts as non-comparable and escapes hostile literals", () => {
    const evil = "<img src=x onerror=alert(7)>";
    const one = { ...p3iClaims[0], assertion_id: "unique",
      property_key: "nickname", literal_value: evil };
    const html = renderToStaticMarkup(createElement(
      M32P3fTwoNovelFictionalReview,
      { input: { ...data, canon_claims: [...p3iClaims, one] } },
    ));
    expect(html).toContain("non comparable");
    expect(html).toContain("premier roman uniquement");
    expect(html).toContain("&lt;img");
    expect(html).not.toContain("<img");
    expect(html).not.toContain("alert(7)</script>");
    expect(html).toContain("STOP_UNAVAILABLE");
  });
});
