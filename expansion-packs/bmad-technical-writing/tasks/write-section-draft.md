<!-- Powered by BMAD™ Core -->

# Write Section Draft

---

task:
id: write-section-draft
name: Write Section Draft
description: Transform section plan and code examples into complete 2-5 page pedagogically sound section content
persona_default: tutorial-architect
inputs:
  - section-plan.md (learning objectives, prerequisites, content plan)
  - section-code-examples/ (tested code with outputs)
  - chapter-outline.md (chapter context and positioning)
steps:
  - Review section plan learning objectives and content plan
  - Study tested code examples and expected outputs
  - Understand section positioning in chapter flow
  - Write concept introduction (what and why)
  - Write concept explanation (background and theory)
  - Write tutorial walkthrough with code examples inline
  - Add practical applications and best practices
  - Create transitions (from previous, to next section)
  - Verify learning objectives addressed
  - Check length (2-5 pages) and pedagogical quality
  - Reference tutorial-section-tmpl.yaml for structure guidance
output: manuscript/sections/chapter-{{chapter_number}}/section-{{section_number}}-draft.md

---

## Purpose

This task guides you through writing a complete section draft (2-5 pages) that transforms your section plan and developed code examples into pedagogically sound instructional content. This is the core writing task in the section-driven development workflow, enabling incremental chapter development.

## Prerequisites

Before starting this task:

- **Section plan completed** - Contains learning objectives, prerequisites, content plan
- **Code examples developed and tested** - All code working with documented outputs
- **Chapter outline available** - Understand how this section fits the chapter
- **Access to tutorial-section-tmpl.yaml** - Structure and format guidance
- **Previous section complete** (if not first) - For transition references

## Workflow Steps

### 1. Review and Prepare

Read all inputs thoroughly before writing:

**Read Section Plan:**

- Learning objectives (1-2 max for a section)
- Prerequisites and dependencies
- Content plan (concepts to cover)
- Code examples needed
- Target length (2-5 pages)
- Success criteria

**Study Code Examples:**

- Review all code files in section-code-examples/
- Understand what each example demonstrates
- Note expected inputs and outputs
- Identify key concepts each example teaches
- Check test results and validation

**Understand Chapter Context:**

- Read chapter outline to see section positioning
- Note what previous sections covered
- Preview what next section will cover
- Understand overall chapter learning arc
- Check chapter-level prerequisites

**Mental Model Check:**
Can you explain:

- What this section teaches?
- Why it matters to readers?
- How code examples demonstrate concepts?
- How this connects to previous/next sections?

### 2. Write Concept Introduction

Start with a clear introduction (0.5-1 page):

**What is Being Taught:**

- Name the concept or skill clearly
- Provide a one-sentence definition
- Use an analogy or real-world comparison if helpful

**Example:**

```markdown
## List Comprehensions

List comprehensions provide a concise way to create lists in Python. Think of them as
a shorthand for writing for-loops that build lists—like using a template to generate
multiple items at once instead of creating each one individually.
```

**Why It Matters:**

- Real-world use cases
- Problems this concept solves
- Benefits over alternative approaches
- When to use this technique

**Example:**

```markdown
List comprehensions make your code more readable and often faster than equivalent
for-loops. They're the Pythonic way to transform, filter, and create lists, and you'll
see them throughout professional Python codebases. Understanding list comprehensions
is essential for reading others' code and writing clean, idiomatic Python.
```

**Where It Fits:**

- Connection to chapter theme
- Builds on previous sections
- Foundation for upcoming sections

**Length:** 0.5-1 page maximum

### 3. Write Concept Explanation

Provide necessary background and theory (0.5-1 page):

**Theoretical Foundation:**

- Key terminology and definitions
- Underlying principles or mechanisms
- Important constraints or rules
- Common misconceptions to address

**Example:**

```markdown
### List Comprehension Syntax

The basic syntax follows this pattern:

[expression for item in iterable if condition]

- **expression**: What to include in the new list
- **item**: Variable representing each element
- **iterable**: The source collection
- **condition**: Optional filter (if clause)

The comprehension evaluates left to right, filtering first, then applying the expression.
```

**Conceptual Understanding:**

- How it works internally (at appropriate depth)
- Mental model for reasoning about it
- Relationship to related concepts

**Keep Theory Practical:**

- Don't overwhelm with academic details
- Focus on what helps understanding
- Connect theory to hands-on practice
- Use diagrams if complex relationships exist

**Length:** 0.5-1 page maximum

### 4. Write Tutorial Walkthrough

Create step-by-step hands-on instructions (2-3 pages):

This is the **core content** of your section—the hands-on learning experience.

**Progressive Building Pattern:**

**Step 1: Start Simple**

- Introduce the most basic use case
- Show complete, working code
- Explain each part of the syntax
- Demonstrate the output

**Example:**

````markdown
### Creating a Basic List Comprehension

Let's start with the simplest case: creating a list of numbers.

**Traditional approach:**

```python
numbers = []
for i in range(5):
    numbers.append(i * 2)
print(numbers)  # Output: [0, 2, 4, 6, 8]
```
````

**List comprehension approach:**

```python
numbers = [i * 2 for i in range(5)]
print(numbers)  # Output: [0, 2, 4, 6, 8]
```

This comprehension reads naturally: "for each `i` in range(5), multiply by 2 and include
in the list." The result is identical, but the comprehension is more concise and expresses
the intent directly.

**When you run this code:**

```python
numbers = [i * 2 for i in range(5)]
print(numbers)
```

**You'll see:**

```
[0, 2, 4, 6, 8]
```

````

**Step 2-N: Build Complexity Gradually**
For each subsequent step:

1. **Introduce the code** - Show what to write
2. **Explain the code** - What each part does (not every line, focus on key concepts)
3. **Show the output** - Expected results when run
4. **Explain why** - What concept this demonstrates

**Code Integration Guidelines:**

**Complete, Runnable Code:**
```python
# Include imports
from typing import List

# Show complete context
def filter_even_numbers(numbers: List[int]) -> List[int]:
    return [n for n in numbers if n % 2 == 0]

# Demonstrate usage
result = filter_even_numbers([1, 2, 3, 4, 5])
print(result)  # Output: [2, 4]
````

**Inline Explanation (not separate comments):**

```markdown
This function uses a list comprehension with a conditional. The `if n % 2 == 0` clause
filters the list, keeping only even numbers. The modulo operator `%` returns the
remainder after division—even numbers have no remainder when divided by 2.
```

**Expected Outputs:**
Always show what happens when code runs:

````markdown
**Running this code:**

```python
cities = ['New York', 'London', 'Tokyo', 'Paris']
lengths = [len(city) for city in cities]
print(lengths)
```
````

**Produces:**

```
[8, 6, 5, 5]
```

Each number represents the length of the corresponding city name.

````

**Progressive Difficulty:**
- Basic: Simple transformation
- Intermediate: Add filtering with conditions
- Advanced: Nested comprehensions or combinations

**Number of Steps:**
- 3-5 examples typical for a section
- Each example builds on previous understanding
- Final example shows realistic usage

**What to Explain vs. Assume:**
- **Explain:** New syntax, concepts, patterns being taught
- **Assume:** Prerequisites from section plan
- **Briefly reference:** Related concepts not central to this section
- **Link for depth:** Point to other resources for tangential topics

**Length:** 2-3 pages (this is the bulk of your section)

### 5. Add Practical Applications

Show real-world use cases (0.5-1 page):

**Real-World Scenarios:**
```markdown
### Practical Applications

List comprehensions are particularly useful in data processing scenarios.

**Processing User Data:**
```python
users = [
    {'name': 'Alice', 'active': True, 'age': 30},
    {'name': 'Bob', 'active': False, 'age': 25},
    {'name': 'Charlie', 'active': True, 'age': 35}
]

# Extract names of active users
active_names = [user['name'] for user in users if user['active']]
print(active_names)  # Output: ['Alice', 'Charlie']
````

This pattern appears frequently in web applications—filtering and transforming datasets
based on criteria.

````

**Best Practices:**
- When to use this technique
- When NOT to use it (alternatives)
- Performance considerations
- Code readability guidelines

**Example:**
```markdown
### Best Practices

**Do use comprehensions when:**
- Transforming one list into another
- Filtering is simple (one condition)
- Improves readability over a for-loop

**Avoid comprehensions when:**
- Logic is complex (use regular for-loop for clarity)
- Multiple operations needed (side effects don't work well)
- Nested comprehensions become hard to read (2 levels max)
````

**Common Mistakes to Avoid:**

````markdown
### Common Pitfalls

**❌ Too complex:**

```python
# Hard to read - use a for-loop instead
result = [x*y for x in range(10) if x % 2 == 0 for y in range(10) if y % 3 == 0]
```
````

**✅ Better:**

```python
# More readable
result = []
for x in range(10):
    if x % 2 == 0:
        for y in range(10):
            if y % 3 == 0:
                result.append(x * y)
```

````

**Tips and Tricks:**
- Performance optimizations
- IDE shortcuts or helpers
- Debugging techniques
- Testing approaches

**Length:** 0.5-1 page

### 6. Create Transitions

Connect to previous and next sections (2-3 sentences each):

**Reference to Prerequisites:**
```markdown
This section assumes you're comfortable with Python for-loops and basic list operations
from Section 2.1.
````

**Connection to Previous Section:**

```markdown
In the previous section, we learned how to iterate through lists using for-loops. List
comprehensions provide a more concise syntax for the common pattern of building new lists
from existing ones.
```

**Preview of Next Section:**

```markdown
Now that you can create lists efficiently with comprehensions, in the next section we'll
explore dictionary and set comprehensions, applying the same patterns to other data structures.
```

**Placement:**

- Prerequisites: Early in introduction
- Previous section: End of introduction or start of concept explanation
- Next section: End of practical applications or conclusion

**Tone:**

- Natural, conversational
- Shows logical progression
- Reinforces learning arc
- Creates narrative flow

### 7. Verify Learning Objectives Addressed

Check each objective is taught and practiced:

**For Each Learning Objective:**

1. **Where is it taught?** - Which step/paragraph explains the concept
2. **Where is it practiced?** - Which code example demonstrates it
3. **Can readers verify?** - Is there a clear success indicator

**Example Check:**

```
Learning Objective: "Implement list comprehensions to transform and filter data"

✓ Taught: Section 3 explains list comprehension syntax and filtering with conditions
✓ Practiced: Steps 2-4 show transformation, Step 5 shows filtering, Step 6 combines both
✓ Verifiable: Code examples run successfully and produce expected outputs
```

**If Objective Not Met:**

- Add missing explanation
- Add missing code example
- Add verification step
- OR revise objective to match actual content

### 8. Check Length and Quality

Validate section meets standards:

**Length Check:**

- Count pages (2-5 pages target)
- If too short: Missing depth, examples, or practical applications?
- If too long: Too much theory? Should split into two sections?

**Quality Standards:**

**Pedagogical Quality:**

- [ ] Clear learning objectives addressed
- [ ] Concept explained before practice
- [ ] Progressive difficulty in examples
- [ ] Code examples are complete and runnable
- [ ] Expected outputs documented
- [ ] Real-world applications shown
- [ ] Common mistakes addressed

**Technical Quality:**

- [ ] All code tested and working
- [ ] Code follows best practices
- [ ] Terminology used consistently
- [ ] Prerequisites explicitly stated
- [ ] Transitions present

**Writing Quality:**

- [ ] Clear, concise language
- [ ] Active voice predominates
- [ ] Imperative instructions ("Create...", "Add...")
- [ ] Appropriate tone for audience
- [ ] No unnecessary jargon
- [ ] Technical terms defined

**Structure Quality:**

- [ ] Logical flow: concept → tutorial → applications
- [ ] Sections clearly delineated
- [ ] Code formatted with language tags
- [ ] Outputs distinguished from code

### 9. Use tutorial-section-tmpl.yaml (If Helpful)

Reference the template for structure guidance:

**When to Use Template:**

- First time writing sections (learn the pattern)
- Complex sections with many parts
- Want structured elicitation of content
- Collaborating with create-doc.md task

**When Workflow Is Sufficient:**

- Experienced with section writing
- Section follows standard pattern
- Direct writing is faster than template

**Template Provides:**

- Structured prompts for each part
- Consistent section organization
- Reminder of all components
- Quality checklist built-in

**To Use Template:**

```bash
# Execute create-doc task with tutorial-section template
Use create-doc.md with:
- template: tutorial-section-tmpl.yaml
- inputs: section plan, code examples, chapter outline
- output: section-{{section_number}}-draft.md
```

### 10. Final Review

Complete these checks before marking section complete:

**Content Completeness:**

- [ ] All input artifacts reviewed (section plan, code, outline)
- [ ] Concept introduction present (what, why, where it fits)
- [ ] Concept explanation present (theory, background)
- [ ] Tutorial walkthrough complete (2-3 pages of hands-on)
- [ ] Code examples integrated inline with explanations
- [ ] Expected outputs documented
- [ ] Practical applications shown
- [ ] Best practices included
- [ ] Common mistakes addressed
- [ ] Transitions present (previous and next)

**Learning Validation:**

- [ ] Each learning objective addressed
- [ ] Progressive difficulty maintained
- [ ] Hands-on practice provided
- [ ] Success criteria clear

**Technical Validation:**

- [ ] All code tested and working
- [ ] Outputs match documentation
- [ ] Prerequisites accurate
- [ ] References correct

**Length and Style:**

- [ ] 2-5 pages (not too short, not too long)
- [ ] Consistent terminology
- [ ] Active, engaging tone
- [ ] Clear, concise language

**Ready for Review:**

- [ ] Section saved to manuscript/sections/chapter-{{chapter_number}}/
- [ ] Filename: section-{{section_number}}-draft.md
- [ ] Ready for technical review

## Output

The completed section draft should be:

- **Format:** Markdown (.md file)
- **Location:** manuscript/sections/chapter-{{chapter_number}}/section-{{section_number}}-draft.md
- **Length:** 2-5 pages
- **Code Examples:** Integrated inline (reference separate files in code-curator if needed)
- **Status:** Ready for technical review

**Section Structure:**

```markdown
# Section {{number}}: {{Title}}

## [Concept Introduction]

- What is being taught
- Why it matters
- Where it fits

## [Concept Explanation]

- Theory and background
- Key terminology
- Mental models

## [Tutorial Walkthrough]

- Step-by-step hands-on
- Code examples inline
- Expected outputs
- Progressive difficulty

## [Practical Applications]

- Real-world use cases
- Best practices
- Common mistakes
- Tips and tricks

[Transitions to previous and next sections integrated throughout]
```

## Quality Standards

A high-quality section draft:

✓ **Pedagogically Sound:**

- Clear learning objectives addressed
- Concept before practice
- Progressive difficulty
- Theory balanced with hands-on
- Appropriate for target audience

✓ **Technically Accurate:**

- All code tested and working
- Best practices demonstrated
- Common mistakes addressed
- Prerequisites accurate

✓ **Well-Written:**

- Clear, concise language
- Engaging, encouraging tone
- Smooth narrative flow
- Proper transitions
- Consistent terminology

✓ **Properly Structured:**

- Logical flow: concept → tutorial → applications
- 2-5 pages length
- Code integrated inline
- Outputs documented
- Complete and ready for review

## Common Pitfalls

Avoid these common mistakes:

❌ **Too much theory, not enough hands-on** - Balance is 30% concept, 60% tutorial, 10% applications

❌ **Code examples without explanation** - Always explain what code does and why

❌ **Missing expected outputs** - Readers need to verify they're on track

❌ **No connection to previous/next sections** - Sections should form cohesive narrative

❌ **Too long (over 5 pages)** - Should split into multiple sections

❌ **Too short (under 2 pages)** - Likely missing depth, examples, or applications

❌ **Untested code** - Everything must run successfully

❌ **Unclear learning objectives** - Reader should know what they'll learn

❌ **Assuming too much knowledge** - State prerequisites explicitly

❌ **No real-world context** - Show why this matters in practice

## Troubleshooting

**Writer's Block:**

- Start with tutorial walkthrough (code first, then explanation)
- Use code examples as outline for explanations
- Reference similar sections for structure
- Break writing into smaller chunks

**Scope Creep (section too long):**

- Focus on 1-2 learning objectives max
- Move advanced topics to next section
- Keep "nice to know" content minimal
- Prioritize hands-on over theory

**Code Integration Challenges:**

- Write code first, test, then integrate
- Show complete runnable examples
- Explain "why" in prose, "how" in code
- Document outputs immediately after code

**Unclear Transitions:**

- Review previous section's conclusion
- Review next section's introduction
- Identify specific concepts to reference
- Use natural language, not formulaic

## Section Writing Best Practices

**Hands-On Focus:**

- Code examples are the primary teaching tool
- Theory supports practice, not vice versa
- Readers should type and run code
- Learning by doing, not just reading

**Code Explanation Balance:**

- Explain new concepts thoroughly
- Reference prerequisites briefly
- Assume stated prior knowledge
- Point to resources for depth

**Progressive Disclosure:**

- Start simple, add complexity gradually
- Each example builds on previous
- Final examples show realistic usage
- Prepare readers for independent work

**Reader Engagement:**

- Use "you" to speak directly to reader
- Show outputs to confirm progress
- Celebrate small wins
- Encourage experimentation

**Quality Over Quantity:**

- 3-5 well-explained examples beats 10 unexplained ones
- Depth over breadth
- Clear understanding over comprehensive coverage
- Practical over academic

## Integration with Section-Development Workflow

This task is **Step 3** in the section-development-workflow:

**Workflow Context:**

1. Plan Section (create section-plan.md)
2. Create Code Examples (develop and test code)
3. **Write Section ← THIS TASK**
4. Technical Review (expert reviews section)
5. Editorial Review (polish and refine)

**Inputs from Previous Steps:**

- section-plan.md (from Step 1)
- section-code-examples/ (from Step 2)
- chapter-outline.md (from chapter planning)

**Output to Next Steps:**

- section-{{section_number}}-draft.md → Technical Review (Step 4)

## Next Steps

After completing the section draft:

1. Save section draft to manuscript/sections/chapter-{{chapter_number}}/
2. Commit to version control
3. Mark section as "Ready for Technical Review"
4. Proceed to technical-review-section.md task
5. Address technical review feedback
6. Proceed to editorial review
7. Finalize section

**When All Sections Complete:**

- Compile sections into chapter
- Review chapter-level flow
- Add chapter introduction if needed
- Add chapter summary if needed
- Proceed to chapter-level review

## Related Resources

- **Template:** tutorial-section-tmpl.yaml - Structure guidance
- **Workflow:** section-development-workflow.yaml - Overall process
- **Task:** create-doc.md - Use with template if helpful
- **Task:** create-code-example.md - For developing code examples
- **Task:** test-code-examples.md - For validating code
- **Checklist:** section-quality-checklist.md - Quality validation
- **Knowledge Base:** technical-writing-standards.md - Writing guidelines
