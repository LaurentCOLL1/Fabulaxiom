-- M3.2 SECOND-STAGE TEST-ONLY append-only correction decisions.
-- Apply only AFTER the M3.1 v7 candidate in disposable in-memory fixtures
-- or freshly created runner-owned file fixtures (never operator SQLite).
-- Never register as an automatic migration or deploy against operator data.
-- Decisions preserve old anchors and edges, and are themselves immutable.
CREATE TABLE world_time_anchor_decisions (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id))>0),
    universe_id TEXT NOT NULL,
    prior_anchor_id TEXT NOT NULL UNIQUE,
    action TEXT NOT NULL CHECK(action IN ('revoke','supersede')),
    replacement_anchor_id TEXT,
    reason TEXT NOT NULL CHECK(length(trim(reason))>0),
    source_revision_id TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK(
        (action='revoke' AND replacement_anchor_id IS NULL)
        OR (action='supersede' AND replacement_anchor_id IS NOT NULL
            AND replacement_anchor_id<>prior_anchor_id)
    ),
    FOREIGN KEY(prior_anchor_id,universe_id)
        REFERENCES world_time_anchors(id,universe_id)
        ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY(replacement_anchor_id,universe_id)
        REFERENCES world_time_anchors(id,universe_id)
        ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY(source_revision_id) REFERENCES scene_text_revisions(id)
        ON DELETE RESTRICT ON UPDATE RESTRICT
) STRICT;
CREATE INDEX idx_m32_anchor_decisions_scope
    ON world_time_anchor_decisions(universe_id,prior_anchor_id);

CREATE TRIGGER m32_anchor_decision_guard
BEFORE INSERT ON world_time_anchor_decisions
BEGIN
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'anchor decision source universe mismatch') END;
    -- Replacement must be current when selected, preventing silent forks and
    -- any cycle in the replacement chain. Future replacements of it may follow.
    SELECT CASE WHEN NEW.action='supersede' AND EXISTS(
        SELECT 1 FROM world_time_anchor_decisions d
        WHERE d.universe_id=NEW.universe_id
          AND d.prior_anchor_id=NEW.replacement_anchor_id
    ) THEN RAISE(ABORT,'anchor replacement is not current') END;
END;
CREATE TRIGGER m32_anchor_decisions_no_update
BEFORE UPDATE ON world_time_anchor_decisions
BEGIN SELECT RAISE(ABORT,'anchor decision immutable'); END;
CREATE TRIGGER m32_anchor_decisions_no_delete
BEFORE DELETE ON world_time_anchor_decisions
BEGIN SELECT RAISE(ABORT,'anchor decision immutable'); END;

-- Existing v7 precedence id is globally unique, but lacks a composite
-- (id,universe_id) UNIQUE key. Scope is therefore checked by INSERT trigger.
CREATE TABLE world_time_precedence_decisions (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id))>0),
    universe_id TEXT NOT NULL,
    prior_precedence_id TEXT NOT NULL UNIQUE,
    action TEXT NOT NULL CHECK(action IN ('revoke','supersede')),
    replacement_precedence_id TEXT,
    reason TEXT NOT NULL CHECK(length(trim(reason))>0),
    source_revision_id TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK(
        (action='revoke' AND replacement_precedence_id IS NULL)
        OR (action='supersede' AND replacement_precedence_id IS NOT NULL
            AND replacement_precedence_id<>prior_precedence_id)
    ),
    FOREIGN KEY(prior_precedence_id) REFERENCES world_time_precedences(id)
        ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY(replacement_precedence_id) REFERENCES world_time_precedences(id)
        ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY(source_revision_id) REFERENCES scene_text_revisions(id)
        ON DELETE RESTRICT ON UPDATE RESTRICT
) STRICT;
CREATE INDEX idx_m32_precedence_decisions_scope
    ON world_time_precedence_decisions(universe_id,prior_precedence_id);

CREATE TRIGGER m32_precedence_decision_guard
BEFORE INSERT ON world_time_precedence_decisions
BEGIN
    SELECT CASE WHEN NOT EXISTS(
        SELECT 1 FROM world_time_precedences p
        WHERE p.id=NEW.prior_precedence_id AND p.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'precedence decision source universe mismatch') END;
    SELECT CASE WHEN NEW.action='supersede' AND NOT EXISTS(
        SELECT 1 FROM world_time_precedences p
        WHERE p.id=NEW.replacement_precedence_id AND p.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'precedence replacement universe mismatch') END;
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'precedence decision revision universe mismatch') END;
    SELECT CASE WHEN NEW.action='supersede' AND EXISTS(
        SELECT 1 FROM world_time_precedence_decisions d
        WHERE d.prior_precedence_id=NEW.replacement_precedence_id
    ) THEN RAISE(ABORT,'precedence replacement is not current') END;
END;
CREATE TRIGGER m32_precedence_decisions_no_update
BEFORE UPDATE ON world_time_precedence_decisions
BEGIN SELECT RAISE(ABORT,'precedence decision immutable'); END;
CREATE TRIGGER m32_precedence_decisions_no_delete
BEFORE DELETE ON world_time_precedence_decisions
BEGIN SELECT RAISE(ABORT,'precedence decision immutable'); END;

-- No NEW edges may be authored against a superseded/revoked anchor.
-- Old edges are immutable historical assertions, not deleted on revocation.
CREATE TRIGGER m32_new_precedence_requires_current_anchors
BEFORE INSERT ON world_time_precedences
BEGIN
    SELECT CASE WHEN EXISTS(
        SELECT 1 FROM world_time_anchor_decisions d
        WHERE d.universe_id=NEW.universe_id AND
            d.prior_anchor_id IN (NEW.before_anchor_id,NEW.after_anchor_id)
    ) THEN RAISE(ABORT,'cannot author precedence with retired anchor') END;
END;
