# Checklist Reference

## Introduction

The BMad Technical Writing Expansion Pack provides **34 quality assurance checklists** that serve as validation gates throughout the book authoring lifecycle. Each checklist defines specific criteria that must be met before proceeding to the next phase.

This comprehensive reference documents all 34 checklists organized by phase, with:

- **Checklist name and purpose** - What it validates
- **When to use** - Quality gate timing
- **Key criteria** - Most important validation points
- **Pass criteria** - What constitutes passing
- **Related workflows** - Which workflows use this checklist
- **Related agents** - Which agents execute this checklist

### Checklist Categories

- **Planning Phase (3 checklists)** **(v2.1+ expanded)**: Learning objectives, prerequisites, research quality
- **Drafting Phase (6 checklists)** **(v2.1+ expanded)**: Chapter completeness, book proposals, tutorials, AI compliance
- **Code Quality (5 checklists)**: Code quality, testing, security, version compatibility, performance
- **Review Phase (4 checklists)**: Technical accuracy, readability, accessibility, inclusive language
- **Publishing Phase (8 checklists)** **(v2.1+ expanded)**: Publisher-specific formats, final manuscript, MEAP, self-publishing, repository integration
- **Final QA (8 checklists)**: Diagrams, screenshots, glossaries, indexes, citations, revisions, repositories, cross-platform

---

## Planning Phase Checklists

### learning-objectives-checklist.md

**Purpose**: Validates learning objectives are measurable and aligned with Bloom's taxonomy

**When to Use**: After defining learning objectives for chapter or book

**Key Criteria**:

- Learning objectives use action verbs (implement, analyze, create, evaluate)
- Objectives are specific and measurable
- Aligned with book-level learning path
- Appropriate for target audience skill level
- 3-5 objectives per chapter (not too few, not too many)
- Each objective maps to specific exercises or assessments

**Pass Criteria**: All objectives are measurable, actionable, and properly scoped

**Related Workflows**: Book Planning, Chapter Development, Tutorial Creation
**Related Agents**: instructional-designer, learning-path-designer, exercise-creator

---

### prerequisite-clarity-checklist.md

**Purpose**: Ensures prerequisites are clearly stated and achievable

**When to Use**: After defining chapter prerequisites or book prerequisites

**Key Criteria**:

- Prerequisites explicitly listed (no assumptions)
- Software/tool versions specified (e.g., "Python 3.11+")
- Prior chapters required are identified
- External knowledge assumptions stated
- Setup time estimated
- Prerequisites are achievable for target audience

**Pass Criteria**: Reader can verify they meet all prerequisites before starting

**Related Workflows**: Book Planning, Chapter Development
**Related Agents**: instructional-designer, tutorial-architect

---

### research-quality-checklist.md **(v2.1+)**

**Purpose**: Validates research findings are comprehensive, well-sourced, credible, and actionable

**When to Use**: After completing technical research for book or chapter planning

**Key Criteria**:

- All sources assessed for credibility (official documentation prioritized)
- Every technical claim has cited source
- All URLs accessible and valid
- Research questions answered or gaps documented
- Findings synthesized across multiple sources
- Conflicting information identified and resolved
- Research findings directly inform chapter content
- Code examples applicable to target audience
- Technical accuracy verified through source triangulation

**Pass Criteria**: Research findings are credible, comprehensive, and actionable for chapter development

**Related Workflows**: Book Planning Workflow, Research Workflow
**Related Agents**: technical-researcher

---

## Drafting Phase Checklists

### chapter-completeness-checklist.md

**Purpose**: Validates chapter has all required components before publication

**When to Use**: Final validation before marking chapter "Ready for Publication"

**Key Criteria**:

- All learning objectives addressed
- Introduction hooks reader and previews content
- All sections from outline present
- Code examples inline and explained
- Exercises included with difficulty progression
- Summary recaps key concepts
- Transitions to next chapter clear
- 3-5 diagrams/screenshots included (if applicable)
- Cross-references validated
- File list updated with all code files

**Pass Criteria**: Chapter meets all structural and content requirements

**Related Workflows**: Chapter Development, Chapter Assembly
**Related Agents**: tutorial-architect

---

### book-proposal-checklist.md

**Purpose**: Validates book proposal is complete and compelling for publishers

**When to Use**: Before submitting proposal to publisher

**Key Criteria**:

- Market analysis included (target audience, market size)
- Competitive titles identified (3-5 books)
- Unique value proposition clearly stated
- High-level chapter list (10-15 chapters typical)
- Author platform described (credentials, audience)
- Realistic timeline (12-18 months typical)
- Technical stack and versions specified
- Sample chapter or outline included

**Pass Criteria**: Proposal ready for publisher submission

**Related Workflows**: Book Planning
**Related Agents**: book-publisher

---

### tutorial-effectiveness-checklist.md

**Purpose**: Validates tutorials are clear, tested, and student-friendly

**When to Use**: After writing tutorial, before integration into chapter

**Key Criteria**:

- ONE clear learning objective stated
- Prerequisites explicitly listed
- 8-15 step-by-step instructions
- Each step has expected output documented
- Troubleshooting section included
- Tested in fresh environment
- Realistic time estimate (add 50-100% buffer for students)
- Success criteria verifiable at end
- Code copy-paste ready but encourages understanding

**Pass Criteria**: Tutorial tested successfully by someone following instructions exactly

**Related Workflows**: Tutorial Creation, Chapter Development
**Related Agents**: tutorial-architect, code-curator

---

### readability-checklist.md

**Purpose**: Ensures content is clear, accessible, and professional

**When to Use**: During copy editing phase

**Key Criteria**:

- Sentences are concise (20-25 words average)
- Paragraphs are scannable (3-5 sentences)
- Active voice used primarily
- Technical jargon defined on first use
- Transitions smooth between sections
- Consistent terminology throughout
- Code examples have clear context
- Headings are descriptive and hierarchical

**Pass Criteria**: Content reads clearly at target audience reading level

**Related Agents**: technical-editor

---

### exercise-difficulty-checklist.md

**Purpose**: Validates exercise difficulty progression and alignment

**When to Use**: After creating exercise sets

**Key Criteria**:

- Exercises aligned with learning objectives
- Difficulty progression (easy → medium → challenging)
- Mix of exercise types (guided, independent, challenges)
- Clear success criteria for each exercise
- Hints provided for challenging exercises
- Solutions available (or "hints only" if pedagogically appropriate)
- Time estimates realistic

**Pass Criteria**: Exercises build confidence and validate learning

**Related Agents**: exercise-creator

---

### generative-ai-compliance-checklist.md **(v2.1+)**

**Purpose**: Validates manuscript content does not trigger AI detection patterns and maintains human authenticity

**When to Use**: Before publisher submission (especially PacktPub), final manuscript review, self-review during writing

**Key Criteria**:

- All technical information verified for accuracy (no hallucinations)
- All code examples tested and working (not hypothetical)
- No generic vague examples ("company X", "financial institution")
- Real-world examples with specific details
- Authentic human voice and personal insights
- No repetitive phrasing or formulaic structure
- Author expertise and unique perspective evident
- Content demonstrates deep understanding beyond surface-level
- Writing style natural and conversational (not overly formal)
- Reader value clear throughout

**Pass Criteria**: Content reads as authentically human with unique expertise and insights

**Related Workflows**: Publisher Submission Workflows (PacktPub, O'Reilly, Manning), Final Manuscript Review
**Related Agents**: technical-editor, book-publisher

---

## Code Quality Checklists

### code-quality-checklist.md

**Purpose**: Validates code examples follow best practices and style guides

**When to Use**: After developing code examples, before integration

**Key Criteria**:

- Code follows language style guide (PEP 8, Airbnb JS, etc.)
- Variable and function names are descriptive
- Functions are appropriately sized (<50 lines typical)
- No code duplication (DRY principle)
- Comments explain "why" not "what"
- Error handling demonstrated
- Complexity reasonable for learning example
- Code is idiomatic (uses language features appropriately)

**Pass Criteria**: Code demonstrates best practices

**Related Workflows**: Code Example Workflow
**Related Agents**: code-curator

---

### code-testing-checklist.md

**Purpose**: Ensures all code examples are thoroughly tested

**When to Use**: After writing code, before marking example complete

**Key Criteria**:

- Code runs on target version (e.g., Python 3.11+)
- Edge cases tested
- Error conditions handled and tested
- Dependencies install cleanly
- Tests pass in fresh environment
- Test coverage adequate for example
- Output matches documented expectations
- Performance acceptable (if relevant)

**Pass Criteria**: All tests pass in clean environment

**Related Workflows**: Code Example Workflow, Section Development
**Related Agents**: code-curator, sample-code-maintainer

---

### security-best-practices-checklist.md

**Purpose**: Validates code examples follow secure coding practices

**When to Use**: Security review during code development

**Key Criteria**:

- No hardcoded secrets or credentials
- Input validation present where needed
- No SQL injection vulnerabilities
- No XSS vulnerabilities (web examples)
- Dependencies have no known CVEs
- Authentication/authorization demonstrated correctly
- HTTPS used (not HTTP) for web examples
- Error messages don't leak sensitive info

**Pass Criteria**: No security vulnerabilities identified

**Related Workflows**: Code Example Workflow, Technical Review
**Related Agents**: code-curator, technical-reviewer

---

### version-compatibility-checklist.md

**Purpose**: Ensures code works across specified versions

**When to Use**: Multi-version testing (e.g., Python 3.10, 3.11, 3.12)

**Key Criteria**:

- Code tested on all specified versions
- Breaking changes documented
- Version-specific workarounds provided if needed
- Dependencies compatible across versions
- Clear version requirements stated
- Deprecated features avoided (or flagged)
- Future-proofing considered

**Pass Criteria**: Code works on all specified versions

**Related Workflows**: Code Example Workflow, Book Edition Update
**Related Agents**: version-manager, code-curator

---

### performance-considerations-checklist.md

**Purpose**: Validates performance implications are addressed

**When to Use**: Technical review phase, especially for performance-critical examples

**Key Criteria**:

- Time complexity stated (Big-O notation)
- Space complexity stated where relevant
- Performance characteristics explained
- Optimization trade-offs discussed
- Scalability considerations addressed
- Benchmarks provided for performance-critical code
- Alternative approaches mentioned when relevant

**Pass Criteria**: Performance implications clearly explained

**Related Workflows**: Technical Review
**Related Agents**: technical-reviewer

---

## Review Phase Checklists

### technical-accuracy-checklist.md

**Purpose**: Validates technical correctness of content

**When to Use**: Technical review phase (primary quality gate)

**Key Criteria**:

- All technical claims verified against official documentation
- Code examples execute correctly
- No technical errors or misconceptions
- API usage follows current best practices
- Information is current (not outdated or deprecated)
- Facts are verifiable
- Links to official documentation provided
- Edge cases and limitations discussed

**Pass Criteria**: No critical technical errors identified

**Related Workflows**: Technical Review, Chapter Assembly
**Related Agents**: technical-reviewer

---

### accessibility-checklist.md

**Purpose**: Ensures content is accessible to all readers

**When to Use**: Editorial review and final manuscript review

**Key Criteria**:

- All images have descriptive alt text
- Color is not sole means of conveying information
- Code snippets have sufficient contrast
- Screen reader friendly formatting
- Inclusive examples (diverse names, scenarios)
- Clear heading hierarchy
- Abbreviations defined on first use
- Tables have header rows

**Pass Criteria**: Content meets accessibility standards (WCAG 2.1 AA)

**Related Workflows**: Technical Editor review, Final manuscript
**Related Agents**: technical-editor

---

### inclusive-language-checklist.md

**Purpose**: Validates use of inclusive, bias-free language

**When to Use**: Editorial review phase

**Key Criteria**:

- Gender-neutral language used (they/them instead of he/she)
- Diverse examples and scenarios
- Avoids ableist language
- Culturally sensitive terminology
- Avoids assumptions about reader background
- Inclusive character names in examples
- Welcoming tone for all skill levels

**Pass Criteria**: Content uses inclusive language throughout

**Related Agents**: technical-editor

---

### citation-accuracy-checklist.md

**Purpose**: Validates all citations, references, and attributions

**When to Use**: Final review before publication

**Key Criteria**:

- All external sources properly cited
- Code adapted from others has attribution
- Quotes have sources
- Links to original sources provided
- Copyright permissions obtained for images
- License compliance for code examples
- Bibliography/references section complete

**Pass Criteria**: All sources properly attributed

**Related Agents**: technical-editor

---

## Publishing Phase Checklists

### packtpub-submission-checklist.md

**Purpose**: Validates manuscript meets PacktPub requirements

**When to Use**: Before submitting to PacktPub

**Key Criteria**:

- Word format (.docx) or requested format
- Chapter count matches proposal
- PacktPub style guide followed
- Code repository URL provided
- Author bio and headshot included
- Sample chapters polished
- Technical depth appropriate for PacktPub audience
- Consistent formatting throughout

**Pass Criteria**: Manuscript ready for PacktPub submission

**Related Workflows**: PacktPub Submission
**Related Agents**: book-publisher, technical-editor

---

### oreilly-format-checklist.md

**Purpose**: Validates manuscript meets O'Reilly Atlas requirements

**When to Use**: Before submitting to O'Reilly

**Key Criteria**:

- AsciiDoc format (or Markdown if permitted)
- Chicago Manual of Style followed
- Atlas repository structure correct
- Code repository linked correctly
- Technical examples follow O'Reilly standards
- Callouts formatted correctly (notes, warnings, tips)
- Cross-references use correct syntax
- Images at appropriate resolution (300 DPI for print)

**Pass Criteria**: Manuscript ready for O'Reilly Atlas

**Related Workflows**: O'Reilly Submission
**Related Agents**: book-publisher, technical-editor

---

### manning-meap-checklist.md

**Purpose**: Validates chapter ready for Manning Early Access Program

**When to Use**: Before each MEAP chapter release

**Key Criteria**:

- Manning style guide followed
- Chapter technically complete
- Code tested and working
- Exercises included
- MEAP-specific formatting applied
- Revision history noted (for updated chapters)
- Chapter stands alone if needed (context provided)

**Pass Criteria**: Chapter ready for Manning MEAP release

**Related Workflows**: Manning MEAP
**Related Agents**: book-publisher

---

### meap-readiness-checklist.md

**Purpose**: General early access program readiness (any publisher)

**When to Use**: Before releasing chapters incrementally

**Key Criteria**:

- Chapter is self-contained
- Code repository accessible
- Known issues documented
- Feedback mechanism clear
- Version/date stamped
- Revision plan for feedback incorporation

**Pass Criteria**: Chapter ready for early access readers

**Related Agents**: book-publisher

---

### self-publishing-standards-checklist.md

**Purpose**: Validates self-published book meets professional standards

**When to Use**: Before self-publishing release

**Key Criteria**:

- Professional cover design
- ISBN obtained (if applicable)
- Copyright page complete
- Table of contents functional (ebook)
- Formatting consistent across platforms
- Code repository public and maintained
- Sales page compelling
- Pricing competitive
- Marketing materials ready

**Pass Criteria**: Book ready for self-publishing platforms

**Related Workflows**: Self-Publishing
**Related Agents**: book-publisher

---

### final-manuscript-checklist.md

**Purpose**: Comprehensive final validation before publication

**When to Use**: Final quality gate before publisher submission or self-publishing

**Key Criteria**:

- All chapters complete and reviewed
- Front matter complete (preface, introduction, TOC)
- Back matter complete (appendices, glossary, index)
- All code tested and repository public
- All images have alt text
- Cross-references validated
- No placeholder text (TODO, TBD, etc.)
- Acknowledgments section complete
- Copyright page accurate
- Version numbers final

**Pass Criteria**: Manuscript is publication-ready

**Related Agents**: book-publisher, technical-editor

---

### repository-integration-checklist.md **(v2.1+)**

**Purpose**: Validates code repository integration for Manning MEAP or publisher-required repositories

**When to Use**: Before Manning MEAP chapter releases, when publisher requires integrated code repository

**Key Criteria**:

- Git repository properly initialized and configured
- Repository structure follows publisher guidelines (Manning, O'Reilly, etc.)
- Chapter code organized in logical folder structure
- README.md provides clear setup instructions
- .gitignore configured appropriately
- LICENSE file included (if required)
- CI/CD pipeline configured and passing
- All code examples tested via CI
- Dependencies documented (requirements.txt, package.json, etc.)
- Code examples match manuscript exactly
- Git history clean (no sensitive data, large binaries)
- Repository publicly accessible (if required)
- Collaboration guidelines clear (CONTRIBUTING.md if accepting PRs)

**Pass Criteria**: Repository meets publisher integration requirements and all CI checks pass

**Related Workflows**: Manning MEAP Publishing Workflow, Publisher Submission Workflows
**Related Agents**: book-publisher, sample-code-maintainer

---

### index-completeness-checklist.md

**Purpose**: Validates book index is comprehensive

**When to Use**: After creating book index

**Key Criteria**:

- Key concepts indexed
- API/function names indexed
- Important code examples indexed
- Cross-references included
- Alphabetically organized
- Page numbers accurate
- No duplicate entries
- See/See also references appropriate

**Pass Criteria**: Index helps readers find information quickly

**Related Agents**: book-publisher

---

## Final QA Checklists

### diagram-clarity-checklist.md

**Purpose**: Validates diagrams are clear and helpful

**When to Use**: After creating diagrams

**Key Criteria**:

- Diagram supports text explanation
- Labels are legible
- Annotations clear
- Consistent styling across all diagrams
- Alt text descriptive
- High resolution (300 DPI for print)
- Colors have sufficient contrast
- Diagram type appropriate (flowchart, sequence, architecture, etc.)

**Pass Criteria**: Diagram clarifies concept effectively

**Related Agents**: screenshot-specialist

---

### screenshot-quality-checklist.md

**Purpose**: Validates screenshots meet quality standards

**When to Use**: After taking screenshots

**Key Criteria**:

- Screenshot shows relevant information clearly
- Text is legible
- Annotations guide reader's eye
- Consistent window/browser styling
- No sensitive information visible
- High resolution
- Cropped appropriately (no unnecessary UI)
- Platform noted if platform-specific

**Pass Criteria**: Screenshots enhance understanding

**Related Agents**: screenshot-specialist

---

### glossary-accuracy-checklist.md

**Purpose**: Validates glossary definitions are accurate and comprehensive

**When to Use**: After compiling glossary

**Key Criteria**:

- All technical terms defined
- Definitions accurate and clear
- Alphabetically organized
- Cross-references to related terms
- Consistent terminology with book
- Acronyms expanded
- No circular definitions

**Pass Criteria**: Glossary is helpful reference

**Related Agents**: api-documenter

---

### repository-quality-checklist.md

**Purpose**: Validates code repository meets professional standards

**When to Use**: Before publishing code repository

**Key Criteria**:

- README.md clear and comprehensive
- Installation instructions tested
- Folder structure logical
- All code tested and working
- Tests included
- LICENSE file present
- CONTRIBUTING.md (if accepting contributions)
- .gitignore appropriate
- CI/CD pipeline working
- Dependency versions pinned

**Pass Criteria**: Repository is professional and maintainable

**Related Agents**: sample-code-maintainer

---

### cross-platform-checklist.md

**Purpose**: Validates code works across platforms (Windows/macOS/Linux)

**When to Use**: Cross-platform testing phase

**Key Criteria**:

- Tested on Windows, macOS, Linux
- File paths use OS-agnostic methods
- Line endings handled correctly
- Platform-specific commands documented
- Dependencies install on all platforms
- No platform-specific bugs

**Pass Criteria**: Code works on all major platforms

**Related Agents**: version-manager, code-curator

---

### revision-completeness-checklist.md

**Purpose**: Validates all revision tasks complete for book updates

**When to Use**: Completing 2nd/3rd edition updates

**Key Criteria**:

- All outdated content updated
- Version migrations complete
- Deprecated code replaced
- New features covered
- Consistency with existing style maintained
- All reviewer feedback incorporated
- Revision history documented

**Pass Criteria**: Revision goals achieved

**Related Workflows**: Book Edition Update
**Related Agents**: book-analyst

---

### existing-book-integration-checklist.md

**Purpose**: Validates new content matches existing book style

**When to Use**: Adding chapters to existing book

**Key Criteria**:

- Voice and tone consistent
- Terminology matches existing chapters
- Code style follows existing patterns
- Format matches existing chapters
- Learning progression maintains flow
- Cross-references updated
- New chapter integrates smoothly

**Pass Criteria**: New content feels integrated, not appended

**Related Workflows**: Add Chapter to Existing Book
**Related Agents**: book-analyst, technical-editor

---

## Checklist Comparison Table

| Checklist                            | Phase        | Mandatory?         | Primary Agent          | Focus Area     |
| ------------------------------------ | ------------ | ------------------ | ---------------------- | -------------- |
| learning-objectives-checklist        | Planning     | Yes                | instructional-designer | Pedagogy       |
| prerequisite-clarity-checklist       | Planning     | Yes                | instructional-designer | Pedagogy       |
| chapter-completeness-checklist       | Drafting     | Yes                | tutorial-architect     | Completeness   |
| book-proposal-checklist              | Drafting     | Yes (if pitching)  | book-publisher         | Proposal       |
| tutorial-effectiveness-checklist     | Drafting     | Yes (if tutorials) | tutorial-architect     | Usability      |
| readability-checklist                | Drafting     | Yes                | technical-editor       | Clarity        |
| exercise-difficulty-checklist        | Drafting     | Yes (if exercises) | exercise-creator       | Pedagogy       |
| code-quality-checklist               | Code Quality | Yes                | code-curator           | Best practices |
| code-testing-checklist               | Code Quality | Yes                | code-curator           | Testing        |
| security-best-practices-checklist    | Code Quality | Yes                | code-curator           | Security       |
| version-compatibility-checklist      | Code Quality | Conditional        | version-manager        | Compatibility  |
| performance-considerations-checklist | Code Quality | Recommended        | technical-reviewer     | Performance    |
| technical-accuracy-checklist         | Review       | Yes                | technical-reviewer     | Accuracy       |
| accessibility-checklist              | Review       | Yes                | technical-editor       | Accessibility  |
| inclusive-language-checklist         | Review       | Yes                | technical-editor       | Inclusivity    |
| citation-accuracy-checklist          | Review       | Yes                | technical-editor       | Attribution    |
| packtpub-submission-checklist        | Publishing   | Conditional        | book-publisher         | Format         |
| oreilly-format-checklist             | Publishing   | Conditional        | book-publisher         | Format         |
| manning-meap-checklist               | Publishing   | Conditional        | book-publisher         | Format         |
| meap-readiness-checklist             | Publishing   | Conditional        | book-publisher         | Early Access   |
| self-publishing-standards-checklist  | Publishing   | Conditional        | book-publisher         | Quality        |
| final-manuscript-checklist           | Publishing   | Yes                | book-publisher         | Completeness   |
| index-completeness-checklist         | Publishing   | Conditional        | book-publisher         | Index          |
| diagram-clarity-checklist            | Final QA     | Recommended        | screenshot-specialist  | Visuals        |
| screenshot-quality-checklist         | Final QA     | Recommended        | screenshot-specialist  | Visuals        |
| glossary-accuracy-checklist          | Final QA     | Recommended        | api-documenter         | Reference      |
| repository-quality-checklist         | Final QA     | Yes                | sample-code-maintainer | Code           |
| cross-platform-checklist             | Final QA     | Conditional        | version-manager        | Compatibility  |
| revision-completeness-checklist      | Final QA     | Conditional        | book-analyst           | Updates        |
| existing-book-integration-checklist  | Final QA     | Conditional        | book-analyst           | Consistency    |

---

## Checklist Roadmap (Quality Gates by Phase)

### Phase 1: Planning

→ learning-objectives-checklist
→ prerequisite-clarity-checklist

### Phase 2: Drafting

→ chapter-completeness-checklist
→ tutorial-effectiveness-checklist (if tutorials)
→ exercise-difficulty-checklist (if exercises)
→ readability-checklist

### Phase 3: Code Development

→ code-quality-checklist
→ code-testing-checklist
→ security-best-practices-checklist
→ version-compatibility-checklist (if multi-version)

### Phase 4: Review

→ technical-accuracy-checklist (CRITICAL GATE)
→ performance-considerations-checklist
→ accessibility-checklist
→ inclusive-language-checklist
→ citation-accuracy-checklist

### Phase 5: Pre-Publication

→ diagram-clarity-checklist (if diagrams)
→ screenshot-quality-checklist (if screenshots)
→ glossary-accuracy-checklist (if glossary)
→ repository-quality-checklist
→ cross-platform-checklist (if multi-platform)

### Phase 6: Publication Prep

→ Publisher-specific checklist (PacktPub, O'Reilly, or Manning)
→ final-manuscript-checklist (FINAL GATE)
→ index-completeness-checklist (if print book)

---

## Quality Gate Recommendations

### Mandatory (Must Pass)

- learning-objectives-checklist
- prerequisite-clarity-checklist
- chapter-completeness-checklist
- code-quality-checklist
- code-testing-checklist
- security-best-practices-checklist
- technical-accuracy-checklist
- accessibility-checklist
- final-manuscript-checklist

### Highly Recommended

- readability-checklist
- inclusive-language-checklist
- repository-quality-checklist
- Publisher-specific checklist

### Conditional (Use When Applicable)

- book-proposal-checklist (if pitching)
- tutorial-effectiveness-checklist (if tutorials)
- exercise-difficulty-checklist (if exercises)
- version-compatibility-checklist (if multi-version)
- performance-considerations-checklist (if performance-critical)
- diagram/screenshot checklists (if visuals)
- glossary-accuracy-checklist (if glossary)
- index-completeness-checklist (if print)
- cross-platform-checklist (if multi-platform)
- revision/integration checklists (if brownfield)

---

## Conclusion

The BMad Technical Writing Expansion Pack's **34 quality checklists** provide comprehensive validation at every stage of book authoring. By using checklists as quality gates, you can:

- **Prevent defects early** through systematic validation
- **Maintain consistency** across chapters and versions
- **Meet professional standards** for publication
- **Ensure accessibility** and inclusivity
- **Validate technical accuracy** before release
- **Track quality** throughout the process

**Critical Checklists**:

- technical-accuracy-checklist - Non-negotiable quality gate
- code-testing-checklist - Ensures code reliability
- final-manuscript-checklist - Publication readiness
- accessibility-checklist - Universal access
- repository-integration-checklist **(v2.1+)** - Publisher code repository requirements
- generative-ai-compliance-checklist **(v2.1+)** - Human authenticity validation
- research-quality-checklist **(v2.1+)** - Research credibility validation

**Sprint 7 (v2.1) Additions**: 3 new checklists

- Repository Integration (Manning MEAP, publisher requirements)
- Generative AI Compliance (authenticity, reader satisfaction)
- Research Quality (credibility, actionability)

**Total checklist count**: 34 (31 v2.0 + 3 v2.1)
**Word count**: ~2,600 words

---

**Related Documentation**:

- [Agent Reference Guide](agent-reference.md) - Agents that execute checklists
- [Workflow Guide](workflow-guide.md) - Workflows that use checklists
- [Task Reference](task-reference.md) - Tasks that run checklists
- [User Guide](user-guide.md) - Quality gates in context
