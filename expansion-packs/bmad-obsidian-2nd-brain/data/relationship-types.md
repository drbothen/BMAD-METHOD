# <!-- Powered by BMAD™ Core -->

# Relationship Types Taxonomy

## Purpose

This taxonomy provides formal definitions, bidirectional implications, and usage guidelines for the 7 semantic relationship types. It serves as the authoritative reference for type classification, helping both agents and users understand how each relationship type behaves and when to use it.

## Taxonomy Overview

The 7 relationship types represent fundamental patterns in knowledge graphs:

1. **SUPPORTS** - Evidence and justification
2. **CONTRADICTS** - Opposition and conflict
3. **ELABORATES** - Detail and explanation
4. **ANALOGOUS_TO** - Structural similarity
5. **GENERALIZES** - Abstraction
6. **SPECIALIZES** - Concretization
7. **INFLUENCES** - Causal lineage

---

## Type Definitions

### 1. SUPPORTS

**Formal Definition:**
A relationship where Note A provides evidence, data, logic, or examples that strengthen, validate, or justify claims made in Note B.

**Symbol:** A ⊢ B (A proves/supports B)

**Directionality:** Directed (A → B)

**Bidirectional Implications:**

- **Forward (A → B):** "A provides evidence for B"
- **Reverse (B ← A):** "B is supported by evidence from A"

**Type Properties:**

- Asymmetric: If A supports B, B typically doesn't support A
- Transitive: If A supports B and B supports C, then A indirectly supports C
- Strength-dependent: Support can be weak, moderate, or strong

**Keywords and Signals:**

- Evidence: "data shows", "research demonstrates", "experiment proves"
- Validation: "confirms", "corroborates", "validates", "verifies"
- Justification: "justifies", "substantiates", "backs up"
- Logical: "therefore", "thus", "consequently"

**Use Cases:**

- Linking empirical findings to theoretical claims
- Connecting examples to general arguments
- Building evidence chains for justification
- Creating argument networks

**When NOT to Use:**

- When A merely elaborates on B without providing evidence
- When A and B are analogous but not evidentially related
- When A influenced B historically but doesn't support its truth
- When the relationship is primarily definitional

**Strength Guidelines:**

- Strong (>= 0.8): Direct empirical evidence, controlled experiments
- Medium (0.6-0.79): Circumstantial evidence, multiple weak signals
- Weak (< 0.6): Anecdotal support, single example

---

### 2. CONTRADICTS

**Formal Definition:**
A relationship where Note A makes claims, assertions, or presents evidence that is logically incompatible with claims made in Note B.

**Symbol:** A ⊥ B (A contradicts B, B contradicts A)

**Directionality:** Bidirectional (A ↔ B)

**Bidirectional Implications:**

- **Forward (A → B):** "A conflicts with B's claims"
- **Reverse (B → A):** "B conflicts with A's claims"
  (These are symmetric - both are true simultaneously)

**Type Properties:**

- Symmetric: If A contradicts B, then B contradicts A
- Non-transitive: If A contradicts B and B contradicts C, A may support C
- Requires resolution: Contradictions demand investigation

**Keywords and Signals:**

- Opposition: "however", "but", "in contrast", "on the contrary"
- Conflict: "contradicts", "conflicts with", "inconsistent with"
- Challenge: "challenges", "refutes", "disproves"
- Paradox: "paradoxically", "surprisingly", "counter-intuitively"

**Use Cases:**

- Highlighting competing theories
- Documenting conflicting evidence
- Revealing paradoxes and tensions
- Creating critical thinking opportunities

**When NOT to Use:**

- When A and B address different aspects (nuance, not contradiction)
- When contradiction is only apparent, not actual
- When A and B apply in different contexts (both can be true)
- When one is a subset/refinement rather than opposition

**Strength Guidelines:**

- Strong (>= 0.8): Direct logical incompatibility, mutually exclusive
- Medium (0.6-0.79): Partial conflict, competing emphases
- Weak (< 0.6): Apparent but resolvable tension

---

### 3. ELABORATES

**Formal Definition:**
A relationship where Note A provides detailed explanation, expansion, or deeper analysis of concepts, ideas, or claims introduced in Note B.

**Symbol:** A ⊃ B (A contains details of B)

**Directionality:** Directed (A → B)

**Bidirectional Implications:**

- **Forward (A → B):** "A explains B in detail"
- **Reverse (B ← A):** "B is explained in detail by A"

**Type Properties:**

- Asymmetric: If A elaborates B, B typically doesn't elaborate A
- Transitive: If A elaborates B and B elaborates C, A super-elaborates C
- Depth-creating: Builds layers of understanding

**Keywords and Signals:**

- Detail: "in detail", "specifically", "precisely"
- Explanation: "for example", "such as", "namely"
- Expansion: "breaking down", "expanding on"
- Clarification: "in other words", "that is to say", "to elaborate"

**Use Cases:**

- Connecting overviews to detailed explanations
- Linking concepts to their components
- Building conceptual hierarchies
- Creating depth in knowledge graphs

**When NOT to Use:**

- When A provides evidence for B (use SUPPORTS)
- When A is a specific case of B (use SPECIALIZES)
- When A adds a new perspective rather than detail
- When A influenced B's creation (use INFLUENCES)

**Strength Guidelines:**

- Strong (>= 0.8): Comprehensive elaboration, all aspects covered
- Medium (0.6-0.79): Partial elaboration, some aspects detailed
- Weak (< 0.6): Minimal detail, mostly restating

---

### 4. ANALOGOUS_TO

**Formal Definition:**
A relationship where Note A describes a pattern, structure, or process that is functionally or structurally similar to Note B despite belonging to different domains or contexts.

**Symbol:** A ≈ B (A is analogous to B, B is analogous to A)

**Directionality:** Bidirectional (A ↔ B)

**Bidirectional Implications:**

- **Forward (A → B):** "A has the same structure as B"
- **Reverse (B → A):** "B has the same structure as A"
  (These are symmetric - both describe the same analogy)

**Type Properties:**

- Symmetric: If A is analogous to B, then B is analogous to A
- Transitive (weakly): If A ~ B and B ~ C, then A may be analogous to C
- Domain-crossing: Enables insight transfer

**Keywords and Signals:**

- Similarity: "similar to", "like", "resembles", "mirrors"
- Analogy: "analogous to", "parallel to", "comparable to"
- Structure: "the same pattern as", "follows the same structure"
- Metaphor: "just as", "in the same way that"

**Use Cases:**

- Cross-domain pattern recognition
- Metaphorical thinking and insight transfer
- Finding isomorphic structures
- Identifying functional equivalents

**When NOT to Use:**

- When similarity is only superficial (both require effort)
- When one is an actual instance of the other (use SPECIALIZES)
- When one explains the other (use ELABORATES)
- When they're in the same domain (use SUPPORTS/ELABORATES)

**Strength Guidelines:**

- Strong (>= 0.8): Deep structural isomorphism, multiple parallels
- Medium (0.6-0.79): Functional similarity, some parallels
- Weak (< 0.6): Superficial similarity, abstract connection

---

### 5. GENERALIZES

**Formal Definition:**
A relationship where Note A describes a broader, more abstract principle, pattern, or category of which Note B is a specific instance or example.

**Symbol:** A ⊇ B (A contains B as a case)

**Directionality:** Directed (A → B)

**Bidirectional Implications:**

- **Forward (A → B):** "A is a broader case of B"
- **Reverse (B ← A):** "B is a specific instance of A"

**Type Properties:**

- Asymmetric: If A generalizes B, then B specializes A (inverse)
- Transitive: If A generalizes B and B generalizes C, then A generalizes C
- Creates abstraction hierarchies

**Keywords and Signals:**

- Abstraction: "in general", "broadly speaking", "more generally"
- Scope: "as a whole", "overall", "the broader principle"
- Subsumption: "this is a case of", "an instance of"
- Application: "applies more widely", "extends beyond"

**Use Cases:**

- Building conceptual hierarchies (general → specific)
- Extracting patterns from instances
- Creating taxonomies and categorizations
- Connecting examples to principles

**When NOT to Use:**

- When A and B are at the same level of abstraction
- When A elaborates B without abstracting (use ELABORATES)
- When A and B are different but parallel (use ANALOGOUS_TO)
- When abstraction difference is minimal

**Strength Guidelines:**

- Strong (>= 0.8): Clear abstraction hierarchy, B clearly a subset of A
- Medium (0.6-0.79): Moderate abstraction difference
- Weak (< 0.6): Minor abstraction difference, ambiguous hierarchy

**Relationship to SPECIALIZES:**

GENERALIZES and SPECIALIZES are inverse relationships:

- If "A GENERALIZES B", then "B SPECIALIZES A"
- Always create both directions explicitly for clarity

---

### 6. SPECIALIZES

**Formal Definition:**
A relationship where Note A describes a specific, concrete instance, implementation, or application of the broader pattern or principle described in Note B.

**Symbol:** A ⊆ B (A is contained in B as a case)

**Directionality:** Directed (A → B)

**Bidirectional Implications:**

- **Forward (A → B):** "A is a specific case of B"
- **Reverse (B ← A):** "B is generalized by A" or "B is a broader case of A"

**Type Properties:**

- Asymmetric: If A specializes B, then B generalizes A (inverse)
- Transitive: If A specializes B and B specializes C, then A specializes C
- Creates concretization paths

**Keywords and Signals:**

- Specificity: "specifically", "in particular", "concretely"
- Instantiation: "for instance", "for example", "one case of"
- Implementation: "in practice", "applied to", "implemented as"
- Context: "in the context of", "within the domain of"

**Use Cases:**

- Connecting general principles to implementations
- Linking categories to instances
- Building concrete examples from abstractions
- Documenting domain-specific applications

**When NOT to Use:**

- When A and B are at same abstraction level
- When A elaborates B without specializing (use ELABORATES)
- When A is analogous but not a true instance (use ANALOGOUS_TO)
- When specificity difference is minimal

**Strength Guidelines:**

- Strong (>= 0.8): A is a clear, direct instance of B's pattern
- Medium (0.6-0.79): A applies B with some adaptation
- Weak (< 0.6): Tenuous connection to general pattern

**Relationship to GENERALIZES:**

SPECIALIZES and GENERALIZES are inverse relationships:

- If "A SPECIALIZES B", then "B GENERALIZES A"
- Both directions should be created explicitly

---

### 7. INFLUENCES

**Formal Definition:**
A relationship where Note A causally or inspirationally led to the creation, revision, or conceptualization of Note B, establishing intellectual lineage.

**Symbol:** A ↝ B (A led to B)

**Directionality:** Directed (A → B)

**Bidirectional Implications:**

- **Forward (A → B):** "A inspired/led to B"
- **Reverse (B ← A):** "B was inspired/influenced by A"

**Type Properties:**

- Asymmetric: If A influenced B, B didn't influence A (temporal precedence)
- Non-transitive: If A influenced B and B influenced C, A may not influence C
- Temporal: Requires A to predate B
- Causal: Establishes lineage and provenance

**Keywords and Signals:**

- Inspiration: "inspired", "sparked", "prompted", "motivated"
- Causation: "led to", "resulted in", "gave rise to"
- Building: "based on", "building on", "grew out of"
- Response: "in response to", "prompted by"

**Use Cases:**

- Tracking idea evolution and lineage
- Documenting intellectual genealogy
- Understanding knowledge provenance
- Mapping thought development over time

**When NOT to Use:**

- When A and B created simultaneously (no temporal order)
- When A supports B logically but didn't cause its creation (use SUPPORTS)
- When A elaborates B but didn't inspire it (use ELABORATES)
- When influence is indirect or unclear

**Strength Guidelines:**

- Strong (>= 0.8): Direct causal influence, explicit acknowledgment
- Medium (0.6-0.79): Probable influence, temporal and thematic alignment
- Weak (< 0.6): Possible influence, circumstantial evidence

**Temporal Verification:**

- Verify A's creation date predates B's creation date
- Check edit timestamps for revision influence
- Reject if temporal order violated

---

## Type Selection Flowchart

```
START: Given two notes A and B, classify their relationship

├─ TEMPORAL CHECK
│  └─ Did A exist first and causally inspire B?
│     YES → INFLUENCES
│     NO/UNCLEAR → Continue

├─ CONFLICT CHECK
│  └─ Do A and B make incompatible claims?
│     YES → CONTRADICTS
│     NO → Continue

├─ EVIDENCE CHECK
│  └─ Does A provide evidence/data for B's claims?
│     YES → SUPPORTS
│     NO → Continue

├─ ABSTRACTION CHECK
│  └─ Are A and B at different abstraction levels?
│     YES → Is A more abstract?
│        YES → GENERALIZES
│        NO → SPECIALIZES
│     NO → Continue

├─ DOMAIN CHECK
│  └─ Are A and B in different domains but structurally similar?
│     YES → ANALOGOUS_TO
│     NO → Continue

├─ ELABORATION CHECK
│  └─ Does A explain/detail B or vice versa?
│     YES → ELABORATES
│     NO → Continue

└─ DEFAULT
   └─ ELABORATES (safest fallback)
```

---

## Type Combination Patterns

### Valid Combinations (Multiple types can apply)

1. **INFLUENCES + SUPPORTS**
   Example: "Ebbinghaus Forgetting Curve" influenced SRS design AND supports its effectiveness

2. **ELABORATES + SPECIALIZES**
   Example: "Cypher Parameterization" elaborates on injection prevention AND specializes SQL parameterization

3. **GENERALIZES + SUPPORTS**
   Example: "Spacing Effect" generalizes from vocabulary learning AND supports language acquisition claims

### Invalid Combinations (Logically incompatible)

1. **SUPPORTS + CONTRADICTS** → Mutually exclusive
2. **GENERALIZES + SPECIALIZES** (same pair) → Inverse, not both directions
3. **INFLUENCES (A→B) + INFLUENCES (B→A)** → Temporal contradiction

---

## Type Strength Calibration

### Confidence Thresholds

For each type, confidence score determines acceptance:

- **High Confidence (>= 0.8):** Auto-approve in batch mode
- **Medium Confidence (0.6-0.79):** Prompt user for confirmation
- **Low Confidence (< 0.6):** Reject or flag for manual review

### Signal Strength Examples

**SUPPORTS - High Confidence:**

- "Meta-analysis of 317 studies confirms..."
- "Controlled experiment demonstrated..."

**SUPPORTS - Medium Confidence:**

- "Several examples suggest..."
- "Anecdotal evidence indicates..."

**SUPPORTS - Low Confidence:**

- "Someone mentioned that..."
- "It seems related to..."

---

## Usage Guidelines for Agents

### For Semantic Linker Agent

1. **Type Identification (identify-concept-overlap.md)**
   - Check linguistic signals against this taxonomy
   - Calculate confidence based on signal strength
   - Apply decision tree for ambiguous cases

2. **Bidirectional Creation**
   - For symmetric types (CONTRADICTS, ANALOGOUS_TO): create same type in both directions
   - For asymmetric types: create inverse context sentences

3. **Validation**
   - INFLUENCES: Verify temporal precedence
   - GENERALIZES/SPECIALIZES: Verify abstraction difference
   - SUPPORTS: Verify evidential relationship

### For Users

1. **Manual Linking**
   - Use \*create-link command with explicit type
   - Refer to this taxonomy for type selection
   - Check "When NOT to Use" to avoid misclassification

2. **Reviewing Suggestions**
   - Understand why agent chose each type
   - Override if context requires different type
   - Provide feedback for learning

---

## References

- Source: `/manuscripts/bmad-obsidian-2nd-brain-requirements.md` (lines 3806-3813)
- Luhmann, N. (1992). _Communicating with Slip Boxes_
- Ahrens, S. (2017). _How to Take Smart Notes_
- Sowa, J. F. (2000). _Knowledge Representation: Logical, Philosophical, and Computational Foundations_
