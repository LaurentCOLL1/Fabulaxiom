# M0 Ollama Loopback Qualification — 2026-10-06

## Final decision

**PASS**

## Final observed state

- user-level `OLLAMA_HOST`: `127.0.0.1:11434`
- machine-level `OLLAMA_HOST`: not defined
- Ollama API: `0.40.0`
- listener: `127.0.0.1:11434`
- server log: `OLLAMA_HOST:http://127.0.0.1:11434`
- server log: `Listening on 127.0.0.1:11434 (version 0.40.0)`

Reachability:

- `127.0.0.1:11434`: ACCESSIBLE
- `172.24.96.1:11434`: NON ACCESSIBLE
- `192.168.1.200:11434`: NON ACCESSIBLE
- `10.100.0.2:11434`: NON ACCESSIBLE

## Root cause of the previous failure

Ollama Desktop's **Expose Ollama to the network** setting was enabled. Current Ollama code forces `OLLAMA_HOST=0.0.0.0` when that setting is enabled.

After disabling it and fully restarting Ollama, the server returned to loopback-only binding.

## Authorization

Fabulaxiom may now add a read-only local Ollama client restricted to `127.0.0.1:11434`.
