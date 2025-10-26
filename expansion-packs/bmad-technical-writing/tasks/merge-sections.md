<!-- Powered by BMAD™ Core -->

# Merge Sections

---

task:
id: merge-sections
name: Merge Sections
description: Systematically merge completed chapter sections into single integrated chapter file with introduction, summary, and consistent formatting
persona_default: tutorial-architect
inputs:
  - completed-sections-list
  - chapter-number
  - chapter-outline
steps:
  - Gather all completed section files
  - Verify all sections marked DONE and present
  - Validate section order for logical learning progression
  - Merge sections in order preserving all content
  - Add chapter introduction if not in section 1
  - Add chapter summary if not in final section
  - Standardize heading hierarchy throughout
  - Ensure code formatting consistency
  - Unify terminology and naming conventions
  - Validate no content lost during merge
  - Create manuscript/chapters/chapter-{{chapter_number}}-integrated.md
output: manuscript/chapters/chapter-{{chapter_number}}-integrated.md

---

## Purpose

Merge all completed sections into a single cohesive chapter file while preserving section content integrity. This is the first step in chapter assembly - combining the pieces without rewriting. Focus is on mechanical integration, not enhancement (transitions come later).

## Prerequisites

- All chapter sections marked DONE
- Section files available (section-*-final.md or equivalent)
- Chapter outline available with section order
- No critical issues blocking sections from integration

## Workflow Steps

### 1. Preparation - Gather All Section Files

Collect and verify section files are ready:

**Locate Section Files:**

- Find all completed section files for this chapter
- Typical naming: `section-{chapter}.{section}-final.md`
- Example: `section-3.1-final.md`, `section-3.2-final.md`
- Check manuscript/sections/ directory

**Verify Completeness:**

- All sections from chapter outline present
- Each section marked DONE or equivalent status
- No sections in draft or review state
- All code examples tested and validated

**Create Section Inventory:**

```
Chapter 3 Sections:
☑ Section 3.1: Lists - section-3.1-final.md
☑ Section 3.2: Dictionaries - section-3.2-final.md
☑ Section 3.3: Sets - section-3.3-final.md
☑ Section 3.4: Tuples - section-3.4-final.md
☑ Section 3.5: List Comprehensions - section-3.5-final.md
☑ Section 3.6: Practical Examples - section-3.6-final.md
```

**Check for Missing Sections:**

- Compare against chapter outline
- Identify any gaps in section sequence
- Verify no sections skipped or forgotten
- HALT if sections missing - cannot merge incomplete chapter

**Purpose:** Ensure all pieces are ready before starting merge.

### 2. Validate Section Order

Confirm sections are in optimal learning sequence:

**Review Chapter Outline:**

- Check planned section order from chapter outline
- Verify section numbering is sequential
- Confirm section titles match outline

**Check Learning Progression:**

- Does difficulty increase gradually?
- Are prerequisites met in sequence?
- Do concepts build logically?
- Are there any circular dependencies?

**Validate Dependencies:**

- Section 3.2 shouldn't require concepts from 3.5
- Earlier sections should cover prerequisites for later ones
- Cross-references should point backward (to covered content) or clearly forward

**Reorder If Needed:**

Sometimes section development reveals better sequencing:

- Discuss reordering with instructional designer if major change
- Update chapter outline to reflect new order
- Document rationale for any changes

**Example Issue:**

```
Problem: Section 3.4 (Tuples) uses list comprehensions extensively
         but Section 3.5 (List Comprehensions) comes after
Solution: Swap order - teach comprehensions before tuples example
```

**Purpose:** Ensure logical learning flow before merge commits the order.

### 3. Merge Section Content

Combine sections into single chapter file:

**Create Chapter File:**

- File: `manuscript/chapters/chapter-{{chapter_number}}-integrated.md`
- Start with chapter title as H1
- Add chapter metadata if using

**Merge Process:**

For each section in order:

1. **Copy section content completely**
   - Include all text, code, images, diagrams
   - Preserve exact wording (no rewriting)
   - Maintain all formatting

2. **Adjust heading levels**
   - Section title becomes H2
   - Subsections become H3
   - Details become H4
   - Never go deeper than H4

3. **Add section dividers (optional)**
   - Consider visual separators between sections
   - Use horizontal rules sparingly
   - Clear white space between sections

4. **Preserve all code examples**
   - Copy code blocks exactly
   - Maintain syntax highlighting language tags
   - Keep all code comments
   - Include expected output

**DO NOT during merge:**

- ❌ Rewrite section content
- ❌ Remove "redundant" explanations (may be intentional reinforcement)
- ❌ Modify code examples (they're tested as-is)
- ❌ Change technical terminology
- ❌ Edit for style or clarity (that comes in later step)

**DO during merge:**

- ✓ Preserve all content exactly
- ✓ Maintain heading hierarchy
- ✓ Keep code formatting
- ✓ Include all images/diagrams

**Purpose:** Mechanical assembly without content changes - preserving tested material.

### 4. Add Chapter Introduction

If first section doesn't include chapter intro, add one:

**When to Add:**

- Section 1 jumps straight into content without context
- No overview of chapter scope
- Prerequisites not stated
- Learning objectives not listed

**Chapter Introduction Template:**

```markdown
# Chapter {{chapter_number}}: {{chapter_title}}

{{Hook paragraph - why this chapter matters to the reader}}

{{Context paragraph - what reader will learn and build}}

**What You'll Build**: {{Specific outcome or project}}

**Prerequisites**:
- {{Previous chapter or knowledge required}}
- {{Tools or environment setup needed}}

**Time Commitment**: {{Estimated hours to complete chapter}}

**Learning Objectives**:
1. {{Objective 1 - specific, measurable}}
2. {{Objective 2}}
3. {{Objective 3}}
4. {{Objective 4}}

---

## {{First Section Title}}

{{Section 1 content begins here...}}
```

**Introduction Guidelines:**

- **Hook**: Connect to reader's goals (Why should I care?)
- **Context**: Big picture of what chapter covers
- **What You'll Build**: Concrete outcome (app, feature, skill)
- **Prerequisites**: Honest assessment of what's needed
- **Time**: Helps readers plan (be realistic)
- **Learning Objectives**: Specific, testable outcomes

**Example Hook:**

> "Database queries can make or break your application's performance. In this chapter, you'll learn how to write efficient queries that scale from hundreds to millions of records without grinding to a halt."

**When to Skip:**

- Section 1 already has comprehensive introduction
- Chapter is part of larger tutorial with shared intro
- Publisher format doesn't use chapter intros

**Purpose:** Orient reader before diving into content.

### 5. Add Chapter Summary

If final section doesn't include summary, add one:

**When to Add:**

- Last section ends without recap
- No review of what was learned
- Missing "what's next" guidance
- No further reading suggestions

**Chapter Summary Template:**

```markdown
## Summary

{{Recap paragraph - what reader accomplished in this chapter}}

**Key Concepts Covered**:
- {{Concept 1 - brief reminder}}
- {{Concept 2}}
- {{Concept 3}}
- {{Concept 4}}

**Skills Developed**:
- {{Skill 1 - what reader can now do}}
- {{Skill 2}}
- {{Skill 3}}

**In the Next Chapter**:

{{Preview of Chapter N+1 - how it builds on this foundation}}

**Further Reading**:
- {{Resource 1 - official docs, articles, books}}
- {{Resource 2}}
- {{Resource 3}}
```

**Summary Guidelines:**

- **Recap**: Celebrate accomplishment
- **Key Concepts**: Refresh main ideas (not exhaustive)
- **Skills**: Emphasize practical abilities gained
- **Next Chapter**: Create momentum
- **Further Reading**: Optional deeper dives

**Example Skills:**

> "After completing this chapter, you can now:
> - Design normalized database schemas with proper relationships
> - Write efficient SQL queries with joins and indexes
> - Optimize query performance using EXPLAIN ANALYZE
> - Handle database migrations safely in production"

**When to Skip:**

- Final section already has comprehensive summary
- Using cumulative end-of-chapter review exercises
- Publisher format has separate review sections

**Purpose:** Reinforce learning and create closure.

### 6. Format Consistency

Standardize formatting throughout merged chapter:

**Heading Hierarchy:**

Ensure consistent structure:

```
# Chapter 3: Data Structures          ← H1 (chapter title only)
## Section 3.1: Lists                  ← H2 (section titles)
### Creating Lists                     ← H3 (subsections)
#### List Initialization Syntax        ← H4 (details)
```

**Check:**
- Only one H1 (chapter title)
- H2 for each section
- H3 for subsections
- H4 sparingly for details
- No heading level skips (H2 → H4)

**Code Block Formatting:**

Standardize all code:

- Language specified: ` ```python `, ` ```javascript `
- Consistent indentation (spaces vs tabs)
- Line length manageable (no extreme horizontal scrolling)
- Comments formatted consistently

**Example:**

```python
# Good - language specified, clear formatting
def calculate_total(items):
    """Calculate total price of items."""
    return sum(item.price for item in items)
```

**Terminology Unification:**

Standardize terms across sections:

- Use same term for same concept throughout
- Match official documentation terminology
- Consistent capitalization (PostgreSQL, not Postgresql)
- Consistent hyphenation (e.g., "database" not "data base")

**Create term glossary:**

```
API (not api or Api)
PostgreSQL (not Postgres in formal text)
JavaScript (not Javascript)
filename (not file name or file-name)
```

**Cross-Reference Formatting:**

If sections reference each other:

- Update section numbers after merge
- Verify cross-references still accurate
- Use consistent reference format
- Consider using "earlier in this chapter" vs specific section numbers

**Purpose:** Professional consistency throughout chapter.

## Quality Checks

Before considering merge complete, verify:

**Content Preservation:**

- ✓ All sections present in final chapter
- ✓ No sections accidentally omitted
- ✓ All code examples included
- ✓ All images/diagrams referenced
- ✓ No content lost during copy-paste

**Section Order:**

- ✓ Sections in logical learning sequence
- ✓ Prerequisites met before use
- ✓ Difficulty increases gradually
- ✓ No circular dependencies

**Heading Hierarchy:**

- ✓ Single H1 (chapter title)
- ✓ H2 for section titles
- ✓ H3 for subsections
- ✓ Logical nesting (no skipped levels)

**Code Formatting:**

- ✓ All code blocks have language tags
- ✓ Consistent indentation
- ✓ Code examples preserved exactly as tested
- ✓ Syntax highlighting will work

**Completeness:**

- ✓ Chapter introduction present
- ✓ Chapter summary present
- ✓ All learning objectives addressed
- ✓ Prerequisites clearly stated

**File Output:**

- ✓ Saved as manuscript/chapters/chapter-{{chapter_number}}-integrated.md
- ✓ File is valid markdown
- ✓ Images paths are correct
- ✓ Ready for next step (transitions enhancement)

## Common Issues and Solutions

**Issue:** Section missing from merge

**Solution:** Go back to preparation step, verify all section files present, check chapter outline for complete section list

---

**Issue:** Heading hierarchy inconsistent (some sections use H2, others H3)

**Solution:** Standardize all section titles to H2, adjust subsection levels accordingly

---

**Issue:** Code formatting varies between sections (tabs vs spaces)

**Solution:** Choose one standard (spaces preferred), convert all code blocks, verify code still runs after reformatting

---

**Issue:** Sections reference each other by wrong numbers

**Solution:** Update cross-references to match final section order, consider using descriptive references ("in the previous section") instead of numbers

---

**Issue:** Duplicate content in multiple sections

**Solution:** Leave as-is if intentional reinforcement; if unintentional, note for transitions phase but don't remove during merge

---

**Issue:** Section order doesn't make sense after merge

**Solution:** Stop merge, consult with instructional designer, reorder sections, update chapter outline, restart merge

## Output

Merged chapter file containing:

- Single H1 chapter title
- Chapter introduction with learning objectives and prerequisites
- All sections in order with consistent H2 section headings
- All content from sections preserved exactly
- All code examples, images, diagrams included
- Consistent heading hierarchy throughout
- Chapter summary with key concepts and skills
- Unified terminology and formatting

**File Location:** `manuscript/chapters/chapter-{{chapter_number}}-integrated.md`

**Status:** Ready for transitions enhancement (next workflow step)

## Next Steps

After merge completion:

1. Verify chapter file is valid markdown
2. Quick read-through to spot any obvious issues
3. Proceed to enhance-transitions.md task (workflow step 2)
4. Do not skip to technical review - transitions first
5. Integrated chapter will be polished in next step

## Notes

**This is mechanical assembly, not creative enhancement.**

- Preserve section content exactly
- Don't rewrite or improve yet
- Focus on getting pieces together correctly
- Transitions and polish come in next steps
- Trust that section content is already tested and validated

**Merge is complete when:**

- All sections present and in order
- Heading hierarchy consistent
- Chapter intro and summary added
- No content lost
- File saved and ready for next step
