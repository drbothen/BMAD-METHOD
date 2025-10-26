<!-- Powered by BMAD™ Core -->

# Execute Checklist

---

task:
id: execute-checklist
name: Execute Checklist
description: Systematically execute checklist items with pass/fail/na status and evidence collection for quality assurance
persona_default: technical-reviewer
inputs:

- checklist_path
- subject_name
- context_notes
  steps:
- Load and parse checklist file
- Process each category and item sequentially
- Evaluate and mark status (PASS/FAIL/NA) with evidence
- Generate results report with summary statistics
- Save results to standard location
  output: reviews/checklist-results/{{checklist-name}}-{{timestamp}}.md

---

## Purpose

This task provides a structured way to execute quality checklists and document results. It ensures all checklist items are systematically evaluated with evidence, creating an auditable record of quality gate execution.

## Prerequisites

- Checklist file exists and is accessible
- Subject material to be reviewed is available
- Understanding of checklist criteria
- Authority to evaluate against checklist standards

## Inputs

**Required:**

- `checklist_path`: Path to the checklist markdown file (e.g., `checklists/code-quality-checklist.md`)
- `subject_name`: Descriptive name of what's being checked (e.g., "Chapter 3: Database Design", "User Authentication Module")

**Optional:**

- `context_notes`: Additional context for the review (e.g., "First draft", "Post-revision", "Version 2.0 update")

## Workflow Steps

### 1. Load Checklist File

Load and parse the checklist:

- Read the checklist file from `checklist_path`
- Identify all categories (markdown H2 headings)
- Extract all checklist items (lines starting with `- [ ]`)
- Count total items for summary statistics
- Verify checklist structure is valid

**Validation:**

- File exists and is readable
- Contains at least one category
- Contains at least one checklist item
- Items follow standard markdown checkbox format

### 2. Initialize Results Document

Create the results file structure:

- Generate timestamp for unique filename
- Extract checklist name from file path
- Create results file path: `reviews/checklist-results/{{checklist-name}}-{{timestamp}}.md`
- Initialize document with header information:
  - Subject name
  - Date and time
  - Checklist source path
  - Context notes (if provided)

**Note:** Results are saved incrementally as you progress through the checklist.

### 3. Process Each Category

Work through checklist categories systematically:

For each category (H2 section):

1. **Announce category**: State which category you're evaluating
2. **Read all items in category**: Get overview of what's being checked
3. **Process items sequentially**: Work through each checkbox item

**Process Flow:**

- Category 1 → All items → Results saved
- Category 2 → All items → Results saved
- Continue until all categories complete

### 4. Evaluate Each Checklist Item

For each checklist item, perform systematic evaluation:

**Evaluation Process:**

1. **Read the item**: Understand what's being checked
2. **Examine the subject**: Review relevant content/code/documentation
3. **Make determination**: Decide on status
4. **Document evidence**: Record specific findings

**Status Values:**

- **✅ PASS**: Item meets criteria fully
  - Provide brief evidence or write "Confirmed"
  - Example: "All code examples follow PEP 8 style guide"

- **❌ FAIL**: Item does not meet criteria
  - Document specific issue found
  - Explain why it fails
  - Provide recommendation for fix
  - Example: "Function `calculateTotal` missing error handling for empty cart scenario. Add validation before processing."

- **⊘ N/A**: Item not applicable to this subject
  - Explain why it doesn't apply
  - Example: "No JavaScript code in this chapter, checklist item not applicable"

**Evidence Requirements:**

- PASS: Brief confirmation or location reference
- FAIL: Detailed explanation with location and recommendation
- N/A: Reason for non-applicability

### 5. Handle Failed Items

When checklist item fails:

**Document Failure:**

- Mark status as ❌ FAIL
- Record specific location of issue (section, file, line number)
- Describe what was found vs what was expected
- Provide actionable recommendation for fixing

**Continue Execution:**

- Do NOT halt on failures (except critical issues - see below)
- Continue through all remaining items
- Capture complete picture of all issues

**Halt Immediately Only For:**

- Critical security vulnerabilities (exposed credentials, SQL injection)
- Data loss risks or corruption
- Legal/compliance violations
- Plagiarism or copyright infringement

If you encounter a halt-worthy issue:

1. Mark the item as ❌ FAIL with detailed explanation
2. Note "CRITICAL ISSUE - EXECUTION HALTED" in results
3. Stop checklist execution
4. Alert user immediately

### 6. Generate Summary Statistics

After all items processed (or if halted):

Calculate and include:

- **Total Items**: Count of all checklist items
- **Passed**: Count and percentage of PASS items
- **Failed**: Count and percentage of FAIL items
- **N/A**: Count and percentage of N/A items
- **Completion**: Percentage of applicable items that passed

**Overall Status Determination:**

- **PASS**: All applicable items passed (100% of PASS/(PASS+FAIL))
- **PASS WITH CONCERNS**: 80-99% pass rate, minor issues present
- **FAIL**: Less than 80% pass rate, significant issues present
- **CRITICAL FAILURE**: Execution halted due to critical issue

### 7. Create Failed Items Priority Section

If any items failed:

Create a dedicated section listing all failures:

**For Each Failed Item:**

- Category and item text
- Status: FAIL
- Evidence: Full details of what was found
- Location: Specific reference (section, file, line)
- Recommendation: How to fix the issue
- Priority: Based on severity (Critical/High/Medium/Low)

**Purpose:** Provides quick reference for remediation work

### 8. Add Recommendations

Include actionable next steps:

**Recommendations based on overall status:**

- **PASS**: Subject meets all checklist criteria, ready to proceed
- **PASS WITH CONCERNS**: Address failed items before final approval
- **FAIL**: Must address all failures before proceeding
- **CRITICAL FAILURE**: Stop all work, address critical issue immediately

**Include:**

- Priority order for addressing failures
- Estimated effort for remediation
- Suggested next steps in workflow

### 9. Save Results

Save the complete results document:

- Write to `reviews/checklist-results/{{checklist-name}}-{{timestamp}}.md`
- Ensure directory exists (create if needed)
- Verify file was written successfully
- Provide user with results file path

**Results file includes:**

- Header with metadata
- Summary statistics
- Results by category (table format)
- Failed items priority section
- Recommendations
- Timestamp and audit trail

## Output Format

Results file structure:

```markdown
# Checklist Results: {{checklist-name}}

**Subject**: {{subject_name}}
**Date**: {{timestamp}}
**Checklist**: {{checklist_path}}
**Context**: {{context_notes}}

## Summary

- **Total Items**: 25
- **Passed**: 20 (80%)
- **Failed**: 3 (12%)
- **N/A**: 2 (8%)
- **Completion**: 87% (20/23 applicable items passed)
- **Overall Status**: PASS WITH CONCERNS

## Results by Category

### [Category Name]

| Status  | Item                     | Evidence/Notes                                     |
| ------- | ------------------------ | -------------------------------------------------- |
| ✅ PASS | Item text from checklist | Brief evidence or "Confirmed"                      |
| ❌ FAIL | Item text from checklist | Detailed explanation of failure and recommendation |
| ⊘ N/A   | Item text from checklist | Reason not applicable                              |

### [Next Category Name]

...

## Failed Items (Priority Review)

### 1. [Category] Item text

- **Status**: FAIL
- **Location**: Specific reference (e.g., "Section 3.2, code example")
- **Evidence**: Detailed explanation of what was found
- **Expected**: What should have been found
- **Recommendation**: Specific fix needed
- **Priority**: High/Medium/Low

### 2. [Category] Next failed item

...

## Recommendations

Based on the overall status of **PASS WITH CONCERNS**:

1. Address all failed items before final approval
2. Priority order: [list priorities]
3. Estimated effort: [estimate]
4. Next steps: [workflow guidance]

---

_Checklist execution completed at {{timestamp}}_
_Executed by: {{agent_name}}_
```

## Quality Standards

Effective checklist execution:

✓ All checklist items evaluated systematically
✓ Evidence provided for every item
✓ Failed items documented with specific locations
✓ Actionable recommendations provided
✓ Summary statistics accurate
✓ Results saved to standard location
✓ Overall status reflects actual state
✓ Audit trail complete and professional

## Common Pitfalls

Avoid:

❌ Skipping items or categories
❌ Marking items PASS without actually checking
❌ Vague failure descriptions ("doesn't work")
❌ Missing evidence or locations
❌ Continuing past critical security issues
❌ Inconsistent status marking
❌ Incomplete summary statistics

## Usage Examples

### Example 1: Technical Review

```
Agent: technical-reviewer
Task: execute-checklist
Inputs:
  - checklist_path: checklists/technical-accuracy-checklist.md
  - subject_name: Chapter 5: Advanced SQL Queries
  - context_notes: Second draft after initial review
Output: reviews/checklist-results/technical-accuracy-checklist-2024-10-24-14-30.md
```

### Example 2: Code Quality Check

```
Agent: code-curator
Task: execute-checklist
Inputs:
  - checklist_path: checklists/code-quality-checklist.md
  - subject_name: Chapter 3: Web Scraping Project
  - context_notes: Final review before publication
Output: reviews/checklist-results/code-quality-checklist-2024-10-24-15-45.md
```

### Example 3: Publisher Submission

```
Agent: publishing-coordinator
Task: execute-checklist
Inputs:
  - checklist_path: checklists/packtpub-submission-checklist.md
  - subject_name: Complete manuscript - Python Web Scraping Book
  - context_notes: Pre-submission quality gate
Output: reviews/checklist-results/packtpub-submission-checklist-2024-10-24-16-20.md
```

### Example 4: Book Outline Validation

```
Agent: instructional-designer
Task: execute-checklist
Inputs:
  - checklist_path: checklists/book-outline-checklist.md
  - subject_name: Machine Learning Fundamentals Book Outline
  - context_notes: Initial outline review before chapter development
Output: reviews/checklist-results/book-outline-checklist-2024-10-24-17-15.md
```

### Example 5: Chapter Outline Validation

```
Agent: tutorial-architect
Task: execute-checklist
Inputs:
  - checklist_path: checklists/chapter-outline-checklist.md
  - subject_name: Chapter 3: Neural Networks Outline
  - context_notes: Validating structure before section planning
Output: reviews/checklist-results/chapter-outline-checklist-2024-10-24-18-00.md
```

### Example 6: Section Plan Validation

```
Agent: tutorial-architect
Task: execute-checklist
Inputs:
  - checklist_path: checklists/section-plan-checklist.md
  - subject_name: Section 2: Building Your First Neural Network
  - context_notes: Section plan complete, ready for development
Output: reviews/checklist-results/section-plan-checklist-2024-10-24-19-30.md
```

### Example 7: Section Completeness Check

```
Agent: tutorial-architect
Task: execute-checklist
Inputs:
  - checklist_path: checklists/section-completeness-checklist.md
  - subject_name: Section 2: Building Your First Neural Network
  - context_notes: Before marking section DONE
Output: reviews/checklist-results/section-completeness-checklist-2024-10-24-20-15.md
```

### Example 8: Code Example Quality Check

```
Agent: code-curator
Task: execute-checklist
Inputs:
  - checklist_path: checklists/code-example-checklist.md
  - subject_name: neural_network_basic.py
  - context_notes: After testing, before section integration
Output: reviews/checklist-results/code-example-checklist-2024-10-24-21-00.md
```

## Troubleshooting

**Issue**: Checklist file not found

- Verify file path is correct relative to project root
- Check file extension is `.md`
- Ensure file exists in expected location

**Issue**: No checklist items detected

- Verify checklist uses standard markdown checkbox format: `- [ ] Item text`
- Check for proper category headings (H2: `## Category Name`)
- Ensure file is not empty or malformed

**Issue**: Unclear how to evaluate item

- Read item carefully and interpret based on context
- Refer to subject material being reviewed
- If truly ambiguous, mark as N/A and note ambiguity in evidence
- Consider consulting checklist owner or subject matter expert

**Issue**: Too many failures to track

- Continue execution, document all failures
- Use Failed Items Priority Section to organize
- Consider if subject needs major rework before continuing
- May indicate checklist mismatch with subject maturity

**Issue**: Results directory doesn't exist

- Create `reviews/checklist-results/` directory structure
- Ensure write permissions
- Verify project root location

## Integration with Workflows

This task is used in quality gates across workflows:

- **Section Development Workflow**: Technical review checkpoint
- **Chapter Assembly Workflow**: Completeness validation
- **Book Planning Workflow**: Proposal and outline validation
- **Publishing Workflows**: Publisher-specific submission requirements
- **Code Repository Workflow**: Code quality validation

## Next Steps

After checklist execution:

1. **If PASS**: Proceed to next workflow step
2. **If PASS WITH CONCERNS**: Review failed items, decide on remediation
3. **If FAIL**: Address failures before proceeding
4. **If CRITICAL FAILURE**: Stop all work, escalate issue

The results file provides an auditable record for:

- Workflow progression decisions
- Quality assurance tracking
- Team communication
- Process improvement analysis
