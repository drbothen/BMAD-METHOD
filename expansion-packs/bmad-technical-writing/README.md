# BMad Technical Writing Expansion Pack

Transform your AI into a complete technical book writing studio with specialized agents for technical authors, trainers, and documentation specialists.

## 📚 Overview

The Technical Writing Expansion Pack extends BMad-Method with a comprehensive suite of tools for creating high-quality technical books, tutorials, and instructional content. Whether you're writing for PacktPub, O'Reilly, Manning, or self-publishing, this pack provides structured AI assistance throughout your technical writing process.

### Key Features

- 🤖 **13 Specialized Agents** - Complete writing team with 10 required agents (greenfield planning/writing/review + brownfield book analysis) + 3 optional agents (Learning Path Designer, Sample Code Maintainer, Version Manager) for advanced scenarios
- 📝 **33 Core Tasks** - Full chapter development, API documentation, diagram design, publishing workflows, PLUS learning path design, code repository setup, version matrix testing, solutions creation, index generation, screenshot management, publisher packaging, MEAP preparation, self-publishing prep, preface/appendix creation, diagram set design, cross-reference validation, and brownfield tasks
- 📋 **31 Quality Checklists** - Technical accuracy, security, performance, publisher compliance, accessibility, visual quality, PLUS cross-platform compatibility, inclusive language, readability, index completeness, citation accuracy, final manuscript review, book proposals, self-publishing standards, repository quality, MEAP readiness, and brownfield checklists
- 🎯 **18 Professional Templates** - Book planning, chapter development, API reference, diagrams, preface, appendix, publishing, brownfield templates, PLUS glossary entry template
- 📚 **6 Knowledge Bases** - Comprehensive publisher guidelines and technical writing standards
- 🔄 **15 Workflows** - Section-driven development, publisher-specific submission workflows (PacktPub, O'Reilly, Manning, Self-Publishing), brownfield workflows for edition updates, and complete book lifecycle management

## 📖 Documentation

**New to Technical Writing Pack? Start here!**

### 🚀 Quick Start
- **[Quick Reference Card](docs/quick-reference.md)** - One-page cheat sheet (5 min read)
- **[Getting Started Tutorial](docs/getting-started.md)** - Write your first chapter hands-on (1-2 hours)
- **[User Guide](docs/user-guide.md)** - Complete system overview (60-90 min read)

### 📚 Complete Documentation
- **[Documentation Index](docs/README.md)** - Navigation hub for all documentation
- **[Process Flows](docs/process-flows.md)** - Visual workflow diagrams
- **[Agent Reference Guide](docs/agent-reference.md)** - All 13 agents in detail
- **[Workflow Guide](docs/workflow-guide.md)** - All 15 workflows explained
- **[Template Gallery](docs/template-gallery.md)** - All 18 templates with examples
- **[Task Reference](docs/task-reference.md)** - All 33 tasks organized by phase
- **[Checklist Reference](docs/checklist-reference.md)** - All 31 checklists with quality gates
- **[FAQ](docs/faq.md)** - Frequently asked questions
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

**See [docs/README.md](docs/README.md) for complete documentation map with 13 guides + 4 examples (~35,000 words).**

## ✍️ Included Agents

### Planning & Design Team (Sprint 1)

1. **Instructional Designer** 🎓 - Learning objectives, pedagogical structure, and instructional scaffolding
2. **Tutorial Architect** 🏗️ - Hands-on tutorial design, exercise creation, and progressive learning paths
3. **Code Curator** 🔧 - Code example development, testing, version management, and quality assurance

### Review & Publishing Team (Sprint 2)

4. **Technical Reviewer** 🔍 - Technical accuracy verification, security audits, best practices validation
5. **Technical Editor** ✍️ - Clarity improvement, style consistency, publisher formatting, accessibility
6. **Book Publisher** 📦 - Publication preparation, manuscript packaging, publisher-specific formatting

### Specialist Team (Sprint 3)

7. **API Documenter** 📚 - API reference documentation, technical specifications, glossaries, and appendices
8. **Screenshot Specialist** 📸 - Visual documentation, technical diagrams, screenshot planning, and annotations
9. **Exercise Creator** 🏋️ - Practice problems, assessments, exercises aligned with learning objectives

### Brownfield Team (Sprint 4)

10. **Book Analyst** 📖 - Existing book analysis, revision planning, 2nd/3rd edition updates, version migrations, pattern extraction, and reviewer feedback incorporation

### Optional Specialist Team (Sprint 5)

11. **Learning Path Designer** 🗺️ - Prerequisite mapping, skill progression design, knowledge scaffolding, learning flow validation (can merge with Instructional Designer for simpler deployments)
12. **Sample Code Maintainer** 🔧 - Code repository management, CI/CD pipelines, dependency management, automated testing (can merge with Code Curator for simpler deployments)
13. **Version Manager** 🔢 - Multi-version compatibility testing, platform-specific code handling, version matrix management (can merge with Code Curator for simpler deployments)

## 🚀 Installation

### Via BMad Installer

```bash
npx bmad-method install
# Select "Technical Book Writing Studio" from the expansion packs list
```

### Manual Installation

1. Clone or download this expansion pack
2. Copy to your BMad Method installation:
   ```bash
   cp -r bmad-technical-writing/* ~/bmad-method/expansion-packs/bmad-technical-writing/
   ```
3. Run the BMad installer to register the pack

## 📁 Project Structure

The Technical Writing Expansion Pack uses `manuscript/` as the primary directory for your book content, aligning with publishing industry terminology and avoiding semantic confusion.

### Directory Structure

```
your-book-project/
├── manuscript/              # ← Your book content (the manuscript)
│   ├── planning/
│   │   ├── book-proposal.md
│   │   ├── book-outline.md
│   │   └── learning-path-validation.md
│   ├── outlines/
│   │   └── chapter-01-outline.md
│   ├── sections/
│   │   └── chapter-01/
│   │       ├── section-1.1-draft.md
│   │       └── section-1.1-final.md
│   ├── chapters/
│   │   ├── chapter-01-integrated.md
│   │   └── chapter-01-final.md
│   └── reviews/
│       └── chapter-01-review.md
├── code-examples/           # Supporting code and tests
│   └── chapter-01/
├── images/                  # Diagrams, screenshots, figures
├── submission/              # Publisher-ready packages
│   ├── packtpub/
│   └── oreilly/
├── docs/                    # Optional: PROJECT documentation
│   ├── README.md
│   └── publisher-notes.md
└── README.md
```

### Why `manuscript/` instead of `docs/`?

**Semantic Clarity**: In software projects, `docs/` typically means "technical documentation about the codebase" (API docs, setup guides). For book authoring, `manuscript/` clearly indicates "the book you're writing" using standard publishing industry terminology.

**Benefits**:
- ✅ **Industry standard**: Publishers use "manuscript submission" terminology
- ✅ **Clear separation**: Book content (`manuscript/`) vs project docs (`docs/`)
- ✅ **Professional**: Authors think in terms of "working on my manuscript"
- ✅ **GitHub clarity**: Contributors immediately understand what `manuscript/` contains

**Note**: The optional `docs/` directory can still be used for meta-documentation about the book project itself (e.g., publisher correspondence, project notes), maintaining clear separation from your manuscript content.

## 💡 Usage

### Quick Start

```bash
# Activate individual agents in your IDE

# Greenfield agents (new book writing)
/bmad-tw:instructional-designer
/bmad-tw:tutorial-architect
/bmad-tw:code-curator
/bmad-tw:technical-reviewer
/bmad-tw:technical-editor
/bmad-tw:book-publisher
/bmad-tw:api-documenter
/bmad-tw:screenshot-specialist
/bmad-tw:exercise-creator

# Brownfield agent (existing book updates)
/bmad-tw:book-analyst
```

### Core Workflows (Sprint 2, 2.5, 2.6)

**Book Planning Workflow** _(Sprint 2.5)_ - Complete book planning from concept to approved outline:

1. Book Publisher drafts comprehensive book proposal
2. Instructional Designer creates detailed book outline
3. Instructional Designer validates learning progression
4. Technical Editor reviews outline for clarity
5. Book Publisher verifies publisher requirements

**Chapter Development Workflow v2.0** _(Sprint 2, refactored Sprint 2.6)_ - Complete chapter creation from outline to publisher-ready:

_Section-Driven Approach (NEW in v2.0):_

1. Tutorial Architect creates chapter outline
2. Tutorial Architect + Instructional Designer plan sections (section-planning-workflow)
3. For each section: Code Curator + Tutorial Architect + Technical Reviewer develop section (section-development-workflow)
4. Tutorial Architect + Technical Editor + Technical Reviewer assemble chapter (chapter-assembly-workflow)
5. Final validation and publication readiness

_Traditional Approach (Original, still supported):_

1. Tutorial Architect creates chapter outline
2. Code Curator develops and tests all code examples
3. Tutorial Architect writes complete chapter draft
4. Technical Reviewer performs comprehensive technical review
5. Tutorial Architect revises based on review feedback
6. Technical Editor performs professional copy editing
7. Tutorial Architect finalizes chapter for publication

**Section Planning Workflow** _(Sprint 2.6)_ - Break chapter into deliverable sections (BMad story analog):

1. Tutorial Architect analyzes chapter outline
2. Tutorial Architect identifies section boundaries (5-8 sections)
3. Tutorial Architect creates section plans with acceptance criteria
4. Instructional Designer validates learning flow
5. Tutorial Architect finalizes section list

**Section Development Workflow** _(Sprint 2.6)_ - Write one section (2-5 pages):

1. Code Curator develops section code examples
2. Code Curator tests all code
3. Tutorial Architect writes section content
4. Technical Reviewer performs focused section review
5. Tutorial Architect revises section
6. Tutorial Architect finalizes section (DONE)

**Chapter Assembly Workflow** _(Sprint 2.6)_ - Integrate completed sections (BMad Sprint Review analog):

1. Tutorial Architect merges all completed sections
2. Tutorial Architect improves transitions
3. Instructional Designer validates learning flow
4. Technical Reviewer performs full chapter review
5. Tutorial Architect revises based on feedback
6. Technical Editor performs copy editing
7. Tutorial Architect finalizes chapter for publication

**Tutorial Creation Workflow** _(Sprint 2)_ - Build effective hands-on tutorials:

1. Instructional Designer designs learning path
2. Tutorial Architect creates step-by-step structure
3. Code Curator develops and tests tutorial code
4. Tutorial Architect writes complete tutorial
5. Code Curator tests end-to-end
6. Tutorial Architect revises based on testing
7. Instructional Designer validates learning effectiveness

**Code Example Workflow** _(Sprint 2.5)_ - Develop, test, and document code examples:

1. Code Curator develops code example
2. Code Curator tests on all target platforms
3. Code Curator verifies code quality
4. Code Curator performs security review
5. Code Curator adds comprehensive documentation

**Technical Review Workflow** _(Sprint 2.5)_ - Comprehensive expert review of chapter:

1. Technical Reviewer verifies technical accuracy
2. Code Curator reviews all code examples
3. Technical Reviewer validates best practices
4. Technical Reviewer compiles comprehensive report

### Common Use Cases

- **Book Planning** - Create comprehensive book outlines with learning objectives
- **Chapter Development** - Full workflow from outline to publication-ready manuscript
- **Code Example Creation** - Develop, test, and document working code examples
- **Technical Review** - Verify accuracy, security, and best practices
- **Editorial Polish** - Ensure clarity, consistency, and publisher compliance
- **Quality Assurance** - 15 checklists covering all aspects of technical writing quality

## 📋 Key Components

### Templates (15 Total)

**Sprint 1 (Planning):**

- `book-outline-tmpl.yaml` - Complete book structure with learning path
- `chapter-outline-tmpl.yaml` - Individual chapter planning with exercises
- `code-example-tmpl.yaml` - Code examples with explanations and testing

**Sprint 2 (Writing & Publishing):**

- `chapter-draft-tmpl.yaml` - Complete chapter manuscript structure
- `technical-review-report-tmpl.yaml` - Review findings and recommendations
- `tutorial-section-tmpl.yaml` - Step-by-step tutorial structure
- `exercise-set-tmpl.yaml` - Practice exercises with solutions
- `book-proposal-tmpl.yaml` - Publisher proposal document
- `introduction-tmpl.yaml` - Chapter introduction structure

**Sprint 2.6 (Section-Driven Development):**

- `section-plan-tmpl.yaml` - Section plan with acceptance criteria (BMad story analog)

**Sprint 3 (Specialist Templates):**

- `learning-objectives-tmpl.yaml` - Learning objective definition with Bloom's Taxonomy
- `api-reference-tmpl.yaml` - API documentation structure with parameters and examples
- `diagram-spec-tmpl.yaml` - Technical diagram specifications
- `preface-tmpl.yaml` - Book preface/foreword structure
- `appendix-tmpl.yaml` - Appendix content structure

### Tasks (15 Total)

**Sprint 1 (Planning):**

- `design-book-outline.md` - Create publisher-aligned book structures
- `create-code-example.md` - Develop tested, documented code examples
- `test-code-examples.md` - Automated testing workflow for all examples
- `create-learning-objectives.md` - Define measurable learning outcomes
- `create-chapter-outline.md` - Plan chapter structure and content

**Sprint 2 (Writing & Review):**

- `write-chapter-draft.md` - Complete chapter manuscript writing workflow
- `technical-review-chapter.md` - Comprehensive chapter review workflow
- `copy-edit-chapter.md` - Editorial polish workflow
- `develop-tutorial.md` - Hands-on tutorial creation workflow
- `design-exercises.md` - Exercise creation workflow

**Sprint 3 (Specialist Tasks):**

- `generate-api-docs.md` - API reference documentation workflow
- `create-diagram-spec.md` - Diagram design workflow with accessibility
- `write-introduction.md` - Chapter introduction creation with hooks and objectives
- `write-summary.md` - Chapter summary creation with reinforcement
- `build-glossary.md` - Glossary compilation workflow

### Checklists (18 Total)

**Sprint 1 (Quality Foundations):**

- Learning objectives validation
- Code quality verification
- Code testing requirements
- Tutorial effectiveness
- Chapter completeness
- Exercise difficulty assessment
- Prerequisite clarity
- Version compatibility

**Sprint 2 (Review & Publishing):**

- Technical accuracy checklist
- Security best practices checklist
- Performance considerations checklist
- PacktPub submission checklist
- O'Reilly format checklist
- Manning MEAP checklist
- Accessibility checklist

**Sprint 3 (Visual & Documentation Quality):**

- Diagram clarity checklist
- Screenshot quality checklist
- Glossary accuracy checklist

### Workflows (12 Core Workflows)

**Sprint 2:**

- `chapter-development-workflow.yaml` - Complete chapter creation workflow (v2.0 - refactored Sprint 2.6)
- `tutorial-creation-workflow.yaml` - Tutorial development workflow

**Sprint 2.5:**

- `book-planning-workflow.yaml` - Book planning from concept to approved outline
- `code-example-workflow.yaml` - Code example development and testing
- `technical-review-workflow.yaml` - Comprehensive technical review

**Sprint 2.6 (Section-Driven Development):**

- `section-planning-workflow.yaml` - Break chapter into sections (BMad epic → stories analog)
- `section-development-workflow.yaml` - Write one section (BMad story development analog)
- `chapter-assembly-workflow.yaml` - Merge sections into chapter (BMad sprint review analog)

**Sprint 3 (Publisher-Specific Workflows):**

- `packtpub-submission-workflow.yaml` - PacktPub submission preparation workflow
- `oreilly-submission-workflow.yaml` - O'Reilly submission preparation workflow
- `manning-meap-workflow.yaml` - Manning MEAP chapter preparation workflow
- `self-publishing-workflow.yaml` - Self-publishing preparation (Leanpub/KDP/Gumroad)

### Knowledge Bases (6 Total)

- `bmad-kb.md` - Core technical writing methodology
- `book-structures.md` - PacktPub, O'Reilly, Manning formats
- `learning-frameworks.md` - Bloom's Taxonomy, scaffolding principles
- `code-style-guides.md` - Python, JavaScript, Java standards (COMPLETE)
- `publisher-guidelines.md` - Publisher-specific requirements (EXPANDED in Sprint 2)
- `technical-writing-standards.md` - Writing standards (COMPLETE in Sprint 2)

## 🎯 Use Cases

### Technical Book Writing

- Plan complete book structure with learning objectives
- Design hands-on tutorials and exercises
- Create and test code examples across versions
- Validate pedagogical effectiveness

### Course Material Development

- Structure learning paths for technical courses
- Create progressive tutorial sequences
- Develop practice exercises with solutions
- Ensure prerequisite clarity

### Documentation Writing

- Design tutorial-based documentation
- Create working code examples
- Structure content for different learning styles
- Validate instructional effectiveness

### Book Updates (Brownfield)

- Update existing books for new framework versions
- Add new chapters to existing content
- Refresh code examples for current standards
- Incorporate technical reviewer feedback

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Follow BMad Method conventions
4. Submit a PR with clear description

## 📄 License

This expansion pack follows the same license as BMad Method core.

## 🙏 Credits

Created by Wes for the BMad Method community.

Special thanks to Brian (BMad) for creating the BMad Method framework.

---

**Version:** 0.3.0 (Sprint 3 - Specialist Agents & Publisher Workflows Complete)
**Compatible with:** BMad Method v4.0+
**Last Updated:** 2025

## ✅ Sprint Status

**Sprint 1 (Complete):** Planning and design foundation

- ✅ 3 planning agents (Instructional Designer, Tutorial Architect, Code Curator)
- ✅ 5 core tasks for book and chapter planning
- ✅ 8 quality checklists
- ✅ 3 templates for planning
- ✅ 6 knowledge bases (initial versions)

**Sprint 2 (Complete):** Review, workflows, and quality assurance

- ✅ 3 review agents (Technical Reviewer, Technical Editor, Book Publisher)
- ✅ 5 additional tasks for writing and review
- ✅ 7 additional checklists (technical, security, performance, publisher, accessibility)
- ✅ 6 additional templates for writing and publishing
- ✅ 2 core workflows (chapter development, tutorial creation)
- ✅ Expanded knowledge bases (publisher guidelines, writing standards)

**Sprint 2.5 (Complete):** Workflow orchestration completion

- ✅ 3 additional workflows: Book Planning Workflow, Code Example Workflow, Technical Review Workflow
- ✅ Total: 5 core workflows for complete book development
- ✅ Version bumped to 0.2.5

**Sprint 2.6 (Complete):** Section-driven development (BMad story analog)

- ✅ 3 section-level workflows: Section Planning, Section Development, Chapter Assembly
- ✅ 1 new template: Section Plan Template (section acceptance criteria)
- ✅ Refactored Chapter Development Workflow v2.0 (orchestrates section workflows)
- ✅ Total: 8 core workflows, 10 templates
- ✅ Section-driven approach enables incremental chapter writing (2-5 pages per section)
- ✅ Perfect analog to BMad's story-driven development workflow
- ✅ Parallel section development supported
- ✅ Backward compatible: Traditional full-chapter approach still supported
- ✅ Version bumped to 0.2.6

**Sprint 3 (Complete):** Specialist agents and publisher workflows

- ✅ 3 specialist agents: API Documenter, Screenshot Specialist, Exercise Creator
- ✅ 5 specialist templates: Learning Objectives, API Reference, Diagram Spec, Preface, Appendix
- ✅ 5 specialist tasks: Generate API Docs, Create Diagram Spec, Write Introduction, Write Summary, Build Glossary
- ✅ 4 publisher-specific submission workflows: PacktPub, O'Reilly, Manning MEAP, Self-Publishing
- ✅ 3 visual/documentation checklists: Diagram Clarity, Screenshot Quality, Glossary Accuracy
- ✅ Total: 9 agents, 15 templates, 15 tasks, 12 workflows, 18 checklists
- ✅ Agent team bundle for web UI (technical-book-team.yaml)
- ✅ Complete technical writing system from planning through publication
- ✅ Version bumped to 0.3.0 (beta - specialist agents complete)

**Sprint 4 (Complete):** Brownfield book authoring support - v1.0.0 PRODUCTION RELEASE

- ✅ 1 brownfield agent: Book Analyst (existing book analysis and revision planning specialist)
- ✅ 2 brownfield templates: Book Analysis Report, Revision Plan
- ✅ 5 brownfield tasks: Analyze Existing Book, Plan Book Revision, Update Chapter for Version, Extract Code Patterns, Incorporate Reviewer Feedback
- ✅ 3 brownfield workflows: Book Edition Update, Incorporate Review Feedback, Add Chapter to Existing Book
- ✅ 3 brownfield checklists: Version Update, Revision Completeness, Existing Book Integration
- ✅ Total: 10 agents, 15 templates, 20 tasks, 12 workflows, 21 checklists
- ✅ Brownfield capabilities: 2nd/3rd edition updates, technology version migrations (Python 3.9→3.12), chapter additions to existing books, systematic reviewer feedback incorporation
- ✅ Pattern extraction for maintaining consistency in existing books
- ✅ Surgical update workflows that preserve learning flow and voice/tone
- ✅ Version bumped to 1.0.0 (production ready - complete greenfield + brownfield support)

**Sprint 5 (Complete):** 100% Research Coverage Achievement - v1.1.0 COMPREHENSIVE RELEASE

- ✅ 3 optional agents: Learning Path Designer (prerequisite mapping), Sample Code Maintainer (repository/CI/CD management), Version Manager (multi-version compatibility testing)
- ✅ 13 remaining tasks: design-learning-path, setup-code-repository, version-matrix-check, create-solutions, create-index-entries, take-screenshots, package-for-publisher, prepare-meap-chapter, self-publish-prep, create-preface, create-appendix, design-diagram-set, validate-cross-references
- ✅ 10 additional checklists: cross-platform, inclusive-language, readability, index-completeness, citation-accuracy, final-manuscript, book-proposal, self-publishing-standards, repository-quality, meap-readiness
- ✅ 1 new template: glossary-entry-tmpl.yaml
- ✅ Total: 13 agents (10 required + 3 optional), 18 templates, 33 tasks, 15 workflows, 31 checklists
- ✅ Optional agents can work standalone or merge with existing agents for flexibility
- ✅ Complete coverage of all authoring workflows from planning through publication
- ✅ Enhanced quality assurance with comprehensive checklist coverage
- ✅ Advanced scenarios supported: learning path design, code repository automation, multi-version testing
- ✅ 100% coverage of research specifications achieved
- ✅ Version bumped to 1.1.0 (comprehensive - all research requirements implemented)

## 📚 Section-Driven Development Approach (NEW in Sprint 2.6)

The section-driven approach mirrors BMad's story-driven development workflow, enabling incremental chapter writing:

**Key Concepts:**

- **Section = Story analog**: Each section is a 2-5 page deliverable unit with clear acceptance criteria
- **Incremental progress**: Track "Chapter 3: 5 of 8 sections complete" like story completion
- **Parallel development**: Multiple sections can be developed simultaneously if dependencies allow
- **Work-in-progress reviews**: Review sections as they're completed, not waiting for full chapter
- **Story-driven iteration**: Write → Review → Polish cycle at section level

**Typical Chapter Breakdown:**

- 20-page chapter = 5-8 sections
- Small section: 2-3 pages, 1 concept, 1 code example (3 story points)
- Medium section: 3-4 pages, 1-2 concepts, 2 code examples (5 story points)
- Large section: 4-5 pages, 2-3 concepts, 2-3 code examples (8 story points)

**Workflow Mapping:**

| BMad Software Dev | Book Writing (Section-Driven)                    |
| ----------------- | ------------------------------------------------ |
| PRD Creation      | book-planning-workflow → book outline            |
| Architecture      | chapter-planning → chapter outline               |
| Epic Breakdown    | section-planning-workflow → section list         |
| Story Development | section-development-workflow → completed section |
| Sprint Review     | chapter-assembly-workflow → integrated chapter   |
| Release           | publisher-submission → published chapter         |

**When to Use Section-Driven:**

- Chapters 15+ pages (too large for single sitting)
- Want incremental progress tracking
- Need parallel development capability
- Prefer iterative story-driven approach
- Want to review work before full chapter complete

**When to Use Traditional:**

- Short chapters (<10-12 pages)
- Simple reference sections
- Author prefers writing full chapter at once
- Chapter already partially written

## 🚧 Roadmap

**Future Enhancements** (Post-v1.1.0):

- Video tutorial support and transcription tools
- Internationalization and translation workflows
- Audio/podcast supplement tools
- Interactive exercise platform integration
- AI-powered diagram generation from descriptions
- Advanced code quality automation (linting, security scanning)
- Multi-book series planning and cross-book consistency tools
- Publishing platform API integrations (Leanpub, KDP automation)
