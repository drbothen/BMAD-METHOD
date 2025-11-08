---
title: Spaced Repetition for Learning
type: concept
building_block: concept
created: 2025-11-05T11:05:00Z
tags: [learning, spaced-repetition]
atomic_score: 0.48
expected_result: non-atomic
test_category: divergent_supporting_evidence
violations:
  - Divergent supporting evidence introduces new topics
  - Tool comparison becomes separate topic
---

# Spaced Repetition for Learning

Spaced repetition is a learning technique that schedules reviews at increasing intervals to improve long-term retention. The technique leverages the Ebbinghaus forgetting curve, which shows that memory decays exponentially without reinforcement.

**Implementation Tools:**

Anki is better than SuperMemo for implementing spaced repetition. Anki has a more intuitive interface and better mobile apps, though SuperMemo's algorithm is more sophisticated. Anki was created in 2006 by Damien Elmes as an open-source alternative.

SuperMemo was the original SRS software, created in 1987 by Piotr Wozniak. It introduced the SM-2 algorithm which many other systems have adopted or modified.

Anki uses a modified version of SM-2 that adjusts interval calculations based on user performance. The algorithm has been refined through millions of user reviews.

## Expected Test Results

- Single Claim Test: FAIL (main claim about spaced repetition + tool comparison is separate claim)
- Evidence Test: FAIL (tool comparison introduces new topics: software history, algorithm details, interface design)
- Self-Contained Test: PASS (defines terms)
- Title Test: PASS (descriptive)
- Related Concepts Test: FAIL (explains Anki/SuperMemo in depth instead of linking)
- Expected score: 0.45-0.55 (NON-ATOMIC)
- Suggested remediation: Extract tool comparison into separate note, link instead of explaining
