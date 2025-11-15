<!-- Powered by BMAD™ Core -->

# Create MOC Structure

## Purpose

Analyze domain coverage, create hierarchical structure (2-3 levels deep), and organize notes into knowledge branches for Map of Content generation.

## Inputs

- **domain** (String, required): Knowledge domain to analyze (e.g., "machine-learning", "zettelkasten")
- **vault_path** (String, required): Path to Obsidian vault
- **user_preferences** (Object, optional): Contains branching style, depth limit, min notes per branch

## Outputs

- **moc_structure** (Object): Hierarchical structure with branches, sub-branches, and assigned notes
- **coverage_report** (Object): Statistics on notes found, gaps identified, suggested additions

## Procedure

### Step 1: Discover Domain Notes

Identify all notes belonging to the domain using multiple discovery methods:

**Tag-based discovery:**
- Query Obsidian for notes with domain-related tags
- Search for exact domain tag (e.g., `#machine-learning`)
- Search for hyphenated variants (e.g., `#ml`, `#machinelearning`)
- Search for parent category tags (e.g., `#ai`, `#data-science`)

**Link-based discovery:**
- If existing MOC exists for domain, get all linked notes
- Traverse backlinks and outlinks from discovered notes (1 hop)
- Build note network graph

**Semantic similarity discovery:**
- Extract domain keywords (2-5 key terms)
- Use `query-semantic-similarity.md` task with similarity threshold > 0.75
- Present candidate notes to user for inclusion decision

**Manual inclusion:**
- Ask user: "Are there specific notes you want included that weren't discovered?"
- Add user-specified notes to domain set

### Step 2: Analyze Note Characteristics

For each discovered note, extract:

- **Building block type**: concept, argument, model, observation, process, question
- **Core topics**: Main subjects/keywords (from frontmatter tags or content analysis)
- **Link density**: Count of outgoing/incoming links
- **Creation date**: Temporal context
- **Content length**: Word count (helps assess maturity)

Build note metadata table for clustering:

```
note_metadata = [
  {
    path: "[[Note 1]]",
    type: "concept",
    topics: ["supervised-learning", "classification"],
    links: 5,
    created: "2024-03-10"
  },
  // ... more notes
]
```

### Step 3: Identify Knowledge Branches

Use semantic clustering to organize notes into 3-6 main branches:

**Clustering Algorithm:**

1. **Extract topic vectors** for all notes (based on tags, keywords, content)
2. **Calculate pairwise similarity** between all notes
3. **Cluster notes** using hierarchical clustering or k-means (k=3-6)
4. **Name each cluster** based on dominant topics within cluster

**Branching Patterns** (suggest to user based on domain):

- **By abstraction level**: Theory → Practice → Examples
- **By subdomain**: Algorithms → Tools → Applications
- **By workflow stage**: Capture → Process → Synthesize
- **By time period**: Historical → Current → Emerging
- **By complexity**: Fundamentals → Intermediate → Advanced

**User interaction:**
Present suggested branches as numbered list:

```
Suggested Knowledge Branches for "machine-learning":

1. Fundamentals & Theory (12 notes)
   - Covers: supervised/unsupervised learning, loss functions, optimization
2. Algorithms & Models (18 notes)
   - Covers: neural networks, decision trees, SVMs, ensemble methods
3. Tools & Frameworks (8 notes)
   - Covers: TensorFlow, PyTorch, scikit-learn
4. Applications & Case Studies (6 notes)
   - Covers: computer vision, NLP, recommender systems

Does this organization make sense? Type 'y' to accept, or suggest changes:
```

Elicit user confirmation or refinement of branch names/structure.

### Step 4: Organize Notes into Hierarchical Structure

**For each branch:**

1. **Assign notes to branch** based on clustering
   - Note can appear in multiple branches if relevant
   - Minimum 3 notes per branch (merge if fewer)
   - Maximum 15 notes per branch (split into sub-branches if more)

2. **Create sub-branches if needed** (level 3):
   - If branch has > 15 notes, cluster into 2-3 sub-branches
   - Name sub-branches by sub-topic
   - Keep sub-branch size to 4-12 notes

3. **Order notes within branch**:
   - Sort by logical progression (fundamentals first, advanced last)
   - Or sort by link density (hub notes first)
   - Or sort alphabetically if no clear ordering

### Step 5: Identify Core Concepts

Extract 5-10 foundational concepts that define the domain:

**Core Concept Criteria:**
- Frequently referenced (high link density)
- Fundamental to domain understanding (appears in multiple branches)
- Well-defined (concept building block type)
- Prerequisite for other concepts

**Extraction Method:**
- Filter notes for `type: concept` building blocks
- Calculate PageRank or betweenness centrality in link graph
- Rank by centrality score
- Select top 5-10 as core concepts

### Step 6: Generate Structure Output

Build hierarchical MOC structure object:

```yaml
moc_structure:
  domain: "machine-learning"
  created: "2024-11-11"
  note_count: 44

  core_concepts:
    - "[[Supervised Learning]]"
    - "[[Loss Functions]]"
    - "[[Gradient Descent]]"
    - "[[Overfitting]]"
    - "[[Feature Engineering]]"

  branches:
    - name: "Fundamentals & Theory"
      summary_placeholder: "[To be generated in generate-summaries task]"
      notes:
        - path: "[[Supervised Learning]]"
          context: "Foundation of ML classification/regression"
        - path: "[[Unsupervised Learning]]"
          context: "Clustering and dimensionality reduction"
        # ... more notes

    - name: "Algorithms & Models"
      summary_placeholder: "[To be generated]"
      sub_branches:
        - name: "Neural Networks"
          notes:
            - path: "[[Perceptron]]"
              context: "Simplest neural unit"
            # ... more notes
        - name: "Tree-Based Methods"
          notes:
            - path: "[[Decision Trees]]"
              context: "Interpretable classification"
            # ... more notes

    # ... more branches

  emerging_questions:
    - "How do transformers compare to CNNs for computer vision tasks?"
    - "What are the ethical implications of bias in training data?"

  coverage_report:
    notes_discovered: 44
    tag_based: 32
    link_based: 8
    semantic_based: 4
    gaps_identified:
      - "Reinforcement learning concepts (< 2 notes found)"
      - "Model interpretability techniques (no notes found)"
```

### Step 7: Validate Structure Quality

**Quality Checks:**

- ✅ **Branch count appropriate**: 3-6 branches (not too few, not too many)
- ✅ **Branch balance**: No single branch has > 50% of notes
- ✅ **Minimum coverage**: Each branch has ≥ 3 notes
- ✅ **No orphans**: Every discovered note assigned to at least one branch
- ✅ **Core concepts identified**: 5-10 foundational concepts extracted
- ✅ **Emerging questions present**: At least 2 questions listed
- ✅ **Hierarchical depth appropriate**: Maximum 3 levels (domain → branch → sub-branch)

If validation fails, refine structure and re-validate.

### Step 8: Generate Coverage Report

Analyze domain coverage completeness:

**Gap Identification:**
- Compare discovered notes to expected domain coverage
- Identify underrepresented topics (e.g., "only 1 note on reinforcement learning")
- Suggest capture targets

**Report Format:**

```markdown
## Domain Coverage Report: Machine Learning

**Notes Discovered:** 44 total
- Tag-based: 32 notes
- Link-based: 8 notes
- Semantic similarity: 4 notes

**Coverage Analysis:**
- ✅ Supervised learning: Well-covered (18 notes)
- ✅ Neural networks: Well-covered (12 notes)
- ⚠️  Unsupervised learning: Moderate coverage (6 notes)
- ⚠️  Reinforcement learning: Under-covered (2 notes)
- ❌ Model interpretability: Gap identified (0 notes)
- ❌ Ethical AI considerations: Gap identified (1 note)

**Recommended Next Captures:**
1. Reinforcement learning fundamentals (Q-learning, policy gradients)
2. Model interpretability techniques (SHAP, LIME, attention visualization)
3. Bias detection and mitigation in ML models

**Domain Maturity:** Developing (nascent in some areas, established in others)
```

### Step 9: Elicit User Approval

Present structure and coverage report to user:

```
MOC Structure Generated for "machine-learning"

Core Concepts: 5 identified
Knowledge Branches: 4 main branches
Note Coverage: 44 notes organized
Gaps Identified: 3 areas need attention

[Display structure summary]

Options:
1. Approve structure (proceed to summary generation)
2. Refine branch names
3. Reorganize note assignments
4. Add/remove notes from domain

Enter choice (1-4):
```

Wait for user input before proceeding.

## Integration Notes

**Obsidian MCP Tools Integration:**
- Use `obsidian.search` to query tags
- Use `obsidian.getBacklinks` / `obsidian.getOutlinks` for link discovery
- Use `obsidian.readNote` to analyze note content

**Neo4j Graphiti Integration (if available):**
- Query note relationships for link-based discovery
- Use graph algorithms (PageRank, centrality) for core concept identification
- Graceful degradation: If Neo4j unavailable, use Obsidian link counts only

**Smart Connections Plugin Integration (if available):**
- Use semantic similarity API for discovery
- If unavailable, skip semantic discovery step

## Error Handling

**No notes found in domain:**
- Error: "No notes found for domain '{domain}'. Check tag spelling or expand search criteria."
- Suggest: Try broader tags, check vault path

**Too few notes (< 10):**
- Warning: "Only {count} notes found. MOC creation works best with 10+ notes."
- Offer: Proceed with nascent MOC, or capture more content first?

**Clustering fails:**
- Fallback: Organize alphabetically or by creation date
- Notify user: "Auto-clustering unavailable, using fallback organization"

**User rejects structure:**
- Return to Step 3, allow manual branch definition
- Support iteration until user approves

## Testing

**Test Case 1: Small Domain (10-15 notes)**
- Expected: 2-3 branches, flat structure (no sub-branches)
- Validate: All notes assigned, no orphans

**Test Case 2: Medium Domain (30-50 notes)**
- Expected: 3-5 branches, possible sub-branches for larger branches
- Validate: Balanced distribution, core concepts identified

**Test Case 3: Large Domain (60+ notes)**
- Expected: 4-6 branches, hierarchical structure with sub-branches
- Validate: No branch with > 15 notes at leaf level

**Test Case 4: Neo4j Unavailable**
- Expected: Graceful degradation (skip graph algorithms)
- Validate: Structure still generated using tag/link discovery only
