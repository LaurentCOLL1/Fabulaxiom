import {describe,expect,it} from "vitest";
import {NARRATIVE_KINDS,KIND_LABELS,isNarrativeKind,formatEntityError,updateAliasDraft} from "./entity";
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

import { decodeEntitySnapshot } from "./entity";
import { renderToStaticMarkup } from "react-dom/server";
import { createElement } from "react";
import EntityAliasList from "./EntityAliasList";

describe("M2.2 alias UI regression",()=>{
  const snapshot={
    entities:[{id:"character-1",universe_id:"u1",kind:"character",
      name:"Ariane",created_at_utc:"2026-10-08"}],
    aliases:[{id:"alias-1",entity_id:"character-1",universe_id:"u1",alias:"Ari"}],
  };
  it("validates the exact alias-bearing IPC snapshot before rendering",()=>{
    const result=decodeEntitySnapshot(snapshot);
    expect(result.aliases).toHaveLength(1);
    expect(result.aliases[0].alias).toBe("Ari");
    expect(()=>decodeEntitySnapshot({...snapshot,aliases:undefined})).toThrow(/incomplète/);
    expect(()=>decodeEntitySnapshot({...snapshot,aliases:[{...snapshot.aliases[0],alias:{name:"Ari"}}]}))
      .toThrow(/alias invalide/);
  });
  it("renders saved aliases and their actions without losing the UI",()=>{
    const aliases=decodeEntitySnapshot(snapshot).aliases;
    const html=renderToStaticMarkup(createElement(EntityAliasList,{
      aliases,busy:false,onRename:()=>{},onDelete:()=>{},
    }));
    expect(html).toContain("Ari");
    expect(html).toContain("alias-1");
    expect(html).toContain("Renommer");
    expect(html).toContain("Supprimer");
  });
  it("captures input synchronously so a deferred state updater never reads a cleared event",()=>{
    const previous:Record<string,string>={"entity-1":"Ancien","entity-2":"Alias conservé"};
    // Mimic React clearing the handler's currentTarget before state is evaluated.
    let currentTarget:{value:string}|null={value:"Ariane"};
    const capturedValue=currentTarget.value;
    currentTarget=null;
    const deferred=()=>updateAliasDraft(previous,"entity-1",capturedValue);
    expect(currentTarget).toBeNull();
    expect(deferred()).toEqual({
      "entity-1":"Ariane",
      "entity-2":"Alias conservé",
    });
    expect(previous["entity-1"]).toBe("Ancien");
  });
  it("keeps each entity's alias input independent while clearing a successful draft",()=>{
    const values=updateAliasDraft({},"first","Ari");
    const withSecond=updateAliasDraft(values,"second","Eli");
    const cleared=updateAliasDraft(withSecond,"first","");
    expect(cleared).toEqual({first:"",second:"Eli"});
    expect(withSecond.first).toBe("Ari");
  });
  it("handles an empty alias list without crashing",()=>{
    const html=renderToStaticMarkup(createElement(EntityAliasList,{
      aliases:[],busy:false,onRename:()=>{},onDelete:()=>{},
    }));
    expect(html).toContain("entity-list");
  });
});
