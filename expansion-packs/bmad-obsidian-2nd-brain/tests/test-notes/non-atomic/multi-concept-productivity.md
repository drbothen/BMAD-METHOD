---
title: Notes on Productivity
created: 2025-11-05T11:00:00Z
tags: [productivity]
---

# Notes on Productivity

Zettelkasten uses atomic notes. Each note should contain exactly one complete idea that can stand alone. This enables flexible recombination and prevents note bloat.

GTD uses context lists to organize next actions. Context lists group actions by location or tool needed (e.g., @computer, @phone, @errands). This reduces cognitive overhead when deciding what to do next.

The PARA method organizes information into Projects, Areas, Resources, and Archives. Projects are active work with deadlines. Areas are ongoing responsibilities. Resources are reference material. Archives are inactive items.

Time blocking is a scheduling technique where you divide your day into blocks of time. Each block is dedicated to a specific task or activity. This prevents context switching and improves focus.

Deep work requires eliminating distractions. Turn off notifications, close unnecessary tabs, and work in a quiet environment. Schedule deep work blocks during your peak energy hours.

## Test Expectations

**Expected atomicity analysis:**

- is_atomic: false
- score: <= 0.3
- building_block_type: concept (first detected concept)
- violations: ["Multiple independent claims detected", "Divergent supporting evidence"]
- verdict: NON-ATOMIC

**Reasoning:**

- Single claim: FAIL - 5 independent claims (Zettelkasten, GTD, PARA, time blocking, deep work) → score: 1.0 - 0.3\*4 = -0.2 → 0.0 ✗
- Evidence: FAIL - Each concept introduces new topic ✗
- Self-contained: PASS - Terms mostly defined ✓
- Title: FAIL - Too generic "Notes on Productivity" ✗
- Related concepts: N/A

**Expected fragmentation:**
Should fragment into 5 atomic notes:

1. "Zettelkasten Principle - Atomicity" (concept)
2. "GTD Context Lists" (concept)
3. "PARA Method for Information Organization" (model)
4. "Time Blocking Technique" (concept)
5. "Deep Work Distraction Elimination" (concept)
