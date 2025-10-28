# Changelog

All notable changes to the BMad Technical Writing Expansion Pack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

**AI Content Humanization System (Story: ai-content-humanization-feature)**

Complete AI pattern detection and removal system for transforming AI-assisted content into authentic human-written expert guidance:

**Core Humanization Tasks:**
- **humanize-ai-drafted-chapter.md** - 11-step systematic workflow for removing AI patterns from AI-assisted content
  - Baseline detection with generative-ai-compliance-checklist.md
  - Pattern-specific removal for 8 AI pattern types (vocabulary, metaphors, generic examples, impersonal voice, sentence uniformity, flowery language, repetitive content, rigid structure)
  - 8 before/after examples embedded in workflow
  - Validation with humanization-checklist.md (target: <20% AI patterns remaining)
  - Change log documentation
  - REQUIRED when AI tools assisted drafting (ChatGPT, Claude, expand-outline-to-draft, etc.)
  - Time estimate: 2-4 hours per chapter

**Quality Assurance:**
- **humanization-checklist.md** - 45-item validation checklist across 7 categories
  - Validates AI pattern removal effectiveness (not detection)
  - Scoring system: (Items Passed / 45) × 100 = Pass Rate
  - Thresholds: ≥80% pass for humanization step (≤20% AI patterns), ≥95% for copy-edit final check (<5% AI patterns)
  - Categories: Word Choice, Metaphor Quality, Sentence Rhythm, Voice Authenticity, Example Specificity, Content Depth, Structural Variation
  - Distinction from generative-ai-compliance-checklist clarified (detection vs validation)

**Knowledge Bases:**
- **ai-pattern-removal-guide.md** - Comprehensive guide to identifying and fixing 8 AI pattern types
  - 3-4 examples per pattern type (24+ total examples)
  - Each pattern includes: description, detection method, why it matters, replacement strategies, before/after examples, contextual notes
  - Publisher-specific notes (PacktPub "sophisticated" 36x case documented)

- **publisher-specific-ai-patterns.md** - Publisher-focused AI pattern guidance
  - PacktPub: Documented problematic patterns, AI declaration requirements, top 5 patterns
  - O'Reilly: Authoritative voice requirements vs AI generic tone
  - Manning: Author personality expectations vs AI impersonality
  - Self-Publishing: Reader expectations and Amazon review patterns
  - Each publisher includes top 5 patterns, before/after examples, integration with formatting workflows

- **humanization-examples.md** - Before/after example library with 20 transformations
  - Categories: AI vocabulary (4), metaphor problems (3), generic examples (3), impersonal voice (3), sentence uniformity (3), flowery language (2), repetitive content (2)
  - Each example includes: context, before/after with word counts, issues identified, changes made, reader impact, AI score improvement
  - Real metrics (60-95% AI score reductions typical)

**Workflow Integration:**
- **chapter-development-workflow.yaml** - Added humanization step after drafting, before technical review
  - New sequence step: tutorial-architect creates chapter-humanized.md (if AI-assisted)
  - Decision nodes in Mermaid flow diagram (AI-Assisted? branches for both section-driven and traditional approaches)
  - New quality gate: humanization_complete (with validation criteria)
  - Handoff prompts: draft_to_humanization, humanization_to_review, humanization_skipped
  - Time estimates updated (+2-4 hours for humanization when needed)
  - Best practices for humanization workflow added

- **section-development-workflow.yaml** - Added humanization step for section-driven development
  - New sequence step: tutorial-architect creates section-humanized.md (if AI-assisted, after section-draft.md)
  - Decision node in Mermaid flow diagram (AI-Assisted? branch after Write Section)
  - New quality gate: humanization_complete (same criteria as chapter workflow)
  - Handoff prompts: draft_to_humanization, humanization_to_review, humanization_skipped for sections
  - Time estimates updated (+30-60 minutes for section humanization when needed)
  - Best practices updated: "ALWAYS humanize AI-assisted sections before technical review"
  - Note: Sections use same humanize-ai-drafted-chapter.md task (adapted for 2-5 page sections)

- **expand-outline-to-draft.md** - Added "AI-Assisted Drafting & Humanization" section
  - AI use acknowledgment and flag in draft metadata (ai_assisted: YES/NO, requires_humanization: true)
  - Common AI patterns to avoid during drafting (top 5)
  - Required next step workflow documentation (Draft → humanize → validate → review)
  - PacktPub AI declaration requirements referenced
  - Integration with tone specification

- **copy-edit-chapter.md** - Added Step 10: Final AI Pattern Check
  - Execute humanization-checklist.md with target <5% AI patterns remaining
  - 6 substeps: checklist execution, score calculation, specific pattern validation, publisher-specific check, status documentation, results handling
  - Quality gate: Do not finalize chapter with >10% AI patterns
  - EXCELLENT (<5%), ACCEPTABLE (5-10%), NEEDS REWORK (>10%) thresholds

**Agent Awareness:**
- **tutorial-architect** agent updated:
  - Added *humanize command (executes humanize-ai-drafted-chapter.md)
  - Dependencies: humanize-ai-drafted-chapter.md task, humanization-checklist.md, ai-pattern-removal-guide.md, humanization-examples.md
  - Startup context: AI Content Humanization guidance added

- **technical-editor** agent updated:
  - Dependencies: humanization-checklist.md, publisher-specific-ai-patterns.md
  - Startup context: AI Pattern Validation guidance for Step 10 of copy-editing
  - "Think in terms of" list: AI pattern removal added
  - "Always consider" list: Human-written authenticity check added

- **book-publisher** agent updated:
  - Dependencies: humanization-checklist.md, publisher-specific-ai-patterns.md
  - Startup context: AI Compliance Verification guidance before submission
  - "Think in terms of" list: AI compliance added
  - "Always consider" list: AI disclosure and humanization validation added

**Documentation Updates:**
- **README.md**: Updated counts (37 tasks, 33 checklists, 10 knowledge bases), added AI humanization to key features, added note about AI-assisted writing support
- **task-reference.md**: Added humanize-ai-drafted-chapter.md entry, updated copy-edit-chapter.md entry with Step 10 reference, updated task counts (68 tasks total, 13 chapter development tasks)
- **checklist-reference.md**: Added humanization-checklist.md entry with comprehensive details, updated checklist counts (35 total, 7 drafting phase)

**Impact:**
- Complete AI content humanization workflow from detection to validation
- Publisher compliance (PacktPub AI disclosure requirements)
- Reader trust (prevents "AI-generated feel" negative reviews)
- Systematic pattern removal with measurable quality thresholds
- Integration across entire chapter development lifecycle

## [2.4.0] - 2025-10-27

### Added

**Section-Writing Enhancements:**
- Added `*write-section` command to tutorial-architect agent for direct access to write-section-draft.md task
  - Enables section-driven workflow (incremental chapter development)
  - Provides 2-5 page granular writing capability
  - Complements existing `*create-tutorial` and chapter-level commands

### Enhanced

**Tone Awareness for Section Writing:**
- **write-section-draft.md** - Added comprehensive tone specification guidance
  - Prerequisites now require tone-specification.md review
  - Step 1 includes "Review Tone Specification" subsection with formality level, characteristics, example passages
  - Quality checklists updated to verify tone alignment
  - Quality standards updated to include tone matching

**tutorial-architect Agent:**
- Added write-section-draft.md to task dependencies
- Updated startup context with section-driven workflow guidance
- Enhanced "Think in terms of" and "Always consider" lists to include tone awareness
- Clarified that tone definition applies to both chapters and sections

**Impact:**
- Complete tone coverage across all writing workflows (chapter-level, section-level, and AI-assisted)
- Consistent voice enforcement from first sentence in section-driven development
- Tutorial-architect now supports both monolithic (chapter) and incremental (section) writing approaches

## [2.3.0] - 2025-10-27

### Added

**Tone Specification System (Story: tone-specification-feature)**

Complete tone and voice management system for maintaining consistent writing style throughout technical books:

**Core Tasks (Greenfield):**
- **define-book-tone.md** - 8-step elicitation workflow for defining book tone before writing begins
  - Formality level definition (1-5 scale with examples)
  - 5 tone characteristics selection (encouraging, authoritative, practical, etc.)
  - Publisher-specific guidance (PacktPub, O'Reilly, Manning, Self-Publishing)
  - Example passages demonstrating target tone
  - Excluded tones/anti-patterns documentation

**Brownfield Tasks (Editions/Updates):**
- **extract-tone-patterns.md** - Extract voice and tone patterns from existing book chapters
  - 9-step workflow analyzing 3-5 existing chapters
  - Voice profile extraction (perspective, active/passive, formality)
  - Common phrase pattern identification
  - Code comment style analysis
  - Author personality marker extraction

- **apply-tone-patterns.md** - Apply extracted patterns to new content for consistency
  - 10-step workflow for tone alignment
  - Voice characteristic matching
  - Formality level adjustment
  - Code comment style alignment
  - Tone adjustment logging

**Template:**
- **tone-specification-tmpl.yaml** - Structured 12-section template for tone documentation
  - Elicitation-enabled for interactive completion
  - Book overview, tone personality, voice characteristics
  - Formality level specification, publisher alignment
  - Example passages, consistency rules, excluded tones

**Checklist:**
- **tone-consistency-checklist.md** - Comprehensive tone validation (10 categories, 15+ items)
  - Voice consistency, formality level, publisher alignment
  - Code comment style, transition patterns
  - Before/after correction examples
  - Red flags and remediation process

**Knowledge Base:**
- **writing-voice-guides.md** - Reference guide with 6 tone profile examples
  - Academic/Formal, Authoritative/Technical, Professional/Conversational
  - Casual/Friendly, Encouraging/Supportive, Direct/Pragmatic
  - Sample passages (3-5 paragraphs each) demonstrating each profile
  - Decision matrix for choosing appropriate tone
  - Publisher-specific tone preferences

**Workflow Integration:**
- **book-planning-workflow.yaml** - Added tone definition step after outline, before validation
  - Updated Mermaid flow diagram with tone definition node
  - New quality gate: `tone_specification_complete`
  - Handoff prompts: `outline_to_tone`, `tone_to_validation`
  - Time estimate: 2-3 hours for tone definition

**Task Enhancements:**
- **expand-outline-to-draft.md** - Enhanced with Step 1: Review Tone Specification (MANDATORY)
  - Tone application examples comparing formality levels
  - Error handling for missing tone-specification.md

- **copy-edit-chapter.md** - Enhanced Step 9 with 5 substeps for tone validation
  - Load tone reference document (greenfield/brownfield)
  - Execute tone-consistency-checklist.md
  - Document tone violations with examples
  - Apply corrections systematically
  - Verify author voice authenticity

**Agent Updates:**
- **instructional-designer.md** - Added `*define-tone` command, tone awareness in startup context
- **tutorial-architect.md** - Added `*define-tone` command, tone reminder in startup context
- **technical-editor.md** - Added `*validate-tone` command, tone validation responsibility

**Use Cases:**
- **Greenfield**: Define tone → Generate specification → Apply during drafting → Validate during editing
- **Brownfield**: Extract patterns → Apply to new chapters → Validate consistency
- **Multi-author**: Shared tone specification ensures unified voice across contributors

**Impact:**
- Prevents tone drift in 400+ page manuscripts
- Enables consistent AI-assisted chapter drafting
- Maintains author voice across editions
- Meets publisher-specific tone requirements

## [2.2.0] - 2025-10-26

### Added

**Content Generation and Enhancement Tasks (Story 7.18)**

Four new AI-assisted content generation tasks for accelerating book writing:

- **expand-outline-to-draft.md** - Converts bullet-point outlines into initial prose drafts with AI assistance
  - 6-step workflow: Review outline → Expand bullets → Integrate code → Add structure → Quality check → Save as draft
  - Prominent AI safety warnings and mandatory human verification
  - Before/after examples showing outline → prose transformation
  - Expected time savings: 2-4 hours per chapter

- **generate-explanation-variants.md** - Creates multiple ways to explain complex technical concepts
  - 5 explanation approaches: Analogy, Bottom-up, Top-down, Example-driven, Comparison-based
  - Comprehensive evaluation matrix for selecting best variant
  - Detailed JavaScript closure examples demonstrating all approaches
  - Selection and combination guidance for multi-learning-style content

- **extract-reusable-content.md** - Identifies patterns and explanations reusable across chapters
  - 4 pattern categories: Concept explanations, Code patterns, Troubleshooting, Best practices
  - Complete content library directory structure
  - Pattern documentation template for consistency
  - Usage tracking system to monitor pattern reuse

- **generate-cross-references.md** - Suggests where to add "see Chapter X" references
  - 4 reference types: Prerequisite, Related, Forward, Example
  - Priority system (high/medium/low) with clear criteria
  - Reciprocal reference checking for bidirectional navigation
  - Cross-reference best practices and formatting standards

**Agent Integration:**

- `tutorial-architect.md` - Added expand-outline-to-draft.md and generate-explanation-variants.md to dependencies
- `technical-editor.md` - Added extract-reusable-content.md and generate-cross-references.md to dependencies

**Research and Brainstorming Tasks (Story 7.16)**

Two new tasks for early-stage research and ideation:

- **brainstorm-chapter-ideas.md** - Generates chapter ideas from topic analysis
  - Mind mapping and concept clustering techniques
  - Learning progression analysis
  - Topic dependency identification
  - Example: Generated 12 chapter ideas from "Modern JavaScript" topic

- **synthesize-research-notes.md** - Transforms research notes into structured outlines
  - Multi-source research aggregation
  - Automatic outline generation with hierarchical structure
  - Code example placeholders
  - Integration with expand-outline-to-draft.md for complete workflow

### Changed

**Orphaned Templates Resolution (Story 7.15)**

- **api-documenter.md**: Added `glossary-entry-tmpl.yaml` to dependencies for structured glossary entry creation
- **tutorial-architect.md**: Added `section-plan-tmpl.yaml` to dependencies for section-level planning
- **build-glossary.md**: Added note referencing `glossary-entry-tmpl.yaml` template for individual glossary entries
- Both previously orphaned templates now properly integrated with their parent agents

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
