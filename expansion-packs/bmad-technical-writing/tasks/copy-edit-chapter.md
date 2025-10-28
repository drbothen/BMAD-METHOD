<!-- Powered by BMAD™ Core -->

# Copy Edit Chapter

---

task:
id: copy-edit-chapter
name: Copy Edit Chapter
description: Professional editorial polish including grammar, clarity, consistency, style compliance, and accessibility
persona_default: technical-editor
inputs:

- chapter-draft
- chapter-number
- target-publisher
  steps:
- Review chapter for grammar and spelling
- Check terminology consistency throughout
- Verify publisher style guide compliance
- Improve sentence clarity and readability
- Enhance transitions between sections
- Check heading hierarchy and structure
- Verify code formatting consistency
- Review accessibility considerations
- Polish language for professional quality
- Ensure consistent voice and tone
- Create summary of editorial changes
- Run execute-checklist.md with accessibility-checklist.md
- Run execute-checklist.md with relevant publisher checklist
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

### 9. Ensure Consistent Voice and Tone (Enhanced)

Final pass for professional quality WITH tone validation:

**CRITICAL: Load Tone Reference Document First**

Before validating tone, load the appropriate reference document:

- **Greenfield projects:** Load `tone-specification.md`
- **Brownfield projects (editions/updates):** Load `extracted-tone-patterns.md`
- If neither exists: Flag for author to create tone specification before proceeding

**Substep 9.1: Load Tone Reference Document**

Identify which tone document applies to this project:

```markdown
**Project Type:** [Greenfield / Brownfield]

**Tone Reference:**
- File: [tone-specification.md OR extracted-tone-patterns.md]
- Location: [docs/ OR manuscript/planning/]

**Key Tone Characteristics to Validate:**
1. [Characteristic 1 from specification]
2. [Characteristic 2 from specification]
3. [Characteristic 3 from specification]
4. [Characteristic 4 from specification]
5. [Characteristic 5 from specification]

**Formality Level:** [1-5]
**Publisher:** [PacktPub / O'Reilly / Manning / Self-Publishing]
```

**Substep 9.2: Execute tone-consistency-checklist.md**

Run the comprehensive tone validation checklist:

**Execute:** Use execute-checklist.md task with tone-consistency-checklist.md

This checklist validates:
- Voice consistency (perspective, active/passive)
- Formality level alignment
- Publisher-specific requirements
- Tone characteristics application (all 5 present)
- Code comment style consistency
- Transition and flow patterns
- Excluded tones avoided

**Document Results:**

```markdown
**Tone Validation Results:**

Checklist: tone-consistency-checklist.md
Date: [Date]
Reviewer: [Name]

**Violations Found:** [Number]

**Category Breakdown:**
- Voice consistency: [Number] issues
- Formality level: [Number] issues
- Publisher alignment: [Number] issues
- Tone characteristics: [Number] issues
- Code comments: [Number] issues
- Other: [Number] issues

**Details:** [See substep 9.3 for specific violations]
```

**Substep 9.3: Document Tone Violations Found**

List specific tone issues discovered:

```markdown
**Tone Violations Log:**

**Violation 1: Formality Level Inconsistency**
- Location: Lines 145-167
- Issue: Level 5 formality (no contractions, passive voice)
- Expected: Level 3 (moderate contractions, active voice)
- Example: "One must configure the service prior to deployment"
- Correction needed: "You'll need to configure the service before deployment"

**Violation 2: Missing Tone Characteristic**
- Location: Section 3.4 (Lines 200-250)
- Issue: "Encouraging" characteristic absent
- Expected: Matter-of-fact encouragement at milestones
- Example: Technical explanation only, no capability acknowledgment
- Correction needed: Add milestone encouragement per specification

**Violation 3: Code Comment Tone Mismatch**
- Location: Code block, lines 300-325
- Issue: Comments too formal for Level 3 prose
- Expected: Comments match prose formality
- Example: "// Instantiate authentication service object"
- Correction needed: "// Set up auth service"

[Continue for all violations found]
```

**Substep 9.4: Apply Tone Corrections**

Systematically fix documented violations:

**Correction Process:**

1. **Prioritize violations:** Critical (publisher misalignment, missing characteristics) first
2. **Apply corrections systematically:** Work through document section by section
3. **Reference tone specification:** Use example passages as models
4. **Maintain technical accuracy:** Never sacrifice clarity for tone

**Example Corrections:**

**Before (Violation):**
```markdown
One must ensure that the authentication mechanism has been properly configured prior to initiating the deployment sequence. The configuration file should be edited to include the necessary credentials.
```

**After (Corrected to Level 3, Second Person, Active Voice):**
```markdown
You'll need to configure authentication before deploying. Edit the configuration file to include your credentials.
```

**Before (Missing Encouragement):**
```markdown
Section 3.4 Summary

This section covered JWT structure, signature validation, and token expiration handling.
```

**After (Added Encouragement Pattern):**
```markdown
Section 3.4 Summary

You've now mastered JWT structure, signature validation, and token expiration handling. You can confidently implement secure token-based authentication in production applications.
```

**Substep 9.5: Verify Corrections Maintain Author Voice**

**CRITICAL CHECK:** Ensure corrections preserve authenticity

After applying tone corrections, validate:

- [ ] Technical accuracy unchanged
- [ ] Author personality still present (not robotic)
- [ ] Natural language flow maintained
- [ ] Corrections feel authentic, not forced
- [ ] Humor/personality markers retained (if in specification)

**Red Flag - Over-Correction:**

If corrections sound robotic or forced, dial back:

```markdown
**Over-Corrected (Too Mechanical):**
"You'll configure the service. You'll deploy the application. You'll verify the results."

**Better (Natural Variation):**
"You'll configure the service, deploy the application, and verify everything works as expected."
```

**Voice and Tone Validation Complete:**

- [x] Tone reference document loaded
- [x] tone-consistency-checklist.md executed
- [x] Violations documented with specific examples
- [x] Corrections applied referencing specification
- [x] Author voice authenticity verified

**Traditional Voice and Tone Checks (Still Apply):**

- Consistent throughout chapter
- Appropriate for audience (formality level from specification)
- Encouraging and supportive per specification style
- Technical but approachable

**Readability:**

- Vary sentence length (check against specification's sentence complexity patterns)
- Break up long paragraphs (3-5 sentences typical)
- Use lists for multiple items
- Add white space for visual breaks

**Professional Polish:**

- Remove filler words (but check specification—some casual tones use "just", "basically" intentionally)
- Strengthen weak verbs (use specific action verbs)
- Replace vague terms with specific ones
- Ensure confident tone per specification (some avoid "might"/"maybe", others embrace uncertainty where appropriate)

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
