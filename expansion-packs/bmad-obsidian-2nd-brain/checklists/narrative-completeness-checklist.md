<!-- Powered by BMAD™ Core -->

# ------------------------------------------------------------

# Narrative Completeness Checklist

# ------------------------------------------------------------

---

checklist:
  id: narrative-completeness-checklist
  name: Narrative Completeness Checklist
  description: Quality gates for temporal narrative validation - ensures evolution narratives are comprehensive, insightful, and actionable
  items:
    - "[ ] Chronological accuracy maintained: Events presented in correct order with accurate dates"
    - "[ ] Key understanding shifts identified and explained: Major changes in thinking documented with context"
    - "[ ] Maturation metrics included: Days-to-evergreen, edit velocity, link accumulation, speed index present"
    - "[ ] Influences documented: Sources, experiences, and factors that shaped understanding listed"
    - "[ ] Visualizations present: ASCII timeline OR Mermaid diagram included"
    - "[ ] Current state assessment: Final phase and current status clearly described"
    - "[ ] Phase narratives complete: All phases (capture, development, maturation, maintenance) have narratives"
    - "[ ] Recommendations provided: Actionable next steps for concept maintenance"
    - "[ ] Vault comparison context: Metrics compared to vault averages with interpretation"
    - "[ ] Narrative readability: Clear prose, avoids jargon, tells coherent story"

---

## Purpose

This checklist ensures temporal evolution narratives are complete, insightful, and useful for understanding concept development patterns.

## When to Use

- After generating narrative via `*analyze-evolution` or `*create-timeline`
- Before publishing temporal analysis
- During narrative quality review
- When Timeline Constructor completes analysis
- Before adding narrative to vault

## Quality Criteria Details

### 1. Chronological Accuracy Maintained

**Check:** Events presented in correct temporal order with accurate dates

**Pass Criteria:** Timeline flows logically from capture to present

**Example PASS:**
> "Jan 15: Captured
> Jan 20: Promoted (5 days later)
> Jan 25: First links created"

**Example FAIL:**
> "Jan 25: First links created
> Jan 15: Note captured
> Jan 20: Promoted"

**Remediation:** Sort events chronologically before narrative generation

### 2. Key Understanding Shifts Identified and Explained

**Check:** Major changes in thinking documented with date, type, and context

**Required elements per shift:**
- Date of shift
- Type (contradiction, source integration, synthesis, perspective)
- Description of what changed
- Context explaining why shift matters

**Pass Criteria:** At least 1 shift identified (if concept > 3 months old)

**Example PASS:**
> "**Feb 15, 2024: Contradiction**
>
> Initially thought fixed intervals optimal. Reading Wozniak's SM-2 paper revealed adaptive algorithms superior.
>
> This shift represents fundamental change in understanding, challenging initial assumptions with new evidence."

**Remediation:** Review edit history for major changes, add shift analysis

### 3. Maturation Metrics Included

**Check:** All key metrics present with vault comparisons

**Required metrics:**
- Days to evergreen (if promoted)
- Edit velocity during development
- Link accumulation rate during maturation
- Reference velocity
- Maturation speed index

**Pass Criteria:** At least 3/5 metrics present

**Remediation:** Run `analyze-concept-maturation.md` to generate metrics

### 4. Influences Documented

**Check:** Sources and factors that shaped understanding identified

**Categories to check:**
- External sources (books, papers, articles)
- Personal experiences or experiments
- Related concepts
- Conversations or collaborations

**Pass Criteria:** At least 1 influence documented

**Remediation:** Review edit history for citations and source attributions

### 5. Visualizations Present

**Check:** Timeline visualization included (ASCII or Mermaid format)

**Pass Criteria:** At least one visualization format present

**Formats:**
- ASCII timeline (for terminal/plain text)
- Mermaid timeline diagram
- Mermaid Gantt chart
- Mermaid graph

**Remediation:** Run `generate-timeline-visualization.md` task

### 6. Current State Assessment

**Check:** Final section describes where concept stands today

**Required elements:**
- Current phase (maintenance, maturation, etc.)
- Current status (evergreen, active development, archived)
- Backlink count or reference metrics
- Last activity date

**Pass Criteria:** Current state clearly described

**Remediation:** Add "Current State" section with present-day assessment

### 7. Phase Narratives Complete

**Check:** All applicable phases have narrative sections

**Phases to check:**
- Capture phase (always present)
- Development phase (if promoted or active edits)
- Maturation phase (if 3+ months old)
- Maintenance phase (if 12+ months old)

**Pass Criteria:** All applicable phases documented

**Remediation:** Generate missing phase narratives from event data

### 8. Recommendations Provided

**Check:** Actionable next steps suggested

**Recommendation types:**
- Maintenance schedule (review frequency)
- Content actions (split, merge, update, archive)
- Integration actions (add to MOC, create links)
- Quality improvements (add examples, refine definitions)

**Pass Criteria:** At least 2 recommendations present

**Example:**
- Maintain with quarterly reviews
- Consider splitting if exceeds 500 lines
- Add to [[Learning Strategies MOC]] if not present

**Remediation:** Add conclusion section with 2-3 recommendations

### 9. Vault Comparison Context

**Check:** Metrics compared to vault averages with interpretation

**Required format:**
```
Metric: X value
- Vault Average: Y value
- Z% faster/slower/higher/lower
```

**Pass Criteria:** Comparisons include interpretation (not just numbers)

**Example PASS:**
> "Days to evergreen: 5 days (vault avg: 18 days) - 72% faster ✓
>
> Fast promotion indicates clear, immediately useful concept"

**Remediation:** Add vault context to metrics, explain what differences mean

### 10. Narrative Readability

**Check:** Clear prose that tells coherent story

**Readability criteria:**
- Avoids excessive jargon
- Uses active voice
- Explains technical terms
- Flows logically from section to section
- Target: Flesch reading ease > 50

**Pass Criteria:** Narrative is comprehensible without deep domain knowledge

**Remediation:** Simplify language, add context, improve transitions

## Scoring

**Total Items:** 10
**Pass Threshold:** >= 8/10 (80%)

## Narrative Length Guidelines

- **Short narrative** (3 months evolution): 800-1000 words
- **Medium narrative** (6-12 months): 1000-1500 words
- **Long narrative** (12+ months): 1500-2500 words

Narratives should be comprehensive but concise.

## Common Issues

1. **Missing context for shifts**: Shifts listed but not explained why they matter
2. **Metrics without interpretation**: Numbers presented but not analyzed
3. **No actionable recommendations**: Analysis ends without guidance
4. **Incomplete phase coverage**: Only covers capture/development, ignores maturation
5. **Poor readability**: Too technical, assumes expert knowledge

## Remediation Workflow

If checklist fails:

1. Identify missing/weak sections
2. Regenerate sections using appropriate tasks:
   - `create-chronological-narrative.md` for phase narratives
   - `analyze-concept-maturation.md` for metrics
   - `generate-timeline-visualization.md` for visuals
3. Add recommendations based on maturation analysis
4. Review readability, simplify if needed
5. Re-run checklist

## Integration

This checklist is automatically run by Timeline Constructor Agent's `*analyze-evolution` command before finalizing temporal narrative document.

## Quality Examples

**High-Quality Narrative Characteristics:**
- Tells a story (not just lists events)
- Explains "why" not just "what"
- Provides insights about learning patterns
- Includes specific dates and metrics
- Offers actionable recommendations
- Readable by non-experts

**Low-Quality Narrative Characteristics:**
- Event dump (no synthesis)
- Missing context for shifts
- No metrics or comparisons
- Generic recommendations
- Technical jargon without explanation
- Incomplete phase coverage
