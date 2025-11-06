<!-- Powered by BMAD™ Core -->

# audit-metadata-completeness

Audit frontmatter metadata completeness and validity across all vault notes - detect missing required fields and format issues.

## Purpose

Ensure consistent, complete metadata across knowledge base for effective organization, search, and automation.

## Prerequisites

- Obsidian MCP server configured
- Access to vault notes with frontmatter
- Understanding of required metadata schema

## Inputs

- **vault_path** (string, required): Path to Obsidian vault
- **required_fields** (array, optional): Required fields (default: ['title', 'created'])
- **recommended_fields** (array, optional): Recommended fields (default: ['tags', 'type'])
- **validate_formats** (boolean, optional): Validate field formats (default: true)

## Outputs

```yaml
metadata_audit:
  total_notes: integer
  notes_with_metadata_issues: integer
  metadata_completeness_percentage: float
  audit_timestamp: string
  metadata_issues:
    - note_path: string
      note_title: string
      issue_severity: string # 'CRITICAL|HIGH|MEDIUM|LOW'
      missing_fields: array # ['title', 'created']
      invalid_fields: array # [{'field': 'created', 'error': 'Invalid date format'}]
      recommendations: array # Auto-fix suggestions
```

## Algorithm

### Step 1: Query All Notes with Frontmatter

```
1. Connect to Obsidian MCP
2. list_notes() with metadata=true
3. For each note:
   - Extract frontmatter (YAML between ---)
   - Parse YAML (handle malformed gracefully)
   - Store: {note_path, frontmatter_dict}
```

### Step 2: Validate Required Fields

**Default Required Fields:**
- **title** (non-empty string)
- **created** (ISO 8601 timestamp)

**Validation:**
```
For each note:
  missing_fields = []

  if 'title' not in frontmatter OR frontmatter['title'] == '':
    missing_fields.append('title')
    issue_severity = 'CRITICAL'

  if 'created' not in frontmatter:
    missing_fields.append('created')
    issue_severity = 'CRITICAL'
```

### Step 3: Validate Recommended Fields

**Default Recommended Fields:**
- **tags** (array, at least 1 tag)
- **type** or **building_block** (for atomic notes)
- **source** or **author** (for notes with external claims)

**Validation:**
```
For each note:
  if 'tags' not in frontmatter OR len(frontmatter['tags']) == 0:
    missing_fields.append('tags')
    issue_severity = max(issue_severity, 'HIGH')

  if 'type' not in frontmatter AND 'building_block' not in frontmatter:
    missing_fields.append('type')
    issue_severity = max(issue_severity, 'HIGH')
```

### Step 4: Format Validation

If validate_formats=true:

**Date Format (ISO 8601):**
```
if 'created' in frontmatter:
  try:
    datetime.fromisoformat(frontmatter['created'])
  except ValueError:
    invalid_fields.append({'field': 'created', 'error': 'Invalid ISO 8601 format'})
    issue_severity = max(issue_severity, 'MEDIUM')
```

**Tags Format (Array):**
```
if 'tags' in frontmatter:
  if not isinstance(frontmatter['tags'], list):
    invalid_fields.append({'field': 'tags', 'error': 'Must be array'})
    issue_severity = max(issue_severity, 'MEDIUM')
```

**Building Block Type (Valid Values):**
```
valid_types = ['concept', 'argument', 'model', 'question', 'claim', 'phenomenon']

if 'type' in frontmatter:
  if frontmatter['type'] not in valid_types:
    invalid_fields.append({'field': 'type', 'error': f'Invalid type, must be one of {valid_types}'})
    issue_severity = max(issue_severity, 'MEDIUM')
```

### Step 5: Classify Issues by Severity

| Severity | Condition |
|----------|-----------|
| **CRITICAL** | Missing required fields (title, created) |
| **HIGH** | Missing important fields (tags, type) |
| **MEDIUM** | Format issues (wrong date format, malformed YAML) |
| **LOW** | Missing optional fields |

### Step 6: Generate Auto-Fix Suggestions

For each issue, provide recommendations:

```
if 'title' missing:
  recommendations.append("Add title field based on filename")

if 'created' missing:
  recommendations.append("Add created field using file system timestamp")

if 'tags' missing:
  recommendations.append("Add at least one tag for categorization")

if 'type' missing:
  recommendations.append("Classify note as one of: concept, argument, model, question, claim, phenomenon")

if date format invalid:
  recommendations.append("Convert date to ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ")
```

### Step 7: Calculate Completeness

```
notes_with_complete_metadata = total_notes - notes_with_metadata_issues
metadata_completeness_percentage = (notes_with_complete_metadata / total_notes) * 100
```

## Performance Target

<3 seconds for 1000-note vault

## Use Cases

**1. Metadata Standardization**
- Ensure all notes have required fields
- Maintain consistent format

**2. Search Optimization**
- Complete metadata improves search
- Tags enable filtering

**3. Automation Readiness**
- Metadata enables automated workflows
- Type classification for processing

## Error Handling

**Malformed YAML:**
- Warning: "Malformed YAML in frontmatter, skipping validation"
- Issue severity: MEDIUM
- Recommendation: "Fix YAML syntax errors"

**Missing Frontmatter:**
- Not an error (personal notes may lack frontmatter)
- Count as incomplete, suggest adding frontmatter

## Testing

**Test Case:** 100-note vault
- 60 complete metadata
- 20 missing title/created (CRITICAL)
- 15 missing tags/type (HIGH)
- 5 format issues (MEDIUM)

Expected: 40 issues detected, 60% completeness

## Integration

Executed by:
- `*audit-metadata` command
- `*audit-full` command
- Progressive audit batch processing
