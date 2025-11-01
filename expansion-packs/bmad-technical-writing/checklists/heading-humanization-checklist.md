# Heading Humanization Checklist

## Purpose

This checklist systematically identifies and corrects AI-generated heading patterns (hierarchy depth, mechanical parallelism, uniform density, verbose headings) that signal automated content creation. Apply this checklist during post-generation editing to transform mechanical heading structures into natural, human-sounding hierarchies that enhance navigation and comprehension.

**Target**: Remove AI heading tells while maintaining clarity and navigability for readers.

---

## 1. Heading Hierarchy Depth Analysis

### Count Heading Levels

- [ ] Extract all headings from document (H1 through H6)
- [ ] Identify deepest heading level used
- [ ] **Target**: 3 heading levels maximum (H1, H2, H3) for 15-20 page chapters
- [ ] **Flag if**: 4+ heading levels present (strong AI signal)

### Apply Flattening Test

For **each heading at H4 or deeper**, ask: "Can this be promoted to H3 or converted to body text?"

- [ ] Review each H4+ heading individually
- [ ] Test alternative structures:
  - **Promote to H3**: If content is substantial enough to warrant section status
  - **Convert to bold body text**: If content is minor detail within section
  - **Merge with parent**: If content is brief and can be integrated
  - **Remove heading entirely**: If structure adds no navigational value
- [ ] **Decision rule**: If H4+ serves no clear navigation purpose → Flatten to H3 or body text
- [ ] Only retain H4 if chapter is exceptionally complex (30+ pages) AND:
  - [ ] H4 genuinely improves navigation
  - [ ] Content cannot be presented clearly at H3
  - [ ] Reader would be lost without additional subdivision

### Hierarchy Flattening Actions

- [ ] **Reduce to 3 levels** (H1, H2, H3) for typical 15-20 page chapters
- [ ] Convert H5/H6 to body text with bold labels
- [ ] Promote essential H4 headings to H3 where appropriate
- [ ] Restructure content to eliminate need for deep nesting
- [ ] Verify final count: 3 levels maximum for most chapters

### Hierarchy Distribution Check

- [ ] H1: Chapter title only (exactly 1)
- [ ] H2: Major sections (4-7 typical for 15-20 page chapters)
- [ ] H3: Subsections where needed (0-6 per H2 section)
- [ ] H4: Rare or absent (only for exceptionally complex chapters)
- [ ] No skipped levels (never H1 → H3 without H2)

---

## 2. Mechanical Parallelism Detection

### Heading Structure Inventory

For **each heading level** (H2, H3), document grammatical patterns:

- [ ] Count headings at each level
- [ ] Identify grammatical structures used:
  - Gerunds: "Understanding X", "Configuring Y"
  - Imperatives: "Install X", "Configure Y"
  - Noun phrases: "Docker Basics", "Advanced Features"
  - Questions: "What Is X?", "How Does Y Work?"
  - Other patterns: Note specific structures
- [ ] **Flag if**: 80%+ of headings at same level use identical structure
- [ ] **Flag if**: All headings start with same word ("Understanding", "How to")

### Parallelism Audit

For **each heading level**, ask: "Do all headings follow the same grammatical pattern?"

- [ ] **H2 headings**: Are they mechanically parallel?
  - [ ] All start with "Understanding"? ❌ AI pattern
  - [ ] All start with "How to"? ❌ AI pattern
  - [ ] All use gerunds? ❌ AI pattern
  - [ ] Natural variation in structures? ✓ Human pattern
- [ ] **H3 headings**: Are they mechanically parallel?
  - [ ] All follow same formula? ❌ AI pattern
  - [ ] Vary based on content type? ✓ Human pattern

### Parallelism Breaking Actions

- [ ] **Rewrite 50%+ of headings** with different grammatical structures
- [ ] Match heading structure to content purpose:
  - **Conceptual sections**: Noun phrases ("State Management Fundamentals")
  - **Procedural sections**: Imperatives ("Configure the Server") or gerunds ("Configuring Options")
  - **Reference sections**: Noun phrases ("`useEffect` Hook Reference")
  - **Explanatory sections**: Questions ("Why Use Containers?") or statements ("How Containers Work")
- [ ] Remove redundant prefixes ("Understanding", "A Guide to", "An Introduction to")
- [ ] Create natural variation within each heading level
- [ ] Verify no single pattern dominates (target <60% same structure)

### Parallelism Distribution Check

- [ ] H2 headings use 3+ different grammatical structures
- [ ] H3 headings adapt structure to content type
- [ ] No predictable rhythm (not all alternating between two patterns)
- [ ] Headings feel natural when read in table of contents

---

## 3. Heading Density Asymmetry Analysis

### Subsection Count Inventory

- [ ] Count H3 subsections under each H2 major section
- [ ] Create distribution map (e.g., Section A: 3 subsections, Section B: 0 subsections, Section C: 5 subsections)
- [ ] Calculate average subsections per section
- [ ] **Flag if**: All sections have same or similar subsection counts (e.g., all have 3 H3s)
- [ ] **Flag if**: No section has 0 subsections (every H2 is subdivided)

### Complexity Assessment

For **each major section** (H2), evaluate content complexity:

- [ ] **Simple sections** (basic concepts, brief introductions):
  - Should have: 0-2 subsections
  - Content flows naturally without subdivision
  - Excessive headings would fragment simple narrative
- [ ] **Moderate sections** (standard explanations):
  - Should have: 2-4 subsections
  - Balance between flow and navigation
  - Headings provide helpful structure
- [ ] **Complex sections** (detailed procedures, multi-faceted topics):
  - Should have: 4-6 subsections
  - More headings aid comprehension and navigation
  - Readers benefit from smaller conceptual chunks

### Asymmetry Creation Actions

- [ ] **Remove subsections from simplest section**:
  - Identify least complex major section
  - Convert H3 subsections to flowing body text
  - Target: At least one H2 with 0-1 subsections
- [ ] **Add subsections to most complex section**:
  - Identify most difficult/detailed major section
  - Add H3 headings to break up dense content
  - Target: At least one H2 with 5-6 subsections
- [ ] **Create natural variation**: Subsection counts should vary across chapter
  - Example distribution: 0, 2, 3, 1, 5, 2 subsections
  - Not: 3, 3, 3, 3, 3, 3 (uniform = AI pattern)
- [ ] Verify variation reflects content complexity, not mechanical formula

### Density Distribution Check

- [ ] Subsection counts vary across chapter (not uniform)
- [ ] Simplest section has fewer subsections than complex section
- [ ] At least one section flows without subsections (0-1 H3s)
- [ ] Most complex section has more headings for navigation (4-6 H3s)
- [ ] Overall average: 2-4 headings per page

---

## 4. Heading Verbosity Reduction

### Heading Length Inventory

- [ ] Count words in each heading
- [ ] Identify headings with 8+ words
- [ ] Calculate average heading length by level:
  - H1 (Chapter title): ____ words average
  - H2 (Major sections): ____ words average
  - H3 (Subsections): ____ words average
- [ ] **Flag if**: 30%+ of headings exceed 8 words
- [ ] **Flag if**: Average H2/H3 length exceeds 7 words

### Verbosity Analysis

For **each long heading** (8+ words), identify bloat sources:

- [ ] Redundant phrases to remove:
  - [ ] "Understanding" / "An Understanding of"
  - [ ] "A Guide to" / "A Complete Guide to"
  - [ ] "How to" (can often be removed or shortened)
  - [ ] "Everything You Need to Know About"
  - [ ] "An Introduction to" / "Introduction to"
  - [ ] "The Fundamentals of"
  - [ ] "A Comprehensive Look at"
- [ ] Complete thoughts (headings should preview, not summarize):
  - [ ] Contains full sentence or multiple clauses
  - [ ] Includes explanatory context better suited to body text
- [ ] Unnecessary specificity (too much detail in heading):
  - [ ] Lists multiple items that could be single concept
  - [ ] Includes version numbers or technical details unnecessarily

### Shortening Actions

- [ ] **Remove redundant prefixes** from all headings:
  - "Understanding Docker Containers" → "Docker Containers"
  - "How to Configure Authentication" → "Configuring Authentication" or "Authentication Setup"
  - "An Introduction to State Management" → "State Management Basics"
- [ ] **Condense complete thoughts** to key concepts:
  - "Understanding the Fundamental Differences Between Synchronous and Asynchronous Processing" → "Synchronous vs Asynchronous Processing"
  - "How to Implement Secure Authentication Using OAuth 2.0" → "Implementing OAuth 2.0 Authentication"
- [ ] **Target word counts**:
  - H1 (Chapter): 3-6 words (max 10)
  - H2 (Sections): 3-5 words (max 8)
  - H3 (Subsections): 3-7 words (max 10)
- [ ] Verify shortened headings remain descriptive and clear

### Heading Length Check

- [ ] 80%+ of H2 headings are 3-7 words
- [ ] 80%+ of H3 headings are 3-7 words
- [ ] Average H2 length: 3-5 words
- [ ] Average H3 length: 3-7 words
- [ ] No headings exceed 10 words (rare exceptions for technical precision)

---

## 5. Heading Best Practices Validation

### Hierarchy Rules Compliance

- [ ] **No skipped levels**: Every heading follows proper hierarchy (H1 → H2 → H3, never H1 → H3)
- [ ] **No lone headings**: Each heading level has at least one sibling at same level
  - Exception: H1 chapter title (only one per chapter)
  - H2 sections: At least 2 H2 headings per chapter
  - H3 subsections: If one H3 exists under H2, add sibling or remove heading
- [ ] **No stacked headings**: Each heading has body text below it before next heading
  - Anti-pattern: H2 immediately followed by H3 with no text in between ❌
  - Correct: H2, introductory paragraph, then H3 ✓
- [ ] **Descriptive over functional**: Headings preview content, not just mark structure
  - Avoid: "Introduction", "Overview", "Summary", "Conclusion" (vague)
  - Prefer: "Getting Started with Docker", "API Design Principles", "Next Steps for Production" (specific)

### Content-Type Alignment

Verify heading density matches content type:

- [ ] **Conceptual sections** (explanations, theory):
  - Fewer headings (0-2 subsections typical)
  - Content flows as narrative
  - Excessive subdivision would disrupt flow
- [ ] **Procedural sections** (tutorials, how-to guides):
  - More headings (3-6 subsections typical)
  - Each heading marks task boundary or step
  - Readers benefit from clear procedural structure
- [ ] **Reference sections** (API docs, configuration options):
  - Structured headings for lookup (predictable pattern acceptable here)
  - Parallelism intentional for easy scanning
  - Consistent structure aids navigation
- [ ] **Mixed sections** (combining explanation and procedure):
  - Variable heading density
  - More headings for procedural parts, fewer for conceptual

### Accessibility and Navigation

- [ ] All headings would make sense in table of contents (scannable in isolation)
- [ ] Heading hierarchy supports screen reader navigation
- [ ] Headings provide clear chapter roadmap
- [ ] Readers can locate specific topics via headings alone

---

## 6. Overall Heading Quality

### AI Pattern Red Flags

Check for these strong AI signals (should be ABSENT):

- [ ] **4+ heading levels** in a chapter: ❌ Strongest AI hierarchy signal
- [ ] **Mechanical parallelism**: ❌ (all H2s start with "Understanding")
- [ ] **Uniform subsection counts**: ❌ (every H2 has exactly 3 H3s)
- [ ] **Verbose headings**: ❌ (30%+ of headings exceed 8 words)
- [ ] **Predictable heading rhythm**: ❌ (heading every 2 paragraphs mechanically)
- [ ] **No variation in density**: ❌ (same heading pattern for all content types)
- [ ] **Skipped levels or lone headings**: ❌ (hierarchy violations)
- [ ] **All sections subdivided**: ❌ (no H2 without H3 subsections)

### Human Pattern Indicators

Check for these human characteristics (should be PRESENT):

- [ ] ✅ Hierarchy restraint (3 levels for typical chapters)
- [ ] ✅ Natural structural variation (different grammatical structures)
- [ ] ✅ Argumentative asymmetry (subsection counts vary: 0, 2, 5, 1, 3, 2)
- [ ] ✅ Concise headings (3-7 words typical for H2/H3)
- [ ] ✅ Content-type adaptation (more headings for procedures, fewer for concepts)
- [ ] ✅ Descriptive headings (preview content clearly)
- [ ] ✅ Natural heading density (2-4 per page average, with variation)
- [ ] ✅ Each heading serves clear navigation purpose

### Final Quality Checks

- [ ] Heading hierarchy enhances comprehension, doesn't obstruct it
- [ ] Table of contents feels natural when read top-to-bottom
- [ ] Headings become invisible (readers notice content, not structure)
- [ ] Professional polish maintained (consistency where appropriate)
- [ ] Technical accuracy preserved during heading changes
- [ ] Heading structure aligns with original outline/chapter spec

---

## 7. Specialized Checks

### Technical Book Chapter Specific

- [ ] Chapter title (H1): Descriptive, not generic ("Chapter 3: Container Networking" not "Chapter 3")
- [ ] Major sections (H2): 4-7 sections typical for 15-20 page chapters
- [ ] Subsections (H3): Variable counts (0-6 per H2 based on complexity)
- [ ] Heading progression matches outline/chapter specification
- [ ] No heading structure divergence from approved spec without justification

### Tutorial/Procedural Content

- [ ] Task boundaries clearly marked with headings
- [ ] Step headings descriptive of action (not "Step 1", "Step 2")
- [ ] More headings acceptable for procedural clarity (4-6 headings per page)
- [ ] Heading structure supports sequential reading
- [ ] Each heading previews task or outcome

### Reference Documentation

- [ ] Parallelism intentional and functional (consistent structure aids lookup)
- [ ] Headings support quick navigation to specific items
- [ ] Alphabetical or logical ordering where appropriate
- [ ] Consistent heading pattern acceptable for reference material
- [ ] Structure optimized for scanning, not narrative flow

### Conceptual/Explanatory Content

- [ ] Fewer headings preferred (1-3 per page)
- [ ] Content flows as cohesive narrative
- [ ] Headings mark major conceptual shifts only
- [ ] Excessive subdivision avoided (disrupts explanatory flow)
- [ ] Natural reading rhythm maintained

---

## Success Criteria

### Hierarchy Depth
✅ **3 heading levels maximum** for 15-20 page chapters (H1, H2, H3)
✅ H4 rare or absent (only for exceptionally complex chapters)
✅ No skipped levels in hierarchy
✅ Each level serves clear navigation purpose

### Mechanical Parallelism
✅ **Natural variation** in heading structures (3+ different patterns per level)
✅ Headings adapted to content type (conceptual vs procedural)
✅ No single pattern dominates (less than 60% same structure)
✅ Headings feel natural in table of contents

### Density Asymmetry
✅ **Variable subsection counts** (0-6 H3s per H2, based on complexity)
✅ Simple sections have fewer subsections (0-2 typical)
✅ Complex sections have more subsections (4-6 typical)
✅ Average 2-4 headings per page with natural variation

### Heading Length
✅ **Concise headings** (3-7 words typical for H2/H3)
✅ Redundant prefixes removed ("Understanding", "How to", "A Guide to")
✅ Headings preview, don't summarize complete content
✅ Average H2: 3-5 words, Average H3: 3-7 words

### Best Practices
✅ **No hierarchy violations** (skipped levels, lone headings, stacked headings)
✅ Descriptive headings over functional headings
✅ Content-type alignment (density matches content purpose)
✅ Accessibility-friendly (screen reader navigation supported)

### Overall
✅ **Heading structure invisible** - supports without distracting
✅ All AI red flags removed
✅ Human pattern indicators present
✅ Professional quality maintained
✅ Technical accuracy preserved
✅ Alignment with chapter outline/specification

---

## Quick Reference: Red Flags vs. Green Flags

### 🚩 Red Flags (AI Patterns - Remove These)

| Element | AI Pattern | Remove |
|---------|-----------|--------|
| Hierarchy | 4-6 levels in chapter | ✂️ Flatten to 3 levels |
| Parallelism | All H2s: "Understanding X" | ✂️ Vary 50%+ structures |
| Density | Every H2 has 3 H3s (uniform) | ✂️ Create asymmetry (0, 2, 5, 1) |
| Length | 10+ words frequently | ✂️ Shorten to 3-7 words |
| Rhythm | Heading every 2 paragraphs | ✂️ Vary based on content |

### ✅ Green Flags (Human Patterns - Keep These)

| Element | Human Pattern | Maintain |
|---------|--------------|----------|
| Hierarchy | 3 levels (H1, H2, H3) | ✓ Keep restraint |
| Parallelism | Varied structures (3+ patterns) | ✓ Keep variation |
| Density | Asymmetric (0, 2, 5, 1, 3) | ✓ Keep flexibility |
| Length | 3-7 words typical | ✓ Keep conciseness |
| Rhythm | 2-4 per page avg, variable | ✓ Keep variation |

---

## Workflow Integration

### When to Apply This Checklist

1. **Post-generation editing** - After AI-assisted content creation
2. **Copy editing phase** - During editorial review (Step 10 of copy-edit-chapter.md)
3. **Chapter compilation** - When assembling full chapters from sections
4. **Pre-publication QA** - Final heading validation before submission
5. **Content humanization** - Systematic AI pattern removal

### Estimated Time

- **Quick scan**: 5-10 minutes (identify major hierarchy issues)
- **Full application**: 30-45 minutes per chapter (systematic heading correction)
- **Deep audit**: 60-90 minutes (comprehensive heading restructuring)

### Tools

- **Manual outline view**: Most effective for seeing full hierarchy
- **Table of contents generation**: Reveals heading structure issues
- **Find/replace**: Efficient for detecting parallelism patterns ("Understanding", "How to")
- **Word count**: Helps identify verbose headings quickly
- **Outline/chapter spec reference**: Ensures alignment with planned structure

---

## Notes

**Priority Order**: Focus on hierarchy depth first (strongest AI signal), then parallelism, then density asymmetry, then verbosity.

**Technical Accuracy**: Never sacrifice correctness for heading changes. If technical precision requires longer heading, keep it.

**Publisher Guidelines**: Check publisher-specific heading requirements before final decisions.

**Context Matters**: These guidelines apply to technical book chapters. Reference documentation and API docs may intentionally use parallelism for consistency.

**Iterative Process**: First pass flattens hierarchy and breaks obvious parallelism. Second pass creates asymmetry and shortens headings. Third pass validates against outline/spec.

**BMAD Workflow Integration**: Heading structure should align with Book Outline (H1), Chapter Outline (H2), and Section Spec (H3). Validate during Chapter Compile phase.
