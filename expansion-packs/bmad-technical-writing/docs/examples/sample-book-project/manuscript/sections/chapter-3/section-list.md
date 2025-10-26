# Chapter 3 Section Planning: Working with Lists and Tuples

<!-- Agent: tutorial-architect + instructional-designer -->
<!-- Workflow: section-planning-workflow.yaml -->
<!-- Input: manuscript/outlines/chapter-3-outline.md -->

## Section Planning Overview

**Chapter**: 3 - Working with Lists and Tuples
**Total sections planned**: 6
**Sections to develop**: 3 (sections 3.1, 3.2, 3.3)
**Sections planned only**: 3 (sections 3.4, 3.5, 3.6)
**Development approach**: Section-driven workflow

**Rationale for developing 3 sections**:

- Demonstrates complete workflow without overwhelming sample size
- Shows core concepts (create, modify, tuples) fully
- Leaves advanced topics (comprehensions, sorting) planned for scope management
- Keeps sample creation time reasonable (~12-16 hours total)

---

## Section 3.1: List Basics (Creating and Accessing Lists) ⭐

**Status**: ✅ DONE

**Learning objectives**:

1. Create lists using literal notation and list() constructor
2. Access list elements using positive and negative indexing
3. Use slicing to extract sublists
4. Understand and avoid common indexing errors

**Prerequisites**:

- Variables and assignment (Chapter 1)
- Basic data types (Chapter 2)
- For loops (Chapter 1)

**Content plan**:

1. **Concept**: What are lists (ordered, mutable collections)
2. **Tutorial**: Creating lists step-by-step
3. **Tutorial**: Accessing elements (indexing)
4. **Tutorial**: Slicing lists
5. **Practice**: Common patterns and pitfalls

**Code examples needed**:

- Example 1: Creating lists (literal notation, various types)
- Example 2: Accessing elements (positive/negative indexing)
- Example 3: Slicing (basic slices, stride, copy)

**Estimated pages**: 6-7 pages

**Transitions**:

- **From**: Chapter 2 (data types, mutability intro)
- **To**: Section 3.2 (now that you can create/access, learn to modify)

**Success criteria**:

- Readers can create lists of various data types
- Readers can access any element by index
- Readers understand slice notation
- Readers know common indexing mistakes to avoid

**Development notes**:

- Code created: ✅ `code/chapter-3/section-1/list_basics.py`
- Tests created: ✅ `code/chapter-3/section-1/test_list_basics.py`
- Draft written: ✅ `section-1-draft.md`
- Technical review: ✅ `reviews/section-1-review-notes.md`
- Checklist results: ✅ `checklists/section-1-checklist-results.md`
- Final version: ✅ `section-1-final.md`

---

## Section 3.2: List Operations (Modify, Add, Remove) ⭐

**Status**: ✅ DONE

**Learning objectives**:

1. Modify existing list elements by index
2. Add elements to lists using append, insert, extend
3. Remove elements using remove, pop, del, clear
4. Understand when to use each modification method

**Prerequisites**:

- Section 3.1 (must know how to create and access lists)
- Understanding of mutability (Chapter 2)

**Content plan**:

1. **Concept**: Lists are mutable (can be changed in place)
2. **Tutorial**: Modifying elements by assignment
3. **Tutorial**: Adding elements (append, insert, extend)
4. **Tutorial**: Removing elements (remove, pop, del, clear)
5. **Practice**: Choosing the right method for the task

**Code examples needed**:

- Example 1: Modifying list elements
- Example 2: Adding elements (append, insert, extend comparisons)
- Example 3: Removing elements (remove, pop, del comparisons)
- Example 4: List concatenation and repetition

**Estimated pages**: 7-8 pages

**Transitions**:

- **From**: Section 3.1 (you can access lists, now modify them)
- **To**: Section 3.3 (lists are mutable, but tuples are not...)

**Success criteria**:

- Readers can modify list elements confidently
- Readers know when to use append vs insert vs extend
- Readers understand remove vs pop vs del differences
- Readers appreciate list mutability

**Development notes**:

- Code created: ✅ `code/chapter-3/section-2/list_operations.py`
- Tests created: ✅ `code/chapter-3/section-2/test_list_operations.py`
- Draft written: ✅ `section-2-draft.md`
- Technical review: ✅ `reviews/section-2-review-notes.md`
- Checklist results: ✅ `checklists/section-2-checklist-results.md`
- Final version: ✅ `section-2-final.md`

---

## Section 3.3: Tuples and Immutability ⭐

**Status**: ✅ DONE

**Learning objectives**:

1. Create tuples using literal notation and tuple() constructor
2. Understand immutability and its implications
3. Distinguish when to use tuples vs lists
4. Use tuple unpacking for multiple assignment

**Prerequisites**:

- Section 3.1 and 3.2 (understand lists first for contrast)
- Mutability concept (Chapter 2)

**Content plan**:

1. **Concept**: What are tuples (ordered, immutable sequences)
2. **Contrast**: Tuples vs lists (similarities and differences)
3. **Tutorial**: Creating and accessing tuples
4. **Tutorial**: Why immutability matters
5. **Tutorial**: Tuple unpacking
6. **Practice**: Choosing lists vs tuples for different scenarios

**Code examples needed**:

- Example 1: Creating tuples
- Example 2: Attempting to modify tuple (shows TypeError)
- Example 3: Using tuples for fixed data (coordinates, RGB values)
- Example 4: Tuple unpacking

**Estimated pages**: 6-7 pages

**Transitions**:

- **From**: Section 3.2 (lists are mutable and powerful, but sometimes you need immutability)
- **To**: Section 3.4 (planned - now that you know lists/tuples, learn efficient creation with comprehensions)

**Success criteria**:

- Readers can create and use tuples
- Readers understand immutability constraints
- Readers can choose between lists and tuples appropriately
- Readers use tuple unpacking confidently

**Development notes**:

- Code created: ✅ `code/chapter-3/section-3/tuples_demo.py`
- Tests created: ✅ `code/chapter-3/section-3/test_tuples_demo.py`
- Draft written: ✅ `section-3-draft.md`
- Technical review: ✅ `reviews/section-3-review-notes.md`
- Checklist results: ✅ `checklists/section-3-checklist-results.md`
- Final version: ✅ `section-3-final.md`

---

## Section 3.4: List Comprehensions

**Status**: 📋 PLANNED (not developed in sample)

**Learning objectives**:

1. Write basic list comprehensions
2. Use conditionals in comprehensions
3. Understand when comprehensions improve code
4. Avoid overly complex comprehensions

**Prerequisites**:

- Section 3.1-3.3 (must understand lists thoroughly)
- For loops (Chapter 1)

**Content plan**:

1. **Concept**: What are comprehensions (concise way to create lists)
2. **Tutorial**: Basic comprehension syntax
3. **Tutorial**: Comprehensions with conditionals
4. **Tutorial**: Nested comprehensions
5. **Practice**: When to use comprehensions vs loops

**Code examples needed**:

- Example 1: Simple comprehension (squares of numbers)
- Example 2: Filtering with conditional
- Example 3: Nested list comprehension
- Example 4: Comprehension vs loop comparison

**Estimated pages**: 6-7 pages

**Transitions**:

- **From**: Section 3.3 (you can create lists manually, now learn efficient creation)
- **To**: Section 3.5 (you can create lists efficiently, now learn to organize them)

**Why not developed in sample**:

- Advanced topic (not essential for beginners)
- Sample focuses on core concepts (create, modify, tuples)
- Demonstrates planning vs execution scope management
- Keeps sample development time reasonable

---

## Section 3.5: Sorting and Searching

**Status**: 📋 PLANNED (not developed in sample)

**Learning objectives**:

1. Search for items in lists using in, index, count
2. Sort lists using sort() method and sorted() function
3. Use key parameter for custom sorting
4. Find min and max values in lists

**Prerequisites**:

- Section 3.1-3.2 (must understand list operations)
- Optional: Section 3.4 (comprehensions useful for examples)

**Content plan**:

1. **Concept**: Finding and organizing data in lists
2. **Tutorial**: Searching (in, index, count)
3. **Tutorial**: Sorting (sort vs sorted, reverse)
4. **Tutorial**: Custom sorting with key parameter
5. **Practice**: Common sorting/searching patterns

**Code examples needed**:

- Example 1: Searching with in and index
- Example 2: Basic sorting (numbers, strings)
- Example 3: Reverse sorting
- Example 4: Custom sort (by length, by attribute)

**Estimated pages**: 7-8 pages

**Transitions**:

- **From**: Section 3.4 (you can create lists, now organize them)
- **To**: Section 3.6 (you have all the tools, now see real applications)

**Why not developed in sample**:

- Builds on comprehensive list knowledge
- Sample demonstrates core workflows sufficiently with 3 sections
- Shows forward planning (section planned for future)

---

## Section 3.6: Practical Applications

**Status**: 📋 PLANNED (not developed in sample)

**Learning objectives**:

1. Apply lists to solve real programming problems
2. Combine multiple list operations effectively
3. Process collections of data
4. Write practical, useful code with lists and tuples

**Prerequisites**:

- Sections 3.1-3.5 (all previous section knowledge)
- Ability to read problem requirements and plan solution

**Content plan**:

1. **Application 1**: Todo list manager (add, remove, list todos)
2. **Application 2**: Grade calculator (input, process, analyze grades)
3. **Application 3**: Simple CSV data processor
4. **Practice**: Building complete programs with lists

**Code examples needed**:

- Example 1: Interactive todo list program
- Example 2: Grade calculator with statistics
- Example 3: Data processing script
- Example 4: Integration of comprehensions, sorting, searching

**Estimated pages**: 7-8 pages

**Transitions**:

- **From**: Section 3.5 (you have all the techniques)
- **To**: Chapter 4 (real programs often need key-value storage... dictionaries!)

**Why not developed in sample**:

- Final capstone section (depends on all previous)
- Sample demonstrates section workflow with 3 representative sections
- Practical applications require full chapter context (5-6 sections)
- Keeps sample focused on workflow demonstration

---

## Development Sequence

**Completed** (in sample):

1. ✅ Section 3.1: List Basics (code → draft → review → final)
2. ✅ Section 3.2: List Operations (code → draft → review → final)
3. ✅ Section 3.3: Tuples and Immutability (code → draft → review → final)
4. ✅ Chapter assembly (merge sections 1-3 → enhance transitions → review → edit → final)

**Planned** (not in sample): 5. 📋 Section 3.4: List Comprehensions 6. 📋 Section 3.5: Sorting and Searching 7. 📋 Section 3.6: Practical Applications 8. 📋 Full chapter assembly (all 6 sections)

---

## Workflow Artifacts Created

**Section 1**:

- `section-1-plan.md` (this file, Section 3.1 entry)
- `code/chapter-3/section-1/list_basics.py`
- `code/chapter-3/section-1/test_list_basics.py`
- `section-1-draft.md`
- `reviews/section-1-review-notes.md`
- `checklists/section-1-checklist-results.md`
- `section-1-final.md`

**Section 2**:

- `section-2-plan.md` (this file, Section 3.2 entry)
- `code/chapter-3/section-2/list_operations.py`
- `code/chapter-3/section-2/test_list_operations.py`
- `section-2-draft.md`
- `reviews/section-2-review-notes.md`
- `checklists/section-2-checklist-results.md`
- `section-2-final.md`

**Section 3**:

- `section-3-plan.md` (this file, Section 3.3 entry)
- `code/chapter-3/section-3/tuples_demo.py`
- `code/chapter-3/section-3/test_tuples_demo.py`
- `section-3-draft.md`
- `reviews/section-3-review-notes.md`
- `checklists/section-3-checklist-results.md`
- `section-3-final.md`

**Chapter assembly**:

- `manuscript/chapters/chapter-3-integrated.md` (merged sections)
- `reviews/chapter-3-technical-review.md`
- `checklists/chapter-3-completeness-results.md`
- `manuscript/chapters/chapter-3-final.md`

---

## Sprint 7 Tasks Used ⭐

This sample demonstrates these Sprint 7 additions in action:

1. **write-section-draft.md** ⭐
   - Used 3 times (sections 3.1, 3.2, 3.3)
   - Core task for section writing
   - Follows tutorial-section-tmpl.yaml structure

2. **execute-checklist.md** ⭐
   - Used 4 times (3 section reviews + 1 chapter review)
   - Quality gate execution
   - Standardized review process

3. **merge-sections.md** ⭐
   - Used once (chapter assembly)
   - Combines sections 1, 2, 3 into integrated chapter
   - Adds chapter intro and summary

4. **enhance-transitions.md** ⭐
   - Used once (after merge)
   - Improves section-to-section flow
   - Creates cohesive narrative

5. **validate-learning-flow.md** ⭐
   - Used once (chapter-level review)
   - Checks instructional design quality
   - Validates learning progression

---

## Time Investment Actual

**Planning** (this file + section plans): 2 hours

**Section development**:

- Section 3.1: 3.5 hours (code 45min, write 2hr, review 30min, revise 30min)
- Section 3.2: 3.5 hours (code 45min, write 2hr, review 30min, revise 30min)
- Section 3.3: 3 hours (code 30min, write 1.5hr, review 30min, revise 30min)
- **Total section development**: 10 hours

**Chapter assembly**: 2.5 hours

- Merge: 45min
- Enhance transitions: 45min
- Technical review: 45min
- Copy edit: 30min

**WALKTHROUGH.md creation**: 2.5 hours

**Total sample creation**: ~17 hours

---

## Key Learnings from Sample Development

1. **Section-driven workflow works**
   - Each section manageable (3-3.5 hours)
   - Quality gates at section level prevented chapter-level issues
   - Clear progress (3 sections complete, visible milestones)

2. **Code-first approach effective**
   - Writing code examples before prose helped structure content
   - Having tested code made writing easier (copy-paste into narrative)
   - Test-first mindset ensured examples work

3. **Sprint 7 tasks are valuable**
   - write-section-draft.md provided clear structure
   - execute-checklist.md standardized reviews
   - merge-sections.md and enhance-transitions.md made assembly systematic

4. **Scope management critical**
   - Developing 3 sections shows workflow fully
   - Planning 3 more demonstrates foresight without overcommitment
   - Sample stays manageable (~17 hours vs 30+ for 6 sections)

5. **Documentation as you go**
   - Creating WALKTHROUGH.md while building sample captured process accurately
   - Annotations in files help users understand workflow
   - Real-time notes more valuable than reconstructed later

---

_This section planning document was created using the tutorial-architect and instructional-designer agents following the section-planning-workflow.yaml as part of the BMAD Technical Writing Expansion Pack._
