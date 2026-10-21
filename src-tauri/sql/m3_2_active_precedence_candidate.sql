-- M3.2 STAGE 4: test-only active precedence restatements. No automatic migration.
-- This is applied after the M3.1 v7 and M3.2 decisions candidates ONLY on
-- disposable in-memory fixtures. Historical source edges remain immutable.
--
-- A restatement has a new independent ID and references a revoked original
-- v7 precedence. A new active graph considers live legacy precedences plus
-- these authored restatements; it does not silently re-date anything.
CREATE TABLE world_time_precedence_restatements (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id)) > 0),
    universe_id TEXT NOT NULL,
    revoked_precedence_id TEXT NOT NULL UNIQUE,
    before_anchor_id TEXT NOT NULL,
    after_anchor_id TEXT NOT NULL,
    reason TEXT NOT NULL CHECK(length(trim(reason)) > 0),
    source_revision_id TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK(before_anchor_id <> after_anchor_id),
    FOREIGN KEY(revoked_precedence_id) REFERENCES world_time_precedences(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(before_anchor_id,universe_id) REFERENCES world_time_anchors(id,universe_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(after_anchor_id,universe_id) REFERENCES world_time_anchors(id,universe_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(source_revision_id) REFERENCES scene_text_revisions(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
) STRICT;
CREATE INDEX idx_m32_restatements_scope
    ON world_time_precedence_restatements(universe_id,before_anchor_id,after_anchor_id);

CREATE TRIGGER m32_restatement_guard BEFORE INSERT ON world_time_precedence_restatements
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM world_time_precedences p
        JOIN world_time_precedence_decisions d ON d.prior_precedence_id=p.id
        WHERE p.id=NEW.revoked_precedence_id AND p.universe_id=NEW.universe_id
          AND d.universe_id=NEW.universe_id AND d.action='revoke'
    ) THEN RAISE(ABORT,'restatement requires same-universe revoked original') END;
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM world_time_anchor_decisions d
        WHERE d.universe_id=NEW.universe_id
          AND d.prior_anchor_id IN (NEW.before_anchor_id,NEW.after_anchor_id)
    ) THEN RAISE(ABORT,'restatement requires current anchors') END;
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'restatement revision universe mismatch') END;
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM world_time_precedences p
        WHERE p.universe_id=NEW.universe_id
          AND p.before_anchor_id=NEW.before_anchor_id
          AND p.after_anchor_id=NEW.after_anchor_id
          AND NOT EXISTS (
              SELECT 1 FROM world_time_precedence_decisions d
              WHERE d.prior_precedence_id=p.id
          )
    ) OR EXISTS (
        SELECT 1 FROM world_time_precedence_restatements t
        WHERE t.universe_id=NEW.universe_id
          AND t.before_anchor_id=NEW.before_anchor_id
          AND t.after_anchor_id=NEW.after_anchor_id
    ) THEN RAISE(ABORT,'duplicate active precedence') END;
    SELECT CASE WHEN EXISTS (
        WITH RECURSIVE active_edges(before_id,after_id) AS (
            SELECT p.before_anchor_id,p.after_anchor_id
            FROM world_time_precedences p
            WHERE p.universe_id=NEW.universe_id
              AND NOT EXISTS (
                  SELECT 1 FROM world_time_precedence_decisions d
                  WHERE d.prior_precedence_id=p.id
              )
              AND NOT EXISTS (
                  SELECT 1 FROM world_time_anchor_decisions d
                  WHERE d.universe_id=p.universe_id AND
                        d.prior_anchor_id IN (p.before_anchor_id,p.after_anchor_id)
              )
            UNION ALL
            SELECT t.before_anchor_id,t.after_anchor_id
            FROM world_time_precedence_restatements t
            WHERE t.universe_id=NEW.universe_id
              AND NOT EXISTS (
                  SELECT 1 FROM world_time_anchor_decisions d
                  WHERE d.universe_id=t.universe_id AND
                        d.prior_anchor_id IN (t.before_anchor_id,t.after_anchor_id)
              )
        ), reachable(id) AS (
            SELECT NEW.after_anchor_id
            UNION
            SELECT e.after_id FROM active_edges e
            JOIN reachable r ON e.before_id=r.id
        )
        SELECT 1 FROM reachable WHERE id=NEW.before_anchor_id
    ) THEN RAISE(ABORT,'active precedence cycle') END;
END;

CREATE TRIGGER m32_restatement_no_update BEFORE UPDATE ON world_time_precedence_restatements
BEGIN SELECT RAISE(ABORT,'restatement immutable'); END;
CREATE TRIGGER m32_restatement_no_delete BEFORE DELETE ON world_time_precedence_restatements
BEGIN SELECT RAISE(ABORT,'restatement immutable'); END;

-- Protect against cycles that a later raw-v7 INSERT would otherwise miss
-- because M3.1 has no knowledge of the separate restatement table.
-- The original v7 guard remains unchanged (and may still veto safe raw edges).
CREATE TRIGGER m32_raw_precedence_active_graph_guard
BEFORE INSERT ON world_time_precedences
BEGIN
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM world_time_precedence_restatements t
        WHERE t.universe_id=NEW.universe_id
          AND t.before_anchor_id=NEW.before_anchor_id
          AND t.after_anchor_id=NEW.after_anchor_id
    ) THEN RAISE(ABORT,'duplicate active restatement edge') END;
    SELECT CASE WHEN EXISTS (
        WITH RECURSIVE active_edges(before_id,after_id) AS (
            SELECT p.before_anchor_id,p.after_anchor_id
            FROM world_time_precedences p
            WHERE p.universe_id=NEW.universe_id
              AND NOT EXISTS (
                  SELECT 1 FROM world_time_precedence_decisions d
                  WHERE d.prior_precedence_id=p.id
              )
              AND NOT EXISTS (
                  SELECT 1 FROM world_time_anchor_decisions d
                  WHERE d.universe_id=p.universe_id AND
                        d.prior_anchor_id IN (p.before_anchor_id,p.after_anchor_id)
              )
            UNION ALL
            SELECT t.before_anchor_id,t.after_anchor_id
            FROM world_time_precedence_restatements t
            WHERE t.universe_id=NEW.universe_id
              AND NOT EXISTS (
                  SELECT 1 FROM world_time_anchor_decisions d
                  WHERE d.universe_id=t.universe_id AND
                        d.prior_anchor_id IN (t.before_anchor_id,t.after_anchor_id)
              )
        ), reachable(id) AS (
            SELECT NEW.after_anchor_id
            UNION
            SELECT e.after_id FROM active_edges e
            JOIN reachable r ON e.before_id=r.id
        )
        SELECT 1 FROM reachable WHERE id=NEW.before_anchor_id
    ) THEN RAISE(ABORT,'active precedence cycle from raw insert') END;
END;
