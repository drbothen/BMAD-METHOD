# BMad Technical Writing Expansion Pack - Complete Workflow Analysis

**Analysis Date**: 2025-01-26
**Version**: 1.1.0
**Purpose**: Complete workflow mapping from Idea → Book Outline → Chapter Development → PacktPub Submission

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Complete Workflow Overview](#complete-workflow-overview)
3. [Phase-by-Phase Breakdown](#phase-by-phase-breakdown)
4. [Agent Reference Guide](#agent-reference-guide)
5. [Supporting Tasks Analysis](#supporting-tasks-analysis)
6. [Workflow Integration Map](#workflow-integration-map)
7. [Time Estimates and Planning](#time-estimates-and-planning)
8. [Best Practices and Recommendations](#best-practices-and-recommendations)

---

## Executive Summary

The BMad Technical Writing Expansion Pack provides a **complete, structured system** for taking a technical book from initial concept through to PacktPub-formatted submission. The system consists of:

- **14 Specialized Agents** (11 required + 3 optional)
- **15 Orchestrated Workflows**
- **33 Core Tasks**
- **31 Quality Checklists**
- **18 Professional Templates**

### Critical Innovation: Section-Driven Development

The pack introduces **section-driven development** (analogous to BMad's story-driven approach), enabling:
- Incremental chapter writing in 2-5 page sections
- Parallel section development when dependencies allow
- Earlier feedback and quality gates
- Progress tracking at granular level ("5 of 8 sections complete")

---

## Complete Workflow Overview

### End-to-End Journey: Idea → Published Book

```
PHASE 1: IDEATION & PLANNING (20-33 hours)
├─ 1. Concept Development (You + Business Analyst optional)
├─ 2. Book Planning Workflow
│  ├─ Book Publisher: Draft Proposal
│  ├─ Instructional Designer: Design Outline
│  ├─ Instructional Designer: Validate Learning Path
│  ├─ Technical Editor: Editorial Review
│  └─ Book Publisher: Publisher Format Check
└─ OUTPUT: Approved book outline (manuscript/planning/book-outline-final.md)

PHASE 2: RESEARCH (Per Chapter, as needed)
├─ Technical Researcher: Generate Research Queries
├─ [External Research or Auto-Research]
└─ Technical Researcher: Document Findings
└─ OUTPUT: Research reports (manuscript/research/chapter-XX-research.md)

PHASE 3: CHAPTER DEVELOPMENT (Section-Driven: 54-123 hours per chapter)
├─ 3.1 Chapter Outline Creation (2-4 hours)
│  └─ Tutorial Architect: Create chapter outline
│
├─ 3.2 Section Planning Workflow (6-11 hours)
│  ├─ Tutorial Architect: Analyze Chapter Structure
│  ├─ Tutorial Architect: Identify Section Boundaries (5-8 sections)
│  ├─ Tutorial Architect: Create Section Plans
│  ├─ Instructional Designer: Validate Learning Flow
│  └─ Tutorial Architect: Finalize Section List
│
├─ 3.3 Section Development Workflow (5.5-10.5 hours PER SECTION, repeatable)
│  ├─ Code Curator: Develop Code Examples
│  ├─ Code Curator: Test Code Examples
│  ├─ Tutorial Architect: Write Section Content (2-5 pages)
│  ├─ Technical Reviewer: Quick Technical Review
│  ├─ Tutorial Architect: Revise Section
│  └─ Tutorial Architect: Verify Acceptance Criteria (DONE)
│  [REPEAT for each section 1-8]
│
└─ 3.4 Chapter Assembly Workflow (13-24 hours)
   ├─ Tutorial Architect: Merge All Sections
   ├─ Tutorial Architect: Improve Transitions
   ├─ Instructional Designer: Validate Learning Flow
   ├─ Technical Reviewer: Full Chapter Review
   ├─ Tutorial Architect: Revise Based on Feedback
   ├─ Technical Editor: Professional Copy Edit
   └─ Tutorial Architect: Finalize Chapter
   └─ OUTPUT: Publisher-ready chapter (manuscript/chapters/chapter-XX-final.md)

[REPEAT PHASE 2-3 for all chapters]

PHASE 4: BOOK-LEVEL REVIEW & POLISH (varies)
├─ Technical Review Workflow (comprehensive)
├─ Incorporate Review Feedback Workflow
└─ Technical Editor: Final manuscript polish

PHASE 5: PUBLICATION PREPARATION - PACKTPUB (10-19 hours)
├─ 5.1 Format Conversion (2-4 hours)
│  ├─ Manuscript Formatter: Run format-for-packtpub.md
│  │  ├─ validate-manuscript.py (pre-check)
│  │  ├─ Pandoc conversion (Markdown → Word)
│  │  ├─ apply-packt-styles-v6.py (77 [PACKT] styles)
│  │  └─ verify-packt-document.py (post-check)
│  └─ OUTPUT: formatted-chapters/ with .docx files
│
├─ 5.2 Format Validation (2-4 hours)
│  ├─ Technical Editor: Verify PacktPub SharePoint format
│  ├─ Check chapter structure (What You'll Learn, Prerequisites, Summary, Q&A)
│  └─ Validate [PACKT] style application
│
├─ 5.3 Code Validation (3-6 hours)
│  ├─ Code Curator: Test all code examples
│  └─ Verify repository structure (chapter-XX/ folders)
│
├─ 5.4 Learning Objectives Summary (2-3 hours)
│  └─ Instructional Designer: Create learning objectives summary
│
├─ 5.5 SharePoint Package Preparation (2-4 hours)
│  ├─ Book Publisher: Prepare submission package
│  │  ├─ /ChapterFiles/ (Word .docx with [PACKT] styles)
│  │  ├─ /CodeFiles/ (organized by chapter)
│  │  ├─ /ImageFiles/ (300 DPI, proper captions)
│  │  ├─ author-questionnaire.md
│  │  └─ learning-objectives-summary.md
│  └─ OUTPUT: submission-package/packtpub-submission/
│
└─ 5.6 Final Validation (1-2 hours)
   ├─ Book Publisher: Run packtpub-submission-checklist
   └─ Book Publisher: Create submission checklist document
   └─ OUTPUT: Ready for SharePoint upload

OUTCOME: Complete PacktPub-ready manuscript with code repository
```

---

## Phase-by-Phase Breakdown

### PHASE 1: Book Planning (20-33 hours)

**Objective**: Transform book concept into approved, pedagogically sound outline

#### Step 1.1: Draft Proposal (4-8 hours)
- **Agent**: Book Publisher
- **Command**: `*create-proposal`
- **Template**: `book-proposal-tmpl.yaml`
- **Deliverable**: `manuscript/planning/book-proposal.md`
- **Content**:
  - Market analysis
  - Competitive titles
  - Target audience profile
  - Unique value proposition
  - High-level chapter list
  - Author platform
  - Timeline

#### Step 1.2: Design Book Outline (8-12 hours)
- **Agent**: Instructional Designer
- **Command**: `*create-book-outline`
- **Task**: `design-book-outline.md`
- **Template**: `book-outline-tmpl.yaml`
- **Deliverable**: `manuscript/planning/book-outline.md`
- **Content**:
  - Learning progression across chapters
  - Prerequisites per chapter
  - Main topics and subtopics
  - Exercise strategy
  - Difficulty curve
- **Key Principle**: Pedagogical soundness (Bloom's Taxonomy progression)

#### Step 1.3: Validate Learning Path (3-5 hours)
- **Agent**: Instructional Designer
- **Task**: `validate-learning-flow.md`
- **Checklists**:
  - `learning-objectives-checklist.md`
  - `prerequisite-clarity-checklist.md`
- **Deliverable**: `manuscript/planning/learning-path-validation.md`
- **Validates**:
  - No knowledge gaps between chapters
  - Concepts build logically
  - Exercises progress appropriately
  - Prerequisites are achievable

#### Step 1.4: Editorial Review (3-5 hours)
- **Agent**: Technical Editor
- **Command**: `*review-outline`
- **Deliverable**: `manuscript/planning/book-outline-edited.md`
- **Reviews**:
  - Chapter titles clarity
  - Topic duplication
  - Terminology consistency
  - Publisher best practices

#### Step 1.5: Publisher Format Check (2-3 hours)
- **Agent**: Book Publisher
- **Checklists**: `packtpub-submission-checklist.md`
- **Deliverable**: `manuscript/planning/book-outline-final.md`
- **Verifies**:
  - Chapter count matches guidelines
  - Technical depth appropriate
  - Format follows template
  - Timeline is realistic
- **Status**: **Ready for Chapter Development**

---

### PHASE 2: Research (Per Chapter, as needed)

**Objective**: Gather accurate technical information for chapter content

#### Research Workflow Modes

**Mode 1: Manual Query Generation** (Copy/Paste)
1. Technical Researcher: `*generate-queries {topic}`
2. Author conducts external research (Perplexity, web search)
3. Technical Researcher: `*import-research`
4. Deliverable: `manuscript/research/chapter-XX-research.md`

**Mode 2: Research Import** (Existing Findings)
1. Author provides notes/interviews/documentation
2. Technical Researcher: `*import-research`
3. Interactive elicitation workflow
4. Deliverable: Structured research report

**Mode 3: Automated Research** (AI-Powered)
1. Technical Researcher: `*research-auto {topic}`
2. Auto-detects available tools (WebSearch, MCP)
3. Executes queries autonomously
4. Synthesizes findings across sources
5. Deliverable: Auto-populated research report

**Supporting Tasks**:
- `create-book-research-queries.md`
- `generate-research-questions.md`
- `research-technical-topic.md`
- `execute-research-with-tools.md`

**Template**: `book-research-report-tmpl.yaml`
**Checklist**: `research-quality-checklist.md`

---

### PHASE 3: Chapter Development (Section-Driven)

**Total Time**: 54-123 hours per chapter (varies by complexity and section count)

#### 3.1: Create Chapter Outline (2-4 hours)

- **Agent**: Tutorial Architect
- **Command**: `*outline-chapter`
- **Task**: `create-chapter-outline.md`
- **Template**: `chapter-outline-tmpl.yaml`
- **Deliverable**: `manuscript/outlines/chapter-XX-outline.md`
- **Content**:
  - Chapter title and learning objectives
  - Prerequisites
  - Main sections (high-level)
  - Code examples identified
  - Exercise plan
  - Estimated page count

---

#### 3.2: Section Planning Workflow (6-11 hours)

**Purpose**: Break chapter into deliverable section units (BMad story analog)

##### Step 3.2.1: Analyze Chapter (1-2 hours)
- **Agent**: Tutorial Architect
- **Action**: Review chapter outline structure
- **Identifies**: Natural breaking points, concept boundaries
- **Deliverable**: `section-analysis.md`

##### Step 3.2.2: Identify Section Boundaries (1-2 hours)
- **Agent**: Tutorial Architect
- **Action**: Break chapter into 5-8 logical sections
- **Criteria**: Each section = 2-5 pages, 1-2 concepts, 1-3 code examples
- **Deliverable**: `preliminary-section-list.md`

##### Step 3.2.3: Create Section Plans (2-4 hours)
- **Agent**: Tutorial Architect
- **Template**: `section-plan-tmpl.yaml`
- **Task**: `create-doc.md` with section-plan template
- **Checklist**: `section-plan-checklist.md`
- **Deliverable**: `section-plans/section-{n}.md` for each section
- **Each Plan Contains**:
  - Section title
  - Learning objectives (1-2 max)
  - Prerequisites
  - Content plan
  - Code examples needed
  - Success criteria (acceptance criteria)
  - Dependencies on other sections

##### Step 3.2.4: Validate Learning Flow (1-2 hours)
- **Agent**: Instructional Designer
- **Validates**:
  - Sections scaffold properly
  - No learning gaps
  - Prerequisites met in order
  - Section granularity appropriate
- **Deliverable**: `section-flow-validation.md`

##### Step 3.2.5: Finalize Section List (1 hour)
- **Agent**: Tutorial Architect
- **Action**: Incorporate feedback, adjust order/prerequisites
- **Deliverable**: `manuscript/sections/chapter-XX-section-list.md`
- **Content**: Prioritized section list with dependencies, parallel-development flags

---

#### 3.3: Section Development Workflow (5.5-10.5 hours per section)

**Purpose**: Complete development of ONE section (the "story" unit)

**REPEAT THIS WORKFLOW FOR EACH SECTION (typically 5-8 times per chapter)**

##### Step 3.3.1: Develop Code Examples (1-2 hours)
- **Agent**: Code Curator
- **Command**: `*create-example`
- **Task**: `create-code-example.md`
- **Template**: `code-example-tmpl.yaml`
- **Deliverable**: `code-examples/chapter-XX/section-YY/`
- **Creates**:
  - Clean, idiomatic code
  - Error handling
  - Inline comments
  - Tests for code

##### Step 3.3.2: Test Code Examples (30 min - 1 hour)
- **Agent**: Code Curator
- **Task**: `test-code-examples.md`
- **Checklist**: `code-testing-checklist.md`
- **Validates**:
  - Correct output
  - Edge cases handled
  - Linting passes
  - Security checks pass
- **Deliverable**: Test results, bug fixes committed

##### Step 3.3.3: Write Section Content (2-4 hours)
- **Agent**: Tutorial Architect
- **Requires**: `section-plan.md`, code examples, `chapter-outline.md`
- **Action**: Write 2-5 page section
- **Content**:
  - Concept explanation
  - Tutorial walkthrough with code inline
  - Practical applications
  - Prerequisites referenced
  - Connections to previous/next sections
- **Deliverable**: `manuscript/sections/chapter-XX/section-YY-draft.md`

##### Step 3.3.4: Quick Technical Review (30 min - 1 hour)
- **Agent**: Technical Reviewer
- **Checklist**: `technical-accuracy-checklist.md` (focused review)
- **Validates**:
  - Technical accuracy
  - Code correctness
  - Complete explanations
  - Security issues
  - Bad practices
- **Deliverable**: `section-review-notes.md` (critical/major/minor issues)

##### Step 3.3.5: Revise Section (1-2 hours)
- **Agent**: Tutorial Architect
- **Action**: Address review feedback
- **Coordinates**: Code Curator if code changes needed
- **Deliverable**: Updated `section-draft.md`

##### Step 3.3.6: Finalize Section (30 min)
- **Agent**: Tutorial Architect
- **Checklist**: `section-completeness-checklist.md`
- **Validates**:
  - Section length (2-5 pages)
  - Learning objectives addressed
  - Code integrated and explained
  - Tutorial quality
  - Transitions present
  - Technical accuracy confirmed
  - Readability verified
- **Deliverable**: `manuscript/sections/chapter-XX/section-YY-final.md`
- **Status**: Mark section as **DONE** in section list

**CRITICAL**: Section is only marked DONE when ALL acceptance criteria from section plan are met.

**Note**: Sections with no dependencies can be developed in parallel.

---

#### 3.4: Chapter Assembly Workflow (13-24 hours)

**Purpose**: Integrate all completed sections into cohesive chapter (BMad Sprint Review analog)

##### Step 3.4.1: Merge Sections (1-2 hours)
- **Agent**: Tutorial Architect
- **Task**: `merge-sections.md`
- **Action**: Systematically merge all completed sections
- **Preserves**: Section content (no rewriting during merge)
- **Adds**: Chapter introduction (if not in section 1), chapter summary (if not in final section)
- **Deliverable**: `manuscript/chapters/chapter-XX-integrated.md`

##### Step 3.4.2: Improve Transitions (2-3 hours)
- **Agent**: Tutorial Architect
- **Task**: `enhance-transitions.md`
- **Action**:
  - Add bridging paragraphs between sections
  - Ensure smooth concept flow
  - Verify prerequisites fulfilled
  - Add cross-references
- **Deliverable**: Updated `chapter-integrated.md`

##### Step 3.4.3: Validate Learning Flow (1-2 hours)
- **Agent**: Instructional Designer
- **Task**: `validate-learning-flow.md`
- **Validates**:
  - Chapter builds concepts logically
  - Exercises progress appropriately
  - No learning gaps
  - Chapter objectives achieved
- **Deliverable**: `learning-flow-validation.md`

##### Step 3.4.4: Full Technical Review (3-5 hours)
- **Agent**: Technical Reviewer
- **Tasks**: `verify-accuracy.md`, `check-best-practices.md`
- **Checklists**:
  - `technical-accuracy-checklist.md`
  - `security-best-practices-checklist.md`
  - `performance-considerations-checklist.md`
- **Validates**:
  - Technical accuracy across all sections
  - All code tested in sequence
  - Security best practices
  - Performance implications
  - No outdated information
- **Template**: `technical-review-report-tmpl.yaml`
- **Deliverable**: `reviews/technical-review-chapter-XX.md`

##### Step 3.4.5: Revise Chapter (3-6 hours)
- **Agent**: Tutorial Architect
- **Requires**: `learning-flow-validation.md`, `technical-review-report.md`
- **Action**:
  - Address instructional designer feedback
  - Fix critical/major technical issues
  - Update code examples if needed
  - Re-test modified code
- **Deliverable**: Updated `chapter-integrated.md`

##### Step 3.4.6: Professional Copy Edit (2-4 hours)
- **Agent**: Technical Editor
- **Command**: `*edit-chapter`
- **Checklists**:
  - `accessibility-checklist.md`
  - `packtpub-submission-checklist.md` (format check)
- **Improves**:
  - Clarity
  - Terminology consistency
  - Transitions
  - Publisher style compliance
  - Accessibility
- **Deliverable**: `edited-chapter.md` with change summary

##### Step 3.4.7: Finalize Chapter (1-2 hours)
- **Agent**: Tutorial Architect
- **Action**:
  - Review and approve editorial changes
  - Verify technical accuracy preserved
  - Run `chapter-completeness-checklist.md`
- **Deliverable**: `manuscript/chapters/chapter-XX-final.md`
- **Status**: **Ready for Publication**

---

### PHASE 4: Book-Level Review & Polish (Varies)

**After all chapters complete, run comprehensive reviews**

#### Technical Review Workflow (Full Book)
- **Agent**: Technical Reviewer
- **Scope**: Comprehensive book-level validation
- **Validates**:
  - Consistency across chapters
  - No contradictions
  - Technology versions consistent
  - Best practices maintained throughout

#### Incorporate Review Feedback Workflow
- **Agent**: Tutorial Architect (with support)
- **Purpose**: Systematically address reviewer feedback
- **Time**: 4-12 hours per chapter (depends on revision scope)
- **Process**:
  1. Triage feedback (critical/major/minor)
  2. Prioritize changes
  3. Implement revisions
  4. Validate corrections
  5. Re-test affected code

---

### PHASE 5: PacktPub Submission (10-19 hours)

**Objective**: Convert manuscript to PacktPub SharePoint format and prepare submission package

#### 5.1: Format Conversion (2-4 hours)

##### Automated Conversion Workflow

**Tool**: `format-for-packtpub.md` task

**Complete Workflow Script** (Single command):
```bash
cd expansion-packs/bmad-technical-writing/data/packtpub-author-bundle
./format-for-packtpub.sh path/to/manuscript.md output-directory
```

**Manual Step-by-Step** (if needed):

1. **Pre-Conversion Validation**
   ```bash
   python3 validate-manuscript.py manuscript.md images/
   ```
   - Checks: Code blocks ≤30 lines, images 300 DPI/2000px
   - Validates: Proper markdown structure

2. **Pandoc Conversion** (Markdown → Word)
   ```bash
   pandoc -f markdown -t docx \
     --reference-doc="Sample Chapter.docx" \
     -o temp-converted.docx \
     manuscript.md
   ```
   - Uses: PacktPub official template (`Sample Chapter.docx`)
   - Preserves: Structure and formatting

3. **Apply PacktPub Styles**
   ```bash
   python3 apply-packt-styles-v6.py \
     temp-converted.docx \
     formatted-manuscript.docx
   ```
   - Applies: All 77 [PACKT] styles
   - Handles: Table captions (BEFORE tables), figure captions (AFTER images)
   - Styles: Code [PACKT], Bullet [PACKT], Table Column Heading [PACKT], etc.
   - Uses: Headings 1-6 (standard, no [PACKT] suffix)

4. **Post-Conversion Verification**
   ```bash
   python3 verify-packt-document.py formatted-manuscript.docx
   ```
   - Validates: [PACKT] style compliance
   - Checks: Caption placement (critical)
   - Reports: Style coverage

**Output**: `formatted-chapters/` with .docx files

**Critical Resources** (Included):
- `data/packtpub-author-bundle/Sample Chapter.docx` - Official template
- `data/packtpub-author-bundle/CAPTION-PLACEMENT-GUIDE.md` - Caption rules
- Validation scripts (Python)
- Style catalogs (JSON)
- PacktPub official guidelines (PDF)

---

#### 5.2: Format Validation (2-4 hours)

- **Agent**: Technical Editor
- **Checklist**: `packtpub-submission-checklist.md`
- **Validates**:

  **Chapter Structure**:
  - What You Will Learn section (bullet points) ✓
  - Prerequisites section ✓
  - Main content sections ✓
  - Summary section (key takeaways) ✓
  - Q&A section (5-10 questions) ✓
  - Further reading (optional)

  **[PACKT] Style Application**:
  - All 77 styles correctly applied ✓
  - Code blocks: Code [PACKT] + Code End [PACKT] on last line ✓
  - Lists: Bullet [PACKT] / Numbered Bullet [PACKT] ✓
  - Headings: Standard "Heading 1-6" (no [PACKT] suffix) ✓
  - Tables: Table Column Heading [PACKT] / Table Column Content [PACKT] ✓

  **Caption Placement** (CRITICAL):
  - Table captions BEFORE tables ✓
  - Figure captions AFTER images ✓

  **Formatting**:
  - Callout boxes (Note, Tip, Warning) ✓
  - Bold for UI elements ✓
  - Italic for emphasis ✓
  - Numbered lists for procedures ✓

- **Deliverable**: `format-validation-report.md`

---

#### 5.3: Code Validation (3-6 hours)

- **Agent**: Code Curator
- **Checklist**: `code-testing-checklist.md`
- **Validates**:

  **Repository Structure**:
  ```
  book-repository/
  ├── chapter-01/
  │   ├── README.md
  │   ├── example-01/
  │   ├── example-02/
  │   └── tests/
  ├── chapter-02/
  │   ├── README.md
  │   └── ...
  ├── requirements.txt (or package.json)
  └── .gitignore
  ```

  **Code Quality**:
  - All examples tested and working ✓
  - Tests passing ✓
  - Version compatibility verified ✓
  - No hardcoded credentials ✓
  - README per chapter with setup instructions ✓
  - Dependencies documented ✓

- **Deliverable**: `code-validation-report.md`

---

#### 5.4: Learning Objectives Summary (2-3 hours)

- **Agent**: Instructional Designer
- **Checklist**: `learning-objectives-checklist.md`
- **Creates**: Summary of learning objectives across all chapters
- **Ensures**:
  - Objectives use action verbs (Bloom's Taxonomy) ✓
  - Measurable outcomes ✓
  - Clear progression from chapter to chapter ✓
- **Deliverable**: `docs/learning-objectives-summary.md`

---

#### 5.5: SharePoint Package Preparation (2-4 hours)

- **Agent**: Book Publisher
- **Creates**: Complete submission package

**Package Structure**:
```
submission-package/packtpub-submission/
├── ChapterFiles/
│   ├── chapter-01.docx (with [PACKT] styles)
│   ├── chapter-02.docx
│   └── ...
├── CodeFiles/
│   ├── chapter-01/
│   ├── chapter-02/
│   └── ...
├── ImageFiles/
│   ├── chapter-01/
│   │   ├── figure-01-description.png (300 DPI)
│   │   └── ...
│   └── ...
├── author-questionnaire.md
└── learning-objectives-summary.md
```

**Naming Conventions**:
- Chapters: `chapter-XX.docx` or `chapter-XX-title.docx`
- Images: `chapterXX-figureYY-description.png`
- Code: Organized by chapter folders

---

#### 5.6: Final Validation (1-2 hours)

- **Agent**: Book Publisher
- **Checklist**: `packtpub-submission-checklist.md` (comprehensive)
- **Validates**:
  - All chapters present ✓
  - Code tested ✓
  - Images high-res (300 DPI) ✓
  - Learning objectives clear ✓
  - Q&A sections included ✓
  - Author questionnaire complete ✓
  - Package structure correct ✓
- **Deliverable**: `docs/packtpub-submission-checklist-final.md`
- **Status**: **Ready for SharePoint Upload**

---

## Agent Reference Guide

### Core Agents (Required)

#### 1. Instructional Designer 🎓
- **Name**: Instructional Designer
- **ID**: `instructional-designer`
- **Activation**: `/bmad-tw:instructional-designer`
- **Role**: Learning architecture and pedagogical structure expert
- **Use When**: Designing book outlines, learning objectives, prerequisite mapping, scaffolding
- **Key Commands**:
  - `*create-book-outline` - Design pedagogical book outline
  - `*create-learning-objectives` - Define measurable outcomes
  - `*design-learning-path` - Map prerequisites
  - `*analyze-difficulty-curve` - Validate progression
- **Dependencies**:
  - Tasks: `design-book-outline.md`, `create-learning-objectives.md`
  - Templates: `book-outline-tmpl.yaml`, `chapter-outline-tmpl.yaml`
  - Checklists: `learning-objectives-checklist.md`, `prerequisite-clarity-checklist.md`
  - Data: `learning-frameworks.md` (Bloom's Taxonomy)

#### 2. Tutorial Architect 📝
- **Name**: Tutorial Architect
- **ID**: `tutorial-architect`
- **Activation**: `/bmad-tw:tutorial-architect`
- **Role**: Hands-on instruction specialist and chapter writing lead
- **Use When**: Creating tutorials, outlining chapters, writing section content, assembling chapters
- **Key Commands**:
  - `*outline-chapter` - Create chapter outline
  - `*create-tutorial` - Design hands-on tutorial
  - `*write-walkthrough` - Step-by-step guide
  - `*write-summary` - Chapter recap
- **Dependencies**:
  - Tasks: `create-chapter-outline.md`, `write-chapter-draft.md`, `develop-tutorial.md`
  - Templates: `chapter-outline-tmpl.yaml`, `section-plan-tmpl.yaml`, `tutorial-section-tmpl.yaml`
  - Checklists: `tutorial-effectiveness-checklist.md`, `chapter-completeness-checklist.md`

#### 3. Code Curator 🔧
- **Name**: Code Curator
- **ID**: `code-curator`
- **Activation**: `/bmad-tw:code-curator`
- **Role**: Code example development, testing, and quality assurance
- **Use When**: Creating code examples, testing code, repository setup, version management
- **Key Commands**:
  - `*create-example` - Develop code example
  - `*test-examples` - Test all code
  - `*setup-repository` - Initialize code repository
  - `*check-versions` - Verify version compatibility
- **Dependencies**:
  - Tasks: `create-code-example.md`, `test-code-examples.md`
  - Templates: `code-example-tmpl.yaml`
  - Checklists: `code-testing-checklist.md`, `code-quality-checklist.md`, `security-best-practices-checklist.md`
  - Data: `code-style-guides.md`

#### 4. Technical Reviewer 🔍
- **Name**: Technical Reviewer
- **ID**: `technical-reviewer`
- **Activation**: `/bmad-tw:technical-reviewer`
- **Role**: Technical accuracy verification and best practices validation
- **Use When**: Reviewing sections, chapters, validating code, security audits
- **Key Commands**:
  - `*review-section` - Quick section review
  - `*review-chapter` - Full chapter review
  - `*verify-code` - Code accuracy check
  - `*security-audit` - Security review
- **Dependencies**:
  - Tasks: `verify-accuracy.md`, `check-best-practices.md`
  - Templates: `technical-review-report-tmpl.yaml`
  - Checklists: `technical-accuracy-checklist.md`, `security-best-practices-checklist.md`, `performance-considerations-checklist.md`

#### 5. Technical Editor ✍️
- **Name**: Technical Editor
- **ID**: `technical-editor`
- **Activation**: `/bmad-tw:technical-editor`
- **Role**: Clarity improvement, style consistency, publisher formatting
- **Use When**: Polishing chapters, ensuring publisher compliance, accessibility review
- **Key Commands**:
  - `*edit-chapter` - Professional copy edit
  - `*check-style` - Style consistency
  - `*verify-format` - Publisher format check
  - `*review-accessibility` - Accessibility review
- **Dependencies**:
  - Checklists: `accessibility-checklist.md`, `readability-checklist.md`, `inclusive-language-checklist.md`
  - Data: `publisher-guidelines.md`, `technical-writing-standards.md`

#### 6. Book Publisher 📦
- **Name**: Book Publisher
- **ID**: `book-publisher`
- **Activation**: `/bmad-tw:book-publisher`
- **Role**: Publication preparation, manuscript packaging, publisher-specific formatting
- **Use When**: Creating proposals, formatting for publishers, submission preparation
- **Key Commands**:
  - `*create-proposal` - Draft book proposal
  - `*format-packtpub` - PacktPub formatting
  - `*format-oreilly` - O'Reilly formatting
  - `*prepare-submission` - Submission package
- **Dependencies**:
  - Tasks: `format-for-packtpub.md`, `package-for-publisher.md`
  - Templates: `book-proposal-tmpl.yaml`
  - Checklists: `packtpub-submission-checklist.md`, `oreilly-format-checklist.md`, `manning-meap-checklist.md`
  - Data: `publisher-guidelines.md`

#### 7. API Documenter 📚
- **Name**: API Documenter
- **ID**: `api-documenter`
- **Activation**: `/bmad-tw:api-documenter`
- **Role**: API reference documentation, technical specifications, glossaries
- **Use When**: Creating appendices, API docs, glossaries, technical references
- **Key Commands**:
  - `*document-api` - Generate API reference
  - `*create-glossary` - Build glossary
  - `*create-appendix` - Create appendix
- **Dependencies**:
  - Tasks: `generate-api-docs.md`, `build-glossary.md`, `create-appendix.md`
  - Templates: `api-reference-tmpl.yaml`, `glossary-entry-tmpl.yaml`, `appendix-tmpl.yaml`

#### 8. Screenshot Specialist 📸
- **Name**: Screenshot Specialist
- **ID**: `screenshot-specialist`
- **Activation**: `/bmad-tw:screenshot-specialist`
- **Role**: Visual documentation, diagrams, screenshot planning, annotations
- **Use When**: Planning screenshots, creating diagrams, managing images
- **Key Commands**:
  - `*plan-screenshots` - Create screenshot plan
  - `*design-diagram` - Design technical diagram
  - `*annotate-images` - Add annotations
- **Dependencies**:
  - Tasks: `take-screenshots.md`, `design-diagram-set.md`
  - Templates: `diagram-spec-tmpl.yaml`
  - Checklists: `screenshot-quality-checklist.md`, `diagram-clarity-checklist.md`

#### 9. Exercise Creator 🏋️
- **Name**: Exercise Creator
- **ID**: `exercise-creator`
- **Activation**: `/bmad-tw:exercise-creator`
- **Role**: Practice problems, assessments, exercises aligned with learning objectives
- **Use When**: Creating end-of-chapter exercises, practice problems, solutions
- **Key Commands**:
  - `*design-exercises` - Create exercise set
  - `*create-solutions` - Develop solutions
  - `*validate-difficulty` - Check difficulty progression
- **Dependencies**:
  - Tasks: `design-exercises.md`, `create-solutions.md`
  - Templates: `exercise-set-tmpl.yaml`
  - Checklists: `exercise-difficulty-checklist.md`

#### 10. Technical Researcher 🔬
- **Name**: Dr. Research
- **ID**: `technical-researcher`
- **Activation**: `/bmad-tw:technical-researcher`
- **Role**: Chapter research, query generation, automated research, findings documentation
- **Use When**: Researching chapter topics, gathering technical information
- **Key Commands**:
  - `*generate-queries {topic}` - Generate research queries (manual workflow)
  - `*research-auto {topic}` - Automated research (AI-powered)
  - `*import-research` - Import existing findings
  - `*document-findings` - Create research report
- **Modes**:
  - **Manual**: Generate queries → copy/paste to external tools → import results
  - **Import**: Accept user notes/interviews → structure with elicitation
  - **Automated**: Auto-detect tools → execute queries → synthesize findings
- **Dependencies**:
  - Tasks: `create-book-research-queries.md`, `research-technical-topic.md`, `execute-research-with-tools.md`
  - Templates: `book-research-report-tmpl.yaml`
  - Checklists: `research-quality-checklist.md`

#### 11. Book Analyst 📖 (Brownfield)
- **Name**: Book Analyst
- **ID**: `book-analyst`
- **Activation**: `/bmad-tw:book-analyst`
- **Role**: Existing book analysis, revision planning, edition updates, pattern extraction
- **Use When**: 2nd/3rd editions, version updates, adding chapters to existing books
- **Key Commands**:
  - `*analyze-book` - Analyze existing book
  - `*plan-revision` - Create revision plan
  - `*extract-patterns` - Extract style patterns
  - `*incorporate-feedback` - Apply reviewer feedback
- **Dependencies**:
  - Tasks: `analyze-existing-book.md`, `plan-book-revision.md`, `extract-code-patterns.md`
  - Templates: `book-analysis-report-tmpl.yaml`, `revision-plan-tmpl.yaml`
  - Checklists: `version-update-checklist.md`, `revision-completeness-checklist.md`

---

### Optional Agents (Advanced Scenarios)

#### 12. Learning Path Designer 🗺️ (Optional)
- **ID**: `learning-path-designer`
- **Use When**: Complex prerequisite mapping, multi-book series, advanced scaffolding
- **Can Merge With**: Instructional Designer (for simpler deployments)
- **Commands**: `*map-learning-path`, `*validate-prerequisites`, `*design-progression`

#### 13. Sample Code Maintainer 🔧 (Optional)
- **ID**: `sample-code-maintainer`
- **Use When**: Extensive code repositories, CI/CD pipelines, automated testing
- **Can Merge With**: Code Curator (for simpler deployments)
- **Commands**: `*setup-ci-cd`, `*manage-dependencies`, `*automate-testing`

#### 14. Version Manager 🔢 (Optional)
- **ID**: `version-manager`
- **Use When**: Multi-version compatibility matrices, platform-specific code
- **Can Merge With**: Code Curator (for simpler deployments)
- **Commands**: `*test-versions`, `*manage-matrix`, `*handle-platform-code`

---

## Supporting Tasks Analysis

### 33 Core Tasks by Category

#### Planning Tasks (8)
1. `design-book-outline.md` - Create pedagogical book outline
2. `create-chapter-outline.md` - Plan chapter structure
3. `create-learning-objectives.md` - Define measurable outcomes
4. `brainstorm-chapter-ideas.md` - Generate chapter concepts
5. `brainstorm-section-topics.md` - Generate section ideas
6. `analyze-difficulty-curve.md` - Validate progression
7. `map-prerequisites.md` - Map prerequisite dependencies
8. `design-assessment-strategy.md` - Plan exercises and assessments

#### Writing Tasks (10)
9. `write-chapter-draft.md` - Complete chapter manuscript
10. `develop-tutorial.md` - Hands-on tutorial creation
11. `write-walkthrough.md` - Step-by-step guide
12. `write-introduction.md` - Chapter introduction
13. `write-summary.md` - Chapter summary
14. `merge-sections.md` - Integrate sections into chapter
15. `enhance-transitions.md` - Improve section transitions
16. `expand-outline-to-draft.md` - Transform outline to content
17. `generate-explanation-variants.md` - Alternative explanations
18. `synthesize-research-notes.md` - Convert research to content

#### Code Tasks (3)
19. `create-code-example.md` - Develop code example
20. `test-code-examples.md` - Test all code
21. `design-exercises.md` - Create practice problems

#### Review Tasks (3)
22. `verify-accuracy.md` - Technical accuracy check
23. `check-best-practices.md` - Best practices validation
24. `execute-checklist.md` - Run quality checklist

#### Research Tasks (4)
25. `create-book-research-queries.md` - Generate research queries
26. `generate-research-questions.md` - Deep questions (Perplexity-style)
27. `research-technical-topic.md` - Systematic research
28. `execute-research-with-tools.md` - Automated research

#### Specialist Tasks (8)
29. `generate-api-docs.md` - API reference creation
30. `build-glossary.md` - Glossary compilation
31. `take-screenshots.md` - Screenshot planning
32. `design-diagram-set.md` - Diagram design
33. `create-solutions.md` - Exercise solutions
34. `create-index-entries.md` - Index generation
35. `create-preface.md` - Book preface
36. `create-appendix.md` - Appendix content

#### Publishing Tasks (5)
37. `format-for-packtpub.md` - PacktPub formatting workflow
38. `package-for-publisher.md` - Submission package
39. `prepare-meap-chapter.md` - Manning MEAP prep
40. `self-publish-prep.md` - Self-publishing preparation
41. `validate-cross-references.md` - Cross-reference check

#### Brownfield Tasks (5)
42. `analyze-existing-book.md` - Existing book analysis
43. `plan-book-revision.md` - Revision planning
44. `extract-code-patterns.md` - Pattern extraction
45. `incorporate-reviewer-feedback.md` - Apply feedback

---

## Workflow Integration Map

### 15 Workflows and Their Relationships

```
GREENFIELD BOOK (NEW BOOK) - COMPLETE SEQUENCE
│
├─ 1. Book Planning Workflow → book-outline-final.md
│  └─ Agents: Book Publisher, Instructional Designer, Technical Editor
│
├─ FOR EACH CHAPTER:
│  │
│  ├─ 2. Research (Optional, per chapter)
│  │  ├─ Technical Researcher: Generate queries
│  │  ├─ [Research execution]
│  │  └─ Technical Researcher: Document findings
│  │
│  ├─ SECTION-DRIVEN APPROACH (15+ page chapters):
│  │  │
│  │  ├─ 3. Section Planning Workflow → section-list.md
│  │  │  └─ Agents: Tutorial Architect, Instructional Designer
│  │  │
│  │  ├─ 4. Section Development Workflow (×5-8 sections) → section-final.md
│  │  │  └─ Agents: Code Curator, Tutorial Architect, Technical Reviewer
│  │  │
│  │  └─ 5. Chapter Assembly Workflow → chapter-final.md
│  │     └─ Agents: Tutorial Architect, Instructional Designer, Technical Reviewer, Technical Editor
│  │
│  └─ TRADITIONAL APPROACH (<12 page chapters):
│     └─ 6. Chapter Development Workflow (Traditional) → chapter-final.md
│        └─ Agents: Tutorial Architect, Code Curator, Technical Reviewer, Technical Editor
│
├─ 7. Code Example Workflow (supporting, per example) → tested code
│  └─ Agent: Code Curator
│
├─ 8. Tutorial Creation Workflow (if standalone tutorials) → tutorial.md
│  └─ Agents: Instructional Designer, Tutorial Architect, Code Curator
│
├─ BOOK-LEVEL REVIEW:
│  │
│  ├─ 9. Technical Review Workflow → technical-review-report.md
│  │  └─ Agents: Technical Reviewer, Code Curator
│  │
│  └─ 10. Incorporate Review Feedback Workflow → revised-chapters
│     └─ Agents: Tutorial Architect, Technical Reviewer
│
└─ PUBLICATION (choose one):
   │
   ├─ 11. PacktPub Submission Workflow → submission-package/
   │  └─ Agents: Manuscript Formatter, Technical Editor, Code Curator, Instructional Designer, Book Publisher
   │
   ├─ 12. O'Reilly Submission Workflow → oreilly-package/
   │  └─ Agents: Book Publisher, Technical Editor
   │
   ├─ 13. Manning MEAP Workflow → meap-package/
   │  └─ Agents: Book Publisher, Technical Editor
   │
   └─ 14. Self-Publishing Workflow → self-pub-package/
      └─ Agents: Book Publisher, Technical Editor

BROWNFIELD BOOK (EXISTING BOOK UPDATE)
│
├─ 15. Book Edition Update Workflow → revision-plan.md
│  └─ Agents: Book Analyst, Version Manager, Technical Reviewer, Technical Editor
│
└─ 16. Add Chapter to Existing Book Workflow → integrated-chapter.md
   └─ Agents: Book Analyst, Instructional Designer, standard chapter agents
```

---

## Time Estimates and Planning

### Complete Book Time Estimates

**Assumptions**:
- 12-chapter book
- Average 20 pages per chapter
- Section-driven approach
- PacktPub submission

#### Planning Phase
- Book Planning Workflow: **20-33 hours**
  - Proposal: 4-8 hours
  - Outline: 8-12 hours
  - Validation: 3-5 hours
  - Editorial: 3-5 hours
  - Publisher check: 2-3 hours

#### Development Phase (Per Chapter)
- Research (optional): **2-6 hours**
- Section Planning: **6-11 hours**
- Section Development (6 sections × 8 hours avg): **48 hours**
- Chapter Assembly: **13-24 hours**
- **Total per chapter**: **69-89 hours**
- **12 chapters**: **828-1068 hours**

#### Review Phase
- Technical Review (per chapter): **3-5 hours** × 12 = **36-60 hours**
- Incorporate Feedback: **4-12 hours** × 12 = **48-144 hours**
- **Total**: **84-204 hours**

#### Publishing Phase
- PacktPub formatting: **10-19 hours**

#### Grand Total (Greenfield Book)
**Min**: 942 hours (≈ 24 weeks at 40 hrs/week)
**Max**: 1324 hours (≈ 33 weeks at 40 hrs/week)

**Realistic Estimate for Solo Author**: **6-9 months** (including breaks, research, rework)

---

### Time-Saving Strategies

1. **Parallel Section Development**
   - Sections without dependencies can be written simultaneously
   - Reduces wall-clock time (though not effort)

2. **Traditional Approach for Short Chapters**
   - Chapters <12 pages: use traditional workflow (28-51 hours vs 54-123 hours)
   - Saves 26-72 hours per short chapter

3. **Optional Agents**
   - Skip optional agents if not needed (Learning Path Designer, Version Manager)
   - Focus effort on core 10 agents

4. **Research Automation**
   - Use automated research mode when possible
   - Saves manual query generation + external research time

5. **Code Repository Setup**
   - Set up CI/CD early (Sample Code Maintainer)
   - Automate testing throughout (saves hours per chapter)

---

## Best Practices and Recommendations

### 1. Workflow Selection

**When to Use Section-Driven Approach**:
- ✓ Chapters 15+ pages
- ✓ Complex topics requiring incremental development
- ✓ Want progress tracking at granular level
- ✓ Need parallel development capability
- ✓ Prefer iterative story-driven approach
- ✓ Want to review work-in-progress before full chapter done

**When to Use Traditional Approach**:
- ✓ Short chapters (<12 pages)
- ✓ Simple reference sections
- ✓ Author prefers writing full chapter at once
- ✓ Chapter already partially written

### 2. Quality Gates - Never Skip!

**Critical Quality Gates**:
1. **Book Outline Approved** - Don't write chapters until outline validated
2. **Section Plans Complete** - Don't write until section boundaries clear
3. **Code Tested** - Never write tutorials for untested code
4. **Technical Review Passed** - Address critical issues before copy edit
5. **Editorial Polish** - Maintain author voice during edits
6. **PacktPub Validation** - Run all validation scripts before submission

**Why Quality Gates Matter**:
- Catch issues early (cheaper to fix)
- Prevent downstream rework
- Ensure pedagogical soundness
- Maintain consistency
- Meet publisher standards

### 3. Agent Coordination

**Handoff Best Practices**:
- Save outputs to specified locations (agents depend on them)
- Use handoff prompts to communicate context
- Follow workflow sequence (agents build on prior work)
- Mark deliverables as DONE when criteria met

**Parallel Development**:
- Sections without dependencies can be developed in parallel
- Check section plan for dependency flags
- Coordinate code changes across sections

### 4. PacktPub-Specific Tips

**Critical Success Factors**:
1. **Caption Placement** (CRITICAL):
   - Table captions BEFORE tables
   - Figure captions AFTER images
   - See `CAPTION-PLACEMENT-GUIDE.md`

2. **Style Application**:
   - Use automated scripts (`apply-packt-styles-v6.py`)
   - Verify with `verify-packt-document.py`
   - All 77 [PACKT] styles must be applied

3. **Code Examples**:
   - Split long code blocks (≤30 lines preferred)
   - Use Code [PACKT] + Code End [PACKT]
   - Test in fresh environment

4. **Chapter Structure**:
   - Always include "What You Will Learn"
   - Prerequisites explicit
   - Summary and Q&A sections required
   - Q&A should test learning objectives

5. **Images**:
   - 300 DPI minimum
   - PNG or JPEG
   - Clear, readable text
   - Annotations for important areas
   - Validate with `validate-manuscript.py`

### 5. Research Workflow Tips

**When to Use Each Mode**:
- **Manual**: Best for specialized technical domains, author has expertise
- **Import**: Converting conference notes, expert interviews, existing research
- **Automated**: Quick research, broad topics, AI tools available

**Research Quality**:
- Always cite sources
- Assess source credibility
- Document research date (technology changes)
- Keep research reports in `manuscript/research/`

### 6. Code Quality Standards

**Before Writing Tutorials**:
- ✓ Code tested and passing
- ✓ Error handling included
- ✓ Inline comments present
- ✓ Security reviewed
- ✓ Linting passed
- ✓ Works on target platforms

**Repository Best Practices**:
- Organize by chapter folders
- README per chapter
- Dependencies documented
- CI/CD setup (optional but recommended)
- No hardcoded credentials
- .gitignore configured

### 7. Common Pitfalls to Avoid

**Planning Phase**:
- ❌ Skipping learning path validation
- ❌ Assuming too much prerequisite knowledge
- ❌ Uneven difficulty curve
- ❌ Writing chapters before outline approved

**Development Phase**:
- ❌ Writing tutorials for untested code
- ❌ Skipping section plans (section-driven approach)
- ❌ Not marking sections DONE when criteria met
- ❌ Rewriting content during chapter assembly (preserve sections!)

**Review Phase**:
- ❌ Skipping technical review
- ❌ Ignoring critical issues
- ❌ Copy editing before technical review
- ❌ Not re-testing code after changes

**Publishing Phase**:
- ❌ Missing "What You Will Learn" sections (PacktPub requirement)
- ❌ Table captions placed AFTER tables (should be BEFORE)
- ❌ Low-resolution screenshots
- ❌ Missing Q&A sections
- ❌ Incomplete author questionnaire
- ❌ Not running validation scripts

### 8. Workflow Efficiency Tips

**For Solo Authors**:
1. Use section-driven for long chapters (easier to track progress)
2. Complete sections incrementally (avoid marathon writing sessions)
3. Automate code testing (CI/CD saves hours)
4. Use automated research when possible
5. Run validation scripts early and often

**For Team Collaboration**:
1. Assign agents to different team members
2. Parallel section development (multiple authors)
3. Code Curator can work ahead on examples
4. Technical Reviewer can review sections as completed
5. Clear handoff points between agents

**Time Management**:
1. Block 2-4 hour chunks for section writing
2. Write code first, then explanations
3. Review frequently (catch issues early)
4. Don't skip breaks (cognitive load matters)
5. Budget time for rework (feedback always reveals issues)

---

## Appendix: Quick Reference Commands

### Agent Activation Commands
```bash
# Planning agents
/bmad-tw:instructional-designer
/bmad-tw:book-publisher

# Development agents
/bmad-tw:tutorial-architect
/bmad-tw:code-curator
/bmad-tw:exercise-creator

# Review agents
/bmad-tw:technical-reviewer
/bmad-tw:technical-editor

# Specialist agents
/bmad-tw:api-documenter
/bmad-tw:screenshot-specialist
/bmad-tw:technical-researcher

# Brownfield agent
/bmad-tw:book-analyst

# Optional agents
/bmad-tw:learning-path-designer
/bmad-tw:sample-code-maintainer
/bmad-tw:version-manager
```

### PacktPub Formatting Commands
```bash
# Complete workflow (single command)
./format-for-packtpub.sh manuscript.md output-dir

# Manual step-by-step
python3 validate-manuscript.py manuscript.md images/
pandoc -f markdown -t docx --reference-doc="Sample Chapter.docx" -o temp.docx manuscript.md
python3 apply-packt-styles-v6.py temp.docx formatted.docx
python3 verify-packt-document.py formatted.docx
```

### Critical File Locations
```
manuscript/
├── planning/
│   └── book-outline-final.md
├── outlines/
│   └── chapter-XX-outline.md
├── sections/
│   └── chapter-XX/
│       └── section-YY-final.md
├── chapters/
│   └── chapter-XX-final.md
└── research/
    └── chapter-XX-research.md

code-examples/
└── chapter-XX/
    └── section-YY/

submission-package/packtpub-submission/
├── ChapterFiles/
├── CodeFiles/
├── ImageFiles/
└── learning-objectives-summary.md
```

---

## Conclusion

The BMad Technical Writing Expansion Pack provides a **complete, professional-grade system** for technical book authoring from concept to publication. Key innovations include:

1. **Section-Driven Development** - Incremental, trackable chapter writing
2. **15 Orchestrated Workflows** - Structured agent collaboration
3. **31 Quality Checklists** - Comprehensive quality assurance
4. **PacktPub Automation** - Complete formatting pipeline with validation

**Success Formula**:
- ✓ Follow workflow sequences
- ✓ Never skip quality gates
- ✓ Use section-driven for complex chapters
- ✓ Automate validation (scripts provided)
- ✓ Test code before writing tutorials
- ✓ Research thoroughly
- ✓ Review iteratively

**Time Investment**: 6-9 months for 12-chapter book (solo author, realistic estimate with breaks and rework)

**Result**: Publisher-ready manuscript meeting all PacktPub standards, with tested code repository and comprehensive learning objectives.

---

**Document Version**: 1.0
**Last Updated**: 2025-01-26
**Author**: Claude Code Analysis Agent
**Source**: BMad Technical Writing Expansion Pack v1.1.0
