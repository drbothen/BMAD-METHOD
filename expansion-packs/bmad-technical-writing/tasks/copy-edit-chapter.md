<!-- Powered by BMAD™ Core -->

# Copy Edit Chapter

---

task:
id: copy-edit-chapter
name: Copy Edit Chapter
description: Professional editorial polish including grammar, clarity, consistency, style compliance, and accessibility
persona_default: technical-editor
inputs: - chapter-draft - chapter-number - target-publisher
steps: - Review chapter for grammar and spelling - Check terminology consistency throughout - Verify publisher style guide compliance - Improve sentence clarity and readability - Enhance transitions between sections - Check heading hierarchy and structure - Verify code formatting consistency - Review accessibility considerations - Polish language for professional quality - Ensure consistent voice and tone - Create summary of editorial changes - Run execute-checklist.md with accessibility-checklist.md - Run execute-checklist.md with relevant publisher checklist
output: Edited chapter with change summary

---

## Purpose

Transform technically accurate content into professionally polished, publication-ready material that is clear, consistent, accessible, and compliant with publisher requirements.

## Prerequisites

- Chapter draft completed and technically reviewed
- Technical review issues addressed
- Publisher style guide available
- Access to publisher-guidelines.md knowledge base
- Access to technical-writing-standards.md knowledge base

## Workflow Steps

### 1. Review Grammar and Spelling

Perform comprehensive language check:

**Grammar:**

- Subject-verb agreement
- Pronoun references
- Verb tenses (use present tense for technical writing)
- Parallel structure in lists
- Sentence fragments and run-ons

**Spelling:**

- Technical terms spelled correctly
- Consistent spelling (US vs UK English)
- Common technical term errors (e.g., "GitHub" not "Github")

**Tools:**

- Use spell checker as first pass
- Manual review for technical terms
- Verify proper nouns and product names

**Note:** Technical writing often uses terms spell checkers don't recognize - verify rather than auto-correct.

### 2. Check Terminology Consistency

Ensure terms used consistently throughout:

**Term Standardization:**

- Create term list for chapter
- Use same term for same concept (not "function" then "method" interchangeably)
- Match terminology to official documentation
- Consistent capitalization (e.g., "JavaScript" not "Javascript")

**Common Inconsistencies:**

- API vs API's vs APIs (plurals and possessives)
- Filename vs file name vs file-name
- Setup vs set up (noun vs verb)
- Backend vs back-end vs back end

**Action:** Search chapter for term variations and standardize.

### 3. Verify Publisher Style Guide Compliance

Apply specific publisher requirements:

**PacktPub:**

- Chicago Manual of Style
- Second person ("you") perspective
- Active voice preferred
- Code formatting in monospace
- Screenshots at required resolution

**O'Reilly:**

- Chicago Manual of Style
- Specific heading levels
- Code highlighting conventions
- Cross-reference formatting

**Manning:**

- Conversational but professional tone
- Author voice encouraged
- Specific formatting for code listings
- Margin note requirements

**Use relevant checklist:**

- packtpub-submission-checklist.md
- oreilly-format-checklist.md
- manning-meap-checklist.md

### 4. Improve Sentence Clarity

Enhance readability and comprehension:

**Clarity Principles:**

- One idea per sentence when possible
- Active voice preferred over passive
- Remove unnecessary words
- Break complex sentences into simpler ones
- Use concrete examples over abstractions

**Before:** "It should be noted that the utilization of this pattern may result in performance improvements."

**After:** "This pattern often improves performance."

**Avoid:**

- Jargon without explanation
- Overly complex sentence structures
- Ambiguous pronouns ("it", "this", "that" without clear referent)
- Double negatives

**Preserve:**

- Author voice and style
- Technical precision
- Necessary complexity

### 5. Enhance Transitions

Improve flow between sections and ideas:

**Between Sections:**

- Add transition sentences linking topics
- Preview what's coming next
- Reference what was just covered
- Explain logical progression

**Example Transitions:**

- "Now that you understand X, let's explore Y..."
- "With this foundation in place, we can tackle..."
- "Building on the previous example, you'll now..."

**Within Paragraphs:**

- Use transition words (however, therefore, additionally)
- Maintain logical flow
- Connect sentences coherently

**Check:** Can reader follow the logical progression without getting lost?

### 6. Check Heading Hierarchy

Ensure proper document structure:

**Hierarchy Rules:**

- H1: Chapter title (one per chapter)
- H2: Major sections
- H3: Subsections
- H4: Minor subsections (use sparingly)

**Heading Best Practices:**

- Parallel structure in same level
- Descriptive and specific
- Avoid "Introduction" as H2 (use descriptive title)
- Capitalize consistently

**Example:**

```
# Chapter 3: Database Design (H1)
## Understanding Relational Databases (H2)
### Tables and Relationships (H3)
### Primary and Foreign Keys (H3)
## Designing Your First Schema (H2)
### Identifying Entities (H3)
```

### 7. Verify Code Formatting Consistency

Ensure all code formatted properly:

**Code Blocks:**

- Language specified for syntax highlighting
- Consistent indentation (spaces vs tabs)
- Line length appropriate (avoid horizontal scrolling)
- Comments formatted consistently

**Inline Code:**

- Use backticks for code terms
- Function names: `function_name()`
- Variables: `variable_name`
- File paths: `path/to/file.py`

**Code Callouts:**

- Explanations below code blocks
- Reference specific lines when needed
- Expected output shown where relevant

**Consistency:**

- Same style throughout chapter
- Matches publisher requirements
- Follows language conventions

### 8. Review Accessibility

Ensure content is accessible to all readers:

**Use accessibility-checklist.md**

**Key Checks:**

- Alt text for all images and diagrams
- Color not the sole means of conveying information
- Code examples screen-reader friendly
- Clear heading hierarchy (aids navigation)
- Descriptive link text (not "click here")
- Plain language where possible
- Acronyms defined on first use

**Example:** Instead of "See the red line in the diagram", use "See the error indicator (red line) in the diagram"

### 9. Polish Language and Readability

Final pass for professional quality:

**Voice and Tone:**

- Consistent throughout chapter
- Appropriate for audience (not too casual, not too formal)
- Encouraging and supportive (avoid condescending)
- Technical but approachable

**Readability:**

- Vary sentence length
- Break up long paragraphs (3-5 sentences typical)
- Use lists for multiple items
- Add white space for visual breaks

**Professional Polish:**

- Remove filler words (basically, simply, just)
- Strengthen weak verbs (use specific action verbs)
- Replace vague terms with specific ones
- Ensure confident tone (avoid "might", "maybe", "probably")

### 10. Create Summary of Changes

Document editorial modifications:

**Change Log Should Include:**

- Major structural changes
- Terminology standardizations
- Sections rewritten for clarity
- Publisher style compliance updates
- Accessibility improvements

**Format:**

```
Editorial Changes Summary - Chapter 3

Structural:
- Combined Sections 3.2 and 3.3 for better flow
- Moved error handling to separate section 3.5

Clarity:
- Simplified complex sentences in Section 3.1
- Added transition between Sections 3.3 and 3.4

Terminology:
- Standardized "filesystem" (not "file system")
- Corrected "GitHub" capitalization throughout

Style:
- Applied PacktPub heading format
- Updated code block syntax highlighting

Accessibility:
- Added alt text to all 8 diagrams
- Defined all acronyms on first use
```

**Purpose:** Helps author understand changes and learn for future chapters.

## Output

Copy edited chapter with:

- Clean, professional prose
- Consistent terminology
- Proper grammar and spelling
- Clear transitions and flow
- Publisher style compliance
- Accessibility improvements
- Change summary document

## Quality Standards

Professional copy edit:

✓ Error-free grammar and spelling
✓ Consistent terminology throughout
✓ Clear, readable sentences
✓ Smooth transitions between sections
✓ Proper heading hierarchy
✓ Code formatting consistent
✓ Publisher requirements met
✓ Accessible to all readers
✓ Professional tone maintained
✓ Author voice preserved

## Common Pitfalls

Avoid:

❌ Over-editing and losing author voice
❌ Introducing new technical errors
❌ Inconsistent style between sections
❌ Removing necessary technical detail
❌ Making changes without understanding context
❌ Ignoring publisher-specific requirements

## Next Steps

After copy editing:

1. Return edited chapter to author for review
2. Author approves or discusses editorial changes
3. Resolve any disagreements collaboratively
4. Finalize chapter text
5. Proceed to final publication preparation
6. Publisher may do additional copy editing pass
