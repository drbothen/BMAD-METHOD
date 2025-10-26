# Sample Book Project Walkthrough

This walkthrough shows you **step-by-step** how this sample chapter was created using the BMAD Technical Writing Expansion Pack's section-driven development workflow.

## Table of Contents

1. [Overview](#part-1-overview)
2. [Setup](#part-2-setup)
3. [Book Planning](#part-3-book-planning)
4. [Section Planning](#part-4-section-planning)
5. [Section Development Loop](#part-5-section-development-loop)
6. [Chapter Assembly](#part-6-chapter-assembly)
7. [Key Takeaways](#part-7-key-takeaways)
8. [Adaptations for Your Book](#part-8-adaptations-for-your-book)

---

## Part 1: Overview

### What This Walkthrough Shows

This walkthrough demonstrates the **complete section-driven development workflow** for creating a technical book chapter, from initial outline to final polished chapter.

**You will see:**
- Which agent to activate at each step
- Which task to execute for each workflow phase
- What inputs are needed and what outputs are produced
- How Sprint 7 tasks integrate into the workflow
- Real examples of all intermediate artifacts

### Workflows Demonstrated

1. **Section Planning Workflow** - Break chapter into manageable sections
2. **Section Development Workflow** (×3) - Develop each section from plan to final
3. **Chapter Assembly Workflow** - Merge sections into cohesive chapter

### Time Investment

**Total**: ~12-16 hours actual work

**Per section**: 3-4 hours (plan → code → write → review → finalize)

### Sprint 7 Tasks Highlighted ⭐

Throughout this walkthrough, you'll see these new Sprint 7 tasks in action:
- `write-section-draft.md` - Core section writing task
- `execute-checklist.md` - Quality gate execution
- `merge-sections.md` - Chapter assembly
- `enhance-transitions.md` - Narrative flow improvement
- `validate-learning-flow.md` - Instructional design validation

---

## Part 2: Setup

### Prerequisites

Before starting, ensure you have:
- BMAD Technical Writing Expansion Pack installed
- Project directory structure set up
- Access to agents: tutorial-architect, instructional-designer, code-curator, technical-reviewer, technical-editor

### Project Structure

Create this structure (or use an existing book project):

```
sample-book-project/
├── book-outline.md                  # Book-level planning
├── manuscript/
│   ├── outlines/
│   │   └── chapter-3-outline.md     # Chapter planning
│   ├── sections/chapter-3/          # Section workflow artifacts
│   └── chapters/                    # Final assembled chapters
├── code/chapter-3/                  # Code examples with tests
├── reviews/                         # Review reports
└── checklists/                      # Quality gate results
```

### File Naming Conventions

Follow these patterns for consistency:
- **Outlines**: `{chapter-name}-outline.md`
- **Section plans**: `section-{n}-plan.md`
- **Section drafts**: `section-{n}-draft.md`
- **Section finals**: `section-{n}-final.md`
- **Code files**: `{topic}.py` and `test_{topic}.py`
- **Reviews**: `section-{n}-review-notes.md`
- **Checklists**: `section-{n}-checklist-results.md`

---

## Part 3: Book Planning

### Step 1: Create Book Outline

**Time**: 30-60 minutes

**Agent**: `/bmad-tw:agents:instructional-designer`

**Task**: `design-book-outline.md`

**Input**: Book idea, target audience, rough chapter list

**Process**:
1. Activate instructional-designer agent
2. Request book outline creation
3. Define 5-7 chapters with descriptions
4. Set learning objectives
5. Identify prerequisite knowledge

**Output**: `book-outline.md`

**Sample book outline**:
- **Title**: Python Essentials: Data Structures and Algorithms
- **Audience**: Beginner programmers with basic Python syntax knowledge
- **Chapters**: 5 chapters (Ch 1-2: Review, Ch 3: Lists/Tuples ← focus, Ch 4-5: Dicts/Algorithms)

**What this looks like in practice**:

```markdown
# Activate agent
/bmad-tw:agents:instructional-designer

# Request outline
"I want to create a beginner Python book focusing on data structures.
Target audience is new programmers who know basic syntax.
5 chapters covering fundamentals through algorithms."

# Agent creates book-outline.md using design-book-outline.md task
```

---

### Step 2: Create Chapter Outline

**Time**: 45-90 minutes

**Agent**: `/bmad-tw:agents:tutorial-architect`

**Task**: `create-chapter-outline.md`

**Input**: Book outline, chapter number/topic

**Process**:
1. Activate tutorial-architect
2. Reference book outline for context
3. Request chapter 3 outline
4. Define learning objectives, prerequisites, estimated length
5. Recommend section-driven approach for 15-20 page chapter

**Output**: `manuscript/outlines/chapter-3-outline.md`

**Key decisions**:
- **Chapter scope**: 15-20 pages (good fit for section-driven)
- **Sections**: 6-8 sections recommended
- **Code examples**: Yes, working Python code
- **Development approach**: Section-driven (develop incrementally)

**What this looks like**:

```markdown
# Activate agent
/bmad-tw:agents:tutorial-architect

# Request chapter outline
"Create outline for Chapter 3: Working with Lists and Tuples.
Should cover list basics, operations, tuples, and some advanced topics.
Aimed at beginners who completed Chapter 2 on data types."

# Agent creates chapter-3-outline.md
```

---

## Part 4: Section Planning

### Step 3: Analyze Chapter and Plan Sections

**Time**: 1-2 hours

**Agent**: `tutorial-architect` + `instructional-designer`

**Workflow**: `section-planning-workflow.yaml`

**Input**: `chapter-3-outline.md`

**Process**:
1. Tutorial-architect analyzes chapter outline
2. Breaks chapter into 6-8 logical sections
3. Instructional-designer validates learning progression
4. Creates section-list.md with all sections planned

**Output**: `manuscript/sections/chapter-3/section-list.md`

**6 Sections Planned**:
1. **Section 3.1**: List Basics (Creating and Accessing Lists) ← develop
2. **Section 3.2**: List Operations (Modify, Add, Remove) ← develop
3. **Section 3.3**: Tuples and Immutability ← develop
4. **Section 3.4**: List Comprehensions (planned, not developed)
5. **Section 3.5**: Sorting and Searching (planned, not developed)
6. **Section 3.6**: Practical Applications (planned, not developed)

**Why 3 developed + 3 planned?**
- Demonstrates complete workflow without overwhelming sample size
- Shows planning foresight (sections 4-6 planned for future)
- Keeps sample creation time reasonable (12-16 hours vs 30+ hours)

**Section plan details**: Each section plan includes:
- Learning objectives
- Prerequisites (which previous section required)
- Content structure (concept → tutorial → practice)
- Code examples needed (count and type)
- Estimated pages (2-5 pages per section)

**What this looks like**:

```markdown
# Activate agent
/bmad-tw:agents:tutorial-architect

# Request section planning
"Analyze chapter-3-outline.md and break it into 6-8 sections.
Create section plans for each. I want to develop 3 sections fully
and leave 3 as planned for scope management."

# Agent executes section-planning-workflow.yaml
# Creates section-list.md with 6 section plans
# Marks sections 1-3 for development, 4-6 as planned
```

---

## Part 5: Section Development Loop

This is the **core workflow** - repeat 3 times (once per section).

**Total time per section**: 3-4 hours

### Section 1: List Basics

#### Step 5.1.A: Create Code Examples

**Time**: 30-45 minutes

**Agent**: `code-curator`

**Task**: `create-code-example.md`

**Input**: `section-1-plan.md` (code examples needed: 2-3)

**Process**:
1. Activate code-curator
2. Reference section-1-plan learning objectives
3. Create `list_basics.py` with 3 examples:
   - Example 1: Creating lists
   - Example 2: Accessing elements (indexing)
   - Example 3: Slicing lists
4. Create `test_list_basics.py` with unit tests
5. Verify tests pass

**Output**:
- `code/chapter-3/section-1/list_basics.py`
- `code/chapter-3/section-1/test_list_basics.py`

**Code example** (see actual files for full code):

```python
# list_basics.py
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "cherry"]
first_fruit = fruits[0]      # "apple"
last_fruit = fruits[-1]       # "cherry"
first_three = numbers[0:3]    # [1, 2, 3]
```

**What this looks like**:

```markdown
# Activate agent
/bmad-tw:agents:code-curator

# Request code examples
"Create code examples for Section 3.1 List Basics.
Need 3 examples: creating lists, accessing elements, slicing.
Include unit tests. All code must be working and tested."

# Agent creates code files
# Run: pytest code/chapter-3/section-1/test_list_basics.py
# All tests pass ✅
```

#### Step 5.1.B: Write Section Draft ⭐

**Time**: 1.5-2 hours

**Agent**: `tutorial-architect`

**Task**: `write-section-draft.md` ⭐ (Sprint 7 addition)

**Template**: `tutorial-section-tmpl.yaml`

**Input**: `section-1-plan.md` + `code/chapter-3/section-1/*.py`

**Process**:
1. Activate tutorial-architect
2. Execute write-section-draft.md task
3. Agent writes 3-4 page section following structure:
   - **Introduction**: What are lists, why they matter
   - **Concept explanation**: Lists are ordered, mutable collections
   - **Tutorial walkthrough**: Step-by-step list creation
   - **Code examples integrated**: Inline with explanations
   - **Practical applications**: When to use lists
   - **Transitions**: From Chapter 2, to Section 3.2

**Output**: `manuscript/sections/chapter-3/section-1-draft.md`

**Key content elements**:
- Clear learning objectives stated upfront
- Progressive complexity (simple → complex)
- Code examples explained line-by-line
- Common pitfalls highlighted
- Practice exercises suggested

**What this looks like**:

```markdown
# Activate agent
/bmad-tw:agents:tutorial-architect

# Request section draft
"Write draft for Section 3.1: List Basics using write-section-draft.md.
Use section-1-plan.md and integrate code from code/chapter-3/section-1/.
Target 3-4 pages. Follow tutorial-section-tmpl.yaml structure."

# Agent writes section-1-draft.md (3.5 pages)
```

#### Step 5.1.C: Technical Review with Checklist ⭐

**Time**: 20-30 minutes

**Agent**: `technical-reviewer`

**Task**: `execute-checklist.md` ⭐ (Sprint 7 addition)

**Checklist**: `technical-accuracy-checklist.md`

**Input**: `section-1-draft.md`

**Process**:
1. Activate technical-reviewer
2. Execute checklist for technical accuracy:
   - ✅ Code examples accurate and tested
   - ✅ Technical explanations correct
   - ✅ No misleading simplifications
   - ✅ Terminology consistent
   - ✅ Best practices followed
3. Generate review report

**Output**: `reviews/section-1-review-notes.md`

**Checklist results**: `checklists/section-1-checklist-results.md`

**Review findings** (example):
- ✅ All code examples tested and working
- ⚠️ Suggest adding note about negative indexing edge cases
- ✅ Terminology accurate
- ⚠️ Minor: inconsistent capitalization of "List" vs "list"

**What this looks like**:

```markdown
# Activate agent
/bmad-tw:agents:technical-reviewer

# Request technical review
"Review section-1-draft.md for technical accuracy.
Execute technical-accuracy-checklist.md.
Save results to checklists/section-1-checklist-results.md"

# Agent reviews and creates review notes
```

#### Step 5.1.D: Revise Section

**Time**: 30-45 minutes

**Agent**: `tutorial-architect`

**Input**: `section-1-draft.md` + `reviews/section-1-review-notes.md`

**Process**:
1. Reactivate tutorial-architect
2. Address review feedback:
   - Added note about negative indexing edge cases
   - Standardized "list" (lowercase) throughout
3. Update draft with revisions

**Output**: `section-1-draft.md` (updated)

#### Step 5.1.E: Finalize Section

**Time**: 10-15 minutes

**Agent**: `tutorial-architect`

**Process**:
1. Create final version: `section-1-final.md`
2. Mark section 1 as DONE in `section-list.md`
3. Section ready for chapter assembly

**Output**: `manuscript/sections/chapter-3/section-1-final.md`

**Section 1 complete!** (Total: ~3 hours)

---

### Section 2: List Operations

Same workflow as Section 1, key differences:

#### Step 5.2.A: Create Code Examples

**Code focus**: Mutating lists
- `list_operations.py`: modify, append, insert, remove, pop
- `test_list_operations.py`: full test coverage

#### Step 5.2.B: Write Section Draft ⭐

**Content focus**:
- Builds on Section 1 (references previous concepts)
- Shows transition from Section 1
- 3-4 code examples integrated
- Explains mutability in depth

**Output**: `section-2-draft.md` (4 pages)

#### Step 5.2.C-E: Review, Revise, Finalize

Same checklist process, produces:
- `reviews/section-2-review-notes.md`
- `checklists/section-2-checklist-results.md`
- `section-2-final.md`

**Section 2 complete!** (~3.5 hours)

---

### Section 3: Tuples and Immutability

Same workflow, key differences:

#### Step 5.3.A: Create Code Examples

**Code focus**: Tuples vs lists
- `tuples_demo.py`: Creating tuples, immutability, when to use
- `test_tuples_demo.py`: tests

#### Step 5.3.B: Write Section Draft ⭐

**Content focus**:
- Contrast pattern (tuples vs lists)
- When to use each
- Immutability explained
- Practical use cases (coordinates, RGB values)

**Output**: `section-3-draft.md` (3 pages)

#### Step 5.3.C-E: Review, Revise, Finalize

Produces:
- `reviews/section-3-review-notes.md`
- `checklists/section-3-checklist-results.md`
- `section-3-final.md`

**Section 3 complete!** (~3 hours)

---

**All 3 sections developed!** (Total: ~9-10 hours)

---

## Part 6: Chapter Assembly

Now we merge the 3 sections into a cohesive chapter.

**Total time**: 2-3 hours

### Step 6.1: Merge Sections ⭐

**Time**: 30-45 minutes

**Agent**: `tutorial-architect`

**Task**: `merge-sections.md` ⭐ (Sprint 7 addition - Story 7.10)

**Input**:
- `section-1-final.md`
- `section-2-final.md`
- `section-3-final.md`

**Process**:
1. Activate tutorial-architect
2. Execute merge-sections.md
3. Agent combines sections:
   - Add chapter introduction (overview, objectives, prerequisites)
   - Merge section content
   - Add chapter summary (recap, key takeaways, next chapter preview)
   - Standardize formatting, headings, terminology
   - Create unified chapter document

**Output**: `manuscript/chapters/chapter-3-integrated.md` (11-12 pages)

**What this looks like**:

```markdown
# Activate agent
/bmad-tw:agents:tutorial-architect

# Request merge
"Merge section-1-final, section-2-final, section-3-final into chapter.
Use merge-sections.md task.
Add chapter intro and summary.
Save as chapter-3-integrated.md"

# Agent creates integrated chapter
```

---

### Step 6.2: Enhance Transitions ⭐

**Time**: 30-45 minutes

**Agent**: `tutorial-architect`

**Task**: `enhance-transitions.md` ⭐ (Sprint 7 addition - Story 7.10)

**Input**: `chapter-3-integrated.md`

**Process**:
1. Identify section boundaries
2. Improve transitions between sections:
   - Section 1 → 2: "Now that you understand list basics, let's explore how to modify lists..."
   - Section 2 → 3: "Lists are powerful because they're mutable. But what if you need immutable sequences? Enter tuples..."
3. Add bridging paragraphs where needed
4. Ensure narrative flow throughout chapter

**Output**: `chapter-3-integrated.md` (updated with smooth transitions)

**What this looks like**:

```markdown
# Still in tutorial-architect

# Request transition enhancement
"Enhance transitions between sections in chapter-3-integrated.md.
Use enhance-transitions.md task.
Ensure smooth narrative flow section-to-section."

# Agent improves transitions
```

---

### Step 6.3: Validate Learning Flow ⭐

**Time**: 20-30 minutes

**Agent**: `instructional-designer`

**Task**: `validate-learning-flow.md` ⭐ (Sprint 7 - Story 7.4)

**Input**: `chapter-3-integrated.md`

**Process**:
1. Activate instructional-designer
2. Check learning progression:
   - ✅ Concepts build progressively
   - ✅ Prerequisites respected
   - ✅ Difficulty curve appropriate
   - ✅ Examples scaffold understanding
   - ✅ Practice opportunities present
3. Report findings

**Output**: Review notes (inline or separate)

**What this looks like**:

```markdown
# Activate agent
/bmad-tw:agents:instructional-designer

# Request validation
"Validate learning flow in chapter-3-integrated.md.
Check progression, scaffolding, difficulty curve.
Use validate-learning-flow.md task."

# Agent validates and suggests minor improvements
```

---

### Step 6.4: Technical Review of Chapter

**Time**: 30-45 minutes

**Agent**: `technical-reviewer`

**Task**: `technical-review-chapter.md`

**Checklist**: `technical-accuracy-checklist.md` (chapter-level)

**Input**: `chapter-3-integrated.md`

**Process**:
1. Activate technical-reviewer
2. Full chapter technical review:
   - Code accuracy across all sections
   - Technical consistency chapter-wide
   - No contradictions between sections
   - Best practices followed
   - Example quality
3. Create comprehensive review report

**Output**: `reviews/chapter-3-technical-review.md`

**Review findings** (example):
- ✅ All code tested and working
- ✅ Technical accuracy excellent
- ⚠️ Suggest adding chapter-level summary table comparing lists vs tuples
- ✅ Transitions between sections smooth
- ⚠️ Minor: Acronym "RGB" used but not defined (define on first use)

---

### Step 6.5: Revise Chapter Based on Review

**Time**: 20-30 minutes

**Agent**: `tutorial-architect`

**Input**: `chapter-3-integrated.md` + `reviews/chapter-3-technical-review.md`

**Process**:
1. Reactivate tutorial-architect
2. Address review feedback:
   - Added comparison table (lists vs tuples)
   - Defined RGB on first use
   - Minor clarifications
3. Update integrated chapter

**Output**: `chapter-3-integrated.md` (updated)

---

### Step 6.6: Copy Edit Chapter

**Time**: 30-45 minutes

**Agent**: `technical-editor`

**Task**: `copy-edit-chapter.md`

**Input**: `chapter-3-integrated.md`

**Process**:
1. Activate technical-editor
2. Polish prose:
   - Grammar, punctuation, spelling
   - Consistency (terminology, style, formatting)
   - Clarity (sentence structure, word choice)
   - Readability (paragraph flow, headings)
3. Maintain technical accuracy (no content changes)

**Output**: `chapter-3-integrated.md` (copy edited)

---

### Step 6.7: Final Quality Gate ⭐

**Time**: 15-20 minutes

**Agent**: `tutorial-architect`

**Task**: `execute-checklist.md` ⭐ (Sprint 7 addition)

**Checklist**: `chapter-completeness-checklist.md`

**Input**: `chapter-3-integrated.md`

**Process**:
1. Reactivate tutorial-architect
2. Execute chapter completeness checklist:
   - ✅ All learning objectives met
   - ✅ Code examples working and tested
   - ✅ Transitions smooth
   - ✅ Consistent terminology
   - ✅ Chapter intro and summary present
   - ✅ Appropriate length (11-12 pages)
   - ✅ Ready for publication

**Output**: `checklists/chapter-3-completeness-results.md`

---

### Step 6.8: Finalize Chapter

**Time**: 5-10 minutes

**Agent**: `tutorial-architect`

**Process**:
1. Create final chapter version
2. Mark chapter as complete

**Output**: `manuscript/chapters/chapter-3-final.md`

**Chapter complete!** 🎉

---

## Part 7: Key Takeaways

### What We Learned

1. **Section-driven workflow enables incremental progress**
   - Each section is 3-4 hours of manageable work
   - Can complete one section per day
   - Quality gates at section level prevent chapter-level rework

2. **Quality gates catch issues early**
   - Section reviews find problems before merge
   - Cheaper to fix issues in 3-page section than 12-page chapter
   - Multiple review layers ensure quality

3. **Sprint 7 tasks make workflow executable**
   - `write-section-draft.md` - Clear task for section writing
   - `execute-checklist.md` - Standardized quality gates
   - `merge-sections.md` - Structured chapter assembly
   - `enhance-transitions.md` - Explicit narrative flow improvement
   - `validate-learning-flow.md` - Instructional design validation

4. **Code examples are first-class citizens**
   - Created before writing (code-first approach)
   - Tested before integration
   - Explained in narrative context
   - Sample demonstrates tested, working code

5. **Workflow is repeatable and scalable**
   - Same process for sections 1, 2, 3
   - Can scale to 6-8 sections per chapter
   - Can apply to any technical topic

### Workflow Efficiency

**Time breakdown** (actual):
- Planning: 2-3 hours (book outline + chapter outline + section planning)
- Section development: 3-4 hours × 3 sections = 9-12 hours
- Chapter assembly: 2-3 hours
- **Total: 13-18 hours** for complete chapter

**Per section time**:
- Code examples: 30-45 min
- Writing draft: 1.5-2 hours
- Review: 20-30 min
- Revisions: 30-45 min
- Finalize: 10-15 min
- **Total: 3-4 hours per section**

### Quality Metrics

**Review layers**:
1. Section-level technical review (3×)
2. Chapter-level technical review (1×)
3. Copy editing (1×)
4. Checklist validations (4× - 3 sections + 1 chapter)

**Result**: High-quality, publication-ready content

---

## Part 8: Adaptations for Your Book

### For Your Topic

Replace Python content with your domain:
- **Web development**: Sections on HTML, CSS, JavaScript
- **Data science**: Sections on pandas, numpy, visualization
- **DevOps**: Sections on Docker, Kubernetes, CI/CD
- **Game development**: Sections on game loop, physics, rendering

**The workflow stays the same** - only content changes.

### Scaling to More Sections

**For 6-8 sections per chapter**:
- Continue section development loop
- Each section: 3-4 hours
- 8 sections = 24-32 hours of section development
- Chapter assembly time stays similar (2-3 hours)
- **Total**: ~30-40 hours per chapter

**Time management**:
- 1 section per day = 1 week for 6-section chapter
- 2 sections per day (if full-time) = 3-4 days

### When to Use Section-Driven vs Traditional

**Use section-driven when**:
- Chapter is 10+ pages
- Multiple distinct topics in chapter
- Want incremental progress and quality gates
- Working with multiple authors/reviewers
- Need to parallelize work

**Use traditional (write whole chapter) when**:
- Chapter is short (5-8 pages)
- Single cohesive topic
- Narrative flow is paramount
- Working solo with clear vision

### Publisher Integration

Most publishers accept section-driven workflow:
1. Deliver sections for early review
2. Assemble into chapters
3. Submit chapters to publisher
4. Publisher's copyediting happens after your assembly
5. Technical review can happen at section or chapter level (your choice)

**Deliverable**: `chapter-3-final.md` is ready for publisher submission

---

## Conclusion

You've seen the **complete section-driven development workflow** from book outline to final chapter.

**Next steps**:
1. Explore the sample files in this project
2. Run the code examples (`pytest` in code/chapter-3/*)
3. Read the final chapter (`manuscript/chapters/chapter-3-final.md`)
4. Use this structure as a template for your book project

**Ready to write your book?** Start with step 1 (book outline) and follow this walkthrough! 🚀

---

## Questions?

Join the BMAD community:
- Discord: https://discord.gg/gk8jAdXWmj
- GitHub: https://github.com/bmadcode/bmad-method
- Issues: https://github.com/bmadcode/bmad-method/issues
