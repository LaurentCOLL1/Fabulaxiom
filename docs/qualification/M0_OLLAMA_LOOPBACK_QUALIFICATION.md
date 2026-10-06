# M0 Ollama Loopback Qualification — 2026-10-06

## Objective

Verify that the Ollama server used by Fabulaxiom is restricted to loopback before application integration.

## Operator-observed evidence

Before restart:

- user-level `OLLAMA_HOST`: `127.0.0.1:11434`
- machine-level `OLLAMA_HOST`: not defined

Ollama executable:

`C:\Users\lauco\AppData\Local\Programs\Ollama\ollama.exe`

Ollama desktop application:

`C:\Users\lauco\AppData\Local\Programs\Ollama\ollama app.exe`

The running Ollama processes were stopped, the user-level variable was saved again as `127.0.0.1:11434`, and Ollama was restarted.

## API result after restart

Request:

`http://127.0.0.1:11434/api/version`

Observed response:

```json
{
  "version": "0.40.0"
}
```

Status: **PASS**

This also records that Ollama upgraded from the previously observed `0.35.1` to `0.40.0` by the time of this restart.

## Listener verification

The first check used:

`Get-NetTCPConnection -LocalPort 11434 -State Listen`

PowerShell returned no matching `MSFT_NetTCPConnection` object.

Because the HTTP API request to `127.0.0.1:11434` had just succeeded, this result is classified as:

**INCONCLUSIVE**

It is not accepted as proof that Ollama had no listener, and it is not accepted as proof of loopback-only binding.

## Current decision

Loopback configuration value: **PASS**

Loopback API access: **PASS**

Actual socket binding: **PENDING independent verification**

The next qualification uses `netstat -ano` and process correlation rather than depending solely on `Get-NetTCPConnection`.
