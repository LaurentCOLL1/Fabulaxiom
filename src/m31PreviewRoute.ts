/** Fail closed when the operator explicitly requests an M3.1 isolated preview. */
export type M31PreviewProbe = "pending" | "available" | "unavailable";
export type M31PreviewRoute = "waiting" | "preview" | "normal" | "blocked";

export function selectM31PreviewRoute(
  probe: M31PreviewProbe,
  previewExpected: boolean,
): M31PreviewRoute {
  if (probe === "pending") return "waiting";
  if (probe === "available") return "preview";
  return previewExpected ? "blocked" : "normal";
}
