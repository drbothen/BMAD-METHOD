<!-- Powered by BMAD™ Core -->

# Analyze Existing Book

---

task:
id: analyze-existing-book
name: Analyze Existing Technical Book
description: Deep analysis of existing book state to inform revision planning
persona_default: book-analyst
inputs: - existing_book_path - revision_motivation (why analyze now?)
steps: - Scan all chapters and sections to understand book structure - Extract book metadata (title, version, publisher, audience, publication date) - Analyze structural organization (parts, chapters, sections, learning flow) - Inventory all code examples (count, languages, versions, complexity) - Identify technology versions currently used in book - Extract writing style patterns (voice, tone, heading styles, terminology) - Map cross-references and chapter dependencies - Assess technical currency (what's outdated, deprecated, or broken) - Identify inconsistencies, gaps, or quality issues - Use template book-analysis-report-tmpl.yaml with create-doc.md task - Generate comprehensive analysis report
output: docs/analysis/{{book_title}}-analysis-report.md

---

## Purpose

This task provides a systematic approach to analyzing an existing technical book before planning revisions. The analysis report becomes the foundation for all brownfield work (2nd editions, version updates, chapter additions, feedback incorporation).

## Prerequisites

Before starting this task:

- Have access to complete current book content (all chapters)
- Know why you're analyzing (new edition? version update? publisher request?)
- Understand the target audience and original publication goals
- Have access to code repository if one exists

## Workflow Steps

### 1. Scan Book Structure

Read through the entire book to understand:

- Total chapter count
- Part/section organization (if applicable)
- Front matter (preface, introduction, how to use this book)
- Back matter (appendices, glossary, index)
- Overall organization pattern (tutorial-based? reference? project-driven?)

Document the table of contents structure completely.

### 2. Extract Book Metadata

Collect core information:

- Title and subtitle
- Author(s)
- Current edition/version (1st, 2nd, 3rd)
- Publication date (original and current edition if different)
- Publisher (PacktPub, O'Reilly, Manning, Self-published)
- Target audience (skill level, role, prerequisites)
- Current page count
- ISBN or product identifiers
- Technology stack and versions

### 3. Analyze Structural Organization

Evaluate the book's architecture:

- How are chapters grouped? (By difficulty? By topic? By project?)
- Is there a clear learning progression?
- Do chapters build on each other sequentially?
- Are there standalone chapters that can be read independently?
- Is the structure appropriate for the content?
- Does the organization match publisher best practices?

### 4. Inventory Code Examples

Catalog all code comprehensively:

- Count total code examples
- List programming languages used (Python, JavaScript, Go, etc.)
- Document technology versions targeted (Python 3.9, Node 16, React 17)
- List frameworks and libraries used
- Assess code testing status (Is code tested? CI/CD? Manual only?)
- Note code repository location (GitHub, GitLab, book companion site)
- Categorize example complexity (simple snippets vs. complete projects)
- Identify code dependencies between chapters

### 5. Identify Technology Versions

For each technology mentioned in the book:

- Document current version in book
- Find latest stable version available
- Identify breaking changes since book publication
- Note deprecated features used in book
- Flag security vulnerabilities in examples
- Assess migration effort (minor updates vs. major rewrites)

### 6. Extract Writing Style Patterns

Learn the book's conventions:

- Voice and tone (conversational vs. formal, friendly vs. academic)
- Structural patterns (typical chapter flow: intro→concept→example→exercise?)
- Heading hierarchy style (action-based? question-based? topic-based?)
- Terminology choices (consistent? any jargon defined?)
- Code comment style (inline comments? docstrings? minimal?)
- Callout usage (tips, warnings, notes - frequency and style)
- Cross-reference patterns ("see Chapter X", "as discussed in Section Y.Z")

This pattern extraction is critical for maintaining consistency in revisions.

### 7. Map Cross-References and Dependencies

Document internal dependencies:

- Which chapters reference other chapters?
- What's the prerequisite flow? (must read Chapter X before Chapter Y)
- Which concepts depend on earlier concepts?
- Do any code examples build on previous examples?
- Are there forward references? ("we'll cover this in Chapter 7")
- Are there backward references? ("as we learned in Chapter 4")

Create a dependency diagram if helpful.

### 8. Assess Technical Currency

Evaluate how current the content is:

- Which sections use outdated technology versions?
- What APIs or methods are now deprecated?
- Are there breaking changes that make examples fail?
- Are security best practices current?
- Is terminology up-to-date?
- Are there discontinued tools or frameworks?
- Do examples follow current best practices?

Flag specific chapters/sections needing updates.

### 9. Identify Issues and Gaps

List problems discovered:

- Outdated sections (specific locations)
- Broken code examples (won't run on current versions)
- Inconsistencies (terminology, formatting, style variations)
- Coverage gaps (missing important topics)
- Missing deprecated warnings
- Technical inaccuracies or errors
- Unclear explanations
- Unstated assumptions or prerequisites

Be specific: note chapter and section numbers.

### 10. Generate Analysis Report

Use the create-doc.md task with book-analysis-report-tmpl.yaml template to create the structured analysis document.

The report should include all findings from steps 1-9, organized into clear sections.

### 11. Make Recommendations

Based on analysis, provide actionable guidance:

- Priority updates (critical, important, nice-to-have)
- Scope suggestions (full 2nd edition? targeted updates? version migration?)
- Timeline estimates (weeks/months for different scope levels)
- Risk assessment (what could go wrong?)
- Testing strategy recommendations
- Learning flow impact considerations
- Publisher communication needs

## Success Criteria

A completed book analysis should have:

- [ ] Complete structural understanding of existing book
- [ ] Metadata fully documented
- [ ] Code inventory complete with version information
- [ ] Technical currency assessment for all technologies
- [ ] Writing style patterns extracted
- [ ] Cross-reference map created
- [ ] All issues and gaps identified with specific locations
- [ ] Recommendations provided with priorities
- [ ] Analysis report generated and saved
- [ ] Report ready to inform revision planning

## Common Pitfalls to Avoid

- **Rushing the analysis**: Take time to read thoroughly, don't skim
- **Missing code inventory**: Must catalog ALL examples, not just major ones
- **Ignoring style patterns**: Pattern extraction is critical for consistency
- **Vague issue identification**: Be specific with chapter/section numbers
- **No prioritization**: Not all issues are equal - categorize by severity
- **Skipping cross-references**: Dependencies affect revision planning

## Next Steps

After completing the book analysis:

1. Review analysis report with stakeholders (author, publisher)
2. Use analysis to plan revision (plan-book-revision.md task)
3. Extract code patterns if planning code updates (extract-code-patterns.md)
4. Begin revision planning with clear understanding of current state
