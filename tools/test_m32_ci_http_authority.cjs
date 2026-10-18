"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { requestAuthorityAllowed } = require("./m32_ci_http_authority.cjs");
const allow = (headers, target) => requestAuthorityAllowed(
  headers, target, Object.entries(headers).flat());
const local = { host: "127.0.0.1:14279" };

test("01 same-origin GET and asset request targets only", () => {
  for (const target of ["/m32-browser-lab.html", "/assets/main.abc.js",
    "/assets/main.abc.css", "/m32-browser-lab.html?query=x"]) {
    assert.equal(allow(local, target), true, target);
  }
});
test("02 prevent DNS rebinding aliases and wildcard authority", () => {
  for (const host of ["localhost:14279","0.0.0.0:14279","[::1]:14279",
    "127.0.0.1:1420", "evil.invalid:14279", "127.0.0.1:14279.evil.invalid",
    "127.0.0.1","127.0.0.1:14279@evil.invalid",""]) {
    assert.equal(allow({host}, "/m32-browser-lab.html"), false, host);
  }
});
test("03 absent Host and extra forwarding metadata denied", () => {
  assert.equal(allow({}, "/m32-browser-lab.html"), false);
  for (const name of ["forwarded", "x-forwarded-host", "x-forwarded-proto",
    "proxy-authorization"]) {
    assert.equal(allow({...local, [name]:"evil.invalid"}, "/m32-browser-lab.html"), false);
  }
});
test("04 Origin must be exact local origin when supplied", () => {
  for (const origin of ["null", "http://localhost:14279", "http://0.0.0.0:14279",
    "https://127.0.0.1:14279", "http://127.0.0.1:1420",
    "https://evil.invalid", "http://127.0.0.1:14279.evil.invalid"]) {
    assert.equal(allow({...local,origin}, "/m32-browser-lab.html"), false);
  }
  assert.equal(allow({...local,origin:"http://127.0.0.1:14279"}, "/m32-browser-lab.html"), true);
});
test("05 reject absolute-form, scheme-relative and backslash targets", () => {
  for (const target of ["http://evil.invalid/", "https://evil.invalid/",
    "//evil.invalid/", "\\\\evil.invalid", "evil.invalid", "",
    "/hello\\r\\nInjected: yes"]) {
    assert.equal(allow(local, target), false);
  }
});
test("06 reject cross-site fetch metadata", () => {
  for(const site of ["cross-site", "same-site", "none-cross", "unexpected"]) {
    assert.equal(allow({...local,"sec-fetch-site":site}, "/m32-browser-lab.html"), false);
  }
  for(const site of ["none", "same-origin"]) {
    assert.equal(allow({...local,"sec-fetch-site":site}, "/m32-browser-lab.html"), true);
  }
});
test("07 raw Host duplicates denied even when normalized Host looks safe", () => {
  const target = "/m32-browser-lab.html";
  for (const raw of [
    ["Host", local.host, "Host", "evil.invalid:14279"],
    ["Host", "evil.invalid:14279", "Host", local.host],
    ["Host", local.host, "hOsT", local.host],
  ]) assert.equal(requestAuthorityAllowed(local, target, raw), false);
});
test("08 duplicate Origin and fetch metadata are denied", () => {
  const target = "/m32-browser-lab.html";
  for (const raw of [
    ["Host", local.host, "Origin", "http://127.0.0.1:14279", "origin", "https://evil.invalid"],
    ["Host", local.host, "Sec-Fetch-Site", "same-origin", "sec-fetch-site", "cross-site"],
    ["Host", local.host, "ORIGIN", "http://127.0.0.1:14279", "Origin", "http://127.0.0.1:14279"],
  ]) assert.equal(requestAuthorityAllowed(local, target, raw), false);
});
test("09 missing malformed or inconsistent raw evidence is denied", () => {
  const target = "/m32-browser-lab.html";
  for (const raw of [undefined, [], ["Host"], ["Host", local.host, "Origin"],
    ["Host", "evil.invalid:14279"], ["Host", local.host, "Forwarded", "for=evil"]]) {
    assert.equal(requestAuthorityAllowed(local, target, raw), false);
  }
  assert.equal(requestAuthorityAllowed({...local,origin:"http://127.0.0.1:14279"},
    target, ["Host",local.host]), false);
});
test("10 valid mixed-case raw headers still allow same-origin fixture routes", () => {
  const headers = {...local,origin:"http://127.0.0.1:14279","sec-fetch-site":"same-origin"};
  assert.equal(requestAuthorityAllowed(headers, "/m32-browser-lab.html",
    ["hOsT",local.host,"OrIgIn",headers.origin,"Sec-Fetch-Site","same-origin"]),true);
  assert.equal(requestAuthorityAllowed(local, "/" + "x".repeat(4096),
    ["Host",local.host]),false);
  assert.equal(requestAuthorityAllowed(local,"/m32-browser-lab.html",
    ["Host",local.host,"Proxy-Connection","keep-alive"]),false);
});
console.log("M32_HTTP_AUTHORITY_RAW_HEADERS_TESTS: normalized/raw mismatch and duplicate veto");
