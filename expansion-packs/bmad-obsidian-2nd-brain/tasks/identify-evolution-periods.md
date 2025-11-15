<!-- Powered by BMAD™ Core -->

# Identify Evolution Periods

## Purpose

Detect phase transitions in concept evolution (capture → development → maturation → maintenance) using temporal event clustering and activity pattern analysis.

## Inputs

- **temporal_events** (Array, required): Events from `query-temporal-events.md`
- **edit_history** (Array, required): Edit history from `retrieve-edit-history.md`
- **note_metadata** (Object, required): Contains creation_date, current_status

## Outputs

- **evolution_phases** (Array): List of identified phases with start/end dates, characteristics
- **phase_transitions** (Array): Key transition points with trigger events

## Procedure

### Step 1: Analyze Event Density Over Time

Cluster events into time windows to identify activity patterns:

```javascript
// Group events by week
const weeks = groupEventsByWeek(temporal_events);

// Calculate edit frequency per week
const edit_frequencies = weeks.map(week => ({
  week_start: week.start_date,
  edit_count: week.edits.length,
  link_count: week.links.length,
  total_activity: week.edits.length + week.links.length
}));
```

### Step 2: Identify Capture Phase

**Capture Phase Characteristics:**
- Duration: Hours to days (0-7 days typically)
- High initial edit frequency (multiple edits per day)
- Few or no links yet
- Triggered by CAPTURE event

**Detection Algorithm:**

```javascript
const capture_event = temporal_events.find(e => e.type === 'CAPTURE');
const capture_start = capture_event.timestamp;

// Find when edit frequency drops below 1/day for first time
const first_week_edits = edit_history.filter(e =>
  daysBetween(capture_start, e.timestamp) <= 7
);

const capture_end = first_week_edits.length > 0
  ? first_week_edits[first_week_edits.length - 1].timestamp
  : addDays(capture_start, 2);  // default 2 days if no edits

evolution_phases.push({
  phase: 'capture',
  start: capture_start,
  end: capture_end,
  duration_days: daysBetween(capture_start, capture_end),
  characteristics: {
    edit_count: first_week_edits.length,
    edit_frequency: first_week_edits.length / daysBetween(capture_start, capture_end),
    link_count: 0
  }
});
```

### Step 3: Identify Development Phase

**Development Phase Characteristics:**
- Duration: Weeks to months (1 week - 3 months typically)
- Moderate edit frequency (few times per week)
- Links being added
- May include PROMOTION event (inbox → evergreen)

**Detection Algorithm:**

```javascript
const development_start = capture_end;

// Development ends when edit frequency drops below 1/week sustained
let development_end = development_start;
let weeks_low_activity = 0;

for (const week of edit_frequencies) {
  if (week.week_start < development_start) continue;

  if (week.edit_count < 1) {
    weeks_low_activity++;
    if (weeks_low_activity >= 2) {
      // 2 consecutive weeks with <1 edit = development phase ended
      development_end = week.week_start;
      break;
    }
  } else {
    weeks_low_activity = 0;  // reset counter
  }
}

// Count edits and links during development
const development_edits = edit_history.filter(e =>
  e.timestamp >= development_start && e.timestamp < development_end
);

const development_links = temporal_events.filter(e =>
  e.type === 'LINK' && e.timestamp >= development_start && e.timestamp < development_end
);

evolution_phases.push({
  phase: 'development',
  start: development_start,
  end: development_end,
  duration_days: daysBetween(development_start, development_end),
  characteristics: {
    edit_count: development_edits.length,
    edit_velocity: development_edits.length / (daysBetween(development_start, development_end) / 7),
    link_count: development_links.length,
    promotion_event: temporal_events.find(e => e.type === 'PROMOTION')
  }
});
```

### Step 4: Identify Maturation Phase

**Maturation Phase Characteristics:**
- Duration: Months (3-12 months typically)
- Low edit frequency (< 1/week)
- Stable structure, refinements only
- Links stabilize or grow slowly

**Detection Algorithm:**

```javascript
const maturation_start = development_end;

// Maturation ends when edit frequency drops to < 1/month sustained
let maturation_end = maturation_start;
let months_very_low_activity = 0;

const months = groupEventsByMonth(edit_history);

for (const month of months) {
  if (month.start_date < maturation_start) continue;

  if (month.edit_count < 1) {
    months_very_low_activity++;
    if (months_very_low_activity >= 2) {
      maturation_end = month.start_date;
      break;
    }
  } else {
    months_very_low_activity = 0;
  }
}

// If still in maturation phase (no transition to maintenance), set end = now
if (maturation_end === maturation_start) {
  maturation_end = new Date();
}

const maturation_edits = edit_history.filter(e =>
  e.timestamp >= maturation_start && e.timestamp < maturation_end
);

const maturation_links = temporal_events.filter(e =>
  e.type === 'LINK' && e.timestamp >= maturation_start && e.timestamp < maturation_end
);

evolution_phases.push({
  phase: 'maturation',
  start: maturation_start,
  end: maturation_end,
  duration_days: daysBetween(maturation_start, maturation_end),
  characteristics: {
    edit_count: maturation_edits.length,
    edit_velocity: maturation_edits.length / (daysBetween(maturation_start, maturation_end) / 30),  // per month
    link_count: maturation_links.length,
    link_accumulation_rate: maturation_links.length / (daysBetween(maturation_start, maturation_end) / 30)
  }
});
```

### Step 5: Identify Maintenance Phase (if applicable)

**Maintenance Phase Characteristics:**
- Duration: Months to years (12+ months)
- Very low edit frequency (< 1/month)
- Edits are updates or reviews, not restructuring
- High reference count (other notes linking to this one)

**Detection Algorithm:**

```javascript
const maintenance_start = maturation_end;
const now = new Date();

// Check if enough time has passed to declare maintenance phase
if (daysBetween(maintenance_start, now) >= 90) {  // at least 3 months
  const maintenance_edits = edit_history.filter(e =>
    e.timestamp >= maintenance_start
  );

  const maintenance_links = temporal_events.filter(e =>
    e.type === 'LINK' && e.timestamp >= maintenance_start
  );

  evolution_phases.push({
    phase: 'maintenance',
    start: maintenance_start,
    end: now,
    duration_days: daysBetween(maintenance_start, now),
    characteristics: {
      edit_count: maintenance_edits.length,
      edit_velocity: maintenance_edits.length / (daysBetween(maintenance_start, now) / 30),
      link_count: maintenance_links.length,
      status: 'evergreen'
    }
  });
}
```

### Step 6: Identify Phase Transition Triggers

For each phase transition, identify what triggered the shift:

```javascript
phase_transitions = [];

// Capture → Development transition
phase_transitions.push({
  from: 'capture',
  to: 'development',
  transition_date: development_start,
  trigger: identifyTrigger(temporal_events, development_start),
  description: "Initial exploration complete, entering active development"
});

// Development → Maturation transition
phase_transitions.push({
  from: 'development',
  to: 'maturation',
  transition_date: maturation_start,
  trigger: identifyTrigger(temporal_events, maturation_start),
  description: "Edit velocity decreased, content stabilizing"
});

// (Optional) Maturation → Maintenance transition
if (evolution_phases.some(p => p.phase === 'maintenance')) {
  phase_transitions.push({
    from: 'maturation',
    to: 'maintenance',
    transition_date: maintenance_start,
    trigger: "Sustained low edit frequency, evergreen status achieved",
    description: "Note reached stable state, enters maintenance mode"
  });
}

function identifyTrigger(events, transition_date) {
  // Find significant events near transition
  const nearby_events = events.filter(e =>
    Math.abs(daysBetween(e.timestamp, transition_date)) <= 3
  );

  // Check for PROMOTION event
  const promotion = nearby_events.find(e => e.type === 'PROMOTION');
  if (promotion) return "Promoted to evergreen";

  // Check for major edit
  const major_edit = nearby_events.find(e =>
    e.type === 'EDIT' && e.edit_size >= 20
  );
  if (major_edit) return "Major revision completed";

  // Check for MOC addition
  const moc_add = nearby_events.find(e => e.type === 'MOC_ADDED');
  if (moc_add) return `Added to ${moc_add.moc} MOC`;

  // Default
  return "Natural activity decline";
}
```

### Step 7: Detect Stagnation (Warning Condition)

**Stagnation**: No edits or references for extended period

```javascript
const last_activity = temporal_events[temporal_events.length - 1];
const days_since_activity = daysBetween(last_activity.timestamp, new Date());

if (days_since_activity > 365) {
  warnings.push({
    type: 'stagnation',
    message: `No activity for ${Math.floor(days_since_activity / 30)} months. Note may be obsolete or needs review.`,
    suggested_action: "Review for relevance, update or archive"
  });
}
```

### Step 8: Generate Phase Visualization

```markdown
## Evolution Phases: [[Spaced Repetition]]

### Phase Timeline

```
CAPTURE          DEVELOPMENT        MATURATION          MAINTENANCE
Jan 15-17        Jan 18 - Mar 10    Mar 11 - Sep 15     Sep 16 - Present
(2 days)         (52 days)          (6 months)          (2 months)
████             ████████████████████████████████████████████████
High activity    Moderate activity  Low activity        Very low

Edits: 3         Edits: 22          Edits: 3            Edits: 0
Links: 0         Links: 8           Links: 2            Links: 0
Velocity: 1.5/d  Velocity: 2.1/w    Velocity: 0.5/m     Velocity: 0/m
```

### Phase Transitions

1. **Capture → Development** (Jan 17, 2024)
   - Trigger: Initial exploration complete
   - Edit frequency dropped below 1/day

2. **Development → Maturation** (Mar 10, 2024)
   - Trigger: Major revision completed
   - Content structure stabilized
   - Edit velocity dropped below 1/week

3. **Maturation → Maintenance** (Sep 15, 2024)
   - Trigger: Sustained low edit frequency
   - Note achieved evergreen status
   - Primarily referenced, rarely edited

### Current Phase: Maintenance
**Duration**: 57 days
**Status**: Evergreen, stable
**Next Review**: 2025-01-15 (quarterly review)
```

### Step 9: Return Results

```json
{
  "note_path": "notes/Spaced Repetition.md",
  "evolution_phases": [
    {
      "phase": "capture",
      "start": "2024-01-15T09:23:00Z",
      "end": "2024-01-17T18:30:00Z",
      "duration_days": 2,
      "characteristics": { ... }
    },
    {
      "phase": "development",
      "start": "2024-01-17T18:30:00Z",
      "end": "2024-03-10T14:20:00Z",
      "duration_days": 52,
      "characteristics": { ... }
    }
    // ... more phases
  ],
  "phase_transitions": [
    {
      "from": "capture",
      "to": "development",
      "transition_date": "2024-01-17T18:30:00Z",
      "trigger": "Initial exploration complete"
    }
    // ... more transitions
  ],
  "current_phase": "maintenance",
  "warnings": []
}
```

## Integration Notes

**Temporal Event Data**: Requires output from `query-temporal-events.md`
**Edit History Data**: Requires output from `retrieve-edit-history.md`
**Threshold Tuning**: Phase transition thresholds may need adjustment per user/vault

## Error Handling

**Insufficient event data**: If <5 events, cannot reliably identify phases, return single "nascent" phase
**Irregular patterns**: Flag for manual review if phase detection is ambiguous

## Testing

**Test Case 1**: Note with clear 4-phase evolution, verify all phases detected
**Test Case 2**: Recent note (< 1 month old), should only show capture/development phases
**Test Case 3**: Stagnant note (no activity 12+ months), verify stagnation warning
