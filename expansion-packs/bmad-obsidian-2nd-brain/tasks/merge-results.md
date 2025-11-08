<!-- Powered by BMAD™ Core -->

# merge-results

**Purpose:** Merge query results from multiple sources (Obsidian, Smart Connections, Neo4j), deduplicate, rank by relevance, and detect contradictions

**Performance Budget:** <500ms

## Overview

Query results come from 3 sources:

1. **Smart Connections** - Semantic similarity search (local embeddings)
2. **Obsidian Text Search** - Exact text pattern matching
3. **Neo4j Graphiti** - Temporal and graph relationship queries (optional)

This task merges results while:

- Deduplicating by note path
- Preserving source attribution
- Ranking by relevance
- Detecting contradictions
- Handling partial failures gracefully

## Deduplication Strategy

### Algorithm

```javascript
function deduplicate_results(results) {
  const seen_paths = new Set();
  const deduplicated = [];

  // Sort by relevance first (highest to lowest)
  results.sort((a, b) => b.relevance_score - a.relevance_score);

  for (const result of results) {
    if (!seen_paths.has(result.note_path)) {
      seen_paths.add(result.note_path);
      deduplicated.push(result);
    } else {
      // Merge metadata from duplicate
      const existing = deduplicated.find((r) => r.note_path === result.note_path);
      merge_result_metadata(existing, result);
    }
  }

  return deduplicated;
}
```

### Metadata Merging

When the same note appears in multiple sources, merge their metadata:

```javascript
function merge_result_metadata(existing, duplicate) {
  // Track all sources that found this note
  if (!existing.sources) {
    existing.sources = [existing.source];
  }

  if (!existing.sources.includes(duplicate.source)) {
    existing.sources.push(duplicate.source);
  }

  // Keep highest relevance score
  if (duplicate.relevance_score > existing.relevance_score) {
    existing.relevance_score = duplicate.relevance_score;
    existing.primary_source = duplicate.source;
  }

  // Merge match types
  if (!existing.match_types) {
    existing.match_types = [existing.match_type];
  }

  if (!existing.match_types.includes(duplicate.match_type)) {
    existing.match_types.push(duplicate.match_type);
  }

  // Keep all unique excerpts
  if (!existing.excerpts) {
    existing.excerpts = [existing.excerpt];
  }

  if (duplicate.excerpt && !existing.excerpts.includes(duplicate.excerpt)) {
    existing.excerpts.push(duplicate.excerpt);
  }
}
```

## Relevance Ranking

### Scoring Algorithm

Rank results by composite relevance score:

```javascript
function calculate_composite_relevance(result) {
  let score = result.relevance_score || 0.5;

  // Boost for multiple source agreement
  if (result.sources && result.sources.length > 1) {
    score += 0.1 * (result.sources.length - 1); // +0.1 per additional source
  }

  // Boost for exact text matches
  if (result.match_types && result.match_types.includes('exact_text')) {
    score += 0.1;
  }

  // Boost for semantic matches (high quality)
  if (result.source === 'smart_connections' && result.relevance_score > 0.8) {
    score += 0.05;
  }

  // Boost for MOC notes (high-level overview value)
  if (result.metadata && result.metadata.building_block === 'moc') {
    score += 0.1;
  }

  // Boost for graph-confirmed relationships
  if (result.source === 'neo4j_graphiti') {
    score += 0.08;
  }

  // Clamp to [0.0, 1.0]
  return Math.max(0.0, Math.min(1.0, score));
}

function rank_results(results) {
  // Calculate composite scores
  for (const result of results) {
    result.composite_relevance = calculate_composite_relevance(result);
  }

  // Sort by composite relevance (highest first)
  results.sort((a, b) => b.composite_relevance - a.composite_relevance);

  return results;
}
```

### Relevance Tiers

Group results into relevance tiers for presentation:

```javascript
function categorize_by_relevance(results) {
  const tiers = {
    highly_relevant: [], // score >= 0.8
    relevant: [], // 0.6 <= score < 0.8
    somewhat_relevant: [], // 0.4 <= score < 0.6
    low_relevance: [], // score < 0.4
  };

  for (const result of results) {
    const score = result.composite_relevance;

    if (score >= 0.8) {
      tiers.highly_relevant.push(result);
    } else if (score >= 0.6) {
      tiers.relevant.push(result);
    } else if (score >= 0.4) {
      tiers.somewhat_relevant.push(result);
    } else {
      tiers.low_relevance.push(result);
    }
  }

  return tiers;
}
```

## Contradiction Detection

### Overview

Contradictions occur when results make conflicting claims about the same concept.

**Detection Threshold:** >70% semantic similarity + opposing sentiment/values

### Algorithm

```javascript
async function detect_contradictions(results) {
  const contradictions = [];

  // Compare all pairs of results
  for (let i = 0; i < results.length; i++) {
    for (let j = i + 1; j < results.length; j++) {
      const result_a = results[i];
      const result_b = results[j];

      // Extract claims from excerpts
      const claims_a = extract_claims(result_a.excerpt);
      const claims_b = extract_claims(result_b.excerpt);

      // Compare claims pairwise
      for (const claim_a of claims_a) {
        for (const claim_b of claims_b) {
          const similarity = calculate_semantic_similarity(claim_a, claim_b);

          // Check if claims are about same topic (>70% similar)
          if (similarity > 0.7) {
            // Check if claims contradict each other
            const contradiction_score = detect_opposing_sentiment(claim_a, claim_b);

            if (contradiction_score > 0.7) {
              contradictions.push({
                note_a: {
                  path: result_a.note_path,
                  title: result_a.note_title,
                  claim: claim_a,
                  timestamp: result_a.metadata?.created_date,
                },
                note_b: {
                  path: result_b.note_path,
                  title: result_b.note_title,
                  claim: claim_b,
                  timestamp: result_b.metadata?.created_date,
                },
                confidence: contradiction_score,
                similarity: similarity,
                type: categorize_contradiction_type(claim_a, claim_b),
              });
            }
          }
        }
      }
    }
  }

  return contradictions;
}
```

### Claim Extraction

Extract individual claims from result excerpts:

```javascript
function extract_claims(excerpt) {
  // Split excerpt into sentences
  const sentences = excerpt.split(/[.!?]+/).filter((s) => s.trim().length > 0);

  const claims = [];

  for (const sentence of sentences) {
    const trimmed = sentence.trim();

    // Filter out non-claims
    if (is_claim(trimmed)) {
      claims.push(trimmed);
    }
  }

  return claims;
}

function is_claim(sentence) {
  // A claim makes an assertion about something

  // Exclude questions
  if (sentence.endsWith('?')) {
    return false;
  }

  // Exclude meta-statements ("This note discusses...", "See also...")
  const meta_patterns = [
    /^(this note|this document|see also|references?|sources?)/i,
    /^(i think|i believe|in my opinion)/i, // Opinions are claims but flagged differently
  ];

  for (const pattern of meta_patterns) {
    if (pattern.test(sentence)) {
      return false;
    }
  }

  // Must have a subject and predicate (simplified heuristic)
  const has_subject_predicate =
    /\w+\s+(is|are|was|were|has|have|does|do|can|will|should|must)/i.test(sentence);

  return has_subject_predicate;
}
```

### Semantic Similarity Calculation

Calculate how similar two claims are:

```javascript
async function calculate_semantic_similarity(claim_a, claim_b) {
  // Use Smart Connections embeddings to calculate similarity
  // This is a conceptual example - actual implementation depends on Smart Connections API

  try {
    const similarity = await mcp__smart_connections__calculate_similarity({
      text_a: claim_a,
      text_b: claim_b,
    });

    return similarity;
  } catch (error) {
    // Fallback: Jaccard similarity on word sets
    return jaccard_similarity(claim_a, claim_b);
  }
}

function jaccard_similarity(text_a, text_b) {
  const words_a = new Set(text_a.toLowerCase().split(/\s+/));
  const words_b = new Set(text_b.toLowerCase().split(/\s+/));

  const intersection = new Set([...words_a].filter((w) => words_b.has(w)));
  const union = new Set([...words_a, ...words_b]);

  return intersection.size / union.size;
}
```

### Opposing Sentiment Detection

Detect if two claims contradict each other:

```javascript
function detect_opposing_sentiment(claim_a, claim_b) {
  let contradiction_score = 0.0;

  // Pattern 1: Negation
  // "X is Y" vs "X is not Y"
  if (has_negation(claim_a) !== has_negation(claim_b)) {
    contradiction_score += 0.4;
  }

  // Pattern 2: Opposing adjectives
  // "X is good" vs "X is bad"
  const adjectives_a = extract_adjectives(claim_a);
  const adjectives_b = extract_adjectives(claim_b);

  for (const adj_a of adjectives_a) {
    for (const adj_b of adjectives_b) {
      if (are_antonyms(adj_a, adj_b)) {
        contradiction_score += 0.3;
      }
    }
  }

  // Pattern 3: Conflicting values
  // "X improves Y" vs "X worsens Y"
  const verbs_a = extract_action_verbs(claim_a);
  const verbs_b = extract_action_verbs(claim_b);

  for (const verb_a of verbs_a) {
    for (const verb_b of verbs_b) {
      if (are_opposite_actions(verb_a, verb_b)) {
        contradiction_score += 0.3;
      }
    }
  }

  // Pattern 4: Incompatible values
  // "X is 100" vs "X is 200"
  const numbers_a = extract_numbers(claim_a);
  const numbers_b = extract_numbers(claim_b);

  if (numbers_a.length > 0 && numbers_b.length > 0) {
    // Check if numbers are significantly different
    for (const num_a of numbers_a) {
      for (const num_b of numbers_b) {
        const diff = Math.abs(num_a - num_b);
        const avg = (num_a + num_b) / 2;

        if (avg > 0 && diff / avg > 0.5) {
          // >50% difference
          contradiction_score += 0.2;
        }
      }
    }
  }

  return Math.min(1.0, contradiction_score);
}

function has_negation(text) {
  const negation_words = ['not', 'no', 'never', 'neither', 'nor', "n't", 'cannot'];
  const words = text.toLowerCase().split(/\s+/);

  return negation_words.some((neg) => words.includes(neg));
}

function are_antonyms(word_a, word_b) {
  // Simplified antonym dictionary
  const antonym_pairs = [
    ['good', 'bad'],
    ['improve', 'worsen'],
    ['increase', 'decrease'],
    ['effective', 'ineffective'],
    ['useful', 'useless'],
    ['simple', 'complex'],
    ['fast', 'slow'],
    ['easy', 'difficult'],
  ];

  for (const [ant1, ant2] of antonym_pairs) {
    if ((word_a === ant1 && word_b === ant2) || (word_a === ant2 && word_b === ant1)) {
      return true;
    }
  }

  return false;
}

function are_opposite_actions(verb_a, verb_b) {
  const opposite_pairs = [
    ['improves', 'worsens'],
    ['increases', 'decreases'],
    ['enhances', 'diminishes'],
    ['supports', 'contradicts'],
    ['helps', 'hinders'],
  ];

  for (const [opp1, opp2] of opposite_pairs) {
    if (
      (verb_a.includes(opp1) && verb_b.includes(opp2)) ||
      (verb_a.includes(opp2) && verb_b.includes(opp1))
    ) {
      return true;
    }
  }

  return false;
}

function extract_numbers(text) {
  const number_pattern = /\b\d+(\.\d+)?\b/g;
  const matches = text.match(number_pattern);

  return matches ? matches.map((n) => parseFloat(n)) : [];
}

// Helper functions for NLP (simplified implementations)
function extract_adjectives(text) {
  // Simplified: Look for common adjective patterns
  const adjective_pattern =
    /\b(good|bad|effective|useful|simple|complex|fast|slow|easy|difficult|important|trivial)\b/gi;
  const matches = text.match(adjective_pattern);

  return matches ? matches.map((m) => m.toLowerCase()) : [];
}

function extract_action_verbs(text) {
  const verb_pattern =
    /\b(improves?|worsens?|increases?|decreases?|enhances?|diminishes?|supports?|contradicts?|helps?|hinders?)\b/gi;
  const matches = text.match(verb_pattern);

  return matches ? matches.map((m) => m.toLowerCase()) : [];
}
```

### Contradiction Types

Categorize detected contradictions:

```javascript
function categorize_contradiction_type(claim_a, claim_b) {
  if (has_negation(claim_a) !== has_negation(claim_b)) {
    return 'negation'; // Direct negation: "X is Y" vs "X is not Y"
  }

  if (extract_numbers(claim_a).length > 0 && extract_numbers(claim_b).length > 0) {
    return 'conflicting_values'; // Incompatible numbers
  }

  const adj_a = extract_adjectives(claim_a);
  const adj_b = extract_adjectives(claim_b);

  for (const a of adj_a) {
    for (const b of adj_b) {
      if (are_antonyms(a, b)) {
        return 'opposing_sentiment'; // Antonym adjectives
      }
    }
  }

  return 'semantic_conflict'; // General semantic contradiction
}
```

## Handling Partial Failures

When some sources fail, merge available results gracefully:

```javascript
function merge_with_partial_failures(source_results, source_errors) {
  const merged_results = [];
  const warnings = [];

  // Collect successful results
  for (const [source_name, results] of Object.entries(source_results)) {
    if (results && results.length > 0) {
      merged_results.push(...results);
    }
  }

  // Generate warnings for failed sources
  for (const [source_name, error] of Object.entries(source_errors)) {
    warnings.push({
      source: source_name,
      error: error.message,
      impact: describe_source_impact(source_name),
    });
  }

  // If ALL sources failed, throw error
  if (merged_results.length === 0) {
    throw QueryExecutionError(
      'All data sources failed. Please check:\n' +
        warnings.map((w) => `- ${w.source}: ${w.error}`).join('\n'),
    );
  }

  return {
    results: merged_results,
    warnings: warnings,
    sources_available: Object.keys(source_results),
    sources_failed: Object.keys(source_errors),
  };
}

function describe_source_impact(source_name) {
  const impacts = {
    smart_connections: 'Semantic similarity search unavailable. Results may be less relevant.',
    obsidian_text_search: 'Exact text matching unavailable. Results may miss direct mentions.',
    neo4j_graphiti: 'Temporal and graph queries unavailable. Relationship context limited.',
  };

  return impacts[source_name] || 'Unknown impact';
}
```

## Result Structure

Return merged and deduplicated results:

```yaml
merged_results:
  results:
    - note_path: 'atomic/zettelkasten-definition.md'
      note_title: 'Zettelkasten Method Definition'
      relevance_score: 0.87
      composite_relevance: 0.95 # Boosted by multiple sources
      sources: ['smart_connections', 'obsidian_text_search']
      primary_source: 'smart_connections'
      match_types: ['semantic', 'exact_text']
      excerpts:
        - 'Zettelkasten is a method of knowledge management using atomic notes...'
        - '...comparing Zettelkasten with PARA method...'
      metadata:
        created_date: '2024-03-15T10:23:00Z'
        modified_date: '2024-10-12T14:45:00Z'
        building_block: 'concept'

  contradictions:
    - note_a:
        path: 'atomic/atomic-notes-improve-recall.md'
        title: 'Atomic Notes Improve Recall'
        claim: 'Atomic notes significantly improve long-term recall'
        timestamp: '2024-05-20T14:30:00Z'
      note_b:
        path: 'literature/critique-of-zettelkasten.md'
        title: 'Critique of Zettelkasten'
        claim: 'Atomic notes do not improve recall compared to traditional notes'
        timestamp: '2024-08-15T09:00:00Z'
      confidence: 0.78
      similarity: 0.85
      type: 'negation'

  query_metadata:
    total_results: 15
    deduplicated_results: 12
    sources_available: ['smart_connections', 'obsidian_text_search', 'neo4j_graphiti']
    sources_failed: []
    contradictions_detected: 1
    merge_duration_ms: 320

  warnings: [] # Empty if all sources succeeded
```

## Performance Budget

- Deduplication: <50ms
- Relevance ranking: <100ms
- Contradiction detection: <300ms
- Metadata merging: <50ms
- **Total: <500ms**

## Testing

Validate result merging:

```
Test 1: Deduplicate results from multiple sources
Input: 10 results with 3 duplicates (same note_path)
Expected: 7 unique results, metadata merged, sources tracked

Test 2: Rank by composite relevance
Input: Results with varying scores and source agreement
Expected: Sorted by composite score, boosted for multiple sources

Test 3: Detect contradiction
Input: Two results with contradictory claims (>70% similarity, opposing sentiment)
Expected: Contradiction flagged with confidence >0.7

Test 4: Handle partial failure
Input: Smart Connections failed, Obsidian succeeded
Expected: Results from Obsidian only, warning about Smart Connections

Test 5: All sources failed
Input: All sources return errors
Expected: QueryExecutionError with actionable advice

Test 6: No contradictions
Input: Results with consistent claims
Expected: contradictions = [], no false positives
```
