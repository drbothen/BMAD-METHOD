<!-- Powered by BMAD™ Core -->

# ------------------------------------------------------------

# Temporal Accuracy Checklist

# ------------------------------------------------------------

---

checklist:
  id: temporal-accuracy-checklist
  name: Temporal Accuracy Checklist
  description: Quality gates for temporal analysis validation - ensures evolution phases, metrics, and timelines are accurate
  items:
    - "[ ] Event timestamps verified: All event timestamps match Neo4j records"
    - "[ ] Phase boundaries correct: Evolution phases (capture/development/maturation/maintenance) correctly identified"
    - "[ ] Metrics accurately calculated: Days-to-evergreen, edit velocity, link accumulation computed correctly"
    - "[ ] Influences properly attributed: Sources and triggers for understanding shifts documented with evidence"
    - "[ ] No temporal contradictions: Events in chronological order, no impossible sequences"
    - "[ ] Vault comparison valid: Metrics compared against current vault averages"
    - "[ ] Phase durations reasonable: Phases have expected durations (capture: days, development: weeks-months, etc.)"
    - "[ ] Edit velocity realistic: Edit frequency matches observed pattern"
    - "[ ] Understanding shifts justified: Each major shift has supporting evidence from edits"
    - "[ ] Maturation speed index calculated: Composite metric properly weighted and interpreted"

---

## Purpose

This checklist ensures temporal analyses and evolution narratives accurately represent concept development history without errors or misinterpretations.

## When to Use

- After generating temporal narrative via `*analyze-evolution`
- Before publishing evolution analysis
- When reviewing Timeline Constructor output
- During temporal data validation
- After calculating maturation metrics

## Quality Criteria Details

### 1. Event Timestamps Verified

**Check:** All event timestamps in narrative match Neo4j database records

**Pass Criteria:** 100% timestamp accuracy

**Verification:** Cross-reference narrative dates with Neo4j query results

**Remediation:** Re-query Neo4j for accurate timestamps

### 2. Phase Boundaries Correct

**Check:** Evolution phases correctly identified based on activity patterns

**Phase Criteria:**
- Capture: 0-7 days, high edit frequency (>1/day)
- Development: 1 week - 3 months, moderate frequency (1-3/week)
- Maturation: 3-12 months, low frequency (<1/week)
- Maintenance: 12+ months, very low frequency (<1/month)

**Pass Criteria:** Phase transitions align with activity pattern changes

**Remediation:** Re-run `identify-evolution-periods.md` with adjusted thresholds

### 3. Metrics Accurately Calculated

**Check:** All maturation metrics computed correctly

**Metrics to verify:**
- Days to evergreen = PROMOTION_date - CAPTURE_date
- Edit velocity = edit_count / weeks_in_development
- Link accumulation = link_count / months_in_maturation
- Reference velocity = backlink_count / note_age_months

**Pass Criteria:** Manual spot-check matches automated calculation

**Remediation:** Re-calculate metrics using `analyze-concept-maturation.md`

### 4. Influences Properly Attributed

**Check:** Each claimed influence has supporting evidence

**Pass Criteria:** All sources/triggers cited have corresponding events

**Example VALID:**
> "Reading Wozniak's SM-2 paper (Feb 15) triggered shift from fixed to adaptive intervals"
[Edit event on Feb 15 added citation to Wozniak paper ✓]

**Remediation:** Remove unsupported claims or find evidence in edit history

### 5. No Temporal Contradictions

**Check:** Events in chronological order, no logical impossibilities

**Common errors:**
- Edit before capture
- Promotion before creation
- Links created before linked note exists
- Understanding shift dated after conclusion written

**Pass Criteria:** Timeline internally consistent

**Remediation:** Review event sequence, correct errors

### 6. Vault Comparison Valid

**Check:** Vault averages are current and correctly applied

**Pass Criteria:** Vault averages recalculated within last 24 hours

**Remediation:** Re-query Neo4j for fresh vault-wide statistics

### 7. Phase Durations Reasonable

**Check:** Phase durations fall within expected ranges

**Expected ranges:**
- Capture: 0-14 days (typical: 2-7 days)
- Development: 7-180 days (typical: 30-90 days)
- Maturation: 90-730 days (typical: 180-365 days)

**Pass Criteria:** No phases with anomalous durations (e.g., 1-day development, 10-year capture)

**Remediation:** Review phase detection algorithm, adjust boundaries

### 8. Edit Velocity Realistic

**Check:** Calculated edit frequency matches observed pattern

**Pass Criteria:** Velocity consistent with edit event distribution

**Example valid:** 2.1 edits/week with 22 edits over 52 days ✓
**Example invalid:** 10 edits/week with 5 total edits over 10 weeks ✗

**Remediation:** Recalculate using correct time window

### 9. Understanding Shifts Justified

**Check:** Each claimed shift has evidence from edit diffs or events

**Shift types requiring evidence:**
- Contradiction: Edit introducing opposing claim
- Source integration: Citation added with substantial content expansion
- Synthesis: Multiple concept links created together
- Perspective: Significant reframing evident in edit diff

**Pass Criteria:** All shifts have supporting edit events

**Remediation:** Remove unjustified shifts or find supporting evidence

### 10. Maturation Speed Index Calculated

**Check:** Composite metric properly weighted and interpreted

**Formula verification:**
```
speed_index = (
  (vault_avg_days / note_days) * 0.3 +
  (note_velocity / vault_velocity) * 0.3 +
  (note_links / vault_links) * 0.2 +
  (note_refs / vault_refs) * 0.2
)
```

**Interpretation:**
- < 0.5: Slow maturer
- 0.5-1.5: Normal
- > 1.5: Fast maturer

**Pass Criteria:** Calculation correct and interpretation matches score

**Remediation:** Recalculate with correct formula and weights

## Scoring

**Total Items:** 10
**Pass Threshold:** >= 9/10 (90%)

Temporal accuracy requires high precision - even small errors compound over time.

## Common Errors

1. **Off-by-one date errors**: Ensure inclusive date ranges
2. **Timezone inconsistencies**: Use UTC consistently
3. **Duplicate event counting**: Deduplicate before metrics calculation
4. **Stale vault averages**: Recalculate frequently
5. **Phase overlap**: Ensure phases don't overlap (exclusive boundaries)

## Remediation Workflow

If checklist fails:

1. Identify specific accuracy errors
2. Re-query Neo4j for source data
3. Re-run temporal analysis tasks
4. Verify calculations manually for spot-check
5. Re-run checklist

## Integration

This checklist is automatically run by Timeline Constructor Agent's `*analyze-evolution` command before generating final narrative.
