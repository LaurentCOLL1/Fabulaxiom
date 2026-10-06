# M0 Ollama Loopback Qualification — 2026-10-06

## Objective

Verify that the Ollama server used by Fabulaxiom is restricted to loopback before application integration.

## Configuration intent

Observed environment:

- user-level `OLLAMA_HOST`: `127.0.0.1:11434`
- machine-level `OLLAMA_HOST`: not defined

After restart, the local API responded:

```json
{
  "version": "0.40.0"
}
```

Local loopback API access: **PASS**

## Independent listener evidence

A later qualification produced decisive evidence.

### Windows socket table

`Get-NetTCPConnection` reported:

- local address: `::`
- local port: `11434`
- owning process: Ollama server

### Current Ollama server log

The current Ollama 0.40.0 server log reported:

```text
OLLAMA_HOST:http://0.0.0.0:11434
Listening on [::]:11434 (version 0.40.0)
```

### Non-loopback reachability

Observed local-interface connection tests:

- `172.24.96.1:11434`: ACCESSIBLE
- `192.168.1.200:11434`: ACCESSIBLE
- `10.100.0.2:11434`: not accessible

The first two successful non-loopback connections prove that the Ollama server is exposed beyond loopback.

## Root cause

The environment variable is not the final authority when the Ollama desktop app has its own **Expose Ollama to the network** setting enabled.

Current Ollama desktop source defines that UI setting as `settings.Expose`.

Current Ollama server-launch source explicitly performs:

```go
if settings.Expose {
    env["OLLAMA_HOST"] = "0.0.0.0"
}
```

Therefore the desktop setting overrides the inherited user-level `OLLAMA_HOST=127.0.0.1:11434` before starting `ollama serve`.

## Decision

Loopback configuration value: **PASS**

Loopback API access: **PASS**

Actual socket binding: **FAIL**

Security gate: **FAIL**

## Required remediation

1. Open Ollama Desktop.
2. Open Settings.
3. Turn **Expose Ollama to the network** OFF.
4. Fully quit Ollama.
5. Restart Ollama from the Windows Start menu.
6. Re-run listener and non-loopback accessibility checks.
7. Require:
   - loopback API PASS;
   - no `0.0.0.0:11434` / `[::]:11434` bind;
   - non-loopback local addresses unable to connect;
   - real local GPU inference still operational.

Fabulaxiom must not add its Ollama client until this security gate passes.
