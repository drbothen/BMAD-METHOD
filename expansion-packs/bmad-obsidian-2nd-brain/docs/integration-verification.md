<!-- Powered by BMAD™ Core -->

# Integration Verification Guide - Semantic Linker Agent

Guide for verifying successful integration of the Semantic Linker Agent into the bmad-obsidian-2nd-brain expansion pack.

## Prerequisites

Before starting verification:

1. **Environment Setup:**
   - Obsidian installed with test vault
   - Smart Connections plugin installed and configured
   - Claude Desktop or VS Code with Claude Code extension
   - MCP Tools configured:
     - Smart Connections MCP server
     - Obsidian MCP server
     - Graphiti Neo4j MCP server (optional)

2. **Test Vault Contents:**
   - Minimum 20 atomic notes created using Structural Analysis Agent (STORY-003)
   - Mix of building block types (concept, argument, phenomenon, model, question, claim)
   - Notes with frontmatter metadata (building_block, tags, created, moc)

3. **Configuration Files:**
   - `expansion-packs/bmad-obsidian-2nd-brain/config.yaml` created
   - Neo4j settings configured (if using Neo4j)
   - `.bmad-obsidian-2nd-brain/` directory created for feedback storage

## Agent Activation Verification

### Step 1: Activate Agent

**Command:**

```
/bmad-2b:semantic-linker-agent
```

**Expected Output:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 Semantic Linker Agent Activated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hello! I'm Connector, your relationship discovery specialist.

I help you discover semantic relationships between atomic notes and create bidirectional links using Smart Connections semantic search.

Focus areas:
- Semantic discovery (similarity >= 0.6)
- Relationship typing (7 types: supports, contradicts, elaborates, analogous_to, generalizes, specializes, influences)
- Link strength calculation (semantic + contextual + temporal)
- Bidirectional linking with context
- Feedback learning

Run *help to see all available commands.
```

**Verification Checklist:**

- [ ] Agent activates without errors
- [ ] Greeting message displayed
- [ ] Agent persona "Connector" mentioned
- [ ] Focus areas listed
- [ ] \*help command mentioned

### Step 2: Verify Command List

**Command:**

```
*help
```

**Expected Output:**

```
Available Commands:

1. *suggest-links {note_path} - Find related notes and suggest links
2. *create-links {source} {targets...} - Bulk create bidirectional links
3. *create-link {source} {target} {type} - Create single link with type
4. *review-suggestions - Show pending link suggestions
5. *accept-suggestion {id} - Accept and create suggested link
6. *reject-suggestion {id} {reason} - Reject with reason
7. *analyze-graph {note_path} - Show graph metrics and patterns
8. *batch-approve {threshold} - Auto-approve suggestions above threshold
9. *yolo - Toggle auto-approve mode (use with caution)
10. *exit - Exit agent mode

Workflows:
- Basic: *suggest-links → *review-suggestions → *accept-suggestion
- Bulk: *suggest-links → *batch-approve 0.8
- Manual: *create-link source.md target.md supports
- Analysis: *analyze-graph note.md
```

**Verification Checklist:**

- [ ] All 11 commands listed (including \*help)
- [ ] Each command has description and parameters
- [ ] Example workflows provided
- [ ] Examples show correct syntax

## Workflow Verification

### Workflow 1: Basic Flow (Suggest → Review → Accept)

**Objective:** Verify end-to-end semantic linking workflow

**Steps:**

1. **Generate Suggestions:**

   ```
   *suggest-links atomic/argument-01-spaced-repetition.md
   ```

   **Expected:**
   - Smart Connections query executes
   - 5+ related notes returned (similarity >= 0.6)
   - Suggestions sorted by strength
   - Each shows: ID, target title, link type, strength, confidence, context preview

2. **Review Suggestions:**

   ```
   *review-suggestions
   ```

   **Expected:**
   - All pending suggestions displayed
   - Full details: type, strength, forward/backward contexts, reasoning, shared concepts
   - Actions listed: *accept-suggestion, *reject-suggestion

3. **Accept Suggestion:**

   ```
   *accept-suggestion abc123
   ```

   **Expected:**
   - Bidirectional link created in both notes
   - Context sentences present in both directions
   - Neo4j relationship created (if enabled) or skipped gracefully (if disabled)
   - Feedback recorded
   - Learning stats shown

**Verification Checklist:**

- [ ] Smart Connections returns results
- [ ] Link types identified correctly
- [ ] Strength scores calculated (0.0-1.0 range)
- [ ] Bidirectional links created
- [ ] Context sentences meaningful
- [ ] Neo4j integration works (if enabled)
- [ ] Feedback learning active

### Workflow 2: Bulk Approval (Suggest → Batch Approve)

**Objective:** Verify batch processing of strong suggestions

**Steps:**

1. **Generate Suggestions:**

   ```
   *suggest-links atomic/phenomenon-01-forgetting-curve.md
   ```

2. **Batch Approve (High Threshold):**

   ```
   *batch-approve 0.8
   ```

   **Expected:**
   - Suggestions filtered (only >= 0.8 strength shown)
   - Preview displayed with count
   - User confirmation requested
   - All approved links created in batch
   - Summary with success/failure count

**Verification Checklist:**

- [ ] Filtering by threshold works
- [ ] Confirmation prompt appears
- [ ] Batch creation successful
- [ ] All feedback logged
- [ ] Summary accurate

### Workflow 3: Manual Linking (Create Link)

**Objective:** Verify manual link creation without semantic search

**Steps:**

1. **Create Single Link:**

   ```
   *create-link atomic/note-a.md atomic/note-b.md supports
   ```

   **Expected:**
   - Link type validated (one of 7 valid types)
   - Strength calculated
   - Context prompted or auto-generated
   - Bidirectional link created
   - Neo4j relationship created (if enabled)

**Verification Checklist:**

- [ ] Link type validation works
- [ ] Strength calculation accurate
- [ ] Context generation functional
- [ ] Link created successfully

### Workflow 4: Bulk Creation (Create Links)

**Objective:** Verify bulk link creation with multiple targets

**Steps:**

1. **Create Multiple Links:**

   ```
   *create-links atomic/note-a.md atomic/note-b.md atomic/note-c.md atomic/note-d.md
   ```

   **Expected:**
   - All 3 target links analyzed
   - Types and strengths calculated
   - Confirmation requested
   - All links created if confirmed

**Verification Checklist:**

- [ ] Multiple targets processed
- [ ] Confirmation shown
- [ ] Batch creation works

### Workflow 5: Graph Analysis

**Objective:** Verify graph metrics and connection patterns

**Steps:**

1. **Analyze Note Graph:**

   ```
   *analyze-graph atomic/argument-01-spaced-repetition.md
   ```

   **Expected:**
   - Node metrics: degree centrality, clustering coefficient
   - Relationship type distribution
   - Strength distribution
   - Connected notes listed (in/out)
   - Suggestions for improvement

**Verification Checklist:**

- [ ] Metrics calculated accurately
- [ ] Type distribution shown
- [ ] Strength distribution shown
- [ ] Connected notes listed
- [ ] Actionable suggestions provided

## Acceptance Criteria Verification

Map integration tests to STORY-004 acceptance criteria:

### AC1: Agent Activation with All Commands

**Test:**

- Activate agent: `/bmad-2b:semantic-linker-agent`
- Run: `*help`

**Verify:**

- [ ] Agent activates successfully
- [ ] All 11 commands available
- [ ] No activation errors

### AC2: Smart Connections Semantic Search

**Test:**

- Run: `*suggest-links atomic/test-note.md`

**Verify:**

- [ ] Smart Connections MCP called
- [ ] Related notes returned (similarity >= 0.6)
- [ ] Results sorted by similarity
- [ ] No duplicates or self-references

### AC3: Relationship Type Identification

**Test:**

- Generate suggestions for various note pairs
- Verify all 7 types identified:
  - supports (phenomenon → argument)
  - contradicts (conflicting claims)
  - elaborates (concept explaining concept)
  - analogous_to (similar patterns)
  - generalizes (abstract principle)
  - specializes (specific instance)
  - influences (temporal precedence)

**Verify:**

- [ ] All 7 types can be identified
- [ ] Confidence scores >= 0.7 for clear relationships
- [ ] Temporal precedence enforced for influences
- [ ] Building block patterns recognized

### AC4: Link Strength Calculation

**Test:**

- Review suggestions with various strengths
- Verify 3-component formula:
  - Semantic similarity (50%)
  - Contextual relevance (30%)
  - Temporal proximity (20%)

**Verify:**

- [ ] Strength scores in [0.0, 1.0] range
- [ ] Classification: strong (>= 0.7), medium (0.5-0.7), weak (< 0.5)
- [ ] Components calculated correctly
- [ ] Formula applied correctly

### AC5: Bidirectional Wikilinks with Context

**Test:**

- Accept suggestion or create manual link
- Check both source and target notes

**Verify:**

- [ ] Wikilink in source: `- [[Target]] - context forward`
- [ ] Wikilink in target: `- [[Source]] - context backward`
- [ ] Context sentences explain relationship
- [ ] Links in "Related Concepts" section

### AC6: Neo4j Relationship Creation

**Test (Neo4j Enabled):**

- Accept suggestion
- Check Neo4j database

**Verify:**

- [ ] [:CONCEPTUALLY_RELATED] relationship created
- [ ] Bi-temporal metadata present:
  - valid_time_start (discovery time)
  - transaction_time (record time)
- [ ] Parameterized query used (no injection)
- [ ] Relationship metadata: link_id, link_type, strength, context

**Test (Neo4j Disabled):**

- Set config.yaml: `neo4j.enabled: false`
- Accept suggestion

**Verify:**

- [ ] Neo4j gracefully skipped
- [ ] Obsidian link still created
- [ ] No errors thrown
- [ ] User informed of skip

### AC7: Pending Suggestions Review & Approval

**Test:**

- Generate suggestions
- Review with `*review-suggestions`
- Accept with `*accept-suggestion abc123`
- Reject with `*reject-suggestion def456 "irrelevant"`

**Verify:**

- [ ] Pending suggestions tracked
- [ ] Full details in review
- [ ] Accept creates link and records feedback
- [ ] Reject records reason and updates learning

### AC8: Circular Reasoning Prevention

**Test:**

- Create: A supports B
- Create: B supports C
- Attempt: C supports A

**Verify:**

- [ ] Cycle detected
- [ ] Link rejected
- [ ] Error message shows chain path
- [ ] Only applies to reasoning types (supports, contradicts, generalizes, specializes)

### AC9: Feedback Learning

**Test:**

- Generate 25 suggestions
- Accept 12, reject 13 (48% acceptance)
- Check learning update

**Verify:**

- [ ] Feedback recorded in `.bmad-obsidian-2nd-brain/link-feedback.json`
- [ ] Threshold adjusted after >= 20 decisions:
  - Low acceptance (< 60%) → threshold raised
  - High acceptance (> 90%) → threshold lowered
- [ ] Type statistics updated
- [ ] Rejection filters applied

### AC10: Security Validation

**Test:**

1. Directory Traversal: `*create-link ../../etc/passwd atomic/note-b.md supports`
2. Cypher Injection: Context with `"}]->(n) MATCH (secret:Note) RETURN secret //`
3. Link Spam: Add 51st link to note with 50 links
4. Link-to-Self: `*create-link atomic/note-a.md atomic/note-a.md supports`

**Verify:**

- [ ] Directory traversal blocked
- [ ] Cypher injection prevented (parameterized queries)
- [ ] Link spam limit enforced (max 50 per note)
- [ ] Link-to-self prevented
- [ ] Duplicate links detected
- [ ] All security checks pass

## Dependency Files Verification

Verify all created files exist and are functional:

### Templates

- [ ] `templates/link-suggestion-tmpl.yaml`
  - [ ] 27 variables defined
  - [ ] 7 sections present
  - [ ] 3 examples provided

- [ ] `templates/relationship-record-tmpl.yaml`
  - [ ] Cypher query template present
  - [ ] Parameterized query (no string concatenation)
  - [ ] Bi-temporal metadata included
  - [ ] 7 examples (one per type)

### Checklists

- [ ] `checklists/linking-quality-checklist.md`
  - [ ] 11 quality criteria
  - [ ] Scoring algorithm defined
  - [ ] Pass/fail criteria (score >= 0.7)
  - [ ] Security test (Test 11) comprehensive

- [ ] `checklists/relationship-confidence-checklist.md`
  - [ ] 8 confidence criteria
  - [ ] Link type confidence >= 0.7 required
  - [ ] Strength classification validated

### Data Files

- [ ] `data/connection-patterns.md`
  - [ ] All 7 relationship types documented
  - [ ] Definitions, characteristics, signals, examples
  - [ ] Decision tree included
  - [ ] Anti-patterns listed

- [ ] `data/relationship-types.md`
  - [ ] Formal taxonomy with symbols
  - [ ] Bidirectional implications
  - [ ] Type selection flowchart
  - [ ] Valid/invalid combinations

- [ ] `data/security-guidelines.md`
  - [ ] Input validation guidelines
  - [ ] Cypher injection prevention
  - [ ] Path sanitization
  - [ ] Circular reasoning detection
  - [ ] Privacy guidelines
  - [ ] Attack scenarios & defenses

### Task Files

- [ ] `tasks/query-semantic-similarity.md`
  - [ ] Smart Connections MCP integration
  - [ ] Input validation (Step 1)
  - [ ] Graceful degradation
  - [ ] Error handling with retries

- [ ] `tasks/identify-concept-overlap.md`
  - [ ] 10-step procedure
  - [ ] Linguistic signal detection
  - [ ] Temporal ordering verification
  - [ ] Confidence calculation
  - [ ] Fallback logic

- [ ] `tasks/rate-connection-strength.md`
  - [ ] 3-component formula
  - [ ] Semantic similarity (50%)
  - [ ] Contextual relevance (30%)
  - [ ] Temporal proximity (20%)
  - [ ] Classification logic

- [ ] `tasks/create-bidirectional-link.md`
  - [ ] 8-step procedure
  - [ ] Duplicate detection
  - [ ] Link-to-self prevention
  - [ ] Rollback mechanism
  - [ ] Verification step

- [ ] `tasks/create-neo4j-relationship.md`
  - [ ] Config check
  - [ ] Parameterized Cypher query
  - [ ] Bi-temporal metadata
  - [ ] Graceful degradation
  - [ ] Error handling

- [ ] `tasks/learn-from-feedback.md`
  - [ ] 8-step procedure
  - [ ] Local storage (`.bmad-obsidian-2nd-brain/link-feedback.json`)
  - [ ] Threshold adjustment logic
  - [ ] Rejection filter building
  - [ ] Privacy-preserving

### Agent File

- [ ] `agents/semantic-linker-agent.md`
  - [ ] BMAD header present
  - [ ] YAML metadata block complete
  - [ ] All 11 commands defined
  - [ ] All 12 dependencies listed
  - [ ] Startup Context section
  - [ ] Command implementations with algorithms
  - [ ] Relationship type classification (7 types)
  - [ ] Link strength algorithm
  - [ ] Feedback learning algorithm
  - [ ] Security considerations

### Tests

- [ ] `tests/semantic-linker-test-plan.md`
  - [ ] 67 test cases defined
  - [ ] 10 test categories
  - [ ] Acceptance criteria mapped to tests
  - [ ] Test execution checklist

### Documentation

- [ ] `docs/integration-verification.md` (this file)
  - [ ] Agent activation guide
  - [ ] Workflow verification
  - [ ] Acceptance criteria verification
  - [ ] Dependency files checklist

## File Count Summary

**Total Files Created:** 16

- **Templates:** 2
- **Checklists:** 2
- **Data:** 3 (including security-guidelines.md)
- **Tasks:** 6
- **Agents:** 1
- **Tests:** 1
- **Docs:** 1

## Integration Test Report Template

Use this template to document integration test results:

```markdown
# Semantic Linker Agent - Integration Test Report

**Date:** YYYY-MM-DD
**Tester:** [Name]
**Environment:** [Claude Desktop / VS Code / Cursor]
**Vault:** [Test vault name]

## Agent Activation

- [ ] Agent activated successfully
- [ ] All 11 commands available
- [ ] Greeting message displayed

## Workflow Tests

### Workflow 1: Basic Flow

- [ ] Suggestions generated
- [ ] Review functional
- [ ] Accept created link
- **Result:** PASS / FAIL
- **Notes:** [Any issues]

### Workflow 2: Bulk Approval

- [ ] Batch filtering works
- [ ] Confirmation prompt shown
- [ ] Links created successfully
- **Result:** PASS / FAIL
- **Notes:** [Any issues]

[... continue for all workflows ...]

## Acceptance Criteria

- [ ] AC1: Agent Activation ✓
- [ ] AC2: Smart Connections ✓
- [ ] AC3: Relationship Types ✓
- [ ] AC4: Link Strength ✓
- [ ] AC5: Bidirectional Links ✓
- [ ] AC6: Neo4j Integration ✓
- [ ] AC7: Suggestions Review ✓
- [ ] AC8: Circular Reasoning ✓
- [ ] AC9: Feedback Learning ✓
- [ ] AC10: Security ✓

**All AC Met:** [ ] Yes [ ] No

## Issues Found

| Issue | Severity | Description   | Status     |
| ----- | -------- | ------------- | ---------- |
| #1    | Critical | [Description] | Open/Fixed |
| #2    | Major    | [Description] | Open/Fixed |

## Overall Result

**PASS** [ ] **FAIL** [ ] **PASS WITH ISSUES** [ ]

**Summary:** [Brief summary of integration test results]
```

## Next Steps After Verification

Once integration verification is complete:

1. **Update README.md:**
   - Add Semantic Linker Agent to agent list
   - Document commands and workflows
   - Add usage examples

2. **Update CHANGELOG.md:**
   - Add entry for STORY-004 completion
   - List all new files created
   - Document new features

3. **Update Expansion Pack README:**
   - Document complete agent workflow:
     1. Inbox Triage Agent (STORY-002)
     2. Structural Analysis Agent (STORY-003)
     3. Semantic Linker Agent (STORY-004)

4. **Build and Distribute:**
   - Run: `npm run build`
   - Verify dist/ outputs
   - Test installation: `npx bmad-method install`

5. **User Documentation:**
   - Create user guide for semantic linking
   - Add troubleshooting section
   - Document MCP setup requirements

## Troubleshooting

### Smart Connections Not Available

**Symptom:** "Smart Connections MCP not available"

**Solution:**

1. Install Smart Connections plugin in Obsidian
2. Configure MCP server in Claude Desktop/VS Code settings
3. Restart IDE/Claude Desktop
4. Verify connection with test query

### Neo4j Connection Failed

**Symptom:** "Neo4j connection failed"

**Solution:**

1. Check `config.yaml` for correct Neo4j settings
2. Verify Neo4j server is running: `docker ps` or `systemctl status neo4j`
3. Test connection with Cypher query: `MATCH (n) RETURN count(n)`
4. If optional, disable in config: `neo4j.enabled: false`

### Links Not Bidirectional

**Symptom:** Link only appears in one note

**Solution:**

1. Check for rollback messages in output
2. Verify both notes are writable (not read-only)
3. Check for file permission errors
4. Review rollback logs

### Feedback Learning Not Triggering

**Symptom:** Threshold not adjusting after 20+ decisions

**Solution:**

1. Check `.bmad-obsidian-2nd-brain/link-feedback.json` exists
2. Verify feedback entries recorded correctly
3. Check decision count: need >= 20 total (approved + rejected)
4. Deferred decisions don't count toward threshold adjustment

## References

- **STORY-004:** `/Users/jmagady/Dev/BMAD-METHOD/manuscripts/stories/obsidian-2nd-brain/STORY-004-semantic-linker-agent.yaml`
- **Agent File:** `expansion-packs/bmad-obsidian-2nd-brain/agents/semantic-linker-agent.md`
- **Test Plan:** `expansion-packs/bmad-obsidian-2nd-brain/tests/semantic-linker-test-plan.md`
- **Security Guidelines:** `expansion-packs/bmad-obsidian-2nd-brain/data/security-guidelines.md`
