# Process Flow Diagrams - Technical Writing Expansion Pack

Visual representations of all workflows, agent collaboration patterns, and the complete book authoring lifecycle.

## Table of Contents

- [How to Read These Diagrams](#how-to-read-these-diagrams)
- [High-Level Overview](#high-level-overview)
  - [Book Authoring Lifecycle](#book-authoring-lifecycle)
  - [Agent Collaboration Map](#agent-collaboration-map)
- [Planning Workflows](#planning-workflows)
  - [Book Planning Workflow](#book-planning-workflow)
- [Development Workflows](#development-workflows)
  - [Section-Driven Development Flow](#section-driven-development-flow)
  - [Section Development Workflow](#section-development-workflow)
  - [Chapter Assembly Workflow](#chapter-assembly-workflow)
  - [Tutorial Creation Workflow](#tutorial-creation-workflow)
  - [Code Example Workflow](#code-example-workflow)
- [Review Workflows](#review-workflows)
  - [Technical Review Workflow](#technical-review-workflow)
  - [Incorporate Review Feedback Workflow](#incorporate-review-feedback-workflow)
- [Publishing Workflows](#publishing-workflows)
  - [Publishing Decision Tree](#publishing-decision-tree)
  - [PacktPub Submission Workflow](#packtpub-submission-workflow)
  - [O'Reilly Submission Workflow](#oreilly-submission-workflow)
  - [Manning MEAP Workflow](#manning-meap-workflow)
  - [Self-Publishing Workflow](#self-publishing-workflow)
- [Brownfield Workflows](#brownfield-workflows)
  - [Book Edition Update Workflow](#book-edition-update-workflow)
  - [Add Chapter to Existing Book Workflow](#add-chapter-to-existing-book-workflow)

---

## How to Read These Diagrams

### Diagram Notation

**Node Colors**:

- 🟡 **Yellow (Planning)** - Initial planning and design activities
- 🟠 **Orange (Development)** - Content creation and code development
- 🔵 **Blue (Review)** - Quality assurance and validation activities
- 🟢 **Green (Complete)** - Finished deliverables and outcomes
- ⚪ **White (Decision)** - Decision points requiring evaluation

**Arrow Types**:

- **Solid arrows** → Required sequence (must follow this path)
- **Dotted arrows** -.-> Optional steps (can be included if needed)

**Agent Indicators**:
Each process step shows which agent performs the work:

- `agent-name: Action Description`

### Reading Flow

1. **Start at the top** - Entry point with prerequisites
2. **Follow solid arrows** - Required sequence of steps
3. **Check decision diamonds** - Branching based on outcomes
4. **Note agent handoffs** - Where one agent passes work to another
5. **End at green nodes** - Final deliverables

---

## High-Level Overview

### Book Authoring Lifecycle

Complete journey from book concept to published book.

```mermaid
graph TD
    A[Book Concept] --> B{Greenfield or Brownfield?}
    B -->|New Book| C[Planning Phase]
    B -->|Existing Book| D[Brownfield Analysis]

    C --> E[Book Planning Workflow]
    E --> F[Book Outline Approved]

    D --> G[Book Edition Update Workflow]
    G --> F

    F --> H[Development Phase]
    H --> I{Development Approach?}
    I -->|Section-Driven| J[Section Planning]
    I -->|Chapter-at-Once| K[Chapter Development]

    J --> L[Section Development Loop]
    L --> M{All Sections Done?}
    M -->|No| L
    M -->|Yes| N[Chapter Assembly]

    K --> N

    N --> O[Chapter Complete]
    O --> P{More Chapters?}
    P -->|Yes| H
    P -->|No| Q[Review Phase]

    Q --> R[Technical Review Workflow]
    R --> S[Incorporate Feedback]
    S --> T[Editing Phase]

    T --> U[Technical Editor Polish]
    U --> V[Publishing Phase]

    V --> W{Publisher Type?}
    W -->|PacktPub| X[PacktPub Submission]
    W -->|O'Reilly| Y[O'Reilly Submission]
    W -->|Manning| Z[Manning MEAP]
    W -->|Self-Publish| AA[Self-Publishing Workflow]

    X --> AB[Manuscript Submitted]
    Y --> AB
    Z --> AB
    AA --> AB

    AB --> AC[Book Published!]

    style A fill:#E0E0E0
    style F fill:#FFD700
    style O fill:#98FB98
    style AB fill:#90EE90
    style AC fill:#32CD32
```

**Caption**: The complete book authoring lifecycle showing greenfield and brownfield paths, development approaches, and publishing options.

---

### Agent Collaboration Map

Shows which agents collaborate with which other agents throughout the workflow.

```mermaid
graph LR
    subgraph Planning_Agents
        ID[Instructional Designer]
        TA[Tutorial Architect]
        BP[Book Publisher]
    end

    subgraph Development_Agents
        CC[Code Curator]
        TA2[Tutorial Architect]
        EC[Exercise Creator]
    end

    subgraph Review_Agents
        TR[Technical Reviewer]
        TE[Technical Editor]
    end

    subgraph Specialist_Agents
        AD[API Documenter]
        SS[Screenshot Specialist]
    end

    subgraph Brownfield_Agents
        BA[Book Analyst]
    end

    subgraph Optional_Agents
        LPD[Learning Path Designer]
        SCM[Sample Code Maintainer]
        VM[Version Manager]
    end

    %% Primary collaborations
    ID --> TA2
    ID --> BP
    TA2 --> CC
    CC --> TR
    TR --> TA2
    TA2 --> TE
    TE --> BP
    BP --> AD
    BP --> SS

    %% Specialist integrations
    CC --> EC
    TA2 --> AD
    TA2 --> SS

    %% Brownfield integrations
    BA --> ID
    BA --> TA2
    BA --> CC

    %% Optional agent enhancements
    LPD -.-> ID
    SCM -.-> CC
    VM -.-> CC

    style ID fill:#FFE4B5
    style TA2 fill:#FFE4B5
    style CC fill:#F0E68C
    style TR fill:#ADD8E6
    style TE fill:#ADD8E6
    style BP fill:#90EE90
```

**Caption**: Agent collaboration patterns showing primary workflows (solid) and optional integrations (dotted).

**Key Collaborations**:

- **Instructional Designer → Tutorial Architect**: Passes learning objectives and chapter structure
- **Tutorial Architect → Code Curator**: Requests code examples for tutorials
- **Code Curator → Technical Reviewer**: Submits code for technical accuracy review
- **Technical Reviewer → Tutorial Architect**: Returns review feedback for revisions
- **Tutorial Architect → Technical Editor**: Passes completed content for polish
- **Technical Editor → Book Publisher**: Delivers polished manuscript for publication prep

---

## Planning Workflows

### Book Planning Workflow

Complete book planning from concept to approved outline.

**Workflow Definition**: `workflows/book-planning-workflow.yaml`
**Agents Used**: `book-publisher.md`, `instructional-designer.md`, `technical-editor.md`
**Key Tasks**: `create-doc.md`, `design-book-outline.md`, `validate-learning-flow.md` (Story 7.4)

```mermaid
graph TD
    A[Start: Book Concept] --> B[book-publisher.md: *create-proposal]
    B --> C[instructional-designer.md: *design-outline]
    C --> D[instructional-designer.md: tasks/validate-learning-flow.md]
    D --> E{Prerequisites Flow?}
    E -->|Issues Found| F[instructional-designer.md: Adjust Outline]
    F --> D
    E -->|Valid| G[technical-editor.md: *review-outline]
    G --> H[book-publisher.md: Publisher Format Check]
    H --> I{Meets Requirements?}
    I -->|Needs Changes| J[Adjust for Publisher]
    J --> G
    I -->|Approved| K[Final Outline Approved]
    K --> L[Ready for Chapter Development]

    B -.-> B1[templates/book-proposal-tmpl.yaml]
    C -.-> C1[templates/book-outline-tmpl.yaml]
    D -.-> D1[checklists/prerequisite-clarity-checklist.md]

    style L fill:#90EE90
    style B fill:#FFE4B5
    style C fill:#FFE4B5
    style D fill:#ADD8E6
    style G fill:#ADD8E6
    style H fill:#F0E68C
```

**Time Estimate**: 20-33 hours | **Agents**: Book Publisher, Instructional Designer, Technical Editor

#### Quick Execution Guide

1. **book-publisher.md**: `*create-proposal` → Use `templates/book-proposal-tmpl.yaml` → Output: `manuscript/planning/book-proposal.md`
2. **instructional-designer.md**: `*design-outline` (runs `tasks/design-book-outline.md`) → Use `templates/book-outline-tmpl.yaml` → Output: `manuscript/planning/book-outline.md`
3. **instructional-designer.md**: `tasks/validate-learning-flow.md` → Use `checklists/learning-objectives-checklist.md` and `prerequisite-clarity-checklist.md` → Output: `manuscript/planning/learning-path-validation.md`
4. **technical-editor.md**: `*review-outline` → Editorial review for clarity/consistency → Output: `manuscript/planning/book-outline-edited.md`
5. **book-publisher.md**: Verify publisher requirements (use `checklists/packtpub-submission-checklist.md`, `oreilly-format-checklist.md`, or `manning-meap-checklist.md`) → Output: `manuscript/planning/book-outline-final.md`

**Success Criteria**: Market analysis complete | Learning path validated (no gaps) | Publisher requirements met

---

## Development Workflows

### Section-Driven Development Flow

High-level overview of section-driven approach to chapter development.

```mermaid
graph TD
    A[Chapter Outline Approved] --> B[Section Planning Workflow]
    B --> C[Section List Created]
    C --> D{Select Next Section}
    D --> E[Section Development Workflow]
    E --> F[Section DONE]
    F --> G{More Sections?}
    G -->|Yes| D
    G -->|No| H[All Sections Complete]
    H --> I[Chapter Assembly Workflow]
    I --> J[Chapter DONE]

    %% Parallel development option
    D -.-> D1[Section 1]
    D -.-> D2[Section 2]
    D -.-> D3[Section 3]
    D1 -.-> E
    D2 -.-> E
    D3 -.-> E

    style A fill:#FFD700
    style C fill:#FFE4B5
    style F fill:#98FB98
    style H fill:#90EE90
    style J fill:#32CD32
```

**Caption**: Section-driven development breaks chapters into 2-5 page sections that can be developed independently and in parallel.

**Why Section-Driven?**

- **Manageable scope**: Small sections easier to write
- **Parallel development**: Multiple sections can progress simultaneously
- **Incremental progress**: Each section completion is a milestone
- **Quality focus**: Easier to maintain quality in small chunks

**Typical Chapter**:

- 6-8 sections
- Each section: 2-5 pages
- Total chapter: 18-24 pages

---

### Section Planning Workflow

Break chapter outline into deliverable section units with clear acceptance criteria.

**Workflow Definition**: `workflows/section-planning-workflow.yaml`
**Agents Used**: `tutorial-architect.md`, `instructional-designer.md`
**Key Tasks**: `create-doc.md` (with `section-plan-tmpl.yaml`)

```mermaid
graph TD
    A[Start: Chapter Outline Ready] --> B[tutorial-architect.md: Analyze Chapter Structure]
    B --> C[tutorial-architect.md: Identify Section Boundaries]
    C --> D[tutorial-architect.md: *create-doc with section-plan-tmpl]
    D --> E[instructional-designer.md: Validate Learning Flow]
    E --> F{Flow Issues?}
    F -->|Yes| G[tutorial-architect.md: Adjust Sections]
    G --> D
    F -->|No| H[tutorial-architect.md: Finalize Section List]
    H --> I[Section Plans Ready for Development]

    D -.-> D1[Use section-plan-tmpl.yaml]
    E -.-> E1[Check: Proper scaffolding]
    E -.-> E2[Check: No learning gaps]
    H -.-> H1[Mark parallel-safe sections]

    style I fill:#90EE90
    style B fill:#FFE4B5
    style C fill:#FFE4B5
    style D fill:#FFE4B5
    style E fill:#ADD8E6
    style H fill:#F0E68C
```

**Time Estimate**: 6-11 hours per chapter
**Agents Involved**: Tutorial Architect, Instructional Designer

#### How to Execute This Workflow

**Prerequisites**:
- Chapter outline completed: `manuscript/outlines/chapter-{n}-outline.md`
- Outline includes learning objectives and main topics

**Step 1: Activate Tutorial Architect**
```bash
/bmad-tw:agents:tutorial-architect
```

**Step 2: Analyze Chapter Structure**
- Read chapter outline: `manuscript/outlines/chapter-{n}-outline.md`
- Review learning objectives, main sections, code examples
- Identify natural breaking points for sections (2-5 pages each)
- Consider logical learning progression and dependencies
- **Output**: Create `section-analysis.md` documenting structure

**Step 3: Identify Section Boundaries**
- Break chapter into 5-8 logical sections
- Each section should teach 1-2 concepts and include 1-3 code examples
- Name each section clearly and define what it teaches
- Identify dependencies (which sections must come first)
- **Output**: Create `preliminary-section-list.md`

**Step 4: Create Section Plans**
- **Command**: `*create-doc` (or run `tasks/create-doc.md`)
- **Template**: Use `templates/section-plan-tmpl.yaml`
- For each section, define:
  - Learning objectives (1-2 max)
  - Prerequisites
  - Content plan
  - Code examples needed
  - Success criteria
  - Dependencies
- **Output**: Create `section-plans/section-{n}.md` for each section

**Step 5: Switch to Instructional Designer**
```bash
/bmad-tw:agents:instructional-designer
```

**Step 6: Validate Learning Flow**
- Review all section plans in `section-plans/`
- **Task**: Run `tasks/validate-learning-flow.md` (Story 7.4)
- Verify:
  - Sections scaffold properly (each builds on previous)
  - Prerequisites met in correct order
  - No learning gaps or concept jumps
  - Section granularity is appropriate (not too small/large)
- **Checklists**:
  - `checklists/learning-objectives-checklist.md`
  - `checklists/prerequisite-clarity-checklist.md`
- **Output**: Create `section-flow-validation.md` with approval/recommendations

**Step 7: Finalize Section List** (back to Tutorial Architect)
```bash
/bmad-tw:agents:tutorial-architect
```
- Incorporate instructional designer feedback
- Adjust section order, prerequisites, or granularity if needed
- Create final prioritized section list with dependencies mapped
- Number sections sequentially
- Mark sections that can be developed in parallel
- **Output**: `manuscript/sections/chapter-{n}-section-list.md` (authoritative plan)

**Success Criteria**:
- [ ] 5-8 sections defined
- [ ] Each section has clear learning objective
- [ ] Prerequisites identified for each section
- [ ] Success criteria defined per section
- [ ] Dependencies mapped
- [ ] Learning flow validated (no gaps)
- [ ] Section granularity appropriate (2-5 pages each)

**File Outputs**:
- `section-analysis.md` - Chapter structure analysis
- `preliminary-section-list.md` - Initial section breakdown
- `section-plans/section-{n}.md` - Detailed plan for each section (5-8 files)
- `section-flow-validation.md` - Instructional designer validation
- `manuscript/sections/chapter-{n}-section-list.md` - Final section list

---

### Section Development Workflow

Complete development of one section (the "story" unit of book writing).

**Workflow Definition**: `workflows/section-development-workflow.yaml`
**Agents Used**: `code-curator.md`, `tutorial-architect.md`, `technical-reviewer.md`
**Key Tasks**: `create-code-example.md`, `test-code-examples.md`, `write-section-draft.md` (Story 7.9)

```mermaid
graph TD
    A[Start: Section Plan Ready] --> B[code-curator.md: *create-code-example]
    B --> C[code-curator.md: *test-all-examples]
    C --> D{All Tests Pass?}
    D -->|No| E[code-curator.md: Fix Code]
    E --> C
    D -->|Yes| F[tutorial-architect.md: tasks/write-section-draft.md]
    F --> G[technical-reviewer.md: Quick Review]
    G --> H{Critical Issues?}
    H -->|Yes| I[tutorial-architect.md: Revise Section]
    I --> J[Update Code if Needed?]
    J -->|Yes| K[code-curator.md: Update Code]
    K --> C
    J -->|No| G
    H -->|No| L[tutorial-architect.md: Verify Acceptance Criteria]
    L --> M{Criteria Met?}
    M -->|No| N[Address Missing Items]
    N --> L
    M -->|Yes| O[Section DONE]

    B -.-> B1[Use section plan code list]
    F -.-> F1[Reference section-plan objectives]
    G -.-> G1[checklists/technical-accuracy-checklist.md]
    L -.-> L1[Check section plan success criteria]

    style O fill:#90EE90
    style B fill:#FFE4B5
    style C fill:#FFE4B5
    style F fill:#FFE4B5
    style G fill:#ADD8E6
    style L fill:#F0E68C
```

**Time Estimate**: 5.5-10.5 hours per section
**Agents Involved**: Code Curator, Tutorial Architect, Technical Reviewer

#### How to Execute This Workflow

**Prerequisites**:
- Section plan completed: `section-plans/section-{n}.md`
- Chapter outline available: `manuscript/outlines/chapter-{n}-outline.md`

**Step 1: Activate Code Curator**
```bash
/bmad-tw:agents:code-curator
```

**Step 2: Develop Code Examples**
- **Command**: `*create-code-example` (runs `tasks/create-code-example.md`)
- Read section plan code example requirements
- Create all code examples identified in section plan (typically 1-3 examples)
- Follow coding best practices and add inline comments
- Include error handling
- **Output**: `code/chapter-{n}/section-{n}/example-{name}.{ext}` (1-3 files)
- **Time**: 1-2 hours

**Step 3: Test Code Examples**
- **Command**: `*test-all-examples` (runs `tasks/test-code-examples.md`)
- Verify correct output for each example
- Test edge cases and error handling
- Run linting and security checks
- Document test results
- **Output**: Test results and any bug fixes committed
- **Time**: 30 minutes - 1 hour

**Step 4: Switch to Tutorial Architect**
```bash
/bmad-tw:agents:tutorial-architect
```

**Step 5: Write Section Draft**
- **Task**: Execute `tasks/write-section-draft.md` (Story 7.9 - follow task instructions)
- **Alternative**: If task not yet implemented, use workflow notes from YAML
- **Input Files**:
  - `section-plans/section-{n}.md` (section plan)
  - `code/chapter-{n}/section-{n}/` (code examples from code-curator)
  - `manuscript/outlines/chapter-{n}-outline.md` (chapter context)
- Write 2-5 pages addressing:
  1. Concept explanation (0.5-1 page)
  2. Tutorial walkthrough with code inline (2-3 pages)
  3. Practical applications (0.5-1 page)
  4. Transitions (to previous and next sections)
- **Output**: `manuscript/sections/chapter-{n}/section-{n}-draft.md`
- **Time**: 2-4 hours

**Step 6: Switch to Technical Reviewer**
```bash
/bmad-tw:agents:technical-reviewer
```

**Step 7: Quick Technical Review**
- Read `section-draft.md`
- **Task**: Run `tasks/verify-accuracy.md` (Story 7.4) for focused section review
- Verify technical accuracy, code correctness, completeness
- Check for security issues or bad practices
- **Checklist**: Execute `tasks/execute-checklist.md` with `checklists/technical-accuracy-checklist.md`
- **Output**: `section-{n}-review-notes.md` with findings (critical/major/minor)
- **Time**: 30 minutes - 1 hour

**Step 8: Back to Tutorial Architect for Revisions**
```bash
/bmad-tw:agents:tutorial-architect
```
- Read review notes
- Address all critical and major issues
- Update code examples if needed (coordinate with code-curator if major changes)
- Re-test revised code
- **Output**: Updated `section-{n}-draft.md`
- **Time**: 1-2 hours

**Step 9: Verify and Finalize**
- Verify section meets ALL success criteria from section plan
- Check:
  - [ ] Learning objectives addressed
  - [ ] Code tested and working
  - [ ] Length appropriate (2-5 pages)
  - [ ] Transitions clear
  - [ ] Prerequisites mentioned
- Mark section status as DONE in section list
- **Output**: `manuscript/sections/chapter-{n}/section-{n}-final.md`
- **Time**: 30 minutes

**Success Criteria**:
- [ ] All code examples developed and tested
- [ ] Section draft 2-5 pages
- [ ] Learning objectives from section plan addressed
- [ ] All code examples integrated and explained
- [ ] Technical review passed (no critical issues)
- [ ] All section plan success criteria met

**File Outputs**:
- `code/chapter-{n}/section-{n}/example-{name}.{ext}` - Code examples (1-3 files)
- `manuscript/sections/chapter-{n}/section-{n}-draft.md` - Section draft
- `section-{n}-review-notes.md` - Technical review findings
- `manuscript/sections/chapter-{n}/section-{n}-final.md` - Final section (DONE)

---

### Chapter Assembly Workflow

Merge completed sections into cohesive chapter with full review and polish.

**Workflow Definition**: `workflows/chapter-assembly-workflow.yaml`
**Agents Used**: `tutorial-architect.md`, `instructional-designer.md`, `technical-reviewer.md`, `technical-editor.md`
**Key Tasks**: `merge-sections.md` (Story 7.10), `enhance-transitions.md` (Story 7.10), `validate-learning-flow.md` (Story 7.4), `verify-accuracy.md` (Story 7.4)

```mermaid
graph TD
    A[All Sections DONE] --> B[tutorial-architect.md: tasks/merge-sections.md]
    B --> C[tutorial-architect.md: tasks/enhance-transitions.md]
    C --> D[instructional-designer.md: tasks/validate-learning-flow.md]
    D --> E[technical-reviewer.md: Full Chapter Review]
    E --> F{Critical Issues?}
    F -->|Yes| G[tutorial-architect.md: Revise Chapter]
    G --> H[Update Code if Needed?]
    H -->|Yes| I[code-curator.md: Retest Code]
    I --> E
    H -->|No| E
    F -->|No| J[technical-editor.md: *copy-edit]
    J --> K[tutorial-architect.md: Review Edits]
    K --> L{Approve Edits?}
    L -->|No| M[Discuss with Editor]
    M --> J
    L -->|Yes| N[tutorial-architect.md: execute-checklist.md]
    N --> O{All Criteria Met?}
    O -->|No| P[Address Missing Items]
    P --> N
    O -->|Yes| Q[Chapter Ready for Publication]

    B -.-> B1[Preserve section content]
    C -.-> C1[Add bridging paragraphs]
    D -.-> D1[Check learning progression]
    E -.-> E1[Test all code in sequence]
    J -.-> J1[Maintain author voice]
    N -.-> N1[checklists/chapter-completeness-checklist.md]

    style Q fill:#90EE90
    style B fill:#FFE4B5
    style C fill:#FFE4B5
    style D fill:#ADD8E6
    style E fill:#ADD8E6
    style J fill:#ADD8E6
    style N fill:#F0E68C
```

**Time Estimate**: 13-24 hours per chapter
**Agents Involved**: Tutorial Architect, Instructional Designer, Technical Reviewer, Technical Editor

#### How to Execute This Workflow

**Prerequisites**:
- All chapter sections marked DONE
- All section files in `manuscript/sections/chapter-{n}/section-{n}-final.md`

**Step 1: Activate Tutorial Architect**
```bash
/bmad-tw:agents:tutorial-architect
```

**Step 2: Merge Sections**
- **Task**: Execute `tasks/merge-sections.md` (Story 7.10)
- Systematically merge all completed sections into single chapter file
- Preserve section content (don't rewrite)
- Add chapter introduction (if not in section 1)
- Add chapter summary (if not in final section)
- Verify all sections present in correct order
- **Output**: `manuscript/chapters/chapter-{n}-integrated.md`
- **Time**: 1-2 hours

**Step 3: Enhance Transitions**
- **Task**: Execute `tasks/enhance-transitions.md` (Story 7.10)
- Review transitions between sections
- Add bridging paragraphs where sections feel disconnected
- Ensure smooth flow from one concept to next
- Check prerequisites mentioned in earlier sections are fulfilled
- Add cross-references where helpful
- **Output**: Update `chapter-{n}-integrated.md` with improved transitions
- **Time**: 2-3 hours

**Step 4: Switch to Instructional Designer**
```bash
/bmad-tw:agents:instructional-designer
```

**Step 5: Validate Learning Flow**
- **Task**: Execute `tasks/validate-learning-flow.md` (Story 7.4)
- Verify chapter builds concepts logically
- Check exercises progress from easy to challenging
- Ensure no learning gaps or concept jumps
- Confirm chapter learning objectives (from chapter outline) achieved
- **Output**: `learning-flow-validation.md` with findings
- **Time**: 1-2 hours

**Step 6: Switch to Technical Reviewer**
```bash
/bmad-tw:agents:technical-reviewer
```

**Step 7: Full Chapter Technical Review**
- Read complete `chapter-integrated.md`
- **Tasks**:
  - `tasks/verify-accuracy.md` (Story 7.4) - Technical accuracy
  - `tasks/check-best-practices.md` (Story 7.4) - Best practices
  - `tasks/test-code-examples.md` - Test all code in sequence
  - `tasks/security-audit.md` (Story 7.3) - Security review
- **Checklists**:
  - `checklists/technical-accuracy-checklist.md`
  - `checklists/security-best-practices-checklist.md`
  - `checklists/performance-considerations-checklist.md`
- **Template**: Use `templates/technical-review-report-tmpl.yaml`
- **Output**: `reviews/technical-review-chapter-{n}.md`
- **Time**: 3-5 hours

**Step 8: Back to Tutorial Architect for Revisions**
```bash
/bmad-tw:agents:tutorial-architect
```
- Incorporate all review feedback
- Address learning flow issues from instructional designer
- Fix all critical and major technical issues
- Update code examples if needed (coordinate with code-curator)
- Re-test modified code
- **Output**: Update `chapter-{n}-integrated.md` with all revisions
- **Time**: 3-6 hours

**Step 9: Switch to Technical Editor**
```bash
/bmad-tw:agents:technical-editor
```

**Step 10: Copy Edit Chapter**
- **Command**: `*copy-edit` (or `tasks/copy-edit-chapter.md`)
- Improve clarity and readability
- Check terminology consistency
- Enhance transitions
- Verify publisher style compliance
- Review accessibility requirements
- **Checklists**:
  - `checklists/accessibility-checklist.md`
  - Publisher-specific checklist (packtpub/oreilly/manning)
- **Output**: `edited-chapter.md` with change summary
- **Time**: 2-4 hours

**Step 11: Back to Tutorial Architect for Final Approval**
```bash
/bmad-tw:agents:tutorial-architect
```
- Review and approve editorial changes
- Verify technical accuracy preserved during editing
- **Checklist**: Run `tasks/execute-checklist.md` with `checklists/chapter-completeness-checklist.md`
- Mark chapter status as 'Ready for Publication'
- **Output**: `manuscript/chapters/chapter-{n}-final.md` (publisher-ready)
- **Time**: 1-2 hours

**Success Criteria**:
- [ ] All sections merged in correct order
- [ ] Smooth transitions between sections
- [ ] Learning flow validated (no gaps)
- [ ] Technical review passed (no critical issues)
- [ ] All code tested in sequence
- [ ] Copy editing complete
- [ ] Chapter completeness checklist verified

**File Outputs**:
- `manuscript/chapters/chapter-{n}-integrated.md` - Merged sections
- `learning-flow-validation.md` - Instructional designer validation
- `reviews/technical-review-chapter-{n}.md` - Technical review report
- `edited-chapter.md` - Copy-edited version
- `manuscript/chapters/chapter-{n}-final.md` - Final publisher-ready chapter

---

### Tutorial Creation Workflow

Create comprehensive hands-on tutorials with practice exercises.

**Workflow Definition**: `workflows/tutorial-creation-workflow.yaml`
**Agents Used**: `instructional-designer.md`, `tutorial-architect.md`, `code-curator.md`, `exercise-creator.md`
**Key Tasks**: `develop-tutorial.md`, `create-code-example.md`, `design-exercises.md`

```mermaid
graph TD
    A[Tutorial Topic Defined] --> B[instructional-designer.md: *create-learning-objectives]
    B --> C[tutorial-architect.md: *create-tutorial]
    C --> D[code-curator.md: *create-code-example]
    D --> E[tutorial-architect.md: Write Step-by-Step]
    E --> F[tutorial-architect.md: *add-troubleshooting]
    F --> G[code-curator.md: *test-all-examples end-to-end]
    G --> H{Tutorial Works?}
    H -->|Issues| I[Fix Tutorial Steps]
    I --> G
    H -->|Success| J[exercise-creator.md: *design-exercises]
    J --> K[Tutorial Complete]

    B -.-> B1[templates/learning-objectives-tmpl.yaml]
    C -.-> C1[templates/tutorial-section-tmpl.yaml]
    G -.-> G1[checklists/tutorial-effectiveness-checklist.md]

    style A fill:#E0E0E0
    style K fill:#90EE90
    style D fill:#FFE4B5
    style E fill:#FFE4B5
    style G fill:#ADD8E6
```

**Time Estimate**: 8-12 hours | **Agents**: Instructional Designer, Tutorial Architect, Code Curator, Exercise Creator

#### Quick Execution Guide

1. **instructional-designer.md**: `*create-learning-objectives` (runs `tasks/create-learning-objectives.md`) → Use `templates/learning-objectives-tmpl.yaml`
2. **tutorial-architect.md**: `*create-tutorial` (runs `tasks/develop-tutorial.md`) → Use `templates/tutorial-section-tmpl.yaml`
3. **code-curator.md**: `*create-code-example` for each example → Test individually
4. **tutorial-architect.md**: Write step-by-step instructions, add expected outcomes, write troubleshooting
5. **code-curator.md**: `*test-all-examples` end-to-end → Use `checklists/tutorial-effectiveness-checklist.md`
6. **exercise-creator.md**: `*design-exercises` (runs `tasks/design-exercises.md`) → Use `templates/exercise-set-tmpl.yaml`

---

### Code Example Workflow

Create, test, and validate code examples for technical accuracy, security, and cross-platform compatibility.

**Workflow Definition**: `workflows/code-example-workflow.yaml`
**Agents Used**: `code-curator.md`
**Key Tasks**: `create-code-example.md`, `test-code-examples.md`, `security-audit.md` (Story 7.3), `cross-platform-test.md` (Story 7.3)

```mermaid
graph TD
    A[Code Example Needed] --> B[code-curator.md: *create-code-example]
    B --> C[code-curator.md: Write Unit Tests]
    C --> D[code-curator.md: *test-all-examples]
    D --> E{Tests Pass?}
    E -->|No| F[Debug and Fix]
    F --> D
    E -->|Yes| G[code-curator.md: Add Comments/Output]
    G --> H[code-curator.md: *security-audit]
    H --> I{Security Issues?}
    I -->|Yes| J[Fix Security Issues]
    J --> H
    I -->|No| K[code-curator.md: *optimize-code]
    K --> L[code-curator.md: *cross-platform-test]
    L --> M{Works on All Platforms?}
    M -->|Issues| N[Fix Platform Issues]
    N --> L
    M -->|Yes| O[Code Example Complete]

    D -.-> D1[checklists/code-testing-checklist.md]
    H -.-> H1[checklists/security-best-practices-checklist.md]
    L -.-> L1[checklists/cross-platform-checklist.md]

    style A fill:#E0E0E0
    style O fill:#90EE90
    style B fill:#FFE4B5
    style D fill:#FFE4B5
    style H fill:#ADD8E6
    style K fill:#ADD8E6
```

**Time Estimate**: 1-3 hours per example | **Agent**: Code Curator

#### Quick Execution Guide

1. **code-curator.md**: `*create-code-example` (runs `tasks/create-code-example.md`) → Use `templates/code-example-tmpl.yaml`
2. Write unit tests and run `*test-all-examples` (runs `tasks/test-code-examples.md`) → Use `checklists/code-testing-checklist.md`
3. Add inline comments and document expected output
4. Run `*security-audit` (runs `tasks/security-audit.md` - Story 7.3) → Use `checklists/security-best-practices-checklist.md`
5. Run `*optimize-code` (runs `tasks/optimize-code.md` - Story 7.6) → Check performance
6. Run `*cross-platform-test` (runs `tasks/cross-platform-test.md` - Story 7.3) → Use `checklists/cross-platform-checklist.md`

---

## Review Workflows

### Technical Review Workflow

Comprehensive technical accuracy, security, and best practices verification.

**Workflow Definition**: `workflows/technical-review-workflow.yaml`
**Agents Used**: `technical-reviewer.md`
**Key Tasks**: `verify-accuracy.md` (Story 7.4), `test-code-examples.md`, `security-audit.md` (Story 7.3), `check-best-practices.md` (Story 7.4)

```mermaid
graph TD
    A[Chapter Draft Complete] --> B[technical-reviewer.md: Read Chapter]
    B --> C[technical-reviewer.md: tasks/verify-accuracy.md]
    C --> D[technical-reviewer.md: tasks/test-code-examples.md]
    D --> E{Code Works?}
    E -->|Issues| F[Document Code Issues]
    E -->|Pass| G[technical-reviewer.md: tasks/security-audit.md]
    G --> H{Security Issues?}
    H -->|Yes| I[Document Security Issues]
    H -->|No| J[technical-reviewer.md: tasks/check-best-practices.md]
    J --> K[technical-reviewer.md: Performance Review]
    K --> L[technical-reviewer.md: Compile Report]
    L --> M{Critical Issues?}
    M -->|Yes| N[NEEDS REVISION]
    M -->|No| O{Major Issues?}
    O -->|Yes| P[APPROVED WITH CHANGES]
    O -->|No| Q[APPROVED]

    F --> L
    I --> L

    C -.-> C1[checklists/technical-accuracy-checklist.md]
    G -.-> G1[checklists/security-best-practices-checklist.md]
    K -.-> K1[checklists/performance-considerations-checklist.md]
    L -.-> L1[templates/technical-review-report-tmpl.yaml]

    style A fill:#FFD700
    style N fill:#FF6B6B
    style P fill:#FFD700
    style Q fill:#90EE90
    style C fill:#ADD8E6
    style G fill:#ADD8E6
```

**Time Estimate**: 3-6 hours per chapter | **Agent**: Technical Reviewer

#### Quick Execution Guide

1. **technical-reviewer.md**: Read chapter completely
2. Run `tasks/verify-accuracy.md` (Story 7.4) → Use `checklists/technical-accuracy-checklist.md` → Verify all explanations
3. Run `tasks/test-code-examples.md` → Test all code in sequence → Document any failing examples
4. Run `tasks/security-audit.md` (Story 7.3) → Use `checklists/security-best-practices-checklist.md` → Identify vulnerabilities
5. Run `tasks/check-best-practices.md` (Story 7.4) → Verify code follows industry standards
6. Performance review → Use `checklists/performance-considerations-checklist.md`
7. Compile review report → Use `templates/technical-review-report-tmpl.yaml` → Output: `reviews/technical-review-chapter-{n}.md`
8. Mark status: NEEDS REVISION (critical issues) | APPROVED WITH CHANGES (major issues) | APPROVED (no major issues)

---

### Incorporate Review Feedback Workflow

Apply technical reviewer feedback systematically.

```mermaid
graph TD
    A[Review Report Received] --> B[tutorial-architect: Read Review Report]
    B --> C[tutorial-architect: Categorize Issues]
    C --> D{Critical Issues?}
    D -->|Yes| E[tutorial-architect: Address Critical First]
    D -->|No| F[tutorial-architect: Address Major Issues]
    E --> G{Code Changes Needed?}
    F --> G
    G -->|Yes| H[code-curator: Update Code Examples]
    H --> I[code-curator: Re-test Code]
    I --> J{Tests Pass?}
    J -->|No| H
    J -->|Yes| K[tutorial-architect: Update Documentation]
    G -->|No| K
    K --> L[tutorial-architect: Address Minor Issues]
    L --> M[tutorial-architect: Verify All Issues Addressed]
    M --> N{All Fixed?}
    N -->|No| O[Complete Remaining]
    O --> M
    N -->|Yes| P[Submit for Re-review]

    style A fill:#FFD700
    style P fill:#90EE90
    style E fill:#FF6B6B
    style F fill:#FFD700
    style K fill:#FFE4B5
```

**Caption**: Feedback incorporation workflow ensures all review issues are systematically addressed and verified.

**Time Estimate**: 2-8 hours depending on issues
**Agents Involved**: Tutorial Architect, Code Curator

---

## Publishing Workflows

### Publishing Decision Tree

Choose the right publishing workflow based on your target publisher.

```mermaid
graph TD
    A[Ready to Publish] --> B{Publisher Type?}
    B -->|PacktPub| C[packtpub-submission-workflow]
    B -->|O'Reilly| D[oreilly-submission-workflow]
    B -->|Manning| E{MEAP or Final?}
    B -->|Self-Publishing| F{Platform?}

    E -->|MEAP| G[manning-meap-workflow]
    E -->|Final| H[manning-submission-workflow]

    F -->|Leanpub| I[self-publishing-workflow: Leanpub]
    F -->|Amazon KDP| J[self-publishing-workflow: KDP]
    F -->|Gumroad| K[self-publishing-workflow: Gumroad]

    C --> L[PacktPub Submission Package]
    D --> M[O'Reilly Submission Package]
    G --> N[Manning MEAP Release]
    H --> O[Manning Final Submission]
    I --> P[Leanpub Manuscript]
    J --> Q[KDP Manuscript]
    K --> R[Gumroad Package]

    style A fill:#FFD700
    style L fill:#90EE90
    style M fill:#90EE90
    style N fill:#90EE90
    style O fill:#90EE90
    style P fill:#90EE90
    style Q fill:#90EE90
    style R fill:#90EE90
```

**Caption**: Publishing decision tree guides you to the correct submission workflow based on your publisher.

---

### PacktPub Submission Workflow

Prepare manuscript for PacktPub submission.

```mermaid
graph TD
    A[Manuscript Complete] --> B[book-publisher: Gather All Chapters]
    B --> C[book-publisher: Format to PacktPub Standards]
    C --> D[book-publisher: Create Front Matter]
    D --> E[book-publisher: Create Back Matter]
    E --> F[api-documenter: Generate Appendices]
    F --> G[book-publisher: Package Code Repository]
    G --> H[screenshot-specialist: Prepare Visual Assets]
    H --> I[book-publisher: Run PacktPub Checklist]
    I --> J{Meets All Requirements?}
    J -->|No| K[Address Missing Items]
    K --> I
    J -->|Yes| L[book-publisher: Create Submission Package]
    L --> M[Ready for PacktPub Submission]

    C -.-> C1[packtpub-format-guidelines]
    I -.-> I1[packtpub-submission-checklist]

    style A fill:#FFD700
    style M fill:#90EE90
    style C fill:#FFE4B5
    style I fill:#F0E68C
```

**Caption**: PacktPub submission workflow formats manuscript to publisher standards and creates complete submission package.

**Time Estimate**: 6-10 hours
**Agents Involved**: Book Publisher, API Documenter, Screenshot Specialist

---

### O'Reilly Submission Workflow

Prepare manuscript for O'Reilly submission.

```mermaid
graph TD
    A[Manuscript Complete] --> B[book-publisher: Convert to AsciiDoc/HTMLBook]
    B --> C[book-publisher: Validate O'Reilly Format]
    C --> D{Format Valid?}
    D -->|Issues| E[Fix Format Issues]
    E --> C
    D -->|Valid| F[book-publisher: Create Atlas Project]
    F --> G[api-documenter: Generate Index]
    G --> H[screenshot-specialist: Prepare Images]
    H --> I[book-publisher: Setup Code Repository]
    I --> J[book-publisher: Run O'Reilly Checklist]
    J --> K{Meets Requirements?}
    K -->|No| L[Address Requirements]
    L --> J
    K -->|Yes| M[Ready for O'Reilly Atlas]

    B -.-> B1[oreilly-htmlbook-spec]
    J -.-> J1[oreilly-format-checklist]

    style A fill:#FFD700
    style M fill:#90EE90
    style B fill:#FFE4B5
    style C fill:#ADD8E6
```

**Caption**: O'Reilly submission workflow converts to HTMLBook format and prepares Atlas-compatible project.

**Time Estimate**: 8-12 hours
**Agents Involved**: Book Publisher, API Documenter, Screenshot Specialist

---

### Manning MEAP Workflow

Prepare chapter for Manning Early Access Program (MEAP).

```mermaid
graph TD
    A[Chapter Complete] --> B[book-publisher: Format to Manning Standards]
    B --> C[book-publisher: Create Chapter Introduction]
    C --> D[book-publisher: Prepare MEAP Metadata]
    D --> E[screenshot-specialist: Optimize Images]
    E --> F[code-curator: Package Chapter Code]
    F --> G[book-publisher: Run MEAP Checklist]
    G --> H{MEAP Ready?}
    H -->|Issues| I[Fix MEAP Issues]
    I --> G
    H -->|Yes| J[book-publisher: Submit to Manning]
    J --> K[MEAP Chapter Released]

    B -.-> B1[manning-format-guidelines]
    G -.-> G1[manning-meap-checklist]

    style A fill:#FFD700
    style K fill:#90EE90
    style B fill:#FFE4B5
    style G fill:#F0E68C
```

**Caption**: Manning MEAP workflow prepares individual chapters for early access release.

**Time Estimate**: 3-5 hours per chapter
**Agents Involved**: Book Publisher, Screenshot Specialist, Code Curator

---

### Self-Publishing Workflow

Prepare manuscript for self-publishing platforms.

```mermaid
graph TD
    A[Manuscript Complete] --> B{Platform?}
    B -->|Leanpub| C[book-publisher: Convert to Leanpub Markdown]
    B -->|Amazon KDP| D[book-publisher: Convert to KDP Format]
    B -->|Gumroad| E[book-publisher: Convert to PDF/ePub]

    C --> F[book-publisher: Setup Leanpub Project]
    D --> G[book-publisher: Create KDP Package]
    E --> H[book-publisher: Create Gumroad Package]

    F --> I[book-publisher: Configure Pricing]
    G --> I
    H --> I

    I --> J[book-publisher: Create Marketing Materials]
    J --> K[screenshot-specialist: Create Cover/Graphics]
    K --> L[book-publisher: Run Self-Publishing Checklist]
    L --> M{Ready to Publish?}
    M -->|No| N[Address Items]
    N --> L
    M -->|Yes| O[Ready for Self-Publishing]

    L -.-> L1[self-publishing-standards-checklist]

    style A fill:#FFD700
    style O fill:#90EE90
    style C fill:#FFE4B5
    style D fill:#FFE4B5
    style E fill:#FFE4B5
```

**Caption**: Self-publishing workflow supports multiple platforms with format conversion and marketing materials.

**Time Estimate**: 8-15 hours
**Agents Involved**: Book Publisher, Screenshot Specialist

---

## Brownfield Workflows

### Book Edition Update Workflow

Systematic approach to 2nd/3rd edition updates.

```mermaid
graph TD
    A[Existing Book] --> B[book-analyst: Analyze Current Edition]
    B --> C[book-analyst: Identify Changes Needed]
    C --> D[book-analyst: Create Revision Plan]
    D --> E{Scope of Changes?}
    E -->|Major| F[Full Restructure Needed]
    E -->|Moderate| G[Chapter Updates]
    E -->|Minor| H[Section Updates]

    F --> I[instructional-designer: Redesign Structure]
    G --> J[Select Chapters to Update]
    H --> K[Select Sections to Update]

    I --> L[Execute Greenfield Workflows]
    J --> L
    K --> L

    L --> M[version-manager: Update Version References]
    M --> N[code-curator: Update All Code Examples]
    N --> O[technical-reviewer: Verify Changes]
    O --> P{Review Passed?}
    P -->|Issues| Q[Address Issues]
    Q --> O
    P -->|Approved| R[technical-editor: Ensure Consistency]
    R --> S[Updated Edition Complete]

    B -.-> B1[book-analysis-report-tmpl]
    D -.-> D1[revision-plan-tmpl]
    O -.-> O1[revision-completeness-checklist]

    style A fill:#FFD700
    style S fill:#90EE90
    style B fill:#FFE4B5
    style N fill:#FFE4B5
    style O fill:#ADD8E6
```

**Caption**: Book edition update workflow analyzes existing content and systematically applies updates for new edition.

**Time Estimate**: 40-120+ hours depending on scope
**Agents Involved**: Book Analyst, Instructional Designer, Code Curator, Version Manager, Technical Reviewer, Technical Editor

---

### Add Chapter to Existing Book Workflow

Add new chapter to already-published book.

```mermaid
graph TD
    A[New Chapter Needed] --> B[book-analyst: Analyze Existing Book]
    B --> C[book-analyst: Determine Chapter Position]
    C --> D[instructional-designer: Design Chapter]
    D --> E[instructional-designer: Validate Prerequisites]
    E --> F{Prerequisites Available?}
    F -->|Missing| G[Update Earlier Chapters]
    F -->|Available| H[Execute Chapter Development]
    G --> H
    H --> I[Chapter Complete]
    I --> J[technical-editor: Update Book Structure]
    J --> K[technical-editor: Update Cross-References]
    K --> L[technical-editor: Update TOC/Index]
    L --> M[book-publisher: Integration Check]
    M --> N{Integrates Smoothly?}
    N -->|Issues| O[Fix Integration Issues]
    O --> M
    N -->|Success| P[New Chapter Integrated]

    B -.-> B1[existing-book-integration-checklist]
    E -.-> E1[prerequisite-clarity-checklist]

    style A fill:#FFD700
    style P fill:#90EE90
    style D fill:#FFE4B5
    style H fill:#FFE4B5
    style J fill:#ADD8E6
```

**Caption**: Add chapter workflow ensures new chapter integrates seamlessly with existing book structure and content.

**Time Estimate**: 20-40 hours
**Agents Involved**: Book Analyst, Instructional Designer, Tutorial Architect, Code Curator, Technical Editor, Book Publisher

---

## Reference Materials

### Agent-Task-Command Mapping

Complete reference showing which agents execute which commands and tasks.

| Agent File | Command | Task File | Purpose |
|-----------|---------|-----------|---------|
| **tutorial-architect.md** | `*create-tutorial` | `tasks/develop-tutorial.md` | Create standalone tutorial |
| | `*outline-chapter` | `tasks/create-chapter-outline.md` | Design chapter structure |
| | `*write-walkthrough` | `tasks/write-walkthrough.md` (Story 7.11) | Create step-by-step guide |
| | `*design-exercises` | `tasks/design-exercises.md` | Create practice problems |
| | `*write-summary` | `tasks/write-summary.md` | Create chapter recap |
| | `*create-doc` | `tasks/create-doc.md` | Universal document creation |
| **code-curator.md** | `*create-code-example` | `tasks/create-code-example.md` | Develop code example |
| | `*test-all-examples` | `tasks/test-code-examples.md` | Test all code |
| | `*security-audit` | `tasks/security-audit.md` (Story 7.3) | Security vulnerability scan |
| | `*cross-platform-test` | `tasks/cross-platform-test.md` (Story 7.3) | Test across platforms |
| | `*version-check` | `tasks/version-check.md` (Story 7.6) | Verify version compatibility |
| | `*optimize-code` | `tasks/optimize-code.md` (Story 7.6) | Improve example efficiency |
| **instructional-designer.md** | `*create-book-outline` | `tasks/design-book-outline.md` | Create book structure |
| | `*create-learning-objectives` | `tasks/create-learning-objectives.md` | Define learning goals |
| | `*design-learning-path` | `tasks/map-prerequisites.md` | Map prerequisite flow |
| | `*analyze-difficulty-curve` | `tasks/analyze-difficulty-curve.md` (Story 7.5) | Check progression |
| **technical-reviewer.md** | `*review-chapter` | `tasks/technical-review-chapter.md` | Full chapter review |
| | _Execute tasks directly_ | `tasks/verify-accuracy.md` (Story 7.4) | Verify technical accuracy |
| | | `tasks/check-best-practices.md` (Story 7.4) | Check code practices |
| | | `tasks/test-code-examples.md` | Test all code |
| | | `tasks/security-audit.md` (Story 7.3) | Security review |
| **technical-editor.md** | `*copy-edit` | `tasks/copy-edit-chapter.md` | Professional editing |
| | `*review-outline` | Editorial review | Outline clarity review |
| **book-publisher.md** | `*create-proposal` | `tasks/create-doc.md` with `book-proposal-tmpl.yaml` | Draft book proposal |
| | _Format tasks_ | `tasks/format-for-packtpub.md` (Story 7.7) | PacktPub formatting |
| | | `tasks/format-for-oreilly.md` (Story 7.7) | O'Reilly formatting |
| | | `tasks/prepare-meap-chapter.md` | Manning MEAP prep |
| **exercise-creator.md** | `*design-exercises` | `tasks/design-exercises.md` | Create practice exercises |
| **book-analyst.md** | `*analyze-book` | `tasks/analyze-existing-book.md` | Analyze existing book |
| | _Plan revision_ | `tasks/plan-book-revision.md` | Create revision plan |
| **version-manager.md** | _Assess impact_ | `tasks/assess-version-impact.md` (Story 7.8) | Evaluate version changes |
| **learning-path-designer.md** | `*validate-flow` | `tasks/validate-learning-flow.md` (Story 7.4) | Validate learning progression |

### File Path Conventions

Standard file paths for manuscript organization.

#### Planning Phase
- **Book Proposal**: `manuscript/planning/book-proposal.md`
- **Book Outline**: `manuscript/planning/book-outline.md`
- **Learning Path Validation**: `manuscript/planning/learning-path-validation.md`
- **Final Outline**: `manuscript/planning/book-outline-final.md`

#### Chapter Development
- **Chapter Outline**: `manuscript/outlines/chapter-{n}-outline.md`
- **Section Analysis**: `section-analysis.md` (working file)
- **Section List**: `manuscript/sections/chapter-{n}-section-list.md`
- **Section Plans**: `section-plans/section-{n}.md` (working files, 5-8 per chapter)

#### Section Development
- **Section Draft**: `manuscript/sections/chapter-{n}/section-{n}-draft.md`
- **Section Final**: `manuscript/sections/chapter-{n}/section-{n}-final.md`
- **Section Review Notes**: `section-{n}-review-notes.md` (working file)

#### Code Examples
- **Code Files**: `code/chapter-{n}/section-{n}/example-{name}.{ext}`
- **Tests**: `code/chapter-{n}/section-{n}/tests/`
- **README**: `code/chapter-{n}/README.md`

#### Chapter Assembly
- **Integrated Chapter**: `manuscript/chapters/chapter-{n}-integrated.md`
- **Learning Flow Validation**: `learning-flow-validation.md` (working file)
- **Technical Review**: `reviews/technical-review-chapter-{n}.md`
- **Edited Chapter**: `edited-chapter.md` (working file)
- **Final Chapter**: `manuscript/chapters/chapter-{n}-final.md`

#### Publication
- **Publisher-Specific Packages**: `publishing/{publisher}/`
- **Submission Packages**: `publishing/{publisher}/submission-package/`
- **Marketing Materials**: `marketing/`
- **Cover Graphics**: `marketing/graphics/`

#### Working Files (Not in Manuscript)
- **Analysis Documents**: Root or `analysis/` directory
- **Review Notes**: Root or `reviews/` directory
- **Validation Reports**: Root or `validation/` directory

### Checklist Reference

Quality gates and their associated checklists.

| Quality Gate | Checklist File | Used By | Execute With |
|-------------|----------------|---------|--------------|
| Section Plan Complete | `section-plan-tmpl.yaml` validates | Tutorial Architect | Template validation |
| Learning Flow Validated | `learning-objectives-checklist.md` | Instructional Designer | `execute-checklist.md` |
| | `prerequisite-clarity-checklist.md` | Instructional Designer | `execute-checklist.md` |
| Code Quality | `code-testing-checklist.md` | Code Curator | `execute-checklist.md` |
| | `code-quality-checklist.md` | Code Curator | `execute-checklist.md` |
| Security Review | `security-best-practices-checklist.md` | Code Curator, Technical Reviewer | `execute-checklist.md` |
| Cross-Platform | `cross-platform-checklist.md` | Code Curator | `execute-checklist.md` |
| Technical Accuracy | `technical-accuracy-checklist.md` | Technical Reviewer | `execute-checklist.md` |
| Best Practices | (checked via `check-best-practices.md` task) | Technical Reviewer | Task execution |
| Performance | `performance-considerations-checklist.md` | Technical Reviewer | `execute-checklist.md` |
| Tutorial Effectiveness | `tutorial-effectiveness-checklist.md` | Code Curator | `execute-checklist.md` |
| Chapter Completeness | `chapter-completeness-checklist.md` | Tutorial Architect | `execute-checklist.md` |
| Accessibility | `accessibility-checklist.md` | Technical Editor | `execute-checklist.md` |
| PacktPub Submission | `packtpub-submission-checklist.md` | Book Publisher | `execute-checklist.md` |
| O'Reilly Format | `oreilly-format-checklist.md` | Book Publisher | `execute-checklist.md` |
| Manning MEAP | `manning-meap-checklist.md` | Book Publisher | `execute-checklist.md` |

---

## Summary

These process flows visualize the complete technical book authoring system:

**High-Level Flows**:

- Book Authoring Lifecycle - Complete journey from concept to published book
- Agent Collaboration Map - How agents work together

**Planning**:

- Book Planning Workflow - Create pedagogically sound outline

**Development**:

- Section-Driven Development - Incremental chapter creation
- Section Development - Core content creation unit
- Chapter Assembly - Merge sections into chapters
- Tutorial Creation - Hands-on learning experiences
- Code Example Workflow - Quality code development

**Review**:

- Technical Review - Comprehensive accuracy validation
- Incorporate Feedback - Systematic issue resolution

**Publishing**:

- Publishing Decision Tree - Choose right workflow
- Publisher-Specific Workflows - PacktPub, O'Reilly, Manning, Self-Publishing

**Brownfield**:

- Edition Updates - Systematic revision process
- Add Chapters - Integrate new content

**Next Steps**:

- **Start writing**: Follow [Getting Started Tutorial](getting-started.md)
- **Deep dive on agents**: Read [Agent Reference](agent-reference.md)
- **Choose workflows**: See [Workflow Guide](workflow-guide.md)
- **See templates**: Explore [Template Gallery](template-gallery.md)

---

_Process Flows - Technical Writing Expansion Pack v1.1.0_
