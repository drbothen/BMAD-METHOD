# <!-- Powered by BMAD™ Core -->

# learn-from-feedback

Learn from user feedback on link suggestions to improve future recommendations.

## Purpose

Track user acceptance/rejection of link suggestions and adjust the semantic similarity threshold and link type preferences based on patterns. Stores feedback locally and applies learning to filter future suggestions.

## Prerequisites

- Local storage at `.bmad-obsidian-2nd-brain/link-feedback.json`
- Write permission to create/update feedback file
- Privacy-preserving (all data stored locally in vault)

## Inputs

- **suggestion_id** (string, required): Unique ID of the suggestion
- **decision** (string, required): 'approved' | 'rejected' | 'deferred'
- **rejection_reason** (string, optional): Reason if rejected
- **link_type** (string, required): Type of suggested link
- **link_strength** (float, required): Calculated strength of link
- **semantic_similarity** (float, required): Smart Connections similarity score

## Outputs

```yaml
learning_result:
  feedback_recorded: true
  total_feedback_count: 125
  acceptance_rate: 0.78
  adjustments_applied:
    threshold_adjustment: +0.05 # Raised or lowered
    type_preferences: { 'supports': 0.92, 'elaborates': 0.74, ... }
  recommendations:
    - 'Acceptance rate high (78%), consider lowering threshold to 0.55'
```

## Feedback Storage Format

```json
{
  "version": "1.0",
  "created": "2025-11-05T10:00:00Z",
  "last_updated": "2025-11-05T14:30:00Z",
  "threshold_history": [
    {"date": "2025-11-05", "value": 0.6, "reason": "initial"},
    {"date": "2025-11-06", "value": 0.65, "reason": "acceptance_low"}
  ],
  "current_threshold": 0.65,
  "feedback_entries": [
    {
      "suggestion_id": "abc123",
      "timestamp": "2025-11-05T14:30:00Z",
      "decision": "approved",
      "link_type": "supports",
      "link_strength": 0.82,
      "semantic_similarity": 0.76,
      "rejection_reason": null
    },
    ...
  ],
  "type_statistics": {
    "supports": {"approved": 45, "rejected": 5, "acceptance_rate": 0.90},
    "elaborates": {"approved": 32, "rejected": 11, "acceptance_rate": 0.74},
    ...
  }
}
```

## Procedure

### Step 1: Load Existing Feedback

```javascript
feedback_file_path = '.bmad-obsidian-2nd-brain/link-feedback.json';

try {
  feedback_data = read_json(feedback_file_path);
} catch (error) {
  // File doesn't exist → initialize
  feedback_data = {
    version: '1.0',
    created: current_iso_timestamp(),
    last_updated: current_iso_timestamp(),
    threshold_history: [{ date: today(), value: 0.6, reason: 'initial' }],
    current_threshold: 0.6,
    feedback_entries: [],
    type_statistics: initialize_type_stats(),
  };
}
```

### Step 2: Record Feedback Entry

```javascript
new_entry = {
  suggestion_id: suggestion_id,
  timestamp: current_iso_timestamp(),
  decision: decision,
  link_type: link_type,
  link_strength: link_strength,
  semantic_similarity: semantic_similarity,
  rejection_reason: rejection_reason,
};

feedback_data.feedback_entries.push(new_entry);
feedback_data.last_updated = current_iso_timestamp();
```

### Step 3: Update Type Statistics

```javascript
// Update stats for this link type
if (!feedback_data.type_statistics[link_type]) {
  feedback_data.type_statistics[link_type] = {
    approved: 0,
    rejected: 0,
    deferred: 0,
    acceptance_rate: 0.0,
  };
}

stats = feedback_data.type_statistics[link_type];

if (decision == 'approved') {
  stats.approved += 1;
} else if (decision == 'rejected') {
  stats.rejected += 1;
} else if (decision == 'deferred') {
  stats.deferred += 1;
}

// Recalculate acceptance rate
total = stats.approved + stats.rejected; // Don't count deferred
if (total > 0) {
  stats.acceptance_rate = stats.approved / total;
}
```

### Step 4: Analyze Patterns

```javascript
// Overall acceptance rate
total_approved = sum(feedback_entries where decision == 'approved')
total_rejected = sum(feedback_entries where decision == 'rejected')
total_decided = total_approved + total_rejected

if (total_decided > 0) {
  overall_acceptance_rate = total_approved / total_decided
} else {
  overall_acceptance_rate = null  // Insufficient data
}

// Analyze rejection reasons
rejection_patterns = group_by(feedback_entries where decision == 'rejected', 'rejection_reason')
// Example: {
//   'irrelevant': 12,
//   'wrong_type': 8,
//   'too_weak': 15,
//   'technical_to_creative': 5  // Pattern: always rejects technical→creative links
// }
```

### Step 5: Adjust Similarity Threshold

```javascript
// Only adjust if sufficient data (>= 20 decisions)
if (total_decided >= 20) {
  current_threshold = feedback_data.current_threshold;

  if (overall_acceptance_rate < 0.6) {
    // Low acceptance → raise threshold (be more selective)
    new_threshold = min(1.0, current_threshold + 0.05);
    adjustment_reason = 'acceptance_low';
  } else if (overall_acceptance_rate > 0.9) {
    // High acceptance → lower threshold (more suggestions)
    new_threshold = max(0.5, current_threshold - 0.05);
    adjustment_reason = 'acceptance_high';
  } else {
    // Acceptance in good range (60%-90%) → no change
    new_threshold = current_threshold;
    adjustment_reason = 'no_change';
  }

  // Record threshold change
  if (new_threshold != current_threshold) {
    feedback_data.threshold_history.push({
      date: today(),
      value: new_threshold,
      reason: adjustment_reason,
      previous_value: current_threshold,
      acceptance_rate: overall_acceptance_rate,
    });
    feedback_data.current_threshold = new_threshold;
  }
}
```

### Step 6: Build Rejection Filters

```javascript
// Identify consistent rejection patterns
rejection_filters = []

// Pattern: specific link types consistently rejected
for (type, stats) in feedback_data.type_statistics:
  if (stats.acceptance_rate < 0.30 && (stats.approved + stats.rejected) >= 10):
    rejection_filters.push({
      type: 'link_type_low_acceptance',
      link_type: type,
      action: 'deprioritize',
      reason: `${type} has low acceptance rate (${stats.acceptance_rate})`
    })

// Pattern: weak links consistently rejected
weak_link_rejections = count(feedback_entries where decision == 'rejected' && link_strength < 0.5)
weak_link_total = count(feedback_entries where link_strength < 0.5)
if (weak_link_total >= 10 && weak_link_rejections / weak_link_total > 0.70):
  rejection_filters.push({
    type: 'weak_links_rejected',
    action: 'skip_weak_links',
    threshold: 0.5,
    reason: 'Weak links (<0.5) rejected 70%+ of the time'
  })
```

### Step 7: Save Updated Feedback

```javascript
try {
  write_json(feedback_file_path, feedback_data)
} catch (error) {
  return error: `Failed to save feedback: ${error.message}`
}
```

### Step 8: Return Learning Results

```yaml
{
  feedback_recorded: true,
  total_feedback_count: feedback_data.feedback_entries.length,
  acceptance_rate: overall_acceptance_rate,
  adjustments_applied:
    {
      threshold_adjustment: new_threshold - current_threshold,
      new_threshold: new_threshold,
      type_preferences: feedback_data.type_statistics,
    },
  rejection_filters: rejection_filters,
  recommendations: generate_recommendations(overall_acceptance_rate,
  type_statistics),
}
```

## Examples

### Example 1: First Feedback (Initialization)

**Input:**

```yaml
suggestion_id: 'abc123'
decision: 'approved'
link_type: 'supports'
link_strength: 0.82
semantic_similarity: 0.76
```

**Output:**

```yaml
feedback_recorded: true
total_feedback_count: 1
acceptance_rate: 1.0
adjustments_applied:
  threshold_adjustment: 0.0 # Insufficient data
  new_threshold: 0.6
recommendations:
  - 'Insufficient data (1 decision). Need 20+ decisions for threshold adjustment'
```

### Example 2: Low Acceptance → Raise Threshold

**Input:** (after 25 decisions, 12 approved, 13 rejected → 48% acceptance)

**Output:**

```yaml
feedback_recorded: true
total_feedback_count: 25
acceptance_rate: 0.48
adjustments_applied:
  threshold_adjustment: +0.05
  new_threshold: 0.65
  type_preferences:
    supports: 0.85
    elaborates: 0.42 # Low acceptance
    analogous_to: 0.60
recommendations:
  - 'Acceptance rate low (48%), raised threshold from 0.60 to 0.65'
  - 'Consider reviewing "elaborates" suggestions (42% acceptance)'
```

### Example 3: High Acceptance → Lower Threshold

**Input:** (after 50 decisions, 46 approved, 4 rejected → 92% acceptance)

**Output:**

```yaml
feedback_recorded: true
total_feedback_count: 50
acceptance_rate: 0.92
adjustments_applied:
  threshold_adjustment: -0.05
  new_threshold: 0.55
recommendations:
  - 'Acceptance rate high (92%), lowered threshold from 0.60 to 0.55 to provide more suggestions'
```

## Privacy & Reset

**Privacy:**

- All feedback stored locally in `.bmad-obsidian-2nd-brain/link-feedback.json`
- No data sent to external services
- User has full control and visibility

**Reset Learning:**

```bash
# Delete feedback file to reset
rm .bmad-obsidian-2nd-brain/link-feedback.json
```

**View Stats:**

```javascript
// User can view learning stats via command
*review-feedback-stats

// Output:
{
  total_decisions: 125,
  acceptance_rate: 0.78,
  current_threshold: 0.65,
  type_preferences: {supports: 0.92, elaborates: 0.74, ...},
  threshold_history: [...]
}
```

## Integration Points

**Called by:** *accept-suggestion, *reject-suggestion
**Outputs to:** \*suggest-links (applies learned threshold and filters)
