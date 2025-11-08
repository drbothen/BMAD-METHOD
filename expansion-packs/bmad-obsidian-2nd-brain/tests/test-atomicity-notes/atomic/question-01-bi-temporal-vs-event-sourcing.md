---
title: How does bi-temporal versioning differ from event sourcing in handling data history?
type: question
building_block: question
created: 2025-11-05T10:15:00Z
tags: [databases, architecture, temporal-data, open-question]
atomic_score: 0.88
expected_result: atomic
test_category: question
---

# How does bi-temporal versioning differ from event sourcing in handling data history?

Both bi-temporal versioning and event sourcing preserve historical data, but they approach the problem from different angles. What are the key architectural differences, and when should each be used?

**Context:**

- Bi-temporal databases track two timelines: valid time (when facts were true in reality) and transaction time (when facts were recorded in the database)
- Event sourcing stores all changes as immutable events, allowing reconstruction of any past state
- Both patterns address similar needs: auditability, time-travel queries, and data lineage

**Significance:**
Understanding the distinction is critical for choosing the right pattern for systems requiring historical data tracking. The wrong choice can lead to unnecessary complexity or inability to answer certain temporal queries.

**Sub-questions to explore:**

- Can bi-temporal modeling be implemented using event sourcing as the storage mechanism?
- How do query patterns differ between the two approaches?
- What are the performance implications of each pattern at scale?

## Test Validation Criteria

- ✓ Single claim: One focused question
- ✓ Evidence: Context establishes significance without introducing new claims
- ✓ Self-contained: Defines both concepts briefly
- ✓ Title: Interrogative, specific, clear
- ✓ Related concepts: Mentioned but not explained in depth
- Expected score: >= 0.85
