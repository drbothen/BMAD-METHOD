<!-- Powered by BMAD™ Core -->

# Extract Code Patterns

---

task:
id: extract-code-patterns
name: Extract Code Patterns from Existing Book
description: Analyze existing code examples to learn style patterns for maintaining consistency in updates
persona_default: book-analyst
inputs: - existing_book_path - code_repository_path (if exists)
steps: - Scan all code examples across entire book - Identify import organization patterns (standard library first? grouped? alphabetical?) - Note naming conventions (snake_case, camelCase, variable prefixes, class names) - Observe comment styles (docstrings? inline? comment density? formatting) - Extract error handling patterns (try/except usage, error messages, logging) - Identify common code structures (class-based? functional? procedural? OOP patterns) - Note formatting choices (indentation, line length, spacing, blank lines) - Document code file organization patterns (imports→constants→classes→main) - Analyze code complexity patterns (simple examples vs. comprehensive demos) - Generate style guide summary document - Run execute-checklist.md with existing-book-integration-checklist.md
output: docs/style/{{book_title}}-code-patterns.md

---

## Purpose

This task extracts code style patterns from an existing book to ensure new or updated code examples maintain consistency with the established style. Critical for brownfield work where consistency matters.

## Prerequisites

Before starting this task:

- Access to all chapters with code examples
- Access to code repository if one exists
- Understanding of programming language(s) used in book

## Workflow Steps

### 1. Scan All Code Examples

Read through the entire book systematically to collect all code examples:

- Chapter-by-chapter scan
- Count total code examples
- Categorize by type (snippets, full files, project code)
- Note which chapters have the most code
- Identify any inconsistencies between chapters

### 2. Identify Import Organization Patterns

Analyze how imports are organized:

**Python Import Patterns:**

- Order: Standard library → Third-party → Local imports?
- Grouping: Alphabetical within groups?
- Spacing: Blank lines between groups?
- Format: `import os` vs `from os import path`?

**Example Pattern Found:**

```python
# Standard library imports (alphabetical)
import json
import os
from pathlib import Path

# Third-party imports (alphabetical)
import numpy as np
import pandas as pd
from flask import Flask, request

# Local imports
from .models import User
from .utils import validate_email
```

**JavaScript Import Patterns:**

- CommonJS vs ESM?
- Named imports vs default imports?
- Import order conventions?

Document the pattern consistently used throughout the book.

### 3. Note Naming Conventions

Extract naming patterns used:

**Variables:**

- snake_case, camelCase, or PascalCase?
- Descriptive names or short names?
- Any prefixes? (e.g., `str_name`, `is_valid`, `has_permission`)

**Functions:**

- Naming style? (snake_case for Python, camelCase for JavaScript?)
- Verb-based names? (get_user, calculate_total, validate_input)
- Prefix patterns? (is_valid, has_items, can_delete)

**Classes:**

- PascalCase? (UserAccount, DatabaseConnection)
- Singular vs plural? (User vs Users)
- Suffix patterns? (UserManager, DataProcessor, HTMLRenderer)

**Constants:**

- UPPER_SNAKE_CASE?
- Placement? (top of file? separate config file?)

**Example Pattern Found:**

```python
# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Functions: snake_case, verb-based
def calculate_total(items):
    pass

def is_valid_email(email):
    pass

# Classes: PascalCase, singular nouns
class UserAccount:
    pass

class DatabaseConnection:
    pass
```

### 4. Observe Comment Styles

Analyze commenting patterns:

**Docstrings:**

- Present? (always, sometimes, rarely?)
- Format? (Google style, NumPy style, Sphinx style?)
- What's documented? (all functions? only public APIs?)

**Inline Comments:**

- Frequency? (heavy, moderate, minimal?)
- Style? (full sentences? fragments? end-of-line? above code?)
- Purpose? (explain why? explain what? both?)

**File Headers:**

- Module docstrings?
- Author, date, description?
- License information?

**Example Pattern Found:**

```python
def calculate_discount(price, discount_percent):
    """
    Calculate discounted price.

    Args:
        price (float): Original price
        discount_percent (float): Discount percentage (0-100)

    Returns:
        float: Discounted price
    """
    # Convert percentage to decimal
    discount_decimal = discount_percent / 100

    # Apply discount
    return price * (1 - discount_decimal)
```

### 5. Extract Error Handling Patterns

Identify error handling approaches:

**Exception Handling:**

- try/except usage frequency?
- Specific exceptions caught or broad Exception?
- Error message style?
- Logging patterns?
- Re-raising exceptions?

**Validation:**

- Input validation at function start?
- Assertions used?
- Guard clauses?

**Example Pattern Found:**

```python
def process_user(user_id):
    """Process user with comprehensive error handling."""
    if not user_id:
        raise ValueError("user_id is required")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return None
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise

    return user
```

### 6. Identify Code Structure Patterns

Analyze overall code organization:

**Programming Paradigm:**

- Object-oriented? (classes, inheritance, polymorphism)
- Functional? (pure functions, immutability, higher-order functions)
- Procedural? (step-by-step scripts)
- Mixed? (where and why?)

**Design Patterns:**

- Any common patterns? (Factory, Singleton, Observer, etc.)
- Consistent pattern usage across examples?

**Code Organization:**

- File structure patterns?
- Class organization patterns (properties→init→public→private)?
- Module organization patterns?

**Example Pattern Found:**

```
File organization:
1. Module docstring
2. Imports (stdlib, third-party, local)
3. Constants
4. Helper functions
5. Main classes
6. if __name__ == '__main__' block
```

### 7. Note Formatting Choices

Document formatting standards:

**Indentation:**

- Spaces or tabs? (Python: 4 spaces is PEP 8)
- Consistent indentation levels?

**Line Length:**

- Maximum line length? (79, 88, 100, 120 chars?)
- Line breaking style?

**Spacing:**

- Blank lines between functions? (2 for top-level, 1 for methods?)
- Spacing around operators? (a + b vs a+b)
- Spacing in function calls? (func(a, b) vs func( a, b ))

**Quotes:**

- Single or double quotes?
- Consistency?

**Example Pattern Found:**

```
- Indentation: 4 spaces (never tabs)
- Line length: 88 characters maximum
- Blank lines: 2 between top-level definitions, 1 between methods
- Quotes: Double quotes for strings, single for identifiers
- Operators: Spaces around (x = y + 2, not x=y+2)
```

### 8. Document Code File Organization

Identify file structure patterns:

**Import Section:**

- Always at top?
- Grouped and ordered how?

**Constants Section:**

- After imports?
- Separate section?

**Class Definitions:**

- Order? (base classes first? main classes first?)
- Internal organization? (properties→**init**→public→private?)

**Main Execution:**

- `if __name__ == '__main__'` block?
- main() function pattern?

**Example Pattern Found:**

```python
# 1. Module docstring
"""
Module for user authentication.
"""

# 2. Imports
import os
from typing import Optional

# 3. Constants
DEFAULT_TIMEOUT = 30

# 4. Helper functions
def _internal_helper():
    pass

# 5. Main classes
class UserAuth:
    pass

# 6. Main execution
if __name__ == '__main__':
    main()
```

### 9. Analyze Code Complexity Patterns

Understand example complexity distribution:

**Simple Snippets:**

- How many? (percentage of total examples)
- Purpose? (demonstrate single concept)
- Typical length? (5-10 lines)

**Medium Examples:**

- How many?
- Purpose? (demonstrate technique in context)
- Typical length? (20-50 lines)

**Complete Projects:**

- How many?
- Purpose? (demonstrate full application)
- Typical length? (100+ lines, multiple files)

This helps maintain appropriate complexity when adding new examples.

### 10. Generate Style Guide Summary

Create comprehensive code-patterns.md document with all findings:

```markdown
# Code Style Patterns for [Book Title]

## Import Organization

[Document pattern]

## Naming Conventions

[Document pattern]

## Comment Styles

[Document pattern]

## Error Handling

[Document pattern]

## Code Structure

[Document pattern]

## Formatting

[Document pattern]

## File Organization

[Document pattern]

## Complexity Guidelines

[Document pattern]

## Examples

[Provide examples of well-styled code from the book]
```

This document becomes the reference for all new/updated code.

### 11. Validate with Integration Checklist

Run execute-checklist.md with existing-book-integration-checklist.md to ensure:

- Code patterns are comprehensive
- Patterns are consistent across book
- Examples are clear and representative
- New code can match extracted patterns

## Success Criteria

A completed code pattern extraction should have:

- [ ] All code examples analyzed
- [ ] Import patterns documented
- [ ] Naming conventions extracted
- [ ] Comment styles identified
- [ ] Error handling patterns noted
- [ ] Code structure patterns documented
- [ ] Formatting choices specified
- [ ] File organization patterns defined
- [ ] Complexity patterns understood
- [ ] Comprehensive style guide created
- [ ] Integration checklist passed

## Common Pitfalls to Avoid

- **Inconsistency analysis**: If book has inconsistent patterns, document the _most common_ pattern and note variations
- **Over-specificity**: Extract patterns, not rigid rules that prevent good code
- **Ignoring context**: Some chapters may intentionally use different patterns (e.g., teaching different styles)
- **Missing examples**: Include code examples in style guide for clarity

## Next Steps

After extracting code patterns:

1. Use style guide when writing new code examples
2. Apply patterns when updating existing code
3. Share style guide with technical reviewers
4. Reference in existing-book-integration-checklist.md
5. Update style guide if patterns evolve
