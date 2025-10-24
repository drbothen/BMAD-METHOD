# BMad Technical Writing Expansion Pack - User Guide

## Table of Contents

- [Introduction](#introduction)
  - [What is the Technical Writing Expansion Pack?](#what-is-the-technical-writing-expansion-pack)
  - [Who is This For?](#who-is-this-for)
  - [What Can You Build With It?](#what-can-you-build-with-it)
  - [How Does It Work With BMad Core?](#how-does-it-work-with-bmad-core)
- [Core Concepts](#core-concepts)
  - [Book Authoring Lifecycle](#book-authoring-lifecycle)
  - [Agent System](#agent-system)
  - [Workflow Orchestration](#workflow-orchestration)
  - [Section-Driven Development](#section-driven-development)
  - [Greenfield vs Brownfield Approaches](#greenfield-vs-brownfield-approaches)
- [Architecture](#architecture)
  - [System Components](#system-components)
  - [Dependencies](#dependencies)
  - [Build System](#build-system)
  - [Web UI vs IDE Usage](#web-ui-vs-ide-usage)
- [Agents](#agents)
- [Workflows](#workflows)
- [Templates](#templates)
- [Tasks](#tasks)
- [Checklists](#checklists)
- [Getting Started](#getting-started)

---

## Introduction

### What is the Technical Writing Expansion Pack?

The Technical Writing Expansion Pack transforms BMad-Method into a complete technical book writing studio. It extends the core BMad framework with specialized agents, workflows, and quality assurance tools specifically designed for technical book authors, technical trainers, and documentation specialists.

Think of it as hiring a complete publishing team:

- **Learning architects** who design effective pedagogical structures
- **Technical writers** who craft clear, engaging tutorials
- **Code experts** who create and maintain working examples
- **Reviewers** who ensure technical accuracy and security
- **Editors** who polish your prose and ensure publisher compliance
- **Publishing specialists** who prepare manuscripts for submission

All working together in an AI-powered framework built entirely in natural language (markdown and YAML).

**Version**: 1.1.0
**Package Name**: `bmad-technical-writing`
**Agents**: 13 (10 required + 3 optional)
**Workflows**: 15
**Templates**: 18
**Tasks**: 33
**Checklists**: 31

### Who is This For?

This expansion pack is designed for:

- **Technical book authors** writing for publishers like PacktPub, O'Reilly, Manning, or Pragmatic Bookshelf
- **Self-published authors** creating technical content for platforms like Leanpub, Amazon KDP, or Gumroad
- **Technical trainers** developing comprehensive course materials with code examples
- **Documentation specialists** creating extensive technical documentation with tutorials
- **Open source maintainers** writing project documentation and getting-started guides
- **Developer advocates** creating technical content and learning resources

You should have:

- Basic understanding of your technical subject matter
- Familiarity with markdown formatting
- Access to an AI chat interface (Gemini, ChatGPT, Claude) or IDE with AI (Cursor, VS Code, Claude Code)
- BMad-Method core installed

### What Can You Build With It?

The Technical Writing Expansion Pack supports:

**Technical Books**:

- Programming language tutorials (Python, JavaScript, Go, Rust, etc.)
- Framework guides (React, Django, Spring Boot, etc.)
- Technology deep-dives (databases, cloud, DevOps, security)
- Best practices and patterns books
- Reference manuals and API documentation

**Book Types**:

- **Greenfield** - New books written from scratch
- **Brownfield** - Second/third editions, version updates, chapter additions

**Publishing Targets**:

- Traditional publishers (PacktPub, O'Reilly, Manning)
- Self-publishing platforms (Leanpub, KDP, Gumroad)
- Open source documentation
- Corporate training materials

**Content Features**:

- Hands-on tutorials with step-by-step instructions
- Working code examples with testing infrastructure
- Practice exercises and solutions
- Technical diagrams and screenshots
- API reference documentation
- Learning objectives and prerequisites
- Glossaries and appendices

### How Does It Work With BMad Core?

The Technical Writing Expansion Pack **extends** BMad-Method core with domain-specific capabilities:

**BMad Core Provides**:

- Agent activation system
- Task execution framework
- Template processing engine
- Dependency resolution
- Build tools and validation
- Configuration management

**Technical Writing Pack Adds**:

- 13 specialized agents for book writing
- 15 book authoring workflows
- 18 publishing templates
- 33 technical writing tasks
- 31 quality assurance checklists
- 6 knowledge bases (publisher guidelines, learning frameworks, etc.)

**Integration Pattern**:

```
BMad Core (Framework) + Technical Writing Pack (Domain Logic) = Complete Book Writing Studio
```

You can also combine this pack with other expansion packs:

- **Creative Writing Pack** - For books with narrative elements or fiction appendices
- **Infrastructure Pack** - For DevOps and cloud infrastructure books

---

## Core Concepts

### Book Authoring Lifecycle

Technical book authoring follows a structured lifecycle with distinct phases:

#### 1. Planning Phase

**Goal**: Design the learning experience and book structure

- Define target audience and prerequisites
- Create learning objectives aligned with outcomes
- Design book outline with chapter progression
- Map prerequisite dependencies between chapters
- Validate pedagogical structure

**Key Deliverables**: Book proposal, book outline, learning objectives

**Agents Involved**: Instructional Designer, Tutorial Architect, Book Publisher

#### 2. Drafting Phase

**Goal**: Create chapter content with code examples and tutorials

- Design chapter outline with section breakdown
- Write section content (2-5 pages per section)
- Create working code examples
- Develop practice exercises
- Document expected outcomes and troubleshooting

**Key Deliverables**: Chapter drafts, code examples, exercise sets

**Agents Involved**: Tutorial Architect, Code Curator, Exercise Creator

#### 3. Review Phase

**Goal**: Ensure technical accuracy, security, and quality

- Verify technical correctness of all content
- Audit code examples for security vulnerabilities
- Validate best practices and patterns
- Check performance considerations
- Test cross-platform compatibility

**Key Deliverables**: Technical review report, revision notes

**Agents Involved**: Technical Reviewer, Code Curator

#### 4. Editing Phase

**Goal**: Polish writing and ensure publisher compliance

- Improve clarity and readability
- Ensure consistent style and tone
- Verify publisher formatting requirements
- Check accessibility standards
- Validate cross-references and citations

**Key Deliverables**: Polished manuscript, style corrections

**Agents Involved**: Technical Editor

#### 5. Publishing Phase

**Goal**: Prepare and submit manuscript to publisher

- Package manuscript per publisher specifications
- Create supplementary materials (preface, appendix, index, glossary)
- Prepare code repositories
- Generate submission materials
- Handle MEAP/beta releases (Manning/Leanpub)

**Key Deliverables**: Submission package, code repository, supplementary materials

**Agents Involved**: Book Publisher, API Documenter, Screenshot Specialist

### Agent System

Agents are specialized AI personas that handle specific aspects of book authoring. Each agent has:

- **Defined role and expertise** - Clear responsibilities and domain knowledge
- **Commands** - Specific actions the agent can perform
- **Dependencies** - Templates, tasks, and checklists the agent uses
- **Activation instructions** - How the agent initializes and operates

**Agent Categories**:

1. **Core Agents (10)** - Required for basic book authoring
   - Instructional Designer, Tutorial Architect, Code Curator
   - Technical Reviewer, Technical Editor, Book Publisher
   - API Documenter, Screenshot Specialist, Exercise Creator
   - Book Analyst (brownfield)

2. **Optional Agents (3)** - For advanced scenarios
   - Learning Path Designer (complex prerequisite mapping)
   - Sample Code Maintainer (extensive code repository management)
   - Version Manager (multi-version compatibility matrices)

**How Agents Work**:

- Agents are activated using slash commands (e.g., `/bmad-tw:instructional-designer`)
- Once activated, an agent loads its persona and presents available commands
- Users select commands to execute specific tasks
- Agents can call other agents via workflow orchestration
- Agents stay in character until explicitly told to exit

**Agent Collaboration**:
Agents collaborate through workflows. For example, in section-development-workflow:

1. Tutorial Architect outlines the section
2. Code Curator creates code examples
3. Tutorial Architect writes tutorial content using the code
4. Technical Reviewer verifies accuracy
5. Tutorial Architect incorporates feedback

### Workflow Orchestration

Workflows are structured sequences that coordinate multiple agents to accomplish complex book authoring tasks.

**Workflow Structure** (YAML):

```yaml
workflow:
  name: section-development-workflow
  agents:
    primary: tutorial-architect
    supporting: [code-curator, technical-reviewer]
  steps:
    - agent: tutorial-architect
      task: outline-section
    - agent: code-curator
      task: create-code-examples
    - agent: tutorial-architect
      task: write-tutorial-content
    - agent: technical-reviewer
      task: review-section
```

**Workflow Types**:

1. **Planning Workflows** - Structure and design
   - `book-planning-workflow` - Complete book planning from concept to outline

2. **Development Workflows** - Content creation
   - `section-planning-workflow` - Break chapter into sections
   - `section-development-workflow` - Write individual sections
   - `chapter-assembly-workflow` - Merge sections into complete chapter
   - `chapter-development-workflow` - Complete chapter creation
   - `tutorial-creation-workflow` - Hands-on tutorial development
   - `code-example-workflow` - Code example creation and testing

3. **Review Workflows** - Quality assurance
   - `technical-review-workflow` - Technical accuracy verification
   - `incorporate-review-feedback-workflow` - Apply reviewer feedback

4. **Publishing Workflows** - Submission preparation
   - `packtpub-submission-workflow` - PacktPub formatting and submission
   - `oreilly-submission-workflow` - O'Reilly standards compliance
   - `manning-meap-workflow` - Manning MEAP release preparation
   - `self-publishing-workflow` - Leanpub/KDP/Gumroad preparation

5. **Brownfield Workflows** - Existing book updates
   - `book-edition-update-workflow` - 2nd/3rd edition revisions
   - `add-chapter-to-existing-book-workflow` - Add chapters to existing books

**How Workflows Execute**:

1. User activates primary agent
2. User triggers workflow command
3. Agent executes workflow steps sequentially
4. Each step may involve tasks, templates, and checklists
5. Agent may call supporting agents for specific steps
6. Workflow completes with deliverable output

### Section-Driven Development

Section-driven development is the recommended approach for writing technical book chapters. It breaks chapters into small, manageable sections (2-5 pages each) that can be developed independently.

**Why Section-Driven?**

- **Manageable scope** - Small sections are easier to write and review
- **Parallel development** - Multiple sections can be developed simultaneously
- **Incremental progress** - Each section completion is a milestone
- **Quality focus** - Easier to maintain quality in small chunks
- **Flexibility** - Sections can be reordered or replaced without major rewrites

**Section-Driven Workflow**:

1. **Plan**: Instructional Designer creates chapter outline, breaks into 6-8 sections
2. **Develop**: Tutorial Architect writes each section individually
3. **Review**: Technical Reviewer validates each section
4. **Assemble**: Technical Editor merges sections into cohesive chapter
5. **Publish**: Book Publisher prepares final chapter for submission

**Section Structure**:

- **Introduction** (0.5-1 page) - What you'll learn, prerequisites
- **Concept Explanation** (1-2 pages) - Theory and context
- **Hands-On Tutorial** (1-2 pages) - Step-by-step implementation
- **Troubleshooting** (0.5-1 page) - Common issues and solutions
- **Summary** (0.5 page) - Key takeaways, next steps

**Example Section Breakdown** (Chapter 3: Lists and Tuples):

- Section 3.1: Introduction to Lists (3 pages)
- Section 3.2: List Operations and Methods (4 pages)
- Section 3.3: List Comprehensions (3 pages)
- Section 3.4: Introduction to Tuples (3 pages)
- Section 3.5: When to Use Lists vs Tuples (2 pages)
- Section 3.6: Advanced List Techniques (4 pages)

### Greenfield vs Brownfield Approaches

**Greenfield** = New book written from scratch

**Use When**:

- Starting a completely new book project
- No existing content to work with
- Clean slate for structure and design

**Agents Used**:

- Instructional Designer (book planning)
- Tutorial Architect (content creation)
- Code Curator (code examples)
- Technical Reviewer (accuracy)
- Technical Editor (polish)
- Book Publisher (submission)
- Plus specialists (API Documenter, Screenshot Specialist, Exercise Creator)

**Workflows**:

- book-planning-workflow
- chapter-development-workflow
- section-development-workflow
- Publisher-specific submission workflows

---

**Brownfield** = Existing book updates, revisions, additions

**Use When**:

- Writing 2nd or 3rd edition
- Updating for new technology version (Python 3.10 → 3.12)
- Adding chapters to existing book
- Incorporating reviewer feedback
- Migrating to new publisher

**Agents Used**:

- Book Analyst (analyze existing content, plan revisions)
- Plus all greenfield agents for new/updated content

**Workflows**:

- book-edition-update-workflow
- add-chapter-to-existing-book-workflow
- incorporate-review-feedback-workflow

**Brownfield Process**:

1. Book Analyst analyzes existing book structure and content
2. Book Analyst creates revision plan (what needs updating/adding/removing)
3. Greenfield agents execute revision plan for updated content
4. Technical Editor ensures consistency between old and new content
5. Book Publisher prepares updated manuscript

---

## Architecture

### System Components

The Technical Writing Expansion Pack consists of five main component types:

#### 1. Agents (`agents/*.md`)

Markdown files with embedded YAML configuration defining AI personas.

**Structure**:

````markdown
# agent-name

ACTIVATION-NOTICE: ...

```yaml
agent:
  name: Agent Name
  id: agent-id
  title: Agent Title
  icon: 🎓
  whenToUse: Description
persona:
  role: Role description
  style: Communication style
  identity: Expertise areas
  focus: Primary focus
commands:
  - command-name: description
dependencies:
  tasks: [...]
  templates: [...]
  checklists: [...]
  data: [...]
```
````

## Startup Context

Detailed persona instructions...

````

#### 2. Workflows (`workflows/*.yaml`)
YAML files defining multi-agent orchestration sequences.

**Structure**:
```yaml
workflow:
  name: workflow-name
  description: Workflow description
  agents:
    primary: agent-id
    supporting: [agent-id, ...]
  steps:
    - step: 1
      agent: agent-id
      task: task-name
      template: template-name
      checklist: checklist-name
    - step: 2
      ...
  outputs:
    - output-name
````

#### 3. Templates (`templates/*.yaml`)

YAML files defining document structures with sections and LLM instructions.

**Structure**:

```yaml
template:
  name: template-name
  description: Template description
  elicit: true/false
elicitation:
  prompts:
    - prompt: Question to ask user
      id: variable-name
output:
  sections:
    - section: Section Name
      instructions: LLM instructions for section
      content: Template content with {{variables}}
```

#### 4. Tasks (`tasks/*.md`)

Markdown files with step-by-step executable instructions.

**Structure**:

```markdown
# task-name

## Purpose

What this task accomplishes

## Inputs

What's needed to start

## Steps

1. Step one
2. Step two
   ...

## Outputs

What this task produces

## Success Criteria

How to know task is complete
```

#### 5. Checklists (`checklists/*.md`)

Markdown files with quality assurance criteria.

**Structure**:

```markdown
# checklist-name

## Purpose

What this checklist validates

## Checklist

- [ ] Criterion 1
- [ ] Criterion 2
      ...

## Pass Criteria

All items must be checked
```

### Dependencies

Agents declare dependencies on templates, tasks, checklists, and data:

```yaml
dependencies:
  tasks:
    - create-doc.md
    - design-book-outline.md
  templates:
    - book-outline-tmpl.yaml
  checklists:
    - learning-objectives-checklist.md
  data:
    - bmad-kb.md
    - learning-frameworks.md
```

**Dependency Resolution**:

- Dependencies are loaded on-demand when agent executes command
- Recursive resolution (templates can reference tasks, etc.)
- Path mapping: `{root}/{type}/{name}` (e.g., `{root}/tasks/create-doc.md`)

### Build System

The Technical Writing Pack integrates with BMad's build system:

**Build Process**:

1. Reads agent/workflow/template definitions
2. Resolves dependencies recursively
3. Bundles content into `.txt` files for web UI
4. Outputs to `dist/` directory

**Build Commands**:

```bash
npm run build                    # Build everything
npm run build:agents            # Only agent bundles
npm run build:teams             # Only team bundles
npm run validate                # Validate all configs
```

### Web UI vs IDE Usage

The Technical Writing Pack works in two environments:

#### Web UI (Gemini, ChatGPT, Claude)

**Use For**: Planning phase (book outline, learning objectives, chapter structure)

**How It Works**:

1. Build system creates bundled `.txt` files with all dependencies
2. User uploads bundle to chat interface
3. Agent activates with full context
4. User executes planning workflows
5. Downloads deliverables (book outline, chapter plans)

**Advantages**:

- Rich context (entire knowledge base available)
- No token limits during planning
- Easy to share and collaborate

**Files**:

- `dist/agents/instructional-designer.txt` (bundled agent)
- `dist/teams/planning-team.txt` (multi-agent bundle)

#### IDE (Cursor, VS Code, Claude Code)

**Use For**: Development phase (writing content, creating code, reviewing)

**How It Works**:

1. Agents load individual `.md` files from expansion pack
2. Dependencies resolved on-demand from project structure
3. Agent works directly with project files
4. Changes committed to version control

**Advantages**:

- Direct file editing
- Code creation and testing
- Git integration
- Efficient for development

**Activation**:

```
/bmad-tw:tutorial-architect
/bmad-tw:code-curator
```

---

## Agents

The Technical Writing Pack provides 13 specialized agents organized in categories:

### Core Planning Agents

- **Instructional Designer** 🎓 - Learning architecture, pedagogical structure, Bloom's taxonomy
- **Tutorial Architect** 📝 - Hands-on tutorials, step-by-step guides, exercises
- **Code Curator** 💻 - Code examples, testing, version management

### Core Review Agents

- **Technical Reviewer** 🔍 - Technical accuracy, security, best practices
- **Technical Editor** ✍️ - Clarity, style, publisher compliance, accessibility

### Core Publishing Agent

- **Book Publisher** 📦 - Publication preparation, manuscript packaging, submissions

### Specialist Agents

- **API Documenter** 📚 - API references, technical specs, glossaries
- **Screenshot Specialist** 📸 - Diagrams, screenshots, visual documentation
- **Exercise Creator** 🏋️ - Practice problems, assessments, solutions

### Brownfield Agent

- **Book Analyst** 📖 - Existing book analysis, revision planning, edition updates

### Optional Agents (Advanced)

- **Learning Path Designer** 🗺️ - Complex prerequisite mapping, skill progression
- **Sample Code Maintainer** 🔧 - Repository management, CI/CD, dependency updates
- **Version Manager** 🔢 - Multi-version compatibility, platform-specific code

**→ See [Agent Reference Guide](agent-reference.md) for complete documentation**

---

## Workflows

The pack provides 15 workflows organized by phase:

### Planning (1)

- `book-planning-workflow` - Complete book planning from concept to approved outline

### Development (6)

- `chapter-development-workflow` - Complete chapter creation
- `section-planning-workflow` - Break chapter into sections
- `section-development-workflow` - Write individual sections
- `chapter-assembly-workflow` - Merge sections into chapter
- `tutorial-creation-workflow` - Hands-on tutorial development
- `code-example-workflow` - Code example creation and testing

### Review (2)

- `technical-review-workflow` - Technical accuracy verification
- `incorporate-review-feedback-workflow` - Apply reviewer feedback

### Publishing (4)

- `packtpub-submission-workflow` - PacktPub submission preparation
- `oreilly-submission-workflow` - O'Reilly standards compliance
- `manning-meap-workflow` - Manning MEAP release
- `self-publishing-workflow` - Leanpub/KDP/Gumroad preparation

### Brownfield (2)

- `book-edition-update-workflow` - 2nd/3rd edition revisions
- `add-chapter-to-existing-book-workflow` - Add chapters to existing books

**→ See [Workflow Guide](workflow-guide.md) for complete documentation and decision tree**

---

## Templates

18 professional templates organized by category:

### Planning (3)

- `book-outline-tmpl` - Complete book structure
- `book-proposal-tmpl` - Publisher proposal
- `chapter-outline-tmpl` - Chapter structure with sections

### Chapter Content (5)

- `section-plan-tmpl` - Individual section plan
- `chapter-draft-tmpl` - Chapter content
- `introduction-tmpl` - Chapter introduction
- `preface-tmpl` - Book preface
- `appendix-tmpl` - Technical appendix

### Code (2)

- `code-example-tmpl` - Code examples with tests
- `api-reference-tmpl` - API documentation

### Learning (2)

- `learning-objectives-tmpl` - Learning outcomes
- `exercise-set-tmpl` - Practice exercises

### Tutorial (1)

- `tutorial-section-tmpl` - Hands-on tutorial

### Review (2)

- `technical-review-report-tmpl` - Review findings
- `revision-plan-tmpl` - Edition update plan

### Visual (1)

- `diagram-spec-tmpl` - Diagram specifications

### Documentation (2)

- `glossary-entry-tmpl` - Glossary terms
- `book-analysis-report-tmpl` - Existing book analysis

**→ See [Template Gallery](template-gallery.md) for examples and usage**

---

## Tasks

33 tasks organized by phase:

### Planning (6)

- `design-book-outline` - Create book structure
- `create-learning-objectives` - Define learning outcomes
- `create-chapter-outline` - Plan chapter structure
- `design-learning-path` - Map skill progression
- `create-preface` - Write book introduction
- `build-glossary` - Create terminology reference

### Chapter Development (8)

- `write-chapter-draft` - Write chapter content
- `write-introduction` - Create chapter intro
- `write-summary` - Write chapter summary
- `develop-tutorial` - Create hands-on tutorial
- `design-exercises` - Create practice problems
- `create-solutions` - Write exercise solutions
- `design-diagram-set` - Plan visual documentation
- `validate-cross-references` - Check internal links

### Code Management (5)

- `create-code-example` - Write code samples
- `test-code-examples` - Verify code works
- `setup-code-repository` - Initialize Git repo
- `version-matrix-check` - Test multi-version compatibility
- `generate-api-docs` - Create API reference

### Review & Editing (4)

- `technical-review-chapter` - Verify accuracy
- `copy-edit-chapter` - Polish writing
- `create-diagram-spec` - Design diagrams
- `take-screenshots` - Capture visuals

### Publishing (7)

- `package-for-publisher` - Prepare submission
- `prepare-meap-chapter` - Manning beta release
- `self-publish-prep` - Self-publishing preparation
- `create-appendix` - Write appendix
- `create-index-entries` - Generate index
- `incorporate-reviewer-feedback` - Apply feedback
- `plan-book-revision` - Plan edition update

### Documentation (3)

- `build-glossary` - Create glossary
- `create-index-entries` - Build index
- `validate-cross-references` - Verify links

**→ See [Task Reference](task-reference.md) for complete documentation**

---

## Checklists

31 checklists organized by phase:

### Planning (2)

- `learning-objectives-checklist` - Validate learning outcomes
- `prerequisite-clarity-checklist` - Verify prerequisites

### Drafting (5)

- `chapter-completeness-checklist` - Ensure chapter complete
- `tutorial-effectiveness-checklist` - Validate tutorials
- `exercise-difficulty-checklist` - Verify exercise quality
- `readability-checklist` - Check clarity
- `inclusive-language-checklist` - Ensure inclusivity

### Code Quality (5)

- `code-quality-checklist` - Verify code standards
- `code-testing-checklist` - Ensure tests pass
- `version-compatibility-checklist` - Check versions
- `cross-platform-checklist` - Test platforms
- `repository-quality-checklist` - Validate repo

### Review (4)

- `technical-accuracy-checklist` - Verify correctness
- `security-best-practices-checklist` - Check security
- `performance-considerations-checklist` - Review performance
- `citation-accuracy-checklist` - Validate citations

### Publishing (7)

- `packtpub-submission-checklist` - PacktPub requirements
- `oreilly-format-checklist` - O'Reilly standards
- `manning-meap-checklist` - Manning MEAP requirements
- `meap-readiness-checklist` - Beta release readiness
- `self-publishing-standards-checklist` - Self-pub standards
- `accessibility-checklist` - WCAG compliance
- `book-proposal-checklist` - Proposal completeness

### Final QA (8)

- `final-manuscript-checklist` - Complete manuscript review
- `index-completeness-checklist` - Verify index
- `diagram-clarity-checklist` - Check diagrams
- `screenshot-quality-checklist` - Verify screenshots
- `glossary-accuracy-checklist` - Check glossary
- Plus 3 more for brownfield scenarios

**→ See [Checklist Reference](checklist-reference.md) for complete documentation**

---

## Getting Started

Ready to write your technical book? Here's what to do next:

### 1. Quick Start (5 Minutes)

Read the [Quick Reference Card](quick-reference.md) for a one-page overview of most common workflows, agents, and commands.

### 2. Hands-On Tutorial (1-2 Hours)

Follow the [Getting Started Tutorial](getting-started.md) to write your first chapter using the "Python Data Structures Handbook" example. You'll learn:

- How to plan a book
- How to outline a chapter
- How to write a section
- How to review and polish content
- How to prepare for publishing

### 3. Deep Dive (Optional)

Explore detailed reference documentation:

- [Process Flows](process-flows.md) - Visual diagrams of all workflows
- [Agent Reference](agent-reference.md) - Complete agent documentation
- [Workflow Guide](workflow-guide.md) - All workflows with decision tree
- [Template Gallery](template-gallery.md) - All templates with examples

### 4. Get Support

- [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions
- [FAQ](faq.md) - Frequently asked questions
- [Discord Community](https://discord.gg/gk8jAdXWmj) - Ask questions and share
- [GitHub Issues](https://github.com/bmadcode/bmad-method/issues) - Report bugs

### Recommended Learning Path

**Beginners**:

1. Quick Reference (5 min)
2. Getting Started Tutorial (1-2 hours)
3. Start writing your first chapter!

**Intermediate Users**:

1. Process Flows (understand orchestration)
2. Agent Reference (know all agent capabilities)
3. Workflow Guide (choose right workflows)

**Advanced Users**:

1. Integration Guide (multi-expansion usage)
2. Task Reference (customize workflows)
3. Template Gallery (create custom templates)

---

## Questions?

- 📖 **Complete tutorial**: [Getting Started Guide](getting-started.md)
- 📋 **Quick reference**: [Quick Reference Card](quick-reference.md)
- ❓ **Common issues**: [Troubleshooting Guide](troubleshooting.md)
- 💬 **Ask community**: [Discord](https://discord.gg/gk8jAdXWmj)
- 🐛 **Report bugs**: [GitHub Issues](https://github.com/bmadcode/bmad-method/issues)

**Ready to write your book? → [Start Tutorial](getting-started.md)**

---

_Technical Writing Expansion Pack v1.1.0_
_Part of BMad-Method™ - The Universal AI Agent Framework_
