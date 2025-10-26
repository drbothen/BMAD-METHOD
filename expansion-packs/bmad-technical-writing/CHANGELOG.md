# Changelog

All notable changes to the BMad Technical Writing Expansion Pack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

**PacktPub Formatting Workflow - v6 Script Update**

- Updated all references from `apply-packt-styles-v5.py` to `apply-packt-styles-v6.py`
- Enhanced script now includes:
  - Table caption detection and styling (format: `Table X.Y: Description`)
  - Figure caption detection and styling (embedded images + keywords)
  - Automatic table cell styling: "Table Column Heading [PACKT]" / "Table Column Content [PACKT]"
  - Both table and figure captions styled as "Figure Caption [PACKT]" (PacktPub standard)

**Updated Files**:
- `tasks/format-for-packtpub.md` - Script reference updated to v6, added caption placement section (2.3)
- `README.md` - Script reference and usage examples updated to v6
- `workflows/packtpub-submission-workflow.yaml` - Added caption placement requirements and common pitfalls

### Added

**Caption Placement Documentation**

- `data/packtpub-author-bundle/CAPTION-PLACEMENT-GUIDE.md` - Comprehensive 200+ line guide covering:
  - **CRITICAL RULE**: Table captions BEFORE tables, figure captions AFTER images
  - Common mistakes with examples
  - Numbering conventions (`Table X.Y:` / `Figure X.Y:`)
  - Alt text vs caption distinction
  - Why placement matters for reader comprehension
  - Integration with validation scripts

**Enhanced Task Documentation**

- Added section 2.3 "Caption Placement Validation" to `tasks/format-for-packtpub.md`
- Updated Python script logic documentation (steps 7-8) for caption and table styling
- Added CAPTION-PLACEMENT-GUIDE.md to related files documentation

**Workflow Enhancements**

- Updated `packtpub-submission-workflow.yaml`:
  - Quality gates now include caption placement validation
  - Format requirements specify table/figure caption formats
  - Common pitfalls warn about incorrect caption placement

### Technical Details

**Script Changes (v5 → v6)**:
- New function: `is_figure_caption()` - Detects both table and figure captions
- New function: `has_image()` - Checks for embedded images in paragraphs
- Table caption regex: `r'^Table\s+\d+\.\d+:'`
- Automatic table cell styling based on row position (first row = headers)
- **NEW**: Automatic removal of Pandoc alt text paragraphs for cleaner output
- **FIXED**: 2-paragraph lookback for figure caption detection (handles Pandoc 3-para structure)
- **SIMPLIFIED**: After alt text removal, only need 1-paragraph lookback

**Testing** (Comprehensive):
- ✅ 5 tables tested with captions (139 cells: 25 headers + 114 content)
- ✅ 4 figures tested with embedded images (all captions detected)
- ✅ Alt text removal: 4 paragraphs removed (130 → 126 total)
- ✅ All captions correctly positioned and styled (9/9 = 100%)
- ✅ Code blocks: 2/2 correctly styled
- ✅ Lists: 34/34 items correctly styled
- ✅ Pre-conversion validation: PASS (0 errors, warnings only)
- ✅ Post-conversion verification: PASS (0 errors)
- ✅ **Overall compliance: 126/126 paragraphs (100%)**

---

## [2.0.0] - 2025-10-21

### 🚨 BREAKING CHANGES

#### Directory Structure Refactor: `docs/` → `manuscript/`

**Changed**: All book content directories renamed from `docs/` to `manuscript/` for semantic clarity and industry alignment.

**Migration Required**: Existing v1.x projects must rename their `docs/` directory to `manuscript/`.

**Affected Paths**:

- `docs/planning/` → `manuscript/planning/`
- `docs/sections/` → `manuscript/sections/`
- `docs/chapters/` → `manuscript/chapters/`
- `docs/outlines/` → `manuscript/outlines/`
- `docs/reviews/` → `manuscript/reviews/`

**Rationale**:

- ✅ Aligns with publishing industry terminology ("manuscript submission")
- ✅ Provides semantic clarity (manuscript content vs project documentation)
- ✅ Enables clear separation: `manuscript/` for book content, `docs/` for project meta-docs
- ✅ Reduces confusion for GitHub contributors

**Migration Guide**: See [docs/MIGRATION-v2.md](docs/MIGRATION-v2.md) for complete migration instructions.

**Architectural Decision**: See [docs/decisions/ADR-001-manuscript-directory.md](docs/decisions/ADR-001-manuscript-directory.md) for full rationale.

### Changed

- **All Workflows** (15 total): Updated all file path references from `docs/` to `manuscript/`
  - `workflows/section-development-workflow.yaml`
  - `workflows/section-planning-workflow.yaml`
  - `workflows/chapter-development-workflow.yaml`
  - `workflows/chapter-assembly-workflow.yaml`
  - `workflows/book-planning-workflow.yaml`
  - `workflows/book-edition-update-workflow.yaml`
  - `workflows/incorporate-review-feedback-workflow.yaml`
  - `workflows/packtpub-submission-workflow.yaml`
  - `workflows/oreilly-submission-workflow.yaml`
  - `workflows/manning-meap-workflow.yaml`
  - `workflows/self-publishing-workflow.yaml`
  - `workflows/tutorial-creation-workflow.yaml`
  - `workflows/code-example-workflow.yaml`
  - All other workflows validated and updated

- **All Tasks** (33 total): Updated file path references in all task definitions
- **All Templates** (18 total): Updated output path specifications
- **All Checklists** (31 total): Updated file location references
- **All Agents** (13 total): Updated directory references in agent definitions

- **Documentation**: Complete documentation overhaul
  - `README.md`: Added "Project Structure" section explaining `manuscript/` rationale
  - `docs/quick-reference.md`: Updated project structure diagram
  - `docs/workflow-guide.md`: Updated all file path examples
  - `docs/integration-guide.md`: Updated git workflow examples
  - `docs/troubleshooting.md`: Updated directory creation commands
  - `docs/user-guide.md`: Updated all file path references

### Added

- **Migration Guide**: `docs/MIGRATION-v2.md` - Step-by-step migration instructions from v1.x to v2.0
- **Architecture Decision Record**: `docs/decisions/ADR-001-manuscript-directory.md` - Complete rationale for directory structure change
- **Directory Structure Section**: Added to README.md explaining the semantic benefits of `manuscript/` over `docs/`

### Technical Details

- **Version**: Bumped from 1.1.0 → 2.0.0 (major version due to breaking change)
- **Build System**: All builds passing with new directory structure
- **Validation**: All configuration validation passing
- **Backward Compatibility**: v1.x documentation archived with clear deprecation notice

### Upgrade Path

**Simple Migration** (most users):

```bash
cd your-book-project
mv docs manuscript
```

**See Full Guide**: [docs/MIGRATION-v2.md](docs/MIGRATION-v2.md)

---

## [1.1.0] - 2024-XX-XX

### Added

**Sprint 5: 100% Research Coverage Achievement**

- 3 optional specialist agents:
  - Learning Path Designer (prerequisite mapping and skill progression)
  - Sample Code Maintainer (repository and CI/CD management)
  - Version Manager (multi-version compatibility testing)

- 13 additional tasks:
  - `design-learning-path.md`
  - `setup-code-repository.md`
  - `version-matrix-check.md`
  - `create-solutions.md`
  - `create-index-entries.md`
  - `take-screenshots.md`
  - `package-for-publisher.md`
  - `prepare-meap-chapter.md`
  - `self-publish-prep.md`
  - `create-preface.md`
  - `create-appendix.md`
  - `design-diagram-set.md`
  - `validate-cross-references.md`

- 10 additional checklists:
  - Cross-platform compatibility
  - Inclusive language
  - Readability standards
  - Index completeness
  - Citation accuracy
  - Final manuscript review
  - Book proposal quality
  - Self-publishing standards
  - Repository quality
  - MEAP readiness

- 1 new template: `glossary-entry-tmpl.yaml`

### Changed

- Total agents: 13 (10 required + 3 optional)
- Total templates: 18
- Total tasks: 33
- Total workflows: 15
- Total checklists: 31
- Complete coverage of all authoring workflows from planning through publication

---

## [1.0.0] - 2024-XX-XX

### Added

**Sprint 4: Brownfield Book Authoring Support - Production Release**

- Book Analyst agent for existing book analysis and revision planning
- 2 brownfield templates: Book Analysis Report, Revision Plan
- 5 brownfield tasks: Analyze Existing Book, Plan Book Revision, Update Chapter for Version, Extract Code Patterns, Incorporate Reviewer Feedback
- 3 brownfield workflows: Book Edition Update, Incorporate Review Feedback, Add Chapter to Existing Book
- 3 brownfield checklists: Version Update, Revision Completeness, Existing Book Integration

### Changed

- Total agents: 10
- Total templates: 15
- Total tasks: 20
- Total workflows: 12
- Total checklists: 21
- Marked as production-ready (v1.0.0)

### Features

- Complete greenfield + brownfield support
- 2nd/3rd edition update workflows
- Technology version migration support
- Systematic reviewer feedback incorporation
- Pattern extraction for consistency

---

## [0.3.0] - 2024-XX-XX

### Added

**Sprint 3: Specialist Agents and Publisher Workflows - Beta Release**

- 3 specialist agents: API Documenter, Screenshot Specialist, Exercise Creator
- 5 specialist templates: Learning Objectives, API Reference, Diagram Spec, Preface, Appendix
- 5 specialist tasks: Generate API Docs, Create Diagram Spec, Write Introduction, Write Summary, Build Glossary
- 4 publisher-specific submission workflows: PacktPub, O'Reilly, Manning MEAP, Self-Publishing
- 3 visual/documentation checklists: Diagram Clarity, Screenshot Quality, Glossary Accuracy
- Agent team bundle for web UI (technical-book-team.yaml)

### Changed

- Total agents: 9
- Total templates: 15
- Total tasks: 15
- Total workflows: 12
- Total checklists: 18

---

## [0.2.6] - 2024-XX-XX

### Added

**Sprint 2.6: Section-Driven Development Workflow**

- Section-driven development workflow (story analog for book writing)
- Section planning workflow
- Section development workflow
- Chapter assembly workflow
- Parallel section development support
- Incremental progress tracking (X of N sections complete)

### Changed

- Enhanced chapter development workflow to support both section-driven and traditional approaches
- Backward compatible with full-chapter writing approach

---

## [0.2.0] - 2024-XX-XX

### Added

**Sprint 2: Review & Publishing Team**

- 3 review/publishing agents: Technical Reviewer, Technical Editor, Book Publisher
- Review and publishing templates
- Code review and editorial tasks
- Publisher submission workflows
- Quality assurance checklists

---

## [0.1.0] - 2024-XX-XX

### Added

**Sprint 1: Planning & Design Team - Initial Release**

- 3 core agents: Instructional Designer, Tutorial Architect, Code Curator
- Book planning templates and workflows
- Chapter development workflows
- Code example creation and testing tasks
- Basic quality checklists

---

[2.0.0]: https://github.com/bmadcode/bmad-method/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/bmadcode/bmad-method/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/bmadcode/bmad-method/compare/v0.3.0...v1.0.0
[0.3.0]: https://github.com/bmadcode/bmad-method/compare/v0.2.6...v0.3.0
[0.2.6]: https://github.com/bmadcode/bmad-method/compare/v0.2.0...v0.2.6
[0.2.0]: https://github.com/bmadcode/bmad-method/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/bmadcode/bmad-method/releases/tag/v0.1.0
