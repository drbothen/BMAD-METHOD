<!-- Powered by BMAD™ Core -->

# Security Guidelines for Semantic Linker Agent

Comprehensive security hardening and validation guidelines for the bmad-obsidian-2nd-brain expansion pack.

## Overview

The Semantic Linker Agent handles user notes, executes database queries, and modifies files. Security is paramount to prevent:

- **Directory traversal attacks** (accessing files outside vault)
- **Cypher injection** (malicious Neo4j queries)
- **Link spam** (overwhelming notes with excessive links)
- **Circular reasoning** (creating invalid logical chains)
- **Data exfiltration** (exposing private notes)
- **Denial of service** (resource exhaustion)

## Security Architecture

### 1. Input Validation

All user inputs must be validated before processing:

**Note Paths:**

```javascript
function validate_note_path(path) {
  // Block directory traversal
  if (path.includes('../') || path.includes('..\\')) {
    throw SecurityError('Directory traversal detected in path')
  }

  // Block absolute paths outside vault
  if (path.startsWith('/') && !path.startsWith(vault_root)) {
    throw SecurityError('Absolute path outside vault not allowed')
  }

  // Block file:// protocol
  if (path.startsWith('file://') || path.startsWith('file:\\\\')) {
    throw SecurityError('File protocol not allowed')
  }

  // Verify path is within allowed directories
  allowed_dirs = ['/inbox/', '/atomic/', '/mocs/', '/literature/']
  if (!any(path.startsWith(dir) for dir in allowed_dirs)) {
    throw SecurityError('Path outside allowed directories')
  }

  // Verify .md extension
  if (!path.endsWith('.md')) {
    throw SecurityError('Only markdown files (.md) allowed')
  }

  return path
}
```

**Semantic Similarity Threshold:**

```javascript
function validate_threshold(threshold) {
  if (typeof threshold !== 'number') {
    throw ValidationError('Threshold must be a number');
  }

  if (threshold < 0.0 || threshold > 1.0) {
    throw ValidationError('Threshold must be in range [0.0, 1.0]');
  }

  return threshold;
}
```

**Link Type:**

```javascript
function validate_link_type(link_type) {
  valid_types = [
    'supports',
    'contradicts',
    'elaborates',
    'analogous_to',
    'generalizes',
    'specializes',
    'influences',
  ];

  if (!valid_types.includes(link_type)) {
    throw ValidationError(
      `Invalid link_type: ${link_type}. Must be one of: ${valid_types.join(', ')}`,
    );
  }

  return link_type;
}
```

**Context Sentences:**

```javascript
function validate_context(context) {
  // Maximum length (prevent resource exhaustion)
  const MAX_LENGTH = 500;

  if (context.length > MAX_LENGTH) {
    throw ValidationError(`Context exceeds max length of ${MAX_LENGTH} characters`);
  }

  // Strip dangerous content
  const dangerous_patterns = [
    /<script/i,
    /javascript:/i,
    /on\w+\s*=/i, // onclick=, onload=, etc.
    /eval\(/i,
    /Function\(/i,
  ];

  for (const pattern of dangerous_patterns) {
    if (pattern.test(context)) {
      throw SecurityError('Dangerous content detected in context');
    }
  }

  return context;
}
```

**Result Limits:**

```javascript
function validate_limit(limit) {
  const MAX_LIMIT = 100; // Prevent DoS via excessive results

  if (typeof limit !== 'number' || limit < 1 || limit > MAX_LIMIT) {
    throw ValidationError(`Limit must be integer in range [1, ${MAX_LIMIT}]`);
  }

  return limit;
}
```

### 2. Cypher Injection Prevention

**ALWAYS use parameterized queries. NEVER concatenate user input into Cypher strings.**

**SAFE (Parameterized Query):**

```cypher
MATCH (source:Note {path: $source_path})
MATCH (target:Note {path: $target_path})
CREATE (source)-[r:CONCEPTUALLY_RELATED {
  link_id: $link_id,
  link_type: $link_type,
  strength: $strength,
  discovered_at: datetime($discovered_at),
  context: $context,
  valid_time_start: datetime($valid_time_start),
  transaction_time: datetime()
}]->(target)
RETURN r
```

**Parameters object (properly escaped):**

```javascript
params = {
  source_path: validate_note_path(source_path), // Validated
  target_path: validate_note_path(target_path), // Validated
  link_id: generate_uuid(), // System-generated
  link_type: validate_link_type(link_type), // Validated enum
  strength: parseFloat(strength), // Type-safe
  discovered_at: new Date().toISOString(), // System-generated
  context: validate_context(context), // Sanitized
  valid_time_start: new Date().toISOString(), // System-generated
};

result = graphiti_mcp.execute_cypher(cypher_query, params);
```

**UNSAFE (String Concatenation - NEVER DO THIS):**

```cypher
// ❌ VULNERABLE TO INJECTION
CREATE (a)-[r:CONCEPTUALLY_RELATED {
  context: '" + user_input + "'
}]->(b)

// Attacker input: "}]->(x), (attacker)-[:OWNS]->(x) WHERE 1=1 //"
// Results in data exfiltration or unauthorized relationships
```

**Cypher Injection Attack Examples:**

1. **Data Exfiltration:**

   ```
   User input: "}]->(n) WITH n MATCH (secret:Note) RETURN secret //"
   → Exposes all notes in database
   ```

2. **Unauthorized Relationships:**

   ```
   User input: "}]->(n), (attacker:Note {path: 'evil.md'})-[:CONTROLS]->(n) //"
   → Creates unauthorized control relationships
   ```

3. **Deletion Attack:**
   ```
   User input: "}]->(n) DELETE n //"
   → Deletes nodes
   ```

**Defense: Parameterized queries eliminate all injection vectors.**

### 3. Path Sanitization

**Filename Sanitization:**

```javascript
function sanitize_filename(title) {
  // Remove special characters that are unsafe in filenames
  const unsafe_chars = /[\/\\:\*\?"<>\|]/g;
  let safe_title = title.replace(unsafe_chars, '-');

  // Limit length
  const MAX_FILENAME_LENGTH = 100;
  if (safe_title.length > MAX_FILENAME_LENGTH) {
    safe_title = safe_title.substring(0, MAX_FILENAME_LENGTH);
  }

  // Convert spaces to hyphens
  safe_title = safe_title.replace(/\s+/g, '-');

  // Remove leading/trailing hyphens
  safe_title = safe_title.replace(/^-+|-+$/g, '');

  // Ensure uniqueness (collision detection)
  if (file_exists(`${safe_title}.md`)) {
    let counter = 1;
    while (file_exists(`${safe_title}-${counter}.md`)) {
      counter++;
    }
    safe_title = `${safe_title}-${counter}`;
  }

  return safe_title;
}
```

**Wikilink Sanitization:**

```javascript
function sanitize_wikilink(link_text) {
  // Ensure wikilink syntax is valid
  // Format: [[Note Title]]

  if (!link_text.startsWith('[[') || !link_text.endsWith(']]')) {
    throw ValidationError('Invalid wikilink format');
  }

  // Extract title
  let title = link_text.slice(2, -2);

  // Check for nested brackets (invalid)
  if (title.includes('[[') || title.includes(']]')) {
    throw ValidationError('Nested brackets not allowed in wikilinks');
  }

  // Check for pipe character (alias)
  if (title.includes('|')) {
    const [target, alias] = title.split('|');
    title = target.trim();
  }

  return `[[${title}]]`;
}
```

### 4. Circular Reasoning Detection

**Algorithm:**

```javascript
function detect_circular_reasoning(source_path, target_path, link_type) {
  // Only check for reasoning-based link types
  reasoning_types = ['supports', 'contradicts', 'generalizes', 'specializes'];

  if (!reasoning_types.includes(link_type)) {
    return false; // Elaborates, analogous_to, influences can be cyclic
  }

  // Build graph of reasoning links
  reasoning_graph = build_reasoning_graph();

  // Check if adding this link creates a cycle
  if (would_create_cycle(reasoning_graph, source_path, target_path, link_type)) {
    return true; // Circular reasoning detected
  }

  return false;
}

function build_reasoning_graph() {
  // Load all existing links of reasoning types
  graph = new DirectedGraph();

  all_notes = list_all_notes();
  for (note_path in all_notes) {
    note_content = read_note(note_path);
    links = extract_typed_links(note_content);

    for (link in links) {
      if (reasoning_types.includes(link.type)) {
        graph.add_edge(note_path, link.target, link.type);
      }
    }
  }

  return graph;
}

function would_create_cycle(graph, source, target, link_type) {
  // Use depth-first search to detect cycle
  visited = new Set();
  stack = [target];

  while (stack.length > 0) {
    current = stack.pop();

    if (current === source) {
      return true; // Cycle detected: target → ... → source
    }

    if (visited.has(current)) {
      continue;
    }

    visited.add(current);

    // Add outgoing edges from current node
    outgoing = graph.get_edges_from(current);
    for (edge in outgoing) {
      if (reasoning_types.includes(edge.type)) {
        stack.push(edge.target);
      }
    }
  }

  return false; // No cycle
}
```

**Example Detection:**

```
Existing: A supports B, B supports C
Proposed: C supports A
→ Would create cycle: A → B → C → A
→ REJECT

Existing: A elaborates B, B elaborates C
Proposed: C elaborates A
→ Elaboration can be cyclic (different relationship type)
→ ALLOW (with warning)
```

### 5. Link Spam Prevention

**Rate Limiting:**

```javascript
function enforce_link_limits(note_path) {
  const MAX_LINKS_PER_NOTE = 50;
  const MAX_SUGGESTIONS_PER_QUERY = 50;
  const MAX_BULK_TARGETS = 20;

  // Check existing link count
  note_content = read_note(note_path);
  existing_links = extract_wikilinks(note_content);

  if (existing_links.length >= MAX_LINKS_PER_NOTE) {
    throw SecurityError(`Note has reached max link limit (${MAX_LINKS_PER_NOTE})`);
  }

  // Check for suspicious patterns
  if (existing_links.length > 30) {
    log_warning(`Note approaching link limit: ${note_path} (${existing_links.length} links)`);
  }

  return true;
}
```

**Duplicate Link Prevention:**

```javascript
function check_duplicate_link(source_path, target_path) {
  source_content = read_note(source_path);
  existing_links = extract_wikilinks(source_content);

  target_title = extract_title_from_path(target_path);

  for (link in existing_links) {
    if (link.includes(target_title)) {
      return true; // Duplicate detected
    }
  }

  return false;
}
```

### 6. Permission Verification

**File Permission Checks:**

```javascript
function verify_write_permissions(note_path) {
  try {
    // Attempt to read file metadata
    stats = file_stats(note_path);

    // Check if writable
    if (!stats.writable) {
      throw PermissionError(`Note is read-only: ${note_path}`);
    }

    // Check if locked by another process
    if (stats.locked) {
      throw PermissionError(`Note is locked: ${note_path}`);
    }

    return true;
  } catch (error) {
    throw PermissionError(`Cannot access note: ${note_path} - ${error.message}`);
  }
}
```

### 7. Data Privacy

**Local-Only Storage:**

- All feedback data stored in `.bmad-obsidian-2nd-brain/link-feedback.json` (local)
- No external API calls for feedback collection
- User has full control: can inspect, modify, or delete feedback file

**Smart Connections Privacy:**

- Uses local BGE-micro-v2 embeddings (no cloud API)
- Embeddings stored in Obsidian vault (user-controlled)
- Fully offline-capable

**Neo4j Security:**

- Optional integration (graceful degradation if disabled)
- Connection credentials in user-controlled `config.yaml`
- No credential exposure in logs or error messages
- Parameterized queries only

**User Data Control:**

```javascript
// User can reset feedback learning
rm .bmad-obsidian-2nd-brain/link-feedback.json

// User can inspect feedback data
cat .bmad-obsidian-2nd-brain/link-feedback.json | jq

// User can view Neo4j data
MATCH (n:Note)-[r:CONCEPTUALLY_RELATED]->(m:Note)
WHERE n.path = 'atomic/my-note.md'
RETURN n, r, m
```

### 8. Error Handling

**Never expose sensitive information in error messages:**

**BAD:**

```javascript
throw Error(`Failed to connect to Neo4j at bolt://localhost:7687 with password: ${password}`);
// Exposes credentials ❌
```

**GOOD:**

```javascript
throw Error('Failed to connect to Neo4j. Check config.yaml for connection settings.');
// No sensitive data ✓
```

**Graceful Degradation:**

```javascript
try {
  neo4j_result = create_neo4j_relationship(...)
} catch (error) {
  log_warning('Neo4j unavailable, continuing in Obsidian-only mode')
  // Don't fail hard - allow workflow to continue
  return {
    success: true,
    neo4j_enabled: true,
    skipped: true,
    error: 'Neo4j connection failed, temporal graph not updated'
  }
}
```

### 9. Content Validation

**Markdown Syntax Validation:**

```javascript
function validate_markdown(content) {
  try {
    // Parse markdown
    parsed = markdown_parser.parse(content);

    // Check for script tags (XSS prevention)
    if (/<script|javascript:|on\w+=/i.test(content)) {
      throw SecurityError('Potentially dangerous content detected');
    }

    return true;
  } catch (error) {
    throw ValidationError(`Invalid markdown: ${error.message}`);
  }
}
```

**Frontmatter YAML Validation:**

```javascript
function validate_frontmatter(content) {
  // Extract frontmatter between --- delimiters
  frontmatter_match = content.match(/^---\n([\s\S]*?)\n---/);

  if (!frontmatter_match) {
    return true; // No frontmatter is valid
  }

  frontmatter_yaml = frontmatter_match[1];

  try {
    // Parse YAML
    parsed = yaml.parse(frontmatter_yaml);

    // Validate required fields
    if (!parsed.building_block) {
      log_warning('Missing building_block in frontmatter');
    }

    return true;
  } catch (error) {
    throw ValidationError(`Invalid frontmatter YAML: ${error.message}`);
  }
}
```

### 10. Rollback Safety

**Atomic Bidirectional Link Creation:**

```javascript
function create_bidirectional_link_safe(
  source_path,
  target_path,
  context_forward,
  context_backward,
) {
  // Store original content for rollback
  original_source = read_note(source_path);
  original_target = read_note(target_path);

  source_updated = false;
  target_updated = false;

  try {
    // Step 1: Update source note
    update_note(source_path, add_link(original_source, target_path, context_forward));
    source_updated = true;

    // Step 2: Update target note
    update_note(target_path, add_link(original_target, source_path, context_backward));
    target_updated = true;

    return { success: true, rollback_performed: false };
  } catch (error) {
    // Rollback if second update failed
    if (source_updated && !target_updated) {
      try {
        update_note(source_path, original_source);
        return {
          success: false,
          rollback_performed: true,
          error: `Target update failed, source rolled back: ${error.message}`,
        };
      } catch (rollback_error) {
        // CRITICAL: Rollback failed
        return {
          success: false,
          rollback_performed: false,
          error:
            'CRITICAL: Target update failed AND rollback failed. Manual intervention required.',
          rollback_error: rollback_error.message,
        };
      }
    }

    return { success: false, error: error.message };
  }
}
```

## Security Checklist

Before deploying or executing semantic linking operations:

- [ ] **Input Validation:** All user inputs validated (paths, thresholds, link types, contexts)
- [ ] **Path Sanitization:** No directory traversal, no absolute paths outside vault
- [ ] **Cypher Injection:** Only parameterized queries used, no string concatenation
- [ ] **Circular Reasoning:** Detection algorithm implemented for reasoning link types
- [ ] **Link Spam:** Max link limits enforced (50 per note, 50 per query, 20 bulk targets)
- [ ] **Duplicate Prevention:** Check existing links before creation
- [ ] **Link-to-Self:** Prevent note from linking to itself
- [ ] **Permission Checks:** Verify file permissions before write operations
- [ ] **Privacy:** All data stored locally, no external API calls for sensitive data
- [ ] **Error Handling:** No sensitive info exposed in error messages
- [ ] **Content Validation:** Markdown and YAML syntax validated
- [ ] **Rollback Safety:** Atomic operations with rollback on failure
- [ ] **Neo4j Security:** Credentials not exposed, parameterized queries only
- [ ] **Rate Limiting:** Max 50 suggestions per query, max 20 bulk targets
- [ ] **Graceful Degradation:** Handle MCP/Neo4j unavailability without hard failure

## Attack Scenarios & Defenses

### Scenario 1: Directory Traversal Attack

**Attack:** User provides path `../../etc/passwd` to exfiltrate system files
**Defense:** Path validation blocks `../` patterns and absolute paths outside vault

### Scenario 2: Cypher Injection

**Attack:** User input in context: `"}]->(n) MATCH (secret:Note) RETURN secret //"`
**Defense:** Parameterized queries prevent injection, user input never concatenated

### Scenario 3: Link Spam

**Attack:** Automated script creates 1000 links to single note
**Defense:** Max 50 links per note enforced, rate limiting blocks excessive operations

### Scenario 4: Circular Reasoning

**Attack:** Create A supports B, B supports C, C supports A (circular argument)
**Defense:** Cycle detection algorithm rejects links that create reasoning cycles

### Scenario 5: Malicious Script Injection

**Attack:** Context sentence contains `<script>alert('XSS')</script>`
**Defense:** Content validation strips script tags and dangerous patterns

### Scenario 6: Credential Exposure

**Attack:** Error message reveals Neo4j password
**Defense:** Error messages sanitized, no credentials in logs

### Scenario 7: Rollback Failure

**Attack:** Second link creation fails, leaving first link orphaned
**Defense:** Atomic rollback restores original state if second operation fails

## References

- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **Cypher Injection Prevention:** https://neo4j.com/docs/cypher-manual/current/syntax/parameters/
- **Path Traversal:** https://owasp.org/www-community/attacks/Path_Traversal
- **Input Validation:** https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
