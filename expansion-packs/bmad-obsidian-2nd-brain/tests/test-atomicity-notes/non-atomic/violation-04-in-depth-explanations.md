---
title: Atomic Notes Enable Flexible Linking
type: concept
building_block: concept
created: 2025-11-05T11:15:00Z
tags: [atomicity, linking]
atomic_score: 0.58
expected_result: non-atomic
test_category: in_depth_related_concept_explanations
violations:
  - In-depth explanation of related concepts (bidirectional links explained over multiple paragraphs)
  - Related concept becomes co-equal focus
---

# Atomic Notes Enable Flexible Linking

Atomic notes contain exactly one complete concept, making them ideal building blocks for a knowledge network. Because each note is independent and self-contained, it can be linked to any other note in unlimited ways.

**Bidirectional Linking:**

Bidirectional links are essential to this flexibility. When Note A links to Note B, Note B automatically shows a backlink to Note A without any manual effort. This creates a web of connections that reveals unexpected relationships.

The power of bidirectional linking emerges from the backlink panel. Every note shows not just the links you explicitly created, but also all the notes that link to it. This reverses the traditional one-way hyperlink model from the web.

In practice, bidirectional links enable discovery. You might write Note C about topic X and link to Note B. Later, when reviewing Note B, you see in the backlinks that both Note C and Note D reference it - revealing an implicit connection between C and D that you hadn't noticed before.

Implementation-wise, most modern PKM tools (Obsidian, Roam, LogSeq) support bidirectional links natively. They use `[[WikiLink]]` syntax and automatically maintain the backlink index. Some tools like Obsidian even show an interactive graph view of all connections.

## Expected Test Results

- Single Claim Test: BORDERLINE (main claim about atomic notes + extensive bidirectional links explanation)
- Evidence Test: FAIL (bidirectional links explanation diverges into implementation details, graph views)
- Self-Contained Test: PASS (defines terms)
- Title Test: PASS (descriptive)
- Related Concepts Test: FAIL (explains bidirectional links in 4+ paragraphs instead of linking)
- Expected score: 0.55-0.65 (BORDERLINE/NON-ATOMIC)
- Suggested remediation: Extract bidirectional links explanation into separate note [[Bidirectional Links]], replace with brief link
