import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import {
  formatOllamaSummary,
  type OllamaStatus,
} from "./ollama";

type BootstrapStatus = {
  app_name: string;
  milestone: string;
  rust_bridge: string;
};

function App() {
  const [status, setStatus] = useState<BootstrapStatus | null>(null);
  const [bridgeError, setBridgeError] = useState<string | null>(null);
  const [bridgePending, setBridgePending] = useState(false);

  const [ollamaStatus, setOllamaStatus] = useState<OllamaStatus | null>(null);
  const [ollamaError, setOllamaError] = useState<string | null>(null);
  const [ollamaPending, setOllamaPending] = useState(false);

  async function verifyRustBridge() {
    setBridgePending(true);
    setBridgeError(null);

    try {
      const result = await invoke<BootstrapStatus>("bootstrap_status");
      setStatus(result);
    } catch (reason) {
      setStatus(null);
      setBridgeError(String(reason));
    } finally {
      setBridgePending(false);
    }
  }

  async function verifyOllama() {
    setOllamaPending(true);
    setOllamaError(null);

    try {
      const result = await invoke<OllamaStatus>("ollama_status");
      setOllamaStatus(result);
    } catch (reason) {
      setOllamaStatus(null);
      setOllamaError(String(reason));
    } finally {
      setOllamaPending(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">M0 · qualification du socle</p>
        <h1>Fabulaxiom</h1>
        <p className="tagline">
          Mémoire narrative locale pour construire des romans, des sagas et des
          univers cohérents.
        </p>
      </section>

      <div className="card-grid">
        <section className="card" aria-labelledby="bootstrap-title">
          <div>
            <p className="card-kicker">Contrôle exécutable</p>
            <h2 id="bootstrap-title">Pont React → Tauri → Rust</h2>
            <p>
              Vérifie que l'interface peut appeler le cœur Rust de
              l'application, sans modifier de manuscrit.
            </p>
          </div>

          <button
            type="button"
            onClick={verifyRustBridge}
            disabled={bridgePending}
          >
            {bridgePending ? "Vérification…" : "Tester le pont Rust"}
          </button>

          {status && (
            <div className="result success" role="status">
              <strong>PASS</strong>
              <span>{status.app_name}</span>
              <span>{status.milestone}</span>
              <span>{status.rust_bridge}</span>
            </div>
          )}

          {bridgeError && (
            <div className="result failure" role="alert">
              <strong>ÉCHEC</strong>
              <span>{bridgeError}</span>
            </div>
          )}
        </section>

        <section className="card" aria-labelledby="ollama-title">
          <div>
            <p className="card-kicker">Service IA local</p>
            <h2 id="ollama-title">Ollama en lecture seule</h2>
            <p>
              Fabulaxiom interroge uniquement l'API de version sur
              127.0.0.1:11434. Aucun manuscrit ni prompt n'est transmis.
            </p>
          </div>

          <button
            type="button"
            onClick={verifyOllama}
            disabled={ollamaPending}
          >
            {ollamaPending ? "Vérification…" : "Vérifier Ollama local"}
          </button>

          {ollamaStatus && (
            <div
              className={`result ${ollamaStatus.available ? "success" : "failure"}`}
              role="status"
            >
              <strong>{ollamaStatus.available ? "PASS" : "INDISPONIBLE"}</strong>
              <span>{formatOllamaSummary(ollamaStatus)}</span>
            </div>
          )}

          {ollamaError && (
            <div className="result failure" role="alert">
              <strong>ÉCHEC IPC</strong>
              <span>{ollamaError}</span>
            </div>
          )}
        </section>
      </div>

      <footer>
        M0 utilise uniquement des contrôles locaux. Les fonctions de génération
        narrative restent désactivées à ce stade.
      </footer>
    </main>
  );
}

export default App;
