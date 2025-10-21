# Quick Reference Card - Technical Writing Expansion Pack

One-page cheat sheet for most common workflows, agents, and commands.

## Quick Start Command Sequence

**For Writing Your First Chapter**:

```
1. /bmad-tw:instructional-designer
   → *create-book-outline

2. /bmad-tw:instructional-designer
   → *create-chapter-outline

3. /bmad-tw:tutorial-architect
   → *outline-section (repeat for each section)

4. /bmad-tw:code-curator
   → *create-code-example

5. /bmad-tw:tutorial-architect
   → *create-tutorial (write section content)

6. /bmad-tw:technical-reviewer
   → *review-section

7. /bmad-tw:technical-editor
   → *assemble-chapter

8. /bmad-tw:book-publisher
   → *run-workflow packtpub-submission
```

---

## Top 5 Workflows

| # | Workflow | Use When | Time |
|---|----------|----------|------|
| 1 | **book-planning-workflow** | Starting new book, need approved outline | 20-33 hrs |
| 2 | **section-development-workflow** | Writing one section (2-5 pages) | 5-10 hrs |
| 3 | **chapter-assembly-workflow** | Merging sections into complete chapter | 4-6 hrs |
| 4 | **technical-review-workflow** | Validating technical accuracy | 3-6 hrs |
| 5 | **packtpub-submission-workflow** | Preparing for PacktPub submission | 6-10 hrs |

---

## Top 5 Agents

| # | Agent | Purpose | Key Commands |
|---|-------|---------|--------------|
| 1 | **Instructional Designer** 🎓 | Plan learning objectives, book structure | `*create-book-outline`<br>`*create-chapter-outline`<br>`*design-learning-path` |
| 2 | **Tutorial Architect** 📝 | Write tutorials, hands-on content | `*create-tutorial`<br>`*write-walkthrough`<br>`*design-exercises` |
| 3 | **Code Curator** 💻 | Create, test code examples | `*create-code-example`<br>`*test-code-examples`<br>`*setup-code-repository` |
| 4 | **Technical Reviewer** 🔍 | Verify technical accuracy, security | `*review-chapter`<br>`*audit-security`<br>`*verify-best-practices` |
| 5 | **Technical Editor** ✍️ | Polish writing, ensure consistency | `*assemble-chapter`<br>`*improve-clarity`<br>`*check-accessibility` |

---

## Top 5 Checklists

| # | Checklist | Use When | Purpose |
|---|-----------|----------|---------|
| 1 | **chapter-completeness-checklist** | After chapter assembly | Ensure all required elements present |
| 2 | **code-quality-checklist** | After code development | Verify code standards met |
| 3 | **technical-accuracy-checklist** | During technical review | Validate correctness |
| 4 | **packtpub-submission-checklist** | Before publisher submission | Ensure PacktPub compliance |
| 5 | **final-manuscript-checklist** | Before final submission | Complete manuscript validation |

---

## Common Commands

### Agent Control
- `*help` - Show agent's available commands
- `*exit` - Exit current agent

### Document Creation
- `*create-doc <template>` - Create document from template
- `*create-book-outline` - Design book structure
- `*create-chapter-outline` - Plan chapter sections
- `*create-tutorial` - Write hands-on tutorial

### Quality Assurance
- `*execute-checklist <checklist>` - Run quality check
- `*review-chapter` - Technical accuracy review
- `*test-code-examples` - Verify code works

### Publishing
- `*run-workflow <workflow>` - Execute publishing workflow
- `*package-for-publisher` - Prepare submission
- `*format-manuscript` - Apply publisher standards

---

## Decision Trees

### Which Workflow Should I Use?

**I want to...**
- **Plan a new book** → `book-planning-workflow`
- **Write one section** → `section-development-workflow`
- **Complete a whole chapter** → `chapter-development-workflow`
- **Review content** → `technical-review-workflow`
- **Submit to PacktPub** → `packtpub-submission-workflow`
- **Submit to O'Reilly** → `oreilly-submission-workflow`
- **Submit to Manning** → `manning-meap-workflow`
- **Self-publish** → `self-publishing-workflow`
- **Update 2nd edition** → `book-edition-update-workflow`
- **Add chapter to existing book** → `add-chapter-to-existing-book-workflow`

### Which Agent Should I Use?

**I want to...**
- **Design learning outcomes** → Instructional Designer
- **Write tutorials** → Tutorial Architect
- **Create code examples** → Code Curator
- **Check technical accuracy** → Technical Reviewer
- **Polish writing** → Technical Editor
- **Prepare for publishing** → Book Publisher
- **Document APIs** → API Documenter
- **Create diagrams** → Screenshot Specialist
- **Design exercises** → Exercise Creator
- **Update existing book** → Book Analyst

---

## File Locations

### Project Structure
```
your-book-project/
├── manuscript/
│   ├── planning/
│   │   ├── book-outline.md
│   │   └── chapter-outlines/
│   ├── sections/
│   │   └── chapter-01/
│   │       ├── section-1.1.md
│   │       └── section-1.2.md
│   ├── chapters/
│   │   └── chapter-01.md
│   └── reviews/
│       └── chapter-01-review.md
├── code-examples/
│   └── chapter-01/
└── submission/
    └── packtpub/
```

---

## Typical Time Estimates

| Activity | Time |
|----------|------|
| Book planning (outline) | 20-33 hrs |
| Chapter outline | 3-5 hrs |
| Section writing (2-5 pages) | 5-10 hrs |
| Code example development | 1-3 hrs |
| Technical review (chapter) | 3-6 hrs |
| Chapter assembly | 4-6 hrs |
| Publisher submission prep | 6-10 hrs |
| **Complete chapter (6 sections)** | **40-70 hrs** |

---

## Section-Driven Development Summary

**Break chapters into 2-5 page sections**:

1. **Plan Sections** - Instructional Designer creates section list
2. **Write Each Section** - Tutorial Architect + Code Curator
3. **Review Sections** - Technical Reviewer validates
4. **Assemble Chapter** - Technical Editor merges

**Benefits**:
- Manageable scope (small chunks)
- Parallel development possible
- Incremental progress visible
- Quality easier to maintain

---

## Quality Gates

### Must Pass Before Moving Forward

**After Book Outline**:
- ✅ All chapters have clear learning objectives
- ✅ Prerequisites flow logically
- ✅ No knowledge gaps between chapters

**After Section Development**:
- ✅ Code examples tested and working
- ✅ Technical review approved
- ✅ 2-5 pages length appropriate
- ✅ Learning objectives met

**After Chapter Assembly**:
- ✅ Smooth transitions between sections
- ✅ Introduction and summary present
- ✅ Cross-references validated
- ✅ Consistent style throughout

**Before Publisher Submission**:
- ✅ All checklists passed
- ✅ Code repository complete
- ✅ Images/diagrams optimized
- ✅ Publisher format requirements met

---

## Next Steps

### New to BMad Technical Writing?
1. Read [Getting Started Tutorial](getting-started.md) - 1-2 hours hands-on
2. Review [User Guide](user-guide.md) - Conceptual overview
3. Start writing your first section!

### Ready to Go Deep?
- [Process Flows](process-flows.md) - Visual workflow diagrams
- [Agent Reference](agent-reference.md) - All 13 agents detailed
- [Workflow Guide](workflow-guide.md) - Complete workflow documentation
- [Template Gallery](template-gallery.md) - All templates with examples

### Need Help?
- [Troubleshooting Guide](troubleshooting.md) - Common issues
- [FAQ](faq.md) - Frequently asked questions
- [Discord Community](https://discord.gg/gk8jAdXWmj) - Get support
- [GitHub Issues](https://github.com/bmadcode/bmad-method/issues) - Report bugs

---

## Print-Friendly Version

**Save this page as PDF for quick reference while writing!**

---

*Quick Reference Card - Technical Writing Expansion Pack v1.1.0*
*Keep this handy while writing your technical book*
