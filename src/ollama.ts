export type OllamaStatus = {
  available: boolean;
  endpoint: string;
  version: string | null;
  error: string | null;
};

export function formatOllamaSummary(status: OllamaStatus): string {
  if (status.available && status.version) {
    return `Ollama ${status.version} disponible sur ${status.endpoint}`;
  }

  return status.error
    ? `Ollama indisponible : ${status.error}`
    : "Ollama indisponible.";
}
