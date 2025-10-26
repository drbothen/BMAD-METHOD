<!-- Powered by BMAD™ Core -->

# Create Book Research Queries

---

task:
id: create-book-research-queries
name: Create Book Research Queries
description: Generate comprehensive research questions for technical book chapter topics with copy/paste formatting for external tools
persona_default: technical-researcher
inputs:
  - chapter-topic
  - target-audience
  - book-context
steps:
  - Analyze chapter topic and scope
  - Identify target audience knowledge level
  - Generate research questions for technical concepts
  - Identify code example needs
  - Create learning progression validation questions
  - Organize questions by priority and category
  - Define research methodology and sources
  - Format queries for copy/paste into external tools
output: Formatted research queries ready for manual research or automated execution

---

## Purpose

This task helps you generate focused, actionable research questions for technical book chapter topics. Well-crafted queries ensure comprehensive coverage of technical concepts, practical code examples, and pedagogically sound learning progressions. Queries are formatted for easy copy/paste into external research tools (web search, Perplexity, academic databases).

## Prerequisites

Before starting this task:

- Chapter topic and scope identified
- Target audience skill level known
- Book context understood (position in learning path)
- Understanding of chapter learning objectives (if defined)

## Research Query Categories

Organize queries into these categories:

**Technical Concepts** - Core knowledge and theory:

- Definitions and terminology
- Technical specifications
- How things work under the hood
- Best practices and conventions

**Code Examples** - Practical implementations:

- Common patterns and idioms
- Real-world use cases
- API usage examples
- Error handling patterns

**Learning Progression** - Pedagogical validation:

- Prerequisites and foundations
- Common misconceptions
- Difficult concepts that need extra explanation
- Ideal sequencing of topics

**Expert Insights** - Professional perspectives:

- Industry best practices
- Common pitfalls to avoid
- Performance considerations
- Security implications

**Sources and References** - Documentation and credibility:

- Official documentation
- Authoritative blog posts
- Academic papers
- Community resources

## Workflow Steps

### 1. Analyze Chapter Topic and Scope

Understand what this chapter will cover:

- Main technical topic or concept
- Depth of coverage (introductory, intermediate, advanced)
- Key subtopics to address
- Connection to previous/future chapters
- Learning objectives (if defined)

### 2. Identify Target Audience Knowledge Level

Determine what readers already know:

- **Beginner**: New to programming or technology stack
- **Intermediate**: Comfortable with basics, learning advanced concepts
- **Advanced**: Experienced, seeking optimization or edge cases

Adjust query complexity based on audience level.

### 3. Generate Technical Concept Questions

Create queries to understand core concepts:

**Definition and Theory:**

- "What is [concept] and how does it work?"
- "What are the main components of [technology/system]?"
- "What problem does [concept] solve?"

**Technical Specifications:**

- "What are the technical requirements for [technology]?"
- "What are the configuration options for [feature]?"
- "What are the performance characteristics of [approach]?"

**Best Practices:**

- "What are the recommended best practices for [concept]?"
- "What are common anti-patterns to avoid with [technology]?"
- "What are the security considerations for [feature]?"

### 4. Identify Code Example Needs

Generate queries for practical implementations:

**Basic Usage:**

- "Show me a simple example of [concept] in [language]"
- "What is the minimal code needed to implement [feature]?"
- "How do you set up [technology] for a basic use case?"

**Common Patterns:**

- "What are common patterns for [use case] using [technology]?"
- "Show me real-world examples of [concept] in production code"
- "What are the different ways to implement [feature]?"

**Error Handling:**

- "How do you handle errors with [technology/API]?"
- "What are common exceptions thrown by [feature]?"
- "What are best practices for error handling in [scenario]?"

**Testing:**

- "How do you test code that uses [concept]?"
- "What are best practices for unit testing [feature]?"
- "Show me examples of testing [scenario]"

### 5. Create Learning Progression Validation Questions

Ensure pedagogical soundness:

**Prerequisites:**

- "What should readers know before learning [concept]?"
- "What foundational topics are required for [advanced topic]?"
- "What dependencies exist between [topic A] and [topic B]?"

**Common Misconceptions:**

- "What are common misconceptions about [concept]?"
- "What do beginners typically get wrong about [feature]?"
- "What confuses learners when first encountering [topic]?"

**Difficulty and Sequencing:**

- "What is the ideal learning sequence for [topic area]?"
- "What are the hardest parts of learning [concept]?"
- "Should [concept A] be taught before or after [concept B]?"

### 6. Organize Questions by Priority and Category

Prioritize queries:

**High Priority** (must answer for chapter):

- Core concept definitions
- Essential code examples
- Critical best practices
- Fundamental prerequisites

**Medium Priority** (enhance chapter quality):

- Advanced patterns
- Edge cases
- Performance considerations
- Alternative approaches

**Low Priority** (nice to have):

- Historical context
- Related technologies
- Future developments
- Deep technical details

### 7. Define Research Methodology and Sources

Specify where to research:

**For Official Information:**

- Official documentation sites
- Technology specification documents
- API reference guides
- Release notes and changelogs

**For Best Practices:**

- Technology blogs (official and community)
- Conference talks and presentations
- GitHub repositories with examples
- Stack Overflow discussions

**For Academic Rigor:**

- Academic papers and journals
- Technical books by recognized experts
- Standards documents (W3C, IETF, etc.)
- Peer-reviewed research

**For Practical Insights:**

- Developer blogs and tutorials
- Open source project code
- Case studies and experience reports
- Community forums and discussions

### 8. Format Queries for Copy/Paste

**Plain Text Format (for manual research):**

```
TECHNICAL CONCEPTS
1. What is [concept] and how does it work?
2. What are the main components of [technology]?
3. What problem does [concept] solve?

CODE EXAMPLES
4. Show me a simple example of [concept] in [language]
5. What are common patterns for [use case]?
6. How do you handle errors with [feature]?

LEARNING PROGRESSION
7. What should readers know before learning [concept]?
8. What are common misconceptions about [topic]?
```

**Query Optimization Guidance:**

- **Web Search**: Use natural language questions
- **Perplexity**: Add "explain" or "compare" for deeper analysis
- **Academic Databases**: Include technical terms and keywords
- **Documentation Sites**: Use specific function/API names

## Success Criteria

Research queries are complete when:

- [ ] All major technical concepts identified
- [ ] Code example needs clearly specified
- [ ] Learning progression validated
- [ ] Queries organized by category and priority
- [ ] Formatted for easy copy/paste
- [ ] Research sources identified
- [ ] Query optimization guidance provided
- [ ] 10-25 focused questions generated (not too broad, not too narrow)

## Examples

### Example 1: Chapter on "Understanding React Hooks"

**Target Audience**: Intermediate React developers
**Chapter Scope**: Introduction to Hooks API, common hooks, custom hooks

**TECHNICAL CONCEPTS**

1. What is the React Hooks API and why was it introduced?
2. What are the rules of hooks and why do they exist?
3. How do hooks differ from class component lifecycle methods?
4. What problems do hooks solve compared to class components?

**CODE EXAMPLES** 5. Show me a simple example of useState and useEffect in React 6. What are common patterns for using useEffect with cleanup? 7. How do you create a custom hook in React? 8. Show me real-world examples of custom hooks for data fetching

**LEARNING PROGRESSION** 9. What should readers know about React before learning hooks? 10. What are common mistakes beginners make with useEffect? 11. Should custom hooks be taught before or after built-in hooks?

**EXPERT INSIGHTS** 12. What are performance considerations when using hooks? 13. What are best practices for organizing hook logic? 14. What are common anti-patterns with hooks to avoid?

### Example 2: Chapter on "Async/Await in JavaScript"

**Target Audience**: Beginner to intermediate JavaScript developers
**Chapter Scope**: Promise basics, async/await syntax, error handling

**TECHNICAL CONCEPTS**

1. What are Promises and how do they work in JavaScript?
2. What is the difference between async/await and Promise.then()?
3. How does async/await improve code readability?
4. What happens under the hood when using async/await?

**CODE EXAMPLES** 5. Show me a simple example of converting Promise.then() to async/await 6. How do you handle errors with async/await using try/catch? 7. What are patterns for running multiple async operations in parallel? 8. Show me examples of async/await in Express.js route handlers

**LEARNING PROGRESSION** 9. Should readers understand Promises before learning async/await? 10. What are common confusion points with async/await for beginners? 11. What is the ideal order to teach: callbacks → Promises → async/await?

**EXPERT INSIGHTS** 12. What are common mistakes developers make with async/await? 13. When should you use async/await vs Promise.then()? 14. What are the performance implications of async/await?

## Common Pitfalls to Avoid

- **Too vague**: "Learn about React" → "What are the rules of hooks and why do they exist?"
- **Too broad**: Queries that require entire books to answer
- **Too technical**: Queries beyond target audience level
- **No prioritization**: All queries treated equally
- **Missing categories**: Only focusing on code, ignoring concepts or pedagogy
- **Not actionable**: Queries that don't lead to concrete chapter content
- **Poor formatting**: Queries not optimized for research tools

## Next Steps

After creating research queries:

1. **Manual Workflow**: Copy queries into research tools (web search, Perplexity, etc.)
2. **Import Workflow**: Conduct research manually, then use `*import-research` command
3. **Automated Workflow**: Use `*research-auto` command to execute queries with available tools
4. Document findings using book-research-report template
5. Feed research results into chapter outline creation
6. Refine queries based on initial research findings

## Integration with Workflows

This task integrates with:

- **book-planning-workflow.yaml**: Research queries during chapter planning phase
- **chapter-development-workflow.yaml**: Research feeds into chapter writing
- **execute-research-with-tools.md**: Automated execution of generated queries
- **book-research-report-tmpl.yaml**: Document research findings
