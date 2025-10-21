<!-- Powered by BMAD™ Core -->

# Write Chapter Draft

---

task:
id: write-chapter-draft
name: Write Chapter Draft
description: Develop complete chapter manuscript from outline with introduction, main content, code examples, and exercises
persona_default: tutorial-architect
inputs: - chapter-outline - learning-objectives - target-page-count
steps: - Review chapter outline for structure and objectives - Write compelling introduction (hook, context, overview, prerequisites) - Draft main content sections (concept → tutorial → examples progression) - Create and test all code examples inline - Develop practice exercises with progressive difficulty - Write chapter summary with key takeaways - Add cross-references to other chapters and resources - Include further reading references - Verify all learning objectives are addressed - Run execute-checklist.md with chapter-completeness-checklist.md - Use template chapter-draft-tmpl.yaml with create-doc.md task
output: manuscript/chapters/chapter-{{chapter_number}}-draft.md

---

## Purpose

This task guides you through writing a complete chapter draft that transforms your chapter outline into full instructional content. The focus is on creating clear, engaging technical content that helps readers learn effectively.

## Prerequisites

Before starting this task:

- Chapter outline completed and reviewed
- Learning objectives clearly defined
- Code examples planned and identified
- Access to technical-writing-standards.md knowledge base
- Understanding of target audience skill level

## Workflow Steps

### 1. Review Chapter Outline

Understand the complete chapter structure:

- Re-read the chapter outline carefully
- Review learning objectives
- Check prerequisite alignment
- Understand how this chapter fits in the book's progression
- Note all planned code examples and exercises

**Validation:** Can you explain the chapter flow without looking at the outline?

### 2. Write the Introduction

Create a compelling chapter opening that hooks readers and sets expectations.

**Introduction Components:**

**Hook (1-2 paragraphs):**

- Start with a real-world problem or relatable scenario
- Make readers care about learning this content
- Use questions, stories, or surprising facts
- Connect to reader pain points or aspirations

**Context (1-2 paragraphs):**

- Explain why this topic matters
- Industry relevance and use cases
- How it fits in the bigger technical picture
- Connection to previous chapters

**Overview (1 paragraph):**

- What will be covered in this chapter
- High-level learning path
- What readers will build or accomplish

**Prerequisites:**

- Previous chapters required
- Assumed knowledge
- Software/tools needed with versions
- Estimated time commitment

**Learning Objectives:**

- 3-5 specific, measurable outcomes
- Use action verbs (implement, analyze, create, debug)
- Align with Bloom's taxonomy

**Use template:** introduction-tmpl.yaml for structured guidance

### 3. Draft Main Content Sections

For each major section (typically 3-5 sections per chapter):

**Section Structure Pattern:**

**a) Concept Introduction**

- Explain the concept clearly and concisely
- Use analogies or real-world comparisons where helpful
- Define technical terms
- Provide theoretical background without overwhelming

**b) Tutorial/Walkthrough**

- Step-by-step hands-on implementation
- Clear, numbered steps
- Imperative voice ("Create...", "Add...", "Run...")
- Expected output at each step
- Explain what each step accomplishes and why

**c) Code Examples**

- Complete, runnable code (not fragments unless explained)
- Inline comments explaining key lines
- Best practices demonstrated
- Common mistakes highlighted and avoided
- Input/output examples showing expected results

**d) Section Practice**

- Mini-exercises reinforcing section concepts
- Quick validation of understanding
- Progressive difficulty within section

**Progression:** Move from foundational concepts to advanced topics within the chapter, building on what was just learned.

**Use template:** tutorial-section-tmpl.yaml for hands-on sections

### 4. Create Code Examples

Develop all code examples referenced in the chapter:

**Code Quality Standards:**

- All code must be tested and run successfully
- Follow language-specific style guides
- Include proper error handling
- Use meaningful variable names
- Add comments explaining complex logic
- Specify language version compatibility

**Code Presentation:**

- Use proper syntax highlighting (specify language)
- Show complete context (imports, setup, etc.)
- Provide expected output or results
- Include error examples when teaching debugging
- Reference code files in repository structure

**Best Practices:**

- Demonstrate current industry best practices
- Avoid deprecated or outdated approaches
- Show security-conscious coding
- Consider performance implications
- Follow DRY principles in examples

**Use task:** create-code-example.md for each major example
**Reference:** code-quality-checklist.md and code-testing-checklist.md

### 5. Add Practice Exercises

Create 4-6 end-of-chapter exercises with progressive difficulty:

**Basic Exercises (2-3):**

- Direct application of chapter concepts
- Provide clear guidance and hints
- Solutions or detailed hints included

**Intermediate Exercises (1-2):**

- Require combining multiple concepts
- More independence required
- Hints provided, full solutions optional

**Challenge Exercise (1):**

- Advanced application requiring creativity
- Minimal guidance
- Extension of chapter topics

**For Each Exercise:**

- Clear problem statement
- Specific requirements
- Estimated completion time
- Difficulty indicator (⭐ ⭐⭐ ⭐⭐⭐)
- Hints provided progressively
- Solution approach (not full code)

**Use template:** exercise-set-tmpl.yaml with create-doc.md

**Reference:** exercise-difficulty-checklist.md

### 6. Write Chapter Summary

Conclude with effective summary (1-2 pages):

**Key Takeaways:**

- Bullet list of main concepts covered
- Important terms and definitions
- Core skills acquired

**What You Accomplished:**

- Concrete deliverables from this chapter
- Skills checklist readers can verify
- How this builds on previous learning

**Looking Ahead:**

- Preview of next chapter
- How upcoming content will build on this foundation
- Why the next topic matters

**Further Reading (Optional):**

- Official documentation links
- Recommended articles or resources
- Community resources
- Tools or libraries mentioned

**Avoid:** Simply repeating content. Summarize and synthesize instead.

### 7. Add Cross-References

Link to related content throughout the chapter:

**Internal References:**

- "See Chapter 2, Section 2.3 for database setup"
- "We'll explore advanced patterns in Chapter 8"
- "Review the glossary in Appendix A for term definitions"

**External References:**

- Official documentation (with URLs)
- Standards or specifications (RFCs, PEPs, etc.)
- Relevant research papers or articles
- Community resources (forums, guides)

**Best Practices:**

- Be specific with chapter and section numbers
- Test all URLs for validity
- Prefer stable, official sources
- Note if external content may change

### 8. Include Further Reading

Provide curated resources for deeper learning:

**Official Sources:**

- Language documentation
- Framework guides
- API references
- Release notes for features used

**Community Resources:**

- Well-regarded tutorials
- Video explanations
- Community forums or discussion
- GitHub repositories

**Quality Over Quantity:**

- 5-8 truly helpful resources beats 20 mediocre ones
- Annotate each resource with what it provides
- Organize by topic or learning path

### 9. Verify Learning Objectives Addressed

Ensure all promised learning outcomes are covered:

**For Each Learning Objective:**

- Where in the chapter is this taught?
- Are there examples demonstrating this skill?
- Can readers practice this skill in exercises?
- Is there clear evidence of skill achievement?

**Self-Check:**

- Read each objective
- Find the section(s) teaching it
- Verify hands-on practice exists
- Confirm assessment opportunity (exercise/quiz)

**If objective not adequately covered:** Add content or revise objective.

### 10. Review Against Chapter Completeness Checklist

Final quality check before review:

**Run:** execute-checklist.md with chapter-completeness-checklist.md

**Checklist Includes:**

- All sections from outline present
- Learning objectives fully addressed
- Code examples tested and working
- Exercises appropriate difficulty
- Cross-references valid
- Length appropriate (15-30 pages typical)
- Consistent terminology
- Voice and style consistent

**Fix any issues found** before marking draft complete.

## Output

The completed chapter draft should be:

- **Format:** Markdown (.md file)
- **Location:** manuscript/chapters/chapter-{{chapter_number}}-draft.md
- **Code Examples:** In separate repository folder with clear organization
- **Length:** Typically 15-30 pages (adjust based on topic complexity)
- **Status:** Ready for technical review

## Quality Standards

A high-quality chapter draft:

✓ Hooks readers with compelling introduction
✓ Explains concepts clearly with helpful analogies
✓ Provides hands-on tutorials with clear steps
✓ Includes tested, working code examples
✓ Offers exercises at appropriate difficulty
✓ Summarizes key takeaways effectively
✓ Addresses all learning objectives
✓ Maintains consistent voice and style
✓ References sources appropriately
✓ Follows technical writing best practices

## Common Pitfalls

Avoid these common mistakes:

❌ **Too much theory, not enough practice** - Balance concepts with hands-on work
❌ **Code examples that don't run** - Test everything before including
❌ **Unclear instructions** - Be specific; use numbered steps
❌ **Assuming too much knowledge** - State prerequisites explicitly
❌ **Inconsistent terminology** - Use terms consistently throughout
❌ **No connection between sections** - Add transitions and explain flow
❌ **Exercises too easy or too hard** - Progressive difficulty is key
❌ **Missing the "why"** - Always explain why things matter

## Next Steps

After completing the chapter draft:

1. Save and commit draft to repository
2. Proceed to technical-review-chapter.md task
3. Technical reviewer will assess accuracy and quality
4. Revise based on technical review feedback
5. Proceed to copy-edit-chapter.md for editorial polish
6. Address copy edit feedback
7. Mark chapter complete and ready for publication review

## Related Resources

- Template: chapter-draft-tmpl.yaml
- Template: introduction-tmpl.yaml
- Template: tutorial-section-tmpl.yaml
- Template: exercise-set-tmpl.yaml
- Task: create-code-example.md
- Task: create-doc.md
- Checklist: chapter-completeness-checklist.md
- Knowledge Base: technical-writing-standards.md
