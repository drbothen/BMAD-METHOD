# Workflow Guide

## Introduction

The BMad Technical Writing Expansion Pack provides **15 specialized workflows** that orchestrate the entire technical book authoring lifecycle. Each workflow defines a complete process with agent sequences, quality gates, time estimates, and decision guidance.

This comprehensive guide documents all 15 workflows organized by category, with detailed information about:

- **Purpose** - What the workflow accomplishes
- **When to use** - Specific scenarios where this workflow is most effective
- **Inputs required** - Prerequisites and files needed to start
- **Outputs produced** - Deliverables created by the workflow
- **Agents involved** - Primary and supporting agents in sequence
- **Estimated time** - Typical duration from workflow YAML
- **Step-by-step breakdown** - Complete workflow sequence
- **Quality gates** - Checkpoints and validation criteria

### Workflow Categories

- **Planning (1)**: Book concept to approved outline
- **Development (6)**: Chapter creation, section-driven approach, tutorials, code examples
- **Review (2)**: Technical validation and incorporating feedback
- **Publishing (4)**: Publisher-specific formatting and submission
- **Brownfield (2)**: Updating existing books and adding chapters

---

## Planning Workflows

### Book Planning Workflow

**ID**: `book-planning-workflow`
**Type**: book-planning
**Version**: 1.0

#### Purpose

Complete book planning from concept to approved outline. Guides technical authors through proposal creation, outline design, learning path validation, editorial review, and publisher requirements verification. Ensures pedagogical soundness and publisher compliance before chapter development begins.

#### When to Use

- Planning a new technical book from scratch
- Pitching book proposal to publisher
- Need structured approach to outline creation
- Want to validate pedagogical design before writing
- Working with traditional publisher with specific requirements

#### When NOT to Use

- Book outline already approved (jump to chapter development)
- Self-publishing without strict format requirements
- Converting existing content to book (use revision workflow)

#### Inputs Required

- Book topic
- Target audience
- Publisher (optional)

#### Outputs Produced

- `book-proposal.md` - Comprehensive proposal with market analysis
- `book-outline.md` - Detailed pedagogical outline
- `learning-path-validation.md` - Prerequisite flow validation
- `book-outline-edited.md` - Editorially polished outline
- `book-outline-final.md` - Publisher-approved outline

#### Agents Involved (Sequence)

1. **book-publisher** - Drafts comprehensive book proposal
2. **instructional-designer** - Creates detailed pedagogical outline
3. **instructional-designer** - Validates learning progression
4. **technical-editor** - Reviews for clarity and consistency
5. **book-publisher** - Verifies publisher requirements

#### Estimated Time

- Draft proposal: 4-8 hours
- Design outline: 8-12 hours
- Validate learning path: 3-5 hours
- Editorial review: 3-5 hours
- Publisher format check: 2-3 hours
- **Total**: 20-33 hours for complete book planning

#### Step-by-Step Breakdown

1. **Draft Proposal** (`book-publisher`)
   - Creates `book-proposal.md` using `book-proposal-tmpl.yaml`
   - Includes: market analysis, competitive titles, target audience profile, unique value proposition, chapter list, author platform, timeline
   - Save to: `manuscript/planning/book-proposal.md`

2. **Design Outline** (`instructional-designer`)
   - Creates `book-outline.md` using `book-outline-tmpl.yaml`
   - Defines: learning progression, prerequisites per chapter, topics/subtopics, exercise strategy, difficulty curve
   - Ensures pedagogical soundness and logical skill building
   - Save to: `manuscript/planning/book-outline.md`

3. **Validate Learning Path** (`instructional-designer`)
   - Validates prerequisite flow ensures no knowledge gaps
   - Checks concepts build logically chapter by chapter
   - Verifies exercises progress from basic to advanced
   - Uses `learning-objectives-checklist.md` and `prerequisite-clarity-checklist.md`
   - Save to: `manuscript/planning/learning-path-validation.md`

4. **Editorial Review** (`technical-editor`)
   - Reviews outline for clarity, consistency, professional quality
   - Checks chapter titles are clear and compelling
   - Ensures terminology is consistent
   - Verifies structure follows publisher best practices
   - Save to: `manuscript/planning/book-outline-edited.md`

5. **Publisher Format Check** (`book-publisher`)
   - Verifies outline matches publisher chapter count guidelines
   - Checks technical depth appropriate for series/imprint
   - Ensures format follows publisher template
   - Confirms timeline is realistic
   - Uses publisher-specific checklist (PacktPub, O'Reilly, or Manning)
   - Save to: `manuscript/planning/book-outline-final.md`
   - **Status**: Ready for Chapter Development

#### Quality Gates

**Proposal Complete:**

- Market analysis included
- Target audience clearly defined
- Competitive titles identified
- Unique value proposition stated
- High-level chapter list provided
- Author platform described
- Realistic timeline included

**Outline Complete:**

- All chapters have clear titles
- Learning objectives defined for each chapter
- Prerequisites stated for each chapter
- Topics and subtopics outlined
- Exercise strategy defined
- Estimated page counts provided

**Learning Path Validated:**

- No knowledge gaps between chapters
- Difficulty curve is smooth
- Prerequisites are achievable
- Exercises progress appropriately
- Reader can succeed with stated background

**Editorial Complete:**

- Chapter titles are compelling
- No topic duplication
- Terminology consistent throughout
- Structure follows best practices

**Publisher Approved:**

- Chapter count matches guidelines
- Technical depth appropriate
- Format matches publisher template
- Timeline is realistic

---

## Development Workflows

### Chapter Development Workflow (v2.0 - Section-Driven)

**ID**: `chapter-development-workflow`
**Type**: chapter-writing
**Version**: 2.0

#### Purpose

Complete chapter creation from outline to publisher-ready manuscript. v2.0 orchestrates **section-driven development** (section-planning → section-development → chapter-assembly). Can also be used for traditional full-chapter writing. Emphasizes learning objectives, hands-on tutorials, tested code examples, and professional quality standards.

#### When to Use Section-Driven Approach

- Chapters 15+ pages (too large for single sitting)
- Want incremental progress tracking ("5 of 8 sections complete")
- Need parallel development (multiple sections in progress)
- Want to review work-in-progress before full chapter done
- Prefer story-driven iterative approach (BMad analog)

#### When to Use Traditional Approach

- Short chapters (<10-12 pages)
- Simple reference sections
- Author prefers writing full chapter at once
- Chapter already partially written

#### Inputs Required

- `book-outline.md` - Approved book outline

#### Outputs Produced (Section-Driven)

- `chapter-outline.md` - Detailed chapter outline
- `section-list.md` - List of all section plans
- `section-{n}-final.md` - Each completed section
- `chapter-integrated.md` - Merged chapter
- `chapter-final.md` - Publisher-ready chapter

#### Agents Involved (Section-Driven Sequence)

1. **tutorial-architect** - Creates chapter outline
2. **tutorial-architect** → **section-planning-workflow** - Plans 5-8 sections
3. **tutorial-architect** → **section-development-workflow** - Develops each section
4. **tutorial-architect** → **chapter-assembly-workflow** - Assembles chapter
5. **tutorial-architect** - Final validation

#### Estimated Time

**Section-Driven Approach:**

- Create outline: 2-4 hours
- Plan sections: 6-11 hours
- Develop sections: 33-84 hours (can be parallel)
- Assemble chapter: 13-24 hours
- **Total**: 54-123 hours per chapter (parallel development possible)

**Traditional Approach:**

- Create outline: 2-4 hours
- Develop code: 4-8 hours
- Write draft: 12-20 hours
- Technical review: 3-5 hours
- Revision: 4-8 hours
- Copy edit: 2-4 hours
- Finalization: 1-2 hours
- **Total**: 28-51 hours per chapter (sequential)

**Comparison**: Section-driven has higher total time but allows parallel work and incremental progress. Traditional is faster for solo authors on short chapters.

#### Step-by-Step Breakdown (Section-Driven)

1. **Create Chapter Outline** (`tutorial-architect`)
   - Defines learning objectives, prerequisites, main sections, exercises, code examples
   - Uses `create-chapter-outline.md` task
   - Save to: `manuscript/outlines/chapter-{n}-outline.md`

2. **Plan Sections** (`tutorial-architect` → **section-planning-workflow**)
   - Breaks chapter into 5-8 deliverable sections (2-5 pages each)
   - Creates section plans with clear acceptance criteria
   - Validates learning flow across sections
   - Save to: `manuscript/sections/chapter-{n}-section-list.md`

3. **Develop Sections** (`tutorial-architect` → **section-development-workflow**)
   - For each section: Code Curator develops code → Tutorial Architect writes section → Technical Reviewer reviews → Tutorial Architect finalizes
   - Sections can be developed in parallel if dependencies allow
   - Mark each section DONE when acceptance criteria met
   - Save to: `manuscript/sections/chapter-{n}/section-{i}-final.md`

4. **Assemble Chapter** (`tutorial-architect` → **chapter-assembly-workflow**)
   - Merges all completed sections
   - Improves transitions between sections
   - Validates learning flow (Instructional Designer)
   - Full technical review (Technical Reviewer)
   - Copy edit (Technical Editor)
   - Save to: `manuscript/chapters/chapter-{n}-final.md`

5. **Final Validation** (`tutorial-architect`)
   - Runs `chapter-completeness-checklist.md`
   - Verifies all learning objectives addressed
   - **Status**: Ready for Publication

#### Quality Gates

**Outline Complete:**

- Learning objectives defined (3-5)
- Prerequisites clearly stated
- All code examples identified
- Exercise plan created

**Sections Complete (each):**

- Section meets acceptance criteria
- Code tested and working
- Learning objectives addressed
- 2-5 pages length

**Chapter Integrated:**

- All sections merged
- Transitions smooth
- Learning flow validated
- Full technical review passed
- Copy editing complete

---

### Section Planning Workflow

**ID**: `section-planning-workflow`
**Type**: section-planning

#### Purpose

Breaks chapter outline into deliverable section units (BMad story analog). Creates section-level work items with acceptance criteria, enabling incremental chapter development. Each section is 2-5 pages with clear learning objectives and success criteria.

#### When to Use

- Breaking down chapter outline into work units
- Need incremental development approach
- Want to track section-by-section progress
- Planning parallel section development
- Chapter is 15+ pages (needs breakdown)

#### Estimated Time

- Analyze chapter: 1-2 hours
- Identify sections: 1-2 hours
- Create section plans: 2-4 hours
- Validate flow: 1-2 hours
- Finalize list: 1 hour
- **Total**: 6-11 hours per chapter

#### Step-by-Step Breakdown

1. **Analyze Chapter** (`tutorial-architect`) - Reviews structure, identifies breaking points
2. **Identify Sections** (`tutorial-architect`) - Breaks into 5-8 logical sections
3. **Create Section Plans** (`tutorial-architect`) - Detailed plan for each section using `section-plan-tmpl.yaml`
4. **Validate Flow** (`instructional-designer`) - Validates proper scaffolding, no learning gaps
5. **Finalize List** (`tutorial-architect`) - Creates final prioritized section list with dependencies

---

### Section Development Workflow

**ID**: `section-development-workflow`
**Type**: section-writing

#### Purpose

Complete development of one section (2-5 pages) - the "story" unit of book writing. Develops code examples, writes section content, and reviews for technical accuracy. Section is DONE when it meets acceptance criteria.

#### When to Use

- Developing one section from section plan
- Incremental chapter development approach
- Want focused work units with clear done criteria
- Tracking progress section by section

#### Estimated Time

- Develop code: 1-2 hours
- Test code: 30 min - 1 hour
- Write section: 2-4 hours
- Technical review: 30 min - 1 hour
- Revise section: 1-2 hours
- Verify criteria: 30 min
- **Total**: 5.5-10.5 hours per section

#### Step-by-Step Breakdown

1. **Develop Code** (`code-curator`) - Creates and tests all code examples for section
2. **Test Code** (`code-curator`) - Verifies correct output, edge cases, linting
3. **Write Section** (`tutorial-architect`) - Writes 2-5 page section with code inline
4. **Quick Review** (`technical-reviewer`) - Focused technical review of section
5. **Revise** (`tutorial-architect`) - Incorporates review feedback
6. **Finalize** (`tutorial-architect`) - Verifies acceptance criteria, marks DONE

---

### Chapter Assembly Workflow

**ID**: `chapter-assembly-workflow`
**Type**: chapter-integration

#### Purpose

Integrates all completed sections into cohesive chapter (BMad Sprint Review analog). Merges sections, improves transitions, validates learning flow, performs full technical review, and finalizes chapter for publication.

#### When to Use

- All chapter sections marked DONE
- Using section-driven development approach
- Ready to integrate sections into cohesive chapter
- Preparing chapter for publication

#### Estimated Time

- Merge sections: 1-2 hours
- Improve transitions: 2-3 hours
- Validate learning flow: 1-2 hours
- Technical review: 3-5 hours
- Revise chapter: 3-6 hours
- Copy edit: 2-4 hours
- Finalize: 1-2 hours
- **Total**: 13-24 hours per chapter

#### Step-by-Step Breakdown

1. **Merge Sections** (`tutorial-architect`) - Integrates all sections into single file
2. **Improve Transitions** (`tutorial-architect`) - Adds bridging paragraphs, cross-references
3. **Validate Learning Flow** (`instructional-designer`) - Checks concept progression
4. **Full Technical Review** (`technical-reviewer`) - Comprehensive chapter review
5. **Revise** (`tutorial-architect`) - Addresses all review feedback
6. **Copy Edit** (`technical-editor`) - Professional editorial polish
7. **Finalize** (`tutorial-architect`) - Runs completeness checklist, approves edits

---

### Tutorial Creation Workflow

**ID**: `tutorial-creation-workflow`
**Type**: tutorial-development

#### Purpose

Creates effective step-by-step tutorials with tested code and clear instructions. Emphasizes learning objectives, progressive difficulty, and student success.

#### When to Use

- Creating hands-on coding tutorials
- Building step-by-step technical guides
- Developing workshop materials
- Interactive learning experiences

#### Estimated Time

- Design plan: 1-2 hours
- Create structure: 2-3 hours
- Develop code: 3-6 hours
- Write tutorial: 4-8 hours
- Test tutorial: 1-2 hours
- Revisions: 2-4 hours
- Validation: 1-2 hours
- Finalization: 30 min - 1 hour
- **Total**: 14-28 hours per tutorial

#### Step-by-Step Breakdown

1. **Design Learning Path** (`instructional-designer`) - Defines objective, audience, prerequisites
2. **Create Structure** (`tutorial-architect`) - 8-15 step progression
3. **Develop Code** (`code-curator`) - Creates starter code, complete code, tests
4. **Write Tutorial** (`tutorial-architect`) - Complete tutorial with troubleshooting
5. **Test End-to-End** (`code-curator`) - Tests in fresh environment
6. **Revise** (`tutorial-architect`) - Incorporates testing feedback
7. **Validate** (`instructional-designer`) - Checks pedagogical standards
8. **Finalize** (`tutorial-architect`) - Ready for students

---

### Code Example Workflow

**ID**: `code-example-workflow`
**Type**: code-development

#### Purpose

Complete code example development from initial code to tested, secure, documented example. Ensures all code examples are production-quality, secure, and well-documented.

#### When to Use

- Creating code examples for technical books or tutorials
- Developing sample applications for documentation
- Need production-quality, tested code examples
- Security and quality standards must be met

#### Estimated Time

- Write code: 1-4 hours
- Test code: 1-2 hours
- Verify quality: 30 min - 1 hour
- Security check: 30 min - 1 hour
- Document example: 1-2 hours
- **Total**: 4-10 hours per code example

#### Step-by-Step Breakdown

1. **Write Code** (`code-curator`) - Clean, idiomatic code with error handling
2. **Test** (`code-curator`) - Tests on target platforms and versions
3. **Verify Quality** (`code-curator`) - Checks style guide, best practices
4. **Security Review** (`code-curator`) - Scans for vulnerabilities
5. **Document** (`code-curator`) - Comprehensive README with troubleshooting

---

## Review Workflows

### Technical Review Workflow

**ID**: `technical-review-workflow`
**Type**: technical-review

#### Purpose

Comprehensive technical validation of chapter content. Verifies technical accuracy, code correctness, security best practices, and current information.

#### When to Use

- Validating technical accuracy before publication
- Ensuring code examples are correct and secure
- Checking for outdated or deprecated information
- Need expert subject matter review

#### Estimated Time

- **Typical**: 3-5 hours per chapter (full review)
- **Focused**: 30 min - 1 hour per section (section review)

#### Agents Involved

- **technical-reviewer** (primary)
- **code-curator** (supporting for code validation)

---

### Incorporate Review Feedback Workflow

**ID**: `incorporate-review-feedback-workflow`
**Type**: revision

#### Purpose

Systematically incorporates feedback from technical reviewers, beta readers, or publishers. Triages feedback, prioritizes changes, implements revisions, and validates corrections.

#### When to Use

- Received feedback from technical review
- Beta reader feedback needs incorporation
- Publisher requests revisions
- Systematically addressing review comments

#### Estimated Time

- Varies based on feedback volume
- **Typical**: 4-12 hours per chapter depending on revision scope

---

## Publishing Workflows

### PacktPub Submission Workflow

**ID**: `packtpub-submission-workflow`
**Type**: publisher-submission

#### Purpose

Prepares and formats manuscript for PacktPub submission. Applies PacktPub-specific formatting, style guidelines, and submission requirements.

#### When to Use

- Submitting book to PacktPub
- Need PacktPub-specific formatting
- Preparing chapter deliverables for PacktPub

#### Agents Involved

1. **book-publisher** - Applies PacktPub formatting
2. **technical-editor** - Verifies PacktPub style compliance
3. **book-publisher** - Packages manuscript for submission

---

### O'Reilly Submission Workflow

**ID**: `oreilly-submission-workflow`
**Type**: publisher-submission

#### Purpose

Prepares and formats manuscript for O'Reilly Media submission. Applies O'Reilly-specific formatting (AsciiDoc, Chicago style), Atlas platform requirements, and submission guidelines.

#### When to Use

- Submitting book to O'Reilly Media
- Need AsciiDoc conversion
- Preparing for Atlas platform

#### Agents Involved

1. **book-publisher** - Converts to AsciiDoc, applies Chicago style
2. **technical-editor** - Verifies O'Reilly format compliance
3. **book-publisher** - Packages for Atlas submission

---

### Manning MEAP Workflow

**ID**: `manning-meap-workflow`
**Type**: publisher-submission

#### Purpose

Prepares chapters for Manning Early Access Program (MEAP). Formats chapters for incremental release to early access readers.

#### When to Use

- Submitting chapters to Manning MEAP
- Incremental chapter releases
- Need Manning-specific formatting

#### Agents Involved

1. **book-publisher** - Applies Manning MEAP formatting
2. **technical-editor** - Verifies Manning style
3. **book-publisher** - Prepares chapter for MEAP release

---

### Self-Publishing Workflow

**ID**: `self-publishing-workflow`
**Type**: self-publishing

#### Purpose

Prepares manuscript for self-publishing platforms (Leanpub, Gumroad, Amazon KDP, etc.). Handles formatting, cover preparation, metadata, and platform-specific requirements.

#### When to Use

- Self-publishing book
- Need platform-specific formatting (Leanpub Markdown, KDP DOCX, etc.)
- Preparing for multiple self-publishing platforms

#### Agents Involved

1. **book-publisher** - Formats for target platform
2. **technical-editor** - Final quality check
3. **book-publisher** - Prepares supplementary materials (cover, metadata)

---

## Brownfield Workflows

### Book Edition Update Workflow

**ID**: `book-edition-update-workflow`
**Type**: brownfield-revision

#### Purpose

Updates existing book for 2nd/3rd edition. Handles technology version migration, content updates, and consistency maintenance with existing style.

#### When to Use

- Planning 2nd or 3rd edition of existing book
- Technology version has changed (e.g., Python 3.10 → 3.12)
- Need to update outdated content
- Want to maintain consistency with existing book style

#### Estimated Time

- Varies significantly based on scope of changes
- **Analysis**: 8-16 hours
- **Planning**: 6-12 hours
- **Implementation**: Depends on changes (can be substantial)

#### Agents Involved

1. **book-analyst** - Analyzes existing book, extracts patterns
2. **book-analyst** - Assesses version impact
3. **version-manager** - Tests code on new versions (if applicable)
4. **book-analyst** - Plans surgical revisions
5. Various agents - Implements revisions based on plan
6. **technical-reviewer** - Validates updates
7. **technical-editor** - Ensures consistency with existing style

---

### Add Chapter to Existing Book Workflow

**ID**: `add-chapter-to-existing-book-workflow`
**Type**: brownfield-addition

#### Purpose

Adds new chapter to existing published book. Ensures new chapter matches existing voice, tone, code style, and pedagogical approach.

#### When to Use

- Adding new chapter to existing book
- Expanding book with additional content
- Need consistency with existing chapters
- Want new chapter to feel integrated, not appended

#### Agents Involved

1. **book-analyst** - Extracts style patterns from existing chapters
2. **instructional-designer** - Plans new chapter to fit learning progression
3. Standard chapter development agents - Creates chapter following extracted patterns
4. **technical-editor** - Verifies consistency with existing book style
5. **book-publisher** - Integrates new chapter into book structure

---

## Workflow Comparison Table

| Workflow                          | Category    | Time Estimate | Primary Agents                                                                   | When to Use                                         |
| --------------------------------- | ----------- | ------------- | -------------------------------------------------------------------------------- | --------------------------------------------------- |
| Book Planning                     | Planning    | 20-33 hrs     | book-publisher, instructional-designer, technical-editor                         | New book concept to approved outline                |
| Chapter Development (Section)     | Development | 54-123 hrs    | tutorial-architect, code-curator, technical-reviewer, technical-editor           | Large chapters (15+ pages), incremental development |
| Chapter Development (Traditional) | Development | 28-51 hrs     | tutorial-architect, code-curator, technical-reviewer, technical-editor           | Short chapters (<12 pages), full-chapter writing    |
| Section Planning                  | Development | 6-11 hrs      | tutorial-architect, instructional-designer                                       | Breaking chapter into sections                      |
| Section Development               | Development | 5.5-10.5 hrs  | code-curator, tutorial-architect, technical-reviewer                             | Developing one section                              |
| Chapter Assembly                  | Development | 13-24 hrs     | tutorial-architect, instructional-designer, technical-reviewer, technical-editor | Merging sections into chapter                       |
| Tutorial Creation                 | Development | 14-28 hrs     | instructional-designer, tutorial-architect, code-curator                         | Standalone tutorials                                |
| Code Example                      | Development | 4-10 hrs      | code-curator                                                                     | Individual code examples                            |
| Technical Review                  | Review      | 3-5 hrs       | technical-reviewer                                                               | Validating technical accuracy                       |
| Incorporate Feedback              | Review      | 4-12 hrs      | tutorial-architect, technical-reviewer                                           | Addressing review comments                          |
| PacktPub Submission               | Publishing  | Varies        | book-publisher, technical-editor                                                 | PacktPub formatting                                 |
| O'Reilly Submission               | Publishing  | Varies        | book-publisher, technical-editor                                                 | O'Reilly/AsciiDoc formatting                        |
| Manning MEAP                      | Publishing  | Varies        | book-publisher, technical-editor                                                 | Manning early access                                |
| Self-Publishing                   | Publishing  | Varies        | book-publisher, technical-editor                                                 | Self-pub platforms                                  |
| Edition Update                    | Brownfield  | Varies        | book-analyst, version-manager                                                    | 2nd/3rd editions                                    |
| Add Chapter                       | Brownfield  | Varies        | book-analyst, standard agents                                                    | Adding to existing book                             |

---

## Workflow Selection Decision Tree

**I want to...**

### Start a new book

→ Use **Book Planning Workflow** (20-33 hrs) to create approved outline
→ Then proceed to chapter development

### Write a chapter

→ **Is it 15+ pages?** → Use **Chapter Development (Section-Driven)** for incremental progress
→ **Is it <12 pages?** → Use **Chapter Development (Traditional)** for faster completion
→ **Section-driven flow**: Section Planning → Section Development (×N) → Chapter Assembly

### Create a tutorial

→ Use **Tutorial Creation Workflow** (14-28 hrs) for standalone tutorial
→ OR embed tutorial in chapter using Tutorial Architect

### Develop code examples

→ Use **Code Example Workflow** (4-10 hrs per example) for tested, secure code

### Review content

→ Use **Technical Review Workflow** for accuracy validation
→ Use **Incorporate Feedback Workflow** to systematically address comments

### Prepare for publication

→ **PacktPub?** → Use **PacktPub Submission Workflow**
→ **O'Reilly?** → Use **O'Reilly Submission Workflow**
→ **Manning MEAP?** → Use **Manning MEAP Workflow**
→ **Self-publishing?** → Use **Self-Publishing Workflow**

### Update existing book

→ **2nd/3rd edition?** → Use **Book Edition Update Workflow**
→ **Add new chapter?** → Use **Add Chapter to Existing Book Workflow**

---

## Common Workflow Sequences

### Greenfield Book (New Book, Section-Driven)

1. **Book Planning Workflow** (20-33 hrs) → Approved outline
2. For each chapter:
   - **Section Planning Workflow** (6-11 hrs) → Section list
   - **Section Development Workflow** (×6-8 sections, parallel) → Completed sections
   - **Chapter Assembly Workflow** (13-24 hrs) → Final chapter
3. **Technical Review Workflow** (per chapter or book)
4. **Publisher Submission Workflow** → Formatted manuscript

**Total per chapter**: ~73-158 hrs (section-driven)

### Greenfield Book (New Book, Traditional)

1. **Book Planning Workflow** (20-33 hrs) → Approved outline
2. For each chapter:
   - **Chapter Development (Traditional)** (28-51 hrs) → Final chapter
3. **Technical Review Workflow** (per chapter)
4. **Publisher Submission Workflow** → Formatted manuscript

**Total per chapter**: ~28-51 hrs (traditional)

### Brownfield Book (2nd Edition Update)

1. **Book Edition Update Workflow (Analysis)** (8-16 hrs) → Patterns extracted, impact assessed
2. **Book Edition Update Workflow (Planning)** (6-12 hrs) → Revision plan
3. For affected chapters:
   - **Incorporate Feedback Workflow** OR **Chapter Development** (depending on scope)
   - **Technical Review Workflow** → Validate updates
4. **Publisher Submission Workflow** → Updated manuscript

### Tutorial-Focused Book

1. **Book Planning Workflow** → Outline
2. For each chapter:
   - **Tutorial Creation Workflow** (×multiple tutorials per chapter)
   - **Chapter Assembly** → Integrate tutorials into chapter
3. **Technical Review Workflow**
4. **Publisher Submission Workflow**

---

## Best Practices

### Workflow Selection

- **Use section-driven** for chapters 15+ pages, parallel development, incremental progress tracking
- **Use traditional** for short chapters, solo authors, simple reference content
- **Use brownfield workflows** when updating existing content (maintain consistency)
- **Start with planning** - never skip book planning workflow for new books

### Time Management

- Section-driven has higher total time but enables parallel work
- Traditional is faster for solo authors on short chapters
- Time estimates include quality gates - don't skip them
- Buffer time for revisions (feedback always reveals issues)

### Quality Gates

- Every workflow has quality gates - they prevent rework
- Address critical issues before proceeding (cheaper to fix early)
- Run checklists at specified points (they catch common errors)
- Technical review before editorial polish (preserve accuracy)

### Agent Coordination

- Follow workflow sequence - agents depend on prior outputs
- Save outputs to specified locations (other agents need them)
- Use handoff prompts to communicate context between agents
- Parallel development possible in section-driven (check dependencies)

### Iteration

- Workflows are iterative - expect revision cycles
- Section review catches issues early (before full chapter assembly)
- Beta readers provide valuable feedback - use incorporate-feedback workflow
- Publishers may request changes - brownfield workflows handle this

---

## Conclusion

The BMad Technical Writing Expansion Pack's **15 specialized workflows** orchestrate the complete book authoring lifecycle. By understanding each workflow's purpose, inputs, outputs, and time estimates, you can:

- **Plan effectively** using structured workflows
- **Choose the right approach** (section-driven vs traditional)
- **Track progress** with clear milestones
- **Maintain quality** through defined quality gates
- **Coordinate agents** in optimal sequences
- **Handle revisions** systematically

**Key Innovation**: The **section-driven approach** (v2.0) brings story-driven iterative development to technical book writing, enabling incremental progress, parallel development, and earlier feedback.

**Total workflow count**: 15
**Word count**: ~2,850 words

---

**Related Documentation**:

- [Agent Reference Guide](agent-reference.md) - Detailed agent capabilities
- [Template Gallery](template-gallery.md) - Templates used in workflows
- [Task Reference](task-reference.md) - Tasks executed by workflows
- [User Guide](user-guide.md) - Conceptual overview
- [Process Flows](process-flows.md) - Visual Mermaid diagrams for all workflows
