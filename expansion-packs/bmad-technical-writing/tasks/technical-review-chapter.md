<!-- Powered by BMAD™ Core -->

# Technical Review Chapter

---

task:
id: technical-review-chapter
name: Technical Review Chapter
description: Comprehensive technical accuracy review with fact-checking, code validation, security audit, and best practices assessment
persona_default: technical-reviewer
inputs:

- chapter-draft
- chapter-number
- subject-area-expertise
  steps:
- Read chapter draft completely for overview
- Verify technical accuracy against official documentation
- Review all code examples for correctness and best practices
- Test code examples to ensure they run properly
- Check for security vulnerabilities in code
- Assess performance implications of recommendations
- Identify outdated information or deprecated features
- Note factual errors or misconceptions
- Compile findings into structured review report
- Assign severity levels to issues (Critical/Major/Minor)
- Provide constructive recommendations with sources
- Run execute-checklist.md with technical-accuracy-checklist.md
- Run execute-checklist.md with security-best-practices-checklist.md
- Run execute-checklist.md with performance-considerations-checklist.md
- Use template technical-review-report-tmpl.yaml with create-doc.md
  output: reviews/technical-review-chapter-{{chapter_number}}.md

---

## Purpose

This task performs a rigorous technical review to ensure all content is accurate, current, secure, and follows best practices. Technical reviewers act as subject matter experts validating the chapter's technical correctness before publication.

## Prerequisites

- Chapter draft completed
- Access to official documentation for technologies covered
- Subject matter expertise in chapter topics
- Code testing environment available
- Access to technical-writing-standards.md knowledge base

## Workflow Steps

### 1. Read Chapter Draft Completely

Get the full context before detailed review:

- Read entire chapter without stopping to take notes
- Understand the learning objectives
- Note the target audience level
- Identify all technologies and concepts covered
- Get a sense of overall quality

**Purpose:** Understand context before nitpicking details.

### 2. Verify Technical Accuracy

Check all technical claims against authoritative sources:

**For Each Technical Claim:**

- Is this factually correct?
- Is it current (not outdated)?
- Can it be verified in official documentation?
- Are version numbers specified correctly?

**Sources to Check:**

- Official language documentation (Python.org, MDN, etc.)
- Framework official docs
- RFCs and standards specifications
- API documentation
- Release notes

**Document Issues:**

- Location (section, page, paragraph)
- Incorrect statement
- Correct information
- Source reference
- Severity (Critical if wrong, Minor if imprecise)

**Use:** technical-accuracy-checklist.md

### 3. Review Code Examples for Correctness

Validate all code in the chapter:

**For Each Code Example:**

**Syntax and Logic:**

- Does the code have syntax errors?
- Will it run as shown?
- Does it produce the claimed results?
- Are there logic errors?

**Completeness:**

- Are all imports shown?
- Are dependencies clear?
- Is setup code included or explained?
- Can a reader actually run this?

**Accuracy:**

- Does the code use APIs correctly?
- Are parameters in the right order?
- Are return types correct?
- Is error handling appropriate?

**Action:** Copy code to test environment and run it!

### 4. Check Best Practices

Assess whether code follows current best practices:

**Code Quality:**

- Follows language style guides (PEP 8, ESLint, etc.)
- Uses meaningful variable names
- Includes appropriate comments
- Avoids deprecated features
- Handles errors properly

**Design Patterns:**

- Uses appropriate patterns
- Avoids anti-patterns
- Demonstrates scalable approaches
- Shows proper separation of concerns

**Modern Approaches:**

- Uses current language features
- Leverages modern libraries
- Follows framework conventions
- Demonstrates industry standards

**Note:** Balance teaching clarity with production quality - sometimes simple is better for learning.

### 5. Identify Security Concerns

Review for security vulnerabilities:

**Critical Issues:**

- Hardcoded credentials or API keys
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Insecure authentication
- Missing input validation
- Unsafe deserialization

**Best Practices:**

- HTTPS/TLS usage
- Password hashing (bcrypt, Argon2)
- JWT secret management
- API rate limiting
- Logging security events
- Principle of least privilege

**For Each Security Issue:**

- Describe the vulnerability
- Explain potential impact
- Provide secure code example
- Reference security standard (OWASP, CWE)
- Mark severity (Critical for exploitable issues)

**Use:** security-best-practices-checklist.md

### 6. Assess Performance Implications

Consider performance and scalability:

**Inefficiencies:**

- O(n²) algorithms where O(n) is possible
- N+1 query problems
- Missing database indexes
- Unnecessary iterations or computations
- Memory leaks or excessive allocation

**Scalability:**

- Will this approach scale to production?
- Are there resource constraints?
- Is caching appropriate?
- Are there blocking operations in async code?

**Recommendations:**

- Better algorithms or data structures
- Optimization techniques
- Profiling suggestions
- When optimization matters vs premature optimization

**Use:** performance-considerations-checklist.md

### 7. Note Outdated Information

Check currency of all technical content:

**Deprecated Features:**

- Language features no longer recommended
- Framework APIs deprecated
- Tools superseded by newer alternatives

**Version Issues:**

- Library versions outdated or EOL
- Examples using old syntax
- Missing modern alternatives

**Update Recommendations:**

- Current best practices
- Modern equivalents
- Migration paths
- Version updates needed

**Example:** "Using React class components; recommend hooks-based functional components (current standard since React 16.8)"

### 8. Compile Findings into Review Report

Create structured technical review report:

**Use template:** technical-review-report-tmpl.yaml

**Report Sections:**

- Executive summary (overall assessment)
- Technical accuracy findings
- Code quality issues
- Security concerns
- Performance considerations
- Best practices assessment
- Outdated information
- Positive findings (what worked well)
- Prioritized recommendations

**Assign Severity:**

- **Critical:** Must fix (factual errors, security issues, broken code)
- **Major:** Should fix (best practice violations, performance issues)
- **Minor:** Nice to fix (style improvements, optimization suggestions)

### 9. Provide Constructive Recommendations

For each issue, provide actionable guidance:

**Good Feedback Format:**

```
Location: Section 2.3, page 12, code example
Issue: Using `collections.MutableMapping` which is deprecated
Severity: Major
Recommendation: Use `collections.abc.MutableMapping` instead (Python 3.3+)
Source: https://docs.python.org/3/library/collections.abc.html
Fixed Code:
from collections.abc import MutableMapping
class MyDict(MutableMapping):
    ...
```

**Be Constructive:**

- Explain why it's wrong
- Show how to fix it
- Provide source reference
- Offer example code where helpful

**Avoid:**

- Vague criticism ("this is bad")
- Nitpicking without explaining why
- Rewriting the entire chapter
- Focusing only on negatives

### 10. Run Technical Checklists

Validate against standard checklists:

**Execute:**

- technical-accuracy-checklist.md
- security-best-practices-checklist.md
- performance-considerations-checklist.md

**Document** any checklist items that fail.

## Output

Technical review report should include:

- Clear severity ratings for all issues
- Specific locations for every finding
- Actionable recommendations with examples
- Source references for claims
- Overall assessment (Ready/Needs Revision/Major Rework)
- Estimated effort to address issues

## Quality Standards

Effective technical review:

✓ Verifies every technical claim
✓ Tests all code examples
✓ Identifies security vulnerabilities
✓ Provides constructive feedback
✓ Includes source references
✓ Prioritizes issues by severity
✓ Offers concrete solutions
✓ Maintains respectful, professional tone

## Next Steps

After technical review:

1. Deliver review report to author
2. Author addresses issues based on priority
3. Re-review critical fixes (optional)
4. Approve chapter to proceed to copy editing
5. May participate in final publication review
