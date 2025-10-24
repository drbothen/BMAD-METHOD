# Getting Started - Your First Technical Book Chapter

This hands-on tutorial walks you through creating your first technical book chapter using the BMad Technical Writing Expansion Pack. You'll go from concept to completed chapter in 2-3 hours.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Tutorial Overview](#tutorial-overview)
- [Step 1: Plan Your Book](#step-1-plan-your-book)
- [Step 2: Plan Your First Chapter](#step-2-plan-your-first-chapter)
- [Step 3: Write Your First Section](#step-3-write-your-first-section)
- [Step 4: Review Your Section](#step-4-review-your-section)
- [Step 5: Complete Remaining Sections](#step-5-complete-remaining-sections)
- [Step 6: Assemble Your Chapter](#step-6-assemble-your-chapter)
- [Step 7: Prepare for Publishing](#step-7-prepare-for-publishing)
- [Next Steps](#next-steps)

---

## Prerequisites

Before starting this tutorial, ensure you have:

- **BMad-Method installed** - Core framework must be installed
- **Technical Writing Expansion Pack installed** - This pack must be installed
- **AI interface ready** - Either:
  - Web UI (Gemini, ChatGPT, or Claude) for planning phase
  - IDE with AI (Cursor, VS Code, or Claude Code) for development phase
- **Basic markdown knowledge** - You should understand markdown formatting
- **Technical subject matter** - Know what you want to teach (we'll use Python as example)

**Installation Check**:

```bash
# Verify BMad is installed
npx bmad-method --version

# Verify Technical Writing pack is installed
ls ~/.bmad-method/expansion-packs/bmad-technical-writing
```

If not installed, run:

```bash
npx bmad-method install
# Select "Technical Book Writing Studio" from expansion packs
```

---

## Tutorial Overview

### What We'll Build

We'll create **Chapter 1** of "Python Data Structures Handbook" - an introductory chapter covering lists, tuples, and basic data manipulation.

**Chapter Title**: "Introduction to Python Data Structures"

**Chapter Content**:

- What are data structures and why they matter
- Introduction to lists with practical examples
- Introduction to tuples with practical examples
- When to use lists vs tuples
- Hands-on exercises with solutions

**Deliverables**:

- Complete chapter outline (6 sections)
- One fully written section (~3 pages)
- Working code examples
- Technical review notes
- Publisher-ready chapter draft

### Estimated Time

- **Planning** (30 min): Book outline + chapter structure
- **Section Writing** (45-60 min): Write one complete section
- **Review** (15 min): Technical review and revision
- **Assembly** (30 min): Complete chapter assembly
- **Total**: 2-3 hours

### What You'll Learn

By completing this tutorial, you'll understand:

- How to activate and use BMad agents
- How to execute workflows for book planning
- How to create sections using section-driven development
- How to review and revise technical content
- How to prepare chapters for publisher submission

Let's begin!

---

## Step 1: Plan Your Book

### Goal

Create a high-level book structure with learning objectives and chapter progression.

### Activate the Instructional Designer

**In Web UI (Gemini/ChatGPT/Claude)**:

1. Navigate to `dist/agents/`
2. Upload `instructional-designer.txt` to your chat interface
3. The agent will activate and greet you

**In IDE (Cursor/VS Code/Claude Code)**:

```
/bmad-tw:instructional-designer
```

The Instructional Designer will greet you and present available commands.

### Create Book Outline

**Command**:

```
*create-book-outline
```

The agent will execute the `design-book-outline` task using the `book-outline-tmpl` template.

**You'll be asked**:

- Book title
- Target audience
- Prerequisites
- Learning outcomes
- Chapter topics

**Example Inputs**:

> **Book Title**: Python Data Structures Handbook
>
> **Target Audience**: Beginner to intermediate Python developers who understand basic Python syntax
>
> **Prerequisites**:
>
> - Basic Python syntax (variables, functions, loops)
> - Understanding of types (int, str, bool)
> - Python 3.10+ installed
>
> **Learning Outcomes**:
>
> - Master Python's core data structures (lists, tuples, sets, dicts)
> - Choose appropriate data structures for different scenarios
> - Implement efficient data manipulation algorithms
> - Understand time/space complexity trade-offs
>
> **Chapters** (10 chapters):
>
> 1. Introduction to Python Data Structures
> 2. Lists and List Operations
> 3. Tuples and Immutability
> 4. Dictionaries and Hash Tables
> 5. Sets and Set Operations
> 6. Advanced List Techniques
> 7. Advanced Dictionary Techniques
> 8. Data Structure Performance
> 9. Choosing the Right Data Structure
> 10. Real-World Applications

**Output**: `book-outline.md`

The agent generates a complete book outline with:

- Chapter descriptions
- Learning objectives per chapter
- Prerequisite mapping
- Estimated page counts
- Difficulty progression

**Sample Output Section**:

```markdown
## Chapter 1: Introduction to Python Data Structures

**Learning Objectives**:

- Understand what data structures are and why they matter
- Recognize different data structure categories
- Implement basic list and tuple operations
- Choose between lists and tuples appropriately

**Prerequisites**: Basic Python syntax, variables, functions

**Estimated Length**: 18-22 pages

**Topics**:

- Data structures overview
- Introduction to sequences (lists, tuples)
- List creation and basic operations
- Tuple creation and immutability
- Lists vs tuples decision criteria
```

### Validate Learning Progression

**Command**:

```
*execute-checklist learning-objectives-checklist
```

The agent reviews your book outline against pedagogical best practices:

- ✅ Learning objectives are measurable
- ✅ Progression follows Bloom's taxonomy
- ✅ Prerequisites are clearly stated
- ✅ Difficulty curve is appropriate

**Result**: Validated book outline ready for chapter development.

---

## Step 2: Plan Your First Chapter

### Goal

Break Chapter 1 into manageable sections with detailed structure.

### Create Chapter Outline

**Still with Instructional Designer, command**:

```
*create-chapter-outline
```

**You'll specify**:

- Chapter number (1)
- Chapter title
- Section breakdown
- Code examples needed

**Example Section Breakdown** (6 sections):

**Section 1.1: Why Data Structures Matter** (3 pages)

- Real-world analogy (organizing a library)
- Performance implications
- Common pitfalls of wrong choices

**Section 1.2: Introduction to Lists** (4 pages)

- List creation syntax
- Basic list operations (append, insert, remove)
- List indexing and slicing
- Hands-on example: Building a task list

**Section 1.3: List Methods and Iteration** (3 pages)

- Common list methods (sort, reverse, count)
- Iterating with for loops
- List comprehensions preview
- Hands-on example: Processing student grades

**Section 1.4: Introduction to Tuples** (3 pages)

- Tuple creation and syntax
- Immutability explained
- Tuple unpacking
- Hands-on example: Coordinate systems

**Section 1.5: Lists vs Tuples Decision Guide** (3 pages)

- When to use lists (mutable collections)
- When to use tuples (immutable records)
- Performance considerations
- Best practices

**Section 1.6: Practice Exercises** (3 pages)

- 5 progressive exercises
- Solutions with explanations

**Output**: `chapter-01-outline.md`

### Switch to Tutorial Architect

Now activate the Tutorial Architect for hands-on section writing:

**In IDE**:

```
/bmad-tw:tutorial-architect
```

---

## Step 3: Write Your First Section

### Goal

Write one complete section (Section 1.2: Introduction to Lists) with code examples and tutorial content.

### Activate Code Curator

First, we need working code examples. Activate Code Curator:

**In IDE**:

```
/bmad-tw:code-curator
```

### Create Code Examples

**Command**:

```
*create-code-example
```

**Specify**:

- Section: 1.2 - Introduction to Lists
- Example title: "Building a Task List Application"
- Concepts to demonstrate: List creation, append, remove, indexing

**Code Curator Creates**:

`examples/chapter-01/task_list.py`:

```python
# Task List Application - Introduction to Lists

def main():
    """Demonstrate basic list operations through a task list app."""

    # Create an empty list
    tasks = []
    print(f"Starting tasks: {tasks}")

    # Add tasks using append
    tasks.append("Write chapter outline")
    tasks.append("Create code examples")
    tasks.append("Review draft")
    print(f"After adding tasks: {tasks}")

    # Access tasks by index
    first_task = tasks[0]
    print(f"First task: {first_task}")

    # Add task at specific position
    tasks.insert(1, "Write section 1")
    print(f"After inserting: {tasks}")

    # Remove completed task
    tasks.remove("Write chapter outline")
    print(f"After completing first task: {tasks}")

    # Check remaining tasks
    print(f"Total remaining tasks: {len(tasks)}")

    # Iterate through tasks
    print("\nRemaining tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

if __name__ == "__main__":
    main()
```

`examples/chapter-01/test_task_list.py`:

```python
import pytest
from task_list import main

def test_list_creation():
    """Test that lists can be created and modified."""
    tasks = []
    assert tasks == []

    tasks.append("test task")
    assert len(tasks) == 1
    assert tasks[0] == "test task"

def test_list_operations():
    """Test insert and remove operations."""
    tasks = ["first", "second"]
    tasks.insert(1, "middle")
    assert tasks == ["first", "middle", "second"]

    tasks.remove("middle")
    assert tasks == ["first", "second"]
```

**Command**:

```
*test-code-examples
```

Code Curator runs tests:

```
pytest examples/chapter-01/test_task_list.py -v
================================ test session starts ================================
examples/chapter-01/test_task_list.py::test_list_creation PASSED                [ 50%]
examples/chapter-01/test_task_list.py::test_list_operations PASSED              [100%]
================================ 2 passed in 0.03s ==================================
✅ All tests passed
```

### Write Section Content

**Reactivate Tutorial Architect**, command:

```
*create-tutorial
```

**Specify**:

- Section: 1.2 - Introduction to Lists
- Use code example: `task_list.py`
- Include: explanation, tutorial, troubleshooting

**Tutorial Architect Writes**:

`sections/section-1.2-introduction-to-lists.md`:

````markdown
# Section 1.2: Introduction to Lists

## What You'll Learn

By the end of this section, you'll be able to:

- Create lists in Python
- Add items to lists using `append()` and `insert()`
- Remove items from lists
- Access list items by index
- Iterate through lists

**Prerequisites**: Basic Python syntax, understanding of variables

**Estimated Time**: 20-30 minutes

---

## What are Lists?

Lists are Python's most versatile data structure. Think of a list as a container that holds multiple items in a specific order, like a to-do list or a shopping list.

**Key characteristics**:

- **Ordered** - Items maintain their position
- **Mutable** - You can add, remove, or change items
- **Allow duplicates** - The same item can appear multiple times
- **Dynamic size** - Lists grow and shrink automatically

---

## Creating Lists

Lists are created using square brackets `[]`:

```python
# Empty list
tasks = []

# List with initial items
numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Charlie"]
mixed = [1, "hello", 3.14, True]  # Lists can hold different types
```
````

---

## Hands-On Tutorial: Building a Task List

Let's build a simple task list application to learn list operations.

### Step 1: Create an Empty List

```python
tasks = []
print(f"Starting tasks: {tasks}")
# Output: Starting tasks: []
```

### Step 2: Add Tasks with append()

The `append()` method adds an item to the end of the list:

```python
tasks.append("Write chapter outline")
tasks.append("Create code examples")
tasks.append("Review draft")
print(f"After adding tasks: {tasks}")
# Output: After adding tasks: ['Write chapter outline', 'Create code examples', 'Review draft']
```

### Step 3: Access Items by Index

Lists use zero-based indexing. The first item is at index 0:

```python
first_task = tasks[0]
print(f"First task: {first_task}")
# Output: First task: Write chapter outline
```

### Step 4: Insert Tasks at Specific Position

Use `insert(position, item)` to add an item at a specific index:

```python
tasks.insert(1, "Write section 1")
print(f"After inserting: {tasks}")
# Output: After inserting: ['Write chapter outline', 'Write section 1', 'Create code examples', 'Review draft']
```

### Step 5: Remove Completed Tasks

Use `remove(item)` to delete an item by value:

```python
tasks.remove("Write chapter outline")
print(f"After completing first task: {tasks}")
# Output: After completing first task: ['Write section 1', 'Create code examples', 'Review draft']
```

### Step 6: Iterate Through Tasks

Loop through list items with a for loop:

```python
print("\nRemaining tasks:")
for i, task in enumerate(tasks, 1):
    print(f"{i}. {task}")

# Output:
# Remaining tasks:
# 1. Write section 1
# 2. Create code examples
# 3. Review draft
```

---

## Expected Output

When you run the complete example:

```
python examples/chapter-01/task_list.py
```

You should see:

```
Starting tasks: []
After adding tasks: ['Write chapter outline', 'Create code examples', 'Review draft']
First task: Write chapter outline
After inserting: ['Write chapter outline', 'Write section 1', 'Create code examples', 'Review draft']
After completing first task: ['Write section 1', 'Create code examples', 'Review draft']
Total remaining tasks: 3

Remaining tasks:
1. Write section 1
2. Create code examples
3. Review draft
```

---

## Common Issues and Troubleshooting

### Issue: IndexError: list index out of range

**Cause**: Trying to access an index that doesn't exist

```python
tasks = ["task 1", "task 2"]
print(tasks[5])  # Error! Only indices 0 and 1 exist
```

**Solution**: Check list length before accessing:

```python
if len(tasks) > 5:
    print(tasks[5])
else:
    print("Index out of range")
```

### Issue: ValueError: list.remove(x): x not in list

**Cause**: Trying to remove an item that doesn't exist

**Solution**: Check if item exists first:

```python
if "task" in tasks:
    tasks.remove("task")
```

---

## Key Takeaways

- Lists are created with square brackets: `[]`
- `append(item)` adds to the end
- `insert(index, item)` adds at a specific position
- `remove(item)` deletes the first occurrence
- Lists use zero-based indexing: `tasks[0]` is the first item
- `len(list)` returns the number of items

---

## Practice Exercise

Create a shopping list application that:

1. Creates an empty list
2. Adds 5 items
3. Removes 1 item
4. Prints the final list

Try it yourself before checking the solution!

**Solution**:

```python
shopping = []
shopping.append("apples")
shopping.append("bread")
shopping.append("milk")
shopping.append("eggs")
shopping.append("cheese")
shopping.remove("milk")
print(f"Shopping list: {shopping}")
```

---

**Next**: Section 1.3 - List Methods and Iteration

```

**Output**: Complete section (~3 pages) with tutorial, code, and exercises.

---

## Step 4: Review Your Section

### Goal
Ensure technical accuracy and quality before moving forward.

### Activate Technical Reviewer

**In IDE**:
```

/bmad-tw:technical-reviewer

```

### Run Technical Review

**Command**:
```

\*review-section sections/section-1.2-introduction-to-lists.md

````

**Technical Reviewer checks**:
- ✅ Code examples are correct
- ✅ Security best practices followed
- ✅ Performance considerations noted
- ✅ Error handling appropriate
- ✅ Python version compatibility (3.10+)

**Review Output**: `reviews/section-1.2-review.md`

```markdown
# Technical Review: Section 1.2

## Overall Assessment: APPROVED ✅

## Code Accuracy: ✅ PASS
- All code examples tested and working
- Syntax is correct for Python 3.10+
- Examples demonstrate concepts clearly

## Security: ✅ PASS
- No security vulnerabilities
- Examples use safe practices

## Best Practices: ✅ PASS
- Follows PEP 8 style guidelines
- Proper error handling demonstrated
- Good variable naming

## Minor Suggestions:
1. Consider adding example with list slicing
2. Could mention list() constructor as alternative

## Recommendation: READY FOR PUBLICATION
````

### Apply Review Feedback (Optional)

**Tutorial Architect adds slicing example**:

```python
# List slicing
first_two = tasks[:2]
print(f"First two tasks: {first_two}")
```

**Section updated and marked complete** ✅

---

## Step 5: Complete Remaining Sections

### Repeat Process for All Sections

You've now completed Section 1.2. Repeat Steps 3-4 for remaining sections:

- **Section 1.1**: Why Data Structures Matter ⏳
- **Section 1.2**: Introduction to Lists ✅
- **Section 1.3**: List Methods and Iteration ⏳
- **Section 1.4**: Introduction to Tuples ⏳
- **Section 1.5**: Lists vs Tuples Decision Guide ⏳
- **Section 1.6**: Practice Exercises ⏳

### Track Progress

As you complete sections, you'll have:

```
sections/
├── section-1.1-why-data-structures-matter.md ⏳
├── section-1.2-introduction-to-lists.md ✅
├── section-1.3-list-methods-iteration.md ⏳
├── section-1.4-introduction-to-tuples.md ⏳
├── section-1.5-lists-vs-tuples.md ⏳
└── section-1.6-practice-exercises.md ⏳
```

### Parallel Development (Optional)

You can work on multiple sections simultaneously by:

- Writing Section 1.3 while Section 1.2 is in review
- Having Code Curator create all code examples first
- Batch reviewing multiple sections

---

## Step 6: Assemble Your Chapter

### Goal

Merge all sections into a cohesive chapter with smooth transitions.

### Activate Technical Editor

**In IDE**:

```
/bmad-tw:technical-editor
```

### Run Chapter Assembly Workflow

**Command**:

```
*assemble-chapter
```

**Specify**:

- Chapter number: 1
- Sections to merge: All 6 sections
- Output file: `chapters/chapter-01-introduction.md`

**Technical Editor**:

1. Merges all sections in order
2. Adds smooth transitions between sections
3. Creates chapter introduction
4. Writes chapter summary
5. Ensures consistent style and tone
6. Validates cross-references
7. Runs checklists

**Output**: `chapters/chapter-01-introduction.md` (complete ~20-page chapter)

### Validate Chapter

**Command**:

```
*execute-checklist chapter-completeness-checklist
```

**Checks**:

- ✅ All sections present
- ✅ Introduction sets expectations
- ✅ Summary recaps key points
- ✅ Code examples work
- ✅ Exercises included
- ✅ Cross-references valid
- ✅ Consistent formatting

**Result**: Publisher-ready Chapter 1 ✅

---

## Step 7: Prepare for Publishing

### Goal

Package chapter for publisher submission (e.g., PacktPub).

### Activate Book Publisher

**In IDE**:

```
/bmad-tw:book-publisher
```

### Choose Publisher Workflow

**Command** (for PacktPub):

```
*run-workflow packtpub-submission
```

**Book Publisher**:

1. Formats chapter to PacktPub standards
2. Generates submission checklist
3. Packages code examples
4. Creates chapter metadata
5. Prepares submission folder

**Output**:

```
submission/
├── chapter-01-introduction.docx
├── chapter-01-metadata.yaml
├── code-examples/
│   ├── task_list.py
│   ├── test_task_list.py
│   └── README.md
└── submission-checklist.md
```

### Final Validation

**Command**:

```
*execute-checklist packtpub-submission-checklist
```

**Validates**:

- ✅ Chapter formatted correctly
- ✅ Code examples packaged
- ✅ Tests pass
- ✅ Metadata complete
- ✅ Word count within range (18-22 pages)
- ✅ All images/diagrams included
- ✅ Submission guidelines met

**Result**: Ready for publisher submission! 🎉

---

## Next Steps

Congratulations! You've completed your first technical book chapter using BMad.

### Continue Your Book

**Option 1: Write Chapter 2**

```
*create-chapter-outline
# Chapter 2: Lists and List Operations
```

**Option 2: Add More Sections to Chapter 1**

```
*create-section
# Add advanced list topics
```

### Explore More Features

**Try Different Workflows**:

- `tutorial-creation-workflow` - Create hands-on tutorials
- `code-example-workflow` - Focus on code-heavy chapters
- `technical-review-workflow` - Deep technical review

**Use Specialist Agents**:

- `api-documenter` - Create API reference chapters
- `screenshot-specialist` - Add visual documentation
- `exercise-creator` - Design comprehensive exercise sets

### Learn Advanced Topics

**Read More Documentation**:

- [Process Flows](process-flows.md) - Visualize all workflows
- [Agent Reference](agent-reference.md) - Master all 13 agents
- [Workflow Guide](workflow-guide.md) - Choose optimal workflows
- [Template Gallery](template-gallery.md) - Customize templates

### Join the Community

- **Discord**: [Join BMad Community](https://discord.gg/gk8jAdXWmj)
- **GitHub**: [Star the repo](https://github.com/bmadcode/bmad-method)
- **Share**: Show us what you're building!

---

## Tutorial Summary

You learned how to:

✅ Plan a complete book with learning objectives
✅ Break chapters into manageable sections
✅ Write tutorial content with hands-on examples
✅ Create and test working code examples
✅ Review content for technical accuracy
✅ Assemble sections into complete chapters
✅ Prepare chapters for publisher submission

**Time Investment**: 2-3 hours
**Output**: 1 publisher-ready chapter (20 pages)
**Skills Gained**: Complete technical book authoring workflow

---

## Questions or Issues?

- 📖 [User Guide](user-guide.md) - Conceptual overview
- 📋 [Quick Reference](quick-reference.md) - Command cheat sheet
- ❓ [FAQ](faq.md) - Common questions
- 🐛 [Troubleshooting](troubleshooting.md) - Common issues
- 💬 [Discord](https://discord.gg/gk8jAdXWmj) - Get help

**Ready to master technical book writing? Keep going!**

---

_Getting Started Tutorial - Technical Writing Expansion Pack v1.1.0_
