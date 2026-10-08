import { Component, type ErrorInfo, type ReactNode } from "react";

type Props = { children: ReactNode };
type State = { failed: boolean; message: string };

export default class EntityErrorBoundary extends Component<Props, State> {
  state: State = { failed: false, message: "" };

  static getDerivedStateFromError(error: unknown): State {
    return {
      failed: true,
      message: error instanceof Error ? error.message : "Erreur d'affichage inconnue.",
    };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Affichage des entités narratives interrompu", error, info.componentStack);
  }

  render() {
    if (this.state.failed) {
      return <section className="workspace" aria-label="Entités narratives">
        <div className="result failure" role="alert">
          <strong>Erreur d'affichage des entités</strong>
          <span>{this.state.message}</span>
          <span>Les autres modules restent accessibles. Aucune suppression n'a été demandée.</span>
        </div>
        <button type="button" onClick={() => this.setState({ failed: false, message: "" })}>
          Réessayer d'afficher les entités
        </button>
      </section>;
    }
    return this.props.children;
  }
}
