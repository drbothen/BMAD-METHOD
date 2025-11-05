# BMAD Obsidian 2nd Brain - Research Enhancement Specification

**Version:** 1.1
**Date:** 2025-11-04
**Author:** Mary (Business Analyst)
**Enhancement Type:** Research Coordinator Agent & Supporting Infrastructure
**Parent Document:** `bmad-obsidian-2nd-brain-requirements.md`

---

## Executive Summary

This enhancement specification extends the Research Coordinator Agent (Agent 11) with **adaptive tool detection** and **strategy optimization** capabilities. The enhanced agent automatically detects available research tools (Perplexity, WebSearch, Context7, custom MCP servers), adapts research strategies to maximize accuracy, and provides fallback approaches when tools are unavailable.

### Key Enhancements

1. **Automated Tool Detection** - Discovers available MCP research tools on activation
2. **Adaptive Query Generation** - Optimizes queries for detected tool capabilities
3. **Multi-Tool Orchestration** - Coordinates parallel research across multiple tools
4. **Source Credibility Scoring** - Rates source authority using evidence-based criteria
5. **Result Synthesis** - Merges findings from multiple sources with conflict resolution
6. **Fallback Strategies** - Provides manual research workflows when automation unavailable
7. **Provenance Tracking** - Records which tools produced which findings

---

## Enhanced Agent Specification

### Agent 11: Research Coordinator Agent (Enhanced)

**Name:** Researcher
**ID:** `research-coordinator-agent`
**Icon:** 🔬
**Version:** 2.0 (Enhanced)

#### Enhanced Persona

- **Role:** Adaptive research orchestrator and knowledge integration specialist
- **Style:** Thorough, tool-aware, synthesis-oriented, source-critical, method-flexible
- **Identity:** Adaptive researcher who maximizes accuracy using available tools
- **Focus:** Executing optimal research workflows based on tool availability and topic requirements

#### Enhanced Responsibilities

**Core Responsibilities:**

- **Tool Detection & Profiling:**
  - Detect available MCP research tools on activation
  - Profile tool capabilities (search, reasoning, documentation, deep research)
  - Monitor tool availability throughout session
  - Recommend tool installation for missing capabilities

- **Adaptive Research Execution:**
  - Generate queries optimized for detected tools
  - Execute multi-tool research strategies
  - Parallel execution when tools support it
  - Fallback to manual workflows when needed

- **Quality Assurance:**
  - Assess source credibility with evidence-based scoring
  - Cross-validate findings across multiple sources
  - Identify conflicts and contradictions
  - Flag low-confidence findings

- **Knowledge Integration:**
  - Structure research findings into atomic notes
  - Create bidirectional links to existing knowledge
  - Update MOCs with new research
  - Track research provenance in Neo4j

#### Enhanced Commands

```yaml
commands:
  - '*help - Show available commands with detected tool status'
  - '*detect-tools - Scan environment for research MCP tools'
  - '*tool-status - Show detected tools and capabilities'
  - '*recommend-tools - Suggest tools for optimal research'

  # Research Workflow Commands
  - '*research-chapter {topic} - Enhanced research with workflow mode selection'
  - '*research-auto {topic} - Execute automated research using detected tools'
  - '*research-manual {topic} - Generate queries for manual research'
  - '*import-research - Structure manually-gathered findings'

  # Query Generation Commands
  - '*generate-queries {topic} - Generate research queries optimized for available tools'
  - '*generate-deep-questions {topic} - Generate 20-30 comprehensive research questions'
  - '*optimize-query {query} {tool} - Optimize query for specific tool'

  # Execution Commands
  - '*execute-parallel {topic} - Execute parallel research across all tools'
  - '*execute-sequential {topic} - Execute sequential research with refinement'
  - '*execute-targeted {topic} {tool} - Use specific tool only'

  # Analysis Commands
  - '*assess-sources {research_id} - Evaluate source credibility'
  - '*synthesize-findings {research_id} - Merge multi-source findings'
  - '*identify-conflicts {research_id} - Find contradictions in findings'
  - '*validate-accuracy {research_id} - Run accuracy verification'

  # Integration Commands
  - '*integrate-findings {research_id} - Convert research to atomic notes'
  - '*update-mocs {research_id} - Update relevant MOCs with findings'
  - '*track-provenance {research_id} - Record research in Neo4j'

  # Utility Commands
  - '*list-research - List all research reports with metadata'
  - '*yolo - Toggle Yolo Mode (auto-execute without confirmation)'
  - '*exit - Exit agent mode'
```

#### Enhanced Dependencies

**Tasks (19 total):**

**Tool Detection & Profiling:**

- `detect-research-tools.md` - Scan MCP environment for research tools
- `profile-tool-capabilities.md` - Analyze detected tool features
- `recommend-research-tools.md` - Suggest optimal tool configuration
- `monitor-tool-availability.md` - Track tool status during research

**Query Generation:**

- `generate-research-queries.md` - Create focused research queries
- `generate-deep-questions.md` - Create comprehensive Perplexity-style questions
- `optimize-query-for-tool.md` - Adapt query to tool capabilities
- `categorize-queries.md` - Organize queries by type and priority

**Research Execution:**

- `execute-automated-research.md` - Orchestrate multi-tool research
- `execute-parallel-research.md` - Coordinate parallel tool execution
- `execute-sequential-research.md` - Progressive refinement research
- `execute-targeted-research.md` - Single-tool focused research
- `execute-fallback-research.md` - Manual workflow when tools unavailable

**Source Evaluation:**

- `assess-source-credibility.md` - Evidence-based source scoring
- `validate-research-accuracy.md` - Cross-validate findings
- `identify-research-conflicts.md` - Detect contradictions

**Synthesis & Integration:**

- `synthesize-multi-source-findings.md` - Merge findings with conflict resolution
- `integrate-research-findings.md` - Convert to atomic notes
- `track-research-provenance.md` - Record in Neo4j temporal graph

**Templates (7 total):**

- `research-report-tmpl.yaml` - Comprehensive research documentation
- `tool-detection-report-tmpl.yaml` - Discovered tools and capabilities
- `research-query-set-tmpl.yaml` - Organized query collection
- `source-assessment-tmpl.yaml` - Credibility evaluation format
- `research-synthesis-tmpl.yaml` - Multi-source finding merger
- `research-conflict-tmpl.yaml` - Contradiction identification
- `research-provenance-tmpl.yaml` - Neo4j provenance record

**Checklists (5 total):**

- `research-quality-checklist.md` - Validates thoroughness
- `source-credibility-checklist.md` - Ensures reliable sources
- `tool-optimization-checklist.md` - Confirms optimal tool usage
- `research-synthesis-checklist.md` - Validates finding integration
- `research-accuracy-checklist.md` - Cross-validation requirements

**Data/Knowledge Bases (6 total):**

- `research-tools-catalog.md` - MCP tool reference (Perplexity, WebSearch, Context7, etc.)
- `research-methodologies.md` - Research approach guidance
- `source-evaluation-criteria.md` - Authority assessment framework
- `query-optimization-patterns.md` - Tool-specific query templates
- `research-strategy-patterns.md` - Workflow decision trees
- `credibility-scoring-rubric.md` - Evidence-based source rating system

#### Enhanced Integration Requirements

**Required Integrations:**

- Obsidian MCP Tools: Create research reports and atomic notes
- Neo4j MCP: Record research provenance with temporal tracking

**Optional Integrations (Detected Automatically):**

- **Perplexity MCP:**
  - `mcp__perplexity__search` - Quick search with Sonar Pro
  - `mcp__perplexity__reason` - Complex multi-step reasoning
  - `mcp__perplexity__deep_research` - Comprehensive research

- **WebSearch MCP:**
  - `mcp__web_search__search` - Web search queries

- **Context7 MCP:**
  - `mcp__context7__resolve-library-id` - Find library documentation
  - `mcp__context7__get-library-docs` - Fetch technical docs

- **Custom MCP Servers:**
  - Any additional research tools detected in environment

---

## Enhanced Task Specifications

### Tool Detection & Profiling Tasks

#### Task: detect-research-tools.md

**Purpose:** Automatically discover available MCP research tools in the environment

**Input:**

- MCP server configuration (read from IDE/environment)
- Available tool list from MCP registry

**Process:**

1. Query MCP environment for available servers
2. Identify research-capable tools by patterns:
   - `mcp__perplexity__*` → Perplexity integration
   - `mcp__web_search__*` → Web search capability
   - `mcp__context7__*` → Documentation lookup
   - Custom patterns for other research tools
3. Test tool availability (ping/health check)
4. Record tool names, capabilities, and status
5. Generate tool detection report

**Output:**

- List of detected research tools with status
- Tool capability profile (search/reasoning/docs/etc.)
- Recommendations for missing tools
- Tool detection report document

**Quality Criteria:**

- All available tools detected
- No false positives (tools marked available but unreachable)
- Clear capability categorization
- Actionable recommendations

**Example Output:**

```yaml
detected_tools:
  - name: perplexity
    mcp_id: mcp__perplexity__*
    status: available
    capabilities:
      - quick_search (sonar_pro)
      - reasoning (sonar_reasoning)
      - deep_research (sonar_deep_research)
    recommended_for:
      - comprehensive_research
      - complex_reasoning
      - current_events

  - name: web_search
    mcp_id: mcp__web_search__search
    status: unavailable
    capabilities: []
    installation_guide: 'Install web-search MCP server'

  - name: context7
    mcp_id: mcp__context7__*
    status: available
    capabilities:
      - library_docs
      - api_reference
    recommended_for:
      - technical_documentation
      - api_research
```

---

#### Task: profile-tool-capabilities.md

**Purpose:** Analyze detected tools to understand their strengths and optimal use cases

**Input:**

- Detected tool list from `detect-research-tools.md`
- Tool metadata from MCP registry

**Process:**

1. For each detected tool, identify:
   - Primary capability (search, reasoning, docs, deep research)
   - Query optimization requirements
   - Rate limits and performance characteristics
   - Result format and structure
   - Strengths and limitations
2. Create capability profile
3. Map capabilities to research workflow phases
4. Generate optimization recommendations

**Output:**

- Tool capability profile for each detected tool
- Mapping of tools to research scenarios
- Query optimization guidelines
- Performance expectations

**Quality Criteria:**

- Accurate capability classification
- Clear strength/limitation analysis
- Actionable optimization guidance
- Scenario-to-tool mapping complete

**Example Output:**

```yaml
tool_profile:
  perplexity_search:
    primary_capability: quick_search
    optimal_for:
      - Simple factual queries
      - Current events (within knowledge cutoff)
      - Quick concept definitions
    query_optimization:
      - Keep queries specific and focused
      - Use keywords rather than natural language
      - Limit query length to 200 chars
    limitations:
      - No multi-step reasoning
      - Limited to recent information
    expected_performance:
      - Response time: 2-5 seconds
      - Result quality: High for factual queries

  perplexity_deep_research:
    primary_capability: comprehensive_research
    optimal_for:
      - Multi-faceted topics requiring synthesis
      - Comparative analysis
      - Trend analysis
      - Historical research
    query_optimization:
      - Use natural language questions
      - Include context and scope
      - Specify depth requirements
    limitations:
      - Slower than quick search (30-60s)
      - May hit rate limits
    expected_performance:
      - Response time: 30-90 seconds
      - Result quality: Very high for complex topics
```

---

#### Task: recommend-research-tools.md

**Purpose:** Suggest optimal tool configuration for user's research needs

**Input:**

- Tool detection results
- User's research patterns (if available)
- Topic complexity indicators

**Process:**

1. Analyze detected tools and gaps
2. Identify missing high-value tools
3. Generate installation recommendations
4. Prioritize by impact on research quality
5. Provide installation instructions
6. Suggest alternative workflows if tools unavailable

**Output:**

- Prioritized tool recommendation list
- Installation instructions for each
- Expected quality improvement
- Fallback strategies

**Quality Criteria:**

- Clear prioritization rationale
- Accurate installation instructions
- Realistic quality impact estimates
- Viable fallbacks provided

---

### Query Generation Tasks

#### Task: generate-research-queries.md

**Purpose:** Generate focused research queries optimized for detected tools

**Input:**

- Research topic or question
- Detected tool capabilities
- Research depth requirement (quick/medium/comprehensive)
- Target audience level (beginner/intermediate/expert)

**Process:**

1. Analyze topic to identify key concepts
2. Break down into sub-questions
3. Categorize questions by type:
   - Factual/definitional
   - Conceptual/explanatory
   - Procedural/how-to
   - Comparative/analytical
   - Historical/evolutionary
   - Critical/evaluative
4. Generate 10-25 queries based on depth requirement
5. Optimize each query for best-fit tool
6. Organize by execution order (foundations → advanced)
7. Format for easy copy/paste (if manual workflow)

**Output:**

- Organized query set (10-25 queries)
- Tool assignment for each query
- Execution order recommendation
- Estimated research time
- Query set document using template

**Quality Criteria:**

- Comprehensive coverage of topic
- Logical progression from basic to advanced
- Optimal tool assignment
- Copy/paste friendly formatting

**Example Output:**

```markdown
# Research Queries: React Hooks

**Generated:** 2025-11-04
**Topic:** React Hooks
**Depth:** Comprehensive
**Tool Status:** Perplexity (available), WebSearch (unavailable), Context7 (available)

## Category 1: Foundational Concepts (5 queries)

**Recommended Tool:** Perplexity Search (quick searches)

1. What is the React Hooks API and when was it introduced?
2. What problem did React Hooks solve compared to class components?
3. What are the Rules of Hooks and why do they exist?
4. What is the difference between useState and useEffect?
5. What are custom hooks and when should you use them?

## Category 2: Technical Deep Dives (8 queries)

**Recommended Tool:** Perplexity Deep Research

1. How does the useState hook manage state updates and re-renders?
2. What is the useEffect dependency array and how does React determine when to re-run effects?
3. How do closure issues manifest with hooks and how can they be prevented?
4. What are the performance implications of using hooks vs class components?
5. How does useCallback optimize component performance and when should it be used?
6. What is the difference between useMemo and useCallback?
7. How does useContext avoid prop drilling and what are its limitations?
8. What are the common pitfalls when migrating from class components to hooks?

## Category 3: Code Examples & Patterns (6 queries)

**Recommended Tool:** Context7 + Perplexity Search

1. What are the most common React hooks patterns for data fetching?
2. How do you implement form handling with React hooks?
3. What are best practices for managing complex state with useReducer?
4. How do you implement debouncing and throttling with hooks?
5. What are common patterns for composing multiple custom hooks?
6. How do you test components that use hooks?

## Category 4: Advanced Topics (4 queries)

**Recommended Tool:** Perplexity Reasoning

1. How do concurrent features in React 18 affect hook behavior?
2. What are the trade-offs between useState and useReducer for complex state?
3. How should hooks be organized in large-scale applications?
4. What are emerging patterns in the React hooks ecosystem?

## Category 5: Community & Ecosystem (2 queries)

**Recommended Tool:** Perplexity Search

1. What are the most popular React hooks libraries and their use cases?
2. What are the common criticisms of React hooks from the community?

---

**Execution Strategy:**

- **Parallel Execution:** Categories 1 & 5 (fast searches)
- **Sequential Execution:** Categories 2-4 (deep research with refinement)
- **Estimated Time:** 15-20 minutes (automated), 45-60 minutes (manual)
```

---

#### Task: generate-deep-questions.md

**Purpose:** Generate 20-30 comprehensive Perplexity-style research questions for deep research

**Input:**

- Research topic
- Specific focus areas (optional)
- Depth level (standard/expert)

**Process:**

1. Analyze topic for multiple dimensions:
   - Historical context
   - Current state of the art
   - Future trends
   - Practical applications
   - Theoretical foundations
   - Controversies and debates
   - Ecosystem and tooling
   - Performance and optimization
   - Security and best practices
   - Community perspectives
2. Generate 2-3 questions per dimension
3. Frame questions to encourage comprehensive responses
4. Optimize for Perplexity deep research format
5. Include context and constraints in questions
6. Order by logical learning progression

**Output:**

- 20-30 comprehensive research questions
- Grouped by dimension
- Optimized for deep research tool
- Expected research depth per question

**Quality Criteria:**

- Questions invite comprehensive answers
- Cover multiple dimensions of topic
- Avoid yes/no or simple factual questions
- Include sufficient context
- Logical progression

**Example Output:**

```markdown
# Deep Research Questions: GraphQL API Design

**Generated:** 2025-11-04
**Topic:** GraphQL API Design
**Depth:** Expert
**Optimized For:** Perplexity Deep Research

## Historical & Evolutionary Context (3)

1. How did GraphQL emerge from Facebook's needs, what problems did it solve compared to REST and RPC, and how has the specification evolved since its open-source release in 2015?

2. What were the key debates and controversies during GraphQL's adoption phase (2015-2020), and how did the community address concerns about complexity, caching, and security?

3. How has the GraphQL ecosystem matured regarding tooling, server implementations, and client libraries, and what patterns have emerged as best practices?

## Architectural Foundations (4)

4. What are the fundamental architectural differences between GraphQL and REST that affect API design decisions, including query flexibility, type systems, and versioning strategies?

5. How should schema design balance granularity (fine-grained fields vs. coarse aggregations) with performance concerns like N+1 queries and database optimization?

6. What are the trade-offs between schema-first and code-first approaches to GraphQL API development, and when is each approach most appropriate?

7. How do GraphQL subscriptions work architecturally, what are the scaling challenges with WebSocket connections, and what are alternative real-time patterns?

## Schema Design Patterns (4)

8. What are the proven patterns for designing GraphQL schemas that remain stable and evolvable over time, including interface design, union types, and field deprecation strategies?

9. How should pagination be implemented in GraphQL APIs, comparing cursor-based, offset-based, and relay-style pagination approaches with their respective trade-offs?

10. What are best practices for handling errors in GraphQL responses, including field-level errors, union error types, and the debate over using HTTP status codes?

11. How should authentication and authorization be integrated into GraphQL APIs, comparing schema-level, resolver-level, and directive-based approaches?

## Performance Optimization (4)

12. What are the most effective strategies for solving the N+1 query problem in GraphQL, including dataloader patterns, query batching, and database query optimization?

13. How should caching be implemented for GraphQL APIs given the dynamic nature of queries, including HTTP caching, persisted queries, and application-level cache patterns?

14. What are the performance implications of deep query nesting and how can query complexity analysis and depth limiting protect against abuse without hindering legitimate use?

15. How do Apollo Federation and schema stitching compare for building distributed GraphQL architectures, and what are the performance and operational trade-offs?

## Security Considerations (3)

16. What are the primary security vulnerabilities in GraphQL APIs (introspection leakage, query depth attacks, field duplication DOS) and what mitigation strategies are most effective?

17. How should rate limiting and query cost analysis be implemented for GraphQL APIs given that traditional per-endpoint rate limiting doesn't apply?

18. What are best practices for securing GraphQL APIs in production, including disabling introspection, implementing persisted queries, and handling sensitive data exposure?

## Tooling & Developer Experience (3)

19. How has GraphQL tooling evolved to support developer productivity, including code generation, schema documentation, and IDE integration, and what are the current best-in-class tools?

20. What are the trade-offs between different GraphQL server implementations (Apollo Server, GraphQL Yoga, Mercurius, Hasura) in terms of features, performance, and ecosystem support?

21. How should GraphQL APIs be tested, including unit testing resolvers, integration testing queries, and contract testing for federated schemas?

## Real-World Implementation (3)

22. What lessons have large-scale GraphQL implementations taught us about API design, performance, and operational complexity (case studies: GitHub, Shopify, Netflix)?

23. How do successful teams handle GraphQL schema governance and evolution in microservices environments, including breaking change management and client migration?

24. What are common pitfalls when migrating from REST to GraphQL, and what incremental adoption strategies minimize risk while delivering value?

## Ecosystem & Future Direction (2)

25. How is the GraphQL specification evolving to address current limitations, including defer/stream directives, input unions, and improved subscription support?

26. What emerging patterns and technologies are shaping the future of GraphQL, including edge GraphQL, serverless GraphQL, and integration with modern frontend frameworks?

---

**Research Execution Strategy:**

- Execute questions in order (foundational → advanced)
- Use Perplexity Deep Research for all questions
- Estimated time: 45-60 minutes
- Expected output: 15-20 pages of comprehensive findings
```

---

#### Task: optimize-query-for-tool.md

**Purpose:** Adapt a research query to specific tool capabilities and constraints

**Input:**

- Original query
- Target tool (perplexity_search/perplexity_deep_research/context7/websearch)
- Tool capability profile

**Process:**

1. Analyze query characteristics (complexity, scope, format)
2. Retrieve tool optimization patterns from knowledge base
3. Apply tool-specific transformations:
   - **Perplexity Search:** Concise, keyword-focused, specific
   - **Perplexity Deep Research:** Natural language, context-rich, comprehensive
   - **Perplexity Reasoning:** Multi-step, logical, analytical
   - **Context7:** Library/framework name, version, specific API
   - **WebSearch:** SEO-optimized, keyword combinations
4. Add constraints if needed (date ranges, domains, file types)
5. Validate optimized query against tool limitations
6. Provide reasoning for changes made

**Output:**

- Optimized query for target tool
- Explanation of optimization changes
- Expected result quality
- Alternative tools if optimization not possible

**Quality Criteria:**

- Query matches tool's optimal input format
- Respects tool constraints (length, complexity)
- Maintains original intent
- Improves expected result quality

**Example Input/Output:**

**Original Query:** "How has understanding of React component lifecycle evolved from class components to hooks?"

**Tool:** Perplexity Search
**Optimized Query:** "React component lifecycle evolution class components hooks comparison"
**Changes:** Removed question framing, extracted keywords, made concise
**Expected Quality:** Good for overview, but lacks depth

**Tool:** Perplexity Deep Research
**Optimized Query:** "How has understanding of React component lifecycle evolved from class components to hooks, including the motivations for the change, the mental model shift required, and how lifecycle methods map to hook equivalents?"
**Changes:** Added context, specified desired depth areas, kept natural language
**Expected Quality:** Excellent for comprehensive understanding

**Tool:** Context7
**Optimized Query:** Library: "react", Topic: "hooks lifecycle comparison"
**Changes:** Structured for Context7 API, separated library from topic
**Expected Quality:** Excellent for official documentation

---

### Research Execution Tasks

#### Task: execute-automated-research.md

**Purpose:** Orchestrate multi-tool research execution with adaptive strategy

**Input:**

- Research topic
- Generated query set
- Tool detection results
- Research depth preference (quick/medium/comprehensive)

**Process:**

1. **Strategy Selection:**
   - Analyze query set and available tools
   - Select execution strategy:
     - **Parallel:** Multiple independent queries, fast tools
     - **Sequential:** Refinement needed, deep research
     - **Hybrid:** Mix of parallel and sequential
   - Estimate total execution time

2. **Query Execution:**
   - Assign queries to optimal tools
   - Execute based on strategy:
     - **Parallel:** Launch all queries simultaneously
     - **Sequential:** Execute → analyze → refine → repeat
   - Handle tool failures with fallbacks
   - Respect rate limits

3. **Result Collection:**
   - Gather findings from all tools
   - Extract key information, citations, examples
   - Track source URLs and timestamps
   - Record tool provenance for each finding

4. **Quality Assessment:**
   - Assess source credibility for each finding
   - Identify conflicts between sources
   - Flag low-confidence findings
   - Calculate completeness score

5. **Synthesis:**
   - Merge findings from multiple sources
   - Resolve conflicts
   - Organize by topic/subtopic
   - Generate research report

**Output:**

- Comprehensive research report
- Organized findings with citations
- Source credibility assessments
- Conflict identification
- Completeness score
- Tool usage statistics

**Quality Criteria:**

- All queries executed successfully or fallbacks used
- Sources assessed for credibility
- Conflicts identified and addressed
- Complete research report generated
- Provenance tracked

**Error Handling:**

- **Tool Unavailable:** Fall back to alternative tool or manual workflow
- **Rate Limited:** Queue remaining queries, warn user
- **Low Quality Results:** Flag and suggest manual follow-up
- **Conflicts Found:** Present both sides, recommend user review

---

#### Task: execute-parallel-research.md

**Purpose:** Execute multiple research queries simultaneously across available tools

**Input:**

- Query set categorized by tool
- Tool availability status
- Rate limit constraints

**Process:**

1. Group queries by assigned tool
2. Calculate parallel execution limits (rate limits, API quotas)
3. Launch queries in batches:
   - Batch size = MIN(available_tools, rate_limit, user_preference)
   - Wait for batch completion before next batch
4. Collect results as they arrive
5. Handle failures individually without blocking other queries
6. Aggregate results when all queries complete

**Output:**

- Collected findings from all queries
- Execution statistics (time per query, success rate)
- Failed queries with error details
- Tool usage summary

**Quality Criteria:**

- Maximum parallelism without violating rate limits
- Individual failures don't block other queries
- All results collected and tagged with source
- Performance metrics tracked

---

#### Task: execute-sequential-research.md

**Purpose:** Execute research queries with progressive refinement based on previous results

**Input:**

- Initial query set
- Tool availability
- Refinement strategy (depth-first vs. breadth-first)

**Process:**

1. Execute foundational queries first
2. Analyze results to identify:
   - Gaps requiring additional queries
   - Topics needing deeper investigation
   - Contradictions requiring clarification
3. Generate follow-up queries based on findings
4. Execute follow-up queries
5. Repeat refinement cycle until:
   - Completeness threshold reached
   - Max depth reached
   - User satisfaction achieved

**Output:**

- Comprehensive findings with refinement history
- Generated follow-up queries and rationale
- Depth reached per topic
- Refinement decision log

**Quality Criteria:**

- Each refinement improves completeness
- Follow-up queries address real gaps
- Refinement stops at appropriate depth
- Decision log shows clear reasoning

---

### Source Evaluation Tasks

#### Task: assess-source-credibility.md

**Purpose:** Evaluate source authority and reliability using evidence-based criteria

**Input:**

- Source URL or reference
- Content excerpt
- Publication date
- Author/organization

**Process:**

1. **Authority Assessment:**
   - Check domain reputation (official docs, academic, news, blog)
   - Identify author credentials
   - Assess organization authority
   - Rate: High/Medium/Low/Unknown

2. **Currency Assessment:**
   - Check publication date
   - Compare to topic evolution timeline
   - Flag outdated information
   - Rate: Current/Recent/Dated/Outdated

3. **Accuracy Indicators:**
   - Look for citations and references
   - Check for factual errors
   - Compare with other sources
   - Rate: Well-sourced/Partially-sourced/Unsourced

4. **Objectivity Assessment:**
   - Identify bias indicators
   - Check for commercial interests
   - Assess balance of perspective
   - Rate: Objective/Somewhat-biased/Highly-biased

5. **Coverage Assessment:**
   - Evaluate depth of treatment
   - Check comprehensiveness
   - Rate: Comprehensive/Moderate/Superficial

6. **Calculate Overall Credibility Score:**
   - Weight factors by importance
   - Generate 0-100 score
   - Classify: Authoritative/Reliable/Questionable/Unreliable

**Output:**

- Source credibility score (0-100)
- Classification (Authoritative/Reliable/Questionable/Unreliable)
- Detailed assessment report
- Recommendations for use

**Quality Criteria:**

- Evidence-based assessment (not subjective)
- Clear rationale for each rating
- Consistent scoring across sources
- Actionable recommendations

**Credibility Scoring Rubric:**

```yaml
authoritative_sources: # Score 85-100
  - Official documentation (react.dev, developer.mozilla.org)
  - Peer-reviewed academic papers
  - Authoritative books from recognized publishers
  - Primary source materials (RFCs, specs, standards)

reliable_sources: # Score 70-84
  - Reputable tech blogs (CSS-Tricks, Smashing Magazine)
  - Industry expert personal blogs (Dan Abramov, Kent C. Dodds)
  - Conference talks by recognized experts
  - Well-maintained open source documentation
  - Major tech news sites (TechCrunch, Ars Technica)

questionable_sources: # Score 50-69
  - Tutorial sites with unknown authors
  - Community forums (Stack Overflow, Reddit)
  - Dated content (>3 years for fast-moving tech)
  - Marketing content with bias
  - AI-generated content without verification

unreliable_sources: # Score 0-49
  - Content farms, low-quality SEO sites
  - Unverified claims without citations
  - Severely outdated content
  - Anonymous sources with no credentials
  - Sites with known misinformation history
```

---

#### Task: validate-research-accuracy.md

**Purpose:** Cross-validate findings across multiple sources to ensure accuracy

**Input:**

- Research findings from multiple sources
- Source credibility assessments

**Process:**

1. **Fact Extraction:**
   - Identify factual claims in findings
   - Extract specific assertions (dates, statistics, quotes, technical specs)

2. **Cross-Validation:**
   - Compare claims across sources
   - Identify consensus (3+ sources agree)
   - Identify conflicts (sources disagree)
   - Identify single-source claims (only one source)

3. **Confidence Assessment:**
   - **High Confidence:** Consensus from authoritative sources
   - **Medium Confidence:** Consensus from reliable sources, or single authoritative source
   - **Low Confidence:** Conflicts present, or single questionable source
   - **Unverified:** Single source, no corroboration possible

4. **Conflict Resolution:**
   - For conflicts, prioritize more authoritative sources
   - Check publication dates (newer may be more accurate)
   - Flag for manual review if resolution unclear

5. **Recommendation Generation:**
   - Accept high-confidence findings
   - Flag medium-confidence for potential follow-up
   - Require manual review for low-confidence
   - Mark unverified findings clearly

**Output:**

- Accuracy validation report
- Findings categorized by confidence level
- Identified conflicts with resolution recommendations
- Manual review queue for uncertain findings

**Quality Criteria:**

- All factual claims validated
- Clear confidence levels assigned
- Conflicts identified and analyzed
- Actionable recommendations provided

---

#### Task: identify-research-conflicts.md

**Purpose:** Detect contradictions and disagreements across research sources

**Input:**

- Research findings from multiple sources
- Source credibility scores

**Process:**

1. **Conflict Detection:**
   - Identify claims about the same topic from different sources
   - Compare claims for agreement/disagreement
   - Classify conflicts:
     - **Hard Conflict:** Direct contradiction (A says X, B says not-X)
     - **Soft Conflict:** Partial disagreement (A emphasizes X, B de-emphasizes X)
     - **Context Conflict:** True in different contexts (A says X for case 1, B says Y for case 2)

2. **Conflict Analysis:**
   - Retrieve source credibility scores
   - Check publication dates (may reflect evolution)
   - Identify potential reasons for conflict:
     - Temporal (practices evolved over time)
     - Contextual (different use cases)
     - Philosophical (different schools of thought)
     - Error (one source is incorrect)

3. **Resolution Strategy:**
   - **Hard Conflicts:** Recommend manual review, favor more authoritative source
   - **Soft Conflicts:** Present both perspectives with context
   - **Context Conflicts:** Clarify contexts, both may be correct
   - **Temporal Conflicts:** Show evolution timeline

4. **Integration Recommendation:**
   - Accept if resolvable programmatically
   - Flag for manual review if complex
   - Suggest additional research if needed

**Output:**

- Conflict identification report
- Classification of each conflict
- Resolution recommendations
- Manual review queue

**Quality Criteria:**

- All conflicts identified
- Clear classification and analysis
- Practical resolution strategies
- Actionable next steps

---

### Synthesis & Integration Tasks

#### Task: synthesize-multi-source-findings.md

**Purpose:** Merge research findings from multiple sources with conflict resolution

**Input:**

- Raw findings from all research tools
- Source credibility assessments
- Conflict identification results

**Process:**

1. **Organize Findings:**
   - Group by topic and subtopic
   - Identify overlapping coverage
   - Detect gaps (topics covered by few sources)

2. **Merge Overlapping Content:**
   - For topics covered by multiple sources:
     - Extract unique insights from each
     - Combine complementary information
     - Resolve conflicts using credibility scores
     - Create comprehensive synthesis

3. **Handle Gaps:**
   - Flag topics with sparse coverage
   - Recommend additional research if critical
   - Note limitations in final report

4. **Synthesize Narrative:**
   - Create coherent synthesis text
   - Integrate multiple perspectives
   - Highlight consensus vs. debate
   - Note confidence levels

5. **Citation Integration:**
   - Provide citation for every claim
   - Use multiple citations for critical claims
   - Format citations consistently

6. **Generate Research Report:**
   - Use research-report-tmpl.yaml
   - Include synthesis, sources, conflicts, gaps
   - Provide confidence assessment
   - Recommend next steps

**Output:**

- Comprehensive research report
- Synthesized findings with citations
- Confidence levels per section
- Identified gaps and recommendations
- Source list with credibility scores

**Quality Criteria:**

- All sources integrated
- Conflicts resolved or clearly noted
- Every claim has citation
- Gaps identified
- Coherent narrative flow

---

#### Task: integrate-research-findings.md

**Purpose:** Convert research findings into atomic notes and integrate into knowledge base

**Input:**

- Research report with synthesized findings
- Source credibility data
- Existing vault structure

**Process:**

1. **Atomization:**
   - Break research report into atomic concepts
   - One concept per note
   - Apply structural-analysis-agent principles

2. **Note Creation:**
   - For each atomic concept:
     - Create note with atomic-note-tmpl.yaml
     - Add source citations in frontmatter
     - Add research provenance metadata
     - Set appropriate tags

3. **Link Discovery:**
   - Query Smart Connections for related notes
   - Create bidirectional links
   - Update relevant MOCs

4. **Neo4j Integration:**
   - Create (:ResearchNote) nodes
   - Link to (:CaptureEvent) from original research request
   - Create [:SUPPORTS] edges to related notes
   - Add temporal metadata

5. **MOC Updates:**
   - Identify relevant MOCs
   - Add new notes to appropriate sections
   - Update MOC summaries if needed

6. **Tracking:**
   - Record research → notes mapping
   - Track usage in content creation
   - Enable provenance queries

**Output:**

- Created atomic notes in vault
- Updated MOCs
- Neo4j provenance graph
- Integration report

**Quality Criteria:**

- All findings atomized appropriately
- Sources preserved with citations
- Links created to existing knowledge
- Neo4j graph updated
- MOCs reflect new knowledge

---

#### Task: track-research-provenance.md

**Purpose:** Record research execution in Neo4j temporal graph for provenance tracking

**Input:**

- Research report ID
- Tool usage statistics
- Source credibility data
- Created atomic notes

**Process:**

1. **Create Research Node:**

   ```cypher
   CREATE (r:ResearchProject {
     id: UUID,
     topic: "...",
     created_at: timestamp,
     method: "automated"|"manual"|"import",
     tools_used: ["perplexity", "context7"],
     query_count: 25,
     source_count: 42,
     duration_seconds: 1200
   })
   ```

2. **Link to Tools:**

   ```cypher
   CREATE (r)-[:USED_TOOL {query_count: 15, success_rate: 1.0}]->(t:ResearchTool {name: "perplexity"})
   ```

3. **Link to Sources:**

   ```cypher
   CREATE (r)-[:CONSULTED {credibility_score: 85}]->(s:Source {url: "...", domain: "..."})
   ```

4. **Link to Created Notes:**

   ```cypher
   CREATE (r)-[:PRODUCED]->(n:AtomicNote {id: "...", title: "..."})
   ```

5. **Temporal Tracking:**

   ```cypher
   CREATE (r)-[:OCCURRED_AT]->(date:Date {date: "2025-11-04"})
   CREATE (r)-[:TRIGGERED_BY]->(gap:KnowledgeGap {identified_at: timestamp})
   ```

6. **Enable Queries:**
   - "What research informed this note?"
   - "Which tools have been most effective?"
   - "What sources do I rely on most?"
   - "How has my research activity evolved?"

**Output:**

- Created Neo4j research provenance graph
- Queryable research history
- Tool effectiveness metrics
- Source usage patterns

**Quality Criteria:**

- Complete provenance chain
- All relationships created
- Temporal metadata recorded
- Queries validated

---

## Enhanced Template Specifications

### Template: tool-detection-report-tmpl.yaml

**Purpose:** Document detected research tools and capabilities

**Structure:**

```yaml
---
template_name: tool-detection-report
version: 1.0
category: research
output_format: markdown
---
document_structure:
  - section: detection_summary
    title: 'Research Tool Detection Summary'
    required: true
    fields:
      - name: detection_date
        type: date
        description: 'When tool detection was performed'

      - name: environment
        type: string
        description: 'IDE/environment context (Claude Code, Cursor, VS Code)'

      - name: total_tools_detected
        type: integer
        description: 'Count of detected research tools'

      - name: recommended_tools
        type: array
        description: 'Tools recommended for installation'

  - section: detected_tools
    title: 'Detected Research Tools'
    required: true
    repeatable: true
    fields:
      - name: tool_name
        type: string
        description: 'Human-readable tool name'

      - name: mcp_id
        type: string
        description: 'MCP server identifier'

      - name: status
        type: enum
        values: [available, unavailable, error]

      - name: capabilities
        type: array
        description: 'List of tool capabilities'

      - name: optimal_use_cases
        type: array
        description: 'What this tool is best for'

      - name: limitations
        type: array
        description: 'Known constraints or weaknesses'

  - section: capability_coverage
    title: 'Research Capability Coverage'
    required: true
    fields:
      - name: quick_search
        type: boolean
        description: 'Fast factual searches available'

      - name: deep_research
        type: boolean
        description: 'Comprehensive research available'

      - name: reasoning
        type: boolean
        description: 'Multi-step reasoning available'

      - name: documentation
        type: boolean
        description: 'Technical docs lookup available'

      - name: gap_analysis
        type: text
        description: 'Missing capabilities and impact'

  - section: recommendations
    title: 'Tool Installation Recommendations'
    required: false
    fields:
      - name: priority_tools
        type: array
        description: 'High-priority missing tools'
        elements:
          - tool_name: string
          - reason: string
          - installation_guide: string
          - expected_benefit: string

  - section: optimization_tips
    title: 'Query Optimization Tips'
    required: true
    fields:
      - name: tips
        type: array
        description: 'How to optimize queries for detected tools'

llm_instructions: |
  When populating this template:

  1. DETECTION SUMMARY:
     - Record exact detection timestamp
     - List total detected tools with status breakdown
     - Be honest about gaps and limitations

  2. DETECTED TOOLS:
     - One section per detected tool
     - Provide accurate capability assessment
     - Be specific about optimal use cases
     - Clearly state limitations

  3. CAPABILITY COVERAGE:
     - Map detected tools to capabilities
     - Identify gaps in coverage
     - Assess impact of missing capabilities

  4. RECOMMENDATIONS:
     - Prioritize by impact on research quality
     - Provide concrete installation instructions
     - Be realistic about expected benefits
     - Offer fallback strategies for unavailable tools

  5. OPTIMIZATION TIPS:
     - Provide actionable query optimization advice
     - Tailor to detected tool combination
     - Include examples for common query types

output_example: |
  # Research Tool Detection Report

  **Detection Date:** 2025-11-04 14:32:15
  **Environment:** Claude Code
  **Tools Detected:** 2 available, 1 unavailable

  ## Detected Research Tools

  ### Perplexity (Available) ✓
  - **MCP ID:** `mcp__perplexity__*`
  - **Status:** Available
  - **Capabilities:**
    - Quick search (Sonar Pro)
    - Deep research (Sonar Deep Research)
    - Complex reasoning (Sonar Reasoning Pro)
  - **Optimal Use Cases:**
    - Comprehensive research on complex topics
    - Current events and recent developments
    - Multi-faceted analysis requiring synthesis
  - **Limitations:**
    - Rate limits may apply for deep research
    - Response time 30-90s for deep research

  ### Context7 (Available) ✓
  - **MCP ID:** `mcp__context7__*`
  - **Status:** Available
  - **Capabilities:**
    - Library documentation lookup
    - API reference retrieval
  - **Optimal Use Cases:**
    - Technical framework documentation
    - API reference research
    - Official documentation queries
  - **Limitations:**
    - Limited to libraries in Context7 database
    - May not have latest versions

  ### WebSearch (Unavailable) ✗
  - **MCP ID:** `mcp__web_search__*`
  - **Status:** Unavailable
  - **Impact:** Medium - Perplexity provides good alternative

  ## Research Capability Coverage

  - ✓ **Quick Search:** Perplexity Sonar Pro
  - ✓ **Deep Research:** Perplexity Deep Research
  - ✓ **Reasoning:** Perplexity Sonar Reasoning Pro
  - ✓ **Documentation:** Context7
  - ✗ **Web Search:** Not available (fallback: Perplexity)

  **Gap Analysis:** No critical gaps. Perplexity covers most research needs. WebSearch would provide broader coverage but is not essential.

  ## Tool Installation Recommendations

  ### Optional: WebSearch MCP
  - **Priority:** Low
  - **Reason:** Adds broader web search, but Perplexity covers most needs
  - **Installation:** `npm install -g web-search-mcp`
  - **Expected Benefit:** 10-15% improvement in breadth of sources

  ## Query Optimization Tips

  ### For Perplexity Search (Quick):
  - Keep queries concise (< 200 chars)
  - Use specific keywords rather than questions
  - Example: "React hooks useState closure issues" (good)
  - Example: "How do I fix closure issues with useState?" (less optimal)

  ### For Perplexity Deep Research:
  - Use natural language questions
  - Include context and desired depth
  - Example: "How do closure issues manifest in React hooks, what causes them, and what are the best practices to prevent them?"

  ### For Context7:
  - Specify library name and version
  - Focus on specific APIs or concepts
  - Example: Library: "react", Topic: "useState closure behavior"
```

---

### Template: research-query-set-tmpl.yaml

**Purpose:** Organize generated research queries with tool assignments and execution strategy

**Structure:**

```yaml
---
template_name: research-query-set
version: 1.0
category: research
output_format: markdown
---
document_structure:
  - section: query_set_metadata
    title: 'Query Set Metadata'
    required: true
    fields:
      - name: generated_date
        type: date

      - name: topic
        type: string
        description: 'Research topic'

      - name: depth_level
        type: enum
        values: [quick, medium, comprehensive]

      - name: total_queries
        type: integer

      - name: tool_status
        type: text
        description: 'Available tools summary'

      - name: estimated_time
        type: string
        description: 'Expected research duration'

  - section: query_categories
    title: 'Query Categories'
    required: true
    repeatable: true
    fields:
      - name: category_name
        type: string

      - name: category_description
        type: text

      - name: recommended_tool
        type: string

      - name: execution_order
        type: integer

      - name: queries
        type: array
        elements:
          - query_text: string
          - priority: enum [high, medium, low]
          - estimated_time: string

  - section: execution_strategy
    title: 'Execution Strategy'
    required: true
    fields:
      - name: strategy_type
        type: enum
        values: [parallel, sequential, hybrid]

      - name: parallel_categories
        type: array
        description: 'Categories to execute in parallel'

      - name: sequential_categories
        type: array
        description: 'Categories requiring sequential execution'

      - name: rationale
        type: text
        description: 'Why this strategy was chosen'

  - section: tool_assignments
    title: 'Tool Assignments'
    required: true
    fields:
      - name: assignments
        type: array
        elements:
          - tool_name: string
          - query_count: integer
          - categories: array
          - estimated_time: string

llm_instructions: |
  When generating query sets:

  1. ORGANIZE BY CATEGORY:
     - Group related queries together
     - Progress from foundational to advanced
     - Assign optimal tool to each category

  2. OPTIMIZE FOR TOOLS:
     - Assign quick searches to fast tools (Perplexity Search)
     - Assign deep research to comprehensive tools (Perplexity Deep Research)
     - Assign documentation queries to Context7

  3. EXECUTION STRATEGY:
     - Parallel: Independent queries, fast tools
     - Sequential: Build on previous results, deep research
     - Hybrid: Mix based on query dependencies

  4. PRACTICALITY:
     - Estimate realistic time requirements
     - Consider rate limits
     - Provide copy/paste friendly format for manual workflow
```

---

### Template: research-synthesis-tmpl.yaml

**Purpose:** Document synthesized findings from multiple research sources

**Structure:**

```yaml
---
template_name: research-synthesis
version: 1.0
category: research
output_format: markdown
---
document_structure:
  - section: synthesis_metadata
    title: 'Research Synthesis Metadata'
    required: true
    fields:
      - name: topic
        type: string

      - name: synthesis_date
        type: date

      - name: source_count
        type: integer

      - name: tool_usage
        type: array
        description: 'Tools used with query counts'

      - name: completeness_score
        type: integer
        description: '0-100 assessment of coverage'

  - section: key_findings
    title: 'Key Findings'
    required: true
    repeatable: true
    fields:
      - name: finding
        type: text
        description: 'Core insight or fact'

      - name: confidence
        type: enum
        values: [high, medium, low, unverified]

      - name: supporting_sources
        type: array
        description: 'Citations supporting this finding'

      - name: contradictions
        type: text
        description: 'Any conflicting information found'

  - section: synthesis_narrative
    title: 'Synthesized Narrative'
    required: true
    fields:
      - name: narrative
        type: long_text
        description: 'Coherent synthesis integrating all findings'

      - name: citations
        type: inline
        description: 'Inline citations in narrative'

  - section: source_analysis
    title: 'Source Analysis'
    required: true
    fields:
      - name: sources
        type: array
        repeatable: true
        elements:
          - url: string
          - title: string
          - credibility_score: integer
          - usage_count: integer
          - key_contributions: text

  - section: conflicts_identified
    title: 'Conflicts & Contradictions'
    required: false
    fields:
      - name: conflicts
        type: array
        elements:
          - conflict_description: text
          - source_a: string
          - source_b: string
          - resolution: text

  - section: gaps_and_recommendations
    title: 'Gaps & Next Steps'
    required: true
    fields:
      - name: identified_gaps
        type: array

      - name: recommendations
        type: array

      - name: manual_review_needed
        type: boolean

llm_instructions: |
  When synthesizing research:

  1. KEY FINDINGS:
     - Extract core insights
     - Assign confidence based on source agreement
     - Cite all supporting sources
     - Note any contradictions

  2. NARRATIVE:
     - Create coherent synthesis text
     - Integrate multiple perspectives
     - Highlight consensus vs. debate
     - Use inline citations

  3. SOURCE ANALYSIS:
     - List all sources with credibility scores
     - Note which sources were most valuable
     - Assess overall source quality

  4. CONFLICTS:
     - Identify all contradictions
     - Provide context for conflicts
     - Recommend resolution approach

  5. GAPS:
     - Identify incomplete coverage
     - Prioritize gaps by importance
     - Suggest follow-up research
```

---

## Enhanced Checklist Specifications

### Checklist: tool-optimization-checklist.md

**Purpose:** Ensure research queries are optimized for detected tools

**Checklist Items:**

```markdown
# Research Tool Optimization Checklist

Use this checklist to validate that research queries are optimally configured for detected tools.

## Tool Detection

- [ ] Tool detection executed before query generation
- [ ] All available research tools identified
- [ ] Tool capabilities profiled accurately
- [ ] Missing high-value tools flagged
- [ ] User notified of tool status

## Query-Tool Matching

- [ ] Each query assigned to optimal tool
- [ ] Tool capabilities match query requirements
- [ ] Complex queries assigned to deep research tools
- [ ] Quick factual queries assigned to fast tools
- [ ] Documentation queries assigned to Context7 (if available)

## Query Optimization

- [ ] Queries formatted for assigned tool
- [ ] Perplexity Search queries: Concise, keyword-focused
- [ ] Perplexity Deep Research queries: Natural language, context-rich
- [ ] Context7 queries: Library specified, topic focused
- [ ] All queries respect tool constraints (length, complexity)

## Execution Strategy

- [ ] Execution strategy selected (parallel/sequential/hybrid)
- [ ] Parallel execution used for independent queries
- [ ] Sequential execution used where refinement needed
- [ ] Rate limits considered in execution plan
- [ ] Fallback strategy defined for tool failures

## Performance Optimization

- [ ] Estimated execution time realistic
- [ ] Batch sizes respect rate limits
- [ ] Parallel execution maximized where safe
- [ ] Tool strengths leveraged appropriately
- [ ] Redundant queries eliminated

## Quality Assurance

- [ ] All queries clear and specific
- [ ] Topic coverage comprehensive
- [ ] Query progression logical (basic → advanced)
- [ ] Success criteria defined per query
- [ ] Manual review triggers identified
```

---

### Checklist: research-synthesis-checklist.md

**Purpose:** Validate quality of synthesized research findings

**Checklist Items:**

```markdown
# Research Synthesis Quality Checklist

Use this checklist to ensure research findings are properly synthesized and integrated.

## Source Integration

- [ ] All sources reviewed and integrated
- [ ] Overlapping content merged appropriately
- [ ] Unique insights extracted from each source
- [ ] Source credibility assessed for all sources
- [ ] High-credibility sources prioritized

## Citation & Attribution

- [ ] Every finding has supporting citation
- [ ] Critical claims have multiple citations
- [ ] Citations formatted consistently
- [ ] Source URLs accessible and valid
- [ ] Publication dates included

## Conflict Resolution

- [ ] All conflicts between sources identified
- [ ] Conflicts analyzed and categorized
- [ ] Resolution strategy applied
- [ ] Unresolvable conflicts flagged for review
- [ ] User notified of significant contradictions

## Confidence Assessment

- [ ] Confidence levels assigned to all findings
- [ ] High confidence: Multiple authoritative sources agree
- [ ] Medium confidence: Single authoritative or multiple reliable sources
- [ ] Low confidence: Single source or conflicts present
- [ ] Unverified: No corroboration available
- [ ] Confidence levels clearly marked in output

## Gap Identification

- [ ] Topic coverage assessed
- [ ] Gaps in coverage identified
- [ ] Missing information prioritized
- [ ] Follow-up research recommended where needed
- [ ] User notified of significant gaps

## Narrative Quality

- [ ] Synthesis flows logically
- [ ] Multiple perspectives integrated
- [ ] Consensus vs. debate clearly indicated
- [ ] Technical accuracy maintained
- [ ] Appropriate depth for audience

## Integration Readiness

- [ ] Findings structured for atomization
- [ ] Clear concept boundaries identified
- [ ] Source attribution preserved
- [ ] Ready for note creation
- [ ] MOC integration points identified

## Provenance Tracking

- [ ] Research method recorded (automated/manual/import)
- [ ] Tools used documented
- [ ] Execution timestamp captured
- [ ] Query set preserved
- [ ] Ready for Neo4j integration
```

---

### Checklist: research-accuracy-checklist.md

**Purpose:** Validate research findings for accuracy and reliability

**Checklist Items:**

```markdown
# Research Accuracy Validation Checklist

Use this checklist to verify research findings are accurate and reliable.

## Source Credibility

- [ ] All sources assessed for authority
- [ ] Authoritative sources (official docs, academic) prioritized
- [ ] Questionable sources flagged
- [ ] Source reputation verified (domain, author, organization)
- [ ] Commercial bias identified where present

## Currency Validation

- [ ] Publication dates checked for all sources
- [ ] Outdated information flagged (>3 years for fast-moving tech)
- [ ] Temporal context considered (practices may have evolved)
- [ ] Current best practices prioritized
- [ ] Historical information contextualized

## Fact Verification

- [ ] Factual claims extracted from findings
- [ ] Claims cross-referenced across sources
- [ ] Consensus identified (3+ sources agree)
- [ ] Conflicts identified and analyzed
- [ ] Single-source claims flagged

## Technical Accuracy

- [ ] Code examples tested where possible
- [ ] API references validated against current docs
- [ ] Version specificity checked (library versions, language versions)
- [ ] Deprecated practices identified
- [ ] Platform-specific details verified

## Completeness Validation

- [ ] Core concepts covered
- [ ] Important caveats included
- [ ] Edge cases addressed
- [ ] Common pitfalls documented
- [ ] Limitations acknowledged

## Error Detection

- [ ] No obvious factual errors
- [ ] No contradictions within findings
- [ ] No outdated practices recommended
- [ ] No broken logical reasoning
- [ ] No missing critical context

## Confidence Rating

- [ ] Overall confidence level assigned
- [ ] High confidence findings clearly marked
- [ ] Low confidence findings flagged for review
- [ ] Unverified claims clearly labeled
- [ ] Recommendations matched to confidence level

## User Notification

- [ ] User informed of accuracy assessment
- [ ] Limitations clearly communicated
- [ ] Follow-up recommendations provided where needed
- [ ] Manual verification suggested for critical findings
```

---

## Enhanced Data/Knowledge Base Specifications

### Data: research-tools-catalog.md

**Purpose:** Reference guide for MCP research tools with capabilities and optimization patterns

**Content Outline:**

````markdown
# Research Tools Catalog

Comprehensive reference for MCP research tools available in the ecosystem.

## Perplexity MCP Server

**MCP ID:** `mcp__perplexity__*`

### Available Tools

#### mcp**perplexity**search

- **Capability:** Quick factual search
- **Model:** Sonar Pro
- **Response Time:** 2-5 seconds
- **Optimal Use Cases:**
  - Simple factual queries
  - Current events
  - Quick concept definitions
  - Fact checking
- **Query Optimization:**
  - Keep concise (< 200 chars)
  - Use specific keywords
  - Avoid complex questions
  - Example: "React hooks closure issues" ✓
  - Example: "How do I prevent closure issues in React hooks?" ✗
- **Limitations:**
  - No multi-step reasoning
  - Limited depth
  - May not cover niche topics

#### mcp**perplexity**reason

- **Capability:** Complex multi-step reasoning
- **Model:** Sonar Reasoning Pro
- **Response Time:** 10-30 seconds
- **Optimal Use Cases:**
  - Analytical questions
  - Comparison tasks
  - Trade-off analysis
  - Problem solving
- **Query Optimization:**
  - Frame as analytical questions
  - Provide context
  - Specify desired reasoning depth
  - Example: "Compare useState vs useReducer for complex state management, analyzing trade-offs in maintainability, performance, and testability"
- **Limitations:**
  - Slower than quick search
  - Rate limits may apply

#### mcp**perplexity**deep_research

- **Capability:** Comprehensive research
- **Model:** Sonar Deep Research
- **Response Time:** 30-90 seconds
- **Optimal Use Cases:**
  - Multi-faceted topics
  - Comprehensive analysis
  - Literature review
  - State-of-the-art surveys
- **Query Optimization:**
  - Use natural language questions
  - Include scope and depth requirements
  - Provide context
  - Example: "Provide a comprehensive analysis of GraphQL schema design patterns, including historical evolution, current best practices, performance considerations, and emerging trends"
- **Limitations:**
  - Slowest option
  - May hit rate limits
  - Expensive token usage

### Installation

```bash
npm install -g perplexity-mcp
```
````

### Configuration

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "perplexity-mcp",
      "env": {
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
      }
    }
  }
}
```

---

## WebSearch MCP Server

**MCP ID:** `mcp__web_search__*`

### Available Tools

#### mcp**web_search**search

- **Capability:** General web search
- **Response Time:** 3-8 seconds
- **Optimal Use Cases:**
  - Broad web searches
  - Finding specific resources
  - Discovering community content
  - Blog posts and tutorials
- **Query Optimization:**
  - Use SEO-friendly keywords
  - Include site: operators when appropriate
  - Use quotes for exact phrases
  - Example: "React hooks tutorial site:react.dev"
- **Limitations:**
  - No synthesis or analysis
  - Raw search results only
  - Quality varies

### Installation

```bash
npm install -g web-search-mcp
```

---

## Context7 MCP Server

**MCP ID:** `mcp__context7__*`

### Available Tools

#### mcp**context7**resolve-library-id

- **Capability:** Find library in Context7 database
- **Response Time:** 1-2 seconds
- **Usage:** First step before fetching docs

#### mcp**context7**get-library-docs

- **Capability:** Fetch official library documentation
- **Response Time:** 2-5 seconds
- **Optimal Use Cases:**
  - Official API documentation
  - Framework reference
  - Technical specifications
  - Code examples
- **Query Optimization:**
  - Specify library name and version
  - Focus on specific APIs or concepts
  - Example: Library: "react", Version: "18", Topic: "hooks"
- **Limitations:**
  - Limited to libraries in Context7 database
  - May not have latest versions
  - Documentation quality varies by library

### Installation

Typically included with Claude Code, Cursor, or Windsurf.

---

## Tool Comparison Matrix

| Tool                     | Speed           | Depth  | Synthesis | Current Info | Technical Docs | Cost   |
| ------------------------ | --------------- | ------ | --------- | ------------ | -------------- | ------ |
| Perplexity Search        | Fast (2-5s)     | Low    | No        | Yes          | No             | Low    |
| Perplexity Reason        | Medium (10-30s) | Medium | Yes       | Yes          | No             | Medium |
| Perplexity Deep Research | Slow (30-90s)   | High   | Yes       | Yes          | No             | High   |
| WebSearch                | Fast (3-8s)     | N/A    | No        | Yes          | No             | Low    |
| Context7                 | Fast (2-5s)     | High   | No        | N/A          | Yes            | Low    |

---

## Recommended Tool Combinations

### Minimal (Free Tier)

- Context7 (usually included)
- Manual research workflows

### Standard (Perplexity Only)

- Perplexity Search for quick queries
- Perplexity Deep Research for comprehensive topics
- Context7 for technical docs
- Fallback: Manual research for gaps

### Comprehensive (All Tools)

- Perplexity Search for quick facts
- Perplexity Reason for analysis
- Perplexity Deep Research for comprehensive research
- Context7 for official docs
- WebSearch for broader coverage
- Optimal coverage across all research needs

````

---

### Data: query-optimization-patterns.md

**Purpose:** Tool-specific query templates and optimization strategies

**Content Outline:**

```markdown
# Query Optimization Patterns

Tool-specific patterns for optimizing research queries.

## Perplexity Search Optimization

### Pattern: Factual Query
**Format:** `[Concept] [Context] [Specific Aspect]`

**Examples:**
- ✓ "React useState closure issues causes"
- ✓ "GraphQL N+1 query problem solutions"
- ✓ "TypeScript discriminated unions type narrowing"
- ✗ "Why do I get closure issues with useState?" (too conversational)
- ✗ "Help me understand TypeScript" (too vague)

### Pattern: Definition Query
**Format:** `[Term] definition [context]`

**Examples:**
- ✓ "Temporal dead zone JavaScript definition"
- ✓ "Referential transparency functional programming"
- ✓ "Semantic versioning SemVer explanation"

### Pattern: Comparison Query
**Format:** `[A] vs [B] [specific aspect]`

**Examples:**
- ✓ "useState vs useReducer performance"
- ✓ "REST vs GraphQL caching strategies"
- ✓ "Flexbox vs Grid layout use cases"

---

## Perplexity Deep Research Optimization

### Pattern: Comprehensive Analysis
**Format:** Natural language question with scope and depth specified

**Template:**
````

Provide a comprehensive analysis of [topic], including:

- [aspect 1]
- [aspect 2]
- [aspect 3]
- [desired insights]

```

**Examples:**
```

Provide a comprehensive analysis of React Hooks, including:

- Historical context and motivation for introduction
- Core hooks and their use cases
- Rules of hooks and technical rationale
- Common pitfalls and how to avoid them
- Performance implications
- Migration strategies from class components

```

### Pattern: Evolution/Trend Analysis
**Template:**
```

How has [topic] evolved from [time period/version/context]? Include historical developments, current state, and future trends.

```

**Examples:**
```

How has state management in React evolved from 2015 to 2025? Include the progression from setState → Redux → Context → Hooks → Zustand/Jotai, analyzing the motivations for each shift and current best practices.

```

### Pattern: Trade-off Analysis
**Template:**
```

Analyze the trade-offs between [approach A] and [approach B] for [use case], considering [criteria 1], [criteria 2], and [criteria 3].

```

**Examples:**
```

Analyze the trade-offs between REST and GraphQL APIs for e-commerce platforms, considering performance, caching, development velocity, and operational complexity.

```

---

## Perplexity Reasoning Optimization

### Pattern: Multi-Step Reasoning
**Template:**
```

[Question requiring logical steps]
Consider: [constraint 1], [constraint 2], [constraint 3]

```

**Examples:**
```

Should a SaaS application use REST or GraphQL for its public API?
Consider: third-party integration needs, caching requirements, mobile client performance, and developer ecosystem maturity.

```

### Pattern: Comparative Analysis
**Template:**
```

Compare [A], [B], and [C] for [use case], ranking by [criterion 1], [criterion 2], and [criterion 3]. Provide reasoning for rankings.

```

**Examples:**
```

Compare useState, useReducer, and Zustand for managing complex form state with validation, ranking by testability, maintainability, and performance. Provide reasoning for each ranking.

```

---

## Context7 Optimization

### Pattern: API Documentation Query
**Format:** Structured parameters

**Template:**
```

Library: [library-name]
Version: [version] (optional)
Topic: [specific-api-or-concept]

```

**Examples:**
```

Library: react
Version: 18
Topic: useState hook API

```

```

Library: next.js
Topic: server-side rendering

```

### Pattern: Code Example Query
**Template:**
```

Library: [library-name]
Topic: [feature] code examples

```

**Examples:**
```

Library: prisma
Topic: transaction examples

```

---

## WebSearch Optimization

### Pattern: SEO-Optimized Query
**Format:** Keywords + modifiers

**Examples:**
- ✓ "React hooks best practices 2025"
- ✓ "GraphQL schema design patterns tutorial"
- ✓ "TypeScript advanced types guide"

### Pattern: Site-Specific Search
**Format:** `[keywords] site:[domain]`

**Examples:**
- "Next.js middleware site:nextjs.org"
- "React Server Components site:react.dev"
- "Prisma migrations site:prisma.io"

### Pattern: File Type Search
**Format:** `[keywords] filetype:[extension]`

**Examples:**
- "React architecture filetype:pdf"
- "GraphQL schema filetype:md"

---

## Anti-Patterns (Avoid These)

### Anti-Pattern: Overly Conversational
- ✗ "Can you help me understand how React hooks work?"
- ✓ "React hooks comprehensive guide"

### Anti-Pattern: Too Vague
- ✗ "Tell me about JavaScript"
- ✓ "JavaScript closures and scope chain explanation"

### Anti-Pattern: Wrong Tool
- ✗ Using Perplexity Search for comprehensive research (use Deep Research)
- ✗ Using Perplexity Deep Research for simple definitions (use Search)
- ✗ Using WebSearch for official docs (use Context7)

### Anti-Pattern: Missing Context
- ✗ "useState issues"
- ✓ "React useState closure issues causes solutions"

---

## Query Optimization Workflow

1. **Analyze Query Intent:**
   - Factual → Quick search tool
   - Analytical → Reasoning tool
   - Comprehensive → Deep research tool
   - Documentation → Context7
   - Broad → WebSearch

2. **Apply Tool-Specific Pattern:**
   - Match query to pattern template
   - Apply formatting rules
   - Add necessary context

3. **Validate Optimization:**
   - Check against anti-patterns
   - Ensure tool capability match
   - Verify query clarity

4. **Execute & Refine:**
   - Run optimized query
   - Assess result quality
   - Refine if needed
```

---

### Data: credibility-scoring-rubric.md

**Purpose:** Evidence-based framework for assessing source credibility

**Content Outline:**

```markdown
# Source Credibility Scoring Rubric

Framework for evaluating research source authority and reliability.

## Scoring Overview

**Score Range:** 0-100
**Categories:**

- **Authoritative (85-100):** Highest quality, primary sources
- **Reliable (70-84):** Trustworthy, secondary sources
- **Questionable (50-69):** Use with caution, verify claims
- **Unreliable (0-49):** Avoid or flag prominently

## Scoring Criteria

### 1. Authority (Weight: 35%)

**Authoritative Sources (30-35 points):**

- Official documentation (react.dev, MDN, RFCs, W3C specs)
- Peer-reviewed academic papers
- Books from established technical publishers (O'Reilly, Manning, Packt)
- Primary source materials (language specifications, standards documents)

**Reliable Sources (20-29 points):**

- Reputable tech blogs (CSS-Tricks, Smashing Magazine, freeCodeCamp)
- Industry expert personal blogs (Dan Abramov, Kent C. Dodds, etc.)
- Conference talks by recognized experts (React Conf, JSConf, etc.)
- Major tech company engineering blogs (Netflix, Uber, Spotify)
- Well-maintained open source documentation

**Questionable Sources (10-19 points):**

- Tutorial sites with unknown authors
- Community forums (Stack Overflow, Reddit, Dev.to)
- Medium articles by unverified authors
- Marketing content with clear bias
- AI-generated content without human verification

**Unreliable Sources (0-9 points):**

- Content farms, low-quality SEO sites
- Anonymous sources with no credentials
- Sites with known misinformation history
- Aggregator sites without original content
- Paraphrased content without attribution

### 2. Currency (Weight: 25%)

**Current (20-25 points):**

- Published within last 12 months
- Explicitly updated for current versions
- Reflects current best practices
- References recent developments

**Recent (15-19 points):**

- Published 1-3 years ago
- Core concepts still valid
- Some practices may be outdated
- Technology still in active use

**Dated (8-14 points):**

- Published 3-5 years ago
- Technology has evolved significantly
- May contain deprecated practices
- Requires validation against current docs

**Outdated (0-7 points):**

- Published >5 years ago for fast-moving tech
- Technology significantly changed or deprecated
- Contains obsolete practices
- Historical value only

**Note:** Adjust timeframes based on technology evolution speed:

- **Fast-moving:** JavaScript frameworks, cloud services (use timeframes above)
- **Moderate:** Programming languages, databases (double timeframes)
- **Stable:** Algorithms, design patterns, computer science fundamentals (currency less critical)

### 3. Accuracy & Evidence (Weight: 20%)

**Well-Sourced (16-20 points):**

- Claims backed by citations
- References to authoritative sources
- Code examples tested and verified
- Technical details accurate
- Peer-reviewed or fact-checked

**Partially-Sourced (10-15 points):**

- Some claims cited
- Mix of sourced and unsourced content
- Code examples may be incomplete
- Technical accuracy mostly good
- Some verification gaps

**Unsourced (5-9 points):**

- Few or no citations
- Claims without evidence
- Code examples untested or incomplete
- Technical accuracy questionable
- Relies on author authority only

**Inaccurate (0-4 points):**

- Contains factual errors
- Code examples don't work
- Contradicts authoritative sources
- Misleading or incorrect claims

### 4. Objectivity (Weight: 10%)

**Objective (8-10 points):**

- Balanced perspective
- Acknowledges trade-offs
- Presents multiple viewpoints
- No commercial bias
- Separates facts from opinions

**Somewhat Biased (5-7 points):**

- Slight commercial bias (sponsored content disclosed)
- Favors one approach but mentions alternatives
- Personal opinions clearly labeled
- Trade-offs partially addressed

**Highly Biased (0-4 points):**

- Strong commercial bias (vendor marketing)
- One-sided perspective
- Opinions presented as facts
- Trade-offs ignored
- Lacks balance

### 5. Coverage & Depth (Weight: 10%)

**Comprehensive (8-10 points):**

- Topic covered in depth
- Edge cases addressed
- Limitations discussed
- Context provided
- Complete explanations

**Moderate (5-7 points):**

- Core concepts covered
- Some edge cases mentioned
- Adequate depth
- Sufficient context

**Superficial (0-4 points):**

- Surface-level treatment
- Important aspects missing
- Insufficient context
- Incomplete explanations

## Scoring Examples

### Example 1: Official React Documentation (react.dev)

- **Authority:** 35/35 (official docs)
- **Currency:** 25/25 (continuously updated)
- **Accuracy:** 20/20 (authoritative source)
- **Objectivity:** 10/10 (balanced, educational)
- **Coverage:** 10/10 (comprehensive)
- **Total:** 100/100 → **Authoritative**

### Example 2: Kent C. Dodds Blog Post on Testing

- **Authority:** 28/35 (recognized expert)
- **Currency:** 23/25 (published 8 months ago)
- **Accuracy:** 18/20 (well-sourced, tested examples)
- **Objectivity:** 9/10 (slight bias toward Testing Library)
- **Coverage:** 9/10 (very comprehensive)
- **Total:** 87/100 → **Authoritative**

### Example 3: Medium Article by Unknown Author

- **Authority:** 15/35 (unknown author, Medium)
- **Currency:** 20/25 (recent, 6 months ago)
- **Accuracy:** 12/20 (partially sourced, examples incomplete)
- **Objectivity:** 6/10 (personal opinions as facts)
- **Coverage:** 6/10 (moderate depth)
- **Total:** 59/100 → **Questionable**

### Example 4: Stack Overflow Answer

- **Authority:** 18/35 (community platform, high reputation user)
- **Currency:** 18/25 (2 years old)
- **Accuracy:** 16/20 (code works, tested by community votes)
- **Objectivity:** 8/10 (fairly objective)
- **Coverage:** 5/10 (answers specific question only)
- **Total:** 65/100 → **Questionable** (but useful for specific problems)

### Example 5: Content Farm SEO Article

- **Authority:** 5/35 (unknown author, low-quality site)
- **Currency:** 10/25 (dated, 4 years old)
- **Accuracy:** 6/20 (unsourced, examples don't work)
- **Objectivity:** 3/10 (highly biased, affiliate links)
- **Coverage:** 4/10 (superficial)
- **Total:** 28/100 → **Unreliable**

## Usage Guidelines

### Scoring Workflow

1. Identify source type (docs, blog, forum, etc.)
2. Score each criterion independently
3. Apply weights to calculate total
4. Assign category (Authoritative/Reliable/Questionable/Unreliable)
5. Document reasoning

### Integration Recommendations

**Authoritative Sources (85-100):**

- ✓ Use without additional verification
- ✓ Prefer for key claims
- ✓ Cite as primary sources

**Reliable Sources (70-84):**

- ✓ Use with confidence
- ✓ Cross-reference for critical claims
- ✓ Good for secondary evidence

**Questionable Sources (50-69):**

- ⚠ Use with caution
- ⚠ Verify claims with better sources
- ⚠ Flag as "needs verification"
- ⚠ Useful for discovering topics, not as primary evidence

**Unreliable Sources (0-49):**

- ✗ Avoid in final research output
- ✗ Do not cite as evidence
- ✗ May use for topic discovery only
- ✗ Flag prominently if must include

### Special Considerations

**Community Content (Stack Overflow, Reddit):**

- High vote count / reputation → increase authority score
- Accepted answer → increase accuracy score
- Recent activity → increase currency score
- Use for specific problems, not general guidance

**Academic Papers:**

- Peer-reviewed → maximum authority
- Conference papers → high authority
- ArXiv preprints → moderate authority (not peer-reviewed)
- Check citation count for impact

**Personal Blogs:**

- Known expert → high authority
- Active in community → increase authority
- Transparent about opinions → increase objectivity
- Detailed explanations → increase coverage

**Company Blogs:**

- Engineering blogs → higher authority than marketing
- Case studies → valuable but potentially biased
- Disclosure of bias → increase objectivity
- Technical depth → increase coverage
```

---

## Implementation Roadmap (Updated)

The research enhancement integrates into the existing implementation roadmap:

### Phase 1: MVP (Enhanced)

**Duration:** 4-6 weeks

**Added to Phase 1:**

- **Research Coordinator Agent (Basic):**
  - Tool detection capability
  - Manual query generation
  - Research import workflow

- **Additional Tasks (3):**
  - `detect-research-tools.md`
  - `generate-research-queries.md`
  - `import-research-findings.md`

- **Additional Templates (2):**
  - `tool-detection-report-tmpl.yaml`
  - `research-query-set-tmpl.yaml`

- **Additional Data (1):**
  - `research-tools-catalog.md`

### Phase 5: Optional Research Integration (Enhanced)

**Duration:** 3-4 weeks

**Enhanced Deliverables:**

**1. Research Coordinator Agent (Full Enhancement):**

- Complete tool detection and profiling
- Automated research execution
- Multi-tool orchestration
- Source credibility assessment
- Result synthesis with conflict resolution
- Neo4j provenance tracking

**2. Research Tasks (16 additional):**

- Tool Detection: `profile-tool-capabilities.md`, `recommend-research-tools.md`
- Query Optimization: `generate-deep-questions.md`, `optimize-query-for-tool.md`, `categorize-queries.md`
- Execution: `execute-parallel-research.md`, `execute-sequential-research.md`, `execute-targeted-research.md`
- Source Evaluation: All 3 tasks
- Synthesis: All 3 tasks

**3. Research Templates (5 additional):**

- All templates specified in enhancement

**4. Research Checklists (3):**

- `tool-optimization-checklist.md`
- `research-synthesis-checklist.md`
- `research-accuracy-checklist.md`

**5. Research Knowledge Bases (5 additional):**

- `query-optimization-patterns.md`
- `research-strategy-patterns.md`
- `credibility-scoring-rubric.md`
- Plus 2 more from original spec

---

## Success Metrics (Research-Specific)

### Research Quality Metrics

- **Source Credibility:** Average credibility score ≥ 75 (Reliable+)
- **Accuracy:** >95% of claims verified across multiple sources
- **Conflict Resolution:** <5% unresolved contradictions
- **Coverage:** Completeness score ≥ 80/100

### Research Efficiency Metrics

- **Time Saved:** 50-70% reduction vs. manual research
- **Tool Utilization:** Detected tools used appropriately ≥ 90% of time
- **Query Optimization:** Optimized queries perform 20-30% better
- **Parallel Execution:** Parallelizable queries executed concurrently ≥ 80% of time

### Research Integration Metrics

- **Note Creation:** 80%+ of findings converted to atomic notes
- **Link Discovery:** 60%+ of research notes linked to existing knowledge
- **MOC Updates:** Relevant MOCs updated within 24 hours
- **Provenance Tracking:** 100% of research tracked in Neo4j

### User Satisfaction Metrics

- **Research Confidence:** Users confident in research quality ≥ 85% of time
- **Tool Recommendations:** Users install recommended tools ≥ 40% of time
- **Workflow Adoption:** Automated research used ≥ 60% of time vs. manual

---

## Conclusion

This enhancement transforms the Research Coordinator Agent from a basic optional component into a sophisticated adaptive research system that:

1. **Automatically adapts** to available tools
2. **Optimizes strategies** for maximum accuracy
3. **Provides fallbacks** when tools unavailable
4. **Ensures quality** through multi-source validation
5. **Tracks provenance** for research transparency

The enhancement maintains backward compatibility (manual research workflows still supported) while providing significant value when research tools are available. Users can adopt incrementally, starting with tool detection and manual query generation, then progressing to automated research as they gain confidence.

By making research adaptive and intelligent, this enhancement ensures users always get the most accurate, up-to-date information regardless of their tool configuration.

---

**End of Enhancement Specification**
