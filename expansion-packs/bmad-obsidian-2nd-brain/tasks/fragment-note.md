<!-- Powered by BMAD™ Core -->

# fragment-note

Fragment a non-atomic note into N atomic pieces using intelligent boundary detection and claim clustering.

## Purpose

Split complex notes containing multiple independent claims into atomic fragments. Each fragment becomes a self-contained atomic note that passes atomicity validation (score >= 0.7). Preserves source attribution and creates bidirectional links between all fragments.

## Prerequisites

- Note has been analyzed with analyze-atomicity.md (score < 0.7)
- Access to atomic-note-tmpl.yaml for creating fragments
- Access to create-atomic-note.md task for Obsidian integration
- Access to building-block-types.md for type classification
- Obsidian MCP Tools configured

## Inputs

- **note_path** (string, required): Path to non-atomic note to fragment
- **note_content** (string, required): Full markdown content
- **note_title** (string, required): Original note title
- **atomicity_score** (float, required): Score from analyze-atomicity
- **violations** (array, required): List of atomicity violations
- **yolo_mode** (boolean, optional): Auto-confirm all fragmentations (default: false)

## Outputs

```yaml
fragmentation_result:
  fragments_created: int # Number of atomic fragments created
  fragment_paths: [] # Array of paths to new atomic notes
  links_added: int # Number of bidirectional links created
  original_status: 'fragmented|archived' # Status of original note
  original_path: string # Path to updated original note
  success: boolean
  errors: [] # List of any errors encountered
```

## Fragmentation Strategy (5 Phases)

### Phase 1: Boundary Detection

**Purpose:** Identify natural and semantic boundaries where note could be split

**Algorithm:**

1. **Identify natural boundaries:**

   ```
   Natural boundaries (structural):
   - Markdown headers (##, ###, ####)
   - Paragraph breaks (double newline \n\n)
   - Horizontal rules (---)
   - Bullet list transitions
   - Code block boundaries
   - Blockquote boundaries
   ```

2. **Identify semantic boundaries:**

   ```
   Semantic boundaries (content):
   - New claim introductions
   - Topic changes (shift in subject matter)
   - Shift in building block type (concept → argument)
   - Transitional phrases: "Another point", "Separately", "Additionally"
   - Change in perspective or voice
   ```

3. **Score each boundary for "splitability" (0.0-1.0):**

   ```python
   def score_boundary(boundary):
       splitability = 0.5  # Start neutral

       # Increase for strong structural signals
       if boundary.type == 'header':
           splitability += 0.3
       elif boundary.type == 'horizontal_rule':
           splitability += 0.4
       elif boundary.type == 'paragraph_break':
           splitability += 0.1

       # Increase for semantic signals
       if boundary.introduces_new_claim:
           splitability += 0.3
       if boundary.topic_shift_detected:
           splitability += 0.2
       if boundary.has_transitional_phrase:
           splitability += 0.2

       # Decrease for coupling signals
       if boundary.references_previous_content:
           splitability -= 0.3
       if boundary.within_list_item:
           splitability -= 0.2
       if boundary.mid_sentence:
           splitability -= 0.5

       # Clamp to valid range
       return max(0.0, min(1.0, splitability))
   ```

4. **Rank boundaries by splitability score (highest first)**

**Output:** List of ranked boundaries with scores

### Phase 2: Claim Clustering

**Purpose:** Group related content together so each cluster becomes an atomic fragment

**Algorithm:**

1. **Extract all distinct claims/concepts:**

   ```python
   def extract_claims(note_content):
       claims = []

       # Parse note line by line
       for paragraph in split_by_paragraphs(note_content):
           # Identify declarative statements
           if is_declarative(paragraph):
               # Check if it's a thesis-level claim
               if is_thesis_level(paragraph):
                   claims.append({
                       'text': paragraph,
                       'position': get_position(paragraph),
                       'type': identify_claim_type(paragraph)
                   })

       return claims
   ```

2. **Cluster related content:**

   ```python
   def cluster_claims(claims, note_content):
       clusters = []

       for claim in claims:
           cluster = {
               'core_claim': claim,
               'supporting_content': [],
               'evidence': [],
               'examples': [],
               'cluster_id': generate_id()
           }

           # Find content that supports this claim
           # (appears after claim, before next claim)
           next_claim_pos = get_next_claim_position(claim, claims)
           content_block = extract_content_between(
               claim.position,
               next_claim_pos
           )

           # Classify supporting content
           for element in content_block:
               if is_evidence(element):
                   cluster['evidence'].append(element)
               elif is_example(element):
                   cluster['examples'].append(element)
               else:
                   cluster['supporting_content'].append(element)

           clusters.append(cluster)

       return clusters
   ```

3. **Validate cluster independence:**

   ```python
   def validate_cluster_independence(cluster):
       # Each cluster should be atomic if extracted
       # Check for cross-dependencies

       dependencies = []

       for other_cluster in all_clusters:
           if cluster.id == other_cluster.id:
               continue

           # Check if cluster references other cluster
           if references(cluster, other_cluster):
               dependencies.append(other_cluster.id)

       # Independent if minimal dependencies
       return len(dependencies) <= 1  # Allow one reference
   ```

4. **Adjust clusters if needed:**
   - Merge clusters with heavy cross-dependencies
   - Split clusters that are still non-atomic

**Output:** List of independent content clusters

### Phase 3: Split Point Selection

**Purpose:** Choose specific boundaries where note will be split

**Algorithm:**

1. **Propose split points between clusters:**

   ```python
   def propose_split_points(clusters, boundaries):
       split_points = []

       for i in range(len(clusters) - 1):
           cluster_end = clusters[i].end_position
           next_cluster_start = clusters[i+1].start_position

           # Find highest-scoring boundary between clusters
           best_boundary = None
           best_score = 0.0

           for boundary in boundaries:
               if cluster_end <= boundary.position < next_cluster_start:
                   if boundary.splitability > best_score:
                       best_boundary = boundary
                       best_score = boundary.splitability

           if best_boundary and best_score >= 0.5:
               split_points.append(best_boundary)

       return split_points
   ```

2. **Validate proposed fragments:**

   ```python
   def validate_fragments(split_points, content):
       # Split content at proposed split points
       fragments = split_at_points(content, split_points)

       all_atomic = True

       for fragment in fragments:
           # Run atomicity analysis on each proposed fragment
           analysis = run_analyze_atomicity(fragment)

           if analysis.score < 0.7:
               all_atomic = False
               # Adjust split points
               adjust_boundaries(fragment, split_points)

       return all_atomic
   ```

3. **Iterate until all fragments are atomic:**

   ```python
   max_iterations = 5
   iteration = 0

   while not all_fragments_atomic and iteration < max_iterations:
       # Adjust split points
       # Re-validate fragments
       # Check atomicity scores
       iteration += 1

   if iteration >= max_iterations:
       # Warn user: May need manual intervention
       log_warning("Could not achieve atomicity after 5 iterations")
   ```

4. **Determine fragment count N:**

   ```python
   N = len(split_points) + 1  # Split points divide into N+1 fragments

   # Validate fragment count is reasonable
   if N > 20:
       # Too many fragments - abort and recommend manual review
       return error("Fragment count exceeds limit (20)")
   elif N > 10:
       # Warn user: May need different organization
       warn("Large fragment count (>10) - consider alternative organization")
   elif N < 2:
       # Cannot fragment into 1 piece
       return error("Note cannot be fragmented (no valid split points)")
   ```

**Output:** Validated split points and fragment count N

### Phase 4: Fragment Creation

**Purpose:** Create N atomic notes from the clusters

**Algorithm:**

1. **For each fragment (1..N):**

   ```python
   for i, cluster in enumerate(clusters):
       fragment = create_fragment(cluster, i, N)
   ```

2. **Extract cluster content:**

   ```python
   def create_fragment(cluster, index, total):
       # Extract content for this fragment
       content = assemble_content(
           cluster.core_claim,
           cluster.supporting_content,
           cluster.evidence,
           cluster.examples
       )

       # Generate descriptive title
       title = generate_title(cluster)

       # Identify building block type
       bb_type = identify_building_block_type(cluster)

       # Run atomicity check
       atomicity = run_analyze_atomicity(content, title)

       if atomicity.score < 0.7:
           # Fragment failed atomicity - adjust content
           content = refine_content_for_atomicity(content, atomicity)

       return {
           'title': title,
           'content': content,
           'type': bb_type,
           'atomic_score': atomicity.score,
           'fragment_index': index + 1,
           'fragment_total': total
       }
   ```

3. **Generate descriptive titles:**

   ```python
   def generate_title(cluster):
       # Extract key concepts from core claim
       key_concepts = extract_key_concepts(cluster.core_claim)

       # Use building block type pattern
       if cluster.type == 'concept':
           # Pattern: "Concept - Specific Aspect"
           title = f"{key_concepts[0]} - {key_concepts[1]}"
       elif cluster.type == 'argument':
           # Pattern: "Claim Statement"
           title = cluster.core_claim[:60]  # First 60 chars
       elif cluster.type == 'model':
           # Pattern: "Model Name for Purpose"
           title = f"{key_concepts[0]} Model for {key_concepts[1]}"
       # ... other patterns

       # Ensure uniqueness
       title = ensure_unique_title(title)

       return title
   ```

4. **Preserve source attribution:**

   ```python
   def add_source_attribution(fragment, original_note):
       fragment.metadata = {
           'fragmented_from': original_note.path,
           'fragment_number': f"{fragment.index} of {fragment.total}",
           'original_title': original_note.title,
           'original_tags': original_note.tags,
           'original_created': original_note.created,
           'fragmentation_date': now()
       }

       return fragment
   ```

5. **Create new notes using atomic-note-tmpl.yaml:**

   ```python
   def create_atomic_note_file(fragment):
       # Prepare template variables
       variables = {
           'title': fragment.title,
           'type': fragment.type,
           'building_block': fragment.type,
           'source_note': fragment.metadata.fragmented_from,
           'created': now(),
           'tags': fragment.metadata.original_tags,
           'atomic_score': fragment.atomic_score,
           'content': fragment.content,
           'fragmented_from': fragment.metadata.fragmented_from,
           'fragment_number': fragment.metadata.fragment_number,
           'created_date': format_date(now()),
           'sanitized_title': sanitize_filename(fragment.title)
       }

       # Use create-atomic-note.md task
       result = create_atomic_note(variables)

       return result.note_path
   ```

**Output:** N atomic note files created in appropriate directories

### Phase 5: Cross-Linking and Original Update

**Purpose:** Create bidirectional links between fragments and mark original

**Algorithm:**

1. **Create cross-links between all fragments:**

   ```python
   def create_cross_links(fragments):
       links_added = 0

       for fragment in fragments:
           # Add "Related Fragments" section
           related_section = "\n## Related Fragments\n\n"
           related_section += f"This note was fragmented from [[{original.title}]]\n\n"

           # Link to all other fragments
           for other in fragments:
               if other.path != fragment.path:
                   # Determine relationship
                   relationship = determine_relationship(fragment, other)

                   # Add semantic link
                   related_section += f"- [[{other.title}]] - {relationship}\n"
                   links_added += 1

           # Append to fragment content
           update_note_content(fragment.path, related_section)

       return links_added
   ```

2. **Determine semantic relationships:**

   ```python
   def determine_relationship(fragment_a, fragment_b):
       # Analyze how fragments relate

       if fragment_a.type == 'concept' and fragment_b.type == 'argument':
           return "argues using this concept"
       elif fragment_a.type == 'argument' and fragment_b.type == 'evidence':
           return "supports this argument"
       elif fragment_a.type == 'model' and fragment_b.type == 'concept':
           return "component of this model"
       else:
           return "related note"  # Generic relationship
   ```

3. **Mark original note as fragmented:**

   ```python
   def mark_original_as_fragmented(original, fragments):
       # Update frontmatter
       original.frontmatter.status = 'fragmented'
       original.frontmatter.fragmented_date = now()

       # Add fragmentation notice
       notice = "\n---\n\n# FRAGMENTED\n\n"
       notice += "This note has been fragmented into atomic notes:\n\n"

       for fragment in fragments:
           notice += f"- [[{fragment.title}]]\n"

       notice += f"\nFragmented on: {now()}\n"
       notice += f"Original content preserved below for reference.\n\n---\n\n"

       # Prepend notice to content
       original.content = notice + original.content

       # Save updated original
       update_note(original.path, original.content)
   ```

4. **Archive original (optional):**

   ```python
   def archive_original(original, config):
       if config.archive_fragmented_notes:
           # Move to archive directory
           archive_path = '/archive/fragmented/'
           new_path = move_note(original.path, archive_path)

           return {
               'original_status': 'archived',
               'original_path': new_path
           }
       else:
           return {
               'original_status': 'fragmented',
               'original_path': original.path
           }
   ```

**Output:** Links created, original note updated/archived

## Security Hardening

**Input Validation:**

```python
# Sanitize all paths
def validate_note_path(path):
    # Block directory traversal
    if '../' in path or '/..' in path:
        raise SecurityError("Directory traversal attempt blocked")

    # Ensure path is within vault
    if not path.startswith(vault_root):
        raise SecurityError("Path outside vault blocked")

    # Validate path format
    if not is_valid_markdown_path(path):
        raise ValidationError("Invalid note path format")

    return sanitize_path(path)
```

**Fragment Limits:**

```python
# Enforce fragment count limits
MAX_FRAGMENTS = 20

if fragment_count > MAX_FRAGMENTS:
    raise ValidationError(
        f"Fragment count ({fragment_count}) exceeds limit ({MAX_FRAGMENTS})"
    )

if fragment_count > 10:
    warn(f"Large fragment count ({fragment_count}) - recommend manual review")
```

**Content Validation:**

```python
# Validate markdown content
def validate_content(content):
    # Check for dangerous patterns
    dangerous_patterns = [
        r'<script.*?>',
        r'javascript:',
        r'onerror=',
        r'onclick=',
        r'eval\('
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            raise SecurityError(f"Dangerous content pattern detected: {pattern}")

    # Validate markdown syntax
    if not is_valid_markdown(content):
        raise ValidationError("Invalid markdown syntax")

    return True
```

**Filename Sanitization:**

```python
def sanitize_filename(title):
    # Remove dangerous characters
    dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

    sanitized = title
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')

    # Convert spaces to hyphens
    sanitized = sanitized.replace(' ', '-')

    # Lowercase
    sanitized = sanitized.lower()

    # Limit length
    if len(sanitized) > 100:
        sanitized = sanitized[:100]

    # Remove double hyphens
    while '--' in sanitized:
        sanitized = sanitized.replace('--', '-')

    # Ensure uniqueness
    sanitized = ensure_unique_filename(sanitized)

    return sanitized
```

## Output Directory Structure

Fragments are placed in appropriate directories by building block type:

```
/atomic/
  concepts/        # Concept fragments
  arguments/       # Argument fragments
  models/          # Model fragments
  questions/       # Question fragments
  claims/          # Claim fragments
  phenomena/       # Phenomenon fragments

/archive/
  fragmented/      # Original fragmented notes (optional)
```

## User Confirmation (if not yolo_mode)

Before executing fragmentation, present plan to user:

```
Fragmentation Plan for: "Complex Note About Productivity"
==========================================================

Detected: 3 independent claims requiring fragmentation

Proposed Fragments:
1. "Zettelkasten Principle - Atomicity" (concept)
   - Atomicity score: 0.91
   - Directory: /atomic/concepts/

2. "GTD Inbox Zero Principle" (concept)
   - Atomicity score: 0.88
   - Directory: /atomic/concepts/

3. "PARA Method for Information Organization" (model)
   - Atomicity score: 0.93
   - Directory: /atomic/models/

Cross-links: 6 bidirectional links will be created
Original note: Will be marked as fragmented (not deleted)

Proceed with fragmentation? [Y/n]
```

## Error Handling

```python
try:
    result = fragment_note(note_path, note_content, config)
except SecurityError as e:
    return error(f"Security violation: {e}")
except ValidationError as e:
    return error(f"Validation failed: {e}")
except MCPError as e:
    return error(f"Obsidian MCP error: {e}")
except Exception as e:
    log_error(e)
    return error(f"Fragmentation failed: {e}")
```

## Success Criteria

Fragmentation is successful if:

1. All fragments created successfully
2. All fragments pass atomicity validation (score >= 0.7)
3. All cross-links created
4. Original note updated
5. No errors encountered

## Usage Notes

- Run via agent command: `*fragment-note {note_path}`
- Requires prior `*analyze-atomicity` run (score < 0.7)
- Use `*yolo` mode to skip confirmations
- Fragments automatically validated before creation
- Original note preserved for audit trail
