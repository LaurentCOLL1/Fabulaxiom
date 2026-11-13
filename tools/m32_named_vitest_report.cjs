"use strict";
// Source-only, synthetic Vitest JSON reporter guard: NO SQLite, IPC, OS identity,
// network, live operator data, writer or application launch.
const fs = require("node:fs");

const EXPECTED = Object.freeze({
  "src/m32WorldOrderIsolation.test.tsx": Object.freeze([
    "accepts homonymous anchors, precedence IDs and scene IDs in SEPARATE Universes",
    "refuses the other Universe selection before any partial proof or history leaks",
    "refuses injected foreign anchor, edge or novel scene even with identical local IDs",
    "refuses same-Universe duplicate identities instead of accepting homonyms as aliases",
    "does not infer chronology from four time kinds, cross-novel narration or source revision",
    "does not turn an unauthored reader reveal into any invented chronological order",
  ]),
  "src/m32WorldOrderBoundaries.test.tsx": Object.freeze([
    "accepts the exact 512-anchor/2048-edge limit and stable shortest witness",
    "refuses 2049 relations even when overflow is only historical",
    "refuses 513 anchors or 2049 narration entries with no partial display",
    "fails closed on a cycle anywhere in the full allowed graph, even for same-ID",
    "ignores a revoked back-edge at the exact relation cap without changing history",
  ]),
});
const EXACT_FILES = Object.keys(EXPECTED);
const fail = message => { throw new Error("M32_NAMED_VITEST_REFUSAL: " + message); };
const goodInt = n => Number.isSafeInteger(n) && n >= 0;
function assertCounter(report, name, exact) {
  if (!goodInt(report[name]) || report[name] !== exact) fail("counter " + name);
}
function verifyNamedVitestReport(report) {
  if (!report || typeof report !== "object" || Array.isArray(report)) fail("invalid report");
  if (report.success !== true) fail("report did not succeed");
  for (const [name, exact] of Object.entries({
    numTotalTestSuites: 2, numPassedTestSuites: 2,
    numFailedTestSuites: 0, numPendingTestSuites: 0,
    numTotalTests: 11, numPassedTests: 11,
    numFailedTests: 0, numPendingTests: 0, numTodoTests: 0,
  })) assertCounter(report, name, exact);
  if (!Array.isArray(report.testResults) || report.testResults.length !== 2)
    fail("not exactly two result suites");

  const found = new Set();
  const accepted = [];
  for (const suite of report.testResults) {
    if (!suite || typeof suite !== "object" || typeof suite.name !== "string")
      fail("invalid suite");
    const normalized = suite.name.replace(/\\/g, "/");
    const name = EXACT_FILES.find(f => normalized === f || normalized.endsWith("/" + f));
    if (!name || found.has(name)) fail("wrong or repeated suite");
    found.add(name);
    if (suite.status !== "passed") fail("suite did not pass");
    if (!Array.isArray(suite.assertionResults) ||
        suite.assertionResults.length !== EXPECTED[name].length)
      fail("missing or extra named assertions");
    const seen = new Set();
    for (const result of suite.assertionResults) {
      if (!result || typeof result.title !== "string" || result.status !== "passed")
        fail("assertion not passed");
      if (!EXPECTED[name].includes(result.title) || seen.has(result.title))
        fail("unexpected or repeated test title");
      if (!Array.isArray(result.failureMessages) || result.failureMessages.length !== 0)
        fail("assertion has failures");
      seen.add(result.title);
    }
    if (seen.size !== EXPECTED[name].length) fail("incomplete named assertions");
    // Only print a pinned title, never arbitrary report data.
    for (const title of EXPECTED[name]) accepted.push(name + " :: " + title);
  }
  if (found.size !== EXACT_FILES.length || accepted.length !== 11) fail("incomplete suite set");
  return accepted.sort();
}
if (require.main === module) {
  try {
    if (process.argv.length !== 3) fail("one explicit JSON output path required");
    const report = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
    const names = verifyNamedVitestReport(report);
    for (const name of names) process.stdout.write("M32_NAMED_VITEST_CASE_PASS " + name + "\n");
    process.stdout.write("M32_NAMED_VITEST_11_INDIVIDUAL_CASES_PASS_SYNTHETIC_ONLY\n");
  } catch (err) {
    process.stderr.write(String(err.message || err) + "\n");
    process.exitCode = 1;
  }
}
module.exports = { EXPECTED, verifyNamedVitestReport };
