<!-- Powered by BMAD™ Core -->

# Create Code Example

---

task:
id: create-code-example
name: Create Code Example
description: Develop working, tested, documented code example with explanation
persona_default: code-curator
inputs:

- concept-to-demonstrate
- programming-language
- target-version
  steps:
- Identify learning objective for this code example
- Choose appropriate complexity level for target audience
- Write working code with inline comments
- Test code for correctness on target version
- Write detailed explanation connecting code to concepts
- Document prerequisites and dependencies
- Add common mistakes section
- Create variations and extensions section
- Define testing approach
- Use template code-example-tmpl.yaml with create-doc.md task
- Run execute-checklist.md with code-quality-checklist.md
- Run execute-checklist.md with code-testing-checklist.md
- Run execute-checklist.md with version-compatibility-checklist.md
  output: docs/{{config.codeExamples.root}}/{{example-name}}-example.md

---

## Purpose

This task guides you through creating high-quality code examples that readers can trust, understand, and adapt. Every code example must work perfectly, follow best practices, and include comprehensive explanation.

## Prerequisites

Before starting this task:

- Clear understanding of the concept to demonstrate
- Target programming language and version
- Access to code-style-guides.md knowledge base
- Ability to test code on target platform(s)

## Workflow Steps

### 0. Load Configuration

- Read `.bmad-technical-writing/config.yaml` to resolve directory paths
- Extract: `config.codeExamples.root`
- If config not found, use default: `code-examples`

### 1. Identify Learning Objective

Define what this example teaches:

- What specific concept or technique does this demonstrate?
- Why is this approach useful?
- When should readers apply this pattern?
- How does this fit into the chapter's learning objectives?

**Example:** "Demonstrate JWT authentication middleware in Express.js to show secure API endpoint protection."

### 2. Choose Complexity Level

Select appropriate complexity:

- **Basic**: Single concept, minimal dependencies, <30 lines
- **Intermediate**: Multiple concepts, moderate structure, 30-100 lines
- **Advanced**: Complex interactions, full patterns, 100+ lines

Match complexity to:

- Reader's current skill level
- Chapter position in book
- Concept difficulty

### 3. Write Working Code

Create the code example:

**Code Quality Requirements:**

- [ ] Code executes successfully without errors
- [ ] Follows language-specific style guide (PEP 8, Airbnb JS, Google Java, etc.)
- [ ] Uses descriptive variable and function names
- [ ] Includes inline comments explaining WHY, not WHAT
- [ ] Demonstrates proper error handling
- [ ] Is DRY (Don't Repeat Yourself)
- [ ] Avoids hardcoded values (use constants/config)
- [ ] Includes all necessary imports/dependencies

**Comment Guidelines:**

- Explain design decisions and tradeoffs
- Highlight key concepts being demonstrated
- Point out important details
- Don't explain obvious syntax

### 4. Test Code Thoroughly

Verify the code works:

- Run code on target version (e.g., Python 3.11+, Node 18+)
- Test on target platforms (Windows/Mac/Linux if applicable)
- Verify output matches expectations
- Test edge cases and error conditions
- Document exact test commands used
- Include expected output

**Testing Checklist:**

- [ ] Code runs without modification
- [ ] Dependencies install correctly
- [ ] Output is as documented
- [ ] Error handling works
- [ ] Edge cases covered

### 5. Write Detailed Explanation

Explain the code thoroughly:

- **Overall structure**: How is the code organized?
- **Key concepts**: What techniques are demonstrated?
- **Design decisions**: Why this approach over alternatives?
- **Tradeoffs**: What are the pros and cons?
- **Important details**: What might readers miss?
- **Integration**: How do parts work together?

Connect code to theory:

- Reference chapter concepts
- Explain how code implements theory
- Show practical application of principles

### 6. Document Prerequisites and Setup

Provide complete setup instructions:

- Prior knowledge required
- Software/tools needed (with versions)
- Dependencies to install (exact commands)
- Environment setup (virtual env, Docker, etc.)
- Configuration needed
- Verification steps

**Setup Template:**

```
Prerequisites:
- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

Setup:
1. Create virtual environment: python -m venv venv
2. Activate: source venv/bin/activate (Mac/Linux) or venv\Scripts\activate (Windows)
3. Install dependencies: pip install -r requirements.txt
4. Verify: python --version (should show 3.11+)
```

### 7. Add Common Mistakes Section

Document pitfalls:

- What mistakes do beginners commonly make?
- Why are these mistakes problematic?
- How to identify these issues
- Corrected examples

**Example:**

```
❌ Common Mistake: Hardcoding API keys
```

api_key = "sk-1234567890abcdef"

```

✅ Correct Approach: Use environment variables
```

api_key = os.getenv("API_KEY")

```

```

### 8. Create Variations and Extensions

Show how to adapt the example:

- Alternative implementations
- How to extend functionality
- When to use variations
- More advanced patterns building on this
- Real-world applications

### 9. Generate Code Example Document

Use the create-doc.md task with code-example-tmpl.yaml template to create the structured code example document.

### 10. Validate Code Quality

Run checklists:

- code-quality-checklist.md - Verify code follows standards
- code-testing-checklist.md - Ensure thorough testing
- version-compatibility-checklist.md - Confirm version support

## Success Criteria

A completed code example should have:

- [ ] Working code that executes successfully
- [ ] Follows language-specific style guide
- [ ] Inline comments explain WHY, not WHAT
- [ ] Tested on target version(s)
- [ ] Complete setup instructions
- [ ] Detailed explanation connecting code to concepts
- [ ] Prerequisites clearly documented
- [ ] Common mistakes section
- [ ] Variations and extensions
- [ ] Testing approach defined
- [ ] All checklists passed

## Common Pitfalls to Avoid

- **Untested code**: Always run code before documenting
- **Missing dependencies**: List ALL requirements
- **Poor comments**: Explain decisions, not syntax
- **Hardcoded values**: Use constants or configuration
- **Insufficient error handling**: Show proper error management
- **Outdated syntax**: Use current language features
- **Platform assumptions**: Test on target platforms
- **No explanation**: Code alone doesn't teach

## Next Steps

After creating the code example:

1. Add code file to chapter's code repository
2. Create unit tests (if appropriate)
3. Test on all supported platforms
4. Integrate into chapter narrative
5. Cross-reference from related sections
