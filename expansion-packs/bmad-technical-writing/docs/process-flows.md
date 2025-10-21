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

```mermaid
graph TD
    A[Start: Book Concept] --> B[book-publisher: Draft Proposal]
    B --> C[instructional-designer: Design Outline]
    C --> D[instructional-designer: Validate Learning Path]
    D --> E{Prerequisites Flow?}
    E -->|Issues Found| F[instructional-designer: Adjust Outline]
    F --> D
    E -->|Valid| G[technical-editor: Editorial Review]
    G --> H[book-publisher: Publisher Format Check]
    H --> I{Meets Requirements?}
    I -->|Needs Changes| J[Adjust for Publisher]
    J --> G
    I -->|Approved| K[Final Outline Approved]
    K --> L[Ready for Chapter Development]

    B -.-> B1[Optional: Market Research]
    C -.-> C1[Optional: Competitive Analysis]
    D -.-> D1[Optional: Pedagogical Review]

    style L fill:#90EE90
    style B fill:#FFE4B5
    style C fill:#FFE4B5
    style D fill:#ADD8E6
    style G fill:#ADD8E6
    style H fill:#F0E68C
```

**Caption**: Book planning workflow coordinates Book Publisher, Instructional Designer, and Technical Editor to create pedagogically sound, publisher-compliant book outline.

**Time Estimate**: 20-33 hours
**Agents Involved**: Book Publisher, Instructional Designer, Technical Editor

**Key Steps**:
1. **Draft Proposal** - Book Publisher creates comprehensive proposal with market analysis
2. **Design Outline** - Instructional Designer creates detailed chapter structure with learning objectives
3. **Validate Learning Path** - Instructional Designer checks prerequisite flow and difficulty progression
4. **Editorial Review** - Technical Editor ensures clarity and consistency
5. **Publisher Check** - Book Publisher verifies format compliance
6. **Approval** - Final outline approved for development

**Quality Gates**:
- Proposal includes market analysis, target audience, competitive titles
- Outline has clear learning objectives and prerequisites for each chapter
- Learning path validated (no knowledge gaps)
- Editorial review passed (clarity, consistency)
- Publisher requirements met

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

### Section Development Workflow

Complete development of one section (the "story" unit of book writing).

```mermaid
graph TD
    A[Start: Section Plan Ready] --> B[code-curator: Develop Code Examples]
    B --> C[code-curator: Test Code Examples]
    C --> D{All Tests Pass?}
    D -->|No| E[code-curator: Fix Code]
    E --> C
    D -->|Yes| F[tutorial-architect: Write Section]
    F --> G[technical-reviewer: Quick Review]
    G --> H{Critical Issues?}
    H -->|Yes| I[tutorial-architect: Revise Section]
    I --> J[Update Code if Needed?]
    J -->|Yes| K[code-curator: Update Code]
    K --> C
    J -->|No| G
    H -->|No| L[tutorial-architect: Verify Acceptance Criteria]
    L --> M{Criteria Met?}
    M -->|No| N[Address Missing Items]
    N --> L
    M -->|Yes| O[Section DONE]

    B -.-> B1[Use section plan code list]
    F -.-> F1[Reference section-plan objectives]
    G -.-> G1[Use technical-accuracy-checklist]
    L -.-> L1[Check section plan success criteria]

    style O fill:#90EE90
    style B fill:#FFE4B5
    style C fill:#FFE4B5
    style F fill:#FFE4B5
    style G fill:#ADD8E6
    style L fill:#F0E68C
```

**Caption**: Section development workflow coordinates Code Curator and Tutorial Architect to create technically accurate, well-tested section content.

**Time Estimate**: 5.5-10.5 hours per section
**Agents Involved**: Code Curator, Tutorial Architect, Technical Reviewer

**Key Steps**:
1. **Develop Code** - Code Curator creates all code examples from section plan
2. **Test Code** - Code Curator runs tests, verifies output, handles edge cases
3. **Write Section** - Tutorial Architect writes 2-5 page section with code integrated
4. **Quick Review** - Technical Reviewer checks accuracy (focused, not full review)
5. **Revise** - Tutorial Architect incorporates feedback
6. **Verify** - Tutorial Architect confirms all acceptance criteria met
7. **Done** - Section marked complete and ready for chapter assembly

---

### Chapter Assembly Workflow

Merge completed sections into cohesive chapter.

```mermaid
graph TD
    A[All Sections Complete] --> B[technical-editor: Gather Sections]
    B --> C[technical-editor: Review Section Order]
    C --> D{Order Optimal?}
    D -->|Needs Adjustment| E[Reorder Sections]
    E --> C
    D -->|Good| F[technical-editor: Write Chapter Introduction]
    F --> G[technical-editor: Merge Sections]
    G --> H[technical-editor: Add Transitions]
    H --> I[technical-editor: Write Chapter Summary]
    I --> J[technical-editor: Validate Cross-References]
    J --> K{Cross-References Valid?}
    K -->|Issues Found| L[Fix References]
    L --> J
    K -->|Valid| M[technical-editor: Check Style Consistency]
    M --> N[technical-editor: Final Polish]
    N --> O[Chapter Complete]

    F -.-> F1[Use introduction-tmpl]
    I -.-> I1[Recap learning objectives]
    M -.-> M1[chapter-completeness-checklist]

    style A fill:#FFD700
    style O fill:#90EE90
    style G fill:#FFE4B5
    style M fill:#ADD8E6
```

**Caption**: Chapter assembly workflow merges sections with smooth transitions, creating cohesive chapter with introduction and summary.

**Time Estimate**: 4-6 hours
**Agents Involved**: Technical Editor

**Key Activities**:
- Merge all sections in logical order
- Add smooth transitions between sections
- Write compelling chapter introduction
- Create comprehensive chapter summary
- Validate all cross-references
- Ensure consistent style and tone

---

### Tutorial Creation Workflow

Create comprehensive hands-on tutorials.

```mermaid
graph TD
    A[Tutorial Topic Defined] --> B[instructional-designer: Define Learning Objectives]
    B --> C[tutorial-architect: Design Tutorial Structure]
    C --> D[code-curator: Create Tutorial Code Examples]
    D --> E[tutorial-architect: Write Step-by-Step Instructions]
    E --> F[tutorial-architect: Add Expected Outcomes]
    F --> G[tutorial-architect: Write Troubleshooting Section]
    G --> H[code-curator: Test Complete Tutorial]
    H --> I{Tutorial Works End-to-End?}
    I -->|Issues| J[Fix Tutorial Steps]
    J --> H
    I -->|Success| K[exercise-creator: Create Practice Exercises]
    K --> L[Tutorial Complete]

    B -.-> B1[learning-objectives-tmpl]
    C -.-> C1[tutorial-section-tmpl]
    H -.-> H1[tutorial-effectiveness-checklist]

    style A fill:#E0E0E0
    style L fill:#90EE90
    style D fill:#FFE4B5
    style E fill:#FFE4B5
    style H fill:#ADD8E6
```

**Caption**: Tutorial creation workflow builds complete hands-on learning experiences with working code and practice exercises.

**Time Estimate**: 8-12 hours
**Agents Involved**: Instructional Designer, Tutorial Architect, Code Curator, Exercise Creator

---

### Code Example Workflow

Create, test, and document code examples.

```mermaid
graph TD
    A[Code Example Needed] --> B[code-curator: Write Code Example]
    B --> C[code-curator: Write Unit Tests]
    C --> D[code-curator: Run Tests]
    D --> E{Tests Pass?}
    E -->|No| F[Debug and Fix]
    F --> D
    E -->|Yes| G[code-curator: Add Inline Comments]
    G --> H[code-curator: Document Expected Output]
    H --> I[code-curator: Security Check]
    I --> J{Security Issues?}
    J -->|Yes| K[Fix Security Issues]
    K --> I
    J -->|No| L[code-curator: Performance Check]
    L --> M[code-curator: Cross-Platform Test]
    M --> N{Works on All Platforms?}
    N -->|Issues| O[Fix Platform Issues]
    O --> M
    N -->|Yes| P[Code Example Complete]

    C -.-> C1[code-testing-checklist]
    I -.-> I1[security-best-practices-checklist]
    M -.-> M1[cross-platform-checklist]

    style A fill:#E0E0E0
    style P fill:#90EE90
    style B fill:#FFE4B5
    style D fill:#FFE4B5
    style I fill:#ADD8E6
    style L fill:#ADD8E6
```

**Caption**: Code example workflow ensures all code is tested, secure, performant, and cross-platform compatible.

**Time Estimate**: 1-3 hours per example
**Agents Involved**: Code Curator

---

## Review Workflows

### Technical Review Workflow

Comprehensive technical accuracy verification.

```mermaid
graph TD
    A[Chapter Draft Complete] --> B[technical-reviewer: Read Chapter]
    B --> C[technical-reviewer: Verify Technical Accuracy]
    C --> D[technical-reviewer: Test All Code Examples]
    D --> E{Code Works?}
    E -->|Issues| F[Document Code Issues]
    E -->|Pass| G[technical-reviewer: Security Audit]
    G --> H{Security Issues?}
    H -->|Yes| I[Document Security Issues]
    H -->|No| J[technical-reviewer: Check Best Practices]
    J --> K[technical-reviewer: Performance Review]
    K --> L[technical-reviewer: Compile Review Report]
    L --> M{Critical Issues?}
    M -->|Yes| N[Mark as NEEDS REVISION]
    M -->|No| O{Major Issues?}
    O -->|Yes| P[Mark as APPROVED WITH CHANGES]
    O -->|No| Q[Mark as APPROVED]

    F --> L
    I --> L

    C -.-> C1[technical-accuracy-checklist]
    G -.-> G1[security-best-practices-checklist]
    K -.-> K1[performance-considerations-checklist]

    style A fill:#FFD700
    style N fill:#FF6B6B
    style P fill:#FFD700
    style Q fill:#90EE90
    style C fill:#ADD8E6
    style G fill:#ADD8E6
```

**Caption**: Technical review workflow performs comprehensive accuracy, security, and best practices validation.

**Time Estimate**: 3-6 hours per chapter
**Agents Involved**: Technical Reviewer

**Review Criteria**:
- Technical accuracy of all explanations
- Code correctness and testing
- Security vulnerabilities
- Performance considerations
- Best practices compliance
- Cross-platform compatibility

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

*Process Flows - Technical Writing Expansion Pack v1.1.0*
