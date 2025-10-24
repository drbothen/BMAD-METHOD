<!-- Powered by BMAD™ Core -->

# Plan Book Revision

---

task:
id: plan-book-revision
name: Plan Book Revision Strategy
description: Create strategic plan for updating existing technical book (2nd/3rd edition, version updates, chapter additions)
persona_default: book-analyst
inputs: - book_analysis_report (from analyze-existing-book.md) - revision_type (new edition, version update, chapter addition, feedback incorporation) - target_versions (if applicable)
steps: - Review book analysis report to understand current state - Define revision scope (full edition? specific chapters? code-only? text-only?) - Identify all technology version changes needed - Create chapter revision matrix (complexity, effort, priority for each chapter) - Assess impact on learning progression and flow - Plan code testing strategy across target versions - Define timeline with phases and milestones - Identify chapter dependencies and critical path - Set success criteria and quality gates - Assess risks and create mitigation plans - Use template revision-plan-tmpl.yaml with create-doc.md task - Run execute-checklist.md with revision-completeness-checklist.md - Generate comprehensive revision plan
output: manuscript/planning/{{book_title}}-revision-plan.md

---

## Purpose

This task transforms the book analysis into an actionable revision plan. It defines scope, priorities, timeline, and success criteria for updating an existing technical book. The revision plan guides all subsequent brownfield work.

## Prerequisites

Before starting this task:

- Book analysis report completed (from analyze-existing-book.md)
- Clear understanding of revision motivation (why update now?)
- Target technology versions identified (if version update)
- Publisher requirements or deadlines known (if applicable)
- Access to stakeholders for scope decisions

## Workflow Steps

### 1. Review Book Analysis Report

Thoroughly review the analysis report to understand:

- Current book structure and content
- Issues and gaps identified
- Technical currency assessment
- Recommendations provided
- Code inventory and version information

This analysis is your foundation for planning.

### 2. Define Revision Scope

Determine the type and extent of revision:

**Revision Type:**

- New edition (2nd, 3rd)? - Full book revision
- Technology version update? - Update code and related text
- Chapter additions? - New content integration
- Reviewer feedback incorporation? - Targeted fixes
- Publisher-requested changes? - Specific modifications

**Scope Level:**

- Full book revision (all chapters)
- Specific chapters only (which ones?)
- Code examples only (no text changes)
- Text updates only (no code changes)
- Mixed (some chapters full revision, others minor updates)

**Triggers:** Why now?

- New technology version released
- Publisher request for new edition
- Market demand or competition
- Technical debt accumulated
- Reviewer or reader feedback

**Goals:** What does success look like?

- Updated to latest technology versions
- All broken examples fixed
- New features demonstrated
- Improved clarity and accuracy
- Publisher approval secured

**Constraints:**

- Timeline (publisher deadline, market window)
- Budget (author time, technical review costs)
- Resources (access to testers, reviewers)

### 3. Identify Technology Version Changes

For each technology in the book, document:

- Current version in book (e.g., Python 3.9)
- Target version for revision (e.g., Python 3.12)
- Breaking changes between versions
- New features to incorporate
- Deprecated features to replace
- Migration effort estimate (low/medium/high)

Example:

- Python: 3.9 → 3.12 (Medium - add match/case, update deprecated methods)
- Django: 3.2 → 4.2 (High - significant async changes, new admin features)
- PostgreSQL: 13 → 15 (Low - mostly backward compatible, add new JSON features)

### 4. Create Chapter Revision Matrix

For each chapter, define revision needs:

| Chapter | Title        | Complexity | Effort | Priority  | Changes Needed                |
| ------- | ------------ | ---------- | ------ | --------- | ----------------------------- |
| 1       | Introduction | Low        | 2h     | Important | Update version refs           |
| 2       | Basic Syntax | High       | 8h     | Critical  | Add match/case (Python 3.10+) |
| 3       | Functions    | Medium     | 5h     | Important | Update type hints syntax      |
| ...     | ...          | ...        | ...    | ...       | ...                           |

**Complexity Levels:**

- **Low**: Minor text updates, version number changes, small corrections
- **Medium**: Code updates, new examples, moderate text revisions
- **High**: Significant rewrites, new sections, major code changes

**Effort Estimates:** Hours per chapter (be realistic)

**Priority Levels:**

- **Critical**: Must fix (broken code, security issues, major inaccuracies)
- **Important**: Should fix (outdated best practices, missing features)
- **Nice-to-have**: Optional improvements (polish, minor enhancements)

### 5. Assess Learning Flow Impact

Consider how revisions affect pedagogical progression:

- Does changing Chapter 3 affect Chapters 4-10 that build on it?
- If adding new content, where does it fit in the learning sequence?
- Will version changes alter the difficulty curve?
- Do prerequisite requirements change?
- Will the learning objectives still be met?

Consult learning-frameworks.md for pedagogical best practices.

### 6. Plan Code Testing Strategy

Define how you'll validate all code updates:

**Testing Approach:**

- Manual testing (run each example)
- Automated testing (unit tests, integration tests)
- CI/CD pipeline (automated validation on commits)

**Version Matrix:**

- Which versions to test? (Python 3.10, 3.11, 3.12? or just 3.12?)
- Multiple platforms? (Windows, macOS, Linux)
- Multiple environments? (development, production)

**Tool Requirements:**

- Testing frameworks (pytest, Jest, etc.)
- Linters (pylint, ESLint, etc.)
- Code formatters (black, prettier, etc.)

**Repository Updates:**

- Update code repository structure
- Add/update tests
- Update documentation (README, setup instructions)

**Regression Testing:**

- Test unchanged examples still work
- Verify backward compatibility where needed

### 7. Define Timeline and Milestones

Break revision into phases with realistic estimates:

**Example Timeline (14-week revision):**

**Phase 1: Analysis and Planning (Weeks 1-2)**

- Week 1: Complete book analysis
- Week 2: Finalize revision plan, set up testing environment

**Phase 2: Chapter Revisions (Weeks 3-10)**

- Weeks 3-4: Chapters 1-5 (Critical priority)
- Weeks 5-6: Chapters 6-10 (Critical priority)
- Weeks 7-8: Chapters 11-15 (Important priority)
- Weeks 9-10: Review, polish, and nice-to-haves

**Phase 3: Testing and QA (Weeks 11-12)**

- Week 11: Code testing across all target versions
- Week 12: Technical review and editorial review

**Phase 4: Finalization (Weeks 13-14)**

- Week 13: Incorporate feedback, final revisions
- Week 14: Final formatting, publisher submission

**Critical Path:** Which tasks block others?

- Must complete Python version update before testing
- Must finish technical review before editorial review
- Must have all chapters revised before final formatting

**Dependencies:** What must complete before next phase?

- Analysis must complete before revision starts
- Critical chapters must finish before important chapters
- All revisions must complete before QA phase

### 8. Set Success Criteria

Define what "done" means:

- [ ] All code examples tested on target versions
- [ ] All deprecated APIs replaced with current equivalents
- [ ] Technical review approved (no critical issues)
- [ ] Editorial review approved (clarity and consistency)
- [ ] All checklists passed (version-update-checklist.md, revision-completeness-checklist.md)
- [ ] Publisher requirements met
- [ ] Learning progression validated (no knowledge gaps)
- [ ] Cross-references updated and verified
- [ ] No broken examples
- [ ] Table of contents reflects changes
- [ ] New edition number documented

### 9. Assess Risks and Create Mitigation Plans

Identify potential problems and solutions:

**Technical Risks:**

- Risk: Breaking changes too extensive, examples can't be easily migrated
  - Mitigation: Incremental testing, provide migration examples, consider backward-compatible alternatives
- Risk: New version not stable yet
  - Mitigation: Target only LTS/stable releases, avoid beta versions
- Risk: Third-party libraries incompatible with new versions
  - Mitigation: Research compatibility early, plan alternative examples

**Scope Risks:**

- Risk: Revision scope creeps beyond original plan
  - Mitigation: Strict scope control, defer enhancements to future edition, track scope changes
- Risk: Underestimating effort for "simple" chapters
  - Mitigation: Add 20% buffer to estimates, track actual time

**Schedule Risks:**

- Risk: Testing takes longer than expected
  - Mitigation: Start testing early, test incrementally, run tests in parallel
- Risk: Publisher deadline pressure
  - Mitigation: Build buffer time into schedule, prioritize critical updates, communicate early if slipping

**Quality Risks:**

- Risk: Inconsistency between old and new content
  - Mitigation: Extract style guide early, editorial review, use existing-book-integration-checklist.md
- Risk: Breaking learning flow with changes
  - Mitigation: Review learning progression, test with beta readers, consult instructional designer

### 10. Generate Revision Plan

Use the create-doc.md task with revision-plan-tmpl.yaml template to create the structured revision plan document.

The plan should include all decisions and details from steps 1-9.

### 11. Validate Revision Plan

Run execute-checklist.md with revision-completeness-checklist.md to ensure:

- All aspects of revision are planned
- Timeline is realistic
- Dependencies are identified
- Risks are assessed
- Success criteria are clear

### 12. Review and Approve

Review the revision plan with stakeholders:

- Author: Is the timeline realistic? Are priorities correct?
- Publisher: Does this meet publication requirements?
- Technical reviewer: Are technical estimates accurate?
- Instructional designer: Will learning flow be maintained?

Get formal approval before starting revision work.

## Success Criteria

A completed revision plan should have:

- [ ] Clear revision scope and type defined
- [ ] All technology version changes documented
- [ ] Chapter revision matrix complete with priorities
- [ ] Learning flow impact assessed
- [ ] Code testing strategy defined
- [ ] Timeline with phases and milestones
- [ ] Critical path and dependencies identified
- [ ] Success criteria clearly stated
- [ ] Risks assessed with mitigation plans
- [ ] Revision plan document generated
- [ ] Stakeholder approval secured

## Common Pitfalls to Avoid

- **Underestimating effort**: Revisions often take longer than expected - add buffer
- **Ignoring learning flow**: Changes in early chapters affect later ones
- **No testing plan**: Can't verify quality without systematic testing
- **Vague success criteria**: Must define "done" explicitly
- **Skipping risk assessment**: Surprises derail timelines
- **No stakeholder buy-in**: Get approval before starting work

## Next Steps

After completing the revision plan:

1. Set up testing environment and code repository
2. Begin chapter revisions following priority order
3. Extract code patterns if needed (extract-code-patterns.md)
4. Execute book-edition-update-workflow.yaml for full coordination
5. Track progress against timeline and adjust as needed
