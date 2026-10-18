"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { requestAuthorityAllowed: allow } = require("./m32_ci_http_authority.cjs");
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
console.log("M32_HTTP_AUTHORITY_SOURCE_ONLY_TESTS: strict local fictional CI rules");
