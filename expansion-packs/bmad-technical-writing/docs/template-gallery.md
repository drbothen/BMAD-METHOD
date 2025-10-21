# Template Gallery

## Introduction

The BMad Technical Writing Expansion Pack provides **18 YAML templates** that structure documentation creation across the entire book authoring lifecycle. Each template defines sections with embedded LLM instructions, ensuring consistent, high-quality output.

This comprehensive gallery showcases all 18 templates organized by category, with:

- **Template name and description** - What the template creates
- **Purpose** - When and why to use it
- **Related workflows** - Which workflows use this template
- **Related agents** - Which agents execute this template
- **Sample output** - Filled template examples showing structure
- **Customization notes** - How to adapt the template

### Template Categories

- **Planning Templates (3)**: Book proposals, outlines, chapter planning
- **Chapter Content Templates (5)**: Section plans, drafts, introductions, prefaces, appendices
- **Code Templates (2)**: Code examples, API reference
- **Learning Templates (2)**: Learning objectives, exercise sets
- **Tutorial Templates (1)**: Tutorial sections
- **Review Templates (2)**: Technical reviews, revision plans
- **Visual Templates (1)**: Diagram specifications
- **Documentation Templates (2)**: Glossaries, book analysis reports

---

## Planning Templates

### Book Outline Template

**ID**: `book-outline-tmpl.yaml`
**Output**: `{book_title}-outline.md`
**Elicitation**: Required

#### Purpose

Creates complete book structure with learning path and chapter-by-chapter breakdown. Used at the start of book planning to define pedagogical progression and content scope.

#### When to Use

- Planning new technical book from scratch
- Pitching book proposal to publisher (use with book-proposal-tmpl)
- Need structured learning progression across chapters
- Validating book concept before writing

#### Sections Defined

1. **Book Metadata** - Title, audience, prerequisites, outcomes, length, publisher, tech stack
2. **Front Matter Plan** - Preface, about author, conventions, setup instructions
3. **Part/Section Organization** - Grouping chapters into parts with learning arcs
4. **Chapter-by-Chapter Outline** - Objectives, topics, exercises, code examples, page counts
5. **Learning Path Progression** - Difficulty increase, scaffolding, Bloom's taxonomy mapping
6. **Back Matter Plan** - Appendices, glossary, index, resources
7. **Code Repository Plan** - Folder structure, testing strategy, version support

#### Related Workflows

- Book Planning Workflow (primary)
- Chapter Development Workflow (uses this as input)

#### Related Agents

- **instructional-designer** (creates this)
- **tutorial-architect** (uses for chapter planning)

#### Sample Output

```markdown
# Python Data Structures Handbook - Book Outline

## Book Metadata

**Title**: Python Data Structures Handbook: Mastering Lists, Dictionaries, Sets, and Beyond
**Subtitle**: A Practical Guide to Python's Built-in Data Structures
**Target Audience**: Intermediate Python developers (1-2 years experience)
**Prerequisites**:
- Python 3.10+ installed
- Basic Python syntax (variables, functions, control flow)
- Object-oriented programming fundamentals

**Learning Outcomes**:
By the end of this book, readers will:
- Master Python's built-in data structures (lists, tuples, dictionaries, sets)
- Implement custom data structures (stacks, queues, trees, graphs)
- Analyze time and space complexity of data structure operations
- Choose optimal data structures for specific use cases
- Optimize performance using appropriate structures

**Estimated Length**: 350-400 pages
**Publisher Target**: O'Reilly Media
**Technology Stack**: Python 3.11+, pytest for testing

## Part Structure

**Part I: Built-in Data Structures** (Chapters 1-5)
Foundation in Python's core data structures. Readers master lists, tuples, dictionaries, and sets before moving to advanced topics.

**Part II: Custom Data Structures** (Chapters 6-9)
Implementation of classic computer science data structures. Builds on Part I concepts to create stacks, queues, trees, and graphs.

**Part III: Real-World Applications** (Chapters 10-12)
Practical applications and performance optimization. Readers apply knowledge to solve real problems efficiently.

## Chapter-by-Chapter Outline

### Chapter 1: List Fundamentals

**Learning Objectives**:
- Implement common list operations (indexing, slicing, concatenation)
- Analyze time complexity of list methods (append, insert, pop)
- Apply list comprehensions for data transformation

**Topics Covered**:
- List creation and initialization
- Indexing and slicing operations
- Common methods (append, extend, insert, remove, pop)
- List comprehensions and filtering
- Performance characteristics (O(1) append vs O(n) insert)

**Tutorials/Exercises**:
- Build a shopping cart system using lists
- Implement a simple task manager
- Performance comparison exercises

**Code Examples**:
- list-basics.py - Basic operations
- list-comprehensions.py - Advanced filtering
- list-performance.py - Benchmark different operations

**Estimated Pages**: 25-30
**Prerequisites**: None (first chapter)
**Difficulty**: Beginner

### Chapter 2: Dictionary Mastery

**Learning Objectives**:
- Implement dictionary operations for key-value storage
- Evaluate when to use dictionaries vs other structures
- Create nested dictionaries for complex data

**Topics Covered**:
- Dictionary creation and access patterns
- Common methods (get, keys, values, items)
- Dictionary comprehensions
- Handling missing keys (defaultdict, get method)
- Nested dictionaries and JSON-like structures

**Tutorials/Exercises**:
- Build a contact management system
- Parse and transform JSON data
- Implement a caching system

**Code Examples**:
- dict-operations.py - Core operations
- dict-advanced.py - Nested structures
- dict-performance.py - Hash table performance

**Estimated Pages**: 30-35
**Prerequisites**: Chapter 1
**Difficulty**: Beginner

[... Continues for remaining 10 chapters ...]

## Learning Path Progression

**Beginner (Chapters 1-5)**: Built-in data structures with clear tutorials
- Remember: Recall syntax and methods
- Understand: Explain when to use each structure
- Apply: Implement in practice exercises

**Intermediate (Chapters 6-9)**: Custom implementations
- Analyze: Compare time/space complexity
- Evaluate: Choose optimal structures
- Create: Build custom data structures

**Advanced (Chapters 10-12)**: Real-world optimization
- Optimize: Performance tuning
- Design: System architecture decisions

## Back Matter Plan

**Appendix A**: Big-O Complexity Reference (Quick lookup table)
**Appendix B**: Python 3.11+ New Features (Relevant to data structures)
**Appendix C**: Performance Benchmarking Tools

**Glossary**: ~50 terms (amortized complexity, hash collision, etc.)
**Index**: Focus on data structures, methods, performance topics

## Code Repository Plan

```
python-data-structures-handbook/
├── README.md (Installation, testing instructions)
├── chapter-01/ (List fundamentals)
│   ├── list-basics.py
│   ├── list-comprehensions.py
│   ├── tests/
├── chapter-02/ (Dictionaries)
│   ├── dict-operations.py
│   ├── dict-advanced.py
│   ├── tests/
[... continues ...]
├── .github/workflows/test.yml (CI/CD)
├── requirements.txt (Python 3.11+, pytest)
└── Makefile (test, lint commands)
```

**Testing Strategy**: Unit tests for all code examples, pytest framework
**Version Support**: Python 3.11+
**CI/CD**: GitHub Actions runs tests on 3.11, 3.12
```

---

### Book Proposal Template

**ID**: `book-proposal-tmpl.yaml`
**Purpose**: Creates comprehensive publisher proposal with market analysis
**Related Workflows**: Book Planning Workflow
**Related Agents**: book-publisher

---

### Chapter Outline Template

**ID**: `chapter-outline-tmpl.yaml`
**Output**: `chapter-{n}-outline.md`
**Elicitation**: Required

#### Purpose

Creates detailed single chapter structure with learning objectives, sections, exercises, and code examples. Used before writing chapter content.

#### Sample Output (Excerpt)

```markdown
# Chapter 3: Set Operations and Applications

## Chapter Metadata

**Chapter Number**: 3
**Estimated Pages**: 28-32
**Time to Complete**: 2-3 hours
**Difficulty**: Intermediate
**Part**: Part I - Built-in Data Structures

## Learning Objectives

1. **Implement** set operations (union, intersection, difference, symmetric difference)
2. **Analyze** when sets provide performance advantages over lists
3. **Apply** sets to solve duplicate detection and membership testing problems

## Prerequisites

- Chapter 1: List Fundamentals (completed)
- Chapter 2: Dictionary Mastery (completed)
- Understanding of hash tables (covered in Chapter 2)
- Python 3.11+ installed with pytest

## Introduction Section

**Hook**: "Have you ever needed to find unique users across multiple datasets, or check if an element exists in a collection instantly? Sets are Python's secret weapon for these scenarios."

**Overview**: This chapter explores Python sets—unordered collections optimized for membership testing and eliminating duplicates. We'll implement mathematical set operations, compare performance against lists, and build practical applications.

**Real-World Use Cases**:
- Deduplicating data streams
- Access control (checking user permissions)
- Finding common elements across datasets
- Graph algorithms (tracking visited nodes)

## Main Content Sections

### Section 1: Set Fundamentals (6-7 pages)
- Set creation and initialization
- Add, remove, discard methods
- Membership testing with `in` operator
- Performance: O(1) lookup vs O(n) list search
- **Code**: `set-basics.py` - Core operations
- **Diagram**: Hash table visualization

### Section 2: Set Operations (8-10 pages)
- Union, intersection, difference, symmetric difference
- Operator syntax (|, &, -, ^) vs method syntax
- Subset and superset testing
- **Code**: `set-operations.py` - Mathematical operations
- **Tutorial**: Building a permission system with sets

### Section 3: Practical Applications (8-10 pages)
- Deduplication strategies
- Fast membership testing
- Set comprehensions
- Frozen sets for immutability
- **Code**: `set-applications.py` - Real-world examples
- **Tutorial**: Finding common followers across social networks

## Exercises & Challenges

**Guided Exercises**:
1. Implement user access control (15 min)
2. Deduplicate log entries (20 min)
3. Find common items in shopping carts (15 min)

**Challenge Problems**:
1. Optimize a slow list-based search (30 min)
2. Build a simple graph traversal using sets (45 min)

**Solutions**: Hints provided in appendix, full solutions in repository

## Code Files List

- `set-basics.py` - Set creation and core operations (Python 3.11+)
- `set-operations.py` - Mathematical set operations
- `set-applications.py` - Practical examples (deduplication, permissions)
- `tests/test_sets.py` - Unit tests for all examples
```

---

## Chapter Content Templates

### Section Plan Template

**ID**: `section-plan-tmpl.yaml`
**Output**: `section-{n}.md`
**Elicitation**: Not required (filled by agent)

#### Purpose

Defines one deliverable section (2-5 pages) with acceptance criteria. This is the "story" unit of section-driven development, enabling incremental chapter progress tracking.

#### When to Use

- Breaking chapter into work units
- Using section-driven development workflow
- Want clear "DONE" criteria for each section
- Tracking incremental progress ("5 of 8 sections complete")

#### Sample Output

```markdown
# Section Plan: Section 3.2 - Set Operations

## Section Metadata

**Section ID**: section-3.2
**Section Title**: Mathematical Set Operations
**Chapter**: Chapter 3 - Set Operations and Applications
**Position**: 2 of 3 sections
**Estimated Pages**: 8-10 pages
**Story Points**: 5 (Medium)

## Learning Objective

**Implement mathematical set operations (union, intersection, difference, symmetric difference) using both operator and method syntax to solve data comparison problems.**

## Prerequisites

- Section 3.1: Set Fundamentals (completed - introduces sets and basic operations)
- Understanding of mathematical set theory (brief review will be provided)
- Code from section 3.1 (set-basics.py) for comparison examples

## Content Plan

**Main Concept**: Python sets support mathematical operations that mirror set theory. Readers will learn to combine, compare, and manipulate sets using intuitive operators.

**Key Points**:
- Union (|): Combines all elements from multiple sets
- Intersection (&): Finds common elements
- Difference (-): Elements in one set but not another
- Symmetric difference (^): Elements in either set but not both
- Operator syntax vs method syntax (when to use each)

**Tutorial Approach**: Example-driven with permission system case study

**Estimated Breakdown**:
- Concept explanation: 2-3 pages (introduce each operation)
- Tutorial walkthrough: 4-5 pages (build permission system)
- Practice exercises: 2 pages (guided problems)

## Code Examples Needed

**Example 1**: `set-operations-basic.py` - Demonstrates all four operations
- Purpose: Show syntax and output for each operation
- Complexity: Simple
- Input: Predefined sets of users/roles
- Expected Output: Visual results of each operation

**Example 2**: `permission-system.py` - Permission checking application
- Purpose: Real-world use case for set operations
- Complexity: Medium
- Demonstrates: Union for combining permissions, intersection for shared access
- Testing: Unit tests for each permission scenario

## Success Criteria

This section is **DONE** when:
- [x] All four set operations explained clearly with examples
- [x] Operator vs method syntax comparison provided
- [x] Permission system tutorial complete and tested
- [x] Code examples developed and all tests passing
- [x] Section length 8-10 pages (not too verbose)
- [x] Transitions from section 3.1 and to section 3.3 clear
- [x] Technical reviewer approved accuracy
- [x] No security issues in permission example code
- [x] Performance note: O(min(len(s), len(t))) for intersection included

## Dependencies

**Must complete before starting**:
- section-3.1 (Set Fundamentals - need basic knowledge)

**Can develop in parallel with**:
- section-3.3 (Practical Applications - different focus)

**Blocks**:
- section-3.3 (builds on these operations for real-world examples)

## Development Notes

**Key Resources**:
- Python official docs: set methods
- Real-world inspiration: Unix file permissions, RBAC systems

**Complexity Areas**:
- Symmetric difference is less intuitive - use Venn diagram
- Method syntax has update variants (union vs update) - clarify in-place vs new set

**Reader Perspective**:
- Most readers familiar with union/intersection from SQL
- Connect to real use cases early (don't stay abstract)

**Special Attention**:
- Permission example must demonstrate security best practices
- Performance implications: when operations matter for large sets
```

---

### Chapter Draft Template

**ID**: `chapter-draft-tmpl.yaml`
**Purpose**: Full chapter draft structure with sections, examples, exercises
**Related Workflows**: Chapter Development Workflow (traditional approach)
**Related Agents**: tutorial-architect

---

### Introduction Template

**ID**: `introduction-tmpl.yaml`
**Purpose**: Book introduction/opening chapter
**Related Agents**: book-publisher, tutorial-architect

---

### Preface Template

**ID**: `preface-tmpl.yaml`
**Purpose**: Book preface (author voice, how to use book)
**Related Agents**: book-publisher

---

### Appendix Template

**ID**: `appendix-tmpl.yaml`
**Purpose**: Reference appendices
**Related Agents**: api-documenter

---

## Code Templates

### Code Example Template

**ID**: `code-example-tmpl.yaml`
**Purpose**: Tested code example with documentation
**Related Workflows**: Code Example Workflow
**Related Agents**: code-curator

---

### API Reference Template

**ID**: `api-reference-tmpl.yaml`
**Purpose**: Comprehensive API documentation with parameters, returns, examples
**Related Workflows**: Tutorial Creation, Chapter Development
**Related Agents**: api-documenter

---

## Learning Templates

### Learning Objectives Template

**ID**: `learning-objectives-tmpl.yaml`
**Purpose**: Measurable learning outcomes using Bloom's taxonomy
**Related Agents**: instructional-designer

#### Sample Output

```markdown
# Learning Objectives: Chapter 5 - Advanced Dictionary Techniques

## Objectives

By the end of this chapter, you will be able to:

1. **Create** custom dictionary classes that extend built-in functionality for specialized use cases

2. **Implement** advanced dictionary patterns (defaultdict, Counter, ChainMap) to simplify complex data handling

3. **Analyze** dictionary performance characteristics to choose optimal implementations for large datasets

4. **Evaluate** when to use dictionaries vs other data structures based on access patterns and memory constraints

5. **Design** caching systems using dictionaries with LRU eviction strategies

## Bloom's Taxonomy Levels

- **Create** (Level 6): Custom dictionary classes, caching systems
- **Evaluate** (Level 5): Structure selection, trade-off analysis
- **Analyze** (Level 4): Performance characteristics, access patterns
- **Implement** (Level 3): Advanced patterns (defaultdict, Counter)

## Measurability

Each objective maps to specific exercises:
- Objective 1 → Exercise 5.3: Build OrderedCache class
- Objective 2 → Exercise 5.1: Implement word counter with defaultdict
- Objective 3 → Exercise 5.4: Benchmark dictionary vs list performance
- Objective 4 → Exercise 5.2: Compare structures for user session storage
- Objective 5 → Exercise 5.5: Create LRU cache decorator

## Alignment

- **Book-Level**: Advances toward "Choose optimal data structures" outcome
- **Part-Level**: Completes Part I mastery of built-in structures
- **Next Chapter**: Prerequisite for Chapter 6 custom data structures
```

---

### Exercise Set Template

**ID**: `exercise-set-tmpl.yaml`
**Purpose**: Practice problems with solutions and difficulty levels
**Related Agents**: exercise-creator

---

## Tutorial Templates

### Tutorial Section Template

**ID**: `tutorial-section-tmpl.yaml`
**Purpose**: Step-by-step hands-on tutorial section
**Related Workflows**: Tutorial Creation Workflow
**Related Agents**: tutorial-architect

---

## Review Templates

### Technical Review Report Template

**ID**: `technical-review-report-tmpl.yaml`
**Purpose**: Structured technical review findings with severity levels
**Related Workflows**: Technical Review Workflow
**Related Agents**: technical-reviewer

---

### Revision Plan Template

**ID**: `revision-plan-tmpl.yaml`
**Purpose**: Strategic plan for book updates/revisions
**Related Workflows**: Book Edition Update Workflow
**Related Agents**: book-analyst

---

## Visual Templates

### Diagram Specification Template

**ID**: `diagram-spec-tmpl.yaml`
**Purpose**: Technical diagram specifications (Mermaid, architecture diagrams)
**Related Agents**: screenshot-specialist

---

## Documentation Templates

### Glossary Entry Template

**ID**: `glossary-entry-tmpl.yaml`
**Purpose**: Consistent glossary term definitions
**Related Agents**: api-documenter

---

### Book Analysis Report Template

**ID**: `book-analysis-report-tmpl.yaml`
**Purpose**: Analysis of existing book for revision planning
**Related Workflows**: Book Edition Update Workflow
**Related Agents**: book-analyst

---

## Template Comparison Table

| Template | Category | Elicit? | Primary Agent | Use Case |
|----------|----------|---------|---------------|----------|
| book-outline-tmpl | Planning | Yes | instructional-designer | Book planning |
| book-proposal-tmpl | Planning | Yes | book-publisher | Publisher proposals |
| chapter-outline-tmpl | Planning | Yes | tutorial-architect | Chapter planning |
| section-plan-tmpl | Chapter Content | No | tutorial-architect | Section-driven development |
| chapter-draft-tmpl | Chapter Content | Yes | tutorial-architect | Full chapter drafts |
| introduction-tmpl | Chapter Content | Yes | book-publisher/tutorial-architect | Book introductions |
| preface-tmpl | Chapter Content | Yes | book-publisher | Book prefaces |
| appendix-tmpl | Chapter Content | No | api-documenter | Reference appendices |
| code-example-tmpl | Code | No | code-curator | Tested code examples |
| api-reference-tmpl | Code | No | api-documenter | API documentation |
| learning-objectives-tmpl | Learning | Yes | instructional-designer | Learning outcomes |
| exercise-set-tmpl | Learning | Yes | exercise-creator | Practice problems |
| tutorial-section-tmpl | Tutorial | Yes | tutorial-architect | Hands-on tutorials |
| technical-review-report-tmpl | Review | No | technical-reviewer | Technical reviews |
| revision-plan-tmpl | Review | No | book-analyst | Update planning |
| diagram-spec-tmpl | Visual | No | screenshot-specialist | Technical diagrams |
| glossary-entry-tmpl | Documentation | No | api-documenter | Glossaries |
| book-analysis-report-tmpl | Documentation | No | book-analyst | Book analysis |

---

## Template Selection Guide

**I want to...**

### Plan a book
→ `book-outline-tmpl` - Complete book structure
→ `book-proposal-tmpl` - Publisher submission

### Plan a chapter
→ `chapter-outline-tmpl` - Detailed chapter structure
→ `section-plan-tmpl` - Break into deliverable sections

### Write content
→ `chapter-draft-tmpl` - Full chapter (traditional approach)
→ `tutorial-section-tmpl` - Hands-on tutorials
→ `introduction-tmpl` or `preface-tmpl` - Front matter

### Create code/examples
→ `code-example-tmpl` - Tested code snippets
→ `api-reference-tmpl` - API documentation

### Define learning
→ `learning-objectives-tmpl` - Measurable outcomes
→ `exercise-set-tmpl` - Practice problems

### Review and revise
→ `technical-review-report-tmpl` - Review findings
→ `revision-plan-tmpl` - Update strategy
→ `book-analysis-report-tmpl` - Existing book analysis

### Add visuals/extras
→ `diagram-spec-tmpl` - Technical diagrams
→ `glossary-entry-tmpl` - Terminology
→ `appendix-tmpl` - Reference sections

---

## Customization Notes

### Variable Substitution

All templates support variable substitution using `{{variable_name}}` syntax:

- `{{book_title}}` - Book title
- `{{chapter_number}}` - Chapter number
- `{{section_number}}` - Section number
- `{{author_name}}` - Author name
- Custom variables can be defined per template

### Elicitation Behavior

- **Elicit=true**: Agent will ask user for input interactively
- **Elicit=false**: Agent fills from context automatically
- **allow_skip**: Can user skip sections? (typically false)

### Adapting Templates

Templates are YAML files - you can:
1. Add new sections to existing templates
2. Modify section instructions
3. Change variable names
4. Adjust elicitation behavior
5. Create custom templates following same structure

### Template Format

All templates follow the BMad Doc Template specification:
- `template` block: metadata (id, name, version, description, output format)
- `workflow` block: elicitation settings
- `sections` array: ordered sections with id, title, instruction, elicit flag

---

## Conclusion

The BMad Technical Writing Expansion Pack's **18 templates** provide comprehensive structure for every document type in technical book authoring. By understanding each template's purpose and seeing filled examples, you can:

- **Create consistent documentation** across your book
- **Follow best practices** embedded in template instructions
- **Save time** with reusable structures
- **Maintain quality** through standardized sections
- **Customize** templates for your specific needs

**Key Templates to Master**:
- **book-outline-tmpl** - Foundation of book planning
- **chapter-outline-tmpl** - Essential for chapter development
- **section-plan-tmpl** - Enables incremental progress
- **code-example-tmpl** - Ensures tested code quality

**Total template count**: 18
**Word count**: ~3,200 words

---

**Related Documentation**:
- [Agent Reference Guide](agent-reference.md) - Agents that use these templates
- [Workflow Guide](workflow-guide.md) - Workflows that execute templates
- [Task Reference](task-reference.md) - Tasks that invoke templates
- [User Guide](user-guide.md) - How templates fit into the process
