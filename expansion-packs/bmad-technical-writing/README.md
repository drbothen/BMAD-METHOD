# BMad Technical Writing Expansion Pack

Transform your AI into a complete technical book writing studio with specialized agents for technical authors, trainers, and documentation specialists.

## 📚 Overview

The Technical Writing Expansion Pack extends BMad-Method with a comprehensive suite of tools for creating high-quality technical books, tutorials, and instructional content. Whether you're writing for PacktPub, O'Reilly, Manning, or self-publishing, this pack provides structured AI assistance throughout your technical writing process.

### Key Features

- 🤖 **6 Specialized Agents** - Complete writing team from planning to publication
- 📝 **10 Core Tasks** - Full chapter development workflow
- 📋 **15 Quality Checklists** - Technical accuracy, security, performance, publisher compliance, accessibility
- 🎯 **9 Professional Templates** - Book planning, chapter development, review, and publishing
- 📚 **6 Knowledge Bases** - Comprehensive publisher guidelines and technical writing standards
- 🔄 **2 Core Workflows** - Chapter development and tutorial creation workflows

## ✍️ Included Agents

### Planning & Design Team (Sprint 1)

1. **Instructional Designer** 🎓 - Learning objectives, pedagogical structure, and instructional scaffolding
2. **Tutorial Architect** 🏗️ - Hands-on tutorial design, exercise creation, and progressive learning paths
3. **Code Curator** 🔧 - Code example development, testing, version management, and quality assurance

### Review & Publishing Team (Sprint 2)

4. **Technical Reviewer** 🔍 - Technical accuracy verification, security audits, best practices validation
5. **Technical Editor** ✍️ - Clarity improvement, style consistency, publisher formatting, accessibility
6. **Book Publisher** 📦 - Publication preparation, manuscript packaging, publisher-specific formatting

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

## 💡 Usage

### Quick Start

```bash
# Activate individual agents in your IDE
/bmad-tw:instructional-designer
/bmad-tw:tutorial-architect
/bmad-tw:code-curator
/bmad-tw:technical-reviewer
/bmad-tw:technical-editor
/bmad-tw:book-publisher
```

### Core Workflows (Sprint 2)

**Chapter Development Workflow** - Complete chapter creation from outline to publisher-ready:
1. Tutorial Architect creates chapter outline
2. Code Curator develops and tests all code examples
3. Tutorial Architect writes complete chapter draft
4. Technical Reviewer performs comprehensive technical review
5. Tutorial Architect revises based on review feedback
6. Technical Editor performs professional copy editing
7. Tutorial Architect finalizes chapter for publication

**Tutorial Creation Workflow** - Build effective hands-on tutorials:
1. Instructional Designer designs learning path
2. Tutorial Architect creates step-by-step structure
3. Code Curator develops and tests tutorial code
4. Tutorial Architect writes complete tutorial
5. Code Curator tests end-to-end
6. Tutorial Architect revises based on testing
7. Instructional Designer validates learning effectiveness

### Common Use Cases

- **Book Planning** - Create comprehensive book outlines with learning objectives
- **Chapter Development** - Full workflow from outline to publication-ready manuscript
- **Code Example Creation** - Develop, test, and document working code examples
- **Technical Review** - Verify accuracy, security, and best practices
- **Editorial Polish** - Ensure clarity, consistency, and publisher compliance
- **Quality Assurance** - 15 checklists covering all aspects of technical writing quality

## 📋 Key Components

### Templates (9 Total)

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

### Tasks (10 Total)

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

### Checklists (15 Total)

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

### Workflows (2 Core Workflows)

**Sprint 2:**
- `chapter-development-workflow.yaml` - Complete chapter creation workflow
- `tutorial-creation-workflow.yaml` - Tutorial development workflow

**Note:** Sprint 2.5 will add 3 additional workflows (book planning, code example creation, technical review) for a total of 5 core workflows.

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

**Version:** 0.2.0 (Sprint 2 - Beta Release)
**Compatible with:** BMad Method v4.0+
**Last Updated:** 2024

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

## 🚧 Roadmap

**Sprint 2.5** (Next):
- 3 additional workflows: Book Planning Workflow, Code Example Workflow, Technical Review Workflow
- Total: 5 core workflows for complete book development

**Sprint 3** (Planned):
- API Documenter agent
- Screenshot Specialist agent
- Additional publisher-specific agents
- Video tutorial support
- Internationalization support
