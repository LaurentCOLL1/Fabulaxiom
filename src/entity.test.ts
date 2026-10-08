import {describe,expect,it} from "vitest";
import {NARRATIVE_KINDS,KIND_LABELS,isNarrativeKind,formatEntityError} from "./entity";
describe("M2.2 entity DTO helpers",()=>{
  it("supports precisely six schema kinds",()=>{
    expect(NARRATIVE_KINDS).toHaveLength(6);
    NARRATIVE_KINDS.forEach(kind=>{
      expect(isNarrativeKind(kind)).toBe(true);
      expect(KIND_LABELS[kind].length).toBeGreaterThan(0);
    });
    expect(isNarrativeKind("monster")).toBe(false);
    expect(isNarrativeKind("Character")).toBe(false);
  });
  it("formats deterministic application errors",()=>{
    expect(formatEntityError({code:"has_children",message:"Alias présents."}))
      .toBe("[has_children] Alias présents.");
    expect(formatEntityError('{"code":"not_found","message":"Alias absent."}'))
      .toBe("[not_found] Alias absent.");
  });
  it("preserves unexpected IPC failure text",()=>{
    expect(formatEntityError(new Error("IPC unavailable"))).toBe("IPC unavailable");
    expect(formatEntityError("unexpected")).toBe("unexpected");
  });
});
