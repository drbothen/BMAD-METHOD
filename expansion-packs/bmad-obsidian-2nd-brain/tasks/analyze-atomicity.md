<!-- Powered by BMAD™ Core -->

# analyze-atomicity

Analyze a note for atomicity - determine if it contains exactly one complete knowledge building block.

## Purpose

Evaluate whether a note meets atomicity standards by running five atomicity tests and computing a composite atomicity score. Returns the score (0.0-1.0), atomicity classification (is_atomic: true/false), detected violations, and remediation suggestions.

## Prerequisites

- Note content is provided (markdown text)
- Access to building-block-types.md for type identification
- Access to atomicity-checklist.md for validation criteria
- Understanding of atomicity principles

## Inputs

- **note_content** (string, required): Full markdown content of the note
- **note_title** (string, required): Note title
- **note_path** (string, optional): Note path for uniqueness checking
- **vault_notes** (array, optional): List of note titles in vault for duplicate detection

## Outputs

```yaml
atomicity_analysis:
  is_atomic: true|false # True if score >= 0.7
  score: 0.0-1.0 # Composite atomicity score (2 decimal places)
  building_block_type: 'concept|argument|model|question|claim|phenomenon|unknown'
  violations: [] # List of failed test names
  suggestions: [] # List of remediation suggestions
  test_results:
    single_claim: {score: float, pass: bool, issues: []}
    evidence: {score: float, pass: bool, issues: []}
    self_contained: {score: float, pass: bool, issues: []}
    title: {score: float, pass: bool, issues: []}
    related_concepts: {score: float, pass: bool, issues: []}
  verdict: 'ATOMIC|BORDERLINE|NON-ATOMIC'
```

## Atomicity Tests

### Test 1: Single Claim Test

**Purpose:** Verify note expresses exactly one core claim/concept

**Algorithm:**

1. **Extract claims** from note content:
   - Identify declarative statements
   - Identify thesis-level assertions
   - Ignore supporting evidence statements
   - Ignore examples and illustrations

2. **Count independent claims:**
   - Claim is independent if it requires separate explanation
   - Core claim + supporting details = 1 claim ✓
   - Multiple standalone assertions = multiple claims ✗

3. **Score calculation:**
   ```
   score = 1.0
   for each additional_independent_claim:
     score -= 0.3
   score = max(0.0, score)
   ```

4. **Pass criteria:** score >= 0.7 (max 1 additional claim allowed)

**Detection Heuristics:**

- **Single claim signals:**
  - One main declarative statement
  - All other statements elaborate/support the main statement
  - Title reflects single topic
  - No "also", "additionally", "furthermore" introducing new claims

- **Multiple claim signals:**
  - Multiple "thesis-level" statements
  - Topic shifts within note
  - Multiple concepts requiring separate definition
  - Lists of unrelated items

**Example - PASS:**
```
"Zettelkasten uses atomic notes. Atomic notes contain one idea.
This enables flexible recombination."
```
→ 1 core claim (Zettelkasten uses atomic notes) + supporting details
→ Score: 1.0 ✓

**Example - FAIL:**
```
"Zettelkasten uses atomic notes. GTD uses context lists.
Both are productivity systems."
```
→ 3 independent claims (Zettelkasten, GTD, productivity systems)
→ Score: 1.0 - 0.3 - 0.3 = 0.4 ✗

**Violations to report:**
- "Multiple independent claims detected: [claim 1], [claim 2]"
- "Topic shifts indicate separate ideas"

**Remediation suggestions:**
- "Fragment note into N separate notes (one per claim)"
- "Extract claims: [list of claims to extract]"

### Test 2: Evidence Test

**Purpose:** Verify supporting statements relate to core claim without introducing new independent topics

**Algorithm:**

1. **Identify core claim/concept:**
   - Usually in first paragraph or heading
   - Title often indicates core claim
   - Main declarative statement

2. **Extract supporting statements:**
   - Evidence, examples, illustrations
   - Elaborations and explanations
   - Citations and references

3. **Check each supporting statement:**
   - Does it directly support the core claim? → Related ✓
   - Does it introduce NEW claims needing explanation? → Divergent ✗
   - Is it an example illustrating the core? → Related ✓

4. **Score calculation:**
   ```
   score = 1.0
   for each divergent_idea:
     score -= 0.3
   score = max(0.0, score)
   ```

5. **Pass criteria:** score >= 0.7 (max 1 divergent idea)

**Detection Heuristics:**

- **Related support signals:**
  - "For example", "such as", "like"
  - "This is because", "due to"
  - Elaborates on main topic
  - Evidence cites sources related to claim

- **Divergent support signals:**
  - Introduces new concepts requiring definition
  - Shifts to different topic area
  - "Meanwhile", "separately", "another point"
  - Comparisons that become full explanations

**Example - PASS:**
```
Core: "Spaced repetition improves retention"
Support: "Ebbinghaus curve shows memory decay without review"
Support: "Multiple exposures strengthen neural pathways"
```
→ All support directly relates to retention/memory
→ Score: 1.0 ✓

**Example - FAIL:**
```
Core: "Spaced repetition improves retention"
Support: "Anki is better than SuperMemo for implementing this"
Support: "SuperMemo was created in 1987 by Piotr Wozniak"
```
→ Introduces tool comparison (new topic)
→ Introduces software history (new topic)
→ Score: 1.0 - 0.3 - 0.3 = 0.4 ✗

**Violations to report:**
- "Divergent ideas detected: [list]"
- "Supporting evidence introduces new topics"

**Remediation suggestions:**
- "Extract tool comparison into separate note"
- "Link to related notes instead of explaining in-depth"

### Test 3: Self-Contained Test

**Purpose:** Verify note is understandable without requiring extensive external context

**Algorithm:**

1. **Identify all terms and concepts:**
   - Extract nouns and noun phrases
   - Identify technical terminology
   - Identify proper names and specialized terms

2. **Check each term:**
   - Is it defined inline or self-explanatory? → OK ✓
   - Is it common knowledge for target audience? → OK ✓
   - Does it require reading other notes to understand? → Missing ✗
   - Is context assumed without stating? → Missing ✗

3. **Check for assumed context:**
   - References to "previous sections" (none exist in atomic note)
   - "As mentioned before" (where?)
   - Assumes background knowledge not stated
   - Depends on other notes to make sense

4. **Score calculation:**
   ```
   score = 1.0
   for each undefined_critical_term:
     score -= 0.2
   for each assumed_context_element:
     score -= 0.2
   score = max(0.0, score)
   ```

5. **Pass criteria:** score >= 0.7 (max 2 missing elements)

**Detection Heuristics:**

- **Self-contained signals:**
  - Defines terms inline: "X (also known as Y)"
  - Provides brief context: "In cognitive psychology, X refers to..."
  - Uses [[WikiLinks]] with one-sentence summary
  - Stands alone as readable document

- **Context-dependent signals:**
  - Undefined acronyms or jargon
  - "As discussed earlier"
  - "The aforementioned technique"
  - References to other notes without summary

**Example - PASS:**
```
"The PARA method organizes information into Projects, Areas,
Resources, Archives. Projects are active work with deadlines.
Areas are ongoing responsibilities."
```
→ Defines all terms inline
→ Score: 1.0 ✓

**Example - FAIL:**
```
"Using the P.A.R.A. categories, my project list is getting cleaner.
The GTD weekly review helps identify Areas vs Projects."
```
→ Assumes knowledge of PARA (undefined)
→ Assumes knowledge of GTD (undefined)
→ Score: 1.0 - 0.2 - 0.2 = 0.6 ✗

**Violations to report:**
- "Undefined terms: [list]"
- "Assumed context: [list]"

**Remediation suggestions:**
- "Define 'PARA' inline or link with brief summary"
- "Add context about GTD weekly review"

### Test 4: Title Test

**Purpose:** Verify title is descriptive AND unique

**Algorithm:**

1. **Descriptiveness check:**
   - Does title indicate the core claim/concept? YES/NO
   - Is title specific (not generic)? YES/NO
   - Could you guess note content from title? YES/NO

   Descriptive if at least 2/3 YES

2. **Uniqueness check:**
   - Search vault for exact duplicate titles
   - Check for very similar titles (fuzzy match >90%)
   - Unique if no duplicates/near-duplicates

3. **Score calculation:**
   ```
   score = 1.0
   if not descriptive:
     score -= 0.4
   if not unique:
     score -= 0.4
   score = max(0.0, score)
   ```

4. **Pass criteria:** score >= 0.7 (must pass at least one criterion)

**Detection Heuristics:**

- **Descriptive title signals:**
  - Includes key concepts from note
  - Pattern: "Concept - Specific Aspect"
  - Pattern: "Topic: Detail"
  - Reflects building block type
  - Uses precise terminology

- **Generic title signals:**
  - "Notes on X" (vague)
  - "Thoughts about Y" (vague)
  - "Misc" or "Random ideas"
  - Just dates or numbers
  - "Ideas", "Notes", "Observations" alone

**Example - PASS:**
```
Title: "Zettelkasten Principle: Atomicity"
Content: Explains atomic notes concept
```
→ Descriptive (indicates concept and topic) ✓
→ Unique (no duplicates) ✓
→ Score: 1.0 ✓

**Example - FAIL:**
```
Title: "Notes on Productivity"
Content: Discusses Zettelkasten, GTD, PARA, time-blocking, deep work
```
→ Not descriptive (too generic, doesn't indicate specific topics) ✗
→ Score: 1.0 - 0.4 = 0.6 ✗

**Violations to report:**
- "Title is too generic"
- "Duplicate title found: [path]"

**Remediation suggestions:**
- "Make title more specific: suggest '[Specific Topic] - [Aspect]'"
- "Add context to differentiate from: [duplicate note]"

### Test 5: Related Concepts Test

**Purpose:** Verify related concepts are linked (not explained in depth)

**Algorithm:**

1. **Identify related concepts mentioned:**
   - Look for [[WikiLinks]]
   - Look for concept names in text
   - Look for references to other ideas

2. **Check each related concept:**
   - Is it just linked? → OK ✓
   - Is it explained in 1-2 sentences max? → OK ✓
   - Is it explained in >2 sentences? → In-depth ✗
   - Does explanation become main focus? → In-depth ✗

3. **Score calculation:**
   ```
   score = 1.0
   for each in_depth_explanation:
     score -= 0.3
   score = max(0.0, score)
   ```

4. **Pass criteria:** score >= 0.7 (max 1 in-depth explanation)

**Detection Heuristics:**

- **Linked-only signals:**
  - Simple [[WikiLink]] with no elaboration
  - "See also [[Concept]]"
  - Brief mention: "relates to [[X]]"
  - Listed in "Related Concepts" section

- **In-depth explanation signals:**
  - Multi-paragraph explanation of related concept
  - Defines related concept extensively
  - Related concept becomes co-equal focus
  - Explains mechanism/structure of related concept

**Example - PASS:**
```
"Atomic notes enable flexible linking.
See also [[Bidirectional Links]] and [[Evergreen Notes]]."
```
→ Related concepts linked only, not explained
→ Score: 1.0 ✓

**Example - FAIL:**
```
"Atomic notes enable flexible linking. Bidirectional links
connect notes in both directions, creating a web of knowledge.
Each link represents a semantic relationship between ideas.
When you link Note A to Note B, Note B automatically shows
the backlink from Note A, revealing unexpected connections..."
```
→ Explains bidirectional links in depth (4+ sentences)
→ Score: 1.0 - 0.3 = 0.7 (borderline) ⚠

**Violations to report:**
- "In-depth explanations of related concepts: [list]"

**Remediation suggestions:**
- "Extract [[Bidirectional Links]] explanation into separate note"
- "Replace explanation with brief link and 1-sentence summary"

## Composite Atomicity Score

**Algorithm:**

```python
# Calculate component scores
single_claim_score = run_single_claim_test(note)
evidence_score = run_evidence_test(note)
self_contained_score = run_self_contained_test(note)
title_score = run_title_test(note)
related_concepts_score = run_related_concepts_test(note)

# Composite score (average of all tests)
total_score = (
    single_claim_score +
    evidence_score +
    self_contained_score +
    title_score +
    related_concepts_score
) / 5.0

# Clamp to valid range
total_score = max(0.0, min(1.0, total_score))

# Round to 2 decimal places
total_score = round(total_score, 2)

# Determine atomicity
is_atomic = (total_score >= 0.7)

# Determine verdict
if total_score >= 0.7:
    verdict = "ATOMIC"
elif total_score >= 0.6:
    verdict = "BORDERLINE"  # Flag for manual review
else:
    verdict = "NON-ATOMIC"
```

## Building Block Type Identification

After running atomicity tests, identify the building block type:

1. **Check for question:** Does note end with "?" and pose inquiry?
   → If YES: **QUESTION**

2. **Check for observation:** Does note report empirical data/measurements?
   → If YES: **PHENOMENON**

3. **Check for definition:** Does note define what something IS/MEANS?
   → If YES: **CONCEPT**

4. **Check for system:** Does note describe components + relationships?
   → If YES: **MODEL**

5. **Check for argumentation:** Does note present claim + substantial evidence?
   → If YES: **ARGUMENT**

6. **Check for assertion:** Does note make claim WITHOUT substantial evidence?
   → If YES: **CLAIM**

7. **Default:** If unclear, label as **UNKNOWN** and flag for manual classification

Reference building-block-types.md for detailed classification criteria.

## Violation Detection

Collect failed tests (score < 1.0) and generate violation list:

```python
violations = []

if single_claim_score < 1.0:
    violations.append("Multiple independent claims detected")

if evidence_score < 1.0:
    violations.append("Divergent supporting evidence")

if self_contained_score < 1.0:
    violations.append("Missing context or undefined terms")

if title_score < 1.0:
    violations.append("Title not descriptive or not unique")

if related_concepts_score < 1.0:
    violations.append("In-depth explanation of related concepts")

return violations
```

## Remediation Suggestions

Based on violations, generate specific suggestions:

```python
suggestions = []

if single_claim_score < 0.7:
    suggestions.append("Fragment note into separate notes (one per claim)")
    suggestions.append(f"Detected {num_claims} independent claims")

if evidence_score < 0.7:
    suggestions.append("Extract divergent ideas into separate notes")
    suggestions.append("Link to related notes instead of explaining in-depth")

if self_contained_score < 0.7:
    suggestions.append("Define undefined terms inline or add brief context")
    suggestions.append(f"Undefined terms: {undefined_terms}")

if title_score < 0.7:
    suggestions.append("Make title more specific and descriptive")
    if not unique:
        suggestions.append("Add context to differentiate from duplicate")

if related_concepts_score < 0.7:
    suggestions.append("Replace in-depth explanations with links")
    suggestions.append(f"Extract concepts into separate notes: {concepts}")

return suggestions
```

## Output Format

Return atomicity analysis in this format:

```yaml
atomicity_analysis:
  is_atomic: true
  score: 0.85
  building_block_type: concept
  violations: []
  suggestions: []
  test_results:
    single_claim:
      score: 1.0
      pass: true
      issues: []
    evidence:
      score: 0.7
      pass: true
      issues: ["Minor divergent idea about tool selection"]
    self_contained:
      score: 1.0
      pass: true
      issues: []
    title:
      score: 1.0
      pass: true
      issues: []
    related_concepts:
      score: 0.8
      pass: true
      issues: ["One concept explained in 3 sentences"]
  verdict: "ATOMIC"
  recommendation: "Note is atomic - ready for permanent collection"
```

## Usage Notes

- Run this task via agent command: `*analyze-atomicity {note_path}`
- Can be run on individual notes or in batch
- Results feed into `*fragment-note` task for non-atomic notes
- Results used by `*validate-note` for full checklist validation
- Accuracy target: >= 90% correct atomic/non-atomic classification
