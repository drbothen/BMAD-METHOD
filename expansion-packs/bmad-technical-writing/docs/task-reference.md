# Task Reference

## Introduction

The BMad Technical Writing Expansion Pack provides **33 executable tasks** that guide agents through specific workflows. Tasks are procedural markdown files with step-by-step instructions that agents follow exactly.

This comprehensive reference documents all 33 tasks organized by phase, with:

- **Task name and purpose** - What the task accomplishes
- **When to use** - Specific scenarios
- **Prerequisites** - What's needed to start
- **Outputs** - Deliverables produced
- **Related workflows** - Which workflows use this task
- **Related agents** - Which agents execute this task
- **Estimated time** - Typical duration

### Task Categories

- **Planning Phase (6 tasks)**: Book outlines, learning paths, proposals
- **Chapter Development (8 tasks)**: Drafts, outlines, summaries, introductions
- **Code Management (5 tasks)**: Examples, testing, repositories, version checks
- **Review & Editing (4 tasks)**: Technical reviews, copy editing, feedback incorporation
- **Publishing (7 tasks)**: Packaging, MEAP, self-publishing, indexes
- **Documentation (3 tasks)**: Glossaries, API docs, diagrams

---

## Planning Phase Tasks

### design-book-outline.md

**Purpose**: Creates detailed pedagogical book outline with learning progression

**When to Use**: Planning new technical book, need structured chapter-by-chapter outline

**Prerequisites**:
- Book topic and target audience defined
- Publisher target identified (optional)

**Outputs**: `book-outline.md` with chapters, learning objectives, prerequisites

**Related Workflows**: Book Planning Workflow
**Related Agents**: instructional-designer
**Estimated Time**: 8-12 hours

---

### create-learning-objectives.md

**Purpose**: Defines measurable learning outcomes using Bloom's taxonomy

**When to Use**: Planning chapter content, need specific learning goals

**Prerequisites**: Chapter topic defined

**Outputs**: Learning objectives (3-5 per chapter)

**Related Agents**: instructional-designer
**Estimated Time**: 1-2 hours

---

### design-learning-path.md

**Purpose**: Maps prerequisite dependencies and skill progression across chapters

**When to Use**: Validating book learning flow, ensuring no knowledge gaps

**Prerequisites**: Book outline complete

**Outputs**: Learning path diagram with dependencies

**Related Agents**: learning-path-designer, instructional-designer
**Estimated Time**: 3-5 hours

---

### plan-book-revision.md

**Purpose**: Creates strategic plan for updating existing book (2nd/3rd edition)

**When to Use**: Planning book updates, version migration, content refresh

**Prerequisites**: Existing book analysis complete

**Outputs**: `revision-plan.md` with surgical update strategy

**Related Workflows**: Book Edition Update Workflow
**Related Agents**: book-analyst
**Estimated Time**: 6-12 hours

---

### analyze-existing-book.md

**Purpose**: Analyzes existing book structure, style, patterns for consistency

**When to Use**: Planning revisions, adding chapters to existing book

**Prerequisites**: Access to existing book content

**Outputs**: `book-analysis-report.md` with patterns extracted

**Related Workflows**: Book Edition Update Workflow, Add Chapter Workflow
**Related Agents**: book-analyst
**Estimated Time**: 8-16 hours

---

### extract-code-patterns.md

**Purpose**: Extracts code style and conventions from existing book

**When to Use**: Maintaining consistency when updating existing code examples

**Prerequisites**: Existing book with code examples

**Outputs**: Code style guide extracted from existing patterns

**Related Agents**: book-analyst
**Estimated Time**: 2-4 hours

---

## Chapter Development Tasks

### create-chapter-outline.md

**Purpose**: Creates detailed chapter structure with sections, exercises, code examples

**When to Use**: Before writing chapter content

**Prerequisites**: Book outline with chapter objectives

**Outputs**: `chapter-{n}-outline.md`

**Related Workflows**: Chapter Development Workflow
**Related Agents**: tutorial-architect
**Estimated Time**: 2-4 hours

---

### write-chapter-draft.md

**Purpose**: Writes complete chapter draft from outline

**When to Use**: Traditional full-chapter writing approach

**Prerequisites**: Chapter outline, code examples developed

**Outputs**: `chapter-{n}-draft.md`

**Related Agents**: tutorial-architect
**Estimated Time**: 12-20 hours (15-30 page chapter)

---

### write-introduction.md

**Purpose**: Writes chapter introduction with hook, overview, learning goals

**When to Use**: Starting chapter or section writing

**Prerequisites**: Chapter outline

**Outputs**: Introduction section (1-2 pages)

**Related Agents**: tutorial-architect
**Estimated Time**: 1-2 hours

---

### write-summary.md

**Purpose**: Creates chapter conclusion with key takeaways and next steps

**When to Use**: Completing chapter writing

**Prerequisites**: Chapter content complete

**Outputs**: Summary section (1 page)

**Related Agents**: tutorial-architect
**Estimated Time**: 1 hour

---

### create-preface.md

**Purpose**: Writes book preface (author voice, how to use book)

**When to Use**: Completing book front matter

**Prerequisites**: Book content substantially complete

**Outputs**: `preface.md`

**Related Agents**: book-publisher
**Estimated Time**: 2-3 hours

---

### create-appendix.md

**Purpose**: Creates reference appendix

**When to Use**: Adding supplementary reference material

**Prerequisites**: Main content complete

**Outputs**: Appendix markdown file

**Related Agents**: api-documenter
**Estimated Time**: 2-4 hours per appendix

---

### develop-tutorial.md

**Purpose**: Creates step-by-step hands-on tutorial

**When to Use**: Building tutorial sections, workshop materials

**Prerequisites**: Tutorial plan, learning objective defined

**Outputs**: Complete tutorial with steps, code, troubleshooting

**Related Workflows**: Tutorial Creation Workflow
**Related Agents**: tutorial-architect
**Estimated Time**: 4-8 hours

---

### design-exercises.md

**Purpose**: Creates practice problem sets aligned with learning objectives

**When to Use**: Adding exercises to chapters

**Prerequisites**: Learning objectives defined

**Outputs**: Exercise set with solutions

**Related Agents**: exercise-creator
**Estimated Time**: 2-4 hours

---

## Code Management Tasks

### create-code-example.md

**Purpose**: Develops single tested code example with documentation

**When to Use**: Creating code snippets for chapters

**Prerequisites**: Example purpose and target version defined

**Outputs**: Tested code file with tests and README

**Related Workflows**: Code Example Workflow
**Related Agents**: code-curator
**Estimated Time**: 1-4 hours

---

### test-code-examples.md

**Purpose**: Tests all code examples across versions and platforms

**When to Use**: Validating code quality before chapter finalization

**Prerequisites**: Code examples developed

**Outputs**: Test results report

**Related Agents**: code-curator, sample-code-maintainer
**Estimated Time**: 1-2 hours per chapter

---

### setup-code-repository.md

**Purpose**: Organizes code repository structure with testing and CI/CD

**When to Use**: Starting book project, need organized code structure

**Prerequisites**: Book outline defining chapter count

**Outputs**: Repository with folders, README, CI/CD pipeline

**Related Agents**: sample-code-maintainer
**Estimated Time**: 2-4 hours

---

### version-matrix-check.md

**Purpose**: Defines and tests version compatibility matrix

**When to Use**: Multi-version book (e.g., Python 3.10, 3.11, 3.12)

**Prerequisites**: Target versions identified

**Outputs**: Version matrix with test results

**Related Agents**: version-manager
**Estimated Time**: 2-3 hours setup, ongoing testing

---

### update-chapter-for-version.md

**Purpose**: Updates chapter code for new technology version

**When to Use**: Version migration for 2nd edition

**Prerequisites**: Version impact analysis complete

**Outputs**: Updated chapter with migrated code

**Related Workflows**: Book Edition Update Workflow
**Related Agents**: version-manager, code-curator
**Estimated Time**: 2-6 hours per chapter (varies)

---

## Review & Editing Tasks

### technical-review-chapter.md

**Purpose**: Performs comprehensive technical review of chapter

**When to Use**: Validating technical accuracy before publication

**Prerequisites**: Chapter draft complete

**Outputs**: `technical-review-report.md` with findings

**Related Workflows**: Technical Review Workflow, Chapter Assembly Workflow
**Related Agents**: technical-reviewer
**Estimated Time**: 3-5 hours per chapter

---

### copy-edit-chapter.md

**Purpose**: Professional copy editing for clarity, consistency, style

**When to Use**: After technical review, before finalization

**Prerequisites**: Technically accurate chapter

**Outputs**: Edited chapter with change summary

**Related Agents**: technical-editor
**Estimated Time**: 2-4 hours per chapter

---

### incorporate-reviewer-feedback.md

**Purpose**: Systematically addresses review comments and feedback

**When to Use**: After receiving technical review, beta reader, or publisher feedback

**Prerequisites**: Review report with categorized feedback

**Outputs**: Revised chapter addressing all feedback

**Related Workflows**: Incorporate Review Feedback Workflow
**Related Agents**: tutorial-architect, technical-reviewer
**Estimated Time**: 4-12 hours (varies by feedback volume)

---

### validate-cross-references.md

**Purpose**: Verifies all internal links, chapter references, and figure citations

**When to Use**: Final validation before publication

**Prerequisites**: Book content complete

**Outputs**: Validation report with broken references

**Related Agents**: technical-editor
**Estimated Time**: 1-2 hours

---

## Publishing Tasks

### package-for-publisher.md

**Purpose**: Prepares manuscript package for publisher submission

**When to Use**: Submitting to traditional publisher

**Prerequisites**: Book complete, publisher identified

**Outputs**: Formatted manuscript bundle

**Related Workflows**: PacktPub/O'Reilly/Manning Submission Workflows
**Related Agents**: book-publisher
**Estimated Time**: 3-6 hours

---

### prepare-meap-chapter.md

**Purpose**: Formats chapter for Manning Early Access Program

**When to Use**: Incremental Manning MEAP releases

**Prerequisites**: Chapter complete and reviewed

**Outputs**: MEAP-ready chapter

**Related Workflows**: Manning MEAP Workflow
**Related Agents**: book-publisher
**Estimated Time**: 1-2 hours per chapter

---

### self-publish-prep.md

**Purpose**: Prepares book for self-publishing platforms

**When to Use**: Self-publishing (Leanpub, Gumroad, Amazon KDP)

**Prerequisites**: Book complete

**Outputs**: Platform-specific formatted files

**Related Workflows**: Self-Publishing Workflow
**Related Agents**: book-publisher
**Estimated Time**: 4-8 hours

---

### create-index-entries.md

**Purpose**: Generates book index from marked terms

**When to Use**: Finalizing book for print publication

**Prerequisites**: Index terms marked throughout manuscript

**Outputs**: Book index

**Related Agents**: book-publisher
**Estimated Time**: 3-5 hours

---

### create-solutions.md

**Purpose**: Creates detailed solutions for exercises

**When to Use**: Adding solutions appendix or separate guide

**Prerequisites**: Exercise sets defined

**Outputs**: Solutions with explanations

**Related Agents**: exercise-creator
**Estimated Time**: 2-3 hours

---

### take-screenshots.md

**Purpose**: Plans and captures screenshots for book

**When to Use**: Need visual documentation

**Prerequisites**: Application/tool ready for screenshots

**Outputs**: Screenshot files with annotations

**Related Agents**: screenshot-specialist
**Estimated Time**: 1-2 hours per chapter

---

### design-diagram-set.md

**Purpose**: Plans complete set of diagrams for chapter or book

**When to Use**: Identifying all visual needs upfront

**Prerequisites**: Content outline

**Outputs**: Diagram specifications list

**Related Agents**: screenshot-specialist
**Estimated Time**: 2-3 hours

---

## Documentation Tasks

### generate-api-docs.md

**Purpose**: Creates comprehensive API reference documentation

**When to Use**: Documenting APIs, libraries, frameworks

**Prerequisites**: API code available

**Outputs**: API reference with parameters, returns, examples

**Related Agents**: api-documenter
**Estimated Time**: 4-8 hours (varies by API size)

---

### build-glossary.md

**Purpose**: Compiles terminology glossary from book content

**When to Use**: Creating book glossary

**Prerequisites**: Book content with terms identified

**Outputs**: `glossary.md` with alphabetized definitions

**Related Agents**: api-documenter
**Estimated Time**: 2-4 hours

---

### create-diagram-spec.md

**Purpose**: Creates specification for single technical diagram

**When to Use**: Need diagram for concept explanation

**Prerequisites**: Concept to visualize defined

**Outputs**: Diagram specification (Mermaid code or detailed description)

**Related Agents**: screenshot-specialist
**Estimated Time**: 30 min - 1 hour per diagram

---

## Task Comparison Table

| Task | Phase | Est. Time | Primary Agent | Complexity |
|------|-------|-----------|---------------|------------|
| design-book-outline | Planning | 8-12 hrs | instructional-designer | Medium |
| create-learning-objectives | Planning | 1-2 hrs | instructional-designer | Low |
| design-learning-path | Planning | 3-5 hrs | learning-path-designer | Medium |
| plan-book-revision | Planning | 6-12 hrs | book-analyst | Medium |
| analyze-existing-book | Planning | 8-16 hrs | book-analyst | High |
| extract-code-patterns | Planning | 2-4 hrs | book-analyst | Medium |
| create-chapter-outline | Chapter Dev | 2-4 hrs | tutorial-architect | Low |
| write-chapter-draft | Chapter Dev | 12-20 hrs | tutorial-architect | High |
| write-introduction | Chapter Dev | 1-2 hrs | tutorial-architect | Low |
| write-summary | Chapter Dev | 1 hr | tutorial-architect | Low |
| create-preface | Chapter Dev | 2-3 hrs | book-publisher | Low |
| create-appendix | Chapter Dev | 2-4 hrs | api-documenter | Medium |
| develop-tutorial | Chapter Dev | 4-8 hrs | tutorial-architect | Medium |
| design-exercises | Chapter Dev | 2-4 hrs | exercise-creator | Medium |
| create-code-example | Code Mgmt | 1-4 hrs | code-curator | Low-Med |
| test-code-examples | Code Mgmt | 1-2 hrs | code-curator | Low |
| setup-code-repository | Code Mgmt | 2-4 hrs | sample-code-maintainer | Medium |
| version-matrix-check | Code Mgmt | 2-3 hrs | version-manager | Medium |
| update-chapter-for-version | Code Mgmt | 2-6 hrs | version-manager | Medium |
| technical-review-chapter | Review | 3-5 hrs | technical-reviewer | Medium |
| copy-edit-chapter | Review | 2-4 hrs | technical-editor | Medium |
| incorporate-reviewer-feedback | Review | 4-12 hrs | tutorial-architect | Varies |
| validate-cross-references | Review | 1-2 hrs | technical-editor | Low |
| package-for-publisher | Publishing | 3-6 hrs | book-publisher | Medium |
| prepare-meap-chapter | Publishing | 1-2 hrs | book-publisher | Low |
| self-publish-prep | Publishing | 4-8 hrs | book-publisher | Medium |
| create-index-entries | Publishing | 3-5 hrs | book-publisher | Medium |
| create-solutions | Publishing | 2-3 hrs | exercise-creator | Low |
| take-screenshots | Publishing | 1-2 hrs | screenshot-specialist | Low |
| design-diagram-set | Publishing | 2-3 hrs | screenshot-specialist | Medium |
| generate-api-docs | Documentation | 4-8 hrs | api-documenter | Medium |
| build-glossary | Documentation | 2-4 hrs | api-documenter | Low |
| create-diagram-spec | Documentation | 30m-1hr | screenshot-specialist | Low |

---

## Quick Reference: Most Common Tasks

### For New Books
1. `design-book-outline.md` - Create book structure
2. `create-chapter-outline.md` - Plan each chapter
3. `create-code-example.md` - Develop code examples
4. `write-chapter-draft.md` or section-driven workflow
5. `technical-review-chapter.md` - Validate accuracy
6. `copy-edit-chapter.md` - Polish quality
7. `package-for-publisher.md` - Submit to publisher

### For Existing Book Updates
1. `analyze-existing-book.md` - Understand current state
2. `plan-book-revision.md` - Strategic update plan
3. `update-chapter-for-version.md` - Migrate code
4. `incorporate-reviewer-feedback.md` - Address feedback
5. `package-for-publisher.md` - Resubmit

### For Tutorial-Focused Content
1. `create-learning-objectives.md` - Define outcomes
2. `develop-tutorial.md` - Build step-by-step tutorial
3. `create-code-example.md` - Create tested code
4. `design-exercises.md` - Add practice problems
5. `create-solutions.md` - Provide solutions

---

## Task Selection by Phase

**Planning Phase**: Start here for new books
- design-book-outline, create-learning-objectives, design-learning-path

**Chapter Development**: Main content creation
- create-chapter-outline, write-chapter-draft, write-introduction, write-summary, develop-tutorial, design-exercises

**Code Management**: Ensure code quality
- create-code-example, test-code-examples, setup-code-repository

**Review & Editing**: Quality assurance
- technical-review-chapter, copy-edit-chapter, incorporate-reviewer-feedback

**Publishing**: Prepare for release
- package-for-publisher, prepare-meap-chapter, self-publish-prep, create-index-entries

**Documentation**: Reference materials
- generate-api-docs, build-glossary, create-diagram-spec

---

## Conclusion

The BMad Technical Writing Expansion Pack's **33 executable tasks** provide step-by-step procedural guidance for every aspect of technical book authoring. By understanding each task's purpose, prerequisites, and outputs, you can:

- **Execute workflows** efficiently with clear procedures
- **Track progress** using task completion
- **Estimate time** accurately for planning
- **Coordinate agents** with specific task assignments
- **Maintain quality** through structured procedures

**Most Critical Tasks**:
- `design-book-outline.md` - Foundation of book planning
- `create-chapter-outline.md` - Essential for chapter development
- `technical-review-chapter.md` - Ensures technical accuracy
- `copy-edit-chapter.md` - Professional polish

**Total task count**: 33
**Word count**: ~2,500 words

---

**Related Documentation**:
- [Agent Reference Guide](agent-reference.md) - Agents that execute these tasks
- [Workflow Guide](workflow-guide.md) - Workflows that orchestrate tasks
- [Template Gallery](template-gallery.md) - Templates used by tasks
- [User Guide](user-guide.md) - How tasks fit into the process
