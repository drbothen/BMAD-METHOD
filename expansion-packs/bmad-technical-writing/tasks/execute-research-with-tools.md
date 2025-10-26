<!-- Powered by BMAD™ Core -->

# Execute Research With Tools

---

task:
id: execute-research-with-tools
name: Execute Research With Tools
description: Autonomously execute technical research queries using available tools (WebSearch, Perplexity, MCP tools) and compile findings with proper citations
persona_default: technical-researcher
inputs:

- chapter-topic
- research-queries
- target-audience
  steps:
- Detect available research tools
- Match query types to optimal tools
- Parse and organize research queries
- Execute queries using available tools
- Collect and organize findings by query
- Extract source citations and credibility metadata
- Synthesize findings across multiple sources
- Identify gaps or conflicting information
- Auto-populate book-research-report template
  output: Structured research findings document with source citations

---

## Purpose

This task enables automated execution of technical research queries using available tools in your environment. It systematically researches chapter topics, gathers technical information, evaluates sources, and compiles findings into a structured report. This automation saves time while ensuring comprehensive coverage and proper source attribution.

## Prerequisites

Before starting this task:

- Research queries generated (from create-book-research-queries.md or provided directly)
- At least one research tool available (WebSearch, Perplexity, or MCP tools)
- Chapter topic and target audience identified
- Understanding of desired research depth

## Available Research Tools

This task integrates with these tools when available:

**WebSearch** - General web search:

- Best for: Current information, documentation, tutorials
- Strengths: Broad coverage, recent content, diverse sources
- Use for: General queries, best practices, code examples

**Perplexity** - AI-powered research:

- Best for: Synthesized analysis, comparisons, explanations
- Strengths: Source aggregation, contextual understanding
- Use for: Complex concepts, technical comparisons, trends

**MCP Tools** - Model Context Protocol tools:

- Best for: Specialized research (academic papers, documentation APIs)
- Strengths: Domain-specific knowledge, structured data
- Use for: Academic research, API references, specifications

## Workflow Steps

### 1. Detect Available Research Tools

Identify which tools are accessible:

**Detection Logic:**

```
Check environment for:
- WebSearch capability (search API available)
- Perplexity access (API key or integration configured)
- MCP tools (context7, academic search, documentation fetchers)

Document available tools for user awareness
Provide fallback messaging if tools unavailable
```

**User Notification:**

```
Available research tools detected:
✓ WebSearch - Enabled
✓ Perplexity - Not available (no API key)
✓ MCP Tools - context7 (documentation lookup)

Research will proceed using WebSearch and context7.
```

### 2. Match Query Types to Optimal Tools

Select the best tool for each query type:

**Tool Selection Matrix:**

| Query Type      | Priority 1                 | Priority 2        | Priority 3 |
| --------------- | -------------------------- | ----------------- | ---------- |
| Official docs   | context7 (docs API)        | WebSearch         | Perplexity |
| Code examples   | WebSearch                  | context7 (GitHub) | Perplexity |
| Best practices  | Perplexity                 | WebSearch         | MCP        |
| Technical specs | WebSearch (official sites) | context7          | Perplexity |
| Comparisons     | Perplexity                 | WebSearch         | MCP        |
| Academic        | MCP (academic tools)       | Perplexity        | WebSearch  |

**Selection Criteria:**

- Prioritize official sources for definitions and specifications
- Use AI tools (Perplexity) for synthesized explanations
- Use web search for practical examples and community insights
- Use MCP tools for specialized or structured data

**Fallback Strategy:**

- If preferred tool unavailable, use next priority
- If no tools available, output queries for manual research
- Inform user of tool selection rationale

### 3. Parse and Organize Research Queries

Structure queries for execution:

**Organization:**

1. Group queries by category (Technical Concepts, Code Examples, etc.)
2. Assign tool to each query based on type
3. Prioritize queries (high/medium/low)
4. Determine execution order (parallel where possible, sequential if dependent)

**Example:**

```
Query Group 1: Technical Concepts (Priority: High, Tool: WebSearch)
- Q1: What is the React Hooks API and why was it introduced?
- Q2: What are the rules of hooks and why do they exist?

Query Group 2: Code Examples (Priority: High, Tool: WebSearch + context7)
- Q3: Show me a simple example of useState and useEffect in React
- Q4: What are common patterns for using useEffect with cleanup?

Query Group 3: Expert Insights (Priority: Medium, Tool: Perplexity)
- Q5: What are performance considerations when using hooks?
- Q6: What are best practices for organizing hook logic?
```

### 4. Execute Queries Using Available Tools

Run queries systematically:

**Execution Pattern:**

```
For each query:
1. Select tool based on query type and availability
2. Format query for optimal tool performance
3. Execute query with appropriate parameters
4. Capture raw results
5. Log execution status (success/partial/failure)
6. Handle errors gracefully (retry, fallback, skip)
7. Apply rate limiting if needed
8. Update progress for user awareness
```

**Query Formatting by Tool:**

**WebSearch:**

```
Original: "What is the React Hooks API?"
Formatted: "React Hooks API documentation official"
```

**Perplexity:**

```
Original: "What are performance considerations for hooks?"
Formatted: "Explain performance implications and optimization strategies for React Hooks with examples"
```

**MCP/context7:**

```
Original: "Show me useState examples"
Formatted: "/reactjs/react docs:Hooks:useState examples"
```

**Error Handling:**

- Tool unavailable: Try fallback tool
- Rate limit hit: Queue query for later, continue with others
- No results: Log as gap, continue
- Tool error: Capture error, try alternative tool

### 5. Collect and Organize Findings by Query

Structure results for analysis:

**Finding Structure:**

```
Query: What is the React Hooks API and why was it introduced?

Finding:
  Answer: [Synthesized answer from sources]
  Sources:
    - URL: https://react.dev/reference/react
      Title: "React Hooks Documentation"
      Excerpt: "Hooks let you use state and other React features..."
      Date Accessed: 2025-10-25
      Credibility: Official Documentation
      Tool Used: WebSearch

    - URL: https://example.com/blog/hooks-intro
      Title: "Understanding React Hooks"
      Excerpt: "Hooks were introduced to solve problems with..."
      Date Accessed: 2025-10-25
      Credibility: Community Blog (Expert Author)
      Tool Used: WebSearch

  Synthesis: [Combined answer drawing from multiple sources]
  Confidence: High (multiple authoritative sources agree)
  Gaps: [Any unanswered aspects of the query]
```

**Organization:**

- Group findings by original research category
- Preserve source attribution for every fact
- Note which tool provided each finding
- Flag conflicting information across sources

### 6. Extract Source Citations and Credibility Metadata

Capture comprehensive source information:

**Citation Elements:**

- **URL**: Full web address
- **Title**: Page or article title
- **Author**: If identifiable
- **Publication Date**: If available
- **Access Date**: When research was conducted
- **Tool Used**: Which research tool found it
- **Content Type**: Documentation, blog, forum, academic, etc.

**Credibility Assessment:**

**Tier 1 - Authoritative:**

- Official documentation (React, MDN, W3C, etc.)
- Specifications and standards
- Core team statements
- Peer-reviewed academic papers

**Tier 2 - Expert:**

- Recognized expert blogs (Dan Abramov, Kent C. Dodds, etc.)
- Conference talks by core contributors
- Technical books by established authors
- High-quality tutorials from reputable sources

**Tier 3 - Community:**

- Stack Overflow answers (high votes)
- GitHub repositories with significant usage
- Community blogs and tutorials
- Forum discussions

**Tier 4 - Unverified:**

- Low-reputation sources
- Outdated content
- Unattributed information
- Conflicting with higher-tier sources

**Credibility Indicators:**

```
Source: https://react.dev/reference/react/useState
Title: "useState – React"
Credibility: Tier 1 (Official Documentation)
Indicators:
  ✓ react.dev domain (official)
  ✓ Maintained by React team
  ✓ Current version (updated 2024)
  ✓ Primary source
```

### 7. Synthesize Findings Across Multiple Sources

Combine information intelligently:

**Synthesis Process:**

1. Identify common themes across sources
2. Reconcile minor differences in explanation
3. Flag major conflicts or contradictions
4. Prefer authoritative sources for facts
5. Use community sources for practical insights
6. Combine complementary information
7. Note source agreement/disagreement

**Synthesis Example:**

```
Query: What are the rules of hooks?

Source 1 (Official Docs): "Only call hooks at the top level. Don't call hooks inside loops, conditions, or nested functions."

Source 2 (Expert Blog): "Hooks must be called in the same order every render, which is why they can't be inside conditions."

Source 3 (Community Tutorial): "Always call hooks in the same order - that's why no conditional hooks."

Synthesized Answer:
React Hooks have a strict rule: they must be called at the top level of functional components or custom hooks, never inside loops, conditions, or nested functions. This requirement exists because React relies on hooks being called in the same order on every render to correctly track state between renders.

Sources: [1] Official React Documentation (react.dev), [2] "Understanding Hooks Rules" by Dan Abramov (blog), [3] "React Hooks Tutorial" (tutorial site)

Confidence: Very High (official source + expert confirmation + community consensus)
```

**Conflict Resolution:**

- **When sources conflict**: Present both views, note credibility tiers, indicate which is likely correct
- **When sources complement**: Combine information for comprehensive answer
- **When gaps exist**: Note what couldn't be answered, suggest manual follow-up

### 8. Identify Gaps or Conflicting Information

Document research limitations:

**Gap Types:**

**Information Gaps:**

- Questions with no satisfactory answers
- Queries that require domain expertise unavailable in sources
- Rapidly changing information (recent releases, breaking changes)
- Edge cases not documented

**Example:**

```
Gap Identified:
Query: What is the performance impact of many useState calls vs one useState with object?
Status: No authoritative answer found
Sources Consulted: Official docs (no mention), 2 blog posts (conflicting opinions), Stack Overflow (speculation)
Recommendation: Conduct manual benchmarking or consult React team directly
```

**Conflicting Information:**

- Sources that directly contradict each other
- Outdated information vs current information
- Theoretical vs practical differences

**Example:**

```
Conflict Identified:
Query: When does useEffect run?
Source A (Official Docs): "After the browser has painted"
Source B (Blog): "After render but before paint"
Resolution: Official documentation is authoritative. Source B may be outdated (pre-React 18).
Confidence: High (official source takes precedence)
```

**Outdated Content:**

- Information predating significant version changes
- Deprecated APIs or patterns
- Old best practices superseded by new approaches

**Documentation Strategy:**

- Clearly mark gaps for manual follow-up
- Present conflicting information with analysis
- Flag outdated content with version notes
- Suggest additional research paths

### 9. Auto-Populate book-research-report Template

Generate structured report:

**Template Population:**

1. Use book-research-report-tmpl.yaml structure
2. Populate all sections with research findings
3. Organize content by template sections
4. Preserve elicitation workflow for user review
5. Include all source citations
6. Add metadata (research method: "automated", tools used)

**Automated Sections:**

- **Research Context**: Derived from input parameters
- **Research Questions & Answers**: Populated from findings with citations
- **Technical Findings**: Synthesized from all sources
- **Code Examples Discovered**: Extracted code snippets with context
- **Expert Insights**: Quotes and insights from Tier 2 sources
- **Chapter Integration**: Preliminary outline suggestions
- **Additional Resources**: All sources in bibliographic format
- **Research Notes**: Gaps, conflicts, observations

**Elicitation Workflow:**

- Present auto-generated content to user
- Allow refinement of synthesized answers
- Enable adding manual insights
- Support removal of irrelevant findings
- Confirm chapter integration suggestions

**Output Example:**

```markdown
---
topic: Understanding React Hooks
date-created: 2025-10-25
research-method: automated
related-chapters: []
research-tools:
  - WebSearch
  - context7
---

# Research Report: Understanding React Hooks

## Research Context

[Auto-populated from inputs]

## Research Questions & Answers

[Populated with synthesized answers + citations]

## Technical Findings

[Synthesized discoveries organized by importance]

[... additional sections ...]
```

## Success Criteria

Automated research is complete when:

- [ ] All available tools detected and selected
- [ ] Queries executed with appropriate tools
- [ ] Findings collected with complete source citations
- [ ] Source credibility assessed for all sources
- [ ] Findings synthesized across multiple sources
- [ ] Conflicts and gaps clearly identified
- [ ] book-research-report template auto-populated
- [ ] User can review and refine through elicitation
- [ ] Research method clearly marked as "automated"
- [ ] All tools used are documented in frontmatter

## Error Handling

Handle these scenarios gracefully:

**No Tools Available:**

```
Message: No automated research tools detected.
Action: Output formatted queries for manual research
Fallback: User can later use *import-research to add findings
```

**Partial Tool Availability:**

```
Message: WebSearch available, Perplexity not configured
Action: Proceed with WebSearch, note limitation in report
Result: Partial automation, some queries may need manual follow-up
```

**Query Failures:**

```
Message: Query "X" failed (rate limit / tool error / no results)
Action: Log failure, continue with remaining queries
Result: Partial results, gaps documented
```

**Conflicting Results:**

```
Message: Sources provide conflicting information for query "X"
Action: Present all viewpoints, assess credibility, recommend resolution
Result: User can make informed decision during elicitation
```

## Tool-Specific Considerations

**WebSearch:**

- Rate Limits: Implement query throttling if needed
- Result Quality: Prioritize official documentation domains
- Code Examples: Look for GitHub, official repos, documentation sites

**Perplexity:**

- Query Formulation: Use natural language, add context
- Citation Tracking: Perplexity provides source links, extract them
- Synthesis: Perplexity synthesizes; still verify against original sources

**MCP Tools:**

- Tool Discovery: Check which MCP servers are configured
- API Variations: Different MCP tools have different query formats
- Structured Data: MCP tools often return structured data, parse accordingly

## Examples

### Example 1: Automated Research for "Understanding React Hooks"

**Input:**

- Topic: Understanding React Hooks
- Audience: Intermediate React developers
- Queries: 15 questions across technical concepts, code examples, best practices

**Execution:**

1. **Tool Detection**: WebSearch available, context7 available
2. **Query Assignment**:
   - Concept queries → WebSearch (official React docs)
   - Code examples → WebSearch + context7 (GitHub examples)
   - Best practices → WebSearch (expert blogs)
3. **Execution**: 15 queries executed, 14 successful, 1 partial (rate limit)
4. **Findings**: 28 sources gathered (12 official docs, 10 expert blogs, 6 community)
5. **Synthesis**: Answers compiled from 2-4 sources each
6. **Gaps**: 1 query incomplete (performance benchmarking data), flagged for manual research
7. **Output**: Complete research report with 28 citations, ready for review

**Result:**

- Research time: 5 minutes (automated) vs ~2 hours (manual)
- Coverage: 93% complete (14/15 queries fully answered)
- Quality: High (multiple authoritative sources per query)
- User action: Review synthesis, fill 1 gap manually, approve report

### Example 2: Partial Automation (Limited Tools)

**Input:**

- Topic: Advanced TypeScript Patterns
- Audience: Experienced developers
- Queries: 20 questions on type theory, advanced patterns, performance

**Execution:**

1. **Tool Detection**: Only WebSearch available (no Perplexity, no MCP)
2. **Query Assignment**: All queries → WebSearch
3. **Execution**: 20 queries executed, 15 successful, 5 limited results
4. **Findings**: 35 sources (Official TypeScript docs, blogs, Stack Overflow)
5. **Gaps**: 5 queries need deeper analysis (would benefit from Perplexity)
6. **Output**: Research report with recommendation for manual deep-dive on 5 topics

**Result:**

- Research time: 8 minutes automated
- Coverage: 75% complete, 25% needs manual follow-up
- Quality: Good for covered areas, gaps clearly marked
- User action: Conduct manual research for 5 advanced topics, integrate results

## Integration with Workflows

This task integrates with:

- **create-book-research-queries.md**: Uses generated queries as input
- **book-research-report-tmpl.yaml**: Auto-populates template sections
- **technical-researcher agent**: Invoked via `*research-auto` command
- **chapter-development-workflow.yaml**: Feeds research into chapter writing

## Common Pitfalls to Avoid

- **Over-reliance on single tool**: Use multiple tools for validation
- **Ignoring source credibility**: Not all web results are equal
- **No synthesis**: Presenting raw results without combining/analyzing
- **Missing citations**: Every fact needs a source
- **Not handling failures**: Some queries will fail, handle gracefully
- **Assuming completeness**: Automated research may miss nuances
- **Skipping user review**: Always enable elicitation for refinement

## Next Steps

After automated research execution:

1. **Review findings**: Use elicitation workflow to validate synthesis
2. **Fill gaps**: Conduct manual research for incomplete queries
3. **Resolve conflicts**: Make decisions on conflicting information
4. **Refine examples**: Adapt code examples for your chapter context
5. **Integrate into chapter**: Use research to create chapter outline
6. **Save report**: Store in manuscripts/research/ for reference
