# Expansion Pack Orphaned Items Analysis Workflow

**Purpose:** Developer workflow for auditing expansion packs to identify orphaned tasks and templates
**Audience:** Expansion pack developers, maintainers, quality assurance
**Version:** 1.0
**Last Updated:** 2025-10-25

---

## Overview

This workflow enables you to analyze any BMAD expansion pack to identify **orphaned items**—tasks and templates that exist but aren't connected to any agents, making them difficult for users to discover and use.

### What Are Orphaned Items?

- **Orphaned Tasks**: Tasks that are NOT referenced in any agent's `dependencies.tasks` section
- **Orphaned Templates**: Templates that are NOT referenced in any agent's `dependencies.templates` OR any task
- **Indirect Orphans**: Templates only referenced by orphaned tasks

### Why This Matters

Orphaned items represent:

- 🚫 **Broken Discoverability**: Users can't find functionality through agents
- 📉 **Reduced Value**: Well-designed features go unused
- 😕 **Poor UX**: Fragmented, incomplete workflows
- ⚠️ **Technical Debt**: Dead code or missing connections

---

## When to Run This Analysis

### ✅ **DO Run Analysis:**

- Before releasing a new expansion pack version
- After adding multiple new tasks or templates
- When users report difficulty discovering functionality
- As part of expansion pack quality assurance process
- During expansion pack refactoring or reorganization
- Quarterly health checks for mature expansion packs
- Before submitting expansion pack PR

### ❌ **DON'T Run Analysis:**

- During active feature development (wait until feature is complete)
- When expansion pack is still in initial scaffolding phase
- If you don't have time to act on findings

---

## Prerequisites

Before starting:

- ✅ Expansion pack follows BMAD structure (`agents/`, `tasks/`, `templates/` directories)
- ✅ All agent files use standard BMAD agent pattern with YAML dependencies block
- ✅ You have access to Claude Code or similar IDE with Task tool support
- ✅ You can commit the analysis report to version control

---

## Workflow Steps

### Step 1: Prepare for Analysis (5 minutes)

**Identify Your Target:**

```bash
# Example expansion pack location
EXPANSION_PACK="/Users/you/Dev/BMAD-METHOD/expansion-packs/bmad-technical-writing"

# Output report location
REPORT_PATH="$EXPANSION_PACK/docs/orphaned-items-analysis.md"
```

**Document Context:**

- Expansion pack name: **\*\*\*\***\_**\*\*\*\***
- Current version: **\*\*\*\***\_**\*\*\*\***
- Analysis date: **\*\*\*\***\_**\*\*\*\***
- Analyst: **\*\*\*\***\_**\*\*\*\***

### Step 2: Execute Automated Analysis (5-10 minutes)

**Using Claude Code or AI with Task Tool (RECOMMENDED):**

Activate an agent (like the analyst or PO agent) and provide this prompt:

```
Analyze the <expansion-pack-name> expansion pack to identify orphaned tasks and templates.

Directory: <absolute-path-to-expansion-pack>

I need you to:

1. **Get all files:**
   - All agent files in agents/
   - All task files in tasks/
   - All template files in templates/

2. **Read all agent files** and extract:
   - What tasks each agent references in their dependencies.tasks section
   - What templates each agent references in their dependencies.templates section

3. **Read all task files** and extract:
   - What templates each task references (look for template names in content)

4. **Create a comprehensive report showing:**

   A. **Orphaned Tasks** - Tasks that are NOT referenced by any agent
      - List task filename
      - Brief description of what the task does (from the task file)
      - Whether it references any templates
      - Which agent(s) should logically reference this task

   B. **Orphaned Templates** - Templates that are NOT referenced by any agent OR any task
      - List template filename
      - Brief description of what the template does
      - Potential uses or recommendations

   C. **Connected Items** - Summary of which tasks/templates ARE connected
      - Agent → Tasks mapping
      - Agent → Templates mapping
      - Task → Template mapping

   D. **Health Metrics** - Calculate and report:
      - Total agents, tasks, templates
      - Percentage of orphaned tasks
      - Percentage of orphaned templates
      - Overall health score

5. **Return the complete analysis** with all findings clearly organized.

Be thorough - read all files to ensure accuracy. Focus only on the expansion pack directory, not core BMAD files.
```

**Expected Output:** Complete analysis with all orphaned items identified

**Alternative: Manual Analysis (1-2 hours)**

If automated tools are unavailable, see Appendix A for manual process.

### Step 3: Analyze and Categorize Findings (15-30 minutes)

Review the analysis output and categorize orphaned items by severity:

#### Severity Classification

**🔴 CRITICAL** (Fix Immediately)

- Core functionality tasks with multiple template references
- Major workflow gaps (e.g., "write chapter" missing from "tutorial architect")
- Agent name implies functionality that's orphaned (e.g., "screenshot-specialist" doesn't list "take-screenshots")

**🟠 HIGH** (Fix Soon)

- Important tasks with clear parent agents
- Tasks that complete logical workflows
- Templates only referenced by orphaned tasks

**🟡 MEDIUM** (Fix Later)

- Useful but non-essential tasks
- Tasks that could fit multiple agents
- Minor workflow enhancements

**⚪ LOW** (Optional)

- Edge case tasks
- Rarely used functionality
- Unclear which agent should own the task

#### For Each Orphaned Item, Note:

1. **Severity**: Critical / High / Medium / Low
2. **Parent Agent**: Which agent should reference it?
3. **Template Status**: Connected, orphaned, or indirect orphan?
4. **User Impact**: What workflow is broken/hidden?
5. **Decision**: Connect, remove, or defer?

### Step 4: Calculate Health Score (5 minutes)

Use this formula to assess expansion pack health:

```
Health Score Components:
- Agent Coverage: (Agents with dependencies / Total agents) × 100%
- Task-Agent Coverage: (Connected tasks / Total tasks) × 100%
- Template-Agent Coverage: (Connected templates / Total templates) × 100%
- Orphan Rate (inverse): 100% - (Orphaned items / Total items) × 100%

Overall Health Score: Average of all components

Health Ratings:
- 90-100%: ✅ Excellent
- 75-89%:  ✓ Good
- 60-74%:  ⚠ Needs Attention
- Below 60%: ❌ Critical Issues
```

**Example:**

```
Expansion Pack: bmad-technical-writing
- Agents: 13 (all have dependencies) = 100%
- Task-Agent Coverage: 27/48 = 56%
- Template-Agent Coverage: 16/18 = 89%
- Orphan Rate: 100% - (23/79 × 100%) = 71%

Overall Health Score: (100 + 56 + 89 + 71) / 4 = 79% (Good, but needs improvement)
```

### Step 5: Create Remediation Plan (20-30 minutes)

Organize findings into a prioritized action plan:

#### Priority 1: Immediate Actions (Do This Week)

List CRITICAL orphaned items:

- [ ] Connect `write-chapter-draft` to `tutorial-architect` (4 templates!)
- [ ] Connect `take-screenshots` to `screenshot-specialist`
- [ ] Connect `verify-accuracy` to `technical-reviewer`

**Estimated Effort:** **\_** hours

#### Priority 2: High Priority (Do This Sprint)

List HIGH severity orphaned items:

- [ ] Connect `validate-learning-flow` to `learning-path-designer`
- [ ] Connect `package-for-publisher` to `book-publisher`
- [ ] etc.

**Estimated Effort:** **\_** hours

#### Priority 3: Medium Priority (Do This Quarter)

List MEDIUM severity orphaned items:

- [ ] Connect `create-solutions` to `exercise-creator`
- [ ] etc.

**Estimated Effort:** **\_** hours

#### Priority 4: Low Priority (Backlog)

List LOW severity orphaned items OR items to remove:

- [ ] Review `glossary-entry-tmpl` - keep or remove?
- [ ] etc.

**Estimated Effort:** **\_** hours

### Step 6: Generate Analysis Report (30-45 minutes)

Create a comprehensive report documenting all findings.

**Report Template Structure:**

```markdown
# [EXPANSION-PACK-NAME]: Orphaned Items Analysis

**Analysis Date:** YYYY-MM-DD
**Expansion Pack:** expansion-pack-name
**Version:** X.Y.Z
**Location:** /path/to/expansion-pack
**Analyst:** [Your Name]

---

## Executive Summary

The expansion pack contains:

- **X Agents** (Y with dependencies)
- **Z Tasks** (N orphaned - W%)
- **M Templates** (P orphaned - Q%)

**Key Finding:** [1-2 sentence summary]

**Health Score:** XX% - [Excellent/Good/Needs Attention/Critical]

### Health Metrics

| Metric                  | Score | Status     |
| ----------------------- | ----- | ---------- |
| Agent Coverage          | 100%  | ✓ Good     |
| Task-Agent Coverage     | 56%   | ✗ Poor     |
| Template-Agent Coverage | 89%   | ✓ Good     |
| Orphaned Tasks          | 44%   | ✗ CRITICAL |
| Orphaned Templates      | 11%   | Moderate   |

---

## Table of Contents

1. [Orphaned Tasks](#orphaned-tasks)
2. [Orphaned Templates](#orphaned-templates)
3. [Connected Items Summary](#connected-items-summary)
4. [Key Issues & Recommendations](#recommendations)
5. [Priority Action Items](#priority-actions)
6. [Conclusion](#conclusion)

---

## Orphaned Tasks

[For each orphaned task, document:]

### Task Name: filename.md

- **Description:** [What the task does]
- **Template References:** [Templates it uses]
- **Should Be Referenced By:** [Logical parent agent(s)]
- **Severity:** Critical/High/Medium/Low
- **User Impact:** [What workflow is broken]
- **Recommendation:** [Connect to agent X / Remove / Defer]

---

## Orphaned Templates

[For each orphaned template, document:]

### Template Name: filename.yaml

- **Status:** Completely unused / Only referenced by orphaned tasks
- **Potential Use:** [How it could be used]
- **Recommendation:** Keep and connect / Remove

---

## Connected Items Summary

### Agent → Task Mapping

[For each agent, list connected tasks and identify gaps:]

**agent-name**

- Connected Tasks: task1, task2, task3
- Missing Tasks: task4, task5
- Status: ✓ Complete / ✗ Gaps identified

### Agent → Template Mapping

[Table showing which agents reference which templates]

### Task → Template Mapping

[Table showing which tasks reference which templates]

---

## Key Issues & Recommendations

### Critical Issues

1. [Issue description and impact]
2. [Issue description and impact]

### Recommendations

#### Short-term Fixes (Quick Wins)

- [Specific agent updates with YAML examples]

#### Medium-term Improvements

- [Process improvements]

#### Long-term Strategy

- [Structural enhancements]

---

## Priority Action Items

### Immediate (This Week)

1. [Action with effort estimate]
2. [Action with effort estimate]

### High Priority (This Sprint)

1. [Action with effort estimate]
2. [Action with effort estimate]

### Medium Priority (This Quarter)

1. [Action with effort estimate]

### Low Priority (Backlog)

1. [Action with effort estimate]

**Total Estimated Remediation Effort:** XX-YY hours

---

## Conclusion

[Summary of findings and expected outcome after remediation]

**Expected Health Score After Remediation:** XX% → YY%

---

**Next Review:** [Date for follow-up analysis]
```

**Save Report:**

- Location: `expansion-packs/<name>/docs/orphaned-items-analysis.md`
- Commit to version control with descriptive message
- Tag with analysis date

### Step 7: Communicate Findings (15-30 minutes)

Share results with relevant stakeholders:

**For Team Review:**

- Present executive summary (health score, key findings)
- Highlight top 3-5 priority issues
- Show estimated remediation effort
- Propose story breakdown if applicable
- Get buy-in for remediation timeline

**Discussion Questions:**

- Which orphaned items are highest priority?
- Should any items be removed instead of connected?
- What's the remediation timeline?
- Who will create/execute remediation stories?

### Step 8: Create Remediation Stories (Optional, 30-60 min per story)

If orphaned items will be fixed through development stories:

**Story Template:**

```markdown
# Story X.Y: Connect [Category] Tasks to [Agent Name]

## Status

Draft

## Story

**As a** user of the [expansion-pack] expansion pack,
**I want** [agent-name] to reference [task-category] tasks,
**So that** I can discover and execute [workflows] through the agent interface.

## Acceptance Criteria

1. Agent file updated: `agents/[agent-name].md`
2. Tasks added to `dependencies.tasks` section: [list]
3. Templates added to `dependencies.templates` section (if applicable): [list]
4. Agent commands updated to reference new tasks (if applicable)
5. Changes validated - agent activation works and shows new commands
6. Documentation updated (if needed)
7. No orphaned items introduced

## Tasks / Subtasks

- [ ] **Update agent dependencies** (AC: 1, 2, 3)
  - [ ] Add tasks to dependencies.tasks: [list]
  - [ ] Add templates to dependencies.templates: [list]
  - [ ] Verify YAML formatting

- [ ] **Update agent commands** (AC: 4) (if applicable)
  - [ ] Add command: `*task-name` - description
  - [ ] Update help output

- [ ] **Test and validate** (AC: 5, 6, 7)
  - [ ] Test agent activation via slash command
  - [ ] Verify help command shows new tasks
  - [ ] Test new command execution
  - [ ] Run orphan analysis to confirm no new orphans
  - [ ] Update documentation if needed

## Dev Notes

### Context

This story connects orphaned tasks identified in orphaned-items-analysis.md
(version [date]) to their logical parent agent.

### Existing System Integration

**Agent File:** `expansion-packs/[name]/agents/[agent-name].md`

**Tasks Being Connected:**

- [task-name].md - [brief description]
- [task-name].md - [brief description]

**Templates Being Connected (if any):**

- [template-name].yaml - [brief description]

### Testing

- Activate agent and verify greeting
- Run `*help` and confirm new commands appear
- Execute new commands and verify they work
- Re-run orphan analysis to confirm fixes

## Change Log

| Date   | Version | Description                        | Author |
| ------ | ------- | ---------------------------------- | ------ |
| [date] | 1.0     | Initial story from orphan analysis | [name] |
```

---

## Success Criteria

The orphaned items analysis is successful when:

1. ✅ **Complete Inventory**: All agents, tasks, and templates catalogued
2. ✅ **Accurate Identification**: Orphaned items correctly identified with no false positives
3. ✅ **Impact Assessment**: Severity and priority assigned to each orphaned item
4. ✅ **Actionable Plan**: Clear remediation plan with effort estimates
5. ✅ **Comprehensive Report**: Document created following template structure
6. ✅ **Stakeholder Buy-In**: Team understands issues and agrees on priorities
7. ✅ **Next Steps Defined**: Stories created or remediation timeline established

---

## Metrics to Track

### Before Analysis

- Total agents: \_\_\_\_
- Total tasks: \_\_\_\_
- Total templates: \_\_\_\_

### Analysis Results

- Orphaned tasks: \_**_ (_**%)
- Orphaned templates: \_**_ (_**%)
- Health score: \_\_\_\_%

### After Remediation

- Orphaned tasks remaining: \_**_ (_**%)
- Orphaned templates remaining: \_**_ (_**%)
- Health score improvement: \_**\_% → \_\_**%
- User experience improvement: [qualitative]

---

## Tips & Best Practices

### For Effective Analysis

1. **✅ Use Automation**: Prefer AI-assisted analysis over manual spreadsheets
   - Task tool with Explore agent: 10 minutes vs 1-2 hours manual
   - More thorough, less error-prone
   - Consistent reporting

2. **✅ Read Agent Files Completely**: Don't just grep for dependencies
   - Understand agent purpose and intended workflows
   - Consider what tasks/templates logically belong

3. **✅ Check Task Content**: Tasks may reference templates without explicit dependency
   - Search for `.yaml`, `tmpl`, template names in task files
   - Document template references found in task content

4. **✅ Think User Perspective**: Prioritize based on discoverability
   - What workflows are users trying to accomplish?
   - Which orphans break critical paths?

5. **✅ Prioritize Ruthlessly**: Not all orphans need immediate remediation
   - Focus on critical workflow gaps first
   - Defer edge cases and experiments
   - Consider removing truly unused items

6. **✅ Document Assumptions**: Note unclear cases
   - If multiple agents could own a task, note why you chose one
   - Document items marked "low priority" with reasoning

### Common Patterns & Red Flags

#### 🚩 **Agent Name Mismatch**

- **Pattern**: Agent is named `screenshot-specialist` but doesn't list `take-screenshots` task
- **Severity**: HIGH - Violates user expectations
- **Action**: Connect immediately

#### 🚩 **Workflow Gaps**

- **Pattern**: Agent has "create outline" but not "write draft" tasks
- **Severity**: MEDIUM - Incomplete logical workflow
- **Action**: Connect to complete workflow

#### 🚩 **Task-Template Misalignment**

- **Pattern**: Task has template, but task is orphaned from agents
- **Severity**: Varies - Template is discoverable but workflow isn't
- **Action**: Connect both task AND template to agent

#### 🚩 **Template-Only Connection**

- **Pattern**: Template is connected to agent, but task using it is orphaned
- **Severity**: MEDIUM - Template discoverable but workflow hidden
- **Action**: Connect the task

#### ⚪ **Truly Unused Items**

- **Pattern**: Template/task created but never implemented or used
- **Severity**: LOW - Technical debt
- **Action**: Consider deprecation/removal

---

## Lessons Learned

### What Worked Well (from 2025-10-25 Analysis)

#### ✅ Task Tool with Explore Agent

- **Impact**: Extremely effective for automated analysis
- **Speed**: 10 minutes vs 1-2 hours manual
- **Accuracy**: More thorough, reads all files completely, less error-prone
- **Recommendation**: Always use if available

#### ✅ Structured Report Template

- **Impact**: Consistent, comprehensive documentation
- **Value**: Executive summary for stakeholders, detailed findings for implementers
- **Recommendation**: Use template for all analyses

#### ✅ Severity Classification

- **Impact**: Helps prioritize remediation effectively
- **Value**: Critical items get immediate attention, low priority deferred
- **Recommendation**: Apply consistent criteria across analyses

### Future Enhancements to Consider

#### 🔧 **Automated Health Scoring**

- Define formulas programmatically
- Auto-generate health score in report
- Track score over time across versions

#### 🔧 **Visual Dependency Graphs**

- Agent → Task → Template flow diagrams
- Identify orphaned items visually (red nodes)
- Use Mermaid diagrams in reports
- Interactive visualization tool

#### 🔧 **Diff Analysis**

- Compare before/after remediation
- Track which orphans were fixed over time
- Document remediation history
- Show improvement trends

#### 🔧 **Integration with Build System**

- Automated orphan detection on commits
- CI/CD pipeline integration
- Fail build if health score drops below threshold
- Generate report artifacts automatically

#### 🔧 **Remediation Story Generator**

- Auto-generate story text from analysis
- Pre-fill tasks/subtasks based on orphans
- Link stories to analysis report
- Reduce manual story creation time

#### 🔧 **Orphan Detection CLI Tool**

```bash
# Proposed future tool
npm run analyze:orphans -- --expansion-pack=bmad-technical-writing
npm run analyze:orphans -- --all  # All expansion packs
npm run analyze:orphans -- --ci   # CI mode, fail if orphans found
```

#### 🔧 **Quality Gates**

- Pre-commit hook: Validate new tasks have agent reference
- PR checks: Fail if orphans introduced
- Enforce "no orphans" policy for new additions
- Maintain health score thresholds

---

## Troubleshooting

### Issue: Analysis Incomplete - Missing Files

**Symptoms:**

- Report shows fewer tasks/templates than actually exist
- Known files not appearing in analysis

**Causes:**

- Glob pattern didn't match all files
- Files in unexpected subdirectories
- Non-standard file naming

**Solutions:**

- Use recursive glob: `tasks/**/*.md`
- Check for files in subdirectories
- Verify file naming conventions (`.md` vs `.markdown`)
- Manually check file count: `ls tasks/ | wc -l`

### Issue: False Positives - Connected Items Flagged

**Symptoms:**

- Task appears orphaned but you know it's referenced
- Agent clearly uses a task but it's listed as orphaned

**Causes:**

- Task referenced indirectly (through another task)
- Task name mentioned in comments, not dependencies
- YAML syntax error in agent file

**Solutions:**

- Verify YAML syntax in agent dependencies section
- Check for task names in non-dependency sections
- Look for indirect references
- Re-read agent file manually to confirm

### Issue: Overwhelming Number of Orphans

**Symptoms:**

- 50%+ items orphaned
- Can't prioritize effectively
- Remediation feels insurmountable

**Causes:**

- Expansion pack grew organically without governance
- Tasks/templates added without agent integration
- Lack of quality gates during development

**Solutions:**

- Focus on top 10 most critical items first
- Create phased remediation plan (3 releases)
- Consider removing truly unused items
- Implement quality gates for future additions
- Break remediation into multiple stories

### Issue: Unclear Parent Agent Assignment

**Symptoms:**

- Task could fit multiple agents
- No obvious "best fit" agent
- Team disagrees on assignment

**Causes:**

- Task has broad applicability
- Overlapping agent responsibilities
- Unclear agent boundaries

**Solutions:**

- Consider task's primary purpose
- Check which agent users would expect to find it in
- Assign to most specific agent (prefer specialized over general)
- Document decision and reasoning
- If truly ambiguous, assign to multiple agents

---

## Examples

### Example 1: Simple Orphan - Clear Fix

**Orphaned Task Found:**

```
Task: create-quiz.md
Description: Generate quiz questions from chapter content
Template References: quiz-tmpl.yaml
Current State: Not referenced by any agent
```

**Analysis:**

- **Severity**: MEDIUM - Useful but not critical
- **Parent Agent**: `exercise-creator` (obvious fit)
- **Template Status**: `quiz-tmpl.yaml` also orphaned
- **User Impact**: Quiz creation workflow hidden

**Recommendation:**

```yaml
# agents/exercise-creator.md
dependencies:
  tasks:
    - design-exercises
    - create-quiz # ADD THIS
  templates:
    - exercise-set-tmpl
    - quiz-tmpl # ADD THIS
```

**Effort**: 15 minutes

### Example 2: Complex Workflow Gap - High Impact

**Orphaned Tasks Found:**

```
Agent: tutorial-architect
Missing Tasks (4):
- write-chapter-draft.md (references 4 templates!)
- develop-tutorial.md (references tutorial-section-tmpl)
- write-introduction.md (references introduction-tmpl)
- write-summary.md (no template)
```

**Analysis:**

- **Severity**: CRITICAL - Core workflow incomplete
- **Parent Agent**: `tutorial-architect` (clear ownership)
- **Template Status**: All 4 templates connected elsewhere, but tasks orphaned
- **User Impact**: Users can't write chapters through tutorial-architect

**Recommendation:**

```yaml
# agents/tutorial-architect.md
dependencies:
  tasks:
    - create-chapter-outline
    - write-chapter-draft # ADD - highest priority
    - develop-tutorial # ADD
    - write-introduction # ADD
    - write-summary # ADD
  templates:
    - chapter-outline-tmpl
    - chapter-draft-tmpl # ADD
    - tutorial-section-tmpl # ADD
    - introduction-tmpl # ADD
```

**Effort**: 1-2 hours (includes testing)

### Example 3: Orphaned Template - Remove Decision

**Orphaned Template Found:**

```
Template: section-plan-tmpl.yaml
Status: Completely unused
Potential Use: Could be used by instructional-designer for section planning
Current References: NONE (no agents, no tasks)
```

**Analysis:**

- **Age**: Created 6 months ago, never used in production
- **Similar Functionality**: `chapter-outline-tmpl` covers similar use case
- **Decision Factors**:
  - No active demand from users
  - No clear workflow needing it
  - Adds maintenance burden

**Recommendation**: **REMOVE**

- Deprecate template
- Document removal in CHANGELOG
- Note: If section-level planning becomes needed, can recreate

**Alternative**: If team wants to keep, create `plan-section.md` task and add to `instructional-designer`

**Effort**: 30 minutes (removal) or 2-3 hours (full integration)

---

## Appendix A: Manual Analysis Process

If automated tools are unavailable, follow this manual process:

### 1. Inventory Phase (30 min)

**Create File Lists:**

```bash
cd /path/to/expansion-pack

# List all files
ls agents/ > analysis-inventory-agents.txt
ls tasks/ > analysis-inventory-tasks.txt
ls templates/ > analysis-inventory-templates.txt

# Count files
echo "Agents: $(ls agents/ | wc -l)"
echo "Tasks: $(ls tasks/ | wc -l)"
echo "Templates: $(ls templates/ | wc -l)"
```

### 2. Extract Agent Dependencies (30-45 min)

**Create Tracking Spreadsheet:**

| Agent Name | Tasks Referenced | Templates Referenced |
| ---------- | ---------------- | -------------------- |
| agent-1    | task-a, task-b   | tmpl-x, tmpl-y       |
| agent-2    | task-c           | tmpl-z               |

**For Each Agent:**

1. Open agent file
2. Find `dependencies:` YAML block
3. Copy tasks list
4. Copy templates list
5. Paste into spreadsheet

### 3. Extract Task Template References (30-45 min)

**Create Tracking List:**

| Task Name | Templates Referenced |
| --------- | -------------------- |
| task-a    | tmpl-x               |
| task-b    | tmpl-y, tmpl-z       |

**For Each Task:**

1. Open task file
2. Search for `.yaml` or `tmpl`
3. Note template references
4. Add to tracking list

### 4. Cross-Reference Analysis (20-30 min)

**Identify Orphaned Tasks:**

- Compare task inventory against ALL agent dependency lists
- Flag tasks that appear NOWHERE in agent dependencies
- Create "Orphaned Tasks" list

**Identify Orphaned Templates:**

- Compare template inventory against agent dependencies
- Compare against task template references
- Flag templates that appear NOWHERE
- Create "Orphaned Templates" list

### 5. Manual Reporting (45-60 min)

Use the report template from Step 6 to document findings manually.

**Total Manual Analysis Time:** 2.5-3.5 hours

---

## Appendix B: Health Score Calculation Details

### Detailed Formula

```
Component Scores (each 0-100%):

1. Agent Coverage = (Agents with dependencies / Total agents) × 100%
   - Measures: Do agents declare dependencies?
   - Target: 100%

2. Task-Agent Coverage = (Tasks referenced by agents / Total tasks) × 100%
   - Measures: Task discoverability through agents
   - Target: 90%+

3. Template-Agent Coverage = (Templates referenced by agents or tasks / Total templates) × 100%
   - Measures: Template integration
   - Target: 85%+

4. Orphan Rate (Inverse) = 100% - (Total orphaned items / Total items) × 100%
   - Measures: Overall integration health
   - Target: 90%+

Overall Health Score = (Sum of all components) / 4

Weighted Alternative (if preferred):
= (Agent Coverage × 0.2) + (Task-Agent Coverage × 0.4) + (Template-Agent Coverage × 0.2) + (Orphan Rate × 0.2)
```

### Rating Scale

| Score     | Rating               | Description                                               |
| --------- | -------------------- | --------------------------------------------------------- |
| 95-100%   | ⭐⭐⭐⭐⭐ Excellent | Nearly perfect integration, minimal issues                |
| 85-94%    | ⭐⭐⭐⭐ Very Good   | Strong integration, minor improvements possible           |
| 75-84%    | ⭐⭐⭐ Good          | Acceptable but needs attention                            |
| 60-74%    | ⭐⭐ Needs Attention | Significant gaps, remediation recommended                 |
| 50-59%    | ⭐ Poor              | Major integration issues, urgent remediation              |
| Below 50% | ❌ Critical          | Severe issues, expansion pack may not be production-ready |

---

## Appendix C: Report Checklist

Use this checklist to ensure your analysis report is complete:

### Report Completeness

- [ ] **Executive Summary**
  - [ ] Expansion pack name and version
  - [ ] Analysis date and analyst
  - [ ] Key finding (1-2 sentences)
  - [ ] Health score with rating

- [ ] **Metrics Table**
  - [ ] Agent coverage %
  - [ ] Task-agent coverage %
  - [ ] Template-agent coverage %
  - [ ] Orphaned tasks count and %
  - [ ] Orphaned templates count and %

- [ ] **Orphaned Tasks Section**
  - [ ] Complete list of all orphaned tasks
  - [ ] Description for each task
  - [ ] Template references noted
  - [ ] Parent agent identified
  - [ ] Severity assigned
  - [ ] Recommendation provided

- [ ] **Orphaned Templates Section**
  - [ ] Complete list of all orphaned templates
  - [ ] Status for each (unused vs indirect)
  - [ ] Potential use identified
  - [ ] Recommendation (keep or remove)

- [ ] **Connected Items Summary**
  - [ ] Agent → Task mapping
  - [ ] Agent → Template mapping
  - [ ] Task → Template mapping
  - [ ] Gaps identified for each agent

- [ ] **Recommendations Section**
  - [ ] Short-term fixes with YAML examples
  - [ ] Medium-term improvements
  - [ ] Long-term strategy

- [ ] **Priority Action Items**
  - [ ] Immediate actions (this week)
  - [ ] High priority (this sprint)
  - [ ] Medium priority (this quarter)
  - [ ] Low priority (backlog)
  - [ ] Effort estimates for each

- [ ] **Conclusion**
  - [ ] Summary of findings
  - [ ] Expected outcome after remediation
  - [ ] Before/after health score projection
  - [ ] Next review date

### Quality Checks

- [ ] All orphaned items accounted for
- [ ] No false positives (verified)
- [ ] Severity classifications consistent
- [ ] Effort estimates realistic
- [ ] YAML examples syntactically correct
- [ ] File paths are absolute and accurate
- [ ] Report saved to version control
- [ ] Stakeholders notified

---

## Appendix D: Template - Analysis Prompt

Copy-paste this prompt template when running automated analysis:

```
Analyze the [EXPANSION-PACK-NAME] expansion pack to identify orphaned tasks and templates.

Directory: [ABSOLUTE-PATH]

I need you to:

1. **Get all files:**
   - All agent files in agents/
   - All task files in tasks/
   - All template files in templates/

2. **Read all agent files** and extract:
   - What tasks each agent references in their dependencies.tasks section
   - What templates each agent references in their dependencies.templates section

3. **Read all task files** and extract:
   - What templates each task references (look for template names, .yaml, tmpl in content)

4. **Create a comprehensive report showing:**

   A. **Orphaned Tasks** - Tasks that are NOT referenced by any agent
      For each orphaned task, provide:
      - Task filename
      - Brief description (from the task file itself)
      - Templates it references (if any)
      - Which agent(s) should logically reference this task
      - Severity recommendation (Critical/High/Medium/Low)
      - User impact (what workflow is broken/hidden)

   B. **Orphaned Templates** - Templates that are NOT referenced by any agent OR any task
      For each orphaned template, provide:
      - Template filename
      - Brief description (from template metadata if available)
      - Status: Completely unused OR only referenced by orphaned tasks
      - Potential uses
      - Recommendation: Keep and connect OR remove

   C. **Connected Items Summary**
      - Agent → Tasks mapping (for each agent, list connected tasks)
      - Agent → Templates mapping (for each agent, list connected templates)
      - Task → Template mapping (for each task, list templates it references)
      - For each agent, identify MISSING tasks/templates that logically belong

   D. **Health Metrics**
      Calculate and report:
      - Total agents, tasks, templates
      - Number and percentage of orphaned tasks
      - Number and percentage of orphaned templates
      - Agent coverage % (agents with dependencies / total agents)
      - Task-agent coverage % (connected tasks / total tasks)
      - Template-agent coverage % (connected templates / total templates)
      - Overall health score (average of components)

5. **Prioritization**
   Organize orphaned items into:
   - CRITICAL (fix immediately)
   - HIGH (fix soon)
   - MEDIUM (fix later)
   - LOW (optional/backlog)

6. **Return the complete analysis** with all findings clearly organized.

Be thorough - read all files completely to ensure accuracy. Focus only on the expansion pack directory, not core BMAD files.

Expected output format: Comprehensive markdown report with all sections above.
```

---

## Version History

| Version | Date       | Changes                        | Author     |
| ------- | ---------- | ------------------------------ | ---------- |
| 1.0     | 2025-10-25 | Initial workflow documentation | Sarah (PO) |

---

## Related Documentation

- **expansion-packs.md**: Guide for creating expansion packs
- **GUIDING-PRINCIPLES.md**: Design philosophy for BMAD
- **CONTRIBUTING.md**: Contribution guidelines
- **core-architecture.md**: BMAD system architecture

---

**Questions or Improvements?**

If you have suggestions for improving this workflow, please:

- Open an issue on GitHub
- Submit a PR with enhancements
- Share findings from your analyses

This is a living document - your experience using this workflow helps make it better!
