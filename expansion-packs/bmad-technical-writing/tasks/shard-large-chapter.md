<!-- Powered by BMAD™ Core -->

# Shard Large Chapter

---

task:
id: shard-large-chapter
name: Shard Large Chapter
description: Break 30+ page chapter into manageable 5-page shards for easier editing and review
persona_default: tutorial-architect
inputs: - chapter-file-path - target-shard-size
steps: - Analyze chapter structure and identify optimal split points - Determine sharding strategy (by heading, by size, or hybrid) - Create shard files with proper naming and metadata - Generate shard index file for reassembly tracking - Validate all content preserved and properly formatted - Document cross-references that span shards
output: Multiple shard files in chapter-{n}-shards/ directory with index file

---

## Purpose

This task breaks large chapters (30+ pages) into smaller, manageable shards (5-10 pages each) to:

- Work within AI context window limits
- Enable focused editing and review sessions
- Allow parallel development by multiple writers
- Improve version control granularity
- Make large chapters less overwhelming

## When to Use This Task

**Shard a chapter when:**

- Chapter exceeds 30 pages
- Context window limits are being hit during editing
- Multiple writers need to work on different sections
- Focused review of specific sections is needed
- Large chapter causes performance issues in editor

**Don't shard when:**

- Chapter is under 30 pages
- Chapter has simple structure (1-2 major sections)
- No collaboration or context issues exist

## Prerequisites

Before sharding:

- Chapter manuscript exists and is complete (or mostly complete)
- Chapter follows standard heading structure (##, ###, ####)
- All code blocks properly fenced with ``` markers
- Chapter content is saved and backed up

## Workflow Steps

### 1. Analyze Chapter Structure

Understand the chapter's organization:

**Read the entire chapter to identify:**

- Total page count (estimate 500-1000 tokens per page)
- Number and distribution of ## headings (major sections)
- Number and distribution of ### headings (subsections)
- Location of code blocks, tables, diagrams
- Complex content that shouldn't be split

**Calculate optimal shard count:**

- Target shard size: 5-10 pages
- Formula: `shard_count = ceil(total_pages / 5)`
- Example: 32-page chapter → 7 shards of ~5 pages each

**Document structure findings:**

```
Chapter Analysis:
- Total pages: 32
- Major sections (##): 8
- Subsections (###): 24
- Code blocks: 12
- Tables/diagrams: 4
- Recommended shards: 6-7
```

### 2. Determine Split Points

Choose where to divide the chapter using the **Hybrid Strategy** (preferred):

**Sharding Strategies:**

**A) By Heading (Preferred):**

- Split at ## (major section) boundaries
- Preserves logical structure
- Easy to understand shard boundaries
- May create uneven shard sizes

**B) By Size (Fallback):**

- Split when shard reaches target page count
- Creates evenly-sized shards
- May split mid-section (less ideal)

**C) Hybrid (Best):**

- Prefer ## heading boundaries
- But enforce maximum shard size (10 pages)
- Split at ### headings if section too large
- Never split mid-paragraph or mid-code-block

**Rules for split points:**

1. **NEVER split:**
   - Mid-paragraph
   - Inside code blocks (```)
   - Inside tables
   - Inside Mermaid diagrams
   - Inside blockquotes or callouts

2. **Prefer splitting at:**
   - ## (major section) headings
   - ### (subsection) headings when ## creates too-large shards
   - Natural topic boundaries

3. **Document borderline cases:**
   - Cross-references spanning shards
   - Code examples referenced across shards
   - Continuing narratives

**Example split point plan:**

```
Shard 1: Pages 1-6 (Introduction + Section 1)
Shard 2: Pages 7-12 (Section 2)
Shard 3: Pages 13-17 (Section 3)
Shard 4: Pages 18-23 (Section 4 + Section 5)
Shard 5: Pages 24-29 (Section 6 + Section 7)
Shard 6: Pages 30-32 (Section 8 + Summary + Exercises)
```

### 3. Create Shard Files

For each determined split point, create a shard file:

**Naming convention:**

- Pattern: `{chapter-name}-shard-{n}.md`
- Example: `chapter-7-shard-1.md`, `chapter-7-shard-2.md`
- Use original chapter filename as base
- Number sequentially starting at 1

**Shard metadata header:**

Add metadata at the top of each shard file:

```markdown
<!-- SHARD METADATA -->
<!-- Original: chapter-7-advanced-queries.md -->
<!-- Shard: 1 of 6 -->
<!-- Pages: 1-6 of 32 -->
<!-- Sections: Introduction, Setting Up the Environment -->
<!-- Split Date: 2025-10-26 -->
<!-- END METADATA -->

# Chapter 7: Advanced PostgreSQL Queries

## Introduction

[content...]
```

**Content extraction:**

1. Extract content from original chapter based on split points
2. Preserve ALL formatting exactly
3. Keep cross-references intact (note if they point outside shard)
4. Include complete code blocks, tables, diagrams
5. Don't modify content, only extract

**Adjust heading levels (IMPORTANT):**

- If shard starts mid-chapter (not at chapter title), NO adjustment needed
- Preserve original heading levels to maintain chapter context
- Exception: If creating standalone shard docs, decrease all heading levels by 1

**Standard approach (preserve levels):**

```markdown
<!-- chapter-7-shard-2.md -->
<!-- SHARD METADATA -->

...

<!-- END METADATA -->

## Section 2: Complex Joins

### Inner Joins

### Outer Joins
```

### 4. Create Shard Index File

Create `{chapter-name}-shards-index.md` in the shard directory:

```markdown
# Chapter 7 Shards Index

**Original File**: chapter-7-advanced-queries.md
**Total Pages**: 32
**Shard Count**: 6
**Split Date**: 2025-10-26
**Sharding Strategy**: Hybrid (heading + size limit)

## Purpose

This chapter has been sharded for easier editing and review. Each shard contains 5-10 pages of content with logical section boundaries preserved.

## Shards

1. **chapter-7-shard-1.md** - Introduction and Prerequisites (pages 1-6)
   - Sections: Introduction, Setting Up the Environment
   - Code files: setup.sql, config.json

2. **chapter-7-shard-2.md** - Complex Joins (pages 7-12)
   - Sections: Inner Joins, Outer Joins, Cross Joins
   - Code files: joins-example.sql

3. **chapter-7-shard-3.md** - Subqueries and CTEs (pages 13-17)
   - Sections: Subqueries, Common Table Expressions
   - Code files: cte-examples.sql

4. **chapter-7-shard-4.md** - Window Functions (pages 18-23)
   - Sections: Window Function Basics, Advanced Window Functions
   - Code files: window-functions.sql

5. **chapter-7-shard-5.md** - Performance Optimization (pages 24-29)
   - Sections: Query Planning, Indexes, EXPLAIN ANALYZE
   - Code files: optimization.sql

6. **chapter-7-shard-6.md** - Summary and Exercises (pages 30-32)
   - Sections: Chapter Summary, Practice Exercises
   - Code files: exercises.sql

## Cross-References

### References Spanning Shards

- Shard 3 references join syntax from Shard 2
- Shard 5 optimization examples use CTEs from Shard 3
- Exercise 4 (Shard 6) requires window functions from Shard 4

## Reassembly

To reassemble the chapter:

1. Use task: merge-chapter-shards.md
2. Or manually concatenate shards in order (remove metadata headers)
3. Validate merged content matches original

## Working with Shards

**Editing a shard:**

1. Edit the specific shard file
2. Note changes in this index if significant
3. Update Split Date when modified

**Adding content:**

- If shard grows beyond 12 pages, consider re-sharding
- Update page counts in metadata and index

**Version control:**

- Commit shards individually for granular history
- Tag major milestones (e.g., "chapter-7-draft-complete")
```

### 5. Validate Shards

**Content validation checklist:**

- [ ] All content from original chapter present in shards
- [ ] No duplicate content across shards
- [ ] No missing paragraphs, code blocks, or sections
- [ ] All code blocks properly fenced (```)
- [ ] All tables complete and formatted
- [ ] All images/diagrams referenced
- [ ] Metadata headers present in all shards
- [ ] Shard index file complete and accurate

**Formatting validation:**

- [ ] Heading levels consistent
- [ ] Code block language tags preserved
- [ ] Lists properly formatted
- [ ] Blockquotes intact
- [ ] Cross-references preserved

**Quick validation method:**

1. Check original page count vs. sum of shard page ranges
2. Search for unique phrases in both original and shards
3. Verify all ## headings accounted for
4. Check shard count matches index

### 6. Document Cross-References

Identify and document references spanning shards:

**In the shard content:**

Add note when referencing content in another shard:

```markdown
As we learned in Section 2 (see shard 2), inner joins...
```

**In the index file:**

List major cross-references:

```markdown
## Cross-References

- Shard 4 references authentication setup from Shard 2
- Exercise 3 (Shard 6) builds on API design from Shard 3
```

**Benefits:**

- Reviewers know when to reference other shards
- Writers can identify dependencies
- Helps during reassembly

### 7. Organize Shard Directory

Create organized directory structure:

```
manuscript/chapters/
├── chapter-7-advanced-queries.md           # Original (keep as backup)
├── chapter-7-shards/
│   ├── chapter-7-shards-index.md           # Index/navigation
│   ├── chapter-7-shard-1.md
│   ├── chapter-7-shard-2.md
│   ├── chapter-7-shard-3.md
│   ├── chapter-7-shard-4.md
│   ├── chapter-7-shard-5.md
│   └── chapter-7-shard-6.md
└── chapter-8-transactions.md
```

**Best practices:**

- Keep original chapter file as backup
- Put all shards in dedicated subdirectory
- Include index file for easy navigation
- Use consistent naming convention

## Output

The completed sharding produces:

**Shard files:**

- Format: Markdown (.md)
- Location: `manuscript/chapters/{chapter-name}-shards/`
- Naming: `{chapter-name}-shard-{n}.md`
- Count: Based on chapter size and strategy
- Size: 5-10 pages per shard (target)

**Index file:**

- Filename: `{chapter-name}-shards-index.md`
- Contains: Shard list, page ranges, sections, cross-references
- Purpose: Navigation and reassembly guide

## Quality Standards

A well-sharded chapter has:

✓ Logical split points at section boundaries
✓ Consistent shard sizes (5-10 pages)
✓ Complete shard metadata headers
✓ Comprehensive shard index file
✓ All original content preserved
✓ No split code blocks or tables
✓ Cross-references documented
✓ Clear naming convention followed

## Common Pitfalls

Avoid these mistakes:

❌ **Splitting inside code blocks** - Always keep code blocks intact
❌ **Uneven shard sizes** - Aim for 5-10 pages, not 2 and 20
❌ **Missing metadata** - Every shard needs metadata header
❌ **No index file** - Index is essential for navigation
❌ **Splitting mid-paragraph** - Always split at heading boundaries
❌ **Modifying content** - Sharding is extraction only, not editing
❌ **Losing cross-references** - Document references spanning shards

## Sharding Best Practices

**Planning:**

- Analyze structure before splitting
- Choose split points carefully
- Document your strategy

**Execution:**

- Use consistent naming
- Add complete metadata
- Preserve all formatting

**Validation:**

- Check content completeness
- Verify formatting integrity
- Test cross-references

**Organization:**

- Create dedicated shard directory
- Keep original as backup
- Maintain clear index file

## Troubleshooting

**Problem: Section too large (15+ pages), but no good ### split point**

- Solution: Split at a natural paragraph break and note in metadata

**Problem: Code block contains ## in example**

- Solution: Properly parse markdown - ## inside ``` is not a heading

**Problem: Cross-reference becomes unclear after sharding**

- Solution: Add clarifying note in shard: "(see shard 3, Section 4.2)"

**Problem: Shard sizes very uneven**

- Solution: Re-evaluate split points, use hybrid strategy

**Problem: Lost content during sharding**

- Solution: Validate against original, search for unique phrases

## Next Steps

After sharding the chapter:

1. Review shard index for accuracy
2. Share specific shards with reviewers/editors
3. Work on shards independently
4. When ready to publish, use merge-chapter-shards.md task
5. Validate merged chapter matches original intent

## Related Resources

- Task: merge-chapter-shards.md - Reassemble shards into complete chapter
- Task: write-chapter-draft.md - Creating chapter content
- Task: technical-review-chapter.md - Reviewing specific shards
- Core: shard-doc.md - General document sharding (using md-tree)
