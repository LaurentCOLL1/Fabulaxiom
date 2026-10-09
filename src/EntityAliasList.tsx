import type { EntityAlias } from "./entity";

type EntityAliasListProps = {
  aliases: EntityAlias[];
  busy: boolean;
  onRename: (alias: EntityAlias) => void;
  onDelete: (alias: EntityAlias) => void;
};

export default function EntityAliasList({
  aliases, busy, onRename, onDelete,
}: EntityAliasListProps) {
  return <div className="entity-list" aria-label="Alias de l'entité">
    {aliases.map(alias => (
      <div className="entity-row" key={alias.id}>
        <span>{alias.alias}</span>
        <code>{alias.id}</code>
        <div className="entity-actions">
          <button type="button" className="secondary" disabled={busy}
            onClick={() => onRename(alias)}>Renommer</button>
          <button type="button" className="danger" disabled={busy}
            onClick={() => onDelete(alias)}>Supprimer</button>
        </div>
      </div>
    ))}
  </div>;
}
