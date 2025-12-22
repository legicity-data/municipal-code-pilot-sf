# AGENTS.md — Legicity Municipal Code Pilot (Spanish Fork)

## Purpose
This repo contains municipal code Titles formatted for:
- consistent navigation (TOCs)
- stable citation anchors (section IDs)
- RAG retrieval + answer citations

**Title 15 (Land Use) is the reference implementation.**
Agents must treat Title 15 as the gold standard and MUST NOT refactor or “improve” it except to fix objective validation failures.

---

## Golden Rule: Do Not Break Title 15
**Title 15 is effectively read-only.**

Agents MUST NOT:
- change Title 15 section IDs / anchors
- merge or split Title 15 `<section>` boundaries
- rewrite any Title 15 legal text
- renumber sections
- remove/alter History notes

If a change is required for consistency, apply it to other Titles to match Title 15—not the other way around.

---

## Required Artifacts Per Title (Minimum)
Each Title must provide the following artifacts (matching Title 15 conventions):

1) Canonical HTML (semantic, stable anchors)
- Example: `title_15_land_use.html`
- Must use semantic structure with stable `<section id="...">` anchors.
- The `<section id="...">` is the atomic citation unit for answers.

2) Plain text export
- Example: `textfiles/title_15_land_use.txt`
- Must be a faithful text export of the HTML content (no paraphrasing).

3) TOC JSON (anchor-keyed)
- Example: `toc_title_15_land_use.json`
- Must resolve to real HTML anchors and provide hierarchical navigation.

---

## Strongly Recommended (Standardize Across All Titles)
4) Canonical JSON representation (may start as stub)
- This is the bridge to cross-title consistency, citations, and future tooling.
- If canonical JSON does not exist for a Title, create a schema-aligned stub.

5) Global schema reference
- Repo schema is authoritative (e.g., `schemas/municipal_code_v1_1_schema.json` or equivalent).
- TOCs and canonical JSON must validate against the schema where applicable.

---

## Formatting Principles (Match Title 15)
### A) Preserve Legal Fidelity
MUST NOT:
- rewrite legal substance
- “simplify” standards
- insert interpretation or rationale not present in the code
- renumber or reorder sections beyond structural wrappers

MUST:
- keep ordinance history / History notes intact
- keep published numbering as-is

### B) Stable Anchor Strategy
- `<section id="...">` anchors must be stable and deterministic.
- Avoid regenerating IDs in a way that breaks existing citations.
- If duplicates exist, resolve deterministically with suffixing (no randomness).

---

## RAG Readiness Rules
### A) Retrieval Units
- The `<section id="...">` remains the citation unit.
- Retrieval/indexing should operate on smaller **chunks within a section** to avoid context overflow.

### B) Chunking Requirements (Indexing / RAG layer)
- Split each `<section>` into semantically meaningful chunks based on block-level units:
  - paragraphs (`p`)
  - list items (`li`)
  - definitions (`dt` / `dd`)
  - similar semantic blocks
- Chunk IDs may be generated (e.g., `15_03_16_032__c1`) but MUST preserve:
  - parent `section_id` for citations
  - deterministic, repeatable chunk numbering

### C) Definitions Handling
- Where definitions exist, prefer `<dl><dt><dd>` structure.
- During chunking, treat each definition entry as retrievable on its own.
- Avoid collapsing definitions into a single mega-block.

### D) Prompt Discipline (Downstream)
- RAG answers must cite `[section_id]` and only answer from retrieved excerpts.
- If not found in excerpts, answer “not found” rather than guessing.

---

## Deal-Breaker Regressions (Stop-the-Line Failures)
Agents must avoid introducing any of the following:

1) Anchor instability
- section IDs change or no longer match TOC and citations

2) Duplicate IDs without deterministic resolution
- creates ambiguity in retrieval and citations

3) Merged `<section>` boundaries
- blurs legal boundaries; increases context bloat

4) Citation failure
- model cannot reliably cite `[section_id]` due to broken mapping

5) TOC drift
- TOC JSON hrefs point to missing anchors or wrong content

6) Definitions collapse
- definitions revert into huge blocks, causing prompt bloat and retrieval noise

---

## Title 15 Quirks: Do Not Blindly Generalize
Title 15 contains patterns that may not apply elsewhere. Agents should adapt heuristics per Title:

- Zoning templates (Permitted/Conditional/Standards) are not universal
- Title 15 has unusually dense definitions; other Titles may not
- Title 15 includes many numeric standards/tables; other Titles may be procedural/narrative
- Cross-references are frequent in Title 15; other Titles may cite differently
- Some Titles will need paragraph-first chunking rather than list-first chunking

If unsure: preserve legal fidelity + stable anchors, then adjust chunking for size and semantics.

---

## Workflow Expectations for Agents
1) Run validation in read-only mode (produce a report) before making edits.
2) Apply changes to Titles 1–14 to match Title 15 conventions.
3) Re-run validation and include a summary of:
   - what changed
   - what could not be safely normalized
   - any remaining inconsistencies
