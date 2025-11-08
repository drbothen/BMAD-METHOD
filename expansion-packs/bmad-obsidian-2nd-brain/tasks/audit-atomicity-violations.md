<!-- Powered by BMAD™ Core -->

# audit-atomicity-violations

Audit vault notes for atomicity violations using STORY-003 analyze-atomicity.md task - detect non-atomic notes and recommend fragmentation.

## Purpose

Identify notes violating atomicity principle (one complete knowledge building block) and provide actionable fragmentation recommendations.

## Prerequisites

- Obsidian MCP server configured
- STORY-003 analyze-atomicity.md task available (`.bmad-core/tasks/analyze-atomicity.md`)
- Access to atomicity-checklist.md for validation criteria
- Access to building-block-types.md for type classification

## Inputs

- **vault_path** (string, required): Path to Obsidian vault
- **sample_size** (integer, optional): Number of notes to sample (default: 10% of vault or min 20)
- **sample_strategy** (string, optional): 'random' or 'all' (default: 'random' for >200 notes, 'all' for <=200)
- **violation_threshold** (float, optional): Score below which note is flagged (default: 0.7)

## Outputs

```yaml
atomicity_audit:
  total_notes: integer
  sample_size: integer
  atomicity_violations_count: integer # In sample
  estimated_violations_vault_wide: integer # Extrapolated
  avg_atomicity_score: float # Average across sample
  audit_timestamp: string
  atomicity_violations:
    - note_path: string
      note_title: string
      atomicity_score: float # 0.0-1.0
      is_atomic: boolean # True if score >= 0.7
      verdict: string # 'ATOMIC|BORDERLINE|NON-ATOMIC'
      failed_tests: array # ['single_claim', 'evidence'] etc.
      fragmentation_recommended: boolean # True if score < 0.5
      suggestions: array # Remediation suggestions
```

## Algorithm

### Step 1: Determine Sample Size

```
if total_notes <= 200:
  sample_strategy = 'all'
  sample_size = total_notes
else:
  sample_strategy = 'random'
  sample_size = max(round(total_notes * 0.1), 20)  # 10% or min 20
```

### Step 2: Sample Notes

**Random Sampling (for large vaults):**

```
1. Query all notes via Obsidian MCP: list_notes()
2. Randomly select sample_size notes
3. Ensure representative sample (avoid clustering)
```

**All Notes (for small vaults):**

```
1. Query all notes
2. Analyze all notes (no sampling)
```

### Step 3: Run Atomicity Analysis (STORY-003)

For each sampled note:

```
1. Load `.bmad-core/tasks/analyze-atomicity.md`
2. Execute 5 atomicity tests:
   - Test 1: Single Claim Test (score -= 0.3 per extra claim)
   - Test 2: Evidence Test (score -= 0.3 per divergent idea)
   - Test 3: Self-Contained Test (score -= 0.2 per undefined term)
   - Test 4: Title Test (score -= 0.4 if not descriptive/unique)
   - Test 5: Related Concepts Test (score -= 0.3 per in-depth explanation)
3. Calculate composite atomicity score (0.0-1.0)
4. Determine verdict:
   - ATOMIC: score >= 0.7
   - BORDERLINE: score 0.5-0.69
   - NON-ATOMIC: score < 0.5
```

**Atomicity Scoring (from STORY-003):**

```
total_score = 1.0
total_score -= single_claim_deduction
total_score -= evidence_deduction
total_score -= self_contained_deduction
total_score -= title_deduction
total_score -= related_concepts_deduction
total_score = max(0.0, min(1.0, total_score))

is_atomic = (total_score >= 0.7)
```

### Step 4: Flag Violations

```
For each note:
  if atomicity_score < 0.7:
    is_violation = true
    atomicity_violations.append(note)

    if atomicity_score < 0.5:
      fragmentation_recommended = true
      suggestions.append("Fragment note using STORY-003 fragment-note.md task")
    else:
      fragmentation_recommended = false
      suggestions.append("Manual review recommended - borderline atomicity")
```

### Step 5: Extrapolate to Full Vault

```
violations_in_sample = len(atomicity_violations)
violation_rate = violations_in_sample / sample_size

estimated_violations_vault_wide = round(violation_rate * total_notes)

confidence_interval = calculate_confidence(sample_size, total_notes, violation_rate)
```

**Confidence Calculation:**

- Sample >= 100: High confidence (±5%)
- Sample 50-99: Medium confidence (±10%)
- Sample < 50: Low confidence (±15%)

### Step 6: Calculate Average Score

```
total_score = sum(note.atomicity_score for note in sampled_notes)
avg_atomicity_score = total_score / sample_size
```

## Performance Target

<10 seconds for 20-note sample

## Use Cases

**1. Vault Health Assessment**

- Estimate atomicity violations across vault
- Prioritize cleanup efforts

**2. Fragmentation Planning**

- Identify notes needing fragmentation
- Focus on severe violations (score < 0.5)

**3. Quality Improvement**

- Track atomicity improvements over time
- Measure vault maturity

## Fragmentation Recommendations

**Score < 0.5 (Severe Violation):**

- Immediate fragmentation recommended
- Use STORY-003 fragment-note.md task
- Likely to yield 3-5 atomic notes

**Score 0.5-0.69 (Borderline):**

- Manual review recommended
- May need light editing or fragmentation
- Coach user on atomicity principles

**Score >= 0.7 (Atomic):**

- No action needed
- Note meets atomicity standards

## Testing

**Test Case:** Use STORY-003 test set

- 10 atomic notes (score >= 0.7)
- 10 non-atomic notes (score < 0.7)

Expected:

- All 10 non-atomic detected as violations
- All 10 atomic pass
- Accuracy >= 90%

## Integration

Executed by:

- `*audit-atomicity [sample_size]` command
- `*audit-full` command (uses default 10% sample)
- Progressive audit batch processing

**Dependency:** Requires STORY-003 analyze-atomicity.md task
