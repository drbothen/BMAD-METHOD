<!-- Powered by BMAD™ Core -->

# create-atomic-note

Create an atomic note in Obsidian vault using MCP Tools integration.

## Purpose

Create a new atomic note file in the appropriate Obsidian vault directory using the atomic-note-tmpl.yaml template. Handles template variable substitution, filename generation, directory routing by building block type, collision detection, and error handling.

## Prerequisites

- Obsidian MCP Tools configured and connected
- Obsidian vault accessible
- Access to atomic-note-tmpl.yaml template
- Template variables prepared

## Inputs

- **title** (string, required): Descriptive title for the atomic note
- **type** (string, required): Building block type (concept|argument|model|question|claim|phenomenon)
- **building_block** (string, required): Same as type (for compatibility)
- **content** (string, required): Main note content (the single core idea)
- **atomic_score** (float, required): Atomicity score from 0.0-1.0
- **created** (string, required): Creation timestamp in ISO 8601 format
- **tags** (array, optional): Array of tags for categorization (default: [])
- **source_note** (string, optional): Link to original note if fragmented (default: null)
- **source_url** (string, optional): Original source URL if applicable
- **source_author** (string, optional): Original author if applicable
- **related_concepts** (array, optional): Array of related concept links (default: [])
- **fragmented_from** (string, optional): Original note path if this is a fragment
- **fragment_number** (string, optional): Fragment number if part of fragmentation (e.g., "1 of 3")

## Outputs

```yaml
creation_result:
  success: boolean
  note_path: string # Full path to created note
  note_title: string # Title of created note
  directory: string # Directory where note was created
  filename: string # Generated filename
  error: string|null # Error message if failed
  retry_count: int # Number of retries attempted
```

## Algorithm

### Step 1: Load Template

```python
def load_template():
    # Load atomic-note-tmpl.yaml
    template_path = f"{expansion_pack_root}/templates/atomic-note-tmpl.yaml"

    try:
        with open(template_path, 'r') as f:
            template = yaml.safe_load(f)
        return template
    except FileNotFoundError:
        raise TemplateError("atomic-note-tmpl.yaml not found")
    except yaml.YAMLError as e:
        raise TemplateError(f"Invalid template YAML: {e}")
```

### Step 2: Prepare Template Variables

```python
def prepare_variables(input_variables):
    # Start with input variables
    variables = input_variables.copy()

    # Construct related_concepts list if provided as array
    if 'related_concepts' in variables and isinstance(variables['related_concepts'], list):
        if variables['related_concepts']:
            # Convert array to newline-separated bullet list
            related_list = '\n'.join(f"- {concept}" for concept in variables['related_concepts'])
            variables['related_concepts'] = related_list
        else:
            variables['related_concepts'] = ''

    # Construct source_attribution_content from individual fields
    attribution_lines = []

    if variables.get('source_url'):
        attribution_lines.append(f"**Source:** {variables['source_url']}")

    if variables.get('source_author'):
        attribution_lines.append(f"**Author:** {variables['source_author']}")

    if variables.get('fragmented_from'):
        attribution_lines.append(f"**Fragmented from:** [[{variables['fragmented_from']}]]")

        if variables.get('fragment_number'):
            attribution_lines.append(f"**Fragment:** {variables['fragment_number']}")

    variables['source_attribution_content'] = '\n'.join(attribution_lines)

    return variables


def substitute_variables(template, variables):
    # Prepare composite variables
    variables = prepare_variables(variables)

    # Get template content structure
    rendered_content = ""

    # Render frontmatter section
    frontmatter = render_frontmatter(template.sections.frontmatter, variables)
    rendered_content += frontmatter + "\n\n"

    # Render main content section
    main_content = render_content(template.sections.content, variables)
    rendered_content += main_content + "\n\n"

    # Render related concepts (if provided)
    if variables.get('related_concepts'):
        related = render_related_concepts(
            template.sections.related_concepts,
            variables
        )
        rendered_content += related + "\n\n"

    # Render source attribution (if any attribution content)
    if variables.get('source_attribution_content'):
        attribution = render_attribution(
            template.sections.source_attribution,
            variables
        )
        rendered_content += attribution + "\n\n"

    # Render metadata (if fragmented)
    if variables.get('fragmented_from'):
        metadata = render_metadata(
            template.sections.metadata,
            variables
        )
        rendered_content += metadata + "\n\n"

    return rendered_content
```

**Variable Substitution:**

```python
def substitute_variable(template_string, variables):
    # Replace {{variable_name}} with actual values
    result = template_string

    for var_name, var_value in variables.items():
        placeholder = f"{{{{{var_name}}}}}"

        if placeholder in result:
            # Handle different value types
            if isinstance(var_value, list):
                # Arrays: join with commas
                value_str = ', '.join(str(v) for v in var_value)
            elif isinstance(var_value, bool):
                # Booleans: lowercase string
                value_str = str(var_value).lower()
            elif var_value is None:
                # Null: empty string or "null"
                value_str = 'null'
            else:
                # Everything else: string conversion
                value_str = str(var_value)

            result = result.replace(placeholder, value_str)

    return result
```

### Step 3: Generate Filename

```python
def generate_filename(title, created_date):
    # Format: YYYY-MM-DD-{sanitized-title}.md

    # Extract date portion
    date_str = format_date(created_date)  # YYYY-MM-DD

    # Sanitize title
    sanitized_title = sanitize_filename(title)

    # Construct filename
    filename = f"{date_str}-{sanitized_title}.md"

    return filename


def sanitize_filename(title):
    # Remove dangerous characters: / \ : * ? " < > |
    dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

    sanitized = title
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')

    # Convert spaces to hyphens
    sanitized = sanitized.replace(' ', '-')

    # Lowercase for consistency
    sanitized = sanitized.lower()

    # Remove multiple consecutive hyphens
    while '--' in sanitized:
        sanitized = sanitized.replace('--', '-')

    # Trim leading/trailing hyphens
    sanitized = sanitized.strip('-')

    # Limit length to 100 characters
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
        # Trim trailing hyphen if cut mid-word
        sanitized = sanitized.rstrip('-')

    # Ensure non-empty
    if not sanitized:
        sanitized = 'untitled'

    return sanitized


def format_date(iso_timestamp):
    # Convert ISO 8601 to YYYY-MM-DD
    # Example: "2025-11-05T14:30:00Z" → "2025-11-05"

    dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d')
```

### Step 4: Determine Target Directory

```python
def determine_directory(building_block_type):
    # Route to appropriate directory based on type

    directory_map = {
        'concept': '/atomic/concepts/',
        'argument': '/atomic/arguments/',
        'model': '/atomic/models/',
        'question': '/atomic/questions/',
        'claim': '/atomic/claims/',
        'phenomenon': '/atomic/phenomena/'
    }

    directory = directory_map.get(building_block_type)

    if not directory:
        # Default to concepts if unknown type
        log_warning(f"Unknown building block type: {building_block_type}")
        directory = '/atomic/concepts/'

    return directory
```

### Step 5: Handle File Collisions

```python
def handle_collision(base_filename, directory):
    # Check if file exists, append -2, -3, etc. until unique

    filename = base_filename
    counter = 2

    while file_exists(f"{directory}{filename}"):
        # Extract base name and extension
        name, ext = split_extension(base_filename)

        # Append counter
        filename = f"{name}-{counter}{ext}"
        counter += 1

        # Safety limit: max 100 attempts
        if counter > 100:
            raise CollisionError("Cannot generate unique filename after 100 attempts")

    return filename
```

### Step 6: Call Obsidian MCP Tools

```python
def create_note_via_mcp(directory, filename, content):
    # Use Obsidian MCP Tools: create_note()

    full_path = f"{directory}{filename}"

    try:
        result = obsidian_mcp.create_note(
            path=full_path,
            content=content
        )

        if result.success:
            return {
                'success': True,
                'note_path': full_path,
                'error': None
            }
        else:
            return {
                'success': False,
                'note_path': None,
                'error': result.error
            }

    except MCPConnectionError as e:
        return {
            'success': False,
            'note_path': None,
            'error': f"MCP connection failed: {e}"
        }
    except MCPTimeoutError as e:
        return {
            'success': False,
            'note_path': None,
            'error': f"MCP timeout: {e}"
        }
    except Exception as e:
        return {
            'success': False,
            'note_path': None,
            'error': f"Unexpected error: {e}"
        }
```

### Step 7: Retry Logic

```python
def create_note_with_retry(directory, filename, content, max_retries=3):
    retry_count = 0
    backoff_seconds = 1  # Exponential backoff: 1s, 2s, 4s

    while retry_count < max_retries:
        result = create_note_via_mcp(directory, filename, content)

        if result.success:
            result.retry_count = retry_count
            return result

        # Failed - retry with backoff
        retry_count += 1
        if retry_count < max_retries:
            log_info(f"Retry {retry_count}/{max_retries} after {backoff_seconds}s")
            time.sleep(backoff_seconds)
            backoff_seconds *= 2  # Exponential backoff

    # All retries failed
    result.retry_count = retry_count
    return result
```

### Step 8: Validate Creation

```python
def validate_note_created(note_path):
    # Verify note exists in Obsidian vault

    try:
        # Use MCP read_note() to verify
        result = obsidian_mcp.read_note(path=note_path)

        if result.success and result.content:
            return True
        else:
            return False

    except Exception as e:
        log_error(f"Validation failed: {e}")
        return False
```

## Error Handling

**Common Errors:**

1. **Vault Not Found:**

   ```python
   if error.message.contains("vault not found"):
       return error(
           "Obsidian vault not found - check MCP configuration",
           recovery="Verify Obsidian is running and vault is open"
       )
   ```

2. **Permission Denied:**

   ```python
   if error.message.contains("permission denied"):
       return error(
           "Permission denied writing to vault",
           recovery="Check vault write permissions and file locks"
       )
   ```

3. **File Already Exists:**

   ```python
   if error.message.contains("file exists"):
       # Collision handling should prevent this, but handle anyway
       filename = handle_collision(filename, directory)
       return retry_with_new_filename(filename)
   ```

4. **Invalid Path:**

   ```python
   if error.message.contains("invalid path"):
       return error(
           "Invalid note path",
           recovery="Check path format and directory structure"
       )
   ```

5. **MCP Not Connected:**
   ```python
   if error.type == "MCPConnectionError":
       return error(
           "Obsidian MCP not connected",
           recovery="Restart Obsidian or check MCP server configuration"
       )
   ```

## Complete Algorithm Flow

```python
def create_atomic_note(variables):
    try:
        # Step 1: Load template
        template = load_template()

        # Step 2: Substitute variables
        content = substitute_variables(template, variables)

        # Step 3: Generate filename
        filename = generate_filename(
            variables['title'],
            variables['created']
        )

        # Step 4: Determine directory
        directory = determine_directory(variables['building_block'])

        # Step 5: Handle collisions
        filename = handle_collision(filename, directory)

        # Step 6-7: Create note with retry
        result = create_note_with_retry(directory, filename, content)

        if not result.success:
            return {
                'success': False,
                'error': result.error,
                'retry_count': result.retry_count
            }

        # Step 8: Validate creation
        if not validate_note_created(result.note_path):
            return {
                'success': False,
                'error': 'Note creation could not be verified',
                'retry_count': result.retry_count
            }

        # Success!
        return {
            'success': True,
            'note_path': result.note_path,
            'note_title': variables['title'],
            'directory': directory,
            'filename': filename,
            'error': None,
            'retry_count': result.retry_count
        }

    except TemplateError as e:
        return error(f"Template error: {e}")
    except ValidationError as e:
        return error(f"Validation error: {e}")
    except Exception as e:
        return error(f"Unexpected error: {e}")
```

## Example Usage

```python
# Prepare template variables
variables = {
    'title': 'Zettelkasten Principle - Atomicity',
    'type': 'concept',
    'building_block': 'concept',
    'content': 'Each note should contain exactly one complete idea...',
    'atomic_score': 0.92,
    'created': '2025-11-05T14:30:00Z',
    'created_date': '2025-11-05',
    'sanitized_title': 'zettelkasten-principle-atomicity',
    'tags': ['zettelkasten', 'note-taking', 'atomicity'],
    'source_note': None,
    'source_url': 'https://zettelkasten.de/posts/create-zettel-from-reading-notes/',
    'source_author': 'Sascha Fast',
    'related_concepts': ['[[Bidirectional Links]]', '[[Evergreen Notes]]'],  # Will be converted to bullet list
    'fragmented_from': None,
    'fragment_number': None
}

# Create the atomic note (prepare_variables will convert arrays to formatted strings)
result = create_atomic_note(variables)

if result.success:
    print(f"✓ Note created: {result.note_path}")
else:
    print(f"✗ Failed: {result.error}")
```

## Security Considerations

**Path Validation:**

```python
def validate_path_security(path):
    # Block directory traversal
    if '../' in path or '/..' in path:
        raise SecurityError("Directory traversal attempt blocked")

    # Ensure path starts with allowed prefix
    allowed_prefixes = ['/atomic/', '/inbox/', '/mocs/']

    if not any(path.startswith(prefix) for prefix in allowed_prefixes):
        raise SecurityError("Path outside allowed directories")

    return True
```

**Content Sanitization:**

```python
def sanitize_content(content):
    # Already validated by analyze-atomicity, but double-check

    dangerous_patterns = [
        r'<script.*?>',
        r'javascript:',
        r'file://',
        r'onerror=',
        r'onclick='
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            raise SecurityError(f"Dangerous content pattern: {pattern}")

    return content
```

## Testing Notes

Test this task with:

1. **Valid atomic note:** Should create successfully
2. **Duplicate filename:** Should append -2, -3 until unique
3. **Invalid building block type:** Should default to /atomic/concepts/
4. **MCP disconnected:** Should fail with clear error message
5. **Very long title:** Should truncate filename to 100 chars
6. **Special characters in title:** Should sanitize to safe filename
7. **Fragmented note:** Should include fragment metadata
8. **Retry scenario:** Simulate MCP timeout, verify retry logic

## Integration Notes

- Called by fragment-note.md task for each fragment
- Called directly via `*fragment-note` agent command
- Requires Obsidian MCP Tools running in Claude Desktop/Cursor
- Outputs feed into `*validate-note` for verification
- File paths returned for linking and tracking

## Usage Notes

- Run via fragment-note.md task (automated)
- Can be tested standalone for debugging
- Retry logic handles transient MCP connection issues
- Collision handling prevents overwriting existing notes
- Directory routing keeps vault organized by type
