# <!-- Powered by BMAD™ Core -->

# rate-connection-strength

Calculate link strength score using semantic similarity, contextual relevance, and temporal proximity.

## Purpose

Compute a composite link strength score (0.0-1.0) by combining three components: semantic similarity (50% weight), contextual relevance (30% weight), and temporal proximity (20% weight). Returns the strength score and classification (strong/medium/weak).

## Prerequisites

- Semantic similarity score from Smart Connections
- Access to both note metadata (tags, creation dates, MOC membership)
- Access to relationship-confidence-checklist.md for validation

## Inputs

- **semantic_similarity** (float, required): Score from Smart Connections (0.0-1.0)
- **source_note_metadata** (object, required): {tags: [], created: iso_datetime, moc: string}
- **target_note_metadata** (object, required): {tags: [], created: iso_datetime, moc: string}
- **shared_concepts** (array, optional): List of shared concepts from identify-concept-overlap
- **common_sources** (bool, optional): Whether notes cite common sources

## Outputs

```yaml
connection_strength:
  strength: 0.0-1.0  # Final composite score
  classification: 'strong|medium|weak'
  components:
    semantic_similarity: 0.0-1.0
    contextual_relevance: 0.0-1.0
    temporal_proximity: 0.0-0.2
  explanation: 'Why this strength was calculated'
```

## Procedure

### Step 1: Validate Inputs

```javascript
if (semantic_similarity < 0.0 || semantic_similarity > 1.0) {
  return error: "Invalid semantic_similarity: must be 0.0-1.0"
}

if (!source_note_metadata.created || !target_note_metadata.created) {
  temporal_proximity = 0.0  // Default if dates unavailable
}
```

### Step 2: Calculate Contextual Relevance

**Component 1: Tag Overlap**
```javascript
shared_tags = intersection(source_note_metadata.tags, target_note_metadata.tags)
all_unique_tags = unique(source_note_metadata.tags + target_note_metadata.tags)

if (all_unique_tags.length > 0) {
  tag_overlap_score = shared_tags.length / all_unique_tags.length
} else {
  tag_overlap_score = 0.0
}
```

**Component 2: MOC Membership**
```javascript
if (source_note_metadata.moc && target_note_metadata.moc) {
  same_moc_bonus = (source_note_metadata.moc == target_note_metadata.moc) ? 0.3 : 0.0
} else {
  same_moc_bonus = 0.0
}
```

**Component 3: Common Sources**
```javascript
common_sources_bonus = common_sources ? 0.2 : 0.0
```

**Final Contextual Relevance:**
```javascript
// Weighted average with bonuses
contextual_relevance = (tag_overlap_score * 0.5) + (same_moc_bonus * 0.3) + (common_sources_bonus * 0.2)
contextual_relevance = max(0.0, min(1.0, contextual_relevance))
```

### Step 3: Calculate Temporal Proximity

```javascript
source_date = parse_iso_datetime(source_note_metadata.created)
target_date = parse_iso_datetime(target_note_metadata.created)

delta_days = abs((source_date - target_date).days)

if (delta_days <= 7) {
  // Same week
  temporal_proximity = 0.2
} else if (delta_days <= 30) {
  // Same month
  temporal_proximity = 0.1
} else if (delta_days <= 90) {
  // Same quarter
  temporal_proximity = 0.05
} else {
  // Distant
  temporal_proximity = 0.0
}
```

### Step 4: Calculate Final Strength

**Formula:**
```javascript
strength = (0.5 * semantic_similarity) +
           (0.3 * contextual_relevance) +
           (0.2 * temporal_proximity)

// Clamp to valid range
strength = max(0.0, min(1.0, strength))

// Round to 2 decimal places
strength = round(strength, 2)
```

### Step 5: Classify Strength

```javascript
if (strength >= 0.7) {
  classification = 'strong'
} else if (strength >= 0.5) {
  classification = 'medium'
} else {
  classification = 'weak'
}
```

### Step 6: Generate Explanation

```javascript
explanation = `This link has ${classification} strength (${strength}) because:
- Semantic similarity: ${semantic_similarity} (weighted 0.5 × ${semantic_similarity} = ${0.5 * semantic_similarity})
- Contextual relevance: ${contextual_relevance} (weighted 0.3 × ${contextual_relevance} = ${0.3 * contextual_relevance})
  - Tag overlap: ${tag_overlap_score} (${shared_tags.length} shared tags / ${all_unique_tags.length} total)
  - Same MOC: ${same_moc_bonus > 0 ? 'Yes (+0.3)' : 'No'}
  - Common sources: ${common_sources_bonus > 0 ? 'Yes (+0.2)' : 'No'}
- Temporal proximity: ${temporal_proximity} (notes created ${delta_days} days apart)
- Formula: (0.5 × ${semantic_similarity}) + (0.3 × ${contextual_relevance}) + (0.2 × ${temporal_proximity}) = ${strength}`
```

### Step 7: Return Results

```yaml
{
  strength: strength,
  classification: classification,
  components: {
    semantic_similarity: semantic_similarity,
    contextual_relevance: contextual_relevance,
    temporal_proximity: temporal_proximity
  },
  explanation: explanation
}
```

## Example: Strong Link

**Input:**
```yaml
semantic_similarity: 0.76
source_note_metadata:
  tags: ['memory', 'learning', 'retention', 'cognition']
  created: '2025-11-05T10:00:00Z'
  moc: 'Knowledge Management'
target_note_metadata:
  tags: ['memory', 'learning', 'spaced-repetition', 'cognition']
  created: '2025-11-06T14:00:00Z'
  moc: 'Knowledge Management'
shared_concepts: ['memory', 'learning', 'cognition']
common_sources: true
```

**Output:**
```yaml
strength: 0.82
classification: strong
components:
  semantic_similarity: 0.76
  contextual_relevance: 0.85
  temporal_proximity: 0.20
explanation: "Strong strength (0.82): similarity 0.76, contextual 0.85 (4 shared tags, same MOC, common sources), temporal 0.20 (1 day apart)"
```

## Example: Weak Link

**Input:**
```yaml
semantic_similarity: 0.52
source_note_metadata:
  tags: ['zettelkasten']
  created: '2025-09-15T10:00:00Z'
  moc: 'Note-Taking'
target_note_metadata:
  tags: ['productivity']
  created: '2025-11-05T14:00:00Z'
  moc: 'Time Management'
common_sources: false
```

**Output:**
```yaml
strength: 0.26
classification: weak
components:
  semantic_similarity: 0.52
  contextual_relevance: 0.0
  temporal_proximity: 0.0
explanation: "Weak strength (0.26): similarity 0.52, no shared tags, different MOCs, 51 days apart"
```

## Integration Points

**Called by:** *suggest-links, *create-links, *accept-suggestion
**Calls:** relationship-confidence-checklist.md (validation)
**Outputs to:** linking-quality-checklist.md (strength test validation)
