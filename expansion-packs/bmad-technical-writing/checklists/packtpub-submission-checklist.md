<!-- Powered by BMAD™ Core -->

# PacktPub Submission Checklist

---

checklist:
  id: packtpub-submission
  name: PacktPub Chapter/Manuscript Submission Checklist
  description: Official PacktPub quality checklist for technical book chapters and manuscripts
  source: Your Writing Checklist.pdf (PacktPub Author Bundle)
  persona_default: manuscript-reviewer
  applies_to:
    - Technical book chapters
    - Full manuscript submissions
    - Sample chapter submissions
  sections:
    - Outline Compliance
    - Structure Requirements
    - Readability Standards
    - Value Proposition
    - Technical Requirements
    - Code Quality
    - Image Quality
    - Style and Formatting

---

## Purpose

This checklist validates technical book chapters and manuscripts against PacktPub's official submission requirements. All items must pass (or be documented as exceptions) before submitting to your PacktPub editor.

**Source**: Official PacktPub Author Bundle ("Your Writing Checklist.pdf")

## How to Use This Checklist

1. **During Writing**: Reference sections to ensure compliance
2. **Before Submission**: Execute complete checklist validation
3. **With Automation**: Use `format-for-packtpub.md` task which runs this checklist
4. **Manual Review**: Check items marked "Manual Review Required"

## Checklist Items

### 1. Outline Compliance

These items verify your chapter matches the agreed-upon outline and objectives.

#### 1.1 Topic Coverage
- [ ] **All topics/skills mentioned in outline are covered**
  - Cross-reference outline document
  - Verify each topic has dedicated section
  - Check that no outline topics are missing

#### 1.2 Page Count
- [ ] **Chapter page count within acceptable range**
  - Outline specifies target page count
  - Too high: content may be too detailed or off-topic
  - Too low: content may be insufficient or missing topics
  - Acceptable variance: ±10% of target

#### 1.3 Learning Objectives
- [ ] **Chapter meets all stated learning objectives**
  - Each objective listed in outline is addressed
  - Reader can demonstrate each skill after reading
  - Practical examples provided for each objective

---

### 2. Structure Requirements

These items ensure your chapter follows PacktPub's required structure and formatting.

#### 2.1 Introduction Section
- [ ] **Chapter opens with brief introduction**
  - Located before first H2 heading
  - 1-3 paragraphs maximum
  - Sets context for the chapter

- [ ] **Introduction lists learning goals**
  - "In this chapter, you will learn..."
  - "This chapter covers..."
  - Bullet list format

- [ ] **Bullet list of main topics/Level 1 headings**
  - Each H2 section listed
  - Uses consistent format
  - Gives reader roadmap of chapter content

#### 2.2 Heading Standards
- [ ] **Appropriate heading styles used (Heading 1-6)**
  - Heading 1: Chapter title
  - Heading 2: Major sections
  - Heading 3: Subsections
  - Avoid skipping levels (H2 → H4)

- [ ] **Headings use "-ing" verbs to imply action**
  - ✓ "Creating a React Component"
  - ✓ "Installing the Development Environment"
  - ✗ "React Components"
  - ✗ "Development Environment"

#### 2.3 Transitions and Flow
- [ ] **Signposts/transitions between major sections**
  - Link previous section to next
  - "Now that we've covered X, let's explore Y..."
  - "With X configured, we can now..."

- [ ] **Content linked to create learning journey**
  - Each section builds on previous
  - Concepts introduced before being used
  - Forward references when appropriate

- [ ] **No consecutive headers (lead-in text required)**
  - Every heading followed by explanatory paragraph
  - Never: H2 immediately followed by H3
  - Always: H2, paragraph(s), then H3

- [ ] **No consecutive images (framing text required)**
  - Text before image explaining what to look for
  - Text after image explaining significance
  - Never: image immediately following another image

#### 2.4 Summary and Conclusion
- [ ] **Summary section present at end of chapter**
  - Recap main learnings
  - Reinforce value/application
  - "You have now learned..."
  - "You can now configure..."
  - "You now understand..."

- [ ] **Summary closes by introducing next chapter topic**
  - "In the next chapter, we will..."
  - Creates continuity across chapters
  - Maintains reader engagement

- [ ] **Reader able to achieve goals mentioned in introduction**
  - Introduction promises match summary delivery
  - All learning objectives addressable by reader
  - Practical skills demonstrated, not just explained

---

### 3. Readability Standards

These items ensure your content is accessible and engaging for the target audience.

#### 3.1 Audience Consideration
- [ ] **Content appropriate for target audience level**
  - Beginners: more detail, simpler explanations, more examples
  - Intermediate: moderate detail, some assumptions of knowledge
  - Advanced: technical depth, fewer basic explanations

- [ ] **Terminology introduced before use**
  - First use of term includes definition or context
  - Use **Key Word [PACKT]** style for first appearance
  - Avoid assuming reader knows jargon

#### 3.2 Writing Style
- [ ] **Content kept concise and straightforward**
  - Short sentences (15-20 words average)
  - One concept per paragraph
  - Active voice preferred

- [ ] **Reader addressed using "you" and "we"**
  - "You can now configure..."
  - "We will explore..."
  - Avoid passive: "The configuration is done by..."
  - Avoid third-person: "The user configures..."

#### 3.3 Visual Variety
- [ ] **Create visual variety throughout chapter**
  - Mix of paragraphs, lists, code, images, tables
  - Avoid long stretches of plain text
  - Break up dense content with formatting

- [ ] **Lists used appropriately**
  - Bullet lists for unordered items
  - Numbered lists for sequential steps
  - Definition lists for term/description pairs

- [ ] **Info boxes used for supplementary content**
  - Tips, warnings, notes, information boxes
  - Not essential to main flow
  - Enhance understanding

#### 3.4 Code and Image Framing
- [ ] **Text before all code blocks explaining context**
  - What the code does
  - Why it's relevant
  - What to focus on

- [ ] **Text after all code blocks explaining significance**
  - What was demonstrated
  - Key points to remember
  - How it connects to larger topic

- [ ] **Text before all images explaining what to look for**
  - "In the following screenshot, notice..."
  - "The diagram shows..."
  - Directs reader's attention

- [ ] **Text after all images explaining significance**
  - "As you can see..."
  - "This illustrates..."
  - Reinforces the point being made

---

### 4. Value Proposition

These items ensure your content provides practical, real-world value to readers.

#### 4.1 Practical Focus
- [ ] **Content hands-on and practical with real-world examples**
  - Prefer working code over theory
  - Use realistic scenarios
  - Avoid contrived "foo/bar" examples when possible

- [ ] **Limit or avoid background information and theory**
  - Some theory needed for understanding
  - Should support practical application, not dominate
  - "Just enough" theory to enable practice

- [ ] **Numbered steps for complex tasks/code execution**
  - 1. Do this
  - 2. Then do this
  - 3. Finally do this
  - Makes procedures clear and followable

#### 4.2 Visual Support
- [ ] **Images support/simplify explanations, not just illustrate**
  - Diagrams explain complex concepts
  - Screenshots show specific UI elements
  - Charts/graphs reveal patterns
  - Each image has clear purpose

#### 4.3 Learning Reinforcement
- [ ] **Value/real-world application stated at end of each section**
  - "This technique allows you to..."
  - "You'll use this when..."
  - "Real-world applications include..."

- [ ] **"Close to goal" reminders for readers**
  - Progress indicators throughout chapter
  - "You're now halfway to building..."
  - Maintains motivation

- [ ] **Summary recaps learnings and reinforces value/application**
  - Not just "we covered X, Y, Z"
  - "You can now X, Y, Z in your projects"
  - Emphasizes practical skills gained

---

### 5. Technical Requirements

These items ensure your technical content is accurate, current, and complete.

#### 5.1 Version Currency
- [ ] **Latest/updated versions for all tech and code**
  - Check for updates before starting chapter
  - Document version numbers in text
  - Avoid deprecated features/APIs

- [ ] **Version updates checked before each chapter**
  - Frameworks update frequently
  - API changes may affect examples
  - Syntax may evolve

#### 5.2 Code Explanation
- [ ] **All code explained in paragraph or sentence**
  - No unexplained code blocks
  - Key lines highlighted and discussed
  - Complex logic broken down

- [ ] **No in-code comments (explain in surrounding text)**
  - Code should be clean, production-like
  - Explanations belong in prose, not comments
  - Exception: Standard documentation comments (JSDoc, etc.)

#### 5.3 Code Repository
- [ ] **GitHub repository updated with each chapter**
  - Complete working examples
  - Organized by chapter
  - README with setup instructions
  - Link provided in manuscript or to editor

---

### 6. Code Quality

These items ensure code blocks meet PacktPub's formatting and quality standards.

#### 6.1 Code Block Length (CRITICAL)
- [ ] **No code blocks exceed 30 lines (HARD LIMIT)**
  - 30 lines = absolute maximum
  - Blocks over 30 lines MUST be split
  - Solutions: extract functions, show key sections only, reference full code on GitHub

- [ ] **Code blocks ideally ≤20 lines (RECOMMENDED)**
  - 20 lines = optimal for readability
  - Blocks 21-30 lines flagged as warning
  - Strive for concise, focused examples

- [ ] **Long code broken into logical sections**
  - Show setup, then usage, then cleanup separately
  - Use "..." to indicate omitted code
  - Explain each section individually

#### 6.2 Code Style and Formatting
- [ ] **Code uses proper syntax highlighting**
  - Language identifier on code fence: ```javascript
  - Enables proper formatting in conversion
  - Improves readability

- [ ] **Code follows language best practices**
  - Idiomatic code for the language
  - Modern syntax (ES6+, Python 3, etc.)
  - Not overly clever or obfuscated

- [ ] **Code is tested and working**
  - All examples actually run
  - No syntax errors
  - Produces expected output

---

### 7. Image Quality

These items ensure images meet PacktPub's print quality standards.

#### 7.1 Resolution Requirements (CRITICAL)
- [ ] **All images 300 DPI minimum**
  - Check DPI metadata
  - Use GIMP for screenshot capture (auto 300 DPI)
  - Paste PrtScr into GIMP document to convert

- [ ] **All images 2000px minimum on shortest edge**
  - Width AND height matter
  - Measure shortest dimension
  - Upscaling doesn't improve quality - capture at correct size

#### 7.2 Format Requirements (CRITICAL)
- [ ] **No JPG format images (PNG/TIFF only)**
  - JPG loses quality with each save
  - PNG: screenshots, UI captures
  - TIFF: diagrams, artwork
  - Convert existing JPG to PNG

- [ ] **Original images provided to editor**
  - Separate files, not just embedded
  - Organized in dedicated folder
  - Descriptive filenames with figure numbers

#### 7.3 Screenshot Quality
- [ ] **Screenshots focused on relevant content**
  - Crop empty space
  - Highlight UI elements being discussed
  - Text in screenshot readable at print size

- [ ] **Full-screen + snippet pairs for detail images**
  - Detail: cropped area of interest
  - Full: entire screen for context
  - Naming: `figure-1-snip.png` and `figure-1-fullscreen.png`

- [ ] **Screenshots file size ≥1000KB at full screen**
  - Indicates sufficient resolution
  - Smaller files likely insufficient quality

#### 7.4 Third-Party Images
- [ ] **Copyright/license checked for third-party images**
  - Permission obtained if needed
  - Attribution included where required
  - Print/digital rights confirmed

- [ ] **Highest resolution obtained (not screenshots of images)**
  - Request original from source
  - Download full-resolution version
  - Don't screenshot existing images

---

### 8. Style and Formatting

These items ensure proper PacktPub style application.

#### 8.1 PACKT Styles Applied
- [ ] **All paragraphs use PacktPub styles**
  - Headings: "Heading 1-6" (standard, no [PACKT])
  - Content: "[PACKT]" suffix styles (Normal [PACKT], Code [PACKT], etc.)
  - No built-in Word styles (except headings)

- [ ] **Code blocks use Code [PACKT] / Code End [PACKT]**
  - Code [PACKT]: all lines except last
  - Code End [PACKT]: last line of code block
  - Single-line code uses Code [PACKT] only

- [ ] **Lists use Bullet [PACKT] / Numbered Bullet [PACKT]**
  - Bullet [PACKT]: unordered lists
  - Numbered Bullet [PACKT]: ordered lists
  - No standard Word list styles

- [ ] **Inline formatting uses character [PACKT] styles**
  - Key Word [PACKT]: first appearance of terms, important concepts
  - Italics [PACKT]: emphasis
  - Code In Text [PACKT]: inline code, commands, filenames

#### 8.2 Document Template
- [ ] **Document based on Sample Chapter.docx template**
  - Contains all 77 [PACKT] styles
  - Ensures style consistency
  - Required for proper conversion

---

## Content Standards

### Writing Quality
- [ ] **Avoid repeating information; cross-reference instead**
  - "As discussed in Chapter 3..."
  - "See the X section earlier in this chapter..."
  - Keeps content concise

- [ ] **No disparaging references (race, gender, religion, etc.)**
  - Inclusive language
  - Professional tone
  - Respectful examples

- [ ] **No plagiarism (text, images, datasets, code)**
  - Original content or properly licensed
  - Citations where required
  - Code examples original or open-source with attribution

---

## Validation Report Format

When this checklist is executed, generate a report in this format:

```markdown
# PacktPub Submission Checklist Results

**Chapter**: [Chapter Title]
**Date**: [Date]
**Overall Score**: X/Y items passed

## Summary

✅ **PASS** - Ready for submission
🟡 **WARNINGS** - Address N warnings before submission
🔴 **FAIL** - Fix N critical issues before submission

## Section Results

### 1. Outline Compliance: 3/3 ✓
### 2. Structure Requirements: 10/11 ⚠️
### 3. Readability Standards: 8/8 ✓
### 4. Value Proposition: 6/7 ⚠️
### 5. Technical Requirements: 4/4 ✓
### 6. Code Quality: 2/4 ✗
### 7. Image Quality: 5/7 ⚠️
### 8. Style and Formatting: 8/8 ✓

## Failed Items (MUST FIX)

### 6.1 Code Block Length
- ❌ Code block at line 245: 35 lines (MAX: 30)
- ❌ Code block at line 389: 42 lines (MAX: 30)

**Action Required**: Split these code blocks into smaller sections

## Warnings (SHOULD FIX)

### 2.3 Transitions and Flow
- ⚠️  Section "Advanced Patterns" lacks transition from previous section

### 4.1 Practical Focus
- ⚠️  Consider adding more numbered steps for configuration procedure

### 7.1 Resolution Requirements
- ⚠️  Image figure-3.png: 1800px shortest edge (target: 2000px)

## All Items Checked

[Detailed list of all checklist items with ✓/⚠️/✗ status]
```

---

## Notes

### Manual Review Items

Some checklist items require human judgment and cannot be fully automated:

- **Audience appropriateness**: Requires understanding of target reader level
- **Writing quality**: Conciseness, clarity, engagement
- **Value proposition**: Whether examples feel "real-world" vs contrived
- **Learning journey**: Whether content flows logically

These items should be marked "Manual Review Required" in automated checks.

### Critical vs Warning vs Info

**Critical (MUST FIX before submission)**:
- Code blocks >30 lines
- Images <2000px or <300 DPI
- JPG format images
- Missing summary section
- No [PACKT] styles applied

**Warning (SHOULD FIX before submission)**:
- Code blocks 21-30 lines (aim for ≤20)
- Images missing frame text
- Consecutive headers
- Missing transitions

**Info (NICE TO HAVE)**:
- Consider adding more visual variety
- Could add more real-world examples
- Might benefit from diagram

---

## Integration

This checklist is used by:
- **format-for-packtpub.md** task - Automated execution during conversion
- **manuscript-review.md** task - Manual content review process
- **chapter-development-workflow.yaml** - Final validation step before submission

## Related Files

- `format-for-packtpub.md` - Automates Markdown→PacktPub Word conversion
- `packtpub-author-bundle-analysis.md` - Detailed requirements documentation
- `validate-manuscript.py` - Automated validation script (to be created)
