<!-- Powered by BMAD™ Core -->

# Analyze Concept Maturation

## Purpose

Calculate maturation metrics (days-to-evergreen, edit velocity, link accumulation rate, reference velocity) and compare to vault averages to assess concept development speed.

## Inputs

- **note_path** (String, required): Path to note
- **evolution_phases** (Array, required): Phases from `identify-evolution-periods.md`
- **temporal_events** (Array, required): Events from `query-temporal-events.md`

## Outputs

- **maturation_metrics** (Object): Calculated metrics for the concept
- **vault_averages** (Object): Vault-wide averages for comparison
- **maturation_assessment** (String): Interpretation and recommendations

## Procedure

### Step 1: Calculate Days to Evergreen

```javascript
const capture_event = temporal_events.find(e => e.type === 'CAPTURE');
const promotion_event = temporal_events.find(e => e.type === 'PROMOTION');

const days_to_evergreen = promotion_event
  ? daysBetween(capture_event.timestamp, promotion_event.timestamp)
  : null;  // null if never promoted or started as evergreen
```

### Step 2: Calculate Edit Velocity

```javascript
const development_phase = evolution_phases.find(p => p.phase === 'development');

if (development_phase) {
  const development_edits = temporal_events.filter(e =>
    e.type === 'EDIT' &&
    e.timestamp >= development_phase.start &&
    e.timestamp <= development_phase.end
  );

  const development_weeks = daysBetween(development_phase.start, development_phase.end) / 7;
  const edit_velocity = development_edits.length / development_weeks;
} else {
  const edit_velocity = 0;
}
```

### Step 3: Calculate Link Accumulation Rate

```javascript
const maturation_phase = evolution_phases.find(p => p.phase === 'maturation');

if (maturation_phase) {
  const maturation_links = temporal_events.filter(e =>
    e.type === 'LINK' &&
    e.timestamp >= maturation_phase.start &&
    e.timestamp <= maturation_phase.end
  );

  const maturation_months = daysBetween(maturation_phase.start, maturation_phase.end) / 30;
  const link_accumulation_rate = maturation_links.length / maturation_months;
} else {
  const link_accumulation_rate = 0;
}
```

### Step 4: Calculate Reference Velocity

```javascript
const backlinks = temporal_events.filter(e =>
  e.type === 'LINK' && e.target === note_path
);

const note_age_months = daysBetween(capture_event.timestamp, new Date()) / 30;
const reference_velocity = backlinks.length / note_age_months;
```

### Step 5: Fetch Vault-Wide Averages

Query Neo4j for vault averages:

```cypher
// Average days to evergreen across vault
MATCH (n:Note)-[:CAPTURED_AT]->(ce:CaptureEvent)
MATCH (n)-[:PROMOTED_AT]->(pe:PromotionEvent)
WITH avg(duration.between(ce.timestamp, pe.timestamp).days) as avg_days_to_evergreen

// Average edit velocity during development
MATCH (n:Note)-[:EDITED_AT]->(ee:EditEvent)
WHERE ee.timestamp >= n.development_phase_start
  AND ee.timestamp <= n.development_phase_end
WITH avg_days_to_evergreen,
     count(ee) * 1.0 / count(DISTINCT n) /
     avg(duration.between(n.development_phase_start, n.development_phase_end).days) * 7
     as avg_edit_velocity

// Average link accumulation
MATCH (n:Note)-[l:LINKED_TO]-(other:Note)
WHERE l.created_at >= n.maturation_phase_start
  AND l.created_at <= n.maturation_phase_end
WITH avg_days_to_evergreen,
     avg_edit_velocity,
     count(l) * 1.0 / count(DISTINCT n) /
     avg(duration.between(n.maturation_phase_start, n.maturation_phase_end).days) * 30
     as avg_link_accumulation

// Average reference velocity
MATCH (n:Note)
MATCH (other:Note)-[l:LINKED_TO]->(n)
WITH avg_days_to_evergreen,
     avg_edit_velocity,
     avg_link_accumulation,
     count(l) * 1.0 / count(DISTINCT n) /
     avg(duration.between(n.captured_at, datetime()).days) * 30
     as avg_reference_velocity

RETURN
  avg_days_to_evergreen,
  avg_edit_velocity,
  avg_link_accumulation,
  avg_reference_velocity
```

### Step 6: Calculate Maturation Speed Index

Composite metric comparing note to vault average:

```javascript
const maturation_speed_index = (
  (vault_averages.days_to_evergreen / note_metrics.days_to_evergreen) * 0.3 +
  (note_metrics.edit_velocity / vault_averages.edit_velocity) * 0.3 +
  (note_metrics.link_accumulation / vault_averages.link_accumulation) * 0.2 +
  (note_metrics.reference_velocity / vault_averages.reference_velocity) * 0.2
);

// Interpretation:
// < 0.5: Slow maturer
// 0.5-1.5: Normal maturation
// > 1.5: Fast maturer
```

### Step 7: Generate Assessment Report

```markdown
## Maturation Metrics: [[Spaced Repetition]]

### Individual Metrics

**Days to Evergreen**: 5 days
- Vault Average: 18 days
- **72% faster** ✓

**Edit Velocity (Development Phase)**: 2.1 edits/week
- Vault Average: 1.4 edits/week
- **50% higher** ✓

**Link Accumulation Rate (Maturation Phase)**: 4.2 links/month
- Vault Average: 2.8 links/month
- **50% higher** ✓

**Reference Velocity**: 1.9 refs/month
- Vault Average: 0.8 refs/month
- **138% higher** ✓

### Composite Score

**Maturation Speed Index**: 1.62
**Classification**: Fast Maturer ⚡

### Interpretation

This concept matured significantly faster than vault average across all dimensions:

1. **Rapid Capture-to-Evergreen** (5 vs 18 days): Clear, immediately useful concept that required minimal development time

2. **High Edit Activity** (2.1 vs 1.4 edits/week): Active engagement during development, suggesting high priority or interest

3. **Strong Integration** (4.2 vs 2.8 links/month): Well-connected to related concepts, indicating central position in knowledge domain

4. **High Reference Rate** (1.9 vs 0.8 refs/month): Frequently cited by newer notes, suggesting foundational concept status

### Likely Reasons for Fast Maturation

- Practical relevance (learning technique directly applicable)
- Clear external sources (Wozniak papers, Ahrens book)
- Active experimentation (Anki usage provided feedback loop)
- High personal priority (aligned with knowledge management interests)

### Recommendations

Given fast maturation and high reference count:
- ✅ Maintain currency with quarterly reviews
- ✅ Consider creating sub-notes for specific algorithms (SM-2, FSRS)
- ✅ Add to relevant MOCs if not already present
- ⚠️ Monitor for splitting (if note exceeds 500 lines, consider atomicity)
```

### Step 8: Return Results

```json
{
  "maturation_metrics": {
    "days_to_evergreen": 5,
    "edit_velocity": 2.1,
    "link_accumulation_rate": 4.2,
    "reference_velocity": 1.9,
    "maturation_speed_index": 1.62
  },
  "vault_averages": {
    "days_to_evergreen": 18,
    "edit_velocity": 1.4,
    "link_accumulation_rate": 2.8,
    "reference_velocity": 0.8
  },
  "comparisons": {
    "days_to_evergreen_diff": -72,  // % faster
    "edit_velocity_diff": 50,        // % higher
    "link_accumulation_diff": 50,
    "reference_velocity_diff": 138
  },
  "classification": "fast_maturer",
  "maturation_assessment": "This concept matured significantly faster than vault average..."
}
```

## Integration Notes

**Vault Average Caching**: Cache vault averages for 24 hours to avoid repeated calculation
**Phase Dependency**: Requires accurate phase identification from `identify-evolution-periods.md`

## Error Handling

**No promotion event**: Set days_to_evergreen = null, exclude from speed index calculation
**Vault averages unavailable**: Cannot calculate speed index, provide raw metrics only
**Single-phase note**: Only calculate metrics for available phases

## Testing

**Test Case 1**: Fast maturer (speed index > 1.5), verify all metrics above average
**Test Case 2**: Slow maturer (speed index < 0.5), verify metrics below average
**Test Case 3**: Vault average calculation accuracy (compare to manual calculation)
