<!-- Powered by BMAD™ Core -->

# classify-content-type

Classify captured content into one of six content types with confidence scoring.

## Purpose

Automatically determine the content type (quote, concept, reference, reflection, question, observation) for captured information using heuristic analysis. Returns the classified type, confidence score (0.0-1.0), and reasoning.

## Prerequisites

- Content text is provided (minimum 10 characters)
- Access to content-type-taxonomy.md for reference
- Understanding of the 6 content types and their signals

## Inputs

- **content** (string, required): The captured content to classify
- **source** (string, optional): Source URL or description (helps with context)
- **context** (string, optional): Surrounding context if available

## Outputs

```yaml
classification:
  type: 'quote|concept|reference|reflection|question|observation'
  confidence: 0.0-1.0 # Float with 2 decimal places
  reasoning: 'Brief explanation of classification decision'
  flagged_for_review: true|false # True if confidence < 0.7
  signals_detected:
    strong: [] # List of strong signals found
    weak: [] # List of weak signals found
    contradictory: [] # List of contradictory signals
```

## Classification Heuristics

### 1. Quote Detection

**Strong Signals (weight: high):**

- Content contains quotation marks (" " or '')
- Block quote markdown formatting (>)
- Attribution present: "- Author", "by X", "according to"
- Phrases: "X said", "X writes", "X argues"
- Complete sentences with distinct voice

**Weak Signals (weight: low):**

- Long sentences (might just be quoted style)
- Names mentioned (could be about someone, not by someone)

**Contradictory Signals (penalize):**

- First-person perspective ("I think", "I believe")
- Questions without answers
- No clear attribution

### 2. Concept Detection

**Strong Signals:**

- Definitional language: "X is", "X refers to", "X means", "X represents"
- Explanatory phrases: "how X works", "the principle of X", "the theory of"
- Educational tone and structure
- Describes mechanisms, processes, frameworks
- Includes examples to illustrate
- Objective, informative language

**Weak Signals:**

- Technical terminology
- Structured formatting (lists, steps)

**Contradictory Signals:**

- Personal opinions and "I" statements
- Questions as primary structure
- Just links with no explanation

### 3. Reference Detection

**Strong Signals:**

- Contains URL or link
- Phrases: "see also", "check out", "read more at", "source:", "watch:"
- Citation format (APA, MLA style)
- Minimal surrounding content (mostly the link)
- Bookmark-like structure
- Resource recommendations

**Weak Signals:**

- Bibliography entries
- Tool mentions

**Contradictory Signals:**

- Extensive quotes or explanations
- Personal commentary and analysis
- Questions about the resource

### 4. Reflection Detection

**Strong Signals:**

- First-person pronouns: "I", "my", "me"
- Thinking verbs: "I think", "I believe", "I notice", "I realize", "I wonder"
- Synthesis language: "connecting X and Y", "this relates to", "pattern between"
- Evaluative language: "I agree/disagree", "this seems", "I'm skeptical"
- Personal voice and opinion
- Analytical or interpretive

**Weak Signals:**

- Tentative language: "might", "could", "perhaps"
- Meta-cognitive statements

**Contradictory Signals:**

- Objective facts only
- Direct quotes
- Simple links

### 5. Question Detection

**Strong Signals:**

- Ends with question mark (?)
- Interrogative words: who, what, when, where, why, how
- Phrases: "I wonder", "curious about", "how does X work"
- Expresses uncertainty or knowledge gap
- Interrogative structure throughout

**Weak Signals:**

- Speculative language

**Contradictory Signals:**

- Rhetorical question in middle of analysis
- Exclamatory question ("Really?!")
- Answers provided immediately after

### 6. Observation Detection

**Strong Signals:**

- Data points: numbers, metrics, measurements
- Objective language: "occurred", "happened", "measured", "recorded"
- Timestamps and dates
- Verifiable facts
- Past tense reporting
- Event records

**Weak Signals:**

- Logs and tracking data
- Timeline formats

**Contradictory Signals:**

- Personal interpretation or analysis
- Explanatory language (why something happened)
- First-person thinking

## Confidence Scoring Algorithm

**Implementation:**

```pseudocode
function calculateConfidence(content, signals):
  confidence = 1.0  # Start with perfect confidence

  # Count signals for the primary type
  strong_signal_count = len(signals.strong)
  contradictory_count = len(signals.contradictory)

  # Deduct for missing expected characteristics
  # Each content type should have 2-3 strong signals ideally
  expected_strong_signals = 3
  missing_signals = max(0, expected_strong_signals - strong_signal_count)
  confidence -= (missing_signals * 0.1)

  # Deduct for contradictory signals
  confidence -= (contradictory_count * 0.15)

  # Deduct if multiple types match equally
  # (Check if second-best type has similar score)
  if second_best_score >= (best_score - 0.1):
    confidence -= 0.2

  # Clamp to valid range [0.0, 1.0]
  confidence = max(0.0, min(1.0, confidence))

  return round(confidence, 2)  # 2 decimal places
```

**Special Cases:**

- **All types score < 0.4:** Default to "observation" with confidence 0.4
- **Confidence < 0.7:** Flag for manual review (flagged_for_review: true)
- **Confidence >= 0.8:** High confidence classification
- **Multiple types tied:** Use priority order: Question > Quote > Reflection > Concept > Reference > Observation

## Classification Decision Tree

Execute in this order:

1. **Check for question mark + interrogative structure** → Question
2. **Check for quotation marks + attribution** → Quote
3. **Check for URL + minimal content** → Reference
4. **Check for first-person + synthesis** → Reflection
5. **Check for definitional language** → Concept
6. **Default or factual data** → Observation

## Step-by-Step Execution

### Step 1: Scan for All Signals

For each content type, scan the content for strong signals, weak signals, and contradictory signals.

**Output:** Signal map for all 6 types

### Step 2: Score Each Type

For each type:

- Start at 1.0
- Add points for strong signals (+0.2 each)
- Add points for weak signals (+0.05 each)
- Subtract for contradictory signals (-0.15 each)
- Track raw scores

**Output:** Raw scores for all 6 types

### Step 3: Identify Best Match

- Find highest scoring type
- Check if multiple types are tied (within 0.1)
- Use priority order to break ties

**Output:** Primary type selected

### Step 4: Calculate Confidence

- Apply confidence algorithm using primary type's signals
- Check for missing expected signals
- Check for contradictory signals
- Check if second-best type is close
- Apply fallback if all scores < 0.4

**Output:** Confidence score (0.0-1.0)

### Step 5: Flag if Needed

If confidence < 0.7:

- Set flagged_for_review: true
- Add note in reasoning about ambiguity

**Output:** Flag status

### Step 6: Generate Reasoning

Create concise reasoning (1-2 sentences):

- "Classified as {type} based on {primary signals}."
- "Confidence moderate due to {reason}." (if < 0.8)
- "Flagged for manual review due to low confidence." (if < 0.7)

**Output:** Reasoning string

### Step 7: Return Result

Package all outputs into classification object.

## Examples

### Example 1: High-Confidence Quote

**Input:**

```
content: '"Knowledge work is about managing your attention, not your time." - Cal Newport'
```

**Classification:**

```yaml
classification:
  type: 'quote'
  confidence: 0.95
  reasoning: 'Classified as quote based on quotation marks and clear attribution to Cal Newport. High confidence.'
  flagged_for_review: false
  signals_detected:
    strong: ['quotation marks', 'attribution present (- Author format)']
    weak: []
    contradictory: []
```

### Example 2: Medium-Confidence Concept

**Input:**

```
content: "The Zettelkasten method is a note-taking approach that emphasizes atomic notes and linking."
```

**Classification:**

```yaml
classification:
  type: 'concept'
  confidence: 0.75
  reasoning: "Classified as concept based on definitional language ('is a', 'emphasizes'). Moderate confidence due to brevity."
  flagged_for_review: false
  signals_detected:
    strong: ["definitional language: 'is a'", 'explains what something is']
    weak: ['structured explanation']
    contradictory: []
```

### Example 3: Low-Confidence (Ambiguous)

**Input:**

```
content: "This idea seems related to what I read about GTD."
```

**Classification:**

```yaml
classification:
  type: 'reflection'
  confidence: 0.60
  reasoning: "Classified as reflection based on first-person thinking ('I read') and synthesis ('related to'). Low confidence due to minimal content and vague reference. Flagged for manual review."
  flagged_for_review: true
  signals_detected:
    strong: ['first-person pronoun', 'synthesis language']
    weak: []
    contradictory: ['reference to external resource']
```

### Example 4: Question (High Confidence)

**Input:**

```
content: "How does bi-temporal versioning differ from event sourcing?"
```

**Classification:**

```yaml
classification:
  type: 'question'
  confidence: 0.90
  reasoning: "Classified as question based on interrogative structure ('How does') and question mark. High confidence."
  flagged_for_review: false
  signals_detected:
    strong: ['question mark', "interrogative word 'how'", 'expresses knowledge gap']
    weak: []
    contradictory: []
```

### Example 5: Observation with Data

**Input:**

```
content: "My note count increased from 487 to 523 notes this month."
```

**Classification:**

```yaml
classification:
  type: 'observation'
  confidence: 0.85
  reasoning: 'Classified as observation based on quantitative data and factual reporting. High confidence.'
  flagged_for_review: false
  signals_detected:
    strong: ['data points (487, 523)', 'factual statement', 'past tense']
    weak: []
    contradictory: []
```

### Example 6: Reference (URL Present)

**Input:**

```
content: "Research on spaced repetition: https://www.gwern.net/Spaced-repetition"
```

**Classification:**

```yaml
classification:
  type: 'reference'
  confidence: 0.95
  reasoning: 'Classified as reference based on URL and minimal surrounding content. High confidence.'
  flagged_for_review: false
  signals_detected:
    strong: ['contains URL', 'minimal content around link']
    weak: []
    contradictory: []
```

## Edge Cases

### Case: Quote + Reflection Combo

**Content:** "Newport says 'Deep work is valuable.' I think this applies to note-taking too."

**Handling:**

- Primary: Reflection (first-person synthesis)
- Confidence: 0.65 (moderate, due to mixed signals)
- Flag for review: true
- Note: Consider splitting into separate captures

### Case: Question in Explanation

**Content:** "How does Zettelkasten work? It uses atomic notes linked by concepts..."

**Handling:**

- Primary: Concept (answer provided, explanatory intent)
- Confidence: 0.70 (pedagogical question, not genuine inquiry)
- Flag for review: false

### Case: Very Short Content

**Content:** "Interesting."

**Handling:**

- Primary: observation (fallback)
- Confidence: 0.40 (minimum fallback confidence)
- Flag for review: true
- Note: Content too short for confident classification

### Case: Multiple Types Equally Strong

**Content:** URL with extensive quote and personal commentary

**Handling:**

- Use priority order: Reflection > Concept > Reference
- Confidence: 0.60 (penalize for ambiguity)
- Flag for review: true
- Note: Consider splitting capture

## Error Handling

### Content Too Short

If content < 10 characters:

- Return error: "Content too short for classification (minimum 10 characters)"
- Do not attempt classification

### Content Missing

If content is null or empty:

- Return error: "Content is required for classification"

### Invalid Input

If input format is wrong:

- Return error with clear message
- Log validation failure

## Usage in Agent Commands

### \*capture command

- Call this task after metadata extraction
- Use result to populate inbox note frontmatter

### \*classify command

- Call this task to reclassify existing note
- Update note frontmatter with new classification

### \*batch-process command

- Call this task for each inbox item
- Collect low-confidence items for bulk review

## Performance Considerations

- Target: < 1 second per classification
- Pattern matching is efficient (regex-based)
- No external API calls needed
- Stateless - can process in parallel

## Testing Requirements

Test with 30-item test set (5 per type):

- Verify accuracy >= 90% (27/30 correct)
- Verify confidence scores align with difficulty
- Verify low-confidence items flagged correctly
- Test all edge cases

## Reference Data

This task references:

- `data/content-type-taxonomy.md` - Detailed type definitions and examples
- `checklists/capture-quality-checklist.md` - Quality criteria (item 2)

## Output Integration

The classification output is used by:

- `create-inbox-note.md` task - Populates frontmatter
- `capture-quality-checklist.md` - Validates confidence >= 0.5
- Inbox Triage Agent - Displays to user for confirmation
