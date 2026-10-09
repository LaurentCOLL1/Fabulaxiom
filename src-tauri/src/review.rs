use rusqlite::{params, Connection, OptionalExtension};
use serde::{Deserialize, Serialize};

pub const REVIEW_STATUSES: [&str; 7] = [
    "draft", "suggestion", "canon", "variant", "unknown", "ambiguous", "contradictory",
];

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct FactReviewState {
    pub fact_id: String,
    pub universe_id: String,
    pub status: String,
    pub revision_number: i64,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct ReviewEvent {
    pub id: String,
    pub fact_id: String,
    pub universe_id: String,
    pub revision_number: i64,
    pub previous_status: String,
    pub next_status: String,
    pub action_kind: String,
    pub reviewer_label: String,
    pub reason: String,
    pub recorded_at_utc: String,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct ReviewHistory {
    pub state: FactReviewState,
    pub events: Vec<ReviewEvent>,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct ReviewSnapshot {
    pub universe_id: String,
    pub reviews: Vec<FactReviewState>,
}

#[derive(Debug, Clone, Deserialize)]
pub struct ReviewFactInput {
    pub id: String,
    pub fact_id: String,
    pub universe_id: String,
    pub expected_revision: i64,
    pub next_status: String,
    pub action_kind: String,
    pub reviewer_label: String,
    pub reason: String,
    pub confirmation_phrase: Option<String>,
}

#[derive(Debug, Clone, Deserialize)]
pub struct ReviewHistoryInput {
    pub fact_id: String,
    pub universe_id: String,
}

#[derive(Debug, Clone, Deserialize)]
pub struct ReviewUniverseInput {
    pub universe_id: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct ReviewErrorPayload {
    pub code: &'static str,
    pub message: String,
}

#[derive(Debug)]
pub enum ReviewError {
    NotFound,
    CrossUniverse,
    Validation(&'static str),
    InvalidStatus,
    InvalidTransition,
    StaleRevision,
    HumanConfirmationRequired,
    Database(rusqlite::Error),
}

impl ReviewError {
    pub fn payload(&self) -> ReviewErrorPayload {
        let (code, message) = match self {
            Self::NotFound => ("not_found", "Fait ou univers introuvable."),
            Self::CrossUniverse => ("cross_universe", "Le fait ne correspond pas à cet univers."),
            Self::Validation(msg) => ("validation", msg),
            Self::InvalidStatus => ("invalid_status", "Statut de fait inconnu."),
            Self::InvalidTransition => ("invalid_transition", "Transition de revue interdite."),
            Self::StaleRevision => ("stale_revision", "La version attendue n'est plus courante."),
            Self::HumanConfirmationRequired => ("human_confirmation_required",
                "Approbation ou retrait explicite du canon requis."),
            Self::Database(_) => ("database", "Échec SQLite de la revue narrative."),
        };
        ReviewErrorPayload { code, message: message.to_owned() }
    }
}
impl From<rusqlite::Error> for ReviewError {
    fn from(value: rusqlite::Error) -> Self { Self::Database(value) }
}

fn required(value: &str) -> Result<String, ReviewError> {
    let trimmed = value.trim();
    if trimmed.is_empty() {
        return Err(ReviewError::Validation("Une donnée obligatoire est vide."));
    }
    Ok(trimmed.to_owned())
}

fn fact_scope(db: &Connection, fact_id: &str, universe_id: &str)
    -> Result<(), ReviewError>
{
    let owner: Option<String> = db.query_row(
        "SELECT universe_id FROM narrative_facts WHERE id=?1",
        params![fact_id], |r| r.get(0),
    ).optional()?;
    match owner {
        None => Err(ReviewError::NotFound),
        Some(owner) if owner != universe_id => Err(ReviewError::CrossUniverse),
        Some(_) => Ok(()),
    }
}

fn state_unchecked(db: &Connection, fact_id: &str, universe_id: &str)
    -> Result<FactReviewState, ReviewError>
{
    let last: Option<(i64, String)> = db.query_row(
        "SELECT revision_number, next_status FROM fact_review_events
         WHERE fact_id=?1 ORDER BY revision_number DESC LIMIT 1",
        params![fact_id], |r| Ok((r.get(0)?, r.get(1)?)),
    ).optional()?;
    let (revision_number, status) = last.unwrap_or((0, "draft".to_owned()));
    Ok(FactReviewState {
        fact_id: fact_id.to_owned(), universe_id: universe_id.to_owned(),
        status, revision_number,
    })
}

pub fn state(db: &Connection, fact_id: &str, universe_id: &str)
    -> Result<FactReviewState, ReviewError>
{
    let fact_id = required(fact_id)?;
    let universe_id = required(universe_id)?;
    fact_scope(db, &fact_id, &universe_id)?;
    state_unchecked(db, &fact_id, &universe_id)
}

pub fn history(db: &Connection, fact_id: &str, universe_id: &str)
    -> Result<ReviewHistory, ReviewError>
{
    let state = state(db, fact_id, universe_id)?;
    let mut statement = db.prepare(
        "SELECT id, fact_id, universe_id, revision_number, previous_status, next_status,
                action_kind, reviewer_label, reason, recorded_at_utc
         FROM fact_review_events WHERE fact_id=?1 ORDER BY revision_number ASC",
    )?;
    let events = statement.query_map(params![state.fact_id], |r| Ok(ReviewEvent {
        id: r.get(0)?, fact_id: r.get(1)?, universe_id: r.get(2)?,
        revision_number: r.get(3)?, previous_status: r.get(4)?,
        next_status: r.get(5)?, action_kind: r.get(6)?,
        reviewer_label: r.get(7)?, reason: r.get(8)?,
        recorded_at_utc: r.get(9)?,
    }))?.collect::<rusqlite::Result<Vec<_>>>()?;
    Ok(ReviewHistory { state, events })
}

pub fn snapshot(db: &Connection, universe_id: &str)
    -> Result<ReviewSnapshot, ReviewError>
{
    let universe_id = required(universe_id)?;
    let exists: i64 = db.query_row(
        "SELECT EXISTS(SELECT 1 FROM universes WHERE id=?1)",
        params![universe_id], |r| r.get(0),
    )?;
    if exists == 0 { return Err(ReviewError::NotFound); }
    let mut statement = db.prepare(
        "SELECT id FROM narrative_facts WHERE universe_id=?1 ORDER BY id",
    )?;
    let ids = statement.query_map(params![universe_id], |r| r.get::<_, String>(0))?
        .collect::<rusqlite::Result<Vec<_>>>()?;
    let reviews = ids.iter().map(|id| state_unchecked(db, id, &universe_id))
        .collect::<Result<Vec<_>, ReviewError>>()?;
    Ok(ReviewSnapshot { universe_id, reviews })
}

/// Explicit operator-requested action; caller-provided reviewer label is not authenticated.
/// No Ollama/automatic promotion path and no UI is introduced in M2.4.
pub fn review(db: &mut Connection, input: ReviewFactInput)
    -> Result<ReviewHistory, ReviewError>
{
    let id = required(&input.id)?;
    let fact_id = required(&input.fact_id)?;
    let universe_id = required(&input.universe_id)?;
    let next_status = required(&input.next_status)?;
    let action_kind = required(&input.action_kind)?;
    let reviewer_label = required(&input.reviewer_label)?;
    let reason = required(&input.reason)?;
    if !REVIEW_STATUSES.contains(&next_status.as_str()) {
        return Err(ReviewError::InvalidStatus);
    }
    if !["set_status", "approve_canon", "revoke_canon"].contains(&action_kind.as_str()) {
        return Err(ReviewError::InvalidTransition);
    }
    let tx = db.transaction()?;
    fact_scope(&tx, &fact_id, &universe_id)?;
    let current = state_unchecked(&tx, &fact_id, &universe_id)?;
    if current.revision_number != input.expected_revision {
        return Err(ReviewError::StaleRevision);
    }
    if current.status == next_status { return Err(ReviewError::InvalidTransition); }
    let approval = next_status == "canon";
    let revocation = current.status == "canon";
    if approval {
        if action_kind != "approve_canon" || input.confirmation_phrase.as_deref() != Some("APPROVE_CANON") {
            return Err(ReviewError::HumanConfirmationRequired);
        }
    } else if revocation {
        if action_kind != "revoke_canon" || input.confirmation_phrase.as_deref() != Some("REVOKE_CANON") {
            return Err(ReviewError::HumanConfirmationRequired);
        }
    } else if action_kind != "set_status" || input.confirmation_phrase.is_some() {
        return Err(ReviewError::InvalidTransition);
    }
    let human_confirmation = i64::from(approval || revocation);
    tx.execute(
        "INSERT INTO fact_review_events
         (id,fact_id,universe_id,revision_number,previous_status,next_status,
          action_kind,actor_kind,reviewer_label,human_confirmation,reason)
         VALUES(?1,?2,?3,?4,?5,?6,?7,'human',?8,?9,?10)",
        params![id, fact_id, universe_id, current.revision_number + 1,
            current.status, next_status, action_kind, reviewer_label,
            human_confirmation, reason],
    )?;
    tx.commit()?;
    history(db, &fact_id, &universe_id)
}

#[cfg(test)]
#[path="review_tests.rs"]
mod tests;
