-- M3.2 stage 5: in-memory candidate only; never run against operator data.
-- Append-only revocation of an already authored M3.2 restatement.
-- Original v7 assertion, its correction, and its revocation are all retained.
-- Deliberately NO replacement chains, un-revocation, or automatic migration.
CREATE TABLE world_time_restatement_revocations (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id)) > 0),
    universe_id TEXT NOT NULL CHECK(length(trim(universe_id)) > 0),
    restatement_id TEXT NOT NULL UNIQUE,
    reason TEXT NOT NULL CHECK(length(trim(reason)) > 0),
    source_revision_id TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(restatement_id)
        REFERENCES world_time_precedence_restatements(id)
        ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY(source_revision_id)
        REFERENCES scene_text_revisions(id)
        ON DELETE RESTRICT ON UPDATE RESTRICT
) STRICT;
CREATE INDEX idx_m32_restatement_revocations_universe
    ON world_time_restatement_revocations(universe_id, restatement_id);

CREATE TRIGGER m32_restatement_revocations_guard
BEFORE INSERT ON world_time_restatement_revocations
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM world_time_precedence_restatements t
        WHERE t.id=NEW.restatement_id AND t.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT, 'restatement revocation wrong universe or missing') END;
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT, 'restatement revocation source universe mismatch') END;
END;
CREATE TRIGGER m32_restatement_revocations_no_update
BEFORE UPDATE ON world_time_restatement_revocations
BEGIN SELECT RAISE(ABORT, 'restatement revocation immutable'); END;
CREATE TRIGGER m32_restatement_revocations_no_delete
BEFORE DELETE ON world_time_restatement_revocations
BEGIN SELECT RAISE(ABORT, 'restatement revocation immutable'); END;

-- Stage 4 insert guards remain intentionally conservative: they may still
-- include revoked corrections in cycle/duplicate checks. They never loosen
-- the historical v7 guards. New authoring after a revoked correction needs a
-- separately governed version-chain and active-cycle trigger revision.
