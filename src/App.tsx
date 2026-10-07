import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import {
  formatDatabaseSummary,
  type DatabaseStatus,
} from "./database";
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

  const [databaseStatus, setDatabaseStatus] = useState<DatabaseStatus | null>(
    null,
  );
  const [databaseError, setDatabaseError] = useState<string | null>(null);
  const [databasePending, setDatabasePending] = useState(false);

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

  async function verifyDatabase() {
    setDatabasePending(true);
    setDatabaseError(null);

    try {
      const result = await invoke<DatabaseStatus>("database_status");
      setDatabaseStatus(result);
    } catch (reason) {
      setDatabaseStatus(null);
      setDatabaseError(String(reason));
    } finally {
      setDatabasePending(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">M1.1 · fondation de persistance</p>
        <h1>Fabulaxiom</h1>
        <p className="tagline">
          Mémoire narrative locale pour construire des romans, des sagas et des
          univers cohérents.
        </p>
      </section>

      <div className="card-grid">
        <section className="card" aria-labelledby="bootstrap-title">
          <div>
            <p className="card-kicker">Socle desktop</p>
            <h2 id="bootstrap-title">Pont React → Tauri → Rust</h2>
            <p>
              Vérifie que l'interface peut appeler le cœur Rust de
              l'application.
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

        <section className="card" aria-labelledby="database-title">
          <div>
            <p className="card-kicker">Persistance locale</p>
            <h2 id="database-title">SQLite et migrations</h2>
            <p>
              Crée ou ouvre la base locale de Fabulaxiom, applique les
              migrations et vérifie l'activation des clés étrangères.
            </p>
          </div>

          <button
            type="button"
            onClick={verifyDatabase}
            disabled={databasePending}
          >
            {databasePending
              ? "Vérification…"
              : "Vérifier la base locale"}
          </button>

          {databaseStatus && (
            <div
              className={`result ${databaseStatus.available ? "success" : "failure"}`}
              role="status"
            >
              <strong>
                {databaseStatus.available ? "PASS" : "INDISPONIBLE"}
              </strong>
              <span>{formatDatabaseSummary(databaseStatus)}</span>
            </div>
          )}

          {databaseError && (
            <div className="result failure" role="alert">
              <strong>ÉCHEC IPC</strong>
              <span>{databaseError}</span>
            </div>
          )}
        </section>

        <section className="card" aria-labelledby="ollama-title">
          <div>
            <p className="card-kicker">Service IA facultatif</p>
            <h2 id="ollama-title">Ollama en lecture seule</h2>
            <p>
              Ce contrôle reste indépendant de la base : Fabulaxiom doit
              fonctionner même si Ollama est arrêté.
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
        M1.1 établit uniquement la persistance locale et les migrations. Aucun
        contenu narratif n'est encore enregistré.
      </footer>
    </main>
  );
}

export default App;
