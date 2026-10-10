import {describe,expect,it} from "vitest";
import {
  announceWorkspaceChange,preferredUniverseId,
  WORKSPACE_HIERARCHY_CHANGED,WORKSPACE_ENTITY_CHANGED,WORKSPACE_REVISION_CHANGED,
} from "./workspaceSync";

describe("M2.5 workspace cross-panel invalidation",()=>{
  it("enables choosing a newly created universe when previously empty",()=>{
    expect(preferredUniverseId([], "")).toBe("");
    expect(preferredUniverseId([{id:"universe-A"},{id:"universe-B"}],"")).toBe("universe-A");
  });
  it("keeps a valid selection and chooses a valid fallback if deleted",()=>{
    const universes=[{id:"universe-A"},{id:"universe-B"}];
    expect(preferredUniverseId(universes,"universe-B")).toBe("universe-B");
    expect(preferredUniverseId(universes,"universe-expired")).toBe("universe-A");
  });
  it("notifies listening panels for successful hierarchy, entity and revision writes",()=>{
    const events=new EventTarget();
    const observed:string[]=[];
    for(const name of [WORKSPACE_HIERARCHY_CHANGED,WORKSPACE_ENTITY_CHANGED,WORKSPACE_REVISION_CHANGED]){
      events.addEventListener(name,()=>observed.push(name));
      announceWorkspaceChange(name,events);
    }
    expect(observed).toEqual([
      WORKSPACE_HIERARCHY_CHANGED,WORKSPACE_ENTITY_CHANGED,WORKSPACE_REVISION_CHANGED
    ]);
  });
});
