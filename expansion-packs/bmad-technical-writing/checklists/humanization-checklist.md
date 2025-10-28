# Humanization Checklist

Use this checklist to validate that AI pattern removal was successful and chapter content reads as authentically human-written. This checklist validates REMOVAL of AI patterns (not detection—that's generative-ai-compliance-checklist.md).

**Purpose**: Confirm humanization task effectiveness after executing humanize-ai-drafted-chapter.md

**Distinction from Other Checklists**:
- **generative-ai-compliance-checklist.md**: DETECTS AI patterns (use before humanization)
- **humanization-checklist.md** (THIS): VALIDATES REMOVAL (use after humanization)
- **tone-consistency-checklist.md**: Validates tone specification compliance (different concern)

## Prerequisites

Before using this checklist:

- [ ] humanize-ai-drafted-chapter.md task has been executed
- [ ] Baseline AI pattern detection report available (from generative-ai-compliance-checklist.md)
- [ ] Access to ai-pattern-removal-guide.md for reference
- [ ] Chapter draft with humanization changes applied

## Scoring System

**Calculation**: (Items Passed / Total Items) × 100 = Humanization Pass Rate

**Thresholds**:
- **≥80%**: PASS - Ready for technical review
- **60-79%**: REVIEW - Some patterns remain, additional humanization recommended
- **<60%**: FAIL - Significant AI patterns remain, rework required

**AI Pattern Remaining Score**: Inverse of pass rate
- Pass rate 90% = 10% AI patterns remaining (excellent)
- Pass rate 80% = 20% AI patterns remaining (acceptable)
- Pass rate 60% = 40% AI patterns remaining (needs work)

**Target**: ≥80% pass rate (≤20% AI patterns remaining) for humanization step
**Copy-Edit Target**: ≥95% pass rate (≤5% AI patterns remaining) for final publication

---

## 1. Word Choice Validation

Validates AI vocabulary patterns have been removed.

### 1.1 AI Vocabulary Elimination

- [ ] **No overuse of "sophisticated"** (maximum 2 occurrences in entire chapter, 0-1 preferred)
- [ ] **No overuse of "delve"** (maximum 1 occurrence, 0 preferred)
- [ ] **No overuse of "leverage"** (maximum 2 occurrences, 0-1 preferred)
- [ ] **No overuse of "robust"** (maximum 2 occurrences, context-appropriate only)
- [ ] **No overuse of "seamless"** (maximum 2 occurrences, 0-1 preferred)
- [ ] **Other AI words minimized** (groundbreaking, revolutionary, cutting-edge, compelling, profound, meticulous, paradigm, synergy each ≤1)

**Validation Method**: Search chapter for each word, count occurrences, verify ≤ threshold

**If Failed**: Return to humanize-ai-drafted-chapter Step 3 (Remove AI Vocabulary Patterns)

### 1.2 Polysyllabic Simplification

- [ ] **Simple words preferred over complex** (use/utilize, help/facilitate, show/demonstrate ratio favors simple)
- [ ] **Technical precision maintained** (complex words used only when technically necessary)
- [ ] **Natural word choices** (words you'd use in conversation with colleague)

**Example Check**:
- ✓ "use this pattern" not "utilize this methodology"
- ✓ "help developers" not "facilitate developer enablement"
- ✓ "improves performance" not "optimizes operational efficiency"

**If Failed**: Return to humanize-ai-drafted-chapter Step 3

### 1.3 Vocabulary Variation

- [ ] **No single term repeated excessively** (check top 5 most common adjectives/verbs, none >5 occurrences)
- [ ] **Synonym variation used** (not same descriptor repeatedly)
- [ ] **Natural language diversity** (reads conversationally, not repetitively)

**If Failed**: Expand vocabulary with varied but simple alternatives

---

## 2. Metaphor Quality

Validates metaphor problems (overuse, nonsense, mixed) have been fixed.

### 2.1 Metaphor Density

- [ ] **Maximum 1-2 metaphors per major section** (not 4+ per paragraph)
- [ ] **Metaphors distributed naturally** (not clustered in introduction)
- [ ] **Overall metaphor count reasonable** (≤10 for typical chapter)

**Validation Method**: Count metaphors per section, ensure ≤2 per section

**If Failed**: Return to humanize-ai-drafted-chapter Step 4 (Fix Metaphor Problems)

### 2.2 Metaphor Clarity

- [ ] **No nonsensical metaphors** (all metaphors make logical sense)
- [ ] **No mixed metaphors** (metaphors in same context are consistent)
- [ ] **Metaphors enhance understanding** (each metaphor clarifies concept, not confuses)

**Example Check**:
- ✗ "Authentication tokens breathe life into security DNA" (nonsense)
- ✓ "Authentication tokens work like temporary security badges" (clear)

**If Failed**: Return to humanize-ai-drafted-chapter Step 4

### 2.3 Metaphor Necessity

- [ ] **Technical concepts clear without metaphors** (metaphor supplements, doesn't replace explanation)
- [ ] **Metaphors add value** (each metaphor genuinely helps understanding)
- [ ] **Can remove metaphors without losing clarity** (technical explanation stands alone)

**If Failed**: Remove unnecessary metaphors or strengthen technical explanations

---

## 3. Sentence Rhythm

Validates sentence structure uniformity has been broken.

### 3.1 Sentence Length Variation

- [ ] **Sentence lengths vary throughout chapter** (mix of short 5-10, medium 10-20, long 20-30+ words)
- [ ] **No monotonous length patterns** (not all 15-word sentences)
- [ ] **Strategic use of short sentences** (for emphasis, impact, clarity)

**Validation Method**: Sample 3 random paragraphs, measure sentence lengths, verify variation

**Example Check**:
- ✗ All sentences: 15, 16, 14, 17, 15, 16 words (uniform)
- ✓ Sentences: 8, 22, 12, 6, 19, 14 words (varied)

**If Failed**: Return to humanize-ai-drafted-chapter Step 5 (Introduce Sentence Rhythm Variation)

### 3.2 Sentence Structure Diversity

- [ ] **Structures vary** (simple, compound, complex, occasional fragments)
- [ ] **Not all subject-verb-object** (varied sentence openings and patterns)
- [ ] **Natural rhythm when read aloud** (sounds conversational, not robotic)

**Example Check**:
- ✗ "You configure X. You define Y. You establish Z. You verify W." (repetitive)
- ✓ "Configure X. Auth credentials go in Y. The connection pool needs Z—especially for production. Before proceeding, verify W." (varied)

**If Failed**: Return to humanize-ai-drafted-chapter Step 5

### 3.3 Reading Flow

- [ ] **Natural rhythm** (mix of sentence lengths creates flow)
- [ ] **Strategic pacing** (complex sentences for detail, short for emphasis)
- [ ] **Reads smoothly aloud** (no tongue-twister patterns or monotony)

**If Failed**: Read aloud, identify monotonous sections, vary structure

---

## 4. Voice Authenticity

Validates personal perspective and author expertise are evident.

### 4.1 Personal Perspective Present

- [ ] **First-person usage throughout** (minimum 3-5 instances per major section)
- [ ] **"I", "we", "my experience" present** (not entirely third-person)
- [ ] **Personal pronouns natural** (not forced, sounds authentic)

**Validation Method**: Search for "I ", " I'", "we ", "my ", count instances per section

**Minimum Threshold**: ≥1 first-person instance per major section (H2 heading)

**If Failed**: Return to humanize-ai-drafted-chapter Step 6 (Add Personal Voice and Author Perspective)

### 4.2 Author Expertise Evident

- [ ] **Real-world experiences shared** (specific projects, challenges, lessons learned)
- [ ] **Expert insights present** (opinions, recommendations, decisions explained)
- [ ] **Personal anecdotes included** (minimum 2-3 per chapter)
- [ ] **"War stories" or debugging experiences** (real scenarios from author's work)

**Example Check**:
- ✗ "Error handling is important" (generic, no expertise)
- ✓ "I learned the importance of error handling after a 2 AM production crash with no logs" (personal experience)

**If Failed**: Return to humanize-ai-drafted-chapter Step 6

### 4.3 Authentic Voice Maintained

- [ ] **Not impersonal documentation style** (reads like expert guidance, not reference manual)
- [ ] **Personality evident** (author's characteristic style present)
- [ ] **Conversational but professional** (natural expert voice)
- [ ] **Not generic or robotic** (sounds like real person wrote it)

**If Failed**: Inject more personality, personal perspective, authentic voice

---

## 5. Example Specificity

Validates generic examples have been replaced with specific, cited examples.

### 5.1 No Generic Placeholders

- [ ] **No "company X" or "a company"** (real company names or specific scenarios)
- [ ] **No "financial institution" vagueness** (specific entities named)
- [ ] **No uncited case studies** (all examples attributed or from author's experience)

**Validation Method**: Search for "company X", "a company", "financial institution", "case study" - should find 0 or have specific context

**If Failed**: Return to humanize-ai-drafted-chapter Step 7 (Replace Generic Examples)

### 5.2 Specific Examples with Details

- [ ] **Real-world examples specific** (actual companies, projects, or detailed scenarios)
- [ ] **Examples cited or attributed** (sources provided for external examples)
- [ ] **Author's own projects referenced** (personal work examples with specifics)

**Example Check**:
- ✗ "A company implemented caching and improved performance" (generic)
- ✓ "Netflix implemented Redis caching for their recommendation engine, reducing response time from 800ms to 120ms (Netflix Tech Blog, 2023)" (specific, cited)

**If Failed**: Return to humanize-ai-drafted-chapter Step 7

### 5.3 Example Relevance

- [ ] **All examples relevant to chapter topic** (not random or forced)
- [ ] **Examples support learning objectives** (tied to chapter goals)
- [ ] **Specific details provided** (not vague scenarios)

**If Failed**: Replace vague examples with specific, relevant ones

---

## 6. Content Depth

Validates filler has been removed and actionable insights added.

### 6.1 No Filler Content

- [ ] **Every paragraph adds value** (no paragraphs that could be deleted without loss)
- [ ] **No generic restatements** (not rehashing obvious points)
- [ ] **No repetitive content across sections** (each section unique)

**Validation Method**: Sample 5 random paragraphs, ask "if I removed this, would reader lose something?" - should be YES for all

**If Failed**: Return to humanize-ai-drafted-chapter Step 8 (Remove Filler and Increase Content Depth)

### 6.2 Actionable Insights Present

- [ ] **Every section provides actionable guidance** (reader can implement)
- [ ] **Concrete examples with code** (not just abstract concepts)
- [ ] **Specific recommendations** (clear guidance, not vague advice)

**Example Check**:
- ✗ "Error handling is important for production applications" (filler, no action)
- ✓ "Implement structured logging with correlation IDs—here's the pattern I use: [code example]" (actionable)

**If Failed**: Return to humanize-ai-drafted-chapter Step 8

### 6.3 Appropriate Content Density

- [ ] **Depth appropriate for expert technical book** (not surface-level tutorial)
- [ ] **Value beyond documentation** (insights, opinions, real-world context)
- [ ] **Reader gets expertise, not just information** (author's knowledge evident)

**If Failed**: Add deeper analysis, expert insights, real-world context

---

## 7. Structural Variation

Validates rigid, templated structure has been broken.

### 7.1 Section Opening Diversity

- [ ] **Section openings vary** (not all "In this section..." or identical pattern)
- [ ] **Mix of opening types** (question, statement, example, problem - not monotonous)
- [ ] **Natural, engaging openings** (draw reader in, not formulaic)

**Validation Method**: Check first sentence of each H2 section, verify no repeated pattern

**Example Check**:
- ✗ All sections start "In this section, we'll..." (rigid template)
- ✓ Mix: question opening, statement, example, problem (varied)

**If Failed**: Return to humanize-ai-drafted-chapter Step 9 (Break Rigid Structural Patterns)

### 7.2 Structure Feels Natural

- [ ] **Chapter structure organic** (not rigid template applied)
- [ ] **Section lengths vary based on content** (not all forced to same length)
- [ ] **Natural flow** (structure serves content, not vice versa)

**If Failed**: Return to humanize-ai-drafted-chapter Step 9

### 7.3 No Formulaic Language

- [ ] **No "Now we will..." repetition** (varied transitions)
- [ ] **No "In conclusion" or similar mechanical phrases** (natural flow)
- [ ] **Transitions varied** (see enhance-transitions.md patterns, not formulaic)

**If Failed**: Replace formulaic phrases with natural language

---

## Overall Assessment

After completing all sections, calculate final scores:

### Humanization Score Summary

```markdown
## Humanization Validation Results

**Chapter**: {{chapter_number}}
**Date**: {{date}}
**Reviewer**: {{name}}

### Category Scores

| Category | Passed | Total | Pass Rate |
|----------|--------|-------|-----------|
| Word Choice Validation | {{passed}} | 9 | {{percent}}% |
| Metaphor Quality | {{passed}} | 6 | {{percent}}% |
| Sentence Rhythm | {{passed}} | 6 | {{percent}}% |
| Voice Authenticity | {{passed}} | 6 | {{percent}}% |
| Example Specificity | {{passed}} | 6 | {{percent}}% |
| Content Depth | {{passed}} | 6 | {{percent}}% |
| Structural Variation | {{passed}} | 6 | {{percent}}% |

### Overall Results

**Total Passed**: {{passed}}/45
**Humanization Pass Rate**: {{percent}}%
**AI Pattern Remaining Score**: {{100 - percent}}%

**Status**:
- [ ] ✅ PASS (≥80% pass rate, ≤20% AI patterns) - Ready for technical review
- [ ] ⚠️ REVIEW (60-79% pass rate, 21-40% AI patterns) - Additional humanization recommended
- [ ] ❌ FAIL (<60% pass rate, >40% AI patterns) - Rework required

### Improvement from Baseline

**Baseline AI Score** (from generative-ai-compliance-checklist): {{baseline_score}}%
**Post-Humanization AI Score**: {{current_score}}%
**Improvement**: {{improvement}}% ({{baseline - current}})

**Target Achieved**:
- [ ] YES - AI score reduced by ≥50%
- [ ] NO - Additional humanization iteration needed
```

### Next Steps Based on Results

**If PASS (≥80%):**
1. Proceed to technical-review.md
2. Document humanization completion in chapter metadata
3. Note: Final AI pattern check will occur at copy-edit (Step 10)

**If REVIEW (60-79%):**
1. Identify top 3 failing categories
2. Return to relevant humanize-ai-drafted-chapter steps
3. Focus on critical issues (generic examples, impersonal voice)
4. Re-execute this checklist after fixes

**If FAIL (<60%):**
1. Review humanize-ai-drafted-chapter task completely
2. May need different humanization approach
3. Consider consulting with human editor
4. Re-execute entire humanization workflow
5. Validate baseline detection was accurate

---

## Red Flags: Humanization Not Successful

If you answer YES to multiple items below, humanization needs rework:

### Critical Red Flags (Must Fix)

- [ ] "sophisticated" appears >3 times in chapter
- [ ] No first-person perspective in entire chapter
- [ ] Generic "company X" or "financial institution" examples present
- [ ] All section openings identical formulaic pattern
- [ ] No personal anecdotes or real experiences
- [ ] Sentence lengths uniform throughout (all ~15 words)
- [ ] 4+ metaphors in single section

### Warning Red Flags (Strongly Recommend Fixing)

- [ ] AI vocabulary (delve, leverage, robust, seamless) appears >5 times combined
- [ ] <3 first-person instances in entire chapter
- [ ] Impersonal documentation style throughout
- [ ] Filler paragraphs still present (removable without loss)
- [ ] No variation in sentence structure
- [ ] No author insights or expertise evident

---

## Integration

This checklist is used by:

- **tutorial-architect** agent - After humanize-ai-drafted-chapter task execution
- **technical-editor** agent - During copy-edit-chapter Step 10 (final AI pattern check)
- **chapter-development-workflow** - Quality gate "humanization_complete"

## Related Files

- **humanize-ai-drafted-chapter.md** - Task this checklist validates
- **generative-ai-compliance-checklist.md** - Baseline AI pattern DETECTION (used before humanization)
- **ai-pattern-removal-guide.md** - Reference for HOW to fix each pattern type
- **copy-edit-chapter.md** - Step 10 uses this checklist for final validation (target <5% AI patterns)

---

## Notes

### Why This Checklist Exists

**Problem**: After AI-assisted drafting, content contains patterns readers notice and complain about.

**Solution**: humanize-ai-drafted-chapter.md systematically removes patterns.

**Validation**: This checklist confirms removal was successful.

**Goal**: Content reads as authentically human-written expert guidance.

### Key Distinctions

**This Checklist (Humanization) vs Compliance Checklist**:

| Aspect | generative-ai-compliance | humanization-checklist |
|--------|------------------------|----------------------|
| **Purpose** | DETECT AI patterns | VALIDATE REMOVAL |
| **When** | Before humanization | After humanization |
| **Output** | List of problems found | Pass/fail for each category |
| **Use** | Baseline measurement | Improvement validation |

**This Checklist vs Tone Consistency Checklist**:

| Aspect | Tone Consistency | Humanization |
|--------|-----------------|--------------|
| **Purpose** | Validate tone specification | Remove AI artifacts |
| **Focus** | Formality, voice consistency | Pattern elimination |
| **Question** | "Does tone match spec?" | "Does this sound AI-generated?" |

### Best Practices

**Using This Checklist Effectively**:

1. **Execute after humanization task** - Don't skip humanize-ai-drafted-chapter.md
2. **Compare to baseline** - Always measure improvement from detection report
3. **Be objective** - Use search/count validation methods, not just subjective feel
4. **Iterate if needed** - First pass may not achieve ≥80%, that's okay
5. **Focus on critical patterns** - Generic examples and impersonal voice are highest priority
6. **Document results** - Include in chapter metadata and change log

**Quality Threshold Philosophy**:

- **80% at humanization stage**: Acceptable for technical review to proceed
- **95% at copy-edit stage**: Required for publication (copy-edit Step 10)
- **100% impossible**: Some patterns acceptable in technical writing context
- **Residual patterns okay**: If technically necessary (e.g., "robust testing framework" is standard term)

### Common Questions

**Q: What if technical terminology matches "AI words"?**
A: Context matters. "Robust statistical model" is acceptable if industry-standard term. "Robust, sophisticated, seamless architecture leveraging cutting-edge paradigms" is AI overload. Use judgment.

**Q: Is any use of "sophisticated" or "leverage" forbidden?**
A: No. Threshold is ≤2 occurrences. Problem is OVERUSE (15+ times), not single contextual use.

**Q: What if author's natural voice is formal/verbose?**
A: Distinguish authentic author voice from AI patterns. If author always wrote formally, preserve that. But "profound efficacy in the empirical realm" is AI vocabulary, not authentic formality.

**Q: Can I pass with <80% if I have good reasons?**
A: Rare exceptions acceptable with justification. Document why certain patterns remain. But standard is ≥80% for good reason—readers notice AI patterns and complain.

### Remember

**Goal**: Authentic human expertise, not just passing a checklist.

**Success Criteria**:
- Reader can't tell AI was used in drafting
- Author's expertise and personality evident
- Content provides unique value beyond AI-generated tutorials
- Passes publisher review without AI-related concerns
- No negative reader reviews citing "AI-like" content

**Quality > Speed**: Take time to humanize properly. 2-4 hours per chapter is normal and worthwhile investment.
