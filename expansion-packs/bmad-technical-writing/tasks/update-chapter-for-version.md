<!-- Powered by BMAD™ Core -->

# Update Chapter for Version

---

task:
  id: update-chapter-for-version
  name: Update Chapter for New Technology Version
  description: Update a specific chapter for new technology version (e.g., Python 3.9 → 3.12)
  persona_default: book-analyst
  inputs:
    - chapter_path
    - current_version (e.g., Python 3.9)
    - target_version (e.g., Python 3.12)
    - breaking_changes_list
  steps:
    - Review chapter current state and code examples
    - Identify target version (Python 3.12, Node 20, etc.)
    - Update import statements for new version conventions
    - Replace deprecated methods/APIs with current equivalents
    - Adopt new syntax features where applicable (e.g., match/case in Python 3.10+)
    - Update all code examples and test on exact target version
    - Revise explanatory text for new best practices
    - Add migration notes if changes are significant
    - Update cross-references if chapter numbers or sections changed
    - Run execute-checklist.md with version-update-checklist.md
    - Document changes in chapter change log
  output: Updated chapter file with version-specific changes documented

---

## Purpose

This task provides a systematic workflow for updating a single chapter when migrating to a new technology version. It ensures code works, text is accurate, and changes are well-documented.

## Prerequisites

Before starting this task:

- Chapter revision matrix identifies this chapter for version update
- Target technology version is clearly defined
- Breaking changes between versions are documented
- Testing environment with target version is set up
- Code patterns extracted (if maintaining consistency is critical)

## Workflow Steps

### 1. Review Chapter Current State

Read the chapter completely to understand:

- What concepts are taught
- What code examples are present
- How examples build on each other
- What the learning objectives are
- Which technology features are demonstrated

Note the chapter's role in the overall learning progression.

### 2. Identify Target Version

Confirm the specific target version:

- Current version: Python 3.9, Node 16, Django 3.2, etc.
- Target version: Python 3.12, Node 20, Django 4.2, etc.
- Release date and stability (LTS preferred)
- Breaking changes list (consult official migration guides)
- New features available in target version

### 3. Update Import Statements

Modernize imports for new version:

**Python Example:**
```python
# Old (Python 3.9)
from typing import List, Dict, Optional

# New (Python 3.10+)
from collections.abc import Sequence
# Use built-in list, dict instead of typing.List, typing.Dict
```

**JavaScript Example:**
```javascript
// Old (Node 16)
const fs = require('fs').promises;

// New (Node 20 with native fetch)
// Update examples to use modern ESM imports if appropriate
```

Verify imports work with target version.

### 4. Replace Deprecated Methods/APIs

Find and replace deprecated functionality:

**Python Example:**
```python
# Old (deprecated in 3.10)
collections.Iterable

# New
collections.abc.Iterable
```

**Django Example:**
```python
# Old (Django 3.x)
from django.conf.urls import url

# New (Django 4.x)
from django.urls import re_path
```

Consult official deprecation notices and migration guides.

### 5. Adopt New Syntax Where Applicable

Introduce new language features where pedagogically appropriate:

**Python 3.10+ Match/Case:**
```python
# Consider updating if/elif chains to match/case
# Old
if status == 'open':
    handle_open()
elif status == 'closed':
    handle_closed()
else:
    handle_unknown()

# New (if teaching Python 3.10+)
match status:
    case 'open':
        handle_open()
    case 'closed':
        handle_closed()
    case _:
        handle_unknown()
```

**Python 3.9+ Type Hints:**
```python
# Old
from typing import List
def process_items(items: List[str]) -> None:
    pass

# New (Python 3.9+)
def process_items(items: list[str]) -> None:
    pass
```

Only add new syntax if:
- It improves clarity
- It's appropriate for the chapter's teaching level
- It doesn't confuse the main concept being taught

### 6. Update Code Examples and Test

For each code example in the chapter:

- Update to target version syntax
- Run the code on exact target version
- Verify output matches expected results
- Fix any errors or warnings
- Update output examples in text if output changed
- Test edge cases

**Testing Checklist:**
- [ ] Code runs without errors
- [ ] Code runs without warnings (or warnings are explained)
- [ ] Output matches what's shown in book
- [ ] Code follows best practices for target version
- [ ] Code is tested on target version specifically

### 7. Revise Explanatory Text

Update prose to reflect version changes:

- Update version references ("Python 3.12 introduced...")
- Revise explanations if behavior changed
- Add notes about version-specific features
- Update best practices if they evolved
- Revise performance notes if characteristics changed
- Update security guidance if recommendations changed

**Example:**
```markdown
Old: "In Python 3.9, you can use type hints with List from the typing module."
New: "In Python 3.12, you can use built-in list directly in type hints without importing from typing."
```

### 8. Add Migration Notes (If Significant)

If changes are substantial, add migration guidance:

- Note what changed from previous version
- Explain why the new approach is better
- Provide migration tips for readers with old code
- Link to official migration guides if helpful

**Example Callout:**
```markdown
> **Migration Note**: If you're updating code from Python 3.9, you can safely replace
> `List[str]` with `list[str]` and `Dict[str, int]` with `dict[str, int]` throughout
> your codebase. The functionality is identical, but the new syntax is more concise.
```

### 9. Update Cross-References

If chapter numbers or section numbers changed:

- Update all "see Chapter X" references
- Update "as discussed in Section Y.Z" references
- Verify forward and backward references are accurate
- Update index entries if applicable
- Update table of contents references

### 10. Run Version Update Checklist

Use execute-checklist.md with version-update-checklist.md to verify:

- [ ] All import statements updated
- [ ] All deprecated methods replaced
- [ ] New syntax adopted appropriately
- [ ] All code tested on target version
- [ ] Text revised for accuracy
- [ ] Best practices current
- [ ] Breaking changes documented
- [ ] Cross-references accurate

### 11. Document Changes

Add to chapter change log:

- Version update: Python 3.9 → 3.12
- Date of update
- Major changes made (deprecated APIs replaced, new syntax added)
- Testing completed on Python 3.12.1
- Reviewer: [name]

This creates an audit trail for future updates.

## Success Criteria

A successfully updated chapter should have:

- [ ] All code examples run successfully on target version
- [ ] No deprecated methods or APIs used
- [ ] Appropriate new syntax features adopted
- [ ] All text accurate for target version
- [ ] Migration notes added where significant changes occurred
- [ ] Cross-references verified and updated
- [ ] Version update checklist passed
- [ ] Changes documented in change log
- [ ] Learning objectives still met with updated content

## Common Pitfalls to Avoid

- **Testing on wrong version**: Must test on exact target version, not "close enough"
- **Over-modernizing**: Don't add new syntax if it obscures the concept being taught
- **Breaking learning flow**: Ensure changes don't confuse the learning progression
- **Forgetting text updates**: Code changes must be reflected in explanations
- **Ignoring cross-references**: Broken references frustrate readers
- **No migration notes**: Readers with old code need guidance

## Next Steps

After updating a chapter:

1. Move to next chapter in revision matrix
2. Track progress against revision timeline
3. Collect updated chapters for comprehensive testing
4. Prepare for technical review phase
5. Ensure consistency across all updated chapters
