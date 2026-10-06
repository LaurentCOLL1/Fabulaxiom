import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";

type BootstrapStatus = {
  app_name: string;
  milestone: string;
  rust_bridge: string;
};

function App() {
  const [status, setStatus] = useState<BootstrapStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function verifyRustBridge() {
    setPending(true);
    setError(null);

    try {
      const result = await invoke<BootstrapStatus>("bootstrap_status");
      setStatus(result);
    } catch (reason) {
      setStatus(null);
      setError(String(reason));
    } finally {
      setPending(false);
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

      <section className="card" aria-labelledby="bootstrap-title">
        <div>
          <p className="card-kicker">Premier contrôle exécutable</p>
          <h2 id="bootstrap-title">Pont React → Tauri → Rust</h2>
          <p>
            Ce test ne modifie aucun manuscrit et ne contacte aucun service
            externe. Il vérifie uniquement que l'interface peut appeler le cœur
            Rust de l'application.
          </p>
        </div>

        <button type="button" onClick={verifyRustBridge} disabled={pending}>
          {pending ? "Vérification…" : "Tester le pont Rust"}
        </button>

        {status && (
          <div className="result success" role="status">
            <strong>PASS</strong>
            <span>{status.app_name}</span>
            <span>{status.milestone}</span>
            <span>{status.rust_bridge}</span>
          </div>
        )}

        {error && (
          <div className="result failure" role="alert">
            <strong>ÉCHEC</strong>
            <span>{error}</span>
          </div>
        )}
      </section>

      <footer>
        Ollama sera testé depuis l'application seulement après validation de ce
        premier pont local.
      </footer>
    </main>
  );
}

export default App;
