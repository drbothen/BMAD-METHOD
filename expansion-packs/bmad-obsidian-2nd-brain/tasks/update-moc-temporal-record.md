<!-- Powered by BMAD™ Core -->

# Update MOC Temporal Record

## Purpose

Record MOC creation or update events in Neo4j Graphiti database, calculate maturity level, and track maintenance history for temporal analysis of knowledge organization evolution.

## Inputs

- **moc_path** (String, required): Path to MOC file in vault
- **event_type** (String, required): "MOC_CREATED" or "MOC_UPDATED"
- **moc_metadata** (Object, required): Contains domain, note_count, branch_count, maturity_level
- **change_description** (String, required for updates): Description of what changed

## Outputs

- **temporal_event_id** (String): UUID of created Neo4j event node
- **maturity_assessment** (Object): Current maturity level with progression suggestions
- **maintenance_schedule** (Object): Recommended next review date based on maturity

## Procedure

### Step 1: Check Neo4j Availability

Determine if temporal tracking is possible:

```
try:
  graphiti.health_check()
  neo4j_available = true
catch:
  neo4j_available = false
  mode = "OBSIDIAN_ONLY"
  log("Neo4j unavailable - skipping temporal record, updating frontmatter only")
```

If Neo4j unavailable:
- Skip Steps 3-5 (Neo4j operations)
- Proceed directly to Step 6 (update MOC frontmatter)
- Notify user: "⚠️ Temporal tracking disabled - MOC history will be stored in frontmatter only"

### Step 2: Calculate Maturity Level

Determine MOC maturity based on quantitative metrics:

**Maturity Calculation Algorithm:**

```
maturity_score = 0

# Note count scoring (0-40 points)
if note_count >= 60:
  maturity_score += 40
elif note_count >= 31:
  maturity_score += 30
elif note_count >= 11:
  maturity_score += 20
else:
  maturity_score += 10

# Branch structure scoring (0-20 points)
if branch_count >= 4 and has_sub_branches:
  maturity_score += 20
elif branch_count >= 3:
  maturity_score += 15
elif branch_count >= 2:
  maturity_score += 10
else:
  maturity_score += 5

# Synthesis quality scoring (0-20 points)
if all_branches_have_summaries and bridge_paragraphs_present:
  maturity_score += 20
elif all_branches_have_summaries:
  maturity_score += 15
elif some_summaries_present:
  maturity_score += 10
else:
  maturity_score += 5

# Link density scoring (0-20 points)
bidirectional_link_ratio = bidirectional_links / total_links
if bidirectional_link_ratio >= 0.9:
  maturity_score += 20
elif bidirectional_link_ratio >= 0.7:
  maturity_score += 15
elif bidirectional_link_ratio >= 0.5:
  maturity_score += 10
else:
  maturity_score += 5

# Assign maturity level based on score
if maturity_score >= 80:
  maturity_level = "comprehensive"
elif maturity_score >= 60:
  maturity_level = "established"
elif maturity_score >= 40:
  maturity_level = "developing"
else:
  maturity_level = "nascent"
```

**Maturity Levels:**

1. **Nascent (0-39 points)**:
   - < 10 notes, 1-2 branches, minimal synthesis
   - Review frequency: Weekly
   - Next milestone: Reach 11 notes, add 3rd branch

2. **Developing (40-59 points)**:
   - 11-30 notes, 2-3 branches, some summaries
   - Review frequency: Bi-weekly
   - Next milestone: Complete all summaries, add bridge paragraphs

3. **Established (60-79 points)**:
   - 31-60 notes, 3+ branches, full synthesis
   - Review frequency: Monthly
   - Next milestone: Reach 60 notes or split into sub-MOCs

4. **Comprehensive (80-100 points)**:
   - 60+ notes, 4+ branches with hierarchy, rich synthesis
   - Review frequency: Quarterly
   - Next milestone: Maintain currency, consider domain splitting

### Step 3: Create MOC Node in Neo4j (if available)

Create or update MOC entity in Graphiti:

**For MOC_CREATED events:**

```cypher
MERGE (moc:MOC {path: $moc_path})
SET moc.domain = $domain,
    moc.created = timestamp(),
    moc.maturity_level = $maturity_level,
    moc.note_count = $note_count,
    moc.branch_count = $branch_count,
    moc.last_updated = timestamp(),
    moc.review_frequency = $review_frequency
RETURN moc
```

**For MOC_UPDATED events:**

```cypher
MATCH (moc:MOC {path: $moc_path})
SET moc.last_updated = timestamp(),
    moc.maturity_level = $maturity_level,
    moc.note_count = $note_count,
    moc.branch_count = $branch_count,
    moc.update_count = COALESCE(moc.update_count, 0) + 1
RETURN moc
```

Use Graphiti MCP:
```
graphiti.add_entity({
  name: moc_path,
  entity_type: "MOC",
  observations: [
    `MOC for ${domain} domain created with ${note_count} notes`,
    `Organized into ${branch_count} knowledge branches`,
    `Maturity level: ${maturity_level}`
  ]
})
```

### Step 4: Create Temporal Event in Neo4j (if available)

Record the MOC creation/update event:

**Event node structure:**

```cypher
CREATE (event:TemporalEvent:MOCEvent {
  id: $event_id,
  type: $event_type,  // "MOC_CREATED" or "MOC_UPDATED"
  timestamp: timestamp(),
  domain: $domain,
  note_count: $note_count,
  maturity_level: $maturity_level,
  change_description: $change_description
})

// Link event to MOC
MATCH (moc:MOC {path: $moc_path})
CREATE (moc)-[:RECORDED_AT]->(event)

RETURN event
```

Use Graphiti MCP:
```
event_id = graphiti.add_episode({
  name: `${event_type}: ${moc_path}`,
  episode_type: "moc_lifecycle",
  content: change_description,
  source_description: "MOC Constructor Agent",
  reference_time: new Date().toISOString()
})
```

### Step 5: Link MOC to Constituent Notes (if available)

Create relationships between MOC and organized notes:

```cypher
MATCH (moc:MOC {path: $moc_path})

// Link to all constituent notes
UNWIND $constituent_note_paths as note_path
MATCH (note:Note {path: note_path})
MERGE (moc)-[r:ORGANIZES]->(note)
SET r.branch = note.assigned_branch,
    r.added_at = timestamp()

RETURN count(r) as links_created
```

Use Graphiti MCP:
```
for each note in constituent_notes:
  graphiti.add_relationship({
    source_entity: moc_path,
    target_entity: note.path,
    relationship_type: "ORGANIZES",
    properties: {
      branch: note.assigned_branch,
      added_at: new Date().toISOString()
    }
  })
```

### Step 6: Update MOC Frontmatter

Update MOC file's frontmatter with temporal metadata:

**For MOC_CREATED:**

```yaml
---
type: moc
domain: machine-learning
maturity: nascent
created: 2024-11-11
updated: 2024-11-11
note_count: 12
branch_count: 3
review_frequency: weekly
next_review: 2024-11-18
temporal_tracking: enabled  # or "disabled" if Neo4j unavailable

# Temporal history
history:
  - date: 2024-11-11
    event: MOC_CREATED
    note_count: 12
    maturity: nascent
    description: "Initial MOC created with 3 knowledge branches"
---
```

**For MOC_UPDATED:**

```yaml
---
# ... existing frontmatter ...
updated: 2024-11-11
note_count: 18  # updated count
maturity: developing  # updated maturity
next_review: 2024-11-25

# Append to history
history:
  - date: 2024-11-11
    event: MOC_CREATED
    note_count: 12
    maturity: nascent
    description: "Initial MOC created with 3 knowledge branches"
  - date: 2024-11-11
    event: MOC_UPDATED
    note_count: 18
    maturity: developing  # progressed!
    description: "Added 6 new notes, upgraded to developing maturity"
---
```

Use Obsidian MCP:
```
obsidian.updateProperties(moc_path, {
  updated: new Date().toISOString().split('T')[0],
  note_count: note_count,
  maturity: maturity_level,
  next_review: calculate_next_review_date(maturity_level)
})

// Append history entry
obsidian.appendToProperty(moc_path, 'history', {
  date: new Date().toISOString().split('T')[0],
  event: event_type,
  note_count: note_count,
  maturity: maturity_level,
  description: change_description
})
```

### Step 7: Calculate Next Review Date

Determine maintenance schedule based on maturity:

**Review Frequency by Maturity:**

```
if maturity_level == "nascent":
  review_interval = 7 days   # Weekly
elif maturity_level == "developing":
  review_interval = 14 days  # Bi-weekly
elif maturity_level == "established":
  review_interval = 30 days  # Monthly
else:  # comprehensive
  review_interval = 90 days  # Quarterly

next_review_date = today + review_interval
```

**Adjustment factors:**

- If note count growing rapidly (>5 new notes since last review): Shorten interval by 50%
- If no updates in 2x review interval: Flag for deep review
- If maturity progressed this update: Reset to new maturity's interval

### Step 8: Generate Maturity Assessment Report

Create detailed maturity assessment for user:

```markdown
## MOC Maturity Assessment

**Domain**: machine-learning
**Current Maturity**: Developing (score: 52/100)
**Progression**: Nascent → **Developing** (upgraded!)

### Scoring Breakdown

**Note Count**: 18 notes (20/40 points)
- Target for next level: 31 notes (established)
- Gap: Need 13 more notes

**Branch Structure**: 3 branches, no sub-branches (15/20 points)
- Target: Add sub-branches to largest branch OR add 4th main branch

**Synthesis Quality**: All summaries present, no bridges yet (15/20 points)
- Target: Add 3-4 bridge paragraphs between related branches

**Link Density**: 68% bidirectional (15/20 points)
- Target: Ensure 90%+ bidirectional links (current: 23/34 bidirectional)
- Missing backlinks: 11 notes need "Part of: [[MOC]]" reference

### Next Milestones

**To reach Established (60 points):**
1. Add 13 more notes to domain (priority)
2. Write 3 bridge paragraphs explaining branch relationships
3. Add bidirectional links to 11 notes missing MOC backlinks

**Estimated timeline**: 3-4 weeks at current capture rate

### Maintenance Schedule

**Next Review**: 2024-11-25 (14 days)
**Review Frequency**: Bi-weekly (developing maturity)
**Recommended Actions**:
- Check for new domain notes to incorporate
- Update summaries if branch focus shifted
- Monitor for need to add 4th branch (if any branch > 15 notes)
```

### Step 9: Track Maturity Progression

If maturity level changed from previous state:

**Detect progression:**

```
previous_maturity = read from MOC frontmatter history
current_maturity = calculated in Step 2

if current_maturity > previous_maturity:
  progression_type = "MATURITY_ADVANCED"
  message = "🎉 MOC matured from {previous} to {current}!"
elif current_maturity < previous_maturity:
  progression_type = "MATURITY_REGRESSED"  # rare, but possible
  message = "⚠️ MOC maturity decreased. Review quality or re-evaluate."
else:
  progression_type = "MATURITY_MAINTAINED"
  message = "MOC remains at {current} maturity."
```

**Record progression event** (if Neo4j available):

```cypher
CREATE (event:MaturityProgressionEvent {
  id: randomUUID(),
  timestamp: timestamp(),
  moc_path: $moc_path,
  from_maturity: $previous_maturity,
  to_maturity: $current_maturity,
  progression_type: $progression_type,
  triggering_change: $change_description
})

MATCH (moc:MOC {path: $moc_path})
CREATE (moc)-[:PROGRESSED_AT]->(event)

RETURN event
```

### Step 10: Generate Maintenance Recommendations

Based on maturity and domain activity, suggest next actions:

**For Nascent MOCs:**
- "Keep capturing! Add 5-10 more notes to reach developing maturity."
- "Identify 1-2 additional knowledge branches as domain expands."
- "Focus on breadth over depth at this stage."

**For Developing MOCs:**
- "Complete synthesis: Write bridge paragraphs connecting branches."
- "Ensure all notes have bidirectional links back to MOC."
- "Consider splitting large branches (>15 notes) into sub-branches."

**For Established MOCs:**
- "Maintain currency: Review quarterly for outdated content."
- "Identify knowledge gaps: What's missing from domain coverage?"
- "Consider creating sub-MOCs if approaching 60+ notes."

**For Comprehensive MOCs:**
- "Consider splitting into focused sub-MOCs if > 80 notes."
- "Establish rigorous review schedule (quarterly minimum)."
- "Document this MOC's relationship to other domain MOCs."

### Step 11: Elicit User Confirmation

Present temporal record summary:

```
MOC Temporal Record Updated

Event: MOC_UPDATED
Domain: machine-learning
Maturity: Developing (52/100)
Progression: Nascent → Developing ✓

Temporal Tracking: Enabled
- Neo4j event recorded: moc_event_uuid_123
- MOC node updated with current state
- 18 constituent notes linked

Next Review: 2024-11-25 (14 days)

[Display maturity assessment]

Maintenance recommendations:
1. Add 13 more notes (target: established maturity)
2. Write 3 bridge paragraphs
3. Add backlinks to 11 notes

Proceed? (y/n):
```

Wait for confirmation before finalizing.

## Integration Notes

**Graphiti MCP Integration:**
- Use `graphiti.add_entity()` for MOC node
- Use `graphiti.add_episode()` for temporal events
- Use `graphiti.add_relationship()` for MOC-note links

**Obsidian MCP Integration:**
- Use `obsidian.updateProperties()` for frontmatter updates
- Use `obsidian.appendToProperty()` for history array

**Graceful Degradation:**
- If Neo4j unavailable, store all temporal data in frontmatter
- Frontmatter becomes single source of truth
- Notify user of limited temporal query capabilities

## Error Handling

**Neo4j connection fails:**
- Log: "Neo4j unavailable, falling back to Obsidian frontmatter only"
- Continue with frontmatter updates
- Set `temporal_tracking: disabled` in frontmatter

**MOC file not found:**
- Error: "MOC file {moc_path} not found. Ensure MOC was created before updating temporal record."
- Abort operation

**Maturity calculation fails:**
- Warning: "Could not calculate maturity. Using previous level or defaulting to nascent."
- Set maturity = previous_maturity OR "nascent" if no previous

**Frontmatter update fails:**
- Critical error: "Failed to update MOC frontmatter. Temporal record may be incomplete."
- Retry once, then abort if fails again

## Testing

**Test Case 1: MOC_CREATED Event**
- Expected: Neo4j node created, event recorded, frontmatter initialized
- Validate: Event ID returned, maturity calculated, next review date set

**Test Case 2: MOC_UPDATED Event with Maturity Progression**
- Expected: Maturity advanced from nascent → developing, progression event recorded
- Validate: History array has 2 entries, maturity_score increased

**Test Case 3: Neo4j Unavailable**
- Expected: Graceful degradation to frontmatter-only
- Validate: Frontmatter updated correctly, user notified

**Test Case 4: Comprehensive Maturity Reached**
- Expected: Review frequency changed to quarterly, recommendations suggest sub-MOC splitting
- Validate: next_review = today + 90 days

**Test Case 5: Maturity Regression (rare)**
- Expected: Warning issued, regression event recorded
- Validate: User prompted to review quality or re-evaluate structure
