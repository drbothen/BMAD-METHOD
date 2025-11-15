<!-- Powered by BMAD™ Core -->

# Create Chronological Narrative

## Purpose

Generate human-readable temporal narrative from event sequence, explaining how concept evolved and highlighting key understanding shifts.

## Inputs

- **temporal_events** (Array, required): Chronologically ordered events
- **evolution_phases** (Array, required): Identified phases from `identify-evolution-periods.md`
- **note_metadata** (Object, required): Note title, current status, domain

## Outputs

- **temporal_narrative** (String): Markdown formatted narrative document
- **key_shifts** (Array): Identified understanding shifts with explanations

## Procedure

### Step 1: Analyze Events for Understanding Shifts

Identify significant changes in thinking:

```javascript
key_shifts = [];

// Look for contradiction introductions
const contradiction_edits = temporal_events.filter(e =>
  e.type === 'EDIT' && e.introduced_contradiction
);

for (const edit of contradiction_edits) {
  key_shifts.push({
    date: edit.timestamp,
    type: 'contradiction',
    description: edit.contradiction_description,
    significance: 'high'
  });
}

// Look for major source integrations
const source_citations = temporal_events.filter(e =>
  e.type === 'EDIT' && e.added_citation
);

for (const edit of source_citations) {
  // Check if edit size increased significantly after citation
  if (edit.lines_changed >= 10) {
    key_shifts.push({
      date: edit.timestamp,
      type: 'source_integration',
      source: edit.citation_source,
      description: `Integrated insights from ${edit.citation_source}`,
      significance: 'high'
    });
  }
}

// Look for synthesis achievements (linking multiple concepts)
const synthesis_links = temporal_events.filter(e =>
  e.type === 'LINK' && e.relationship === 'synthesizes'
);

if (synthesis_links.length >= 3) {
  const synthesis_date = synthesis_links[synthesis_links.length - 1].timestamp;
  key_shifts.push({
    date: synthesis_date,
    type: 'synthesis',
    description: `Connected multiple concepts to form integrated understanding`,
    significance: 'high'
  });
}
```

### Step 2: Structure Narrative by Phases

Organize narrative into sections by evolution phase:

```markdown
# Temporal Evolution: [[{note_title}]]

## Overview
{summary_paragraph}

## Evolution Timeline

### Capture Phase ({phase.duration_days} days)
{capture_narrative}

### Development Phase ({phase.duration_days} days)
{development_narrative}

### Maturation Phase ({phase.duration_days} days)
{maturation_narrative}

### Current State ({current_phase})
{current_state_narrative}

## Key Understanding Shifts
{shifts_narrative}

## Influences
{influences_narrative}

## Conclusion
{conclusion_narrative}
```

### Step 3: Generate Phase Narratives

**Capture Phase Narrative:**

```javascript
function generateCaptureNarrative(phase, events) {
  const capture_event = events.find(e => e.type === 'CAPTURE');
  const source = capture_event?.source || "unknown source";

  const capture_edits = events.filter(e =>
    e.type === 'EDIT' &&
    e.timestamp >= phase.start &&
    e.timestamp <= phase.end
  );

  return `
This concept was captured on ${formatDate(phase.start)} from ${source}.
Initial exploration lasted ${phase.duration_days} days with ${capture_edits.length}
rapid edits as the core idea was articulated. The note began as ${initialForm},
focused on ${initialFocus}.
  `.trim();
}
```

**Development Phase Narrative:**

```javascript
function generateDevelopmentNarrative(phase, events, shifts) {
  const promotion = events.find(e =>
    e.type === 'PROMOTION' &&
    e.timestamp >= phase.start &&
    e.timestamp <= phase.end
  );

  const promotion_text = promotion
    ? `Promoted to evergreen on ${formatDate(promotion.timestamp)} (${daysBetween(phase.start, promotion.timestamp)} days after capture).`
    : '';

  const key_milestones = shifts.filter(s =>
    s.date >= phase.start && s.date <= phase.end
  );

  const milestone_text = key_milestones.map(m => `
**${formatDate(m.date)}**: **${capitalizeFirst(m.type)}** - ${m.description}
  `).join('\n');

  return `
Active development lasted ${phase.duration_days} days with edit velocity of
${phase.characteristics.edit_velocity.toFixed(1)} edits/week. ${promotion_text}

**Key milestones:**

${milestone_text || 'Steady development without major shifts'}

The note grew from ${initialSize} to ${endSize} lines, and ${phase.characteristics.link_count}
connections were made to related concepts.
  `.trim();
}
```

**Maturation Phase Narrative:**

```javascript
function generateMaturationNarrative(phase, events) {
  const moc_additions = events.filter(e =>
    e.type === 'MOC_ADDED' &&
    e.timestamp >= phase.start &&
    e.timestamp <= phase.end
  );

  const moc_text = moc_additions.length > 0
    ? `Added to ${moc_additions.map(m => `[[${m.moc}]]`).join(' and ')} MOC${moc_additions.length > 1 ? 's' : ''}.`
    : '';

  const reference_count = events.filter(e =>
    e.type === 'LINK' && e.target === note_path
  ).length;

  return `
Content stabilized during ${Math.floor(phase.duration_days / 30)}-month maturation phase.
Edit frequency dropped to ${phase.characteristics.edit_velocity.toFixed(1)} edits/month—
refinements rather than restructuring. ${moc_text}

The note gained ${reference_count} backlinks during this period, averaging
${(reference_count / (phase.duration_days / 30)).toFixed(1)} new references per month.
This indicates growing integration into the broader knowledge network.
  `.trim();
}
```

### Step 4: Generate Key Shifts Section

```javascript
function generateShiftsNarrative(key_shifts) {
  if (key_shifts.length === 0) {
    return "No major understanding shifts detected. Development was incremental.";
  }

  return key_shifts.map((shift, index) => `
### ${index + 1}. ${formatDate(shift.date)}: ${capitalizeFirst(shift.type)}

${shift.description}

${generateShiftContext(shift)}
  `).join('\n');
}

function generateShiftContext(shift) {
  switch (shift.type) {
    case 'contradiction':
      return `This shift represents a fundamental change in understanding. The introduction
of contradictory information suggests encountering new evidence or perspectives that
challenged initial assumptions.`;

    case 'source_integration':
      return `Reading ${shift.source} significantly influenced thinking on this topic,
expanding understanding beyond initial capture. This demonstrates how external sources
shape and deepen conceptual knowledge.`;

    case 'synthesis':
      return `Connecting multiple related concepts demonstrates conceptual maturation.
Synthesis represents moving beyond isolated facts to integrated understanding.`;

    case 'perspective':
      return `This shift in perspective or framing indicates evolving sophistication in
thinking about the topic. The same content viewed through a different lens.`;

    default:
      return '';
  }
}
```

### Step 5: Generate Influences Section

```javascript
function generateInfluencesNarrative(events) {
  const sources = events
    .filter(e => e.type === 'EDIT' && e.citation_source)
    .map(e => e.citation_source);

  const unique_sources = [...new Set(sources)];

  if (unique_sources.length === 0) {
    return "No external sources explicitly cited. Development was primarily internal synthesis.";
  }

  return `
Key sources that shaped understanding:

${unique_sources.map(source => `- **${source}** (cited ${sources.filter(s => s === source).length} time${sources.filter(s => s === source).length > 1 ? 's' : ''})`).join('\n')}

Additionally, personal experimentation and practical application informed perspective shifts,
particularly the transition from theoretical to practical understanding.
  `.trim();
}
```

### Step 6: Generate Conclusion with Metrics Comparison

```javascript
function generateConclusion(note_path, phases, metrics, vault_averages) {
  const total_days = daysBetween(phases[0].start, new Date());
  const current_phase = phases[phases.length - 1].phase;

  const days_to_evergreen = phases.find(p => p.phase === 'development')
    ?.characteristics.promotion_event
    ? daysBetween(phases[0].start, promotion_event.timestamp)
    : null;

  const comparison = days_to_evergreen
    ? days_to_evergreen < vault_averages.days_to_evergreen
      ? `${Math.round((1 - days_to_evergreen / vault_averages.days_to_evergreen) * 100)}% faster than vault average`
      : `${Math.round((days_to_evergreen / vault_averages.days_to_evergreen - 1) * 100)}% slower than vault average`
    : 'Comparison unavailable';

  return `
This concept evolved over ${Math.floor(total_days / 30)} months from initial capture to
current ${current_phase} phase. ${days_to_evergreen ? `Maturation to evergreen status
took ${days_to_evergreen} days (${comparison}).` : ''}

Development pattern shows ${metrics.key_shifts > 2 ? 'rich' : 'moderate'} conceptual
evolution with ${metrics.key_shifts} major understanding shifts. The note's integration
into the broader knowledge network is ${metrics.reference_velocity > vault_averages.reference_velocity ? 'above' : 'below'}
average, indicating ${metrics.reference_velocity > vault_averages.reference_velocity ? 'strong foundational status' : 'specialized focus'}.

**Maturation Speed Index**: ${metrics.maturation_speed_index.toFixed(2)}
(${metrics.maturation_speed_index > 1.5 ? 'fast' : metrics.maturation_speed_index > 0.5 ? 'normal' : 'slow'} maturer)
  `.trim();
}
```

### Step 7: Assemble Complete Narrative

```javascript
temporal_narrative = `
# Temporal Evolution: [[${note_metadata.title}]]

## Overview

${generateOverview(phases, key_shifts)}

## Evolution Timeline

${phases.map(phase => `
### ${capitalizeFirst(phase.phase)} Phase (${formatDateRange(phase.start, phase.end)})
**Duration**: ${phase.duration_days} days

${generatePhaseNarrative(phase, temporal_events, key_shifts)}
`).join('\n')}

### Current State (${current_phase})

${generateCurrentState(temporal_events, phases)}

## Key Understanding Shifts

${generateShiftsNarrative(key_shifts)}

## Influences

${generateInfluencesNarrative(temporal_events)}

## Maturation Metrics vs. Vault Average

${generateMetricsComparison(metrics, vault_averages)}

## Conclusion

${generateConclusion(note_path, phases, metrics, vault_averages)}
`.trim();
```

### Step 8: Return Results

```json
{
  "temporal_narrative": "# Temporal Evolution: [[Spaced Repetition]]\n\n...",
  "key_shifts": [
    {
      "date": "2024-02-15T10:30:00Z",
      "type": "contradiction",
      "description": "Initially thought fixed intervals optimal, discovered adaptive algorithms superior",
      "significance": "high"
    }
    // ... more shifts
  ],
  "narrative_metadata": {
    "word_count": 847,
    "phase_count": 4,
    "shift_count": 3,
    "influence_count": 2
  }
}
```

## Integration Notes

**Template Integration**: Use with `temporal-narrative-tmpl.yaml` for consistent formatting
**Visualization**: Include ASCII/Mermaid timeline from `generate-timeline-visualization.md`

## Error Handling

**No understanding shifts detected**: Still generate narrative, note incremental development
**Missing phase data**: Generate narrative for available phases only, flag gaps

## Testing

**Test Case 1**: Note with 3 major shifts, verify each explained in narrative
**Test Case 2**: Note with minimal activity, verify narrative handles gracefully
**Test Case 3**: Narrative readability (target: 800-1200 words, Flesch reading ease > 50)
