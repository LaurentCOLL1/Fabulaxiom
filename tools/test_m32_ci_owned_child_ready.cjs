"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const net = require("node:net");
const { spawn } = require("node:child_process");
const { createOwnedReadyGate } = require("./m32_ci_owned_child_ready.cjs");
const pid = 31415, nonce = "0123456789abcdef0123456789abcdef";
const valid = { type:"M32_CI_STATIC_LISTENING", host:"127.0.0.1",
  port:14279, pid, nonce };
const gate = () => createOwnedReadyGate(pid, nonce);

test("01 child IPC witness accepted only for exact launched pid/nonce/port", () => {
  const g = gate();
  assert.deepEqual(g.status(), { ready:false, error:null });
  g.observe({ ...valid });
  assert.deepEqual(g.status(), { ready:true, error:null });
});
test("02 spoofed or missing process identity refused", () => {
  for (const changes of [{pid:pid+1},{pid:0},{nonce:"f".repeat(32)},
    {nonce:""},{host:"localhost"},{port:1420},{type:"READY"}]) {
    const g = gate(); g.observe({...valid,...changes});
    assert.equal(g.status().ready,false);
    assert.ok(g.status().error);
  }
});
test("03 extra fields and wrong message shapes refused", () => {
  for (const message of [null, false, "READY", [], {},
    {...valid, remote:"true"}, Object.fromEntries(Object.entries(valid).filter(([k])=>k!=="nonce"))]) {
    const g=gate(); g.observe(message);
    assert.ok(g.status().error);
  }
});
test("04 duplicate ready messages revoke admission", () => {
  const g=gate(); g.observe(valid); g.observe(valid);
  assert.equal(g.status().ready,false);
  assert.ok(g.status().error);
});
test("05 bad first message cannot be repaired by a later good message", () => {
  const g=gate(); g.observe({...valid,pid:22}); g.observe(valid);
  assert.equal(g.status().ready,false);
});
test("06 invalid expected launch identity fails closed", () => {
  for (const [id,secret] of [[0,nonce],[-1,nonce],[1,"bad"],[null,nonce]]) {
    assert.throws(()=>createOwnedReadyGate(id,secret),/STOP/);
  }
});
test("07 occupied loopback port blocks a toy child listening witness", async () => {
  const foreign=net.createServer();
  await new Promise((resolve,reject)=>{
    foreign.once("error",reject);
    foreign.listen(0,"127.0.0.1",resolve);
  });
  try {
    const occupied=foreign.address().port;
    const code = 'const net=require("node:net");' +
      'net.createServer().on("error",err=>' +
      'process.exit(err.code==="EADDRINUSE"?26:27))' +
      '.listen(' + occupied + ',"127.0.0.1",()=>{' +
      'if(process.send)process.send({type:"UNEXPECTED_LISTEN_SUCCESS"});' +
      'process.exit(28);});';
    const child=spawn(process.execPath,["-e",code],
      {stdio:["ignore","pipe","pipe","ipc"],windowsHide:true});
    let received=false;
    const done=await new Promise((resolve,reject)=>{
      const timeout=setTimeout(()=>{child.kill();reject(Error("toy child did not exit"));},5000);
      child.on("message",()=>{received=true;});
      child.on("error",e=>{clearTimeout(timeout);reject(e);});
      child.on("exit",exit=>{clearTimeout(timeout);resolve(exit);});
    });
    assert.equal(done,26,"another process occupied the port: child cannot claim ownership");
    assert.equal(received,false,"no positive listening witness is authorized");
  } finally {
    await new Promise(resolve=>foreign.close(resolve));
  }
});
console.log("M32_CI_OWNED_CHILD_GATE_TESTS: synthetic IPC and port-collision tests");
