import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import HierarchyWorkspace from "./HierarchyWorkspace";
import EntityWorkspace from "./EntityWorkspace";
import EntityErrorBoundary from "./EntityErrorBoundary";
import FactWorkspace from "./FactWorkspace";
import FactErrorBoundary from "./FactErrorBoundary";
import BackupWorkspace from "./BackupWorkspace";
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
        <p className="eyebrow">M2.5 · faits sourcés et revue humaine sans IA</p>
        <h1>Fabulaxiom</h1>
        <p className="tagline">
          Mémoire narrative locale pour construire des romans, des sagas et des
          univers cohérents.
        </p>
      </section>

      <BackupWorkspace />

      <HierarchyWorkspace />

      <EntityErrorBoundary>
        <EntityWorkspace />
      </EntityErrorBoundary>

      <FactErrorBoundary>
        <FactWorkspace />
      </FactErrorBoundary>

      <section className="diagnostics" aria-labelledby="diagnostics-title">
        <div className="section-heading">
          <div>
            <p className="card-kicker">Diagnostics séparés</p>
            <h2 id="diagnostics-title">Socle local</h2>
          </div>
          <p>
            Le CRUD et les révisions de texte n'appellent jamais Ollama. Le contrôle
            Ollama reste volontairement indépendant.
          </p>
        </div>

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
                Ouvre la base locale de Fabulaxiom et vérifie le schéma courant
                et les clés étrangères.
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
                className={
                  "result " + (databaseStatus.available ? "success" : "failure")
                }
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
                Ce contrôle reste indépendant du CRUD : la hiérarchie doit
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
                className={
                  "result " + (ollamaStatus.available ? "success" : "failure")
                }
                role="status"
              >
                <strong>
                  {ollamaStatus.available ? "PASS" : "INDISPONIBLE"}
                </strong>
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
      </section>

      <footer>
        M1.5 protège la base et les révisions par des sauvegardes contrôlées
        et une restauration non destructive. Les fonctions narratives IA restent
        hors périmètre.
      </footer>
    </main>
  );
}


type M31IsolatedPreview = {
  status: "PASS" | "FAIL";
  identity: string;
  schema_version: number | null;
  integrity_ok: boolean;
  foreign_keys_ok: boolean;
  strict_empty_time_tables: number;
  write_ipc_registered: false;
  production_migrated: false;
  error: string | null;
};

/**
 * No regular M2 components are mounted until we know the backend build flavor.
 * A preview-only backend does not register ANY historical write command.
 */
function AppGate() {
  const [preview, setPreview] = useState<M31IsolatedPreview | null | undefined>(undefined);

  useEffect(() => {
    let current = true;
    invoke<M31IsolatedPreview>("m31_readonly_preview_status")
      .then((report) => { if (current) setPreview(report); })
      .catch(() => { if (current) setPreview(null); });
    return () => { current = false; };
  }, []);

  if (preview === undefined) {
    return <main className="app-shell"><p>Vérification de l’identité applicative…</p></main>;
  }
  if (preview !== null) {
    return (
      <main className="app-shell">
        <section className="hero">
          <p className="eyebrow">M3.1 · Prévisualisation isolée · Lecture seule</p>
          <h1>Fabulaxiom — v7 isolée</h1>
          <p className="tagline">
            Diagnostic du schéma de chronologie, sans création, édition, suppression
            ou migration de données.
          </p>
        </section>
        <section className="card" aria-label="Diagnostic v7 isolé">
          <h2>{preview.status === "PASS" ? "Schéma v7 vérifié" : "Prévisualisation refusée"}</h2>
          <p>Identité : <code>{preview.identity}</code></p>
          <p>Version SQLite : {preview.schema_version ?? "non qualifiée"}</p>
          <p>Intégrité : {preview.integrity_ok ? "PASS" : "NON VALIDÉE"}</p>
          <p>Clés étrangères : {preview.foreign_keys_ok ? "PASS" : "NON VALIDÉES"}</p>
          <p>Tables temporelles STRICT et vides : {preview.strict_empty_time_tables}/3</p>
          <p>Commandes de modification enregistrées : aucune</p>
          <p>Migration en production : non</p>
          {preview.error && <p role="alert">Blocage : {preview.error}</p>}
        </section>
      </main>
    );
  }
  return <App />;
}

export default AppGate;
