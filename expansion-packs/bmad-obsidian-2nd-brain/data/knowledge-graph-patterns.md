# Knowledge Graph Patterns

**Version:** 2.0
**Phase:** 2 - Synthesis & Temporal Analysis
**Last Updated:** 2025-11-11
**Purpose:** Graph patterns for temporal relationship tracking and knowledge evolution modeling in Neo4j Graphiti

---

## Table of Contents

1. [Introduction](#introduction)
2. [Temporal Relationship Types](#temporal-relationship-types)
3. [Evolution Patterns](#evolution-patterns)
4. [Example Graph Structures](#example-graph-structures)
5. [Pattern Catalog](#pattern-catalog)
6. [Query Patterns](#query-patterns)

---

## Introduction

### What are Knowledge Graph Patterns?

Knowledge graph patterns are recurring structures that represent how concepts, relationships, and temporal events are connected in a knowledge base. This guide documents patterns specific to temporal evolution tracking in the BMAD Obsidian 2nd Brain system.

### Why Graph Patterns Matter

**Benefits:**
- **Discoverability**: Recognize patterns when they emerge
- **Consistency**: Model similar scenarios in similar ways
- **Queryability**: Standard patterns enable reusable queries
- **Evolution tracking**: Understand how knowledge develops over time

**Core Concepts:**
- **Nodes**: Concepts, notes, events, MOCs
- **Relationships**: How entities connect and influence each other
- **Temporal dimension**: When relationships formed and how they evolved
- **Metadata**: Additional context about connections

### Phase 2 Focus

This version adds temporal relationship types and evolution patterns introduced in Phase 2:
- Temporal event tracking (CAPTURE, EDIT, PROMOTION, LINK, MOC_ADDED)
- Understanding shift detection (contradictions, synthesis, integrations)
- Maturation metrics and development phases
- Cross-domain evolution patterns

---

## Temporal Relationship Types

### Core Relationship Types

These are the fundamental relationships used to model temporal evolution:

#### EVOLVED_FROM

**Direction:** Newer concept → Older concept
**Semantics:** Indicates that one concept developed from or built upon another
**Metadata:**
- `evolution_type`: refinement | expansion | synthesis | specialization
- `time_gap_days`: Days between concepts
- `trigger_event`: What caused the evolution
- `preserved_aspects`: What stayed the same
- `changed_aspects`: What was different

**Example:**

```cypher
(new_concept:Note {title: "Spaced Repetition Systems"})-[:EVOLVED_FROM {
  evolution_type: "specialization",
  time_gap_days: 45,
  trigger_event: "Read Wozniak's SuperMemo research",
  preserved_aspects: "Timing intervals for review",
  changed_aspects: "Added algorithmic optimization"
}]->(old_concept:Note {title: "Spaced Repetition"})
```

**Use Cases:**
- Track concept refinement over time
- Trace idea lineages
- Identify knowledge consolidation points

#### CONTRADICTS

**Direction:** New understanding → Previous understanding
**Semantics:** New information contradicts or replaces earlier beliefs
**Metadata:**
- `contradiction_type`: full_replacement | partial_conflict | reframing
- `resolution_status`: unresolved | resolved_synthesis | resolved_rejection
- `discovered_at`: Timestamp when contradiction emerged
- `evidence`: What revealed the contradiction
- `synthesis_note`: If resolved, reference to synthesis

**Example:**

```cypher
(new:Note {title: "Memory is Reconstructive"})-[:CONTRADICTS {
  contradiction_type: "full_replacement",
  resolution_status: "resolved_synthesis",
  discovered_at: "2024-02-10T14:30:00Z",
  evidence: "Loftus & Palmer (1974) eyewitness study",
  synthesis_note: "[[Memory Models Compared]]"
}]->(old:Note {title: "Memory as Filing Cabinet"})
```

**Use Cases:**
- Detect understanding shifts
- Track resolution of conflicting ideas
- Generate temporal narratives about belief revision

#### INFLUENCED_BY

**Direction:** Dependent concept → Influencing source
**Semantics:** One concept was shaped by another (source, reference, related concept)
**Metadata:**
- `influence_type`: source_citation | conceptual_analogy | methodology | framework
- `strength`: 0.0-1.0 (how much influence)
- `first_cited`: Timestamp of first reference
- `influence_description`: How the influence manifested
- `specific_aspects`: What parts were influenced

**Example:**

```cypher
(concept:Note {title: "Zettelkasten Workflow"})-[:INFLUENCED_BY {
  influence_type: "source_citation",
  strength: 0.95,
  first_cited: "2024-01-20T10:00:00Z",
  influence_description: "Core methodology and principles",
  specific_aspects: ["atomicity", "linking", "permanent notes"]
}]->(source:Note {title: "Ahrens (2017) How to Take Smart Notes"})
```

**Use Cases:**
- Map knowledge provenance
- Identify high-impact sources
- Generate "influenced by" sections in temporal narratives

#### MATURED_AT

**Direction:** Concept → Maturation milestone event
**Semantics:** Concept reached a significant maturation stage
**Metadata:**
- `milestone_type`: promoted_permanent | promoted_evergreen | first_moc_integration | synthesis_achieved
- `maturation_phase`: capture | development | maturation | maintenance
- `time_from_capture_days`: Days since concept creation
- `trigger_events`: What caused maturation
- `quality_indicators`: Metrics at milestone

**Example:**

```cypher
(concept:Note {title: "Spaced Repetition"})-[:MATURED_AT {
  milestone_type: "promoted_evergreen",
  maturation_phase: "maturation",
  time_from_capture_days: 78,
  trigger_events: ["comprehensive_editing", "moc_integration", "citation_accumulation"],
  quality_indicators: {
    edit_count: 15,
    link_count: 23,
    backlink_count: 8,
    moc_memberships: 2
  }
}]->(event:MilestoneEvent {timestamp: "2024-04-10T16:00:00Z"})
```

**Use Cases:**
- Track maturation speed
- Identify maturation bottlenecks
- Calculate maturation metrics

### Supplementary Relationship Types

Additional relationships that complement temporal tracking:

#### SYNTHESIZED_INTO

**Direction:** Component concepts → Synthesis note
**Semantics:** Multiple concepts were combined into a new unified understanding
**Metadata:**
- `synthesis_date`: When synthesis occurred
- `synthesis_type`: integration | reconciliation | emergence
- `component_count`: Number of ideas combined
- `synthesis_insight`: New understanding created

**Example:**

```cypher
(concept1:Note {title: "Active Recall"})-[:SYNTHESIZED_INTO {
  synthesis_date: "2024-03-15T12:00:00Z",
  synthesis_type: "integration",
  component_count: 3,
  synthesis_insight: "Retrieval practice is the unifying mechanism"
}]->(synthesis:Note {title: "Desirable Difficulties Framework"})

(concept2:Note {title: "Spaced Practice"})-[:SYNTHESIZED_INTO]->(synthesis)
(concept3:Note {title: "Interleaving"})-[:SYNTHESIZED_INTO]->(synthesis)
```

#### BRANCHED_FROM

**Direction:** Specialized concept → General concept
**Semantics:** A specific case or application branched from a general principle
**Metadata:**
- `branch_date`: When specialization occurred
- `specificity_dimension`: application | subdomain | example | constraint
- `retained_properties`: General aspects preserved
- `new_properties`: Specialized aspects added

**Example:**

```cypher
(specific:Note {title: "Anki Algorithm"})-[:BRANCHED_FROM {
  branch_date: "2024-02-20T09:00:00Z",
  specificity_dimension: "application",
  retained_properties: ["spacing_intervals", "forgetting_curve_basis"],
  new_properties: ["sm2_algorithm", "ease_factor", "digital_implementation"]
}]->(general:Note {title: "Spaced Repetition Theory"})
```

#### TEMPORALLY_COOCCURRED

**Direction:** Concept A ← bidirectional → Concept B
**Semantics:** Concepts were developed, edited, or thought about during the same time periods
**Metadata:**
- `cooccurrence_count`: Number of shared time windows
- `cooccurrence_windows`: Specific date ranges
- `cooccurrence_strength`: 0.0-1.0 (frequency of co-development)
- `relationship_discovered`: Was explicit link eventually created?

**Example:**

```cypher
(conceptA:Note {title: "Evergreen Notes"})-[:TEMPORALLY_COOCCURRED {
  cooccurrence_count: 5,
  cooccurrence_windows: ["2024-01-15 to 2024-01-22", "2024-02-01 to 2024-02-07"],
  cooccurrence_strength: 0.82,
  relationship_discovered: true
}]->(conceptB:Note {title: "Atomic Notes"})
```

---

## Evolution Patterns

### Pattern 1: Concept Emergence

**Description:** How a new concept forms from capture to maturation

**Graph Structure:**

```
CAPTURE_EVENT → fleeting_note → EDIT → EDIT → PROMOTION_EVENT →
permanent_note → LINK → LINK → MOC_ADDED_EVENT → PROMOTION_EVENT →
evergreen_note
```

**Cypher Representation:**

```cypher
// Concept emergence timeline
(capture:Event {type: 'CAPTURE', timestamp: '2024-01-15'})-[:CREATED]->(note:Note {status: 'fleeting'})
(note)-[:HAS_EVENT]->(edit1:Event {type: 'EDIT', timestamp: '2024-01-17'})
(note)-[:HAS_EVENT]->(edit2:Event {type: 'EDIT', timestamp: '2024-01-22'})
(note)-[:HAS_EVENT]->(promo1:Event {type: 'PROMOTION', from: 'fleeting', to: 'permanent'})
(note)-[:HAS_EVENT]->(link1:Event {type: 'LINK', target: 'Related Concept'})
(note)-[:HAS_EVENT]->(moc:Event {type: 'MOC_ADDED', moc_name: 'Domain MOC'})
(note)-[:HAS_EVENT]->(promo2:Event {type: 'PROMOTION', from: 'permanent', to: 'evergreen'})
```

**Characteristics:**
- Linear progression through phases
- Promotion events mark phase transitions
- Linking intensity increases over time
- MOC integration signals domain establishment

**Detection Query:**

```cypher
MATCH path = (capture:Event {type: 'CAPTURE'})-[:CREATED]->(n:Note)-[:HAS_EVENT*]->(promo:Event {type: 'PROMOTION'})
WHERE promo.metadata.to = 'evergreen'
RETURN path, length(path) AS emergence_steps
```

### Pattern 2: Understanding Shift

**Description:** How contradictions lead to revised understanding

**Graph Structure:**

```
old_understanding → EDIT_EVENT (contradiction detected) →
contradiction_note ← INFLUENCED_BY ← new_source →
synthesis_note (resolves contradiction) → EVOLVED_FROM → old_understanding
```

**Cypher Representation:**

```cypher
// Understanding shift pattern
(old:Note {title: "Memory as Storage"})-[:CONTRADICTED_BY]->(new:Note {title: "Memory as Reconstruction"})
(new)-[:INFLUENCED_BY {evidence: "Loftus & Palmer (1974)"}]->(source:Note {title: "Eyewitness Research"})
(synthesis:Note {title: "Dual Process Memory Model"})-[:SYNTHESIZED_INTO]-(old)
(synthesis)-[:SYNTHESIZED_INTO]-(new)
(synthesis)-[:EVOLVED_FROM]->(old)
```

**Characteristics:**
- Contradiction triggers re-evaluation
- New evidence drives understanding shift
- Synthesis resolves contradiction at higher level
- Old understanding not deleted, but contextualized

**Detection Query:**

```cypher
MATCH (old:Note)-[c:CONTRADICTS]->(new:Note)
OPTIONAL MATCH (new)-[:INFLUENCED_BY]->(source)
OPTIONAL MATCH (synthesis)-[:SYNTHESIZED_INTO]->(old), (synthesis)-[:SYNTHESIZED_INTO]->(new)
RETURN old, new, c, source, synthesis
```

### Pattern 3: Knowledge Consolidation

**Description:** How scattered insights consolidate into structured domains

**Graph Structure:**

```
atomic_note_1 → MOC_ADDED → Domain_MOC
atomic_note_2 → MOC_ADDED → Domain_MOC
atomic_note_3 → MOC_ADDED → Domain_MOC
...
Domain_MOC → MATURED (nascent → developing → established)
Domain_MOC → BRANCHED_INTO → subdomain_MOC_1
Domain_MOC → BRANCHED_INTO → subdomain_MOC_2
```

**Cypher Representation:**

```cypher
// Knowledge consolidation pattern
(note1:Note)-[:BELONGS_TO]->(moc:MOC {title: "Learning Systems", maturity: "nascent"})
(note2:Note)-[:BELONGS_TO]->(moc)
(note3:Note)-[:BELONGS_TO]->(moc)
// ... 30 notes added
(moc)-[:MATURED_AT {from: "nascent", to: "developing"}]->(milestone1:Event)
// ... continued growth
(moc)-[:MATURED_AT {from: "developing", to: "established"}]->(milestone2:Event)
(submoc1:MOC {title: "Spaced Repetition Systems"})-[:BRANCHED_FROM]->(moc)
(submoc2:MOC {title: "Active Learning Techniques"})-[:BRANCHED_FROM]->(moc)
```

**Characteristics:**
- Gradual accumulation of notes
- Maturity thresholds: nascent (0-10), developing (11-30), established (31-60), comprehensive (60+)
- Branching occurs as domains mature
- Hierarchical organization emerges

**Detection Query:**

```cypher
MATCH (moc:MOC)-[:MATURED_AT]->(milestone)
OPTIONAL MATCH (moc)<-[:BELONGS_TO]-(notes:Note)
WITH moc, count(notes) AS note_count, collect(milestone) AS milestones
WHERE note_count > 30
RETURN moc, note_count, milestones
```

### Pattern 4: Source Integration

**Description:** How multiple sources combine to shape understanding

**Graph Structure:**

```
source_1 → INFLUENCED_BY → concept ← INFLUENCED_BY ← source_2
                            ↓
                         EDIT_EVENT (integration)
                            ↓
                      enriched_concept ← INFLUENCED_BY ← source_3
```

**Cypher Representation:**

```cypher
// Source integration pattern
(concept:Note {title: "Zettelkasten"})-[:INFLUENCED_BY {
  influence_type: "source_citation",
  first_cited: "2024-01-20",
  strength: 0.95
}]->(source1:Note {title: "Ahrens (2017)"})

(concept)-[:INFLUENCED_BY {
  influence_type: "source_citation",
  first_cited: "2024-02-05",
  strength: 0.80
}]->(source2:Note {title: "Forte (2022)"})

(concept)-[:HAS_EVENT]->(integration:Event {
  type: 'EDIT',
  edit_type: 'source_integration',
  timestamp: '2024-02-10'
})

(concept)-[:INFLUENCED_BY {
  influence_type: "methodology",
  first_cited: "2024-03-01",
  strength: 0.75
}]->(source3:Note {title: "Luhmann's Original System"})
```

**Characteristics:**
- Multiple sources cited over time
- Integration events synthesize sources
- Influence strength varies by source
- Progressive enrichment through accumulation

**Detection Query:**

```cypher
MATCH (concept:Note)-[i:INFLUENCED_BY]->(source)
WITH concept, count(source) AS source_count, collect({source: source.title, strength: i.strength}) AS influences
WHERE source_count >= 3
RETURN concept, source_count, influences
ORDER BY source_count DESC
```

### Pattern 5: Stagnation and Revival

**Description:** How concepts stall in development, then revive

**Graph Structure:**

```
concept → EDIT (active development) → ... → EDIT → [90+ days gap] →
STAGNANT_PERIOD → [trigger_event] → EDIT (revival) → MOC_ADDED → PROMOTED
```

**Cypher Representation:**

```cypher
// Stagnation and revival pattern
(concept:Note)-[:HAS_EVENT]->(edit1:Event {type: 'EDIT', timestamp: '2024-01-15'})
(concept)-[:HAS_EVENT]->(edit2:Event {type: 'EDIT', timestamp: '2024-01-22'})
// Long gap
(concept)-[:HAS_EVENT]->(revival:Event {
  type: 'EDIT',
  timestamp: '2024-05-10',
  revival_trigger: 'Project requirement',
  stagnation_days: 108
})
(concept)-[:HAS_EVENT]->(moc:Event {type: 'MOC_ADDED', timestamp: '2024-05-15'})
(concept)-[:HAS_EVENT]->(promo:Event {type: 'PROMOTION', timestamp: '2024-05-20'})
```

**Characteristics:**
- Extended inactivity (90+ days)
- External trigger causes revival
- Rapid progress after revival
- Often MOC integration or project need triggers

**Detection Query:**

```cypher
MATCH (n:Note)-[:HAS_EVENT]->(e1:Event {type: 'EDIT'})
MATCH (n)-[:HAS_EVENT]->(e2:Event {type: 'EDIT'})
WHERE e2.timestamp > e1.timestamp
WITH n, e1, e2, duration.between(e1.timestamp, e2.timestamp).days AS gap
WHERE gap > 90
RETURN n, e1.timestamp AS before_gap, e2.timestamp AS after_gap, gap AS stagnation_days
ORDER BY gap DESC
```

### Pattern 6: Cross-Domain Synthesis

**Description:** How concepts from different domains connect and synthesize

**Graph Structure:**

```
domain_A_concept → cross_domain_link → domain_B_concept
       ↓                                        ↓
   MOC_A (domain A)                        MOC_B (domain B)
       ↓                                        ↓
       └───────────→ synthesis_concept ←────────┘
                            ↓
                      meta_MOC (bridge)
```

**Cypher Representation:**

```cypher
// Cross-domain synthesis
(conceptA:Note {title: "Spaced Repetition"})-[:BELONGS_TO]->(mocA:MOC {title: "Learning Systems"})
(conceptB:Note {title: "Git Commit Frequency"})-[:BELONGS_TO]->(mocB:MOC {title: "Software Engineering"})

(conceptA)-[:HAS_EVENT]->(link:Event {
  type: 'LINK',
  target: conceptB.path,
  timestamp: '2024-03-15',
  cross_domain: true
})

(synthesis:Note {title: "Spaced Practice in Coding"})-[:SYNTHESIZED_INTO]-(conceptA)
(synthesis)-[:SYNTHESIZED_INTO]-(conceptB)

(metaMoc:MOC {title: "Learning Techniques Applied"})-[:BRIDGES]->(mocA)
(metaMoc)-[:BRIDGES]->(mocB)
(synthesis)-[:BELONGS_TO]->(metaMoc)
```

**Characteristics:**
- Links between different MOC domains
- Synthesis note combines insights
- Meta-MOC bridges domains
- Analogical thinking manifested

**Detection Query:**

```cypher
MATCH (moc1:MOC)<-[:BELONGS_TO]-(n1:Note)-[:LINKED_TO]->(n2:Note)-[:BELONGS_TO]->(moc2:MOC)
WHERE moc1 <> moc2
WITH moc1, moc2, count(*) AS cross_links
WHERE cross_links >= 3
RETURN moc1.title AS domain1, moc2.title AS domain2, cross_links
ORDER BY cross_links DESC
```

---

## Example Graph Structures

### Example 1: Complete Concept Evolution

**Scenario:** "Spaced Repetition" concept from fleeting note to evergreen

```cypher
// Create initial capture
CREATE (capture:Event {
  type: 'CAPTURE',
  timestamp: datetime('2024-01-15T10:30:00Z'),
  initial_content: 'Review material at increasing intervals'
})

CREATE (concept:Note {
  title: 'Spaced Repetition',
  path: 'atomic/spaced-repetition.md',
  status: 'fleeting',
  building_block_type: 'concept'
})

CREATE (capture)-[:CREATED]->(concept)

// Development phase edits
CREATE (edit1:Event {
  type: 'EDIT',
  timestamp: datetime('2024-01-17T14:00:00Z'),
  lines_changed: 12,
  edit_type: 'expansion'
})
CREATE (concept)-[:HAS_EVENT]->(edit1)

CREATE (edit2:Event {
  type: 'EDIT',
  timestamp: datetime('2024-01-22T09:15:00Z'),
  lines_changed: 8,
  edit_type: 'source_integration'
})
CREATE (concept)-[:HAS_EVENT]->(edit2)

// Add influences
CREATE (source1:Note {
  title: 'Ebbinghaus Forgetting Curve',
  path: 'sources/ebbinghaus.md'
})
CREATE (concept)-[:INFLUENCED_BY {
  influence_type: 'source_citation',
  strength: 0.95,
  first_cited: datetime('2024-01-22T09:15:00Z')
}]->(source1)

// Promotion to permanent
CREATE (promo1:Event {
  type: 'PROMOTION',
  timestamp: datetime('2024-02-03T11:00:00Z'),
  from: 'fleeting',
  to: 'permanent'
})
CREATE (concept)-[:HAS_EVENT]->(promo1)
SET concept.status = 'permanent'

// Linking phase
CREATE (related:Note {title: 'Active Recall', path: 'atomic/active-recall.md'})
CREATE (link1:Event {
  type: 'LINK',
  timestamp: datetime('2024-02-14T16:20:00Z'),
  target: 'atomic/active-recall.md',
  direction: 'bidirectional'
})
CREATE (concept)-[:HAS_EVENT]->(link1)

// MOC integration
CREATE (moc:MOC {
  title: 'Learning Systems MOC',
  path: 'mocs/learning-systems.md',
  maturity: 'developing'
})
CREATE (mocEvent:Event {
  type: 'MOC_ADDED',
  timestamp: datetime('2024-03-20T10:00:00Z'),
  moc_name: 'Learning Systems MOC'
})
CREATE (concept)-[:HAS_EVENT]->(mocEvent)
CREATE (concept)-[:BELONGS_TO]->(moc)

// Promotion to evergreen
CREATE (promo2:Event {
  type: 'PROMOTION',
  timestamp: datetime('2024-04-10T16:00:00Z'),
  from: 'permanent',
  to: 'evergreen'
})
CREATE (concept)-[:HAS_EVENT]->(promo2)
SET concept.status = 'evergreen'

// Maturation milestone
CREATE (milestone:MilestoneEvent {
  timestamp: datetime('2024-04-10T16:00:00Z'),
  milestone_type: 'promoted_evergreen',
  days_from_capture: 85
})
CREATE (concept)-[:MATURED_AT {
  maturation_phase: 'maturation',
  time_from_capture_days: 85,
  quality_indicators: {
    edit_count: 15,
    link_count: 23,
    backlink_count: 8
  }
}]->(milestone)
```

### Example 2: Understanding Shift with Contradiction

**Scenario:** Memory understanding evolves from storage model to reconstruction model

```cypher
// Old understanding
CREATE (old:Note {
  title: 'Memory as Filing Cabinet',
  path: 'atomic/memory-storage-model.md',
  created: datetime('2024-01-10'),
  status: 'permanent'
})

// New conflicting information
CREATE (new:Note {
  title: 'Memory is Reconstructive',
  path: 'atomic/memory-reconstruction.md',
  created: datetime('2024-02-10'),
  status: 'permanent'
})

// Evidence source
CREATE (evidence:Note {
  title: 'Loftus & Palmer (1974) Study',
  path: 'sources/eyewitness-testimony.md'
})

// Create contradiction relationship
CREATE (new)-[:CONTRADICTS {
  contradiction_type: 'full_replacement',
  discovered_at: datetime('2024-02-10T14:30:00Z'),
  evidence: 'Eyewitness testimony malleability',
  resolution_status: 'resolved_synthesis'
}]->(old)

// Influence relationship
CREATE (new)-[:INFLUENCED_BY {
  influence_type: 'source_citation',
  strength: 0.98,
  first_cited: datetime('2024-02-10T14:30:00Z')
}]->(evidence)

// Synthesis resolves contradiction
CREATE (synthesis:Note {
  title: 'Dual Process Memory Model',
  path: 'atomic/memory-dual-process.md',
  created: datetime('2024-02-15'),
  status: 'permanent'
})

CREATE (synthesis)-[:SYNTHESIZED_INTO]-(old)
CREATE (synthesis)-[:SYNTHESIZED_INTO]-(new)
CREATE (synthesis)-[:EVOLVED_FROM {
  evolution_type: 'synthesis',
  time_gap_days: 36,
  trigger_event: 'Contradiction resolution'
}]->(old)

// Update contradiction status
MATCH (new)-[c:CONTRADICTS]->(old)
SET c.synthesis_note = 'atomic/memory-dual-process.md'
```

### Example 3: Domain Consolidation with MOC Maturation

**Scenario:** Learning domain grows from scattered notes to structured MOC system

```cypher
// Create domain MOC
CREATE (moc:MOC {
  title: 'Learning Systems MOC',
  path: 'mocs/learning-systems.md',
  created: datetime('2024-01-01'),
  maturity: 'nascent',
  note_count: 0
})

// Add initial notes (nascent: 0-10 notes)
UNWIND range(1, 8) AS i
CREATE (note:Note {
  title: 'Learning Concept ' + i,
  path: 'atomic/learning-' + i + '.md',
  created: datetime('2024-01-' + (i+10))
})
CREATE (note)-[:BELONGS_TO]->(moc)
WITH moc
SET moc.note_count = 8

// First maturation milestone: nascent → developing
CREATE (milestone1:MilestoneEvent {
  timestamp: datetime('2024-02-15T10:00:00Z'),
  milestone_type: 'maturity_threshold',
  from_maturity: 'nascent',
  to_maturity: 'developing'
})
CREATE (moc)-[:MATURED_AT {
  from: 'nascent',
  to: 'developing',
  time_from_creation_days: 45
}]->(milestone1)
SET moc.maturity = 'developing'

// Continue adding notes (developing: 11-30 notes)
UNWIND range(9, 25) AS i
CREATE (note:Note {
  title: 'Learning Concept ' + i,
  path: 'atomic/learning-' + i + '.md'
})
CREATE (note)-[:BELONGS_TO]->(moc)
WITH moc
SET moc.note_count = 25

// Second maturation: developing → established
CREATE (milestone2:MilestoneEvent {
  timestamp: datetime('2024-04-20T15:00:00Z'),
  milestone_type: 'maturity_threshold',
  from_maturity: 'developing',
  to_maturity: 'established'
})
CREATE (moc)-[:MATURED_AT {
  from: 'developing',
  to: 'established',
  time_from_creation_days: 110
}]->(milestone2)
SET moc.maturity = 'established'

// Domain branches emerge
CREATE (submoc1:MOC {
  title: 'Spaced Repetition Systems',
  path: 'mocs/spaced-repetition-systems.md',
  maturity: 'nascent'
})
CREATE (submoc1)-[:BRANCHED_FROM {
  branch_date: datetime('2024-05-01'),
  specificity_dimension: 'subdomain'
}]->(moc)

CREATE (submoc2:MOC {
  title: 'Active Learning Techniques',
  path: 'mocs/active-learning.md',
  maturity: 'nascent'
})
CREATE (submoc2)-[:BRANCHED_FROM {
  branch_date: datetime('2024-05-10'),
  specificity_dimension: 'subdomain'
}]->(moc)
```

---

## Pattern Catalog

### Quick Reference Table

| Pattern Name | Primary Relationships | Use Case | Detection Difficulty |
|--------------|----------------------|----------|---------------------|
| Concept Emergence | CAPTURE → EDIT* → PROMOTION → LINK → MOC_ADDED | Track note maturation | Easy |
| Understanding Shift | CONTRADICTS + INFLUENCED_BY + SYNTHESIZED_INTO | Detect belief revision | Medium |
| Knowledge Consolidation | BELONGS_TO + MATURED_AT + BRANCHED_FROM | Domain growth tracking | Easy |
| Source Integration | INFLUENCED_BY (multiple) | Provenance mapping | Easy |
| Stagnation & Revival | HAS_EVENT with time gaps | Identify stuck concepts | Medium |
| Cross-Domain Synthesis | LINKED_TO across MOCs + BRIDGES | Analogical connections | Hard |

### Pattern Applicability

**For Timeline Constructor Agent:**
- Concept Emergence: Primary pattern for temporal narratives
- Understanding Shift: Detects shifts for narrative inclusion
- Source Integration: Generates influences section

**For MOC Constructor Agent:**
- Knowledge Consolidation: Tracks domain maturity
- Cross-Domain Synthesis: Identifies bridging opportunities

**For Semantic Linker Agent:**
- Cross-Domain Synthesis: Suggests high-value cross-domain links
- Stagnation & Revival: Deprioritizes stagnant concepts

---

## Query Patterns

### Pattern Detection Queries

#### Find All Understanding Shifts

```cypher
MATCH (new:Note)-[c:CONTRADICTS]->(old:Note)
OPTIONAL MATCH (new)-[:INFLUENCED_BY]->(evidence)
OPTIONAL MATCH (synthesis)-[:SYNTHESIZED_INTO]->(new)
OPTIONAL MATCH (synthesis)-[:SYNTHESIZED_INTO]->(old)
RETURN new.title AS new_understanding,
       old.title AS old_understanding,
       c.discovered_at AS when_shifted,
       c.evidence AS what_caused_shift,
       evidence.title AS evidence_source,
       synthesis.title AS synthesis_note,
       c.resolution_status AS resolution
ORDER BY c.discovered_at DESC
```

#### Find Rapidly Maturing Concepts

```cypher
MATCH (n:Note)-[:MATURED_AT {milestone_type: 'promoted_evergreen'}]->(m:MilestoneEvent)
WHERE m.time_from_capture_days < 60  // Faster than 60 days
RETURN n.title AS concept,
       m.timestamp AS promoted_date,
       m.time_from_capture_days AS maturation_days
ORDER BY maturation_days ASC
LIMIT 10
```

#### Find Cross-Domain Connections

```cypher
MATCH (moc1:MOC)<-[:BELONGS_TO]-(n1:Note)
MATCH (n1)-[:HAS_EVENT]->(link:Event {type: 'LINK'})
MATCH (n2:Note {path: link.metadata.target_note})-[:BELONGS_TO]->(moc2:MOC)
WHERE moc1 <> moc2
WITH moc1.title AS domain1,
     moc2.title AS domain2,
     count(link) AS link_count,
     collect({note1: n1.title, note2: n2.title, when: link.timestamp}) AS connections
WHERE link_count >= 3
RETURN domain1, domain2, link_count, connections
ORDER BY link_count DESC
```

#### Find Concepts with Multiple Influences

```cypher
MATCH (concept:Note)-[i:INFLUENCED_BY]->(source:Note)
WITH concept,
     count(source) AS source_count,
     collect({
       source: source.title,
       influence_type: i.influence_type,
       strength: i.strength,
       first_cited: i.first_cited
     }) AS influences
WHERE source_count >= 3
RETURN concept.title AS concept_title,
       source_count,
       influences
ORDER BY source_count DESC
```

#### Track MOC Domain Growth

```cypher
MATCH (moc:MOC)-[:MATURED_AT]->(milestone)
OPTIONAL MATCH (moc)<-[:BELONGS_TO]-(notes:Note)
WITH moc,
     count(DISTINCT notes) AS current_note_count,
     moc.maturity AS current_maturity,
     collect({
       from: milestone.from_maturity,
       to: milestone.to_maturity,
       when: milestone.timestamp
     }) AS maturation_history
RETURN moc.title AS domain,
       current_note_count,
       current_maturity,
       maturation_history
ORDER BY current_note_count DESC
```

---

## Best Practices

### Pattern Application Guidelines

1. **Prefer explicit relationships over inference**
   - Create EVOLVED_FROM rather than inferring from timestamps
   - Document INFLUENCED_BY when you cite sources
   - Mark CONTRADICTS when you detect conflicts

2. **Capture metadata at creation time**
   - Relationship metadata degrades over time
   - Record triggers and evidence immediately
   - Note resolution status for contradictions

3. **Use appropriate granularity**
   - Not every edit needs EVOLVED_FROM
   - Reserve for significant conceptual shifts
   - Balance completeness with query performance

4. **Maintain temporal consistency**
   - Timestamps must be chronological
   - Event sequences should make logical sense
   - Cross-reference with file system timestamps

### Performance Considerations

- **Index critical properties**: `Note.path`, `Event.timestamp`, `Event.type`
- **Limit traversal depth**: Most queries shouldn't exceed 5 hops
- **Use directional relationships**: Avoid bidirectional when possible
- **Aggregate at query time**: Don't store computed metrics in graph

### Error Handling

- **Graceful degradation**: Fall back to file system when graph unavailable
- **Validation**: Check relationship consistency periodically
- **Conflict resolution**: Latest timestamp wins for contradictions

---

**Document End**

_This knowledge graph patterns guide is maintained by the BMAD Obsidian 2nd Brain expansion pack Phase 2. For temporal query execution, see [[obsidian-technical-guide]]. For Cypher examples, see `examples/neo4j/temporal-queries.cypher`._
