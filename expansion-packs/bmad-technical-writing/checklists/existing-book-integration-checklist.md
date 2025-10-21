# Existing Book Integration Checklist

Use this checklist when adding new content to an existing book (new chapters, revised chapters, expanded sections) to ensure consistency with existing content.

## Voice and Tone

- [ ] Voice matches existing chapters (conversational vs. formal)
- [ ] Tone is consistent (friendly, authoritative, encouraging, etc.)
- [ ] Person usage consistent (first person "I/we", second person "you", third person)
- [ ] Formality level matches (casual vs. academic)
- [ ] Humor style consistent (if book uses humor)
- [ ] Technical depth appropriate for book's level

## Code Style Patterns

- [ ] Import organization follows extracted patterns
- [ ] Naming conventions match (snake_case, camelCase, PascalCase)
- [ ] Comment style consistent with existing examples
- [ ] Docstring style matches (Google, NumPy, Sphinx, or none)
- [ ] Error handling patterns followed
- [ ] Code structure patterns maintained (OOP, functional, procedural)
- [ ] Formatting consistent (indentation, line length, spacing)
- [ ] File organization patterns followed

## Terminology Consistency

- [ ] Technical terms match existing usage
- [ ] Abbreviations used consistently (introduce on first use?)
- [ ] Jargon usage consistent (explained or assumed?)
- [ ] Product names match (capitalization, trademarks)
- [ ] Variable names in examples follow patterns
- [ ] Glossary terms used consistently
- [ ] No conflicting definitions for same terms

## Heading Hierarchy

- [ ] Heading levels used correctly (H1, H2, H3)
- [ ] Heading style matches (action-based, question-based, topic-based)
- [ ] Heading capitalization consistent (title case vs. sentence case)
- [ ] Heading length similar to existing chapters
- [ ] Heading numbering follows book's pattern (if numbered)
- [ ] No skipped heading levels (H1→H3 without H2)

## Structural Patterns

- [ ] Chapter organization matches typical flow
- [ ] Section lengths similar to existing chapters
- [ ] Introduction section follows pattern (if pattern exists)
- [ ] Summary section follows pattern (if pattern exists)
- [ ] Exercise placement consistent
- [ ] Code listing placement consistent
- [ ] Callout usage matches frequency and style

## Cross-References

- [ ] Cross-reference format matches ("Chapter 5" vs. "chapter 5")
- [ ] Section reference style consistent ("Section 5.2" vs. "section 5.2")
- [ ] Forward references styled consistently ("we'll cover this in Chapter 7")
- [ ] Backward references styled consistently ("as discussed in Chapter 3")
- [ ] Page references avoided (if book uses digital distribution)
- [ ] All referenced chapters/sections exist
- [ ] Reference accuracy verified

## Learning Progression

- [ ] Prerequisites clearly stated and match book's approach
- [ ] Difficulty level appropriate for chapter placement
- [ ] Learning objectives styled consistently
- [ ] Complexity builds on existing chapters
- [ ] No assumptions beyond stated prerequisites
- [ ] Scaffolding follows book's pedagogical approach
- [ ] Practice opportunities similar to existing chapters

## Callouts and Asides

- [ ] Tip callouts styled consistently (icon, formatting, length)
- [ ] Warning callouts styled consistently
- [ ] Note callouts styled consistently
- [ ] Sidebar usage consistent (if book uses sidebars)
- [ ] Callout frequency similar to existing chapters
- [ ] Callout content length appropriate
- [ ] No new callout types introduced without reason

## Code Examples

- [ ] Code example length similar to existing chapters
- [ ] Code complexity appropriate for chapter level
- [ ] Code snippets vs. full programs ratio similar
- [ ] Code explanations follow book's pattern (before? after? inline?)
- [ ] Output examples styled consistently
- [ ] Error examples styled consistently (if book shows errors)
- [ ] Code file naming follows patterns

## Exercises and Practice

- [ ] Exercise difficulty matches book's progression
- [ ] Exercise format consistent (numbered, titled, etc.)
- [ ] Exercise quantity similar to existing chapters
- [ ] Solution availability consistent (provided, hints, none)
- [ ] Challenge problem format consistent (if book has challenges)
- [ ] Quiz format consistent (if book has quizzes)

## Formatting and Style

- [ ] List formatting consistent (bullets, numbers, indentation)
- [ ] Table formatting matches
- [ ] Figure/image style consistent
- [ ] Caption style matches
- [ ] Code block formatting consistent
- [ ] Inline code formatting consistent (`backticks` vs. other)
- [ ] Emphasis usage consistent (bold, italic, both)
- [ ] Quotation marks consistent (single, double, smart quotes)

## Front/Back Matter References

- [ ] Chapter listed in Table of Contents
- [ ] Learning objectives added to chapter overview (if book has this)
- [ ] Key terms added to glossary (if applicable)
- [ ] Index entries created for new content
- [ ] Appendix references added (if applicable)
- [ ] Resource list updated (if applicable)

## Technology and Versions

- [ ] Technology versions match book's target versions
- [ ] Platform assumptions consistent (OS, hardware)
- [ ] Tool requirements consistent with book's setup
- [ ] Library versions match or are compatible
- [ ] Installation instructions match book's approach
- [ ] Testing approach consistent

## Publisher Compliance

- [ ] Page count appropriate for chapter position
- [ ] Format requirements met (if publisher-specific)
- [ ] Legal disclaimers present (if needed)
- [ ] Trademark usage consistent
- [ ] Copyright notices consistent
- [ ] Attribution style matches

## Quality Standards

- [ ] No placeholder content (TBD, TODO, XXX)
- [ ] No broken links or references
- [ ] No orphaned footnotes or endnotes
- [ ] Spelling checked with book's dictionary
- [ ] Grammar consistent with book's style
- [ ] Readability score similar to existing chapters

## Examples of Good vs. Bad Integration

**✅ Good Integration:**
```markdown
## Setting Up Authentication

As we saw in Chapter 3, user authentication is critical for secure applications.
In this section, we'll implement JWT-based authentication using Flask.

> **Note**: JWT tokens should always include an expiration time to limit
> security exposure.

```python
from flask import Flask, request
from datetime import datetime, timedelta

def create_token(user_id):
    """
    Create JWT token for user.

    Args:
        user_id: Unique user identifier

    Returns:
        Encoded JWT token string
    """
    # Implementation follows
```
- Matches voice/tone
- Follows cross-reference style
- Uses consistent callout format
- Follows code patterns (imports, docstring style)

**❌ Bad Integration:**
```markdown
# Auth Setup

Let's do authentication now!

**IMPORTANT!!!** Don't forget expiration!

from flask import *
def make_token(uid):
    # make the token
```
- Heading style different (# vs ##)
- Voice too casual/inconsistent
- Callout style different (bold vs. callout box)
- Code style inconsistent (import *, no docstring, different naming)

## Red Flags

- New content "feels different" when reading sequentially
- Reviewers comment on inconsistency
- Different terminology for same concepts
- Code style visibly different
- Heading styles don't match
- Callout formats vary
- Cross-references styled differently
- Learning difficulty jumps unexpectedly
