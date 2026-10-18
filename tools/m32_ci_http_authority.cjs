"use strict";
/** CI fixture HTTP request-target and authority veto. No operator server. */
function requestAuthorityAllowed(headers, target) {
  if (!headers || typeof target !== "string" || !target.startsWith("/") ||
      target.startsWith("//") || target.includes("\\") || /[\r\n]/.test(target)) return false;
  const keys = Object.keys(headers);
  if (keys.some(k => k.toLowerCase() === "forwarded" ||
      k.toLowerCase().startsWith("x-forwarded-") || k.toLowerCase() === "proxy-authorization")) return false;
  if (headers.host !== "127.0.0.1:14279") return false;
  const origin = headers.origin;
  if (origin !== undefined && origin !== "http://127.0.0.1:14279") return false;
  if (headers["sec-fetch-site"] && !["same-origin", "none"].includes(headers["sec-fetch-site"])) return false;
  return true;
}
module.exports = { requestAuthorityAllowed };
