"use strict";
// Failure-oriented unit tests over INVENTED JSON reporter payloads only.
const test = require("node:test");
const assert = require("node:assert/strict");
const { EXPECTED, verifyNamedVitestReport } = require("./m32_named_vitest_report.cjs");
const files = Object.keys(EXPECTED);
function fakeReport() {
  return {
    success: true,
    numTotalTestSuites: 4, numPassedTestSuites: 4, // two files + two describe blocks
    numFailedTestSuites: 0, numPendingTestSuites: 0,
    numTotalTests: 11, numPassedTests: 11,
    numFailedTests: 0, numPendingTests: 0, numTodoTests: 0,
    testResults: files.map(file => ({
      name: "C:\\ephemeral\\ci\\" + file.replace(/\//g, "\\"),
      status: "passed",
      assertionResults: EXPECTED[file].map(title => ({
        title, status: "passed", failureMessages: [], fullName: "Fictional " + title,
      })),
    })),
  };
}
const rejects = report =>
  assert.throws(() => verifyNamedVitestReport(report), /M32_NAMED_VITEST_REFUSAL:/);

test("accepts 11 named cases in two files despite nested describe suite counts", () => {
  const names = verifyNamedVitestReport(fakeReport());
  assert.equal(names.length, 11);
  assert.deepEqual(names, [...names].sort());
});
test("rejects missing test case despite success counters", () => {
  const f = fakeReport(); f.testResults[0].assertionResults.pop(); rejects(f);
});
test("rejects duplicate title despite success counters", () => {
  const f = fakeReport();
  f.testResults[0].assertionResults[1].title = f.testResults[0].assertionResults[0].title;
  rejects(f);
});
test("rejects invented extra test by another file", () => {
  const f = fakeReport(); f.testResults[1].name = "C:\\tmp\\src\\other.test.tsx"; rejects(f);
});
test("rejects status failure even if top-level success is forged", () => {
  const f = fakeReport(); f.testResults[0].assertionResults[0].status = "failed"; rejects(f);
});
test("rejects pending test even if suite otherwise passed", () => {
  const f = fakeReport(); f.testResults[1].assertionResults[0].status = "pending"; rejects(f);
});
test("rejects extra failure message on passed result", () => {
  const f = fakeReport(); f.testResults[1].assertionResults[0].failureMessages = ["fictional failure"]; rejects(f);
});
test("rejects a wrong test count", () => {
  const f = fakeReport(); f.numPassedTests = 10; rejects(f);
});
test("rejects a wrong suite count", () => {
  const f = fakeReport(); f.numPassedTestSuites = 1; rejects(f);
});
test("rejects missing suite and misleading passing counters", () => {
  const f = fakeReport(); f.testResults.pop(); rejects(f);
});
test("rejects a duplicate suite", () => {
  const f = fakeReport(); f.testResults[1].name = f.testResults[0].name; rejects(f);
});
test("rejects additional historical test name not in sealed fixture list", () => {
  const f = fakeReport(); f.testResults[0].assertionResults[2].title = "unexpected historical claim"; rejects(f);
});
test("rejects report success false and invalid report shape", () => {
  const f = fakeReport(); f.success = false; rejects(f);
  rejects(null); rejects([]); rejects({ success: true });
});
