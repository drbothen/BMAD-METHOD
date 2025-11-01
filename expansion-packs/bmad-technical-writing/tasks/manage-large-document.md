<!-- Powered by BMAD™ Core -->

# Manage Large Document

---

task:
id: manage-large-document
name: Manage Large Document
description: Comprehensive strategies for handling 500+ page books and massive reference guides
persona_default: book-publisher
inputs: - project-scope - team-size - timeline
steps: - Assess document scale and determine organizational approach - Choose sharding strategy appropriate to project size - Design directory structure for large-scale project - Establish version control practices - Plan parallel development workflow (if multiple authors) - Implement context management techniques - Define quality assurance approach at scale - Create milestone tracking system
output: Large document management plan and project structure

---

## Purpose

This task provides strategic guidance for managing large-scale technical writing projects:

- Books exceeding 500 pages
- Comprehensive reference guides (1000+ pages)
- Multi-author documentation projects
- Long-term writing projects (6-12+ months)
- Complex technical content requiring systematic organization

## When to Use This Task

**Use this task when:**

- Starting a 500+ page book project
- Managing multi-author documentation
- Experiencing context/organizational issues with large project
- Planning long-term technical writing initiative
- Need systematic approach to scale

**Applicable to:**

- Technical books (O'Reilly, Manning, PacktPub scale)
- Comprehensive reference guides
- Large-scale API documentation
- Multi-volume series
- Enterprise documentation projects

## Large Document Challenges

### Scale-Specific Problems

**Context Window Limits:**

- Problem: AI tools can't process 500-page document at once
- Impact: Can't review/edit full book context
- Solution: Shard into manageable units, work incrementally

**Consistency Across Hundreds of Pages:**

- Problem: Terminology, style, tone drift over long projects
- Impact: Inconsistent reader experience
- Solution: Glossaries, style guides, systematic reviews

**Cross-References Across Many Chapters:**

- Problem: "See Chapter 7" but which section in 30-page chapter?
- Impact: Reader frustration, broken references
- Solution: Detailed cross-reference system, validation tools

**Long Development Cycles:**

- Problem: 6-12 month projects, technology changes mid-project
- Impact: Content becomes outdated before publication
- Solution: Incremental releases (MEAP), version planning

**Multiple Contributors:**

- Problem: Coordinating 3-5 authors on different chapters
- Impact: Merge conflicts, inconsistent quality
- Solution: Chapter ownership, merge protocols, standards

**Overwhelming Scope:**

- Problem: Writer paralysis from massive project
- Impact: Slow progress, procrastination
- Solution: Break into milestones, celebrate incremental wins

## When to Shard Documents

### Sharding Thresholds

**Chapter-level sharding:**

- Trigger: Chapter exceeds 30 pages
- Task: shard-large-chapter.md
- Creates: 5-10 page shards
- Benefit: Easier focused editing

**Outline-level sharding:**

- Trigger: Book outline exceeds 100 pages or 20+ chapters
- Task: shard-book-outline.md
- Creates: Per-chapter outline files
- Benefit: Parallel chapter planning

**General document sharding:**

- Trigger: Any document > 50 pages causing context issues
- Task: shard-doc.md (BMAD Core)
- Creates: Section-based shards
- Benefit: Manageable work units

### Sharding Decision Matrix

| Document Type | Size          | Shard? | Strategy                        |
| ------------- | ------------- | ------ | ------------------------------- |
| Chapter       | < 30 pages    | No     | Keep as single file             |
| Chapter       | 30-50 pages   | Maybe  | If context issues arise         |
| Chapter       | 50+ pages     | Yes    | shard-large-chapter.md          |
| Book Outline  | < 20 chapters | No     | Single file sufficient          |
| Book Outline  | 20+ chapters  | Yes    | shard-book-outline.md           |
| Reference Doc | < 50 pages    | No     | Single file                     |
| Reference Doc | 50-100 pages  | Maybe  | Use shard-doc.md if needed      |
| Reference Doc | 100+ pages    | Yes    | shard-doc.md or manual sharding |

## Organizational Strategies

### 1. Part-Based Organization

Best for: Books with clear part divisions (400-800 pages)

**Structure:**

```
{{config.manuscript.root}}/
├── book-outline-index.md
├── book-level-info.md
├── part-1-foundations/
│   ├── chapter-1-introduction.md
│   ├── chapter-2-prerequisites.md
│   ├── chapter-3-setup.md
│   └── chapter-4-first-app.md
├── part-2-core-concepts/
│   ├── chapter-5-architecture.md
│   ├── chapter-6-data-modeling.md
│   └── ...
├── part-3-advanced/
│   └── ...
├── part-4-production/
│   └── ...
└── assembled/
    ├── part-1-complete.md     # Optional: assembled parts
    ├── part-2-complete.md
    └── full-book.md           # Only for final review
```

**Advantages:**

- Logical grouping by learning progression
- Easy to navigate
- Natural milestone boundaries
- Can publish parts incrementally (MEAP style)

**Disadvantages:**

- Requires well-defined part structure
- Rearranging chapters between parts is cumbersome

### 2. Chapter-Based Organization (Recommended)

Best for: Most technical books (300-800 pages)

**Structure:**

```
{{config.manuscript.root}}/
├── book-outline-index.md
├── book-level-info.md
├── chapters/
│   ├── chapter-01-introduction.md
│   ├── chapter-02-setup.md
│   ├── chapter-03-fundamentals.md
│   ├── chapter-04-data-types.md
│   ├── ...
│   ├── chapter-25-conclusion.md
│   └── large-chapters/                # Sharded chapters
│       ├── chapter-12-shards/
│       │   ├── chapter-12-shards-index.md
│       │   ├── chapter-12-shard-1.md
│       │   └── ...
│       └── chapter-18-shards/
│           └── ...
├── outlines/                          # Chapter outlines
│   ├── chapter-01-outline.md
│   ├── chapter-02-outline.md
│   └── ...
├── {{config.codeExamples.root}}/                     # Organized by chapter
│   ├── chapter-03/
│   ├── chapter-04/
│   └── ...
└── assets/
    ├── diagrams/
    └── screenshots/
```

**Advantages:**

- One file per chapter (simple)
- Easy to find chapters
- Natural for version control
- Flexible chapter ordering

**Disadvantages:**

- Large chapters may still need sharding
- Less obvious part/section organization

### 3. Section-Based Organization

Best for: Massive reference guides (1000+ pages)

**Structure:**

```
{{config.manuscript.root}}/
├── reference-index.md
├── 01-getting-started/
│   ├── installation.md
│   ├── configuration.md
│   └── first-steps.md
├── 02-core-concepts/
│   ├── architecture.md
│   ├── data-model.md
│   ├── queries.md
│   └── transactions.md
├── 03-api-reference/
│   ├── api-overview.md
│   ├── authentication-api.md
│   ├── users-api.md
│   ├── orders-api.md
│   └── ...               # 50+ API sections
├── 04-advanced-topics/
│   └── ...
└── appendices/
    ├── appendix-a-troubleshooting.md
    └── ...
```

**Advantages:**

- Extremely granular (5-10 page sections)
- Excellent for reference material
- Easy to update individual sections
- Perfect for parallel development

**Disadvantages:**

- Many files to manage
- Harder to see overall structure
- May need secondary navigation

### 4. Hybrid Organization

Best for: Complex projects with varied content types

**Structure:**

```
{{config.manuscript.root}}/
├── book-info/
│   ├── book-level-info.md
│   ├── book-outline-index.md
│   └── glossary.md
├── front-matter/
│   ├── preface.md
│   └── introduction.md
├── tutorial-chapters/          # Narrative chapters
│   ├── chapter-01-intro.md
│   ├── chapter-02-setup.md
│   └── ...
├── reference-sections/         # Reference material
│   ├── api-reference/
│   ├── configuration-guide/
│   └── troubleshooting/
├── exercises-and-solutions/
│   ├── chapter-01-exercises.md
│   └── ...
├── {{config.codeExamples.root}}/
└── back-matter/
    ├── appendix-a.md
    └── index.md
```

**Advantages:**

- Optimized structure per content type
- Very flexible
- Supports complex projects

**Disadvantages:**

- More complex to navigate
- Requires clear documentation
- Steeper learning curve

## Version Control Best Practices

### Granular Commits

**Good commit strategy:**

```bash
# Commit per chapter or section
git add chapters/chapter-07-queries.md
git commit -m "feat(ch7): add window functions section"

# Commit per major milestone
git add chapters/chapter-*.md
git commit -m "feat: complete Part 2 draft (chapters 6-10)"

# Commit code examples separately
git add {{config.codeExamples.root}}/chapter-07/
git commit -m "code(ch7): add window function examples"
```

**Benefits:**

- Easy to review changes
- Simple to revert specific chapters
- Clear project history
- Granular blame/attribution

### Branching Strategy

**For single author:**

```
main                 # Published/stable version
├── draft           # Current draft work
└── revision-v2     # Major revision branch
```

**For multiple authors:**

```
main                 # Published/stable version
├── draft           # Integration branch
├── chapter-7-jane  # Jane working on Chapter 7
├── chapter-8-bob   # Bob working on Chapter 8
└── chapter-9-alice # Alice working on Chapter 9
```

**Workflow:**

1. Create branch per chapter
2. Author works independently
3. Merge to draft when chapter complete
4. Review and integration testing
5. Merge draft to main for publication

### Milestone Tagging

Tag major milestones:

```bash
# Outline complete
git tag -a v0.1-outline-complete -m "Complete book outline"

# Part 1 draft complete
git tag -a v0.2-part1-draft -m "Part 1 chapters 1-5 draft complete"

# Full draft complete
git tag -a v1.0-draft-complete -m "Complete manuscript draft"

# Technical review complete
git tag -a v1.1-tech-review -m "Incorporated technical review feedback"

# Production ready
git tag -a v2.0-production -m "Final manuscript for publication"
```

**Benefits:**

- Easy to roll back to milestone
- Track major achievements
- Reference specific versions
- Useful for incremental publishing (MEAP)

## Parallel Development Workflow

### Multiple Writers on Same Book

**Chapter Ownership Model (Recommended):**

1. **Assign chapter ownership:**

   ```
   Jane: Chapters 1-5, 11-15
   Bob: Chapters 6-10
   Alice: Chapters 16-20, Appendices
   ```

2. **Each writer works in own branch:**

   ```bash
   # Jane
   git checkout -b jane-chapters-1-5

   # Bob
   git checkout -b bob-chapters-6-10

   # Alice
   git checkout -b alice-chapters-16-20
   ```

3. **Merge chapters when complete:**

   ```bash
   # Jane completes Chapter 3
   git checkout draft
   git merge jane-chapters-1-5 --no-ff
   ```

4. **Coordination:**
   - Weekly sync meetings
   - Shared style guide
   - Common glossary
   - Cross-chapter review

**Parallel Section Development:**

For reference guides with many independent sections:

1. **Use section-based organization**
2. **Writers claim sections:**
   ```
   Jane: API Authentication sections
   Bob: API Users and Orders sections
   Alice: API Admin sections
   ```
3. **Minimal merge conflicts** (different files)
4. **Independent progress**

### Merge Protocols

**Before merging chapters:**

1. Self-review against checklist
2. Spell check and grammar check
3. Test all code examples
4. Validate cross-references
5. Request peer review

**Merge process:**

1. Create pull request
2. Peer review (different author)
3. Address feedback
4. Technical lead approval
5. Merge to integration branch

**Conflict resolution:**

- Glossary conflicts: Lead author decides
- Style conflicts: Follow style guide
- Technical conflicts: Technical reviewer decides
- Cross-reference conflicts: Update references

## Context Management Techniques

### Work Incrementally

**Instead of loading full book:**

1. Load single chapter
2. Load relevant dependencies (previous chapter, glossary)
3. Work on focused task (write one section)
4. Save and commit
5. Move to next chapter/section

**Benefits:**

- Stay within AI context limits
- Maintain focus
- Reduce cognitive load

### Use Summaries for Cross-Chapter Context

**Create chapter summaries:**

```markdown
# Chapter 7 Summary (for cross-reference)

**Main Topics:**

- Complex JOINs (inner, outer, cross, self)
- Subqueries and CTEs
- Window functions

**Key Examples:**

- `join-examples.sql`: All join types
- `cte-hierarchy.sql`: Recursive CTE for org chart
- `window-ranking.sql`: ROW_NUMBER, RANK, DENSE_RANK

**Important Sections:**

- Section 7.2.3: Join Performance (referenced by Ch 8)
- Section 7.4: Window Functions (referenced by Ch 12, 18)

**Terminology Introduced:**

- Common Table Expression (CTE)
- Window Frame
- Partition
```

**Use summaries when:**

- Writing chapter that references previous chapters
- Need context without full chapter reload
- Reviewing cross-references
- Coordinating between authors

### Assemble Only When Needed

**Don't assemble full book unless:**

- Final review before publication
- Checking overall flow/transitions
- Generating table of contents
- Formatting for publisher

**Work with parts instead:**

- Review Part 1 (chapters 1-5) as unit
- Review Part 2 separately
- Final assembly only at end

## Quality Assurance at Scale

### Chapter-Level QA (Primary)

**QA each chapter independently:**

1. Technical review: `technical-review-chapter.md`
2. Copy edit: `copy-edit-chapter.md`
3. Code testing: `test-{{config.codeExamples.root}}.md`
4. Cross-reference check: `validate-cross-references.md`

**Benefits:**

- Focused reviews
- Parallel QA by multiple reviewers
- Easier to manage feedback
- Incremental quality improvement

### Part-Level Integration QA

**QA assembled parts:**

1. Assemble Part 1 (chapters 1-5)
2. Review part flow and transitions
3. Check consistency across part
4. Validate prerequisites build properly

**Focus areas:**

- Chapter transitions
- Terminology consistency within part
- Learning progression across part
- No duplicate content

### Full-Book QA (Final Only)

**Reserve for final review:**

1. Assemble complete book
2. Read cover-to-cover
3. Check global consistency
4. Verify cross-references across all chapters
5. Final editorial pass

**Timing:**

- After all chapters individually reviewed
- After part-level integration complete
- Before sending to publisher

### Systematic Checklist Usage

**Per chapter:**

- chapter-completeness-checklist.md
- code-quality-checklist.md
- technical-accuracy-checklist.md

**Per part:**

- part-consistency-checklist.md (custom)
- learning-progression-checklist.md

**Full book:**

- book-completeness-checklist.md
- cross-reference-validation-checklist.md
- style-consistency-checklist.md

## Milestone Tracking System

### Project Phases

**Phase 1: Planning (Months 1-2)**

- [ ] Book outline complete (all chapters)
- [ ] Target audience defined
- [ ] Chapter authors assigned (if multi-author)
- [ ] Style guide created
- [ ] Glossary started
- [ ] Code repository structure established

**Phase 2: Drafting (Months 3-7)**

- [ ] Part 1 draft complete (chapters 1-5)
- [ ] Part 2 draft complete (chapters 6-10)
- [ ] Part 3 draft complete (chapters 11-15)
- [ ] Part 4 draft complete (chapters 16-20)
- [ ] Part 5 draft complete (chapters 21-25)
- [ ] All code examples written and tested
- [ ] All diagrams created

**Phase 3: Review (Months 8-9)**

- [ ] Technical review complete (all chapters)
- [ ] Beta reader feedback received
- [ ] Revisions based on technical review
- [ ] Code examples updated for latest versions
- [ ] Cross-references validated

**Phase 4: Editorial (Months 10-11)**

- [ ] Copy edit complete
- [ ] Editorial feedback addressed
- [ ] Final code testing
- [ ] Screenshots and diagrams finalized
- [ ] Formatting for publisher

**Phase 5: Production (Month 12)**

- [ ] Final manuscript submitted
- [ ] Publisher production review
- [ ] Final corrections
- [ ] Publication

### Progress Tracking

**Use index file status table:**

```markdown
## Chapter Status

| Ch  | Title | Outline | Draft       | Tech Review | Copy Edit   | Final |
| --- | ----- | ------- | ----------- | ----------- | ----------- | ----- |
| 1   | Intro | ✓       | ✓           | ✓           | ✓           | ✓     |
| 2   | Setup | ✓       | ✓           | ✓           | In Progress | -     |
| 3   | SQL   | ✓       | ✓           | In Progress | -           | -     |
| 4   | Types | ✓       | In Progress | -           | -           | -     |
| 5   | Index | ✓       | Not Started | -           | -           | -     |

...
```

**Benefits:**

- Visual progress overview
- Identify bottlenecks
- Coordinate reviews
- Celebrate milestones

## Strategies for Specific Challenges

### Challenge: Maintaining Consistency Across 500 Pages

**Solutions:**

1. **Comprehensive Glossary:**

   ```markdown
   # Glossary

   **database**: Lowercase, unless part of product name (PostgreSQL Database)
   **table**: Not "relation" (use consistently)
   **PRIMARY KEY**: Uppercase when referring to SQL keyword
   **primary key**: Lowercase when referring to concept
   ```

2. **Style Guide:**
   - Tone: Professional but conversational
   - Voice: Second person ("you will...")
   - Code style: Follow language conventions
   - Heading capitalization: Title case for chapters, sentence case for sections

3. **Terminology Audit:**

   ```bash
   # Find inconsistent usage
   grep -r "relation" {{config.manuscript.root}}/
   grep -r "table" {{config.manuscript.root}}/
   # Standardize to one term
   ```

4. **Regular Consistency Reviews:**
   - Review Part 1 for baseline terminology
   - Check each new chapter against Part 1
   - Final global consistency pass

### Challenge: Cross-References Across Many Chapters

**Solutions:**

1. **Detailed Section Numbers:**

   ```markdown
   See Chapter 7, Section 7.4.2 (Window Functions - RANK vs DENSE_RANK)
   ```

2. **Cross-Reference Index:**

   ```markdown
   # Cross-Reference Index

   **Window Functions:**

   - Introduced: Chapter 7, Section 7.4
   - Advanced usage: Chapter 12, Section 12.3
   - Performance: Chapter 8, Section 8.6
   - Exercises: Chapter 7 Exercise 5, Chapter 12 Exercise 3
   ```

3. **Validation Tool:**

   ```bash
   # Script to extract and validate all cross-references
   ./scripts/validate-cross-refs.sh {{config.manuscript.chapters}}/
   ```

4. **Use shard index for dependencies:**
   - Document what each chapter references
   - Update when chapters modified

### Challenge: Long Development Cycles (6-12 Months)

**Solutions:**

1. **Incremental Publishing (MEAP):**
   - Publish Part 1 at Month 3
   - Publish Part 2 at Month 5
   - Get early feedback, incorporate into later parts

2. **Version Planning:**

   ```markdown
   # Version Strategy

   **Primary Version:** PostgreSQL 15 (current stable)
   **Secondary Version:** PostgreSQL 14 (for migration notes)
   **Future Version:** PostgreSQL 16 (in appendix)

   **Update Schedule:**

   - Month 6: Check for new versions
   - Month 10: Final version update
   ```

3. **Milestone Reviews:**
   - Every 2 months: Review completed chapters
   - Check if content still current
   - Update if technology changed

4. **Modular Content:**
   - Core concepts less likely to change
   - Version-specific content in appendices
   - Easy to update specific sections

### Challenge: Multiple Contributors

**Solutions:**

1. **Chapter Ownership:**
   - Clear assignment
   - Owner responsible for quality
   - Owner makes final decisions

2. **Communication Protocols:**
   - Weekly sync meetings
   - Shared Slack/Discord channel
   - Document cross-chapter dependencies

3. **Shared Standards:**
   - Common style guide (all follow)
   - Shared glossary (all use same terms)
   - Code formatting standards
   - Review checklist standards

4. **Cross-Review:**
   - Jane reviews Bob's chapters
   - Bob reviews Alice's chapters
   - Fresh perspective
   - Consistency check

## Technology Stack for Large Projects

### Essential Tools

**Writing:**

- Markdown editor (VS Code, Typora, iA Writer)
- Spell check / grammar (Grammarly, LanguageTool)

**Version Control:**

- Git (mandatory for multi-author)
- GitHub/GitLab (collaboration)

**Code Examples:**

- Language-specific IDE
- Testing framework
- CI/CD for code validation

**Diagram Creation:**

- Mermaid (code-based diagrams)
- Draw.io / Excalidraw (visual diagrams)
- Screenshot tools (platform-specific)

**Reference Management:**

- Glossary (markdown file)
- Cross-reference tracker (spreadsheet or script)

**Project Management:**

- Milestone tracking (GitHub Projects, Trello)
- Communication (Slack, Discord)

### Optional Tools

**Build System:**

```bash
# Assemble chapters into full book
npm run build:book

# Generate PDF preview
npm run preview:pdf

# Validate all cross-references
npm run validate:refs
```

**Automation:**

- Spell check on commit (pre-commit hook)
- Code example testing (CI)
- Link validation (weekly cron)

## Project Structure Templates

### Small Team (1-2 Authors, 300-500 Pages)

```
project/
├── {{config.manuscript.root}}/
│   ├── book-outline-index.md
│   ├── chapters/
│   │   ├── chapter-01.md
│   │   └── ...
│   └── assets/
├── {{config.codeExamples.root}}/
├── docs/
│   ├── style-guide.md
│   └── glossary.md
└── README.md
```

### Large Team (3-5 Authors, 500-1000 Pages)

```
project/
├── {{config.manuscript.root}}/
│   ├── book-info/
│   │   ├── book-level-info.md
│   │   ├── book-outline-index.md
│   │   ├── style-guide.md
│   │   └── glossary.md
│   ├── part-1/
│   ├── part-2/
│   ├── part-3/
│   └── assembled/          # Assembled parts for review
├── {{config.codeExamples.root}}/
│   ├── chapter-01/
│   └── ...
├── assets/
│   ├── diagrams/
│   └── screenshots/
├── reviews/
│   ├── technical/
│   └── editorial/
├── scripts/
│   ├── build-book.sh
│   └── validate-refs.sh
└── README.md
```

## Next Steps

After setting up large document management:

1. Choose organizational strategy for your project
2. Set up directory structure
3. Initialize version control
4. Create style guide and glossary
5. Shard outline if 20+ chapters (shard-book-outline.md)
6. Assign chapter ownership (if multi-author)
7. Begin systematic chapter development
8. Implement milestone tracking
9. Establish QA checkpoints
10. Celebrate progress regularly

## Related Resources

- Task: shard-large-chapter.md - Breaking large chapters into shards
- Task: shard-book-outline.md - Breaking outline into per-chapter files
- Task: merge-chapter-shards.md - Reassembling sharded chapters
- Task: design-book-outline.md - Creating initial book structure
- Task: write-chapter-draft.md - Chapter writing workflow
- Core: shard-doc.md - General document sharding
