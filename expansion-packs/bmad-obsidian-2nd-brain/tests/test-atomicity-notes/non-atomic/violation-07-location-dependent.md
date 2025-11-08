---
title: Knowledge Management Best Practices
type: unknown
building_block: unknown
created: 2025-11-05T14:00:00Z
tags: [knowledge-management]
atomic_score: 0.25
expected_result: non-atomic
test_category: location_dependent
violations:
  - Location-dependent references ("as mentioned above", "in the previous section")
  - Assumes folder structure context
  - Not self-contained
  - Multiple independent claims
---

# Knowledge Management Best Practices

As mentioned above, the key to effective note-taking is consistency.

In the previous section, we covered the importance of linking. Building on that foundation, bidirectional links create a knowledge graph that reveals unexpected connections.

The parent folder contains related templates. Make sure to reference ../templates/note-template.md when creating new notes.

This approach, combined with the three principles outlined earlier, ensures your knowledge system scales over time.

See the related resources in /resources/knowledge-management/ for more details.

## Expected Test Results

- Single Claim Test: FAIL (multiple claims about note-taking, linking, templates)
- Evidence Test: FAIL (divergent topics)
- Self-Contained Test: FAIL (references "above", "previous section", assumes prior context)
- Title Test: FAIL (too generic)
- Related Concepts Test: FAIL (no actual links, just file path references)
- Building Block Test: FAIL (type unknown)
- Completeness Test: FAIL (references missing context)
- Independence Test: FAIL (depends on document structure and folder location)
- Link Quality Test: FAIL (no wikilinks, uses file paths)
- Metadata Test: PASS
- Expected score: 0.2-0.3 (NON-ATOMIC - critical failure on independence)
- Suggested remediation: Remove location-dependent references, define all concepts inline, convert to wikilinks
