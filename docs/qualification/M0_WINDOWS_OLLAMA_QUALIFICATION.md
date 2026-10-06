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
| rustc | command not found | BLOCKED |
| cargo | command not found | BLOCKED |
| Ollama | `0.35.1` | PASS |

## Ollama inventory

30 installed model entries were observed:

1. `captioner-zimage:latest`
2. `tinyrick/Qwen3.6-35B-A3B-uncensored-heretic-vision-llmfan46:Q4_K_M`
3. `qwen3-vl:8b`
4. `svjack/gpt-oss-20b-heretic_open:latest`
5. `svjack/gpt-oss-20b-heretic:latest`
6. `huihui_ai/qwen3.5-abliterated:9b`
7. `laguna-xs-2.1:Q4_K_M`
8. `ornith:9b`
9. `north-mini-code-1.0:Q4_K_M`
10. `devstral-small-2:24b`
11. `gpt-oss:20b`
12. `granite4.1:3b`
13. `qwen3.5:4b`
14. `Laurent-Adult-Prose-12B-FR-v2.2.4-Balanced50:latest`
15. `Laurent-Adult-Prose-12B-FR-v2.2.4-Balanced50-Diagnostic:latest`
16. `hf.co/bartowski/Mistral-Nemo-Instruct-2407-GGUF:Q4_K_M`
17. `hf.co/bartowski/magnum-v4-12b-GGUF:Q4_K_M`
18. `goekdenizguelmez/JOSIEFIED-Qwen3:8b`
19. `jimscard/new-adult-writer:latest`
20. `MrTails/Tails-assistant-ai-v3.0.0:latest`
21. `moophlo/Satyr-V0.1-4B:latest`
22. `huihui_ai/qwen2.5-coder-abliterate:7b`
23. `studiobrn/uncensoredmodAI:latest`
24. `FableForge-AI/mythos-9b-enhanced:latest`
25. `deepseek-r1:32b`
26. `deepseek-r1:14b`
27. `richardyoung/qwythos-9b-abliterated:Q8_0`
28. `qwen3.6:27b`
29. `qwen3.5:9b`
30. `qwen2.5-coder:7b-instruct`

No installed model is assumed to be an embeddings model solely from its name.

## GPU execution test

Test model: `qwen3.5:9b`

Prompt category: long-form French narrative-planning explanation.

Observed `ollama ps` repeatedly reported:

- runtime size: `7.7 GB`;
- processor: `100% GPU`;
- context: `65536`;
- model remained loaded across repeated observations.

The requested generation completed successfully.

### Qualification

- Local inference: **PASS**
- GPU offload/acceleration: **PASS**
- Exact AMD backend implementation: **PENDING**

The output proves GPU use but does not identify whether Ollama is using Vulkan, ROCm/HIP or another supported backend path.

## Local HTTP API

The first `Invoke-RestMethod http://127.0.0.1:11434/api/version` attempt did not show a visible payload in the pasted transcript.

Status: **PENDING explicit rendered response**

This is not treated as a failure because `ollama run` and `ollama ps` both successfully interacted with the local Ollama service.

## GPU identity / driver evidence

The first `Win32_VideoController` query did not show a visible device row in the pasted transcript.

Declared target remains:

- AMD Radeon RX 6750 XT;
- 12 GB VRAM.

Status: **PENDING forced-formatted Windows evidence**

## Tauri prerequisite state

Rust/Cargo are absent.

Before a Tauri skeleton can be qualified, verify/install:

- Microsoft C++ Build Tools with Desktop development with C++;
- Rust via rustup;
- stable MSVC Rust toolchain.

WebView2 is expected on supported modern Windows systems, but the application build itself will be the practical qualification.

## M0 conclusion

The most important local-AI uncertainty is resolved: Ollama can perform a real generation while reporting `100% GPU`.

M0 is **not complete** because:

- exact backend is still unconfirmed;
- explicit API response remains to be captured;
- C++ Build Tools are not yet verified;
- Rust/MSVC is not installed;
- no Tauri executable has been built yet.
