<!-- Powered by BMAD™ Core -->

# Apply Tone Patterns (Brownfield)

---

task:
id: apply-tone-patterns
name: Apply Extracted Tone Patterns to New Content
description: Apply previously extracted tone patterns to new chapters or updated sections in existing books to maintain consistency
persona_default: tutorial-architect
inputs: - extracted-tone-patterns.md (from extract-tone-patterns task) - new-chapter-draft (or updated section)
steps: - Load extracted-tone-patterns.md - Review tone profile and key patterns - Load new/updated chapter draft - Validate voice characteristics match patterns - Check formality consistency - Apply common phrase patterns to transitions/introductions - Align code comment style with patterns - Apply personality markers appropriately - Verify no anti-patterns present - Document tone adjustments made
output: Tone-aligned chapter draft
use_case: brownfield

---

## Purpose

Apply tone and voice patterns extracted from existing book chapters to new content (2nd edition chapters, added sections, updated examples) to ensure consistency with the established book voice. This maintains reader experience across editions and prevents jarring tone shifts between original and new content.

## When to Use

**Use this task when:**

- Writing new chapters for 2nd/3rd/4th edition
- Adding sections to existing chapters in updated edition
- Updating code examples while maintaining original commentary style
- Multiple authors contributing to edition update (need consistency)
- Replacing outdated content with new material (same tone)
- Expanding book with bonus chapters matching original voice

**Use during:**

- Initial chapter drafting (with expand-outline-to-draft task)
- Copy editing phase (with copy-edit-chapter task)
- Technical review corrections (maintaining tone while fixing technical issues)

**Do NOT use for:**

- New books from scratch (use define-book-tone.md instead)
- Books where you intentionally want to CHANGE tone for new edition
- Minor typo fixes or technical corrections (tone already correct)

## Prerequisites

Before starting this task:

- **extracted-tone-patterns.md exists** - Run extract-tone-patterns.md task first if not available
- **New content drafted** - Have initial draft of new chapter/section
- **Patterns are current** - Extracted patterns reflect most recent edition
- **Authority to modify** - You have permission to edit the draft

## Workflow Steps

### 1. Load and Review Extracted Tone Patterns

**Load extracted-tone-patterns.md:**

Read the complete tone patterns document before making any changes.

**Key Sections to Internalize:**

1. **Voice Profile** - Perspective (first/second/third person), active/passive ratios
2. **Formality Level** - Level 1-5, contraction usage, vocabulary complexity
3. **Common Phrases** - Introduction patterns, transitions, conclusions
4. **Code Comment Style** - Density, tone, purpose
5. **Author Personality Markers** - Humor style, encouragement approach, directness
6. **Anti-Patterns** - What to avoid

**Create Application Checklist:**

Based on extracted patterns, identify what to check:

```markdown
**My Application Checklist for This Chapter:**

Voice:

- [ ] Use second person ("You'll implement...")
- [ ] ~85% active voice, passive only for system actions
- [ ] No first person singular ("I think")

Formality:

- [ ] Level 3 (Professional/Conversational)
- [ ] ~13 contractions per 1000 words
- [ ] Use "Let's" for collaborative actions

Phrases:

- [ ] Chapter intro: "In this chapter, you'll [action]. By the end, you'll [outcome]."
- [ ] Theory to practice: "Let's put this into practice"
- [ ] Transitions: "Building on this..."

Code Comments:

- [ ] 1 comment per 3-4 lines
- [ ] Explain "why", not "what" (unless syntax unusual)
- [ ] Match Level 3 formality

Personality:

- [ ] Light technical humor (1-2 instances per chapter)
- [ ] Matter-of-fact encouragement at milestones
- [ ] Share real-world experience

Avoid:

- [ ] No "Obviously", "clearly", "simply"
- [ ] No marketing hype or superlatives
- [ ] No excessive formality or academic voice
```

### 2. Read New Draft for Tone Assessment

**First Read - Tone Only:**

Read your new draft IGNORING technical accuracy. Focus solely on tone:

- Does this sound like the same author/book?
- What formality level does this feel like?
- Are contractions used similarly?
- Do transitions match extracted patterns?
- Do code comments sound consistent?

**Identify Tone Mismatches:**

Document specific sections where tone doesn't match patterns:

```markdown
**Tone Mismatches Found:**

Section: "Understanding Service Mesh" (Lines 45-67)
Issue: Formality Level 5 (too formal)
Evidence: "One must configure the service mesh prior to deployment" (no contractions, passive voice)
Pattern: Should be Level 3: "You'll need to configure the service mesh before deployment"

Section: Code Example (Lines 120-145)
Issue: Code comments too terse
Evidence: Only 2 comments for 25 lines of code
Pattern: Should have ~8 comments (1 per 3-4 lines)

Section: Chapter Conclusion (Lines 450-470)
Issue: Missing encouragement pattern
Evidence: Just summarizes topics, no forward-looking statement
Pattern: Should end with "You now have [skill]. In the next chapter, we'll [future topic]."
```

### 3. Align Voice Characteristics

**Perspective Consistency:**

Ensure pronouns match extracted patterns:

**Example - Correcting Perspective:**

```markdown
**Original Draft (Mixed Perspective):**
"One should configure the authentication service. You'll need to specify the credentials. The developer implements token validation."

**Pattern:** Second person throughout

**Corrected:**
"You'll configure the authentication service. You'll need to specify the credentials. You'll implement token validation."
```

**Active vs. Passive Voice:**

Adjust voice construction to match pattern ratios:

**Example - Activating Passive Constructions:**

```markdown
**Original Draft (Excessive Passive):**
"The configuration file should be edited. The service is then deployed by Kubernetes. The logs can be viewed using kubectl."

**Pattern:** ~85% active voice

**Corrected:**
"Edit the configuration file. Kubernetes then deploys the service. View the logs using kubectl."
```

### 4. Adjust Formality Level

**Contraction Alignment:**

Match contraction frequency to extracted patterns:

**Example - Level 3 Pattern (Moderate Contractions):**

```markdown
**Original Draft (Level 5 - No Contractions):**
"We will examine the authentication flow. You will implement token validation. Do not store credentials in code."

**Pattern:** Level 3 with ~13 contractions per 1000 words

**Corrected:**
"We'll examine the authentication flow. You'll implement token validation. Don't store credentials in code."
```

**Vocabulary Adjustment:**

Match technical vocabulary style:

```markdown
**Original Draft (Overly Academic):**
"The subsequent section delineates the authentication methodology pursuant to industry specifications."

**Pattern:** Technical but accessible vocabulary

**Corrected:**
"The next section explains authentication methods following industry standards."
```

**Sentence Complexity:**

Adjust sentence length to match patterns:

```markdown
**Pattern:** Average 16-18 words per sentence

**Original Draft (Too Complex - 35 words):**
"The authentication service, which we'll configure in this section using environment variables for security, connects to the database through a connection pool that maintains persistent connections for performance optimization."

**Corrected (Breaking into shorter sentences):**
"You'll configure the authentication service in this section using environment variables for security. The service connects to the database through a connection pool. This maintains persistent connections for better performance."
```

### 5. Apply Common Phrase Patterns

**Chapter Introductions:**

Match extracted introduction patterns:

```markdown
**Extracted Pattern:**
"In this chapter, you'll [action]. By the end, you'll [concrete outcome]."

**Original Draft:**
"This chapter discusses service mesh architecture and its implementation."

**Corrected (Applying Pattern):**
"In this chapter, you'll implement a service mesh for your application. By the end, you'll have secure service-to-service communication with traffic management and observability."
```

**Section Transitions:**

Use extracted transition phrases:

```markdown
**Extracted Patterns:**

- "Building on this..."
- "Now that you understand [X], let's explore [Y]"
- "Let's put this into practice"

**Original Draft:**
"The previous section covered configuration. The following section addresses deployment."

**Corrected (Applying Patterns):**
"Now that you understand configuration, let's explore deployment strategies."
```

**Technical Explanations:**

Follow extracted explanation structure:

````markdown
**Extracted Pattern:**

1. State concept
2. Explain why it matters
3. Provide concrete example
4. Show code/config
5. Explain key parts
6. Common pitfall

**Apply to New Content:**

[Concept] A service mesh provides secure communication between microservices.

[Why it matters] Without a service mesh, you'd need to implement security and observability in every service, leading to duplicated code and inconsistencies.

[Concrete example] Here's a service mesh configuration for our authentication service:

[Code/config]

```yaml
apiVersion: v1
kind: ServiceMesh
spec:
  mtls: enabled # Mutual TLS for secure communication
  tracing: jaeger # Distributed tracing
```
````

[Explain key parts] The `mtls: enabled` setting ensures all service communication is encrypted. The `tracing: jaeger` setting enables request tracing across services.

[Common pitfall] Don't enable service mesh after deploying services—install the mesh first, then deploy services into it.

````

### 6. Align Code Comment Style

**Match Comment Density:**

Adjust to match pattern (e.g., 1 comment per 3-4 lines):

```markdown
**Original Draft (Too Few Comments):**
```python
def authenticate(username, password):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        token = create_jwt(user.id)
        return token
    return None
````

**Pattern:** 1 comment per 3-4 lines

**Corrected (Applying Pattern):**

```python
def authenticate(username, password):
    # Query database for user with matching username
    user = db.query(User).filter(User.username == username).first()

    # Verify password hash matches stored hash
    if user and verify_password(password, user.hashed_password):
        # Generate JWT token with user ID as payload
        token = create_jwt(user.id)
        return token

    # Return None if authentication fails
    return None
```

````

**Match Comment Tone:**

Ensure comments match prose formality:

```markdown
**Original Draft (Comments too formal for Level 3 prose):**
```javascript
// Instantiate the authentication service object utilizing environment configuration
const auth = new AuthService(process.env);
````

**Pattern:** Level 3 formality in comments

**Corrected:**

```javascript
// Set up auth service with environment variables
const auth = new AuthService(process.env);
```

````

### 7. Apply Author Personality Markers

**Humor Integration (if pattern includes it):**

Add light humor matching extracted style:

```markdown
**Extracted Humor Pattern:**
- Frequency: 1-2 instances per chapter
- Style: Light technical humor, self-deprecating
- Example: "After a 3am debugging session, you'll appreciate this logging configuration."

**Application to New Content:**
"Service mesh configuration has 47 different settings. Yes, 47. After you've configured a few, you'll appreciate tools that generate these files automatically."
````

**Encouragement Markers:**

Apply encouragement at similar points as original:

```markdown
**Extracted Encouragement Pattern:**

- Frequency: At chapter milestones (mid-chapter, end-of-chapter)
- Style: Matter-of-fact, capability-building
- Example: "You've now deployed a production-ready service."

**Application:**
"You've configured service mesh security and observability. This is exactly what production environments require—you're ready to deploy confidently."
```

**Experience Sharing:**

Add real-world context matching author's approach:

```markdown
**Extracted Pattern:**

- References production incidents, debugging sessions
- Pragmatic: "In theory X, in practice Y"
- Example: "I've deployed hundreds of applications..."

**Application:**
"The documentation suggests configuring all 47 settings. In practice, you'll use 8-10 settings for most applications. Start with the essential ones shown here, add others as needed."
```

### 8. Verify Anti-Patterns Avoided

**Check Against Excluded Patterns:**

Review new content against documented anti-patterns:

```markdown
**Extracted Anti-Patterns to Avoid:**

- ❌ "Obviously", "clearly", "simply"
- ❌ Marketing hype ("revolutionary", "game-changing")
- ❌ Excessive formality ("One must ensure")
- ❌ Apologetic language ("Sorry for the complexity")
- ❌ Condescending ("Even beginners know")

**Scan New Draft:**

Search for: "obvious", "clear", "simple", "amazing", "must ensure", "sorry", "even"

**Found Violations:**
Line 67: "Obviously, you'll need to configure security."
Line 145: "This revolutionary approach changes everything."

**Corrected:**
Line 67: "You'll need to configure security first."
Line 145: "This approach simplifies service communication significantly."
```

### 9. Validate Tone Consistency

**Execute tone-consistency-checklist.md:**

Run the full tone consistency checklist on updated draft:

- Load extracted-tone-patterns.md (as reference)
- Execute tone-consistency-checklist.md
- Document any remaining violations
- Apply final corrections

**Compare to Original Chapters:**

Side-by-side comparison:

```markdown
**Comparison: Original Chapter 3 vs. New Chapter 15**

Voice Perspective:

- Original: Second person throughout ✓
- New: Second person throughout ✓

Formality Level:

- Original: Level 3, 14 contractions/1000 words
- New: Level 3, 13 contractions/1000 words ✓

Chapter Introduction:

- Original: "In this chapter, you'll deploy..." pattern
- New: "In this chapter, you'll implement..." pattern ✓

Code Comment Density:

- Original: 1 comment per 3.5 lines
- New: 1 comment per 3.2 lines ✓

Personality Markers:

- Original: 2 humor instances, matter-of-fact encouragement
- New: 1 humor instance, matter-of-fact encouragement ✓

**Assessment:** Tone consistency achieved. New chapter matches original voice.
```

### 10. Document Tone Adjustments

**Create Tone Adjustment Log:**

Record changes made for transparency:

```markdown
# Tone Adjustments: Chapter 15 - Service Mesh Implementation

**Date:** 2024-01-15
**Editor:** [Your Name]
**Reference:** extracted-tone-patterns.md

## Changes Made

### Formality Level Corrections

- Removed 15 instances of formal constructions ("one must", "it is imperative")
- Added 18 contractions to reach Level 3 target (13/1000 words)
- Simplified vocabulary: "utilize" → "use", "facilitate" → "help"

### Voice Alignment

- Changed 8 passive constructions to active voice
- Unified perspective: removed 3 instances of third person, changed to second person
- Final ratio: 87% active voice (target: 85%) ✓

### Phrase Pattern Application

- Applied standard chapter intro pattern (line 1-15)
- Added 12 extracted transition phrases
- Updated chapter conclusion to match pattern (lines 450-465)

### Code Comment Updates

- Added 14 comments to meet density target (1 per 3-4 lines)
- Revised 6 comments to match Level 3 formality
- Aligned comment style with extracted patterns

### Personality Markers

- Added 1 light humor instance (line 234)
- Added matter-of-fact encouragement at milestone (line 280)
- Added experience-based pragmatic note (line 367)

### Anti-Pattern Removals

- Removed "obviously" (3 instances)
- Removed "simply" in condescending context (2 instances)
- Removed marketing language: "revolutionary" (1 instance)

## Validation

- [x] tone-consistency-checklist.md executed
- [x] Compared to original Chapter 3 (reference)
- [x] All 5 tone characteristics present
- [x] Formality level matches (Level 3)
- [x] No anti-patterns remain

## Result

Chapter 15 now matches established book voice. Reader experience consistent with original edition.
```

## Success Criteria

✅ **Tone application is complete when:**

- extracted-tone-patterns.md reviewed and internalized
- New draft analyzed for tone mismatches
- Voice characteristics aligned (perspective, active/passive)
- Formality level matches patterns (contractions, vocabulary, sentence complexity)
- Common phrase patterns applied (introductions, transitions, conclusions)
- Code comment style matches density and tone
- Author personality markers present (humor, encouragement, experience)
- All anti-patterns removed
- tone-consistency-checklist.md executed and passed
- Tone adjustment log documented

✅ **Quality indicators:**

- New content sounds like original author
- No jarring tone shifts between original and new chapters
- Readers can't distinguish which chapters are original vs. new edition
- Formality level quantifiably matches (contraction count, sentence length)
- Code comments indistinguishable from original book's style

## Integration Points

**Input From:**

- **extract-tone-patterns.md** - Provides tone patterns to apply
- **New chapter draft** - Content needing tone alignment

**Output To:**

- **copy-edit-chapter.md** - Further refinement after tone application
- **Tone-aligned draft** - Ready for technical review

**Use With:**

- **expand-outline-to-draft.md** - Apply patterns during initial drafting
- **copy-edit-chapter.md** - Apply patterns during editing phase
- **tone-consistency-checklist.md** - Validate pattern application

## Important Notes

**Preserve Technical Accuracy:**

- Tone alignment must NOT change technical meaning
- If technical correction requires different phrasing, find tone-aligned alternative
- Technical accuracy always trumps tone perfection

**Maintain Author Authenticity:**

- Patterns guide consistency, not robotic compliance
- Natural variation is acceptable (contraction count can vary ±2-3 per 1000 words)
- Don't force humor if it doesn't fit the content naturally

**When Patterns Don't Fit:**

- Some content types may need different tone (reference appendix vs. tutorial chapter)
- Document intentional deviations with rationale
- Ensure deviations are justified, not lazy

**Multiple Authors:**

- All authors must use same extracted-tone-patterns.md
- Establish "tone reviewer" role to catch inconsistencies
- Conduct cross-author tone review before submission

**Edition-Specific Considerations:**

- If 10+ years since original, slight tone evolution may be appropriate
- Modern technical writing tends more casual—may need slight formality adjustment
- Document and justify any intentional pattern deviations

## Common Pitfalls

**Over-Correction:**
❌ Don't make every sentence identical length
❌ Don't force contractions where they sound unnatural
❌ Don't add humor where it doesn't fit content

**Under-Correction:**
❌ Don't skip code comment alignment (often forgotten)
❌ Don't ignore formality drift ("just a few formal sentences won't matter"—they will)
❌ Don't assume "close enough" for personality markers (readers notice absence)

**Technical vs. Tone Conflicts:**
❌ Don't sacrifice clarity for tone matching
❌ Don't use extracted phrases that don't fit new technical content
❌ Don't force patterns that make technical explanation worse

## Before/After Examples

**Example 1: Complete Section Transformation**

**Before (Mismatched Tone):**

````markdown
## Understanding Service Mesh Architecture

The implementation of a service mesh necessitates careful consideration of architectural paradigms. One must ensure that the control plane has been properly configured prior to deploying the data plane components. The architecture comprises several key elements which facilitate communication.

Configure the service mesh:

```yaml
apiVersion: v1
kind: ServiceMesh
spec:
  mtls: enabled
  tracing: jaeger
```
````

The configuration file delineates security and observability parameters.

````

**After (Applying Extracted Patterns - Level 3, Practical, Encouraging):**
```markdown
## Understanding Service Mesh Architecture

Let's implement a service mesh for your microservices application. You'll start by configuring the control plane, then deploy the data plane components. This architecture has three key elements that enable secure, observable service communication.

Configure your service mesh:
```yaml
apiVersion: v1
kind: ServiceMesh
spec:
  mtls: enabled  # Encrypts all service-to-service traffic
  tracing: jaeger  # Enables distributed request tracing
````

The `mtls` setting enables mutual TLS between services. The `tracing` setting connects to Jaeger for observability. You'll see these in action when you deploy services in the next section.

```

**Changes Applied:**
- Perspective: "One must" → "You'll" (second person)
- Formality: "necessitates" → "Let's implement", "delineates" → simpler language
- Active voice: "has been configured" → "configuring"
- Code comments: Added inline explanations
- Personality: Added forward-looking encouragement ("You'll see these in action...")

## Related Tasks

- **extract-tone-patterns.md** - Creates patterns document this task uses
- **define-book-tone.md** - Greenfield alternative (new books)
- **expand-outline-to-draft.md** - Use patterns during initial drafting
- **copy-edit-chapter.md** - Further refinement after tone application

## Related Checklists

- **tone-consistency-checklist.md** - Validates pattern application quality

## Related Knowledge Base

- **writing-voice-guides.md** - General tone profile examples for reference
```
