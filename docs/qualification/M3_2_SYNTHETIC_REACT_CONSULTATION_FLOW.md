# M3.2 — Synthetic React chronology consultation (composed, unmounted)

**2026-10-17. Frontend prototype only; no source acquisition, no operator DB, no Tauri registration and no M3.2 production authorization.**

Starting protected main `125579506e7b7485e9ffab3163fe62193fee321d` after PR #58 merged and [Windows CI #39035926354](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39035926354) exact head success 40/40 steps and 24/24 targeted synthetic React tests. PR #35 remains OPEN/DRAFT (head `41ce7b915e76d22785d53d7fffe288d113dd0bf5`) and is not promoted.

## Functionality

`src/M32ChronologyConsultation.tsx` composes two independently qualified, **unmounted** components: `M32ChronologyPreview` displays world assertions, narration position and not-yet-authored reader reveal; `M32WorldOrderComparison` displays explicit current-world `before`, `after`, `same`, or `incomparable` with a shortest human-authored edge-by-edge reason chain. Two **native HTML selects with associated labels** select immutable IDs of only `current` assertions in one invented Universe. Identical names remain distinct because selections use IDs; no event is preselected, and a cleared selector removes the comparison. Both `select` elements manipulate local demonstration state only, never narrative or SQLite records. Keyboard accessibility follows native-select semantics rather than a custom ARIA listbox.

`inspectM32Consultation` and `chooseM32ConsultationAnchor` are pure exported admission/transition helpers. Entire synthetic DTO is revalidated, and the **whole active precedence graph is checked for cycles, duplicate pairs and historical endpoints even when no pair is selected**. Missing/invalid/retired/foreign IDs, improper fields, stale selection, or mismatched Universe fail closed with no partial chronology shown; no fallback selection or backend open is performed. Names/calendars remain raw fictional labels, not date comparisons.

The controlled component takes an explicit `selection` and a state callback; it never writes or reads source files. The optional `M32SyntheticConsultationLab` harness owns `useState` locally and resets when its explicit fictional `scenarioKey` changes through React's key-based remount. The key is NOT source identity, integrity or authorization. Both remain **absent from `src/App.tsx`**. The SSR/Vitest checks verify static accessible markup, pure transitions and refusals; they do **not** simulate keyboard interactions or replace a native Windows GUI acceptance run.

## Qualification and threat boundary

`src/m32ChronologyConsultation.test.tsx` contains **24 targeted Vitest tests** on the composed view, explicit paired selection, before/after/same/incomparable outcomes, nested witness ID and reason, old edge rejection, preselection full-graph veto, mismatched Universe, stale IDs, clearing selections, empty state, script text escaping, no mutable inputs and preservation of inputs. The existing full `npm run test:ci`, added targeted Windows CI step and `npm run build` must succeed on the exact final PR HEAD, as must the existing Rust, Python and source-G3 audits; a green fixture view never authorizes original data or G3.

**Governance unchanged:** historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, real G3 source `STOP_UNAVAILABLE`, real G3/G4/G5/G6 `NOT_AUTHORIZED`, PR #35 OPEN/DRAFT. No operator v6 or isolated v7 source open, production migration 007, writer IPC, activation marker, M3.3, release or independent human attestation. No private paths, ACL evidence, manifest hashes or secrets published.

References: [React useState](https://react.dev/reference/react/useState), [React rendering lists](https://react.dev/learn/rendering-lists), and [W3C combobox/select-only accessibility](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/).
