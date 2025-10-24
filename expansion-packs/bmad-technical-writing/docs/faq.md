# FAQ - Frequently Asked Questions

Common questions about the BMad Technical Writing Expansion Pack.

## General Questions

### What is the Technical Writing Expansion Pack?

The Technical Writing Expansion Pack extends BMad-Method with 13 specialized agents, 15 workflows, and comprehensive tools for writing technical books for publishers like PacktPub, O'Reilly, Manning, or self-publishing platforms.

### Who is this for?

Technical book authors, technical trainers, documentation specialists, and anyone creating comprehensive technical content with code examples and tutorials.

### Do I need BMad core?

Yes, this expansion pack requires BMad-Method core to be installed first.

### How much does it cost?

The expansion pack is free and open source, part of the BMad-Method framework.

## Getting Started Questions

### Where should I start?

1. Read the [Quick Reference Card](quick-reference.md) (5 min)
2. Follow the [Getting Started Tutorial](getting-started.md) (1-2 hours)
3. Start writing your first section!

### Which workflow should I use first?

Start with `book-planning-workflow` to create your book outline, then use `section-development-workflow` for incremental chapter development.

### Do I need all 13 agents?

No. The 10 core agents handle most needs. The 3 optional agents (Learning Path Designer, Sample Code Maintainer, Version Manager) are for advanced scenarios.

## Agent Questions

### When should I use optional agents?

- **Learning Path Designer**: Complex prerequisite mapping across 15+ chapters
- **Sample Code Maintainer**: Managing large code repositories with CI/CD
- **Version Manager**: Supporting multiple platform versions (e.g., Python 3.8, 3.9, 3.10, 3.11)

### Can I skip agents?

You can streamline by merging optional agents with core agents for simpler projects.

## Workflow Questions

### Greenfield vs Brownfield - which do I need?

- **Greenfield**: New book from scratch → Use planning and development workflows
- **Brownfield**: Updating existing book (2nd edition, new chapters) → Use brownfield workflows

### Section-driven vs Chapter-driven - what's the difference?

- **Section-driven**: Break chapter into 2-5 page sections, develop independently (recommended)
- **Chapter-driven**: Write entire chapter at once (faster but less manageable)

### Can I customize workflows?

Yes! Workflows are YAML files you can modify. See [Workflow Guide](workflow-guide.md) for details.

## Publishing Questions

### Which publisher workflow should I use?

- **PacktPub** → `packtpub-submission-workflow`
- **O'Reilly** → `oreilly-submission-workflow`
- **Manning** → `manning-meap-workflow`
- **Self-publishing** → `self-publishing-workflow`

### Can I self-publish?

Yes! The `self-publishing-workflow` supports Leanpub, Amazon KDP, and Gumroad.

### Do I need to use publisher workflows?

Only if you're submitting to a publisher. For internal docs or open source, you can skip these.

## Technical Questions

### Can I use this with the Creative Writing expansion?

Yes! You can combine expansion packs. Useful for technical books with narrative elements.

### Can multiple authors collaborate?

Yes! Use Git for version control and coordinate through workflows.

### How does this work with Git?

All outputs are markdown files that work great with Git. Commit sections as you complete them.

## Advanced Questions

### How do I manage multiple versions (Python 3.10, 3.11, etc.)?

Use the Version Manager agent or the `version-matrix-check` task to test across versions.

### Can I write multi-platform books (Windows/Mac/Linux)?

Yes! Use the `cross-platform-checklist` and Code Curator to test on all platforms.

### How do I handle large books (1000+ pages)?

Use section-driven development to break into manageable units. Develop chapters in parallel.

---

## Still Have Questions?

- 📖 [User Guide](user-guide.md) - Comprehensive overview
- 🔧 [Troubleshooting Guide](troubleshooting.md) - Common issues
- 💬 [Discord Community](https://discord.gg/gk8jAdXWmj) - Ask questions
- 🐛 [GitHub Issues](https://github.com/bmadcode/bmad-method/issues) - Report bugs

---

_FAQ - Technical Writing Expansion Pack v1.1.0_
