# M0 Windows and Ollama Qualification — 2026-10-06

## Evidence source

These results were executed by the operator on the target Windows machine and pasted back into the development conversation.

They are **operator-observed evidence**. They were not executed remotely by the development assistant.

## Toolchain snapshot

| Component | Observed result | Status |
|---|---|---|
| Windows | Product name output `Windows 10 Pro`, version `2009`, build `26220` | Recorded; product label not interpreted |
| Git | `2.55.0.windows.3` | PASS |
| Python | `3.12.4` | PASS |
| Node.js | `24.16.0` | PASS |
| npm | `11.11.0` | PASS |
| rustup | `1.29.1` | PASS |
| rustc | `1.99.0` | PASS |
| cargo | `1.99.0` | PASS |
| Rust toolchain | `stable-x86_64-pc-windows-msvc` | PASS |
| Microsoft C++ Build Tools | VS 2022 BuildTools detected | PASS |
| WebView2 Runtime | `154.0.4258.53` | PASS |
| Ollama | `0.35.1` | PASS |

## Ollama local API

Observed response:

```json
{
  "version": "0.35.1"
}
```

Status: **PASS**

## GPU identity

Windows reported:

- GPU: `AMD Radeon RX 6750 XT`
- Driver: `32.0.21045.5002`
- Video processor: `AMD Radeon Graphics Processor (0x73DF)`

The WMI `AdapterRAM` value is not treated as authoritative for VRAM capacity because the Ollama runtime reports the active device directly.

## Ollama GPU backend

The Ollama server log explicitly reported:

- `OLLAMA_VULKAN:true`
- inference library: `Vulkan`
- device: `Vulkan0`
- description: `AMD Radeon RX 6750 XT`
- total GPU memory: `12.0 GiB`

A loaded inference run further reported:

- Vulkan backend loaded from Ollama's `ggml-vulkan.dll`;
- GPU visible as AMD Radeon RX 6750 XT;
- 34/34 model layers offloaded to GPU;
- model buffer, KV cache and compute buffers allocated on Vulkan0.

Therefore:

- Local inference: **PASS**
- GPU acceleration: **PASS**
- Exact backend: **PASS — Vulkan**

## Real generation test

Test model: `qwen3.5:9b`

Observed `ollama ps` repeatedly reported:

- runtime size: `7.7 GB`;
- processor: `100% GPU`;
- context: `65536`.

The requested French long-form generation completed successfully.

Status: **PASS**

## Tauri prerequisite state

Observed:

- Microsoft C++ Build Tools found at:
  `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`
- Microsoft Edge WebView2 Runtime:
  `154.0.4258.53`
- rustup:
  `1.29.1`
- rustc:
  `1.99.0 (b940084d7 2026-09-28)`
- cargo:
  `1.99.0 (5f94df478 2026-08-27)`
- active toolchain:
  `stable-x86_64-pc-windows-msvc`
- host:
  `x86_64-pc-windows-msvc`

Status: **PASS for attempting the first Tauri build**

## Non-blocking warnings

### AMD driver warning

Ollama logged:

`AMD driver is too old. Update your AMD driver to enable GPU inference.`

However, Ollama subsequently selected and successfully used the Vulkan backend on the RX 6750 XT. The warning is retained as an environment issue, but the verified Vulkan inference path is working.

### Potentially incompatible ggml library in PATH

Ollama reported:

`potentially incompatible library detected in PATH`

for a `ggml-base.dll` located under a separately installed WinGet llama.cpp package.

This is retained as a diagnostic risk because PATH/library collisions may cause future runtime instability even though the verified run succeeded.

### Corrupt Ollama manifests

Ollama reported bad/corrupt manifests for:

- `registry.ollama.ai/library/Claude-Fable5:MiniCPM5-1B-Claude-Opus-Fable5-Thinking-Q8_0.gguf`
- `registry.ollama.ai/library/llama-mesh:LLaMA-Mesh-Q5_K_S.gguf`

These do not block the verified qwen3.5:9b run but should be repaired or removed later.

## M0 prerequisite conclusion

The Windows/Tauri prerequisite gate is now **PASS**.

M0 itself is **not complete** yet because the Fabulaxiom Tauri application has not been built, launched and tested on the target machine.

Next acceptance step:

1. build the initial Tauri 2 + React/TypeScript application;
2. launch it successfully;
3. exercise a Rust command from the frontend;
4. exercise a read-only Ollama API request from the application;
5. add automated tests and CI.
