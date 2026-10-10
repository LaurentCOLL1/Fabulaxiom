import {Component,type ErrorInfo,type ReactNode} from "react";
type Props={children:ReactNode};
type State={failed:boolean;message:string};
export default class FactErrorBoundary extends Component<Props,State> {
  state:State={failed:false,message:""};
  static getDerivedStateFromError(e:unknown):State {
    return {failed:true,message:e instanceof Error?e.message:"Erreur de rendu inconnue."};
  }
  componentDidCatch(error:Error,info:ErrorInfo) {
    console.error("Erreur isolée dans l'espace des faits",error,info.componentStack);
  }
  render() {
    if(!this.state.failed)return this.props.children;
    return <section className="workspace" aria-label="Faits narratifs">
      <div className="result failure" role="alert">
        <strong>Erreur d'affichage des faits</strong>
        <span>{this.state.message}</span>
        <span>Les autres modules restent accessibles ; aucune décision de canon n'a été lancée.</span>
      </div>
      <button type="button" onClick={()=>this.setState({failed:false,message:""})}>
        Réessayer l'affichage des faits
      </button>
    </section>;
  }
}
