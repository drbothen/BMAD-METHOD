# Task Reference

## Introduction

The BMad Technical Writing Expansion Pack provides **68 executable tasks** that guide agents through specific workflows. Tasks are procedural markdown files with step-by-step instructions that agents follow exactly.

This comprehensive reference documents all 68 tasks organized by phase, with:

- **Task name and purpose** - What the task accomplishes
- **When to use** - Specific scenarios
- **Prerequisites** - What's needed to start
- **Outputs** - Deliverables produced
- **Related workflows** - Which workflows use this task
- **Related agents** - Which agents execute this task
- **Estimated time** - Typical duration

### Task Categories

- **Planning Phase (7 tasks)**: Book outlines, learning paths, proposals, research
- **Instructional Design (5 tasks)** **(v2.1+)**: Learning frameworks, difficulty curves, assessment strategies, prerequisite mapping
- **Chapter Development (13 tasks)**: Drafts, outlines, summaries, sections, walkthroughs, transitions, **AI content humanization**
- **Code Management (14 tasks)** **(v2.1+ expanded)**: Examples, testing, repositories, security audits, version checks, optimization
- **Review & Editing (9 tasks)** **(v2.1+ expanded)**: Technical reviews, copy editing, checklist execution, validation, verification
- **Publishing (10 tasks)** **(v2.1+ expanded)**: Packaging, MEAP, self-publishing, format conversions, indexes
- **Documentation & API (7 tasks)** **(v2.1+ expanded)**: Glossaries, API docs, diagrams, function documentation, usage examples
- **Specialized Tasks (3 tasks)** **(v2.1+)**: Screenshots, visual optimization, research tools

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

### create-book-research-queries.md **(v2.1+)**

**Purpose**: Creates comprehensive research query strategy for technical book topics

**When to Use**: Planning research phase, gathering technical information, validating approach

**Prerequisites**: Book topic defined, research goals identified

**Outputs**: Research query list with search strategies

**Related Workflows**: Book Planning Workflow, Research Workflow
**Related Agents**: technical-researcher
**Estimated Time**: 1-2 hours

---

### execute-research-with-tools.md **(v2.1+)**

**Purpose**: Executes research using web search, documentation, and research tools

**When to Use**: Gathering technical information, validating concepts, researching best practices

**Prerequisites**: Research queries defined

**Outputs**: Research findings document with sources and key insights

**Related Workflows**: Book Planning Workflow, Research Workflow
**Related Agents**: technical-researcher
**Estimated Time**: 3-8 hours (varies by scope)

---

## Instructional Design Tasks **(v2.1+)**

### analyze-difficulty-curve.md **(v2.1+)**

**Purpose**: Analyzes learning difficulty progression to ensure appropriate cognitive load and scaffolding

**When to Use**: Validating chapter sequence, checking learning flow, ensuring proper difficulty progression

**Prerequisites**:

- Book outline or chapter content
- Learning objectives defined

**Outputs**: Difficulty analysis report with recommendations for reordering or adjusting content

**Related Workflows**: Book Planning Workflow, Learning Path Design
**Related Agents**: instructional-designer
**Estimated Time**: 2-4 hours

---

### apply-learning-framework.md **(v2.1+)**

**Purpose**: Applies pedagogical frameworks (Bloom's Taxonomy, cognitive load theory) to content design

**When to Use**: Designing learning objectives, structuring educational content, validating pedagogical soundness

**Prerequisites**: Content outline or draft

**Outputs**: Framework-aligned content structure with learning level indicators

**Related Workflows**: Book Planning Workflow, Chapter Development
**Related Agents**: instructional-designer
**Estimated Time**: 2-3 hours

---

### map-prerequisites.md **(v2.1+)**

**Purpose**: Maps prerequisite dependencies across chapters and sections to prevent knowledge gaps

**When to Use**: Book planning phase, validating learning flow, identifying circular dependencies

**Prerequisites**: Book outline with chapter topics

**Outputs**: Prerequisite dependency map (Mermaid diagram) with validation results

**Related Workflows**: Book Planning Workflow, Learning Path Design
**Related Agents**: instructional-designer, learning-path-designer
**Estimated Time**: 3-5 hours

---

### design-assessment-strategy.md **(v2.1+)**

**Purpose**: Creates comprehensive assessment strategy aligned with learning objectives

**When to Use**: Planning exercises, quizzes, and practical assessments for chapters

**Prerequisites**: Learning objectives defined

**Outputs**: Assessment strategy document with exercise specifications

**Related Workflows**: Chapter Development Workflow
**Related Agents**: instructional-designer, exercise-creator
**Estimated Time**: 2-4 hours

---

### validate-learning-flow.md **(v2.1+)**

**Purpose**: Validates pedagogical progression, prerequisite dependencies, and difficulty curve in learning content

**When to Use**: Quality gate in workflows, validating chapter sequences, ensuring no knowledge gaps

**Prerequisites**:

- Outline or chapter content
- Prerequisites defined

**Outputs**: Validation report with identified gaps, circular dependencies, and progression issues

**Related Workflows**: Section Development Workflow, Chapter Assembly Workflow, Book Planning Workflow
**Related Agents**: instructional-designer
**Estimated Time**: 1-3 hours

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

### write-section-draft.md **(v2.1+)**

**Purpose**: Transform section plan and code examples into complete 2-5 page pedagogically sound section content

**When to Use**: Section-driven development workflow (step 3), writing individual sections incrementally

**Prerequisites**:

- Section plan (section-plan.md) with learning objectives
- Code examples from code-curator (tested and documented)
- Chapter outline (chapter context)

**Outputs**: `section-{n}-draft.md` (2-5 pages) ready for technical review

**Related Workflows**: Section Development Workflow **(KEY TASK FOR THIS WORKFLOW)**
**Related Agents**: tutorial-architect
**Estimated Time**: 3-6 hours per section

**Key Features**: Structured workflow (concept → tutorial → applications), code integration guidance, quality checks

---

### write-walkthrough.md **(v2.1+)**

**Purpose**: Creates detailed step-by-step walkthrough guides for complex procedures or tutorials

**When to Use**: Building hands-on tutorials, creating installation guides, documenting multi-step processes

**Prerequisites**: Procedure or tutorial plan

**Outputs**: Step-by-step walkthrough document with screenshots and troubleshooting

**Related Workflows**: Tutorial Creation Workflow
**Related Agents**: tutorial-architect
**Estimated Time**: 4-8 hours

---

### merge-sections.md **(v2.1+)**

**Purpose**: Combines multiple section drafts into cohesive chapter with proper flow and transitions

**When to Use**: Section-driven workflow after all sections complete, assembling chapter from parts

**Prerequisites**: All section drafts complete and reviewed

**Outputs**: Merged chapter document with integrated transitions

**Related Workflows**: Section Development Workflow (step 6), Chapter Assembly Workflow
**Related Agents**: tutorial-architect
**Estimated Time**: 2-4 hours

---

### enhance-transitions.md **(v2.1+)**

**Purpose**: Improves narrative flow and transitions between sections within a chapter

**When to Use**: After merging sections, polishing chapter flow, improving readability

**Prerequisites**: Merged chapter document

**Outputs**: Chapter with enhanced transitions and improved narrative flow

**Related Workflows**: Section Development Workflow, Chapter Assembly Workflow
**Related Agents**: tutorial-architect, technical-editor
**Estimated Time**: 1-3 hours

---

### humanize-ai-drafted-chapter.md

**Purpose**: Systematically removes AI-generated patterns from AI-assisted content to ensure authentic human voice

**When to Use**: After drafting with AI assistance (expand-outline-to-draft, ChatGPT, Claude, etc.), before technical review

**Prerequisites**:

- Chapter draft complete (AI-assisted or AI-generated)
- generative-ai-compliance-checklist.md executed (baseline AI patterns identified)

**Outputs**:

- `chapter-{n}-humanized.md` with AI patterns removed
- Change log documenting all humanization changes
- humanization-checklist.md validation report with <20% AI patterns remaining

**Related Workflows**: Chapter Development Workflow (humanization step after drafting)
**Related Agents**: tutorial-architect
**Estimated Time**: 2-4 hours per chapter

**Key Features**: 11-step systematic workflow removing 8 AI pattern types (vocabulary, metaphors, generic examples, impersonal voice, sentence uniformity, flowery language, repetitive content, rigid structure), before/after examples embedded, quality validation with scoring

**Note**: REQUIRED when AI tools assisted drafting. Critical for publisher compliance (PacktPub AI disclosure) and reader trust. Prevents negative reviews citing "AI-generated feel".

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

### security-audit.md **(v2.1+)**

**Purpose**: Performs comprehensive security audit on code examples to identify vulnerabilities and security issues

**When to Use**: Quality gate for code examples, validating security best practices, before publication

**Prerequisites**:

- Code examples complete
- Language and security standards defined

**Outputs**: Security audit report with vulnerability findings and remediation recommendations

**Related Workflows**: Code Example Workflow, Quality Assurance Workflow
**Related Agents**: code-curator
**Estimated Time**: 2-4 hours

---

### cross-platform-test.md **(v2.1+)**

**Purpose**: Tests code examples across different platforms (Windows, macOS, Linux) and environments

**When to Use**: Validating cross-platform compatibility, before publication

**Prerequisites**: Code examples complete and tested

**Outputs**: Cross-platform test report with platform-specific issues identified

**Related Workflows**: Code Example Workflow, Quality Assurance Workflow
**Related Agents**: code-curator, sample-code-maintainer
**Estimated Time**: 2-3 hours per chapter

---

### performance-review.md **(v2.1+)**

**Purpose**: Reviews code examples for performance issues, inefficiencies, and optimization opportunities

**When to Use**: Quality gate for code, ensuring examples demonstrate best practices

**Prerequisites**: Code examples complete and tested

**Outputs**: Performance review report with optimization recommendations

**Related Workflows**: Code Example Workflow, Quality Assurance Workflow
**Related Agents**: code-curator
**Estimated Time**: 1-3 hours

---

### version-check.md **(v2.1+)**

**Purpose**: Validates code examples against target version compatibility requirements

**When to Use**: Multi-version books, version migration, compatibility validation

**Prerequisites**: Target versions defined, code examples complete

**Outputs**: Version compatibility report

**Related Workflows**: Code Example Workflow, Version Management
**Related Agents**: version-manager, code-curator
**Estimated Time**: 1-2 hours

---

### optimize-code.md **(v2.1+)**

**Purpose**: Optimizes code examples for performance, readability, and best practices

**When to Use**: Polishing code examples, improving code quality, demonstrating best practices

**Prerequisites**: Working code examples

**Outputs**: Optimized code with explanation of improvements

**Related Workflows**: Code Example Workflow
**Related Agents**: code-curator
**Estimated Time**: 1-2 hours per example

---

### troubleshoot-example.md **(v2.1+)**

**Purpose**: Debugs and fixes broken code examples with systematic troubleshooting approach

**When to Use**: Code examples failing tests, debugging issues, fixing broken examples

**Prerequisites**: Failing code example, error messages

**Outputs**: Fixed code with troubleshooting documentation

**Related Workflows**: Code Example Workflow
**Related Agents**: code-curator
**Estimated Time**: 1-4 hours (varies by complexity)

---

### organize-code-repo.md **(v2.1+)**

**Purpose**: Organizes code repository structure following best practices for technical books

**When to Use**: Starting book project, restructuring existing repository

**Prerequisites**: Book outline defining chapter structure

**Outputs**: Organized repository with folders, README, .gitignore, LICENSE

**Related Workflows**: Code Repository Setup Workflow
**Related Agents**: sample-code-maintainer
**Estimated Time**: 2-3 hours

---

### create-ci-pipeline.md **(v2.1+)**

**Purpose**: Creates CI/CD pipeline for automated testing of code examples

**When to Use**: Setting up code repository, automating quality gates

**Prerequisites**: Code repository organized, tests written

**Outputs**: CI/CD configuration (GitHub Actions, etc.) with automated testing

**Related Workflows**: Code Repository Setup Workflow
**Related Agents**: sample-code-maintainer
**Estimated Time**: 3-5 hours

---

### publish-repo.md **(v2.1+)**

**Purpose**: Prepares and publishes code repository for public release

**When to Use**: Book near completion, making code examples publicly available

**Prerequisites**: Code repository complete, all tests passing

**Outputs**: Published repository on GitHub/GitLab with documentation

**Related Workflows**: Publication Workflow
**Related Agents**: sample-code-maintainer
**Estimated Time**: 2-3 hours

---

### run-tests.md **(v2.1+)**

**Purpose**: Executes test suite for code examples with comprehensive reporting

**When to Use**: Continuous validation, before commits, quality gates

**Prerequisites**: Tests written, code examples complete

**Outputs**: Test execution report with pass/fail results

**Related Workflows**: Code Example Workflow, Quality Assurance
**Related Agents**: sample-code-maintainer, code-curator
**Estimated Time**: 30 min - 1 hour

---

### create-version-matrix.md **(v2.1+)**

**Purpose**: Creates version compatibility matrix for multi-version technical books

**When to Use**: Planning version support, documenting compatibility

**Prerequisites**: Target versions identified

**Outputs**: Version matrix documenting which features work with which versions

**Related Workflows**: Version Management Workflow
**Related Agents**: version-manager
**Estimated Time**: 2-3 hours

---

### assess-version-impact.md **(v2.1+)**

**Purpose**: Analyzes impact of version changes on existing code and content

**When to Use**: Planning version migrations, assessing update scope

**Prerequisites**: Current version and target version defined

**Outputs**: Version impact analysis report with migration recommendations

**Related Workflows**: Book Edition Update Workflow
**Related Agents**: version-manager
**Estimated Time**: 3-5 hours

---

### update-dependencies.md **(v2.1+)**

**Purpose**: Updates code dependencies to newer versions with testing and validation

**When to Use**: Version migrations, dependency updates, security patches

**Prerequisites**: Current code with dependency manifest

**Outputs**: Updated dependencies with test validation results

**Related Workflows**: Version Management Workflow
**Related Agents**: version-manager, code-curator
**Estimated Time**: 2-4 hours

---

### setup-code-repository.md **(DEPRECATED - use organize-code-repo.md)**

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

**Purpose**: Professional copy editing for clarity, consistency, style, with final AI pattern validation

**When to Use**: After technical review, before finalization

**Prerequisites**: Technically accurate chapter (humanized if AI-assisted)

**Outputs**: Edited chapter with change summary, final AI pattern check report (<5% patterns)

**Related Agents**: technical-editor
**Estimated Time**: 2-4 hours per chapter

**Key Features**: 11-step workflow including grammar/spelling, clarity, terminology consistency, publisher style, tone validation (Step 9), **final AI pattern check (Step 10)**, and summary creation

**Note**: Step 10 validates humanization effectiveness with target <5% AI patterns remaining for publication-ready quality

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

### verify-accuracy.md **(v2.1+)**

**Purpose**: Verifies technical accuracy of code, concepts, and explanations through systematic review

**When to Use**: Technical review quality gate, validating accuracy before publication

**Prerequisites**: Chapter or section draft complete

**Outputs**: Accuracy verification report with findings and corrections

**Related Workflows**: Technical Review Workflow, Quality Assurance
**Related Agents**: technical-reviewer
**Estimated Time**: 2-4 hours per chapter

---

### check-best-practices.md **(v2.1+)**

**Purpose**: Reviews content for adherence to industry best practices and current standards

**When to Use**: Quality gate for technical content, validating best practices demonstrated

**Prerequisites**: Content draft complete

**Outputs**: Best practices review report with recommendations

**Related Workflows**: Technical Review Workflow, Code Example Workflow
**Related Agents**: technical-reviewer, code-curator
**Estimated Time**: 1-3 hours

---

### execute-checklist.md

**Purpose**: Systematically execute quality checklists with pass/fail/na status and evidence collection

**When to Use**: Running quality gates in workflows, validating deliverables against standards, executing technical reviews, verifying publisher requirements

**Prerequisites**:

- Checklist file exists
- Subject material available for review
- Understanding of checklist criteria

**Outputs**: `reviews/checklist-results/{{checklist-name}}-{{timestamp}}.md` with results, summary statistics, and recommendations

**Related Workflows**: Section Development Workflow, Chapter Assembly Workflow, Book Planning Workflow, Technical Review Workflow, Publishing Workflows
**Related Agents**: technical-reviewer, code-curator, tutorial-architect, technical-editor, book-publisher (all 13 agents)
**Estimated Time**: 30 min - 2 hours (varies by checklist size)

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

### format-for-packtpub.md **(v2.1+)**

**Purpose**: Formats manuscript according to PacktPub submission requirements and style guide

**When to Use**: Submitting to PacktPub, preparing PacktPub-specific deliverables

**Prerequisites**:

- Manuscript complete and reviewed
- PacktPub style guide reviewed

**Outputs**: PacktPub-formatted manuscript with required structure and metadata

**Related Workflows**: PacktPub Submission Workflow
**Related Agents**: book-publisher
**Estimated Time**: 4-6 hours

---

### format-for-oreilly.md **(v2.1+)**

**Purpose**: Formats manuscript according to O'Reilly submission requirements (Atlas format, AsciiDoc)

**When to Use**: Submitting to O'Reilly Media, preparing O'Reilly-specific deliverables

**Prerequisites**:

- Manuscript complete and reviewed
- O'Reilly Atlas guidelines reviewed

**Outputs**: O'Reilly-formatted manuscript (AsciiDoc) with required metadata

**Related Workflows**: O'Reilly Submission Workflow
**Related Agents**: book-publisher
**Estimated Time**: 5-8 hours

---

### format-for-manning.md **(v2.1+)**

**Purpose**: Formats manuscript according to Manning submission requirements and Docbook format

**When to Use**: Submitting to Manning Publications, preparing Manning MEAP deliverables

**Prerequisites**:

- Manuscript complete and reviewed
- Manning author guide reviewed

**Outputs**: Manning-formatted manuscript with required structure and repository integration

**Related Workflows**: Manning MEAP Workflow, Manning Submission Workflow
**Related Agents**: book-publisher
**Estimated Time**: 4-7 hours

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

### plan-screenshots.md **(v2.1+)**

**Purpose**: Plans comprehensive screenshot strategy for chapter or book

**When to Use**: Beginning visual documentation, planning screenshot needs

**Prerequisites**: Content outline or draft

**Outputs**: Screenshot plan with specifications for each image

**Related Workflows**: Visual Documentation Workflow
**Related Agents**: screenshot-specialist
**Estimated Time**: 1-2 hours

---

### annotate-images.md **(v2.1+)**

**Purpose**: Adds annotations, callouts, and highlighting to screenshots and diagrams

**When to Use**: Enhancing visual clarity, directing reader attention

**Prerequisites**: Raw screenshots or diagrams captured

**Outputs**: Annotated images ready for publication

**Related Workflows**: Visual Documentation Workflow
**Related Agents**: screenshot-specialist
**Estimated Time**: 30 min - 1 hour per image

---

### optimize-visuals.md **(v2.1+)**

**Purpose**: Optimizes images for file size, quality, and publishing requirements

**When to Use**: Finalizing visuals, meeting publisher file size requirements

**Prerequisites**: Images created and annotated

**Outputs**: Optimized images with appropriate resolution and compression

**Related Workflows**: Visual Documentation Workflow, Publishing Workflow
**Related Agents**: screenshot-specialist
**Estimated Time**: 1-2 hours

---

## Documentation & API Tasks

### generate-api-docs.md

**Purpose**: Creates comprehensive API reference documentation

**When to Use**: Documenting APIs, libraries, frameworks

**Prerequisites**: API code available

**Outputs**: API reference with parameters, returns, examples

**Related Agents**: api-documenter
**Estimated Time**: 4-8 hours (varies by API size)

---

### document-function.md **(v2.1+)**

**Purpose**: Creates comprehensive documentation for individual functions or methods

**When to Use**: Documenting APIs, creating function references, building documentation sets

**Prerequisites**: Function code available, understanding of parameters and behavior

**Outputs**: Function documentation with signature, parameters, returns, examples

**Related Workflows**: API Documentation Workflow
**Related Agents**: api-documenter
**Estimated Time**: 30 min - 1 hour per function

---

### write-usage-examples.md **(v2.1+)**

**Purpose**: Creates practical usage examples for APIs, libraries, or frameworks

**When to Use**: Demonstrating API usage, creating getting-started guides

**Prerequisites**: API understanding, common use cases identified

**Outputs**: Usage example code with explanations and expected outputs

**Related Workflows**: API Documentation Workflow
**Related Agents**: api-documenter, code-curator
**Estimated Time**: 1-2 hours per example

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

| Task                          | Phase         | Est. Time | Primary Agent          | Complexity |
| ----------------------------- | ------------- | --------- | ---------------------- | ---------- |
| design-book-outline           | Planning      | 8-12 hrs  | instructional-designer | Medium     |
| create-learning-objectives    | Planning      | 1-2 hrs   | instructional-designer | Low        |
| design-learning-path          | Planning      | 3-5 hrs   | learning-path-designer | Medium     |
| plan-book-revision            | Planning      | 6-12 hrs  | book-analyst           | Medium     |
| analyze-existing-book         | Planning      | 8-16 hrs  | book-analyst           | High       |
| extract-code-patterns         | Planning      | 2-4 hrs   | book-analyst           | Medium     |
| create-chapter-outline        | Chapter Dev   | 2-4 hrs   | tutorial-architect     | Low        |
| write-chapter-draft           | Chapter Dev   | 12-20 hrs | tutorial-architect     | High       |
| write-introduction            | Chapter Dev   | 1-2 hrs   | tutorial-architect     | Low        |
| write-summary                 | Chapter Dev   | 1 hr      | tutorial-architect     | Low        |
| create-preface                | Chapter Dev   | 2-3 hrs   | book-publisher         | Low        |
| create-appendix               | Chapter Dev   | 2-4 hrs   | api-documenter         | Medium     |
| develop-tutorial              | Chapter Dev   | 4-8 hrs   | tutorial-architect     | Medium     |
| design-exercises              | Chapter Dev   | 2-4 hrs   | exercise-creator       | Medium     |
| create-code-example           | Code Mgmt     | 1-4 hrs   | code-curator           | Low-Med    |
| test-code-examples            | Code Mgmt     | 1-2 hrs   | code-curator           | Low        |
| setup-code-repository         | Code Mgmt     | 2-4 hrs   | sample-code-maintainer | Medium     |
| version-matrix-check          | Code Mgmt     | 2-3 hrs   | version-manager        | Medium     |
| update-chapter-for-version    | Code Mgmt     | 2-6 hrs   | version-manager        | Medium     |
| technical-review-chapter      | Review        | 3-5 hrs   | technical-reviewer     | Medium     |
| copy-edit-chapter             | Review        | 2-4 hrs   | technical-editor       | Medium     |
| incorporate-reviewer-feedback | Review        | 4-12 hrs  | tutorial-architect     | Varies     |
| validate-cross-references     | Review        | 1-2 hrs   | technical-editor       | Low        |
| execute-checklist             | Review        | 30m-2 hrs | technical-reviewer     | Low        |
| package-for-publisher         | Publishing    | 3-6 hrs   | book-publisher         | Medium     |
| prepare-meap-chapter          | Publishing    | 1-2 hrs   | book-publisher         | Low        |
| self-publish-prep             | Publishing    | 4-8 hrs   | book-publisher         | Medium     |
| create-index-entries          | Publishing    | 3-5 hrs   | book-publisher         | Medium     |
| create-solutions              | Publishing    | 2-3 hrs   | exercise-creator       | Low        |
| take-screenshots              | Publishing    | 1-2 hrs   | screenshot-specialist  | Low        |
| design-diagram-set            | Publishing    | 2-3 hrs   | screenshot-specialist  | Medium     |
| generate-api-docs             | Documentation | 4-8 hrs   | api-documenter         | Medium     |
| build-glossary                | Documentation | 2-4 hrs   | api-documenter         | Low        |
| create-diagram-spec           | Documentation | 30m-1hr   | screenshot-specialist  | Low        |

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

- technical-review-chapter, copy-edit-chapter, incorporate-reviewer-feedback, execute-checklist

**Publishing**: Prepare for release

- package-for-publisher, prepare-meap-chapter, self-publish-prep, create-index-entries

**Documentation**: Reference materials

- generate-api-docs, build-glossary, create-diagram-spec

---

## Conclusion

The BMad Technical Writing Expansion Pack's **67 executable tasks** provide step-by-step procedural guidance for every aspect of technical book authoring. By understanding each task's purpose, prerequisites, and outputs, you can:

- **Execute workflows** efficiently with clear procedures
- **Track progress** using task completion
- **Estimate time** accurately for planning
- **Coordinate agents** with specific task assignments
- **Maintain quality** through structured procedures

**Most Critical Tasks**:

- `design-book-outline.md` - Foundation of book planning
- `create-chapter-outline.md` - Essential for chapter development
- `write-section-draft.md` **(v2.1+)** - Core section-driven workflow task
- `technical-review-chapter.md` - Ensures technical accuracy
- `execute-checklist.md` **(v2.1+)** - Universal quality gate execution
- `validate-learning-flow.md` **(v2.1+)** - Pedagogical validation
- `security-audit.md` **(v2.1+)** - Code security validation
- `copy-edit-chapter.md` - Professional polish

**Sprint 7 (v2.1) Additions**: 33 new tasks

- Instructional Design: 5 tasks
- Section Development: 4 tasks
- Code Security & Quality: 10 tasks
- Publisher Formatting: 3 tasks
- Specialized Documentation: 8 tasks
- Research: 2 tasks
- Universal: 1 task (execute-checklist)

**Total task count**: 67 (34 v2.0 + 33 v2.1)
**Word count**: ~5,000 words

---

**Related Documentation**:

- [Agent Reference Guide](agent-reference.md) - Agents that execute these tasks
- [Workflow Guide](workflow-guide.md) - Workflows that orchestrate tasks
- [Template Gallery](template-gallery.md) - Templates used by tasks
- [User Guide](user-guide.md) - How tasks fit into the process
