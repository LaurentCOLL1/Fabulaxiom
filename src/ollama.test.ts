import { describe, expect, it } from "vitest";
import { formatOllamaSummary, type OllamaStatus } from "./ollama";

describe("formatOllamaSummary", () => {
  it("formats an available local Ollama status", () => {
    const status: OllamaStatus = {
      available: true,
      endpoint: "http://127.0.0.1:11434",
      version: "0.40.0",
      error: null,
    };

    expect(formatOllamaSummary(status)).toBe(
      "Ollama 0.40.0 disponible sur http://127.0.0.1:11434",
    );
  });

  it("keeps the diagnostic error when Ollama is unavailable", () => {
    const status: OllamaStatus = {
      available: false,
      endpoint: "http://127.0.0.1:11434",
      version: null,
      error: "connexion refusée",
    };

    expect(formatOllamaSummary(status)).toBe(
      "Ollama indisponible : connexion refusée",
    );
  });
});
