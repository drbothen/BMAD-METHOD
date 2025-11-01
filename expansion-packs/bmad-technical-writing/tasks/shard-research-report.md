<!-- Powered by BMAD™ Core -->

# Shard Research Report

---

task:
id: shard-research-report
name: Shard Research Report
description: Break 30+ page research reports into manageable sections for easier editing and focused review within AI context limits
persona_default: technical-researcher
inputs: - research-report-file-path - target-shard-size
steps: - Analyze research report structure and identify optimal split points - Determine sharding strategy (by template section, by size, or hybrid) - Create shard files with proper naming and metadata - Generate comprehensive shard index file with cross-references - Validate all research content preserved (citations, code examples, expert insights) - Document cross-references between findings and sources
output: Multiple shard files in {topic}-shards/ directory with comprehensive index file

---

## Purpose

This task breaks large research reports (30+ pages) into smaller, manageable shards (5-10 pages each) to:

- Work within AI context window limits during editing
- Enable focused review of specific research areas
- Allow parallel work on different research sections
- Improve version control granularity
- Make extensive research findings easier to navigate
- Maintain citation and source integrity across shards

## When to Use This Task

**Shard a research report when:**

- Research report exceeds 30 pages
- Context window limits are being hit during editing
- Extensive citations span multiple research areas
- Multiple writers need to work on different research sections
- Focused review of specific findings is needed
- Large research report causes performance issues in editor

**Don't shard when:**

- Research report is under 30 pages
- Report has simple structure (1-2 major research areas)
- No collaboration or context issues exist
- Citations and cross-references are minimal

## Prerequisites

Before sharding:

- Research report exists and follows `book-research-report-tmpl.yaml` structure
- Report has proper section headings (##, ###, ####)
- All code blocks properly fenced with ``` markers
- All source citations complete with URLs and access dates
- Research content is saved and backed up

## Workflow Steps

**Note:** This task references config paths (e.g., {{config.manuscript.*}}). Load `.bmad-technical-writing/config.yaml` at the start to resolve these paths, or use defaults: `manuscript/{type}`, `code-examples`.

### 1. Analyze Research Report Structure

Understand the research report's organization:

**Read the entire report to identify:**

- Total page count (estimate 500-1000 tokens per page)
- Number and distribution of ## headings (major sections per template):
  - Research Context
  - Research Questions & Answers
  - Technical Findings
  - Code Examples Discovered
  - Expert Insights Captured
  - Integration into Chapter Outline
  - Additional Resources & Bibliography
  - Research Notes & Observations
- Location of code blocks, citation lists, expert quotes
- Complex multi-line content that shouldn't be split

**Calculate optimal shard count:**

- Target shard size: 5-10 pages
- Formula: `shard_count = ceil(total_pages / 5)`
- Example: 35-page research report → 7 shards of ~5 pages each

**Document structure findings:**

```
Research Report Analysis:
- Total pages: 35
- Major sections (##): 8 (following template structure)
- Research questions: 15
- Code examples: 8
- Expert quotes: 12
- Source citations: 40+
- Recommended shards: 6-7
```

### 2. Determine Split Points

Choose where to divide the research report using the **Hybrid Strategy** (preferred):

**Sharding Strategies:**

**A) By Template Section (Preferred):**

- Split at ## (major section) boundaries following template structure
- Preserves logical research organization
- Easy to understand shard boundaries
- May create uneven shard sizes

**B) By Size (Fallback):**

- Split when shard reaches target page count (10 pages maximum)
- Creates evenly-sized shards
- May split mid-section (less ideal)

**C) Hybrid (Best):**

- Prefer ## heading boundaries (template sections)
- But enforce maximum shard size (10 pages)
- Split at ### headings if section too large (e.g., many research questions)
- Never split mid-paragraph, mid-code-block, or mid-citation

**Rules for split points:**

1. **NEVER split:**
   - Mid-paragraph or mid-citation
   - Inside code blocks (```)
   - Inside citation lists
   - Inside expert quotes
   - Inside tables or diagrams
   - Mid-research question and answer pairs

2. **Prefer splitting at:**
   - ## (major section) headings per template structure
   - ### (subsection) headings when ## creates too-large shards
   - Natural topic boundaries within Research Questions section
   - Between code examples or expert insights

3. **Research-specific considerations:**
   - Keep related research questions together
   - Don't split citation chains referencing the same source
   - Keep code examples with their explanations
   - Keep expert quotes with full attribution and source

**Example split point plan:**

```
Shard 1: Pages 1-6 (Frontmatter + Research Context)
Shard 2: Pages 7-13 (Research Questions & Answers: Questions 1-8)
Shard 3: Pages 14-19 (Research Questions & Answers: Questions 9-15)
Shard 4: Pages 20-25 (Technical Findings + Code Examples)
Shard 5: Pages 26-31 (Expert Insights + Chapter Integration)
Shard 6: Pages 32-35 (Additional Resources + Research Notes)
```

### 3. Create Shard Files

For each determined split point, create a shard file:

**Naming convention:**

- Pattern: `{topic-slug}-shard-{n}.md`
- Example: `react-hooks-shard-1.md`, `react-hooks-shard-2.md`
- Use original research report filename base as topic slug
- Number sequentially starting at 1

**Shard metadata header:**

Add metadata at the top of each shard file:

```markdown
<!-- SHARD METADATA -->
<!-- Original: react-hooks-research-report.md -->
<!-- Shard: 1 of 6 -->
<!-- Sections: Frontmatter Metadata, Research Context -->
<!-- Split Date: 2025-10-26 -->
<!-- END METADATA -->

# React Hooks Research Report - Shard 1

## Frontmatter Metadata

[content...]

<!-- SHARD END -->
<!-- Continue to react-hooks-shard-2.md -->
```

**Content extraction:**

1. Extract content from original research report based on split points
2. Preserve ALL formatting exactly
3. Keep all citations intact with URLs and access dates
4. Include complete code blocks with explanations
5. Preserve expert quotes with full attribution
6. Keep cross-references intact (note if they point outside shard)
7. Don't modify content, only extract

**Adjust heading levels:**

- If shard starts mid-report (not at report title), NO adjustment needed
- Preserve original heading levels to maintain research report context
- Exception: If creating standalone shard docs, decrease all heading levels by 1

**Standard approach (preserve levels):**

```markdown
<!-- react-hooks-shard-2.md -->
<!-- SHARD METADATA -->
<!-- Original: react-hooks-research-report.md -->
<!-- Shard: 2 of 6 -->
<!-- Sections: Research Questions & Answers (Q1-Q8) -->
<!-- Split Date: 2025-10-26 -->
<!-- END METADATA -->

## Research Questions & Answers

### Technical Concepts

**Q: What is the React Hooks API and why was it introduced?**

A: [complete answer with citations...]

*Source: [React Hooks Documentation](https://react.dev/reference/react) (Official Docs) - Accessed 2025-10-25*

[... more content ...]

<!-- SHARD END -->
<!-- Continue to react-hooks-shard-3.md -->
```

### 4. Create Comprehensive Shard Index File

Create `{topic-slug}-shards-index.md` or `research-shards-index.md` in the shard directory:

```markdown
# React Hooks Research Report - Shards Index

**Original File**: react-hooks-research-report.md
**Total Pages**: 35
**Shard Count**: 6
**Split Date**: 2025-10-26
**Sharding Strategy**: Hybrid (template section + size limit)

## Purpose

This research report has been sharded for easier editing and focused review. Each shard contains 5-10 pages of content with logical section boundaries preserved.

## Research-Level Metadata

**Topic**: React Hooks API, useState, useEffect, custom hooks
**Research Method**: Manual web research
**Date Created**: 2025-10-20
**Related Chapters**: Chapter 5: Understanding React Hooks
**Target Audience**: Intermediate React developers
**Total Sources Cited**: 42 (15 official docs, 18 expert blogs, 9 community resources)

## Shards

1. **react-hooks-shard-1.md** - Frontmatter and Research Context (pages 1-6)
   - Sections: Frontmatter Metadata, Research Context
   - Key Content: Research objectives, scope, target audience
   - Sources: N/A (contextual)

2. **react-hooks-shard-2.md** - Research Questions Part 1 (pages 7-13)
   - Sections: Research Questions & Answers (Technical Concepts Q1-Q8)
   - Key Content: Hooks API rationale, rules of hooks, state management
   - Sources: 8 (official docs, React team blog posts)

3. **react-hooks-shard-3.md** - Research Questions Part 2 (pages 14-19)
   - Sections: Research Questions & Answers (Q9-Q15)
   - Key Content: useEffect behavior, custom hooks, performance
   - Sources: 10 (official docs, expert blogs)

4. **react-hooks-shard-4.md** - Technical Findings and Code Examples (pages 20-25)
   - Sections: Technical Findings, Code Examples Discovered
   - Key Content: 8 code examples with explanations
   - Sources: 12 (official docs, CodeSandbox examples, GitHub repos)

5. **react-hooks-shard-5.md** - Expert Insights and Chapter Integration (pages 26-31)
   - Sections: Expert Insights Captured, Integration into Chapter Outline
   - Key Content: Best practices, common pitfalls, chapter structure proposal
   - Sources: 8 (expert blogs, conference talks)

6. **react-hooks-shard-6.md** - Resources and Notes (pages 32-35)
   - Sections: Additional Resources & Bibliography, Research Notes & Observations
   - Key Content: Complete bibliography, unanswered questions, future research
   - Sources: 4 (additional reading materials)

## Cross-References

### References Spanning Shards

- Shard 3 (Q11) references code example from Shard 4 (Example 5: Custom useFetch hook)
- Shard 5 (Expert Insight #3) references research question from Shard 2 (Q4: Rules of hooks)
- Shard 5 (Chapter Integration) references findings from Shards 2, 3, and 4
- Shard 6 (Bibliography) contains all sources cited in Shards 2-5

### Citation Integrity Map

Documents which shards reference which sources (useful for source verification):

**Official React Documentation**:
- Referenced in: Shards 2, 3, 4

**Dan Abramov Blog Posts**:
- Referenced in: Shards 2, 3, 5

**Kent C. Dodds Articles**:
- Referenced in: Shards 3, 5

**Community Resources (Stack Overflow, GitHub)**:
- Referenced in: Shards 3, 4

**Code Example Repositories**:
- Referenced in: Shard 4

**Additional Reading (not directly cited)**:
- Listed in: Shard 6

## Reassembly

To reassemble the research report:

1. Use task: merge-chapter-shards.md (works for research reports too)
2. Or manually concatenate shards in order (remove metadata headers)
3. Validate merged content matches original
4. Verify all citations present and complete

## Working with Shards

**Editing a shard:**

1. Edit the specific shard file
2. Update Split Date in metadata when modified
3. Note significant changes in this index
4. Ensure citations remain intact if modifying research questions or findings

**Adding content:**

- If shard grows beyond 12 pages, consider re-sharding
- Update page counts in metadata and index
- Add new sources to Cross-Reference section

**Citation verification:**

- Use Citation Integrity Map to locate which shards use which sources
- Verify source URLs are still accessible
- Update access dates if re-checking sources

**Version control:**

- Commit shards individually for granular history
- Tag major milestones (e.g., "react-hooks-research-complete")
```

### 5. Validate Shards

**Content validation checklist:**

- [ ] All content from original research report present in shards
- [ ] No duplicate content across shards
- [ ] No missing paragraphs, code blocks, or citations
- [ ] All research questions and answers preserved
- [ ] All source citations intact with URLs and access dates
- [ ] All code examples complete with explanations
- [ ] All expert insights with quotes and attributions preserved
- [ ] All tables/diagrams referenced
- [ ] Metadata headers present in all shards
- [ ] Shard index file complete and accurate

**Research-specific validation:**

- [ ] Citation chains traceable across shards
- [ ] Expert quotes with full attribution preserved
- [ ] Code blocks properly fenced and complete
- [ ] Research methodology notes intact
- [ ] Cross-references between findings and sources documented
- [ ] Bibliography/resources section complete in final shard

**Formatting validation:**

- [ ] Heading levels consistent
- [ ] Code block language tags preserved
- [ ] Citation format consistent (URLs, dates, credibility notes)
- [ ] Lists properly formatted
- [ ] Blockquotes intact (for expert quotes)

**Quick validation method:**

1. Check original page count vs. sum of shard page ranges
2. Search for unique citations in both original and shards
3. Verify all ## headings accounted for
4. Check shard count matches index
5. Verify first and last citation present in shards

### 6. Document Cross-References

Identify and document cross-references spanning shards:

**In the shard content:**

Add note when referencing content in another shard:

```markdown
As noted in the Technical Findings section (see shard 4), useState is synchronous within render...

The code example for custom hooks (see shard 4, Example 5) demonstrates this pattern...
```

**In the index file:**

List major cross-references in the "Cross-References" section:

```markdown
## Cross-References

### Content References
- Shard 5 references code example from Shard 4 (Custom useFetch hook)
- Shard 5 chapter integration builds on findings from Shards 2, 3, 4

### Citation References
- Shard 3 and Shard 5 both cite Dan Abramov's "Complete Guide to useEffect"
- Shards 2, 3, 4 all reference official React documentation
```

**Benefits:**

- Reviewers know when to reference other shards
- Writers can identify research dependencies
- Helps during reassembly
- Facilitates citation verification

### 7. Organize Shard Directory

Create organized directory structure following expansion pack conventions:

```
{{config.manuscript.research}}/
├── react-hooks-research-report.md           # Original (keep as backup)
└── react-hooks-shards/
    ├── research-shards-index.md             # Index/navigation/cross-refs
    ├── react-hooks-shard-1.md               # Frontmatter + Context
    ├── react-hooks-shard-2.md               # Research Questions Part 1
    ├── react-hooks-shard-3.md               # Research Questions Part 2
    ├── react-hooks-shard-4.md               # Findings + Code Examples
    ├── react-hooks-shard-5.md               # Expert Insights + Integration
    └── react-hooks-shard-6.md               # Resources + Notes
```

**Best practices:**

- Keep original research report file as backup
- Put all shards in dedicated subdirectory named `{topic}-shards/`
- Include comprehensive index file for navigation and cross-references
- Use consistent naming convention
- Follow expansion pack directory structure (`{{config.manuscript.research}}/`)

## Output

The completed sharding produces:

**Shard files:**

- Format: Markdown (.md)
- Location: `{{config.manuscript.research}}/{topic}-shards/`
- Naming: `{topic-slug}-shard-{n}.md`
- Count: Based on research report size and strategy
- Size: 5-10 pages per shard (target)
- Content: Preserves all research questions, citations, code examples, expert insights

**Shard metadata:**

Each shard file includes metadata at the top and bottom:

**Header metadata:**
- Original filename
- Shard number (N of M)
- Sections included
- Split date

**Footer metadata:**
- SHARD END marker
- Continuation pointer to next shard

**Index file:**

- Filename: `research-shards-index.md` or `{topic}-shards-index.md`
- Contains: Research-level metadata, shard list with descriptions, cross-reference documentation, citation integrity map
- Purpose: Navigation, reassembly guide, source verification

## Quality Standards

A well-sharded research report has:

✓ Logical split points at template section boundaries
✓ Consistent shard sizes (5-10 pages)
✓ Complete shard metadata headers
✓ Comprehensive shard index file with cross-references
✓ All original research content preserved
✓ No split code blocks, citations, or expert quotes
✓ Citation integrity maintained across shards
✓ Cross-references documented (findings → sources)
✓ Clear naming convention followed

## Common Pitfalls

Avoid these mistakes specific to research reports:

❌ **Splitting citation chains** - Keep related citations together with their context
❌ **Losing source context** - Preserve full citations with URLs, dates, credibility notes
❌ **Breaking research question pairs** - Keep Q&A together, don't split mid-answer
❌ **Splitting code examples** - Keep code blocks with their explanations
❌ **Fragmenting expert quotes** - Preserve complete quotes with attribution and source
❌ **Missing metadata** - Every shard needs metadata header
❌ **No cross-reference documentation** - Index must map which shards reference which sources
❌ **Incomplete bibliography** - Ensure all sources cited in shards appear in bibliography shard
❌ **Splitting mid-citation list** - Keep bibliography entries intact

## Troubleshooting

**Problem: Research Questions section too large (15+ pages), but no good split point**

- Solution: Split by question groups (e.g., "Technical Concepts" vs "Learning Progression")
- Note split strategy in metadata: "Research Questions Part 1 (Q1-Q8)"

**Problem: Citation references become unclear after sharding**

- Solution: Add clarifying note: "(see shard 4, Code Example 5)" or "Source cited in shard 6 bibliography"
- Document in index Cross-References section

**Problem: Expert quote split from its attribution**

- Solution: Treat quote + attribution + source as atomic unit, never split
- If section too large, split between different quotes, not within

**Problem: Bibliography section is large but must stay in one shard**

- Solution: Keep complete bibliography together even if 12+ pages
- This is acceptable for the final shard containing Additional Resources

**Problem: Lost citation URLs or access dates during sharding**

- Solution: Validate against original, search for unique source titles
- Use Citation Integrity Map in index to verify all sources accounted for

**Problem: Cross-references between Technical Findings and Code Examples broken**

- Solution: Add explicit notes in both shards referencing each other
- Document major cross-references in index file

## Sharding Best Practices

**Planning:**

- Analyze structure before splitting
- Choose split points carefully at template section boundaries
- Document your strategy in the index

**Execution:**

- Use consistent naming convention
- Add complete metadata headers to every shard
- Preserve all formatting exactly

**Validation:**

- Check content completeness against original
- Verify citation integrity across all shards
- Test cross-references work correctly

**Organization:**

- Create dedicated shard directory
- Keep original as backup
- Maintain comprehensive index file with cross-references

## Next Steps

After sharding the research report:

1. Review shard index for accuracy and completeness
2. Verify Citation Integrity Map covers all sources
3. Share specific shards with reviewers (e.g., only code examples shard)
4. Work on shards independently during chapter writing
5. Reference appropriate shards when drafting chapter sections
6. When ready to archive, use merge-chapter-shards.md task if needed
7. Keep shards for ongoing research updates

## Related Resources

- Task: merge-chapter-shards.md - Reassemble shards into complete report (if needed)
- Task: shard-large-chapter.md - Similar sharding for chapter manuscripts
- Task: shard-book-outline.md - Sharding book outlines for parallel development
- Core: shard-doc.md - General document sharding (using md-tree)
- Template: book-research-report-tmpl.yaml - Source document structure
