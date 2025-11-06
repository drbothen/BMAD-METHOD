<!-- Powered by BMAD™ Core -->

# ------------------------------------------------------------

# Atomicity Checklist

# ------------------------------------------------------------

---

checklist:
  id: atomicity-checklist
  name: Atomicity Checklist
  description: Quality gates for atomic note validation - ensures notes contain exactly one complete knowledge building block
  items:
    - "[ ] Single claim test: Note expresses exactly one core claim/concept"
    - "[ ] Evidence test: Evidence supports core claim without introducing new claims"
    - "[ ] Self-contained test: Note understandable without extensive external context"
    - "[ ] Title test: Title is descriptive and unique"
    - "[ ] Related concepts test: Related concepts linked but not explained in detail"
    - "[ ] Building block test: Clear identification of building block type"
    - "[ ] Completeness test: Note contains complete thought (not fragment)"
    - "[ ] Independence test: Note can be moved/reorganized without breaking system"
    - "[ ] Link quality test: Links are bidirectional and meaningful"
    - "[ ] Metadata test: All required metadata present"
    - "[ ] Security test: No dangerous content or path traversal attempts"

---

## Purpose

This checklist ensures every note meets atomicity standards - containing exactly one complete knowledge building block that can stand alone and be recombined in unlimited ways. It serves as a quality gate to prevent non-atomic notes from entering the permanent knowledge system.

## When to Use

- After fragmenting a complex note into atomic pieces
- Before accepting a note into the permanent collection
- When validating atomicity analysis results
- During atomicity testing and validation
- When reviewing fragmented notes for quality

## Quality Criteria Details

### 1. Single Claim Test

**Check:** Note expresses exactly one core claim, concept, or observation (not multiple independent claims)

**Scoring:**
- Start: 1.0
- Deduct: -0.3 per additional independent claim
- Min: 0.0

**Pass Criteria:** Score >= 0.7 (max 1 additional claim allowed)

**Remediation if failed:**
- Identify each independent claim in the note
- Create separate notes for each claim
- Keep only one claim in the current note
- Link the separated claims if they're related

**Example PASS:**
"Zettelkasten uses atomic notes. Atomic notes contain one idea. This enables flexible recombination."
→ 1 core claim + supporting details ✓

**Example FAIL:**
"Zettelkasten uses atomic notes. GTD uses context lists. Both are productivity systems."
→ 3 independent claims (needs fragmentation) ✗

### 2. Evidence Test

**Check:** All supporting statements directly support the core claim without introducing new independent claims requiring explanation

**Scoring:**
- Start: 1.0
- Deduct: -0.3 per divergent idea requiring separate explanation
- Min: 0.0

**Pass Criteria:** Score >= 0.7 (max 1 divergent idea allowed)

**Remediation if failed:**
- Identify supporting statements that introduce new topics
- Extract divergent ideas into separate notes
- Keep only direct support in the current note
- Link to extracted notes if relevant

**Example PASS:**
Core: "Spaced repetition improves retention"
Support: "Ebbinghaus curve shows memory decay" ✓
Support: "Multiple exposures strengthen neural pathways" ✓

**Example FAIL:**
Core: "Spaced repetition improves retention"
Support: "Anki is better than SuperMemo for this"
→ Introduces tool comparison (separate topic) ✗

### 3. Self-Contained Test

**Check:** Note is understandable without requiring extensive external context or undefined terms

**Scoring:**
- Start: 1.0
- Deduct: -0.2 per undefined critical term
- Deduct: -0.2 per assumed context element
- Min: 0.0

**Pass Criteria:** Score >= 0.7 (max 2 missing elements allowed)

**Remediation if failed:**
- Define all critical terms inline
- Add necessary context to make note self-contained
- Or link to definition notes with brief inline summary
- Remove assumptions about prior knowledge

**Example PASS:**
"The PARA method organizes information into Projects, Areas, Resources, Archives. Projects are active work with deadlines."
→ Defines all terms ✓

**Example FAIL:**
"Using the P.A.R.A. categories, my project list is getting cleaner."
→ Assumes knowledge of PARA, doesn't define ✗

### 4. Title Test

**Check:** Title is descriptive (indicates core concept) AND unique (no duplicates in vault)

**Scoring:**
- Start: 1.0
- Deduct: -0.4 if not descriptive
- Deduct: -0.4 if not unique
- Min: 0.0

**Pass Criteria:** Score >= 0.7 (must pass one of two criteria)

**Remediation if failed:**
- Make title more specific and descriptive
- Add context to differentiate from similar titles
- Use pattern: "Topic - Specific Aspect" or "Concept: Detail"
- Ensure title reflects the core claim

**Example PASS:**
Title: "Zettelkasten Principle: Atomicity"
Content: Explains atomic notes
→ Descriptive + Unique ✓

**Example FAIL:**
Title: "Notes on Productivity"
Content: Discusses 5 concepts
→ Too generic ✗

### 5. Related Concepts Test

**Check:** Related concepts are linked only (not explained in depth >2 sentences)

**Scoring:**
- Start: 1.0
- Deduct: -0.3 per in-depth explanation (>2 sentences)
- Min: 0.0

**Pass Criteria:** Score >= 0.7 (max 1 in-depth explanation allowed)

**Remediation if failed:**
- Extract in-depth explanations into separate notes
- Replace explanations with links [[Concept]]
- Add brief 1-sentence context if needed
- Create atomic notes for each explained concept

**Example PASS:**
"Atomic notes enable flexible linking. See also [[Bidirectional Links]] and [[Evergreen Notes]]."
→ Links only ✓

**Example FAIL:**
"Atomic notes enable flexible linking. Bidirectional links connect notes in both directions, creating a web of knowledge..."
→ Explains concept in depth ✗

### 6. Building Block Test

**Check:** Note clearly identifies its building block type (concept, argument, model, question, claim, phenomenon)

**Scoring:**
- Pass: 1.0 if type identified correctly
- Fail: 0.0 if no type or wrong type

**Pass Criteria:** Score >= 0.7 (must identify type correctly)

**Remediation if failed:**
- Analyze note structure and content
- Classify as one of 6 building block types
- Add type to frontmatter metadata
- Restructure note if type is ambiguous

**Building Block Types:**
1. **Concept** - Definition/explanation of idea
2. **Argument** - Claim + evidence + reasoning
3. **Model** - Framework/system with components
4. **Question** - Open inquiry with context
5. **Claim** - Statement of belief/hypothesis
6. **Phenomenon** - Observed pattern/empirical finding

### 7. Completeness Test

**Check:** Note contains a complete thought, not just a fragment or partial idea

**Scoring:**
- Pass: 1.0 if complete
- Fail: 0.0 if incomplete fragment

**Pass Criteria:** Score >= 0.7 (must be complete)

**Remediation if failed:**
- Expand fragment into complete thought
- Add missing context, evidence, or explanation
- Combine with related fragments if necessary
- Delete if fragment is not salvageable

**Example PASS:**
"Spaced repetition improves retention because multiple exposures strengthen neural pathways."
→ Complete thought ✓

**Example FAIL:**
"Spaced repetition is..."
→ Fragment ✗

### 8. Independence Test

**Check:** Note can be moved, renamed, or reorganized without breaking the knowledge system

**Scoring:**
- Pass: 1.0 if independent
- Fail: 0.0 if tightly coupled to location/structure

**Pass Criteria:** Score >= 0.7 (must be independent)

**Remediation if failed:**
- Remove dependencies on folder structure
- Replace relative references with absolute [[links]]
- Ensure note makes sense out of context
- Add self-contained metadata

**Example PASS:**
Note uses [[WikiLinks]] and doesn't assume folder location
→ Independent ✓

**Example FAIL:**
Note refers to "the previous section" or "parent folder"
→ Location-dependent ✗

### 9. Link Quality Test

**Check:** Links are bidirectional and meaningful (not just random connections)

**Scoring:**
- Start: 1.0
- Deduct: -0.2 per broken or one-way link
- Deduct: -0.3 per meaningless/random link
- Min: 0.0

**Pass Criteria:** Score >= 0.7 (max 2 link quality issues)

**Remediation if failed:**
- Ensure all outgoing links have backlinks
- Add context to links (why are they related?)
- Remove random or weak connections
- Use semantic link labels when possible

**Example PASS:**
"[[Spaced Repetition]] leverages the [[Ebbinghaus Forgetting Curve]]"
→ Meaningful relationship ✓

**Example FAIL:**
Links to 20 random notes without context
→ Link spam ✗

### 10. Metadata Test

**Check:** All required metadata fields are present and valid

**Required Fields:**
- title (non-empty string)
- type (one of 6 building block types)
- building_block (matches type)
- created (valid ISO 8601 timestamp)
- atomic_score (float 0.0-1.0)
- tags (array, can be empty)

**Scoring:**
- Start: 1.0
- Deduct: -0.2 per missing required field
- Min: 0.0

**Pass Criteria:** Score >= 0.7 (max 2 missing fields allowed)

**Remediation if failed:**
- Add missing metadata fields
- Validate field formats (timestamps, types, scores)
- Ensure frontmatter YAML is valid
- Run metadata validation script

---

## Scoring Algorithm

```python
# Start with perfect atomicity
total_score = 1.0

# Apply deductions from each test
total_score += single_claim_deduction    # -0.3 per extra claim
total_score += evidence_deduction        # -0.3 per divergent idea
total_score += self_contained_deduction  # -0.2 per undefined term
total_score += title_deduction           # -0.4 if not descriptive/unique
total_score += related_concepts_deduction # -0.3 per in-depth explanation

# Binary tests (pass=1.0, fail=0.0)
total_score *= building_block_score      # 1.0 or 0.0
total_score *= completeness_score        # 1.0 or 0.0
total_score *= independence_score        # 1.0 or 0.0

# Additional deductions
total_score += link_quality_deduction    # -0.2 per link issue
total_score += metadata_deduction        # -0.2 per missing field

# Clamp to valid range
total_score = max(0.0, min(1.0, total_score))

# Determine atomicity
is_atomic = (total_score >= 0.7)
```

---

## Pass/Fail Criteria

**PASS (Atomic):** Total score >= 0.7

**BORDERLINE:** Score 0.6-0.69 (flag for manual review)

**FAIL (Non-Atomic):** Score < 0.6

**Blocking Failures (auto-fail regardless of score):**
- Building block type not identified (test 6)
- Note is incomplete fragment (test 7)
- Note is location-dependent (test 8)

**Critical Warnings (fail if not addressed):**
- Multiple independent claims (test 1)
- Extensive undefined context (test 3)
- No metadata present (test 10)

---

## Usage in Agent Commands

### \*validate-note command

Run full checklist on a note, return detailed pass/fail report with scores for each test.

### \*analyze-atomicity command

Run tests 1-5 (core atomicity tests), return atomicity score and violations.

### \*fragment-note command

After fragmentation, run checklist on each fragment to ensure all fragments are atomic (score >= 0.7).

### \*yolo mode

Still run checklist, but auto-accept borderline scores (0.6-0.69) without manual review.

---

## Testing

To test this checklist, create test notes with:

1. Multiple independent claims (expect: fail test 1)
2. Divergent supporting evidence (expect: fail test 2)
3. Undefined terms and missing context (expect: fail test 3)
4. Generic or duplicate title (expect: fail test 4)
5. In-depth explanation of related concepts (expect: fail test 5)
6. No building block type specified (expect: fail test 6)
7. Incomplete fragment (expect: fail test 7)
8. Location-dependent references (expect: fail test 8)
9. Broken or meaningless links (expect: fail test 9)
10. Missing required metadata (expect: fail test 10)

All test scenarios documented in STORY-003 testing section.

---

## Example Validation Report

```yaml
note: "2025-11-05-zettelkasten-atomicity.md"
is_atomic: true
total_score: 0.92
tests:
  single_claim: {score: 1.0, pass: true}
  evidence: {score: 1.0, pass: true}
  self_contained: {score: 0.8, pass: true, issues: ["Term 'evergreen' not defined"]}
  title: {score: 1.0, pass: true}
  related_concepts: {score: 1.0, pass: true}
  building_block: {score: 1.0, pass: true, type: "concept"}
  completeness: {score: 1.0, pass: true}
  independence: {score: 1.0, pass: true}
  link_quality: {score: 0.8, pass: true, issues: ["1 one-way link detected"]}
  metadata: {score: 1.0, pass: true}
verdict: "PASS - Note is atomic"
recommendations:
  - "Define term 'evergreen' inline or link to definition"
  - "Add backlink from [[Evergreen Notes]]"
```

### 11. Security Test

**Check:** Note paths and content do not contain dangerous patterns or security risks

**Security Checks:**
- Path validation: No directory traversal (../) attempts
- Content scanning: No script tags, JavaScript injection, eval()
- Link safety: All generated links are safe wikilinks
- Filename safety: Special characters sanitized
- Fragment limits: Max 20 fragments per note

**Scoring:**
- Pass: 1.0 if all security checks pass
- Fail: 0.0 if any security violation detected

**Pass Criteria:** Score >= 0.7 (must pass security validation)

**Remediation if failed:**
- Block dangerous content immediately
- Sanitize paths and filenames
- Strip unsafe HTML/JavaScript
- Reject if critical security violation

**Example PASS:**
Valid markdown content with safe wikilinks [[Note]]
→ No security violations ✓

**Example FAIL:**
Content contains: <script>alert('xss')</script>
→ JavaScript injection attempt ✗

