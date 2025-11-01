# Technical Accuracy Preservation Checklist

<!-- Powered by BMAD™ Core -->

## Purpose

Ensure that humanization editing preserves 100% technical accuracy while improving naturalness and readability. This checklist provides systematic verification that no technical errors, inaccuracies, or misconceptions were introduced during the humanization process.

## When to Use

- **During humanization** - Reference to avoid introducing errors
- **After humanization editing** - Verify accuracy preservation
- **Before publication** - Final technical accuracy gate
- **During peer review** - Technical accuracy audit
- **When editing technical content** - Ongoing accuracy check

---

## Critical Principle

**NEVER sacrifice technical accuracy for style or naturalness.**

If improving readability or humanizing language would compromise technical correctness, preserve the accurate version. Technical precision always takes priority over stylistic preferences in technical writing.

---

## Section 1: Code Accuracy

### Code Examples Verification

For each code example in the document:

**Example 1**: (Line/Section: _______)

- [ ] Code compiles/runs without errors
- [ ] Code produces expected output
- [ ] Syntax is correct for stated language/version
- [ ] All imports/dependencies are correct
- [ ] Variable names are meaningful (not changed to be "cute")
- [ ] Comments are accurate and helpful

**Example 2**: (Line/Section: _______)

- [ ] Code compiles/runs without errors
- [ ] Code produces expected output
- [ ] Syntax is correct for stated language/version
- [ ] All imports/dependencies are correct
- [ ] Variable names are meaningful
- [ ] Comments are accurate and helpful

**Example 3**: (Line/Section: _______)

- [ ] Code compiles/runs without errors
- [ ] Code produces expected output
- [ ] Syntax is correct for stated language/version
- [ ] All imports/dependencies are correct
- [ ] Variable names are meaningful
- [ ] Comments are accurate and helpful

*(Continue for all code examples)*

### Code-Related Text Accuracy

- [ ] Code descriptions match what code actually does
- [ ] Function/method names spelled correctly in prose
- [ ] Parameter descriptions match actual parameters
- [ ] Return value descriptions are accurate
- [ ] Error handling described accurately

### Testing Verification

**Testing Method Used**:
- [ ] Copied code and ran in development environment
- [ ] Reviewed by experienced developer in the technology
- [ ] Compared against official documentation
- [ ] Verified in stated environment/version
- [ ] Other: _____________________________________

---

## Section 2: Technical Terminology

### Term Accuracy

**Critical Technical Terms** (verify each):

List key technical terms and verify accuracy:

- [ ] **Term**: _________________ - Definition accurate: Yes / No
- [ ] **Term**: _________________ - Definition accurate: Yes / No
- [ ] **Term**: _________________ - Definition accurate: Yes / No
- [ ] **Term**: _________________ - Definition accurate: Yes / No
- [ ] **Term**: _________________ - Definition accurate: Yes / No

### Terminology Consistency

- [ ] Same concept uses same term throughout
- [ ] No contradictory definitions across sections
- [ ] Technical terms not replaced with incorrect synonyms
- [ ] Abbreviations/acronyms defined before first use
- [ ] Standard terminology preferred over invented names

### Domain Convention Compliance

- [ ] Terminology matches industry-standard usage
- [ ] No mixing of terminology from different frameworks
- [ ] Language-specific conventions followed (e.g., camelCase vs snake_case)
- [ ] No archaic or deprecated terminology used

---

## Section 3: Factual Statements

### Technical Claims Verification

For each major technical claim:

**Claim 1**: "_____________________________________"
- [ ] Factually accurate
- [ ] Properly qualified (if conditional)
- [ ] Citations provided (if needed)
- [ ] Reflects current state (not outdated)

**Claim 2**: "_____________________________________"
- [ ] Factually accurate
- [ ] Properly qualified (if conditional)
- [ ] Citations provided (if needed)
- [ ] Reflects current state (not outdated)

**Claim 3**: "_____________________________________"
- [ ] Factually accurate
- [ ] Properly qualified (if conditional)
- [ ] Citations provided (if needed)
- [ ] Reflects current state (not outdated)

*(Continue for all major claims)*

### Best Practices Accuracy

- [ ] Stated "best practices" are actually current standards
- [ ] Practices apply to stated technology/version
- [ ] Context and limitations mentioned
- [ ] Alternative approaches acknowledged where applicable

### Performance Claims

**For any performance-related statements**:

- [ ] Claims are verifiable or properly qualified
- [ ] Metrics are accurate (if provided)
- [ ] Context specified (hardware, scale, etc.)
- [ ] No unsupported superlatives ("fastest," "best")

---

## Section 4: Version and Compatibility

### Version Accuracy

**Technology/Library/Tool Versions** (verify each mentioned):

- [ ] **Tool**: _________________ Version: _______ - Correct: Yes / No
- [ ] **Tool**: _________________ Version: _______ - Correct: Yes / No
- [ ] **Tool**: _________________ Version: _______ - Correct: Yes / No

### Version-Specific Features

- [ ] Features described exist in stated version
- [ ] No mixing of features from different versions
- [ ] Breaking changes acknowledged when relevant
- [ ] Deprecated features marked as such

### Compatibility Statements

- [ ] Compatibility claims are accurate
- [ ] Platform requirements stated correctly
- [ ] Dependency versions specified correctly
- [ ] Incompatibilities noted where applicable

---

## Section 5: API and Interface Accuracy

### API Usage

**For each API reference**:

**API 1**: (Name: _______________)

- [ ] Method/function names spelled correctly
- [ ] Parameters described accurately
- [ ] Parameter types are correct
- [ ] Return types are correct
- [ ] Example usage is valid
- [ ] Required vs. optional parameters marked correctly

**API 2**: (Name: _______________)

- [ ] Method/function names spelled correctly
- [ ] Parameters described accurately
- [ ] Parameter types are correct
- [ ] Return types are correct
- [ ] Example usage is valid
- [ ] Required vs. optional parameters marked correctly

*(Continue for all APIs)*

### Interface Descriptions

- [ ] Signatures match actual implementation
- [ ] Behavior descriptions are accurate
- [ ] Side effects mentioned where applicable
- [ ] Exception handling described correctly

---

## Section 6: Command and Configuration

### Command Accuracy

**For each command-line instruction**:

**Command 1**: `_____________________________________`

- [ ] Command syntax is correct
- [ ] Flags/options are accurate
- [ ] Works in stated environment (OS, shell)
- [ ] Produces described result
- [ ] Paths and filenames are correct

**Command 2**: `_____________________________________`

- [ ] Command syntax is correct
- [ ] Flags/options are accurate
- [ ] Works in stated environment
- [ ] Produces described result
- [ ] Paths and filenames are correct

*(Continue for all commands)*

### Configuration Accuracy

**For each configuration example**:

- [ ] Configuration syntax is valid
- [ ] Keys/properties spelled correctly
- [ ] Values are appropriate types
- [ ] Example would work if applied
- [ ] Matches stated version's config schema

---

## Section 7: Conceptual Accuracy

### Concept Explanations

**Core Concepts** (verify accuracy of each):

**Concept 1**: _____________________________________
- [ ] Explanation is technically correct
- [ ] Doesn't create misconceptions
- [ ] Appropriate level of simplification for audience
- [ ] Key characteristics accurately described

**Concept 2**: _____________________________________
- [ ] Explanation is technically correct
- [ ] Doesn't create misconceptions
- [ ] Appropriate level of simplification
- [ ] Key characteristics accurately described

*(Continue for all concepts)*

### Analogies and Metaphors

**If analogies/metaphors were added during humanization**:

- [ ] Analogies are accurate, not misleading
- [ ] Metaphors illuminate, don't obscure
- [ ] Limitations of analogy acknowledged if needed
- [ ] Don't oversimplify to point of inaccuracy

### Mental Models

- [ ] Mental models presented are valid
- [ ] Don't contradict actual implementation
- [ ] Useful for understanding, not misleading
- [ ] Clarify complex concepts without distorting

---

## Section 8: Procedures and Workflows

### Step-by-Step Accuracy

**For each procedure/tutorial**:

**Procedure 1**: _____________________________________

- [ ] Steps are in correct order
- [ ] No steps omitted
- [ ] Each step is technically accurate
- [ ] Prerequisites mentioned
- [ ] Expected outcomes match reality
- [ ] Troubleshooting advice is sound

**Procedure 2**: _____________________________________

- [ ] Steps are in correct order
- [ ] No steps omitted
- [ ] Each step is technically accurate
- [ ] Prerequisites mentioned
- [ ] Expected outcomes match reality
- [ ] Troubleshooting advice is sound

### Workflow Descriptions

- [ ] Workflows described match actual practice
- [ ] Sequence is logical and correct
- [ ] Dependencies and order constraints respected
- [ ] Edge cases and exceptions handled

---

## Section 9: Error and Warning Information

### Error Messages

**For each error message discussed**:

- [ ] Error message text is accurate
- [ ] Error code (if applicable) is correct
- [ ] Cause explanation is accurate
- [ ] Solution/resolution is valid
- [ ] Context (when error occurs) is correct

### Warning and Advisory Content

- [ ] Warnings are justified (real risks)
- [ ] Severity appropriately communicated
- [ ] Mitigation strategies are sound
- [ ] No unnecessary alarmism
- [ ] No missing critical warnings

---

## Section 10: Examples and Scenarios

### Example Validity

**For each example scenario**:

**Example 1**: _____________________________________

- [ ] Scenario is realistic and would work
- [ ] Technical details are accurate
- [ ] Demonstrates stated concept correctly
- [ ] Scale/complexity appropriate for point being made

**Example 2**: _____________________________________

- [ ] Scenario is realistic and would work
- [ ] Technical details are accurate
- [ ] Demonstrates stated concept correctly
- [ ] Scale/complexity appropriate

### Case Study Accuracy

**If case studies included**:

- [ ] Facts are verifiable or clearly hypothetical
- [ ] Technical implementation described accurately
- [ ] Results/outcomes are realistic
- [ ] Lessons drawn are valid

---

## Section 11: Security and Safety

### Security Statements

- [ ] Security advice is current and correct
- [ ] No insecure patterns recommended
- [ ] Vulnerabilities mentioned accurately
- [ ] Mitigations are effective
- [ ] No dangerous simplifications of security

### Safety-Critical Accuracy

**For safety-critical systems content**:

- [ ] All safety considerations mentioned
- [ ] No errors that could cause harm
- [ ] Standards and regulations referenced correctly
- [ ] Testing/validation requirements stated accurately

---

## Section 12: Cross-Reference Verification

### Internal References

- [ ] References to other sections are accurate
- [ ] Page/section numbers correct (if applicable)
- [ ] No broken references after editing
- [ ] Forward/backward references make sense

### External References

- [ ] URLs are valid and point to correct resources
- [ ] Documentation links are current
- [ ] Citations are accurate
- [ ] Version-specific links reference correct versions

---

## Section 13: Humanization-Specific Accuracy Risks

### Common Humanization Errors to Check

These errors often occur during humanization—verify none present:

**Vocabulary Changes**:
- [ ] Technical terms not replaced with incorrect synonyms
- [ ] Precision not lost in pursuit of "simpler" words
- [ ] No technical meanings altered by word substitution

**Sentence Restructuring**:
- [ ] Sentence changes didn't alter technical meaning
- [ ] Qualifiers (if, when, unless) not accidentally removed
- [ ] Conditional statements remain conditional
- [ ] Scope and applicability not changed

**Voice Addition**:
- [ ] Personal anecdotes (if added) are technically accurate
- [ ] "In my experience" statements are valid
- [ ] Generalizations from experience are appropriate
- [ ] No false claims added for authenticity

**Example Enhancement**:
- [ ] Made-up details are realistic and accurate
- [ ] Specific tools/versions mentioned actually work together
- [ ] "Realistic" scenarios would actually work
- [ ] Numbers and metrics are plausible

---

## Section 14: Edge Cases and Limitations

### Completeness of Caveats

- [ ] Important limitations mentioned
- [ ] Edge cases acknowledged where relevant
- [ ] "It depends" contexts clarified
- [ ] Trade-offs discussed honestly

### Scope Accuracy

- [ ] Content doesn't claim broader applicability than warranted
- [ ] Platform/environment specifics noted
- [ ] Assumptions clearly stated
- [ ] Boundary conditions mentioned

---

## Section 15: Testing and Validation

### Validation Method Documentation

**Record validation method used**:

- [ ] **Testing**: Code examples executed and verified
- [ ] **Documentation**: Compared against official docs
- [ ] **Expert Review**: Reviewed by subject matter expert
- [ ] **Community**: Checked against community best practices
- [ ] **Tools**: Validated using linters/validators
- [ ] **Other**: _____________________________________

### Validation Evidence

**Evidence of Accuracy** (attach or reference):

- [ ] Test results from code examples
- [ ] Expert reviewer sign-off
- [ ] Documentation references used
- [ ] Links to authoritative sources
- [ ] Other verification artifacts

---

## Overall Technical Accuracy Assessment

### Critical Issues (Must Fix)

List any technical inaccuracies found:

**CRITICAL** (incorrect facts, broken code, dangerous advice):
1. _____________________________________
2. _____________________________________
3. _____________________________________

**IMPORTANT** (misleading statements, incomplete information):
1. _____________________________________
2. _____________________________________

**MINOR** (typos in code, small clarifications needed):
1. _____________________________________
2. _____________________________________

### Accuracy Certification

**Final Verification**:

- [ ] All code examples tested and working
- [ ] All technical claims verified
- [ ] All terminology reviewed for accuracy
- [ ] All procedures tested or validated
- [ ] No inaccuracies introduced during humanization
- [ ] Technical reviewer sign-off obtained (if applicable)

**Certification Statement**:

- [ ] ✅ **TECHNICALLY ACCURATE** - Content verified 100% accurate
- [ ] ⚠️ **MINOR ISSUES** - Small corrections needed before publication
- [ ] ❌ **NOT ACCURATE** - Critical issues must be resolved

**Reviewer**: _____________________________________
**Date**: _____________________________________
**Notes**: _____________________________________

---

## Action Items

### Required Corrections

**Before Publication**:

1. _____________________________________
2. _____________________________________
3. _____________________________________

**Priority**: Critical / Important / Minor

### Follow-Up Validation

- [ ] Corrections made and re-verified
- [ ] Updated sections re-tested
- [ ] Final accuracy check completed
- [ ] Publication approved

---

## Related Resources

- **Tasks**: humanize-post-generation.md, analyze-ai-patterns.md
- **Checklists**: humanization-quality-checklist.md, ai-pattern-detection-checklist.md
- **Data**: humanization-techniques.md

---

## Notes

**Key Principles**:

1. **Technical accuracy is non-negotiable** - When in doubt, verify
2. **Test all code** - Never assume code works without testing
3. **Verify claims** - Check facts against authoritative sources
4. **Document validation** - Record how accuracy was verified
5. **Get expert review** - For complex technical content, have expert verify

**Common Pitfalls**:

- Changing technical terms to "synonyms" that aren't actually synonymous
- Simplifying explanations to point where they become wrong
- Adding specific details that seem realistic but are inaccurate
- Removing important qualifiers or context during editing
- Making code "more readable" in ways that break it

**Remember**: Better to keep slightly awkward but accurate language than to create beautiful prose that's technically wrong.
