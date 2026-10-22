-- M3.2 stage 8: recursive append-only correction lineage; test fixtures ONLY.
-- Apply after M3.1 v7 and M3.2 stage 2-7 candidates in a NEW in-memory DB.
-- No migration registration, operator file, production activation or GUI writes.
-- A predecessor must be WITHDRAWN before one uniquely linked child may exist.
CREATE TABLE world_time_chain_links (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id))>0),
    universe_id TEXT NOT NULL CHECK(length(trim(universe_id))>0),
    prior_successor_id TEXT UNIQUE,
    prior_chain_id TEXT UNIQUE,
    before_anchor_id TEXT NOT NULL,
    after_anchor_id TEXT NOT NULL,
    reason TEXT NOT NULL CHECK(length(trim(reason))>0),
    source_revision_id TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK((prior_successor_id IS NOT NULL AND prior_chain_id IS NULL)
       OR (prior_successor_id IS NULL AND prior_chain_id IS NOT NULL)),
    CHECK(before_anchor_id<>after_anchor_id),
    FOREIGN KEY(prior_successor_id)
       REFERENCES world_time_restatement_successors(id)
       ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(prior_chain_id)
       REFERENCES world_time_chain_links(id)
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
CREATE INDEX idx_m32_chain_links_scope
    ON world_time_chain_links(universe_id,prior_chain_id,prior_successor_id);

CREATE TABLE world_time_chain_revocations (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id))>0),
    universe_id TEXT NOT NULL CHECK(length(trim(universe_id))>0),
    chain_id TEXT NOT NULL UNIQUE,
    reason TEXT NOT NULL CHECK(length(trim(reason))>0),
    source_revision_id TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(chain_id) REFERENCES world_time_chain_links(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(source_revision_id) REFERENCES scene_text_revisions(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
) STRICT;

CREATE TRIGGER m32_chain_link_no_update
BEFORE UPDATE ON world_time_chain_links
BEGIN SELECT RAISE(ABORT,'chain link immutable'); END;
CREATE TRIGGER m32_chain_link_no_delete
BEFORE DELETE ON world_time_chain_links
BEGIN SELECT RAISE(ABORT,'chain link immutable'); END;
CREATE TRIGGER m32_chain_revocation_no_update
BEFORE UPDATE ON world_time_chain_revocations
BEGIN SELECT RAISE(ABORT,'chain revocation immutable'); END;
CREATE TRIGGER m32_chain_revocation_no_delete
BEFORE DELETE ON world_time_chain_revocations
BEGIN SELECT RAISE(ABORT,'chain revocation immutable'); END;

-- Same named read projection is used by the earlier stage-6/7 INSERT guards.
-- Legacy history, first restatement, successor and all chain links are retained
-- in their tables; only non-withdrawn assertions are in the active graph.
DROP VIEW m32_active_precedence_projection;
CREATE VIEW m32_active_precedence_projection AS
SELECT p.id,p.universe_id,p.before_anchor_id,p.after_anchor_id,'legacy' AS origin
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
)
UNION ALL
SELECT c.id,c.universe_id,c.before_anchor_id,c.after_anchor_id,'chain'
FROM world_time_chain_links c
WHERE NOT EXISTS(
    SELECT 1 FROM world_time_chain_revocations r
    WHERE r.chain_id=c.id AND r.universe_id=c.universe_id
) AND NOT EXISTS(
    SELECT 1 FROM world_time_anchor_decisions d
    WHERE d.universe_id=c.universe_id
      AND d.prior_anchor_id IN(c.before_anchor_id,c.after_anchor_id)
);

CREATE TRIGGER m32_chain_link_guard
BEFORE INSERT ON world_time_chain_links
BEGIN
    SELECT CASE WHEN NEW.prior_successor_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM world_time_restatement_successors s
        JOIN world_time_successor_revocations r
          ON r.successor_id=s.id AND r.universe_id=s.universe_id
        WHERE s.id=NEW.prior_successor_id AND s.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'chain successor parent not withdrawn in same universe') END;
    SELECT CASE WHEN NEW.prior_chain_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM world_time_chain_links c
        JOIN world_time_chain_revocations r
          ON r.chain_id=c.id AND r.universe_id=c.universe_id
        WHERE c.id=NEW.prior_chain_id AND c.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'chain parent not withdrawn in same universe') END;
    SELECT CASE WHEN EXISTS(
        SELECT 1 FROM world_time_anchor_decisions d
        WHERE d.universe_id=NEW.universe_id
          AND d.prior_anchor_id IN(NEW.before_anchor_id,NEW.after_anchor_id)
    ) THEN RAISE(ABORT,'chain endpoints not current') END;
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'chain source revision wrong universe') END;
    SELECT CASE WHEN EXISTS(
        SELECT 1 FROM m32_active_precedence_projection e
        WHERE e.universe_id=NEW.universe_id
          AND e.before_anchor_id=NEW.before_anchor_id
          AND e.after_anchor_id=NEW.after_anchor_id
    ) THEN RAISE(ABORT,'chain duplicates active edge') END;
    SELECT CASE WHEN EXISTS(
        WITH RECURSIVE reached(id) AS(
            SELECT NEW.after_anchor_id
            UNION
            SELECT e.after_anchor_id FROM m32_active_precedence_projection e
            JOIN reached r ON r.id=e.before_anchor_id
            WHERE e.universe_id=NEW.universe_id
        )
        SELECT 1 FROM reached WHERE id=NEW.before_anchor_id
    ) THEN RAISE(ABORT,'chain creates active cycle') END;
END;

CREATE TRIGGER m32_chain_revocation_guard
BEFORE INSERT ON world_time_chain_revocations
BEGIN
    SELECT CASE WHEN NOT EXISTS(
        SELECT 1 FROM world_time_chain_links c
        WHERE c.id=NEW.chain_id AND c.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'chain revocation wrong universe or missing') END;
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'chain revocation revision wrong universe') END;
END;
