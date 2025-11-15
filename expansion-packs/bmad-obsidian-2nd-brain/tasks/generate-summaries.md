<!-- Powered by BMAD™ Core -->

# Generate Summaries

## Purpose

Read constituent notes within MOC branches and generate synthesized 2-3 sentence summaries that explain the branch's theme, relationships, and significance to the domain.

## Inputs

- **moc_structure** (Object, required): Hierarchical structure from `create-moc-structure.md` task
- **vault_path** (String, required): Path to Obsidian vault
- **summary_style** (String, optional): "explanatory" (default), "descriptive", or "narrative"

## Outputs

- **enriched_moc_structure** (Object): MOC structure with summaries added to all branches and sub-branches
- **core_concept_definitions** (Array): Brief 1-sentence definitions for each core concept

## Procedure

### Step 1: Validate Input Structure

- Check that `moc_structure` contains branches with assigned notes
- Verify each branch has at least 3 notes (if fewer, warn but proceed)
- Confirm vault_path is accessible
- If validation fails, return error with details

### Step 2: Read Constituent Notes

For each branch/sub-branch in the structure:

**Read note content:**
- Use Obsidian MCP `obsidian.readNote` for each note in branch
- Extract key information:
  - Title
  - Building block type (from frontmatter: concept, argument, model, etc.)
  - Core topics/tags
  - First paragraph (often contains key idea)
  - Key claims or definitions (if concept/argument type)

**Build branch content summary:**

```
branch_notes_content = {
  branch_name: "Fundamentals & Theory",
  notes: [
    {
      path: "[[Supervised Learning]]",
      type: "concept",
      key_idea: "Learning from labeled examples to predict outcomes",
      topics: ["classification", "regression"]
    },
    {
      path: "[[Loss Functions]]",
      type: "concept",
      key_idea: "Measure prediction error to guide optimization",
      topics: ["optimization", "training"]
    },
    // ... more notes
  ]
}
```

### Step 3: Identify Branch Theme

Analyze the collection of notes to identify unifying theme:

**Theme Identification Algorithm:**

1. **Extract common topics**: Find topics that appear in 50%+ of notes in branch
2. **Identify relationships**: How do these notes connect to each other?
   - Sequential relationship (A → B → C)
   - Hierarchical relationship (general → specific)
   - Complementary relationship (different perspectives on same domain)
3. **Determine abstraction level**: Are these theoretical, practical, or applied notes?
4. **Assess scope**: What aspect of the domain does this branch cover?

**Example Theme Identification:**

```
Branch: "Fundamentals & Theory"
Notes: 12 concept-type notes covering learning paradigms, optimization, evaluation

Common Topics: ["learning", "optimization", "theory"]
Relationship: Hierarchical (learning paradigms → optimization methods → evaluation metrics)
Abstraction: Theoretical
Scope: Foundational concepts underlying all ML approaches

Theme: "Core theoretical foundations of machine learning"
```

### Step 4: Generate Section Summary (2-3 sentences)

Write synthesized summary following this structure:

**Sentence 1: What this branch covers (theme statement)**
- Start with the branch's focus
- Use active, declarative language
- Avoid "This section contains..." (too generic)

**Sentence 2: Key insight or relationship**
- Explain the significance of these concepts together
- Show how they connect or build on each other
- Highlight the "why this matters" aspect

**Sentence 3: Connection to broader domain (optional but recommended)**
- Relate branch to overall domain
- Explain prerequisite relationships or downstream applications
- Position this branch in the knowledge landscape

### Step 5: Apply Summary Style

**Explanatory Style (default):**
Focus on relationships and significance

Example:
> "This branch explores the fundamental learning paradigms in machine learning, from supervised to unsupervised approaches. Each paradigm defines how models learn from data—whether through labeled examples, pattern discovery, or reward signals—shaping the choice of algorithms and evaluation methods. Understanding these paradigms is prerequisite to selecting appropriate techniques for specific problems."

**Descriptive Style:**
Focus on content inventory and characteristics

Example:
> "This branch contains 12 concept notes covering core theoretical foundations. Topics include supervised learning, unsupervised learning, loss functions, gradient descent, and overfitting. These concepts form the mathematical and algorithmic basis of modern machine learning systems."

**Narrative Style:**
Focus on learning journey and evolution

Example:
> "Machine learning begins with understanding how models learn from data. This branch traces that foundation, starting with supervised learning's labeled examples, expanding to unsupervised pattern discovery, and culminating in the optimization techniques that make learning possible. These are the building blocks every ML practitioner must master."

### Step 6: Generate Core Concept Definitions

For each core concept listed in `moc_structure.core_concepts`:

**Read the concept note:**
- Extract title and first 1-2 sentences
- Identify the definition statement (often follows "is defined as", "refers to", "means")

**Generate 1-sentence definition:**
- Format: "[Concept] is [definition]"
- Keep to 10-20 words
- Avoid jargon unless necessary
- Focus on clarity over completeness

**Example Definitions:**

```yaml
core_concepts:
  - name: "[[Supervised Learning]]"
    definition: "A learning paradigm where models learn from labeled examples to predict outcomes for new data."

  - name: "[[Loss Functions]]"
    definition: "Mathematical functions that quantify prediction error, guiding model optimization during training."

  - name: "[[Gradient Descent]]"
    definition: "An iterative optimization algorithm that minimizes loss by adjusting parameters in the direction of steepest descent."
```

### Step 7: Quality Check Summaries

**Summary Quality Criteria:**

- ✅ **Synthesis over enumeration**: Explains relationships, not just lists notes
- ✅ **Concise**: 2-3 sentences (50-80 words)
- ✅ **Active voice**: "This branch explores..." not "Notes in this section are about..."
- ✅ **Insight present**: Conveys "why this matters", not just "what is here"
- ✅ **Context provided**: Relates branch to broader domain
- ✅ **Accessible**: Understandable without reading all constituent notes
- ✅ **No orphan phrases**: Every sentence adds value

**Bad Example (too generic):**
> "This section contains notes about machine learning algorithms. There are notes on neural networks, decision trees, and SVMs. These are important for machine learning."

**Good Example (synthesized):**
> "This branch examines the core algorithms that power machine learning systems, from interpretable decision trees to complex neural architectures. Each algorithm represents a different trade-off between accuracy, interpretability, and computational cost, making algorithm selection a critical modeling decision. Understanding these trade-offs enables choosing the right tool for each problem domain."

If summary fails quality check, regenerate following the 3-sentence structure more carefully.

### Step 8: Handle Sub-Branches

For branches with sub-branches (hierarchical structure):

1. **Generate sub-branch summaries first** (bottom-up approach)
2. **Generate parent branch summary** that synthesizes across sub-branches

**Example Hierarchical Summary:**

```yaml
branches:
  - name: "Algorithms & Models"
    summary: "This branch surveys the algorithmic landscape of machine learning, organized by approach and architecture. From neural networks' layered representations to tree-based methods' interpretable decisions, each algorithm family offers distinct advantages. Selecting the right algorithm requires understanding these trade-offs and matching them to problem constraints."

    sub_branches:
      - name: "Neural Networks"
        summary: "Neural networks learn hierarchical representations through layers of interconnected neurons. From simple perceptrons to deep architectures like CNNs and transformers, depth and structure determine what patterns can be learned. These models excel at high-dimensional data but require substantial data and computation."

      - name: "Tree-Based Methods"
        summary: "Decision trees and ensemble methods (Random Forests, XGBoost) provide interpretable alternatives to neural networks. By recursively partitioning feature space, these models reveal which features drive predictions. Their transparency and robustness make them popular for tabular data and regulated domains."
```

### Step 9: Enrich MOC Structure

Add generated summaries to the MOC structure object:

```yaml
moc_structure:
  domain: "machine-learning"
  created: "2024-11-11"
  note_count: 44

  core_concepts:
    - name: "[[Supervised Learning]]"
      definition: "A learning paradigm where models learn from labeled examples to predict outcomes for new data."
    - name: "[[Loss Functions]]"
      definition: "Mathematical functions that quantify prediction error, guiding model optimization during training."
    # ... more concepts

  branches:
    - name: "Fundamentals & Theory"
      summary: "This branch explores the fundamental learning paradigms in machine learning, from supervised to unsupervised approaches. Each paradigm defines how models learn from data—whether through labeled examples, pattern discovery, or reward signals—shaping the choice of algorithms and evaluation methods. Understanding these paradigms is prerequisite to selecting appropriate techniques for specific problems."
      notes:
        - path: "[[Supervised Learning]]"
          context: "Foundation of ML classification/regression"
        # ... more notes
    # ... more branches
```

### Step 10: Generate Summary Report

Create a summary generation report for user review:

```markdown
## Summary Generation Report

**Domain**: machine-learning
**Branches Processed**: 4 main branches, 3 sub-branches
**Core Concepts Defined**: 5 concepts

### Generated Summaries

#### Branch: Fundamentals & Theory (12 notes)
✅ Summary: "This branch explores the fundamental learning paradigms..."
Quality: Pass (synthesis present, context provided, concise)

#### Branch: Algorithms & Models (18 notes)
  #### Sub-branch: Neural Networks (10 notes)
  ✅ Summary: "Neural networks learn hierarchical representations..."
  Quality: Pass

  #### Sub-branch: Tree-Based Methods (8 notes)
  ✅ Summary: "Decision trees and ensemble methods..."
  Quality: Pass

✅ Parent summary: "This branch surveys the algorithmic landscape..."
Quality: Pass

[... more branches]

### Core Concept Definitions

1. [[Supervised Learning]]: "A learning paradigm where models learn from labeled examples..."
2. [[Loss Functions]]: "Mathematical functions that quantify prediction error..."
[... more definitions]

**Review**: All summaries pass quality criteria. Ready to proceed to bridge paragraph generation.
```

### Step 11: Elicit User Feedback

Present summaries to user for approval:

```
Summary Generation Complete

4 branch summaries generated
3 sub-branch summaries generated
5 core concepts defined

Options:
1. Approve all summaries (proceed to bridge paragraphs)
2. Regenerate specific branch summary (which branch?)
3. Edit summary manually (which branch?)
4. Change summary style (current: explanatory)

Enter choice (1-4):
```

Wait for user input. If user requests regeneration, repeat Step 4-7 for specified branch.

## Integration Notes

**Obsidian MCP Tools:**
- Use `obsidian.readNote` to fetch note content
- Use `obsidian.getProperties` to extract frontmatter (building block type, tags)

**AI Content Generation:**
- Use LLM to generate summaries with prompt:
  ```
  Given these notes in the "{branch_name}" branch of a machine learning MOC:
  [list of note titles and key ideas]

  Generate a 2-3 sentence summary that:
  1. Explains the unifying theme
  2. Highlights key relationships or insights
  3. Connects to the broader machine learning domain

  Use explanatory style (focus on "why this matters").
  ```

## Error Handling

**Note not found:**
- Warning: "Note [[X]] listed in structure but not found in vault"
- Skip note, proceed with remaining notes
- Flag in report: "Summary generated with {count} of {total} notes (some missing)"

**Empty note content:**
- Warning: "Note [[X]] has no content to summarize"
- Use title and tags only
- Proceed with limited information

**Summary generation fails:**
- Retry with simplified prompt
- If retry fails, generate placeholder: "[Summary pending - manual input required]"
- Flag for user attention in report

**User rejects summary:**
- Allow manual editing via text input
- Or trigger regeneration with different style
- Support iteration until approved

## Testing

**Test Case 1: Small Branch (3-5 notes)**
- Expected: Concise summary covering all notes
- Validate: All note key ideas represented

**Test Case 2: Large Branch (15+ notes)**
- Expected: High-level synthesis, not exhaustive enumeration
- Validate: Summary focuses on theme, not listing all notes

**Test Case 3: Hierarchical Branch (with sub-branches)**
- Expected: Parent summary synthesizes across sub-branches
- Validate: Sub-branch summaries more specific than parent

**Test Case 4: Mixed Building Block Types**
- Expected: Summary adapts to mix (concepts + arguments + models)
- Validate: Relationships between different types explained

**Test Case 5: Technical Domain**
- Expected: Technical accuracy preserved, jargon used appropriately
- Validate: Domain expert would approve summary accuracy
