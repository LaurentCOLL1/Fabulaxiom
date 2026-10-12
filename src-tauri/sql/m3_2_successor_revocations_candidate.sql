-- M3.2 stage 7. Test-only append-only retirement of a SECOND-generation edge.
-- v7 original + initial restatement + its withdrawal + one successor
-- remain permanently auditable. No arbitrary chain or production migration.
CREATE TABLE world_time_successor_revocations (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id)) > 0),
    universe_id TEXT NOT NULL CHECK(length(trim(universe_id)) > 0),
    successor_id TEXT NOT NULL UNIQUE,
    reason TEXT NOT NULL CHECK(length(trim(reason)) > 0),
    source_revision_id TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(successor_id) REFERENCES world_time_restatement_successors(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(source_revision_id) REFERENCES scene_text_revisions(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
) STRICT;
CREATE INDEX idx_m32_successor_revocation_scope
    ON world_time_successor_revocations(universe_id, successor_id);

CREATE TRIGGER m32_successor_revocation_guard
BEFORE INSERT ON world_time_successor_revocations
BEGIN
    SELECT CASE WHEN NOT EXISTS(
        SELECT 1 FROM world_time_restatement_successors s
        WHERE s.id=NEW.successor_id AND s.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'successor revocation wrong universe or missing') END;
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'successor revocation revision wrong universe') END;
END;
CREATE TRIGGER m32_successor_revocation_no_update
BEFORE UPDATE ON world_time_successor_revocations
BEGIN SELECT RAISE(ABORT,'successor revocation immutable'); END;
CREATE TRIGGER m32_successor_revocation_no_delete
BEFORE DELETE ON world_time_successor_revocations
BEGIN SELECT RAISE(ABORT,'successor revocation immutable'); END;

-- Replace ONLY the test-fixture's derived read projection. No assertion is
-- deleted, no predecessor trigger loosened, no production schema altered.
-- Already-created triggers refer to the view by its stable name and therefore
-- see the newly-filtered current graph on subsequent INSERT operations.
DROP VIEW m32_active_precedence_projection;
CREATE VIEW m32_active_precedence_projection AS
SELECT p.id AS id,p.universe_id AS universe_id,
       p.before_anchor_id AS before_anchor_id,
       p.after_anchor_id AS after_anchor_id,'legacy' AS origin
FROM world_time_precedences p
WHERE NOT EXISTS(
    SELECT 1 FROM world_time_precedence_decisions d
    WHERE d.prior_precedence_id=p.id
) AND NOT EXISTS(
    SELECT 1 FROM world_time_anchor_decisions d
    WHERE d.universe_id=p.universe_id
      AND d.prior_anchor_id IN(p.before_anchor_id,p.after_anchor_id)
)
UNION ALL
SELECT t.id,t.universe_id,t.before_anchor_id,t.after_anchor_id,'restatement'
FROM world_time_precedence_restatements t
WHERE NOT EXISTS(
    SELECT 1 FROM world_time_restatement_revocations r
    WHERE r.restatement_id=t.id AND r.universe_id=t.universe_id
) AND NOT EXISTS(
    SELECT 1 FROM world_time_anchor_decisions d
    WHERE d.universe_id=t.universe_id
      AND d.prior_anchor_id IN(t.before_anchor_id,t.after_anchor_id)
)
UNION ALL
SELECT s.id,s.universe_id,s.before_anchor_id,s.after_anchor_id,'successor'
FROM world_time_restatement_successors s
WHERE NOT EXISTS(
    SELECT 1 FROM world_time_successor_revocations r
    WHERE r.successor_id=s.id AND r.universe_id=s.universe_id
) AND NOT EXISTS(
    SELECT 1 FROM world_time_anchor_decisions d
    WHERE d.universe_id=s.universe_id
      AND d.prior_anchor_id IN(s.before_anchor_id,s.after_anchor_id)
);
