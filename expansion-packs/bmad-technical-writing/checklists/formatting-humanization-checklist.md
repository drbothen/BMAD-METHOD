# Formatting Humanization Checklist

## Purpose

This checklist systematically identifies and corrects AI-generated formatting patterns (em-dashes, bolding, italics) that signal automated content creation. Apply this checklist during post-generation editing to transform mechanical formatting into natural, human-sounding patterns.

**Target**: Remove AI formatting tells while maintaining clarity and emphasis where genuinely needed.

---

## 1. Em-Dash Analysis (The "ChatGPT Dash")

### Count Em-Dashes

- [ ] Count total em-dashes in the document
- [ ] Calculate em-dashes per page (divide total by page count)
- [ ] **Target**: 1-2 em-dashes per page maximum
- [ ] **Flag if**: 3+ em-dashes per page (strong AI signal)

### Apply Substitution Test

For **each em-dash**, ask: "Could a period, semicolon, or comma work as well or better?"

- [ ] Review each em-dash individually
- [ ] Test alternative punctuation:
  - **Period**: Creates stronger separation, clearer boundary
  - **Semicolon**: Connects related independent clauses
  - **Comma**: Works for simpler connections or lists
- [ ] **Decision rule**: If alternative works equally well → Use alternative
- [ ] Only retain em-dash if it serves specific purpose:
  - [ ] Marks abrupt change in thought
  - [ ] Introduces explanation/example
  - [ ] Creates emphasis through interruption
  - [ ] Sets off crucial parenthetical information

### Em-Dash Reduction Actions

- [ ] **Replace 80-90%** of em-dashes with alternative punctuation
- [ ] Restructure sentences to eliminate need for em-dashes
- [ ] Break compound sentences into simpler sentences
- [ ] Use colons for introducing examples/explanations
- [ ] Verify final count: 1-2 per page maximum

### Em-Dash Distribution Check

- [ ] Remaining em-dashes are scattered, not clustered
- [ ] No paragraphs contain multiple em-dashes
- [ ] No predictable pattern (e.g., em-dash every 3rd paragraph)
- [ ] Em-dashes appear purposeful, not mechanical

---

## 2. Bold Text Humanization

### Bold Inventory

- [ ] Count total bolded elements in document
- [ ] Estimate percentage of content that is bolded
- [ ] **Target**: 2-5% of content bolded maximum
- [ ] **Flag if**: 10%+ of content bolded (AI pattern)

### Purposefulness Audit

For **each bolded element**, ask: "Does THIS need visual emphasis HERE?"

- [ ] **UI elements**: Yes, retain bolding (button names, menu items)
- [ ] **Critical warnings**: Yes, retain bolding (safety, errors, important notices)
- [ ] **Key terms (first use)**: Yes, retain bolding when being defined
- [ ] **Essential information**: Yes, retain if readers MUST notice
- [ ] **Decorative emphasis**: No, remove bolding
- [ ] **Repetitive patterns**: No, remove bolding (e.g., every function name)

### Bold Reduction Actions

- [ ] **Remove 50-70%** of current bolding
- [ ] Retain only genuinely critical elements
- [ ] Ensure similar elements are NOT all bolded (purposeful inconsistency)
- [ ] Use negative space effectively (unbolded similar content signals less importance)
- [ ] Verify final percentage: 2-5% or less

### Bold Distribution Check

- [ ] Bolding creates visual anchors for scanning, not decoration
- [ ] No mechanical pattern (every instance of X term bolded)
- [ ] Purposeful inconsistency exists (some similar elements bolded, others not)
- [ ] Bolding helps navigation without creating visual noise

---

## 3. Italic Text Humanization

### Italic Inventory

- [ ] Count total italicized elements/passages
- [ ] Identify what types of content receive italics
- [ ] **Flag if**: Italics appear with predictable frequency
- [ ] **Flag if**: Extended passages (3+ sentences) in italics

### Category Definition

Define 2-4 functional categories that should receive italics:

- [ ] **Publication titles**: (books, journals, software names)
- [ ] **Terms being defined**: (first use only)
- [ ] **Subtle emphasis**: (specific words requiring attention)
- [ ] **Foreign expressions**: (non-English terms)
- [ ] Other category: ________________

### Italic Reduction Actions

- [ ] Remove casual/decorative italics
- [ ] Remove italics from extended passages (break into shorter sentences or remove)
- [ ] Apply italics **only** to defined functional categories
- [ ] Ensure category consistency (all publication titles get italics, etc.)
- [ ] Verify no extended passages remain italicized

### Italic Distribution Check

- [ ] Italics serve functional purpose, not decoration
- [ ] Same element types receive consistent italic treatment
- [ ] No scattered italics without clear category
- [ ] Readability maintained (no multi-sentence italic passages)

---

## 4. Formatting Distribution (Burstiness)

### Section-Level Analysis

- [ ] Divide document into logical sections
- [ ] Calculate formatting density for each section:
  - Count: em-dashes + bolded elements + italicized elements
  - Divide by section word count
  - Note density per 100 words
- [ ] **Target**: Natural variation across sections (not uniform)

### Argumentative Asymmetry Check

- [ ] **Complex sections**: Should have MORE formatting (3-5 elements per 100 words)
- [ ] **Simple sections**: Should have LESS formatting (0-2 elements per 100 words)
- [ ] Formatting density reflects conceptual difficulty
- [ ] More emphasis where readers need guidance
- [ ] Less emphasis where content is straightforward

### Pattern Detection

- [ ] No uniform formatting density across all sections
- [ ] No predictable rhythm (formatting every N paragraphs)
- [ ] Variation reflects content needs, not mechanical pattern
- [ ] Deliberate inconsistency creates authenticity

### Distribution Adjustment Actions

- [ ] Increase formatting in complex sections if needed
- [ ] Reduce formatting in simple sections
- [ ] Create natural variation in formatting density
- [ ] Ensure variation serves reader comprehension

---

## 5. Overall Formatting Quality

### AI Pattern Red Flags

Check for these strong AI signals (should be ABSENT):

- [ ] **3+ em-dashes per page**: ❌ Strongest AI signal
- [ ] **Uniform bolding pattern**: ❌ (e.g., every command bolded)
- [ ] **Predictable formatting rhythm**: ❌ (formatting every N paragraphs)
- [ ] **Scattered italics**: ❌ (no clear functional purpose)
- [ ] **Consistent formatting depth**: ❌ (same density across all sections)
- [ ] **Formulaic transitions with em-dashes**: ❌ ("Furthermore — ", "Moreover — ")

### Human Pattern Indicators

Check for these human characteristics (should be PRESENT):

- [ ] ✅ Em-dash restraint (1-2 per page or fewer)
- [ ] ✅ Purposeful bold inconsistency (similar elements treated differently based on context)
- [ ] ✅ Functional italic categories (consistent within categories)
- [ ] ✅ Formatting variation across sections (burstiness)
- [ ] ✅ Argumentative asymmetry (more formatting for complex content)
- [ ] ✅ Each formatting choice serves clear purpose

### Final Quality Checks

- [ ] Formatting supports comprehension, doesn't distract from it
- [ ] Visual rhythm feels natural, not mechanical
- [ ] Formatting becomes invisible (readers notice content, not formatting)
- [ ] Professional polish maintained
- [ ] Technical accuracy preserved during formatting changes

---

## 6. Specialized Checks

### Technical Documentation Specific

- [ ] Code examples: Formatting consistent with language conventions
- [ ] Command names: Selective bolding (not all instances)
- [ ] File paths: Consistent monospace/code formatting
- [ ] Error messages: Appropriate formatting for severity

### Tutorial/Instructional Content

- [ ] Step numbers: Clear visual hierarchy without excessive bolding
- [ ] Expected outputs: Distinguished from code without italic overuse
- [ ] UI elements: Bolded for clarity in instructions
- [ ] Transitions between steps: Natural flow without em-dash reliance

### Academic/Formal Writing

- [ ] Citation formatting: Consistent with style guide
- [ ] Term definitions: Italics on first use only
- [ ] Emphasis: Minimal, purposeful only
- [ ] Section markers: Clear hierarchy without excessive decoration

---

## Success Criteria

### Em-Dashes
✅ **1-2 per page maximum**
✅ Each serves specific structural purpose
✅ Substitution test passed for all instances
✅ Natural distribution (not clustered or patterned)

### Bold Text
✅ **2-5% of content or less**
✅ Only genuinely critical elements bolded
✅ Purposeful inconsistency (similar elements treated contextually)
✅ Creates visual anchors without noise

### Italics
✅ **Functional categories only** (2-4 defined categories)
✅ Category consistency maintained
✅ No extended passages italicized
✅ No casual/decorative italics

### Distribution
✅ **Natural variation** across sections
✅ More formatting for complex content
✅ Less formatting for simple content
✅ No mechanical patterns detected

### Overall
✅ **Formatting invisible** - supports without distracting
✅ All AI red flags removed
✅ Human pattern indicators present
✅ Professional quality maintained
✅ Technical accuracy preserved

---

## Quick Reference: Red Flags vs. Green Flags

### 🚩 Red Flags (AI Patterns - Remove These)

| Element | AI Pattern | Remove |
|---------|-----------|--------|
| Em-dashes | 3+ per page, clustered | ✂️ Reduce to 1-2/page |
| Bold | 10%+ of content, mechanical pattern | ✂️ Cut 50-70% |
| Italics | Scattered, decorative, extended passages | ✂️ Define categories |
| Distribution | Uniform density across sections | ✂️ Create variation |

### ✅ Green Flags (Human Patterns - Keep These)

| Element | Human Pattern | Maintain |
|---------|--------------|----------|
| Em-dashes | 1-2 per page, purposeful | ✓ Keep restraint |
| Bold | 2-5%, contextual selection | ✓ Keep selectivity |
| Italics | Functional categories, consistent | ✓ Keep purpose |
| Distribution | Variable density, asymmetric | ✓ Keep variation |

---

## Workflow Integration

### When to Apply This Checklist

1. **Post-generation editing** - After AI-assisted content creation
2. **Copy editing phase** - During editorial review (Step 9 of copy-edit-chapter.md)
3. **Pre-publication QA** - Final quality check before submission
4. **Content humanization** - Systematic AI pattern removal

### Estimated Time

- **Quick scan**: 5-10 minutes (identify major patterns)
- **Full application**: 20-40 minutes per chapter (systematic correction)
- **Deep audit**: 60-90 minutes (comprehensive formatting overhaul)

### Tools

- **Manual count**: Simple but effective for em-dash audit
- **Find/replace**: Efficient for pattern identification
- **Section markers**: Help analyze distribution variation
- **Style guide reference**: Ensure compliance during changes

---

## Notes

**Priority Order**: Focus on em-dashes first (strongest AI signal), then bolding, then italics, then distribution.

**Technical Accuracy**: Never sacrifice correctness for formatting. If a technical term needs bolding for clarity, keep it bolded.

**Publisher Guidelines**: Check publisher-specific style requirements before final formatting decisions.

**Context Matters**: These guidelines apply to technical writing. Creative writing, marketing copy, or other domains have different standards.

**Iterative Process**: First pass removes obvious patterns. Second pass refines for natural variation. Third pass validates quality.
