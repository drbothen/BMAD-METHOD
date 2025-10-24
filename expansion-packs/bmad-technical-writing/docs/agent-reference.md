# Agent Reference Guide

## Introduction

The BMad Technical Writing Expansion Pack provides **13 specialized AI agents** designed to support every phase of technical book authorship—from planning to publication. Each agent is a specialized persona with specific expertise, commands, dependencies, and integration patterns.

This comprehensive reference guide documents all 13 agents, organized by category, with detailed information about:

- **Purpose and role** - What the agent does and their expertise
- **When to use** - Specific scenarios where this agent is most effective
- **Key commands** - All available commands with descriptions
- **Dependencies** - Templates, tasks, checklists, and data files used
- **Usage examples** - Real command sequences for common scenarios
- **Integration patterns** - Which other agents they work with

### Agent Categories

- **Core Planning Agents (3)**: Design book structure, learning architecture, and content organization
- **Core Review Agents (2)**: Ensure technical accuracy and editorial polish
- **Core Publishing Agent (1)**: Prepare manuscripts for submission
- **Specialist Agents (3)**: Handle API docs, visual documentation, and exercises
- **Brownfield Agent (1)**: Analyze existing books and plan revisions
- **Optional Agents (3)**: Provide advanced capabilities for complex scenarios

---

## Core Planning Agents

These agents are essential for the planning and drafting phases of technical book writing.

### 🎓 Instructional Designer

**Agent ID**: `instructional-designer`
**Title**: Learning Architecture Specialist

#### Purpose and Role

Expert in learning experience architecture and pedagogical structure. Masters Bloom's taxonomy, scaffolding principles, cognitive load theory, and adult learning methodologies. Designs book structures and learning paths that enable readers to successfully master technical content.

#### When to Use

- Designing overall book outlines with learning-focused chapter progression
- Creating learning objectives for chapters and sections
- Mapping prerequisite knowledge and scaffolding sequences
- Analyzing difficulty curves to ensure proper learning progression
- Designing assessment strategies aligned with learning objectives
- Applying pedagogical frameworks (Bloom's taxonomy, cognitive load theory)

#### Key Commands

- `*help` - Show numbered list of available commands
- `*create-book-outline` - Runs `design-book-outline.md` task to create pedagogically sound book structure
- `*create-learning-objectives` - Runs `create-learning-objectives.md` task to define measurable learning outcomes
- `*design-learning-path` - Maps prerequisite dependencies and skill progression
- `*analyze-difficulty-curve` - Ensures proper learning progression across chapters
- `*design-assessment-strategy` - Creates exercises and quizzes aligned with objectives
- `*apply-learning-framework` - Applies Bloom's taxonomy or other pedagogical frameworks
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-doc.md`, `design-book-outline.md`, `create-learning-objectives.md`, `execute-checklist.md`
**Templates**: `book-outline-tmpl.yaml`, `chapter-outline-tmpl.yaml`
**Checklists**: `learning-objectives-checklist.md`, `prerequisite-clarity-checklist.md`
**Data**: `bmad-kb.md`, `learning-frameworks.md`, `book-structures.md`

#### Usage Example

```bash
# Start Instructional Designer
/BMad:agents:instructional-designer

# Create book outline for "Python Data Structures Handbook"
*create-book-outline
# Agent elicits: book topic, target audience, prerequisites, learning goals
# Output: book-outline.md with 10 chapters, learning progression

# Create learning objectives for Chapter 3
*create-learning-objectives
# Agent elicits: chapter topic, target Bloom's level, prior knowledge
# Output: learning-objectives.md with measurable outcomes
```

#### Integration Patterns

- **Works with Tutorial Architect**: Instructional Designer defines learning objectives → Tutorial Architect designs tutorials to meet them
- **Works with Exercise Creator**: Provides learning objectives → Exercise Creator designs aligned assessments
- **Works with Learning Path Designer**: Collaborates on prerequisite mapping and skill scaffolding
- **Feeds into**: Chapter development workflows, learning objective validation

---

### 📝 Tutorial Architect

**Agent ID**: `tutorial-architect`
**Title**: Hands-On Instruction Specialist

#### Purpose and Role

Expert in hands-on instruction and step-by-step learning design. Specializes in breaking down complex topics into actionable steps, creating effective tutorials where readers can follow along and build working solutions.

#### When to Use

- Creating step-by-step tutorial sections
- Designing chapter outlines with hands-on exercises
- Writing detailed walkthroughs and how-to guides
- Adding troubleshooting sections for common issues
- Designing practice exercises and challenges
- Writing chapter summaries and key takeaways

#### Key Commands

- `*help` - Show numbered list of available commands
- `*create-tutorial` - Designs hands-on tutorial section with clear steps
- `*outline-chapter` - Runs `create-chapter-outline.md` task to structure tutorial-based chapters
- `*write-walkthrough` - Creates detailed step-by-step guide with expected outcomes
- `*add-troubleshooting` - Documents common issues and their solutions
- `*design-exercises` - Creates practice problems and hands-on activities
- `*write-summary` - Creates chapter recap and key takeaways
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-doc.md`, `create-chapter-outline.md`, `execute-checklist.md`
**Templates**: `chapter-outline-tmpl.yaml`
**Checklists**: `tutorial-effectiveness-checklist.md`, `chapter-completeness-checklist.md`, `exercise-difficulty-checklist.md`
**Data**: `bmad-kb.md`, `learning-frameworks.md`, `book-structures.md`

#### Usage Example

```bash
# Start Tutorial Architect
/BMad:agents:tutorial-architect

# Create chapter outline for tutorial-heavy chapter
*outline-chapter
# Agent elicits: chapter topic, target skills, prerequisites
# Output: chapter-outline.md with tutorial steps, exercises, troubleshooting

# Create walkthrough for "Building Your First Binary Tree"
*write-walkthrough
# Agent guides creation of step-by-step tutorial
# Output: Tutorial section with clear steps, expected results, troubleshooting
```

#### Integration Patterns

- **Works with Instructional Designer**: Receives learning objectives → Creates tutorials to teach them
- **Works with Code Curator**: Tutorial Architect designs tutorial flow → Code Curator ensures all code works
- **Works with Exercise Creator**: Creates tutorial content → Exercise Creator adds practice problems
- **Feeds into**: Chapter development workflows, section-driven development

---

### 💻 Code Curator

**Agent ID**: `code-curator`
**Title**: Code Example Quality Guardian

#### Purpose and Role

Expert in code quality, testing, and example craftsmanship. Ensures every code example works perfectly on first try, follows best practices, and is thoroughly tested across specified versions and platforms.

#### When to Use

- Creating tested, production-quality code examples
- Testing all code examples across versions and platforms
- Verifying version compatibility for specified tech stacks
- Optimizing code examples for clarity and efficiency
- Debugging and troubleshooting code example issues
- Ensuring code follows language-specific style guides

#### Key Commands

- `*help` - Show numbered list of available commands
- `*create-code-example` - Runs `create-code-example.md` task to build tested code snippets
- `*test-all-examples` - Runs `test-code-examples.md` task to validate all code
- `*version-check` - Verifies version compatibility across specified versions
- `*optimize-code` - Improves example clarity, efficiency, and best practices
- `*troubleshoot-example` - Debugs common issues in code examples
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-code-example.md`, `test-code-examples.md`, `execute-checklist.md`
**Templates**: `code-example-tmpl.yaml`
**Checklists**: `code-quality-checklist.md`, `code-testing-checklist.md`, `version-compatibility-checklist.md`
**Data**: `bmad-kb.md`, `code-style-guides.md`

#### Usage Example

```bash
# Start Code Curator
/BMad:agents:code-curator

# Create code example for binary search tree insertion
*create-code-example
# Agent elicits: language, concept to demonstrate, versions
# Output: Fully tested code example with comments, error handling

# Test all examples in chapter
*test-all-examples
# Agent runs tests, reports failures, suggests fixes
# Output: Test report with pass/fail status for each example
```

#### Integration Patterns

- **Works with Tutorial Architect**: Receives code requirements from tutorials → Creates tested, working code
- **Works with Sample Code Maintainer**: Creates examples → Sample Code Maintainer organizes into repository
- **Works with Version Manager**: Collaborates on multi-version testing and compatibility
- **Feeds into**: Code example workflows, technical review processes

---

## Core Review Agents

These agents ensure content quality through technical validation and editorial refinement.

### 🔍 Technical Reviewer

**Agent ID**: `technical-reviewer`
**Title**: Subject Matter Expert & Technical Validator

#### Purpose and Role

Subject matter expert focused on ensuring technical accuracy, security, and best practices. Validates technical content thoroughly while providing constructive guidance for improvement.

#### When to Use

- Conducting comprehensive technical reviews of chapters
- Verifying technical accuracy against official documentation
- Checking code examples for correctness and best practices
- Identifying security vulnerabilities and unsafe patterns
- Assessing performance implications of recommended approaches
- Ensuring information is current and not outdated
- Providing constructive technical feedback

#### Key Commands

- `*help` - Show numbered list of available commands
- `*review-chapter` - Runs `technical-review-chapter.md` task for comprehensive chapter review
- `*verify-accuracy` - Checks technical facts against official documentation
- `*check-best-practices` - Validates code and recommendations follow industry standards
- `*identify-errors` - Finds technical inaccuracies, bugs, or misconceptions
- `*suggest-improvements` - Provides constructive recommendations for enhancements
- `*security-audit` - Reviews code examples for security issues
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-doc.md`, `technical-review-chapter.md`, `execute-checklist.md`
**Templates**: `technical-review-report-tmpl.yaml`
**Checklists**: `technical-accuracy-checklist.md`, `security-best-practices-checklist.md`, `performance-considerations-checklist.md`
**Data**: `bmad-kb.md`, `technical-writing-standards.md`

#### Usage Example

```bash
# Start Technical Reviewer
/BMad:agents:technical-reviewer

# Review Chapter 5 for technical accuracy
*review-chapter
# Agent reads chapter, checks facts, validates code
# Output: technical-review-report.md with findings, severity, recommendations

# Security audit for code examples
*security-audit
# Agent scans for SQL injection, XSS, hardcoded secrets, etc.
# Output: Security findings with severity levels and remediation steps
```

#### Integration Patterns

- **Works with Code Curator**: Reviews Code Curator's examples for correctness and best practices
- **Works with Technical Editor**: Technical Reviewer validates accuracy → Technical Editor improves clarity
- **Receives from**: All content-creating agents (Instructional Designer, Tutorial Architect, etc.)
- **Feeds into**: Technical review workflows, revision planning

---

### ✍️ Technical Editor

**Agent ID**: `technical-editor`
**Title**: Technical Communication Expert & Copy Editor

#### Purpose and Role

Expert in technical writing style, clarity, consistency, flow, and publisher requirements. Transforms technically accurate content into professionally polished, reader-friendly material ready for publication.

#### When to Use

- Copy editing chapters for grammar, spelling, and style
- Improving sentence clarity and readability
- Checking terminology and style consistency
- Enhancing transitions between sections and chapters
- Verifying compliance with publisher style guidelines
- Ensuring accessibility for diverse readers
- Providing professional polish before submission

#### Key Commands

- `*help` - Show numbered list of available commands
- `*edit-chapter` - Runs `copy-edit-chapter.md` for comprehensive editorial review
- `*improve-clarity` - Enhances sentence clarity and readability
- `*check-consistency` - Verifies terminology, style, and formatting consistency
- `*enhance-transitions` - Improves flow between sections and chapters
- `*copy-edit` - Performs professional copy editing (grammar, spelling, style)
- `*check-publisher-style` - Verifies compliance with specific publisher guidelines
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-doc.md`, `copy-edit-chapter.md`, `execute-checklist.md`
**Checklists**: `packtpub-submission-checklist.md`, `oreilly-format-checklist.md`, `manning-meap-checklist.md`, `accessibility-checklist.md`
**Data**: `bmad-kb.md`, `publisher-guidelines.md`, `code-style-guides.md`, `technical-writing-standards.md`

#### Usage Example

```bash
# Start Technical Editor
/BMad:agents:technical-editor

# Copy edit Chapter 3 for clarity and consistency
*edit-chapter
# Agent reviews for clarity, grammar, style, consistency
# Output: Edited chapter with tracked changes and style notes

# Check for O'Reilly compliance
*check-publisher-style
# Agent elicits: target publisher (O'Reilly selected)
# Output: Compliance report with formatting adjustments needed
```

#### Integration Patterns

- **Works with Technical Reviewer**: Technical Reviewer validates accuracy → Technical Editor polishes clarity
- **Works with Book Publisher**: Technical Editor ensures quality → Book Publisher handles formatting
- **Receives from**: All content-creating agents after technical review
- **Feeds into**: Publishing workflows, final submission preparation

---

## Core Publishing Agent

### 📦 Book Publisher

**Agent ID**: `book-publisher`
**Title**: Publication Specialist & Manuscript Packager

#### Purpose and Role

Expert in publisher requirements, submission processes, and professional manuscript packaging for traditional and self-publishing. Transforms finished manuscripts into professionally packaged submissions that meet exact publisher requirements.

#### When to Use

- Preparing book proposals for publishers
- Packaging complete manuscripts for submission
- Formatting for specific publishers (PacktPub, O'Reilly, Manning)
- Preparing chapters for Manning Early Access Program (MEAP)
- Formatting manuscripts for self-publishing platforms
- Creating book indexes from marked terms
- Ensuring all supplementary materials are ready

#### Key Commands

- `*help` - Show numbered list of available commands
- `*prepare-proposal` - Uses `book-proposal-tmpl` to create publisher proposal
- `*package-manuscript` - Organizes and formats complete manuscript for submission
- `*format-for-packtpub` - Applies PacktPub-specific formatting and requirements
- `*format-for-oreilly` - Applies O'Reilly-specific formatting (AsciiDoc, Chicago style)
- `*prepare-meap` - Formats chapter for Manning Early Access Program
- `*self-publish-prep` - Prepares manuscript for self-publishing platforms
- `*create-index` - Generates book index from marked terms
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-doc.md`, `execute-checklist.md`
**Templates**: `book-proposal-tmpl.yaml`, `introduction-tmpl.yaml`
**Checklists**: `packtpub-submission-checklist.md`, `oreilly-format-checklist.md`, `manning-meap-checklist.md`
**Data**: `bmad-kb.md`, `publisher-guidelines.md`

#### Usage Example

```bash
# Start Book Publisher
/BMad:agents:book-publisher

# Prepare O'Reilly book proposal
*prepare-proposal
# Agent elicits: publisher (O'Reilly), book details, author bio
# Output: book-proposal.md formatted for O'Reilly submission

# Package manuscript for PacktPub
*format-for-packtpub
# Agent applies PacktPub style, checks requirements
# Output: Formatted manuscript bundle ready for submission
```

#### Integration Patterns

- **Works with Technical Editor**: Technical Editor polishes content → Book Publisher formats for submission
- **Receives from**: All content agents after review and editing phases
- **Feeds into**: Publisher-specific submission workflows
- **Final agent**: In most workflows (prepares final deliverables)

---

## Specialist Agents

These agents provide specialized capabilities for specific content types.

### 📚 API Documenter

**Agent ID**: `api-documenter`
**Title**: Reference Documentation Specialist

#### Purpose and Role

Expert in API design patterns, documentation standards, and reference material organization. Creates complete, accurate, and searchable reference documentation that developers trust and rely on.

#### When to Use

- Generating comprehensive API reference documentation
- Documenting functions/methods with parameters and return values
- Creating structured parameter/return tables
- Writing API usage examples and patterns
- Building glossaries and terminology references
- Creating reference appendices

#### Key Commands

- `*help` - Show numbered list of available commands
- `*generate-api-docs` - Runs `generate-api-docs.md` to create comprehensive API reference
- `*document-function` - Documents single function with parameters and returns
- `*create-reference-table` - Builds structured parameter/return tables
- `*write-usage-examples` - Creates code examples showing API usage patterns
- `*build-glossary` - Runs `build-glossary.md` to compile terminology reference
- `*generate-appendix` - Creates reference appendix using `appendix-tmpl.yaml`
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-doc.md`, `generate-api-docs.md`, `build-glossary.md`, `execute-checklist.md`
**Templates**: `api-reference-tmpl.yaml`, `appendix-tmpl.yaml`
**Checklists**: `glossary-accuracy-checklist.md`
**Data**: `bmad-kb.md`, `code-style-guides.md`, `technical-writing-standards.md`

#### Usage Example

```bash
# Start API Documenter
/BMad:agents:api-documenter

# Generate API docs for Python data structures module
*generate-api-docs
# Agent analyzes module, extracts functions, parameters
# Output: api-reference.md with complete function documentation

# Build glossary for book
*build-glossary
# Agent compiles terms from chapters
# Output: glossary.md with alphabetized terminology
```

#### Integration Patterns

- **Works with Code Curator**: Code Curator creates examples → API Documenter documents API usage
- **Works with Tutorial Architect**: Creates reference docs → Tutorial Architect uses for tutorial content
- **Specialist role**: Called when API documentation or glossaries needed
- **Feeds into**: Appendix creation, reference section development

---

### 📸 Screenshot Specialist

**Agent ID**: `screenshot-specialist`
**Title**: Visual Documentation Expert

#### Purpose and Role

Expert in technical diagrams, screenshot planning, and visual communication. Creates clear, professional visuals that enhance understanding and meet accessibility standards.

#### When to Use

- Creating technical diagram specifications (flowcharts, sequence diagrams, architecture diagrams)
- Planning screenshot sequences for tutorials
- Annotating images with callouts and labels
- Optimizing visuals for clarity and appropriate file size
- Ensuring accessibility (alt text, color contrast)
- Maintaining visual consistency across the book

#### Key Commands

- `*help` - Show numbered list of available commands
- `*create-diagram-spec` - Runs `create-diagram-spec.md` to design technical diagrams
- `*plan-screenshots` - Plans screenshot sequence and identifies key captures
- `*annotate-images` - Adds callouts, labels, and highlighting
- `*optimize-visuals` - Ensures clarity, file size, and print/web quality
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-doc.md`, `create-diagram-spec.md`, `execute-checklist.md`
**Templates**: `diagram-spec-tmpl.yaml`
**Checklists**: `diagram-clarity-checklist.md`, `screenshot-quality-checklist.md`
**Data**: `bmad-kb.md`, `technical-writing-standards.md`

#### Usage Example

```bash
# Start Screenshot Specialist
/BMad:agents:screenshot-specialist

# Create architecture diagram specification
*create-diagram-spec
# Agent elicits: diagram type, components, relationships
# Output: diagram-spec.md with Mermaid code or detailed specification

# Plan screenshot sequence for tutorial
*plan-screenshots
# Agent identifies key steps needing screenshots
# Output: Screenshot plan with annotations and accessibility notes
```

#### Integration Patterns

- **Works with Tutorial Architect**: Tutorial Architect identifies visual needs → Screenshot Specialist creates diagrams
- **Works with Technical Editor**: Creates visuals → Technical Editor ensures alt text and accessibility
- **Specialist role**: Called when visual documentation is needed
- **Feeds into**: Chapter assembly, visual asset workflows

---

### 🏋️ Exercise Creator

**Agent ID**: `exercise-creator`
**Title**: Practice Problem Designer

#### Purpose and Role

Expert in exercise design, scaffolding practice, and aligned assessment. Creates exercises that reinforce learning, build confidence, and validate mastery through pedagogically sound practice problems.

#### When to Use

- Designing practice problem sets aligned with learning objectives
- Creating end-of-chapter quizzes and knowledge checks
- Writing detailed solutions with explanations
- Calibrating exercise difficulty levels
- Ensuring variety in exercise types
- Aligning exercises with Bloom's taxonomy levels

#### Key Commands

- `*help` - Show numbered list of available commands
- `*design-exercise-set` - Runs `design-exercises.md` to create practice problems
- `*create-quiz` - Designs knowledge check questions for chapter review
- `*write-solutions` - Creates detailed solutions with explanations
- `*grade-difficulty` - Assesses and calibrates exercise difficulty levels
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-doc.md`, `design-exercises.md`, `execute-checklist.md`
**Templates**: `exercise-set-tmpl.yaml`
**Checklists**: `exercise-difficulty-checklist.md`, `learning-objectives-checklist.md`
**Data**: `bmad-kb.md`, `learning-frameworks.md`

#### Usage Example

```bash
# Start Exercise Creator
/BMad:agents:exercise-creator

# Design exercise set for Chapter 4
*design-exercise-set
# Agent elicits: learning objectives, Bloom's level, difficulty
# Output: exercise-set.md with 5-7 problems, solutions, difficulty levels

# Create quiz questions
*create-quiz
# Agent creates multiple choice, short answer, coding challenges
# Output: Quiz with answer key and explanations
```

#### Integration Patterns

- **Works with Instructional Designer**: Receives learning objectives → Creates aligned exercises
- **Works with Tutorial Architect**: Tutorial teaches concepts → Exercise Creator adds practice
- **Works with Code Curator**: Exercise Creator designs coding challenges → Code Curator ensures they work
- **Feeds into**: Chapter development, assessment workflows

---

## Brownfield Agent

### 📖 Book Analyst

**Agent ID**: `book-analyst`
**Title**: Existing Book Analysis & Revision Planning Specialist

#### Purpose and Role

Expert in brownfield book authoring: analyzing existing books, planning 2nd/3rd edition updates, technology version migrations, chapter additions, and systematic incorporation of reviewer feedback while maintaining consistency.

#### When to Use

- Analyzing existing technical books for revision planning
- Planning 2nd/3rd edition updates
- Extracting patterns from existing content (style, voice, code conventions)
- Assessing impact of technology version changes
- Triaging and prioritizing reviewer/publisher feedback
- Identifying outdated content and deprecated APIs
- Planning chapter additions to existing books

#### Key Commands

- `*help` - Show numbered list of available commands
- `*analyze-book` - Runs `analyze-existing-book.md` to analyze current book state
- `*plan-revision` - Runs `plan-book-revision.md` to create strategic revision plan
- `*extract-patterns` - Runs `extract-code-patterns.md` to learn existing code style
- `*assess-version-impact` - Analyzes impact of technology version changes
- `*triage-feedback` - Categorizes and prioritizes reviewer/publisher feedback
- `*identify-outdated-content` - Scans for deprecated APIs and breaking changes
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `create-doc.md`, `analyze-existing-book.md`, `plan-book-revision.md`, `extract-code-patterns.md`, `incorporate-reviewer-feedback.md`, `execute-checklist.md`
**Templates**: `book-analysis-report-tmpl.yaml`, `revision-plan-tmpl.yaml`
**Checklists**: `version-update-checklist.md`, `revision-completeness-checklist.md`, `existing-book-integration-checklist.md`
**Data**: `bmad-kb.md`, `learning-frameworks.md`

#### Usage Example

```bash
# Start Book Analyst
/BMad:agents:book-analyst

# Analyze existing book for 2nd edition planning
*analyze-book
# Agent reads entire book, extracts patterns, identifies issues
# Output: book-analysis-report.md with structure, patterns, outdated content

# Plan revision for Python 3.10 → 3.12 migration
*assess-version-impact
# Agent identifies breaking changes, deprecated features
# Output: version-impact-assessment.md with migration plan
```

#### Integration Patterns

- **Initiates brownfield workflows**: Analyzes existing content → Provides context to other agents
- **Works with all agents**: Provides pattern extraction and consistency guidelines
- **Feeds into**: Revision planning workflows, version update workflows
- **Coordinates**: Book edition updates, chapter additions to existing books

---

## Optional Agents

These agents provide advanced capabilities for complex scenarios. They can be merged with other agents for simpler deployments.

### 🗺️ Learning Path Designer

**Agent ID**: `learning-path-designer`
**Title**: Prerequisite Mapping & Skill Progression Specialist

#### Purpose and Role

Expert in cognitive scaffolding and prerequisite mapping. Designs learning journeys where readers can successfully navigate without encountering unexplained concepts or prerequisite violations.

#### When to Use

- Designing learning progressions and skill trees
- Mapping chapter-to-chapter prerequisite dependencies
- Creating visual skill scaffolding diagrams
- Assessing reader readiness at chapter transitions
- Validating learning flow for knowledge gaps
- Identifying missing foundational topics
- Distinguishing optional vs. required chapters

#### Key Commands

- `*help` - Show numbered list of available commands
- `*map-prerequisites` - Runs `design-learning-path.md` to map chapter dependencies
- `*design-skill-tree` - Creates skill progression tree showing knowledge building
- `*assess-readiness` - Evaluates reader readiness at specific chapter points
- `*validate-learning-flow` - Checks for knowledge gaps and prerequisite violations
- `*identify-gaps` - Finds missing foundational topics or unexplained concepts
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `design-learning-path.md`, `execute-checklist.md`
**Templates**: `learning-objectives-tmpl.yaml`, `book-outline-tmpl.yaml`
**Checklists**: `learning-objectives-checklist.md`, `prerequisite-clarity-checklist.md`
**Data**: `bmad-kb.md`, `learning-frameworks.md`

**Note**: Can be merged with Instructional Designer for simpler deployments. Use this specialist when dealing with complex, multi-level technical topics requiring careful prerequisite analysis.

#### Usage Example

```bash
# Start Learning Path Designer
/BMad:agents:learning-path-designer

# Map prerequisites for entire book
*map-prerequisites
# Agent analyzes chapters, identifies dependencies
# Output: learning-path.md with dependency graph, skill tree

# Validate learning flow
*validate-learning-flow
# Agent checks for knowledge gaps, prerequisite violations
# Output: Validation report with identified gaps and recommendations
```

#### Integration Patterns

- **Works with Instructional Designer**: Collaborates on learning objectives and progression
- **Optional enhancement**: Provides deeper prerequisite analysis than Instructional Designer alone
- **Complex books**: Most useful for multi-level technical topics

---

### 🔧 Sample Code Maintainer

**Agent ID**: `sample-code-maintainer`
**Title**: Code Repository Management & CI/CD Specialist

#### Purpose and Role

DevOps-minded specialist in code repository management and automation. Creates and maintains code repositories that readers can clone, install, and use immediately without frustration.

#### When to Use

- Setting up code repository structure and organization
- Managing dependencies and version pinning
- Creating CI/CD pipelines (GitHub Actions, etc.)
- Automating testing across all code examples
- Publishing repositories for public release
- Maintaining long-term repository health

#### Key Commands

- `*help` - Show numbered list of available commands
- `*organize-code-repo` - Runs `setup-code-repository.md` to create repository structure
- `*update-dependencies` - Updates package dependencies and tests compatibility
- `*create-ci-pipeline` - Sets up GitHub Actions or other CI/CD automation
- `*run-tests` - Executes `test-code-examples.md` across all examples
- `*publish-repo` - Prepares repository for public release
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `setup-code-repository.md`, `test-code-examples.md`, `execute-checklist.md`
**Checklists**: `code-testing-checklist.md`, `repository-quality-checklist.md`, `version-compatibility-checklist.md`
**Data**: `bmad-kb.md`

**Note**: Can be merged with Code Curator for simpler deployments. Use this specialist when managing large code repositories with complex dependencies and CI/CD requirements.

#### Usage Example

```bash
# Start Sample Code Maintainer
/BMad:agents:sample-code-maintainer

# Set up repository for book code
*organize-code-repo
# Agent creates chapter folders, README, dependencies
# Output: Well-organized repository structure

# Create GitHub Actions CI pipeline
*create-ci-pipeline
# Agent creates workflow YAML for automated testing
# Output: .github/workflows/test.yml with matrix testing
```

#### Integration Patterns

- **Works with Code Curator**: Code Curator creates examples → Sample Code Maintainer organizes and automates
- **Optional enhancement**: Provides repository management and CI/CD beyond Code Curator's scope
- **Large codebases**: Most useful for books with extensive code examples

---

### 🔢 Version Manager

**Agent ID**: `version-manager`
**Title**: Multi-Version & Platform Support Specialist

#### Purpose and Role

Expert in multi-version compatibility and cross-platform support. Ensures code examples work correctly across entire version matrix and that readers know exactly which versions are supported.

#### When to Use

- Managing multi-version compatibility testing
- Documenting platform-specific code differences
- Creating version testing matrices
- Testing code across all versions and platforms
- Adapting code examples for specific version requirements
- Documenting breaking changes between versions

#### Key Commands

- `*help` - Show numbered list of available commands
- `*create-version-matrix` - Runs `version-matrix-check.md` to define version testing scope
- `*adapt-for-version` - Modifies code examples for specific version compatibility
- `*platform-variations` - Documents platform-specific code differences
- `*test-matrix` - Executes tests across all versions and platforms in matrix
- `*exit` - Exits persona

#### Dependencies

**Tasks**: `version-matrix-check.md`, `execute-checklist.md`
**Checklists**: `version-compatibility-checklist.md`, `cross-platform-checklist.md`
**Data**: `bmad-kb.md`, `code-style-guides.md`

**Note**: Can be merged with Code Curator for simpler deployments. Use this specialist when writing books covering multiple versions or platforms with significant compatibility differences.

#### Usage Example

```bash
# Start Version Manager
/BMad:agents:version-manager

# Create version testing matrix
*create-version-matrix
# Agent elicits: languages, versions, platforms
# Output: version-matrix.yaml with testing scope (e.g., Python 3.10, 3.11, 3.12)

# Test across matrix
*test-matrix
# Agent runs tests on all version/platform combinations
# Output: Matrix test results with pass/fail for each combination
```

#### Integration Patterns

- **Works with Code Curator**: Collaborates on multi-version testing and compatibility
- **Optional enhancement**: Provides explicit version management beyond Code Curator's testing
- **Multi-version books**: Most useful when covering Python 3.10+3.11+3.12 or Node 18+20+22, etc.

---

## Agent Comparison Table

| Agent                  | Category        | Icon | Primary Focus                                | When to Use                                       |
| ---------------------- | --------------- | ---- | -------------------------------------------- | ------------------------------------------------- |
| Instructional Designer | Core Planning   | 🎓   | Learning architecture, pedagogical structure | Book outlines, learning objectives, scaffolding   |
| Tutorial Architect     | Core Planning   | 📝   | Hands-on tutorials, step-by-step instruction | Tutorial design, chapter outlines, walkthroughs   |
| Code Curator           | Core Planning   | 💻   | Code quality, testing, best practices        | Code examples, testing, version compatibility     |
| Technical Reviewer     | Core Review     | 🔍   | Technical accuracy, security, validation     | Chapter reviews, accuracy checks, security audits |
| Technical Editor       | Core Review     | ✍️   | Clarity, consistency, publisher compliance   | Copy editing, style checks, publication prep      |
| Book Publisher         | Core Publishing | 📦   | Manuscript packaging, submission prep        | Publisher proposals, manuscript formatting        |
| API Documenter         | Specialist      | 📚   | API reference, glossaries, appendices        | API docs, reference tables, glossaries            |
| Screenshot Specialist  | Specialist      | 📸   | Diagrams, screenshots, visual documentation  | Technical diagrams, screenshot planning           |
| Exercise Creator       | Specialist      | 🏋️   | Practice problems, assessments, quizzes      | Exercise sets, quizzes, solutions                 |
| Book Analyst           | Brownfield      | 📖   | Existing book analysis, revision planning    | 2nd editions, version migrations, updates         |
| Learning Path Designer | Optional        | 🗺️   | Prerequisite mapping, skill progression      | Complex skill trees, prerequisite validation      |
| Sample Code Maintainer | Optional        | 🔧   | Repository management, CI/CD                 | Large codebases, automated testing                |
| Version Manager        | Optional        | 🔢   | Multi-version compatibility, platforms       | Multi-version testing, platform differences       |

---

## Agent Selection Decision Tree

**I want to...**

### Plan a new book

→ Start with **Instructional Designer** (`*create-book-outline`)
→ Then **Tutorial Architect** for chapter-level structure
→ Consider **Learning Path Designer** for complex prerequisite mapping

### Create tutorial content

→ Use **Tutorial Architect** (`*create-tutorial`, `*write-walkthrough`)
→ Collaborate with **Code Curator** for tested code examples
→ Add **Exercise Creator** for practice problems

### Ensure code quality

→ Use **Code Curator** (`*create-code-example`, `*test-all-examples`)
→ Add **Sample Code Maintainer** for large repositories with CI/CD
→ Add **Version Manager** for multi-version compatibility

### Review and refine content

→ Use **Technical Reviewer** first (`*review-chapter` for accuracy)
→ Then **Technical Editor** (`*edit-chapter` for clarity and style)
→ Finish with **Book Publisher** for submission formatting

### Create specialized content

→ **API Documenter** for API reference sections
→ **Screenshot Specialist** for diagrams and visuals
→ **Exercise Creator** for practice problem sets

### Update existing book

→ Start with **Book Analyst** (`*analyze-book`, `*plan-revision`)
→ Then coordinate other agents based on revision needs
→ Use **Version Manager** for version migration

---

## Common Agent Workflows

### Greenfield Book (New Book from Scratch)

1. **Instructional Designer** - Create book outline with learning objectives
2. **Tutorial Architect** - Design chapter outlines with tutorial structure
3. **Code Curator** - Develop and test all code examples
4. **Exercise Creator** - Create practice problems and quizzes
5. **Technical Reviewer** - Validate technical accuracy
6. **Technical Editor** - Polish clarity and consistency
7. **Book Publisher** - Format and submit to publisher

### Section-Driven Development

1. **Tutorial Architect** - Outline section with tutorial steps
2. **Code Curator** - Create tested code examples for section
3. **Screenshot Specialist** - Design diagrams and visuals (if needed)
4. **Technical Reviewer** - Review section for accuracy
5. **Technical Editor** - Edit section for clarity
6. Repeat for next section

### Brownfield Book (2nd Edition Update)

1. **Book Analyst** - Analyze existing book, extract patterns
2. **Book Analyst** - Assess version impact, plan revision
3. **Version Manager** - Test code examples on new versions
4. **Code Curator** - Update failing code examples
5. **Technical Reviewer** - Review updated content
6. **Technical Editor** - Ensure consistency with existing style
7. **Book Publisher** - Reformat for submission

### API Reference Book

1. **Instructional Designer** - Structure book around API concepts
2. **API Documenter** - Generate comprehensive API documentation
3. **Code Curator** - Create usage examples for each API
4. **Tutorial Architect** - Create walkthroughs for common patterns
5. **Technical Reviewer** - Validate API accuracy
6. **Technical Editor** - Polish reference documentation
7. **Book Publisher** - Format for publication

---

## Integration Best Practices

### Agent Coordination Principles

1. **Sequential workflows**: Planning agents → Content agents → Review agents → Publishing agent
2. **Parallel collaboration**: Code Curator + Screenshot Specialist can work simultaneously on same chapter
3. **Iteration cycles**: Technical Reviewer → Author revisions → Technical Editor → Final review
4. **Specialist inclusion**: Add API Documenter, Screenshot Specialist, Exercise Creator as needed

### Dependency Sharing

Multiple agents share common dependencies:

- **All agents**: Use `create-doc.md`, `execute-checklist.md`, `bmad-kb.md`
- **Planning agents**: Share `learning-frameworks.md`, `book-structures.md`
- **Code agents**: Share `code-style-guides.md`
- **Review/Publishing agents**: Share `technical-writing-standards.md`, `publisher-guidelines.md`

### When to Use Optional Agents

- **Learning Path Designer**: Complex books with deep prerequisite dependencies (e.g., advanced algorithms, distributed systems)
- **Sample Code Maintainer**: Books with 50+ code examples, complex build systems, or CI/CD requirements
- **Version Manager**: Books covering Python 3.10/3.11/3.12 or Node 18/20/22 with breaking changes

---

## Conclusion

The BMad Technical Writing Expansion Pack's **13 specialized agents** provide comprehensive coverage of the entire technical book authoring lifecycle. By understanding each agent's purpose, commands, and integration patterns, you can:

- **Plan effectively** using Core Planning Agents
- **Ensure quality** through Core Review Agents
- **Prepare for publication** with the Core Publishing Agent
- **Handle specialized content** with Specialist Agents
- **Update existing books** using the Brownfield Agent
- **Address complex scenarios** with Optional Agents

Choose agents based on your workflow needs, and combine them strategically to create high-quality technical books efficiently.

**Total agent count**: 13
**Word count**: ~5,100 words

---

**Related Documentation**:

- [Workflow Guide](workflow-guide.md) - Detailed workflows using these agents
- [Template Gallery](template-gallery.md) - Templates used by agent dependencies
- [Task Reference](task-reference.md) - Tasks executed by agent commands
- [User Guide](user-guide.md) - Conceptual overview of the framework
