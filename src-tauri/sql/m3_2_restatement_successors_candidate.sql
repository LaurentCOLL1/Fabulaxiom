-- M3.2 stage 6: ONE guarded successor after a withdrawn initial restatement.
-- Candidate for fresh in-memory fixtures only. Never auto-migrate production.
-- Supports original -> first restatement -> withdrawn -> one successor.
-- A successor itself is not yet revocable; arbitrary chains are NOT supported.
CREATE TABLE world_time_restatement_successors (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id))>0),
    universe_id TEXT NOT NULL CHECK(length(trim(universe_id))>0),
    prior_restatement_id TEXT NOT NULL UNIQUE,
    before_anchor_id TEXT NOT NULL,
    after_anchor_id TEXT NOT NULL,
    reason TEXT NOT NULL CHECK(length(trim(reason))>0),
    source_revision_id TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK(before_anchor_id<>after_anchor_id),
    FOREIGN KEY(prior_restatement_id)
        REFERENCES world_time_precedence_restatements(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(before_anchor_id,universe_id)
        REFERENCES world_time_anchors(id,universe_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(after_anchor_id,universe_id)
        REFERENCES world_time_anchors(id,universe_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(source_revision_id)
        REFERENCES scene_text_revisions(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
) STRICT;
CREATE INDEX idx_m32_successors_scope
    ON world_time_restatement_successors(universe_id,prior_restatement_id);

-- ONE source of truth for CURRENT assertions. This view deliberately does not
-- impose a total chronology; its IDs are display labels, never time values.
CREATE VIEW m32_active_precedence_projection AS
SELECT p.id AS id,p.universe_id AS universe_id,
       p.before_anchor_id AS before_anchor_id,
       p.after_anchor_id AS after_anchor_id,'legacy' AS origin
FROM world_time_precedences p
WHERE NOT EXISTS (
    SELECT 1 FROM world_time_precedence_decisions d
    WHERE d.prior_precedence_id=p.id
) AND NOT EXISTS (
    SELECT 1 FROM world_time_anchor_decisions d
    WHERE d.universe_id=p.universe_id
      AND d.prior_anchor_id IN (p.before_anchor_id,p.after_anchor_id)
)
UNION ALL
SELECT t.id,t.universe_id,t.before_anchor_id,t.after_anchor_id,'restatement'
FROM world_time_precedence_restatements t
WHERE NOT EXISTS (
    SELECT 1 FROM world_time_restatement_revocations r
    WHERE r.restatement_id=t.id AND r.universe_id=t.universe_id
) AND NOT EXISTS (
    SELECT 1 FROM world_time_anchor_decisions d
    WHERE d.universe_id=t.universe_id
      AND d.prior_anchor_id IN (t.before_anchor_id,t.after_anchor_id)
)
UNION ALL
SELECT s.id,s.universe_id,s.before_anchor_id,s.after_anchor_id,'successor'
FROM world_time_restatement_successors s
WHERE NOT EXISTS (
    SELECT 1 FROM world_time_anchor_decisions d
    WHERE d.universe_id=s.universe_id
      AND d.prior_anchor_id IN (s.before_anchor_id,s.after_anchor_id)
);

CREATE TRIGGER m32_successor_guard
BEFORE INSERT ON world_time_restatement_successors
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM world_time_precedence_restatements t
        JOIN world_time_restatement_revocations r
          ON r.restatement_id=t.id AND r.universe_id=t.universe_id
        WHERE t.id=NEW.prior_restatement_id
          AND t.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'successor requires same-universe withdrawn correction') END;
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM world_time_anchor_decisions d
        WHERE d.universe_id=NEW.universe_id
          AND d.prior_anchor_id IN (NEW.before_anchor_id,NEW.after_anchor_id)
    ) THEN RAISE(ABORT,'successor endpoints must be current') END;
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id
          AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'successor revision wrong universe') END;
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM m32_active_precedence_projection e
        WHERE e.universe_id=NEW.universe_id
          AND e.before_anchor_id=NEW.before_anchor_id
          AND e.after_anchor_id=NEW.after_anchor_id
    ) THEN RAISE(ABORT,'successor duplicate active edge') END;
    SELECT CASE WHEN EXISTS (
        WITH RECURSIVE reached(id) AS (
            SELECT NEW.after_anchor_id
            UNION
            SELECT e.after_anchor_id FROM m32_active_precedence_projection e
            JOIN reached r ON r.id=e.before_anchor_id
            WHERE e.universe_id=NEW.universe_id
        )
        SELECT 1 FROM reached WHERE id=NEW.before_anchor_id
    ) THEN RAISE(ABORT,'successor active graph cycle') END;
END;
CREATE TRIGGER m32_successor_no_update
BEFORE UPDATE ON world_time_restatement_successors
BEGIN SELECT RAISE(ABORT,'successor immutable'); END;
CREATE TRIGGER m32_successor_no_delete
BEFORE DELETE ON world_time_restatement_successors
BEGIN SELECT RAISE(ABORT,'successor immutable'); END;

-- Stage-4 restatement INSERT trigger was created before the successor table;
-- add a second gate to prevent its bypass via a different withdrawn original.
CREATE TRIGGER m32_stage6_initial_restatement_guard
BEFORE INSERT ON world_time_precedence_restatements
BEGIN
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM m32_active_precedence_projection e
        WHERE e.universe_id=NEW.universe_id
          AND e.before_anchor_id=NEW.before_anchor_id
          AND e.after_anchor_id=NEW.after_anchor_id
    ) THEN RAISE(ABORT,'restatement duplicates current successor edge') END;
    SELECT CASE WHEN EXISTS (
        WITH RECURSIVE reached(id) AS (
            SELECT NEW.after_anchor_id
            UNION
            SELECT e.after_anchor_id FROM m32_active_precedence_projection e
            JOIN reached r ON r.id=e.before_anchor_id
            WHERE e.universe_id=NEW.universe_id
        )
        SELECT 1 FROM reached WHERE id=NEW.before_anchor_id
    ) THEN RAISE(ABORT,'restatement cycle with successor') END;
END;

-- Raw-v7 precedence INSERTs must also not bypass the successor graph.
CREATE TRIGGER m32_stage6_raw_precedence_guard
BEFORE INSERT ON world_time_precedences
BEGIN
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM m32_active_precedence_projection e
        WHERE e.universe_id=NEW.universe_id
          AND e.before_anchor_id=NEW.before_anchor_id
          AND e.after_anchor_id=NEW.after_anchor_id
    ) THEN RAISE(ABORT,'raw precedence duplicates current successor edge') END;
    SELECT CASE WHEN EXISTS (
        WITH RECURSIVE reached(id) AS (
            SELECT NEW.after_anchor_id
            UNION
            SELECT e.after_anchor_id FROM m32_active_precedence_projection e
            JOIN reached r ON r.id=e.before_anchor_id
            WHERE e.universe_id=NEW.universe_id
        )
        SELECT 1 FROM reached WHERE id=NEW.before_anchor_id
    ) THEN RAISE(ABORT,'raw precedence cycle with successor') END;
END;
