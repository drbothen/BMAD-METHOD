# BMad Technical Writing Expansion Pack

Transform your AI into a complete technical book writing studio with specialized agents for technical authors, trainers, and documentation specialists.

## 📚 Overview

The Technical Writing Expansion Pack extends BMad-Method with a comprehensive suite of tools for creating high-quality technical books, tutorials, and instructional content. Whether you're writing for PacktPub, O'Reilly, Manning, or self-publishing, this pack provides structured AI assistance throughout your technical writing process.

### Key Features

- 🤖 **3 Specialized Agents** (Sprint 1) - Instructional design, tutorial architecture, and code curation
- 📝 **5 Core Tasks** - Book outline design, code example creation, testing workflows
- 📋 **8 Quality Checklists** - Learning objectives, code quality, tutorial effectiveness
- 🎯 **3 Professional Templates** - Book outlines, chapter planning, code examples
- 📚 **6 Knowledge Bases** - Publisher guidelines, learning frameworks, code style guides

## ✍️ Included Agents (Sprint 1)

### Core Technical Writing Team

1. **Instructional Designer** - Learning objectives, pedagogical structure, and instructional scaffolding
2. **Tutorial Architect** - Hands-on tutorial design, exercise creation, and progressive learning paths
3. **Code Curator** - Code example development, testing, version management, and quality assurance

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
```

### Common Workflows

- **Book Planning** - Create comprehensive book outlines with learning objectives
- **Chapter Development** - Design chapter structure with tutorials and exercises
- **Code Example Creation** - Develop, test, and document working code examples
- **Quality Assurance** - Validate learning objectives, code quality, and tutorial effectiveness

## 📋 Key Components

### Templates (Sprint 1)

- `book-outline-tmpl.yaml` - Complete book structure with learning path
- `chapter-outline-tmpl.yaml` - Individual chapter planning with exercises
- `code-example-tmpl.yaml` - Code examples with explanations and testing

### Tasks (Sprint 1)

- `design-book-outline.md` - Create publisher-aligned book structures
- `create-code-example.md` - Develop tested, documented code examples
- `test-code-examples.md` - Automated testing workflow for all examples
- `create-learning-objectives.md` - Define measurable learning outcomes
- `create-chapter-outline.md` - Plan chapter structure and content

### Checklists (Sprint 1)

- Learning objectives validation
- Code quality verification
- Code testing requirements
- Tutorial effectiveness
- Chapter completeness
- Exercise difficulty assessment
- Prerequisite clarity
- Version compatibility

### Knowledge Bases (Sprint 1)

- `bmad-kb.md` - Core technical writing methodology
- `book-structures.md` - PacktPub, O'Reilly, Manning formats
- `learning-frameworks.md` - Bloom's Taxonomy, scaffolding principles
- `code-style-guides.md` - Python, JavaScript, Java standards
- `publisher-guidelines.md` - Publisher-specific requirements (placeholder)
- `technical-writing-standards.md` - Writing standards (placeholder)

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

**Version:** 0.1.0 (Sprint 1 - Alpha Release)
**Compatible with:** BMad Method v4.0+
**Last Updated:** 2024

## 🚧 Roadmap

**Sprint 2** (Planned):

- Technical Reviewer agent
- Technical Editor agent
- Book Publisher agent
- Additional templates and workflows
- Enhanced publisher guidelines
- Complete writing standards documentation
