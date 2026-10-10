-- M3.1 isolated schema candidate only. DO NOT register in the automatic migration runner
-- until controlled operator pre-v7 backup and migration qualification are authorized.
-- All chronology is explicitly declared; nothing is converted to Gregorian timestamps.
CREATE TABLE fictional_calendars (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id)) > 0),
    universe_id TEXT NOT NULL,
    name TEXT NOT NULL CHECK(length(trim(name)) > 0),
    definition_text TEXT NOT NULL CHECK(length(trim(definition_text)) > 0),
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id, universe_id),
    FOREIGN KEY(universe_id) REFERENCES universes(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
) STRICT;
CREATE INDEX idx_fictional_calendars_universe
    ON fictional_calendars(universe_id, id);

CREATE TABLE world_time_anchors (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id)) > 0),
    universe_id TEXT NOT NULL,
    calendar_id TEXT,
    event_entity_id TEXT,
    source_revision_id TEXT,
    time_kind TEXT NOT NULL CHECK(time_kind IN
        ('exact','approximate','relative','unknown')),
    exact_label TEXT,
    window_start_text TEXT,
    window_end_text TEXT,
    precision_text TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id, universe_id),
    FOREIGN KEY(universe_id) REFERENCES universes(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(calendar_id, universe_id)
        REFERENCES fictional_calendars(id, universe_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(event_entity_id, universe_id)
        REFERENCES narrative_entities(id, universe_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(source_revision_id) REFERENCES scene_text_revisions(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CHECK(
        (time_kind='exact' AND calendar_id IS NOT NULL
          AND exact_label IS NOT NULL AND length(trim(exact_label))>0
          AND window_start_text IS NULL AND window_end_text IS NULL
          AND (precision_text IS NULL OR length(trim(precision_text))>0))
        OR
        (time_kind='approximate' AND calendar_id IS NOT NULL
          AND exact_label IS NULL
          AND (window_start_text IS NOT NULL OR window_end_text IS NOT NULL)
          AND (window_start_text IS NULL OR length(trim(window_start_text))>0)
          AND (window_end_text IS NULL OR length(trim(window_end_text))>0)
          AND precision_text IS NOT NULL AND length(trim(precision_text))>0)
        OR
        (time_kind IN ('relative','unknown') AND calendar_id IS NULL
          AND exact_label IS NULL AND window_start_text IS NULL
          AND window_end_text IS NULL AND precision_text IS NULL)
    )
) STRICT;
CREATE INDEX idx_world_time_anchors_universe
    ON world_time_anchors(universe_id, id);
CREATE INDEX idx_world_time_anchors_calendar
    ON world_time_anchors(calendar_id, universe_id)
    WHERE calendar_id IS NOT NULL;
CREATE INDEX idx_world_time_anchors_event
    ON world_time_anchors(event_entity_id, universe_id)
    WHERE event_entity_id IS NOT NULL;
CREATE INDEX idx_world_time_anchors_revision
    ON world_time_anchors(source_revision_id)
    WHERE source_revision_id IS NOT NULL;

-- Existing SQLite FK only checks revision identity, not its indirect Universe.
-- These guards check the complete immutable source -> scene -> novel ancestry.
CREATE TRIGGER world_time_anchors_scope_guard
BEFORE INSERT ON world_time_anchors
BEGIN
    SELECT CASE WHEN NEW.event_entity_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM narrative_entities e
        WHERE e.id=NEW.event_entity_id AND e.universe_id=NEW.universe_id
          AND e.kind='event'
    ) THEN RAISE(ABORT,'world time event ownership or type mismatch') END;
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'world time revision universe mismatch') END;
END;

-- A partial order, never an invented total order. Cross-calendar precedence
-- is a separately asserted human relation, NOT a date conversion.
CREATE TABLE world_time_precedences (
    id TEXT PRIMARY KEY NOT NULL CHECK(length(trim(id))>0),
    universe_id TEXT NOT NULL,
    before_anchor_id TEXT NOT NULL,
    after_anchor_id TEXT NOT NULL,
    reason TEXT NOT NULL CHECK(length(trim(reason))>0),
    source_revision_id TEXT,
    created_at_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(before_anchor_id, after_anchor_id),
    CHECK(before_anchor_id<>after_anchor_id),
    FOREIGN KEY(before_anchor_id, universe_id)
        REFERENCES world_time_anchors(id, universe_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(after_anchor_id, universe_id)
        REFERENCES world_time_anchors(id, universe_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY(source_revision_id) REFERENCES scene_text_revisions(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
) STRICT;
CREATE INDEX idx_world_time_precedences_before
    ON world_time_precedences(universe_id, before_anchor_id, after_anchor_id);
CREATE INDEX idx_world_time_precedences_after
    ON world_time_precedences(universe_id, after_anchor_id, before_anchor_id);

CREATE TRIGGER world_time_precedences_guard
BEFORE INSERT ON world_time_precedences
BEGIN
    SELECT CASE WHEN NEW.source_revision_id IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM scene_text_revisions r
        JOIN scenes s ON s.id=r.scene_id
        JOIN chapters c ON c.id=s.chapter_id
        JOIN novels n ON n.id=c.novel_id
        WHERE r.id=NEW.source_revision_id AND n.universe_id=NEW.universe_id
    ) THEN RAISE(ABORT,'world time precedence revision universe mismatch') END;
    SELECT CASE WHEN EXISTS(
        WITH RECURSIVE reachable(anchor_id) AS (
            SELECT NEW.after_anchor_id
            UNION
            SELECT p.after_anchor_id
            FROM world_time_precedences p
            JOIN reachable r ON p.before_anchor_id=r.anchor_id
            WHERE p.universe_id=NEW.universe_id
        )
        SELECT 1 FROM reachable WHERE anchor_id=NEW.before_anchor_id
    ) THEN RAISE(ABORT,'world time precedence cycle') END;
END;

-- Correction must be modeled explicitly through future governed supersession,
-- not by silently editing or deleting previously asserted chronology.
CREATE TRIGGER fictional_calendars_no_update BEFORE UPDATE ON fictional_calendars
BEGIN SELECT RAISE(ABORT,'fictional calendar definition immutable'); END;
CREATE TRIGGER fictional_calendars_no_delete BEFORE DELETE ON fictional_calendars
BEGIN SELECT RAISE(ABORT,'fictional calendar definition immutable'); END;
CREATE TRIGGER world_time_anchors_no_update BEFORE UPDATE ON world_time_anchors
BEGIN SELECT RAISE(ABORT,'world time anchors immutable'); END;
CREATE TRIGGER world_time_anchors_no_delete BEFORE DELETE ON world_time_anchors
BEGIN SELECT RAISE(ABORT,'world time anchors immutable'); END;
CREATE TRIGGER world_time_precedences_no_update BEFORE UPDATE ON world_time_precedences
BEGIN SELECT RAISE(ABORT,'world time precedence immutable'); END;
CREATE TRIGGER world_time_precedences_no_delete BEFORE DELETE ON world_time_precedences
BEGIN SELECT RAISE(ABORT,'world time precedence immutable'); END;
