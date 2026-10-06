# Fabulaxiom — V1 Product Scope

## Product goal

Fabulaxiom is a local application for creating, editing and continuing long-form stories while preserving a persistent, verifiable narrative memory.

It must support multiple novels inside the same fictional universe and detect inconsistencies both inside one work and across works.

## Narrative hierarchy

- Universe
- optional Series
- Novel
- Chapter
- Scene

The model must also support:

- prequels, sequels and simultaneous novels;
- multiple points of view;
- flashbacks;
- alternate branches;
- fictional calendars;
- approximate time;
- universe and novel style bibles.

## Persistent memory

The V1 combines:

1. full scene text and version history;
2. structured facts;
3. full-text search;
4. semantic retrieval;
5. hierarchical summaries.

Structured data and original sources are authoritative. Summaries and embeddings are derived artifacts.

## Fact model

A fact may include:

- concerned entities;
- structured content;
- source novel/scene/version/passage;
- period of validity;
- status;
- creation method;
- uncertainty or dispute.

AI suggestions must not become canonical automatically.

## Entity model

The V1 covers:

- characters;
- places;
- organizations;
- objects;
- events;
- world rules.

Character state includes identity, aliases, appearance, age, personality, speech style, history, motivations, objectives, fears, skills, limits, secrets, possessions, health, location, actions, consequences, psychological evolution, relationships and sources.

## Knowledge model

The V1 distinguishes:

- truth of the fictional universe;
- what each character knows;
- what each character believes, including false beliefs;
- what the narrator may know;
- what the reader has learned at a given point.

## Consistency model

The V1 must be able to detect or flag:

- impossible simultaneous presence;
- impossible travel;
- age inconsistencies;
- knowledge acquired too early;
- object use before acquisition;
- missing possession transfer;
- forgotten injury/death;
- relationship inconsistency;
- effect preceding cause;
- cross-novel contradiction;
- violation of world rules.

Alerts must link sources, explain compared facts, state severity and suggest possible corrections.

## Assisted writing

The V1 includes:

- editing without AI;
- scene-goal generation;
- plans and continuation ideas;
- rewriting;
- style variants;
- dialogue;
- summaries;
- manuscript/entity search;
- sourced memory questions;
- consistency checks around generated text;
- extraction of proposed facts followed by explicit validation.

## Additional V1 capabilities

- relationship map by time;
- shared timeline;
- plot-thread tracking;
- clue/mystery/reveal tracking;
- “what if” mode outside canon;
- retcon impact analysis;
- spoiler controls;
- contradiction/validation dashboard;
- version history and restore;
- backups;
- existing-text import;
- Markdown/DOCX/EPUB export;
- documented complete-universe export/reimport;
- local visual references;
- full usability without AI.

## Privacy and safety boundary

The application listens locally by default. Manuscripts are treated as data to analyze, never as instructions that authorize system changes or command execution. No external transmission occurs without explicit consent.
