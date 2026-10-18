"use strict";
/** CI-only HTTP request authority check; inspect raw, not just normalized headers. */
function requestAuthorityAllowed(headers, target, rawHeaders) {
  if (!headers || typeof target !== "string" || target.length > 4096 ||
      !target.startsWith("/") || target.startsWith("//") ||
      target.includes("\\") || /[\r\n]/.test(target)) return false;
  // Node may silently discard duplicate Host entries when building req.headers.
  // The pair array must come directly from req.rawHeaders, not reconstructed.
  if (!Array.isArray(rawHeaders) || rawHeaders.length % 2 !== 0) return false;
  const witnessed = new Map();
  for (let i = 0; i < rawHeaders.length; i += 2) {
    const name = rawHeaders[i];
    const value = rawHeaders[i + 1];
    if (typeof name !== "string" || typeof value !== "string") return false;
    const key = name.toLowerCase();
    if (key === "forwarded" || key.startsWith("x-forwarded-") ||
        key === "proxy-authorization" || key === "proxy-connection") return false;
    if (["host", "origin", "sec-fetch-site"].includes(key)) {
      if (witnessed.has(key)) return false; // reject even identical duplicates
      witnessed.set(key, value);
    }
  }
  if (witnessed.get("host") !== "127.0.0.1:14279" ||
      headers.host !== witnessed.get("host")) return false;
  const origin = witnessed.get("origin");
  if ((origin === undefined) !== (headers.origin === undefined) ||
      (origin !== undefined && (origin !== "http://127.0.0.1:14279" ||
        headers.origin !== origin))) return false;
  const site = witnessed.get("sec-fetch-site");
  if ((site === undefined) !== (headers["sec-fetch-site"] === undefined) ||
      (site !== undefined && (headers["sec-fetch-site"] !== site ||
        !["same-origin", "none"].includes(site)))) return false;
  return true;
}
module.exports = { requestAuthorityAllowed };
