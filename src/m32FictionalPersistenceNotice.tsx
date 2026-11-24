import type { ReactElement } from "react";

/** Inert M3.2 fixture status. No writer is called or authorized. */
export type M32FictionalPersistenceState = "fixture" | "action_refused";
export type M32FictionalPersistenceClaim = Readonly<{
  state: M32FictionalPersistenceState;
  persisted: false;
  writer_called: false;
  writer_authorized: false;
  status: "non_persisted";
  message: string;
}>;

export function describeM32FictionalPersistence(
  state: M32FictionalPersistenceState,
): M32FictionalPersistenceClaim {
  if (state === "fixture") return {
    state, persisted: false, writer_called: false, writer_authorized: false,
    status: "non_persisted",
    message: "Simulation fictive non persistée. Aucune sauvegarde ; writer réel indisponible (G3 STOP_UNAVAILABLE).",
  };
  if (state === "action_refused") return {
    state, persisted: false, writer_called: false, writer_authorized: false,
    status: "non_persisted",
    message: "Action fictive refusée ; aucune sauvegarde, aucun changement des données réelles. Aucun appel au writer réel (G3 STOP_UNAVAILABLE).",
  };
  throw new Error("STOP M32-076 : état de persistance fictive inconnu");
}

/** Reusable visible warning for nonmounted, browser-memory-only workshops. */
export default function M32FictionalPersistenceNotice({
  state = "fixture",
}: { state?: M32FictionalPersistenceState }): ReactElement {
  const claim = describeM32FictionalPersistence(state);
  return <p role={state === "action_refused" ? "alert" : "status"}
    aria-label="Persistance de la simulation chronologique">
    {claim.message}
  </p>;
}
