<!-- Powered by BMAD™ Core -->

# Validate Learning Flow

---

task:
id: validate-learning-flow
name: Validate Learning Flow
description: Validate pedagogical progression, prerequisite dependencies, and difficulty curve in learning content. Ensures no knowledge gaps, logical concept building, and appropriate cognitive load.
persona_default: instructional-designer
inputs:
  - outline_or_chapter_path
  - prerequisites_defined
steps:
  - Read the outline or chapter content completely
  - Map all concepts and their dependencies
  - Check prerequisite dependencies for circular references
  - Validate difficulty progression using Bloom's Taxonomy
  - Verify no knowledge gaps between sections/chapters
  - Assess exercise complexity alignment with concepts
  - Evaluate cognitive load management
  - Run execute-checklist.md with learning-objectives-checklist.md
  - Run execute-checklist.md with prerequisite-clarity-checklist.md
  - Compile validation report with pass/fail status
  - Use template learning-flow-validation-report-tmpl.yaml with create-doc.md
output: reviews/validation-results/learning-flow-validation-{{timestamp}}.md

---

## Purpose

This task validates that learning content follows sound pedagogical principles. It ensures concepts build logically, prerequisites are met in order, difficulty progresses appropriately, and learners can successfully achieve objectives without encountering knowledge gaps.

## Prerequisites

- Outline or chapter content to validate
- Prerequisites clearly stated for the content
- Understanding of Bloom's Taxonomy
- Access to learning-objectives-checklist.md
- Access to prerequisite-clarity-checklist.md

## Workflow Steps

### 1. Read Content Completely

Read the entire outline or chapter without interruption:

- Understand the overall learning arc
- Note stated learning objectives
- Identify all major concepts covered
- Understand target audience level
- Note stated prerequisites

**Purpose:** Get full context before detailed analysis.

### 2. Map Concepts and Dependencies

Create a concept dependency map:

**For Each Concept:**

- List the concept name
- Identify prerequisite concepts needed to understand it
- Note where prerequisites are taught (chapter/section)
- Mark if prerequisite is external (not taught in book)

**Example Map:**

```
Concept: JWT Authentication
Prerequisites:
  - HTTP requests (Chapter 2) ✓
  - JSON format (Chapter 1) ✓
  - Basic cryptography (External - stated) ✓
```

**Create:** A dependency graph or list showing concept flow.

### 3. Check Prerequisite Dependencies

Validate dependency integrity:

**Check for Circular Dependencies:**

- Does Concept A require B, and B require A?
- Flag any circular references as critical errors

**Check for Forward Dependencies:**

- Is any concept required before it's taught?
- Example: Chapter 3 uses async/await but it's taught in Chapter 5
- Flag as critical learning gap

**Check for Missing Prerequisites:**

- Are external prerequisites clearly stated?
- Are in-book prerequisites explicitly noted?
- Can a reader identify what they need to know?

**Pass Criteria:**

- No circular dependencies
- No forward dependencies
- All external prerequisites clearly stated

### 4. Validate Difficulty Progression (Bloom's Taxonomy)

Assess cognitive complexity using Bloom's Taxonomy levels:

**Bloom's Taxonomy Levels (Simple → Complex):**

1. **Remember** - Recall facts, terms, concepts
   - Example: "List the HTTP methods"
2. **Understand** - Explain ideas or concepts
   - Example: "Explain why GET is idempotent"
3. **Apply** - Use information in new situations
   - Example: "Implement a GET endpoint"
4. **Analyze** - Draw connections among ideas
   - Example: "Compare REST and GraphQL trade-offs"
5. **Evaluate** - Justify decisions or approaches
   - Example: "Evaluate whether to use JWT or sessions"
6. **Create** - Produce new or original work
   - Example: "Design an authentication system"

**For Each Chapter/Section:**

- Identify the Bloom's level of learning objectives
- Check that difficulty increases gradually
- Ensure no sudden jumps (e.g., Remember → Create without intermediate steps)
- Verify exercises match or slightly exceed objective level

**For Beginners:** Start with Remember/Understand, build to Apply
**For Intermediate:** Apply/Analyze heavily, introduce Evaluate
**For Advanced:** Analyze/Evaluate/Create focus

**Pass Criteria:**

- Smooth progression through Bloom's levels
- No jumps > 2 levels between adjacent chapters
- Exercise difficulty aligns with objectives

### 5. Verify No Knowledge Gaps

Check for missing conceptual bridges:

**Identify Gaps:**

- Concepts used but not explained
- Assumptions about reader knowledge not stated in prerequisites
- Terms used without definition
- Jumps in complexity without scaffolding

**Examples of Gaps:**

❌ **Gap:** Chapter 4 uses promises extensively but Chapter 3 only briefly mentions them
✓ **No Gap:** Chapter 3 teaches promises thoroughly, Chapter 4 builds on that foundation

❌ **Gap:** Example uses arrow functions assuming reader knows them, but they're not taught
✓ **No Gap:** Arrow functions introduced in Chapter 2, used consistently thereafter

**For Each Gap Found:**

- Describe the missing knowledge
- Identify where it first appears
- Suggest where it should be taught
- Assess severity (critical if blocks learning, minor if just confusing)

**Pass Criteria:**

- No critical knowledge gaps
- All concepts taught before use
- Assumptions explicitly stated

### 6. Assess Exercise Complexity Alignment

Verify exercises support learning objectives:

**For Each Exercise:**

- Does it practice the concept just taught?
- Is difficulty appropriate for reader's current level?
- Can it be completed with knowledge from current + prior chapters?
- Does it require unstated prerequisites?

**Exercise Progression Check:**

- Early exercises should be guided and concrete
- Middle exercises should be less guided, more application
- Later exercises should be open-ended problem solving

**Example Good Progression:**

1. Chapter 2 End: "Add a GET endpoint to the provided server" (Guided)
2. Chapter 5 End: "Implement authentication for your API" (Less guided)
3. Chapter 10 End: "Design and implement a complete feature" (Open-ended)

**Pass Criteria:**

- All exercises are completable with taught content
- Difficulty progression is logical
- No exercises require forward knowledge

### 7. Evaluate Cognitive Load Management

Assess if content avoids overwhelming learners:

**Intrinsic Load (Concept Difficulty):**

- Are complex concepts broken into digestible parts?
- Is new terminology introduced gradually?
- Are difficult topics given sufficient time/space?

**Extraneous Load (Presentation Issues):**

- Are diagrams clear and necessary?
- Are code examples focused (not too many concepts at once)?
- Are digressions or "nice to know" items clearly marked?

**Germane Load (Schema Building):**

- Are patterns and connections explicitly highlighted?
- Are summaries provided to aid memory?
- Are mental models reinforced?

**Red Flags:**

- More than 3 new concepts introduced simultaneously
- Complex code examples with 5+ unfamiliar elements
- Missing scaffolding for difficult transitions

**Pass Criteria:**

- No more than 3 major new concepts per section
- Complex examples are built up incrementally
- Cognitive load appears manageable for target audience

### 8. Run Learning Objectives Checklist

Execute checklist validation:

**Run:** `execute-checklist.md` with `learning-objectives-checklist.md`

**Verify:**

- Action verbs used appropriately
- Objectives are measurable
- Specificity is adequate
- Alignment with content
- Prerequisites are clear
- Difficulty level is appropriate

**Document** any checklist items that fail.

### 9. Run Prerequisite Clarity Checklist

Execute checklist validation:

**Run:** `execute-checklist.md` with `prerequisite-clarity-checklist.md`

**Verify:**

- Prerequisites are explicitly stated
- Required knowledge level is clear
- External dependencies identified
- In-book dependencies noted

**Document** any checklist items that fail.

### 10. Compile Validation Report

Create structured validation report:

**Report Structure:**

#### Executive Summary

- Overall Pass/Fail status
- Critical issues count
- Major issues count
- Minor issues count
- Recommendation (Approve / Minor Revision / Major Revision)

#### Concept Dependency Analysis

- Dependency map or graph
- Circular dependency findings
- Forward dependency findings
- Missing prerequisite findings

#### Bloom's Taxonomy Progression

- Table of chapters/sections with Bloom's levels
- Difficulty progression assessment
- Identified jumps or gaps
- Exercise alignment findings

#### Knowledge Gap Analysis

- List of identified gaps with severity
- Locations where gaps occur
- Recommendations for bridging gaps

#### Cognitive Load Assessment

- Sections with high cognitive load
- Recommendations for reducing load
- Positive examples of good scaffolding

#### Checklist Results

- Learning objectives checklist pass/fail items
- Prerequisite clarity checklist pass/fail items

#### Recommendations

- Prioritized action items
- Specific suggestions for improvement
- Examples of fixes

**Pass/Fail Thresholds:**

- **Pass:** 0 critical issues, ≤ 2 major issues, minor issues acceptable
- **Minor Revision:** 0 critical, 3-5 major issues
- **Major Revision:** Any critical issues OR > 5 major issues

## Output

Learning flow validation report should include:

- Clear pass/fail status
- Concept dependency map
- Bloom's taxonomy progression analysis
- All identified knowledge gaps with severity
- Cognitive load assessment
- Checklist results
- Prioritized recommendations

**Save to:** `reviews/validation-results/learning-flow-validation-{{timestamp}}.md`

## Quality Standards

Effective learning flow validation:

✓ Maps all concept dependencies completely
✓ Identifies all prerequisite issues
✓ Assesses Bloom's taxonomy progression accurately
✓ Finds all knowledge gaps
✓ Evaluates cognitive load thoughtfully
✓ Provides actionable recommendations
✓ Uses clear severity ratings
✓ Supports pedagogical soundness

## Examples

### Example: Prerequisite Violation Found

**Finding:**

```
Location: Chapter 5, Section 2
Severity: Critical
Issue: Uses async/await extensively without prior introduction
Prerequisite: Async/await is taught in Chapter 7
Impact: Readers will not understand the code examples
Recommendation: Move async/await introduction to Chapter 4, or delay Chapter 5 examples until after Chapter 7
```

### Example: Bloom's Taxonomy Jump

**Finding:**

```
Location: Chapter 3 → Chapter 4 transition
Severity: Major
Issue: Chapter 3 focuses on Remember/Understand level (explaining concepts). Chapter 4 immediately jumps to Evaluate level (comparing architectural approaches)
Gap: Missing Apply and Analyze exercises between chapters
Recommendation: Add hands-on implementation exercises in Chapter 3 to reach Apply level before Chapter 4's evaluation tasks
```

### Example: Cognitive Load Issue

**Finding:**

```
Location: Chapter 2, Section 3
Severity: Major
Issue: Introduces 5 new concepts simultaneously (promises, async/await, error handling, HTTP clients, JSON parsing) in a single code example
Impact: Overwhelming for beginners; too much new information at once
Recommendation: Break into 2-3 sections:
  - Section 3A: Promises basics with simple examples
  - Section 3B: Async/await with promise refactoring
  - Section 3C: HTTP requests combining all concepts
```

## Next Steps

After validation:

1. Deliver validation report to content author or instructional designer
2. Author addresses critical issues (must fix)
3. Author addresses major issues (should fix)
4. Re-validate if critical or major changes made
5. Approve for continued development or publication
