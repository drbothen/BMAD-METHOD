<!-- Powered by BMAD™ Core -->

# ------------------------------------------------------------

# MOC Completeness Checklist

# ------------------------------------------------------------

---

checklist:
  id: moc-completeness-checklist
  name: MOC Completeness Checklist
  description: Quality gates for Map of Content validation - ensures MOCs provide effective navigation and synthesis across knowledge domains
  items:
    - "[ ] Overview clarity: Overview provides clear 2-3 sentence synthesis (not generic)"
    - "[ ] Core concepts defined: 5-10 foundational concepts identified with definitions"
    - "[ ] Branch summaries present: All knowledge branches have 2-3 sentence summaries"
    - "[ ] Bidirectional links: MOC links to notes AND notes link back to MOC"
    - "[ ] Emerging questions listed: At least 2 unanswered questions identified"
    - "[ ] Maturity level appropriate: Maturity level matches note count and structure depth"
    - "[ ] Temporal history recorded: Creation date and major updates documented"
    - "[ ] No orphaned notes: All discovered notes accessible via branches"
    - "[ ] Bridge paragraphs present: Related branches connected with explanatory text (if maturity >= developing)"
    - "[ ] Hierarchical structure: 2-3 levels deep (domain → branches → sub-branches)"
    - "[ ] Dataview queries valid: Optional queries execute without errors"

---

## Purpose

This checklist ensures Maps of Content meet Phase 2 quality standards for knowledge domain organization. MOCs should provide effective navigation, synthesis, and maturity tracking.

## When to Use

- After creating a new MOC via `*create-moc` command
- After updating an existing MOC via `*update-moc` command
- Before marking MOC as "established" or "comprehensive" maturity
- During MOC quality audits
- When reviewing MOC for publication or sharing

## Quality Criteria Details

### 1. Overview Clarity

**Check:** Overview synthesizes domain in 2-3 sentences, explaining what MOC covers and why it matters (not just "This MOC contains notes about X")

**Pass Criteria:** Overview is substantive and insightful

**Example PASS:**
> "Machine learning encompasses algorithms that learn patterns from data without explicit programming. From supervised classification to unsupervised clustering, these techniques enable computers to improve performance through experience. This MOC organizes core ML concepts, algorithms, and practical applications."

**Example FAIL:**
> "This MOC contains notes about machine learning. It has several branches."

**Remediation:** Rewrite overview to explain domain significance and MOC's organizational approach

### 2. Core Concepts Defined

**Check:** 5-10 foundational concepts identified, each with 1-sentence definition

**Pass Criteria:** At least 5 concepts, all with clear definitions

**Example PASS:**
- **[[Supervised Learning]]**: Learning paradigm using labeled examples to predict outcomes
- **[[Loss Functions]]**: Metrics quantifying prediction error to guide optimization
- **[[Gradient Descent]]**: Iterative algorithm minimizing loss by adjusting parameters

**Remediation:** Use MOC Constructor's `*analyze-coverage` to identify missing core concepts

### 3. Branch Summaries Present

**Check:** Every knowledge branch has 2-3 sentence summary explaining theme and relationships

**Pass Criteria:** All branches (100%) have summaries

**Remediation:** Run `generate-summaries.md` task for branches missing summaries

### 4. Bidirectional Links

**Check:** MOC links to constituent notes AND notes reference MOC back

**Pass Criteria:** >= 90% bidirectional coverage

**Remediation:** Add "Part of: [[MOC Name]]" to notes missing backlinks

### 5. Emerging Questions Listed

**Check:** At least 2 unanswered questions showing active thinking

**Pass Criteria:** Minimum 2 questions present

**Example:**
- How do transformers compare to CNNs for computer vision?
- What are ethical implications of training data bias?

**Remediation:** Review domain gaps and formulate 2-3 research questions

### 6. Maturity Level Appropriate

**Check:** Maturity level matches quantitative criteria

**Scoring:**
- Nascent: 0-10 notes, 1-2 branches
- Developing: 11-30 notes, 2-3 branches, some summaries
- Established: 31-60 notes, 3+ branches, full synthesis
- Comprehensive: 60+ notes, 4+ branches, hierarchical structure

**Pass Criteria:** Maturity level aligns with actual state

**Remediation:** Recalculate maturity using `*check-maturity` command

### 7. Temporal History Recorded

**Check:** Creation date and major updates documented

**Pass Criteria:** At least creation date present, updates logged if MOC modified

**Example:**
- 2024-11-01: MOC created with 3 branches (nascent)
- 2024-12-15: Added 4th branch, 15 new notes (developing)

**Remediation:** Add temporal history section with key milestones

### 8. No Orphaned Notes

**Check:** All notes discovered in domain are accessible via branches

**Pass Criteria:** 100% coverage (no notes excluded from structure)

**Remediation:** Review domain coverage, assign orphaned notes to branches

### 9. Bridge Paragraphs Present

**Check:** Related branches connected with explanatory paragraphs (required for developing+ maturity)

**Pass Criteria:** At least 2 bridge paragraphs for established MOCs

**Remediation:** Run `write-bridge-paragraphs.md` task

### 10. Hierarchical Structure

**Check:** Proper depth (2-3 levels: domain → branches → sub-branches)

**Pass Criteria:** Not too flat (1 level) or too deep (4+ levels)

**Remediation:** Reorganize structure, merge shallow branches or flatten deep hierarchies

### 11. Dataview Queries Valid

**Check:** Optional Dataview queries execute without errors

**Pass Criteria:** All queries valid (if present)

**Remediation:** Test queries in Obsidian, fix syntax errors

## Scoring

**Total Items:** 11
**Pass Threshold:** >= 9/11 (82%)

**Maturity-Specific Requirements:**
- Nascent: Items 1-5, 7-8 required (7/11)
- Developing: Items 1-8 required (8/11)
- Established: Items 1-9, 11 required (10/11)
- Comprehensive: All items required (11/11)

## Remediation Workflow

If checklist fails:

1. Identify failed items
2. Prioritize by maturity requirements
3. Use MOC Constructor commands:
   - `*analyze-coverage` for gaps
   - `*suggest-branches` for structure
   - `*update-moc` for enhancements
4. Re-run checklist after fixes

## Integration

This checklist is automatically run by MOC Constructor Agent's `*create-moc` and `*update-moc` commands before finalizing MOC.
