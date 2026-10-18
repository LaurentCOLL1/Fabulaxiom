"use strict";
/** Synthetic Windows CI parent/child listening witness, NOT an OS process attestation. */
function createOwnedReadyGate(expectedPid, nonce) {
  if (!Number.isInteger(expectedPid) || expectedPid <= 0 ||
      typeof nonce !== "string" || !/^[a-f0-9]{32}$/.test(nonce)) {
    throw Error("STOP: invalid synthetic child launch identity");
  }
  let accepted = false;
  let veto = null;
  function observe(message) {
    if (accepted || veto) {
      veto = "duplicate or late IPC ready message";
      return;
    }
    const keys = message && typeof message === "object" && !Array.isArray(message)
      ? Object.keys(message).sort().join(",") : "";
    if (keys !== "host,nonce,pid,port,type" ||
        message.type !== "M32_CI_STATIC_LISTENING" ||
        message.pid !== expectedPid ||
        message.host !== "127.0.0.1" ||
        message.port !== 14279 ||
        message.nonce !== nonce) {
      veto = "invalid child listening witness";
      return;
    }
    accepted = true;
  }
  return { observe, status: () => ({ ready: accepted && veto === null, error: veto }) };
}
module.exports = { createOwnedReadyGate };
