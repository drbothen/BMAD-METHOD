# <!-- Powered by BMAD™ Core -->

# create-bidirectional-link

Create bidirectional wikilinks with context in both source and target notes via Obsidian MCP.

## Purpose

Insert wikilinks in both source and target notes to establish a true bidirectional connection. Each link includes a context sentence explaining the relationship. Implements rollback if one direction fails to maintain consistency.

## Prerequisites

- Obsidian MCP configured for note read/write
- Access to both notes (read and write permissions)
- Link type and context sentences generated
- Access to linking-quality-checklist.md for validation

## Inputs

- **source_note_path** (string, required): Path to source note
- **target_note_path** (string, required): Path to target note
- **link_type** (string, required): One of 7 relationship types
- **context_forward** (string, required): Context for source → target
- **context_backward** (string, required): Context for target → source
- **dry_run** (bool, optional): Preview changes without writing (default: false)

## Outputs

```yaml
bidirectional_link_result:
  success: true|false
  source_updated: true|false
  target_updated: true|false
  rollback_performed: false
  source_link_added: '- [[Target Note]] - context'
  target_link_added: '- [[Source Note]] - context'
  error: null
```

## Procedure

### Step 1: Validate Inputs

```javascript
// Check required fields
if (!source_note_path || !target_note_path) {
  return error: "Both source_note_path and target_note_path required"
}

if (!context_forward || !context_backward) {
  return error: "Both context sentences required"
}

// Validate link type
valid_types = ['supports', 'contradicts', 'elaborates', 'analogous_to', 'generalizes', 'specializes', 'influences']
if (!valid_types.includes(link_type)) {
  return error: `Invalid link_type: ${link_type}. Must be one of ${valid_types.join(', ')}`
}

// Prevent link-to-self
if (source_note_path == target_note_path) {
  return error: "Cannot link note to itself"
}
```

### Step 2: Load Note Contents

```javascript
try {
  source_note = obsidian_mcp.read_note(source_note_path)
  target_note = obsidian_mcp.read_note(target_note_path)
} catch (error) {
  if (error.code == 'NOT_FOUND') {
    return error: `Note not found: ${error.path}`
  } else if (error.code == 'PERMISSION_DENIED') {
    return error: `Cannot read note (permission denied): ${error.path}`
  } else {
    return error: `Failed to read notes: ${error.message}`
  }
}

// Store original content for rollback
original_source_content = source_note.content
original_target_content = target_note.content
```

### Step 3: Check for Duplicate Links

```javascript
// Extract existing wikilinks from source
existing_source_links = extract_wikilinks(source_note.content)

// Check if target already linked
target_note_title = extract_title_from_path(target_note_path)
if (existing_source_links.includes(`[[${target_note_title}]]`)) {
  return {
    success: false,
    error: `Link already exists: source already links to ${target_note_title}`,
    action: 'Skipped duplicate link creation'
  }
}
```

### Step 4: Generate Wikilink Format

```javascript
// Format: - [[Note Title]] - context sentence

source_to_target_link = `- [[${target_note.title}]] - ${context_forward}`
target_to_source_link = `- [[${source_note.title}]] - ${context_backward}`
```

**Example:**
```markdown
## Related Concepts

- [[Evergreen Notes]] - Atomic notes are the foundation of evergreen notes which can stand alone and be continuously refined
- [[Bidirectional Links]] - Atomicity enables meaningful bidirectional linking between concepts
```

### Step 5: Find Insertion Point

```javascript
function find_insertion_point(note_content) {
  // Priority 1: Insert in "Related Concepts" section if exists
  if (note_content.includes('## Related Concepts')) {
    section_start = note_content.indexOf('## Related Concepts')
    section_end = note_content.indexOf('\n## ', section_start + 1)
    if (section_end == -1) section_end = note_content.length
    insertion_point = section_end
    return {location: 'related_concepts_section', index: insertion_point}
  }

  // Priority 2: Insert before "Source Attribution" section if exists
  if (note_content.includes('## Source Attribution')) {
    insertion_point = note_content.indexOf('## Source Attribution')
    // Create Related Concepts section
    new_section = '\n## Related Concepts\n\n'
    return {location: 'before_source_attribution', index: insertion_point, prefix: new_section}
  }

  // Priority 3: Append to end of note
  return {location: 'end_of_note', index: note_content.length, prefix: '\n\n## Related Concepts\n\n'}
}
```

### Step 6: Insert Links (with Dry Run Support)

```javascript
// Find insertion points
source_insertion = find_insertion_point(source_note.content)
target_insertion = find_insertion_point(target_note.content)

// Build updated content
if (source_insertion.prefix) {
  updated_source = source_note.content.slice(0, source_insertion.index) +
                  source_insertion.prefix +
                  source_to_target_link + '\n' +
                  source_note.content.slice(source_insertion.index)
} else {
  updated_source = source_note.content.slice(0, source_insertion.index) +
                  source_to_target_link + '\n' +
                  source_note.content.slice(source_insertion.index)
}

// Same for target
updated_target = ... // Similar logic

// If dry run, return preview without writing
if (dry_run) {
  return {
    success: true,
    dry_run: true,
    source_preview: updated_source,
    target_preview: updated_target,
    message: "Dry run: no changes written"
  }
}
```

### Step 7: Write Updated Content (with Rollback)

```javascript
source_updated = false
target_updated = false

try {
  // Step 7a: Update source note
  obsidian_mcp.update_note(source_note_path, updated_source)
  source_updated = true

  // Step 7b: Update target note
  obsidian_mcp.update_note(target_note_path, updated_target)
  target_updated = true

  return {
    success: true,
    source_updated: true,
    target_updated: true,
    rollback_performed: false,
    source_link_added: source_to_target_link,
    target_link_added: target_to_source_link,
    error: null
  }

} catch (error) {
  // Rollback if second write failed
  if (source_updated && !target_updated) {
    try {
      obsidian_mcp.update_note(source_note_path, original_source_content)
      return {
        success: false,
        source_updated: false,
        target_updated: false,
        rollback_performed: true,
        error: `Target update failed, source rolled back: ${error.message}`,
        original_error: error.message
      }
    } catch (rollback_error) {
      return {
        success: false,
        source_updated: true,
        target_updated: false,
        rollback_performed: false,
        error: `CRITICAL: Target update failed AND rollback failed. Source note modified but target not updated. Manual intervention required.`,
        rollback_error: rollback_error.message
      }
    }
  } else {
    return {
      success: false,
      source_updated: false,
      target_updated: false,
      error: `Failed to update notes: ${error.message}`
    }
  }
}
```

### Step 8: Verify Link Creation

```javascript
// Re-read both notes to confirm links present
try {
  source_verify = obsidian_mcp.read_note(source_note_path)
  target_verify = obsidian_mcp.read_note(target_note_path)

  source_has_link = source_verify.content.includes(`[[${target_note.title}]]`)
  target_has_link = target_verify.content.includes(`[[${source_note.title}]]`)

  if (!source_has_link || !target_has_link) {
    return {
      success: false,
      error: "Verification failed: links not found in updated notes",
      source_has_link: source_has_link,
      target_has_link: target_has_link
    }
  }
} catch (error) {
  // Non-critical: verification failed but links likely created
  log_warning(`Link verification failed: ${error.message}`)
}
```

## Examples

### Example 1: Successful Bidirectional Link

**Input:**
```yaml
source_note_path: 'atomic/argument-01-spaced-repetition.md'
target_note_path: 'atomic/phenomenon-01-forgetting-curve.md'
link_type: 'supports'
context_forward: 'The forgetting curve provides empirical evidence for why distributed practice outperforms cramming'
context_backward: 'This phenomenon supports the argument for spaced repetition by demonstrating natural memory decay'
dry_run: false
```

**Output:**
```yaml
success: true
source_updated: true
target_updated: true
rollback_performed: false
source_link_added: '- [[Ebbinghaus Forgetting Curve]] - The forgetting curve provides empirical evidence for why distributed practice outperforms cramming'
target_link_added: '- [[Spaced Repetition Superior to Massed Practice]] - This phenomenon supports the argument for spaced repetition by demonstrating natural memory decay'
error: null
```

### Example 2: Rollback After Target Failure

**Input:** (same as above, but target note locked/read-only)

**Output:**
```yaml
success: false
source_updated: false
target_updated: false
rollback_performed: true
error: 'Target update failed (read-only), source rolled back successfully'
original_error: 'Permission denied: note is read-only'
```

### Example 3: Duplicate Link Detected

**Input:** (link already exists)

**Output:**
```yaml
success: false
error: 'Link already exists: source already links to Forgetting Curve'
action: 'Skipped duplicate link creation'
```

## Error Handling

- **Note not found:** Clear error, verify paths
- **Permission denied:** Skip with warning, log for user review
- **MCP timeout:** Retry with exponential backoff (max 3 attempts)
- **Rollback failure:** CRITICAL alert, require manual intervention

## Integration Points

**Called by:** *create-links, *create-link, *accept-suggestion
**Calls:** Obsidian MCP read_note(), update_note()
**Depends on:** linking-quality-checklist.md (validation before calling)
