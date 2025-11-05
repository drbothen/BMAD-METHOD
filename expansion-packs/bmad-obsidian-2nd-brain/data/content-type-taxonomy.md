<!-- Powered by BMAD™ Core -->

# Content Type Taxonomy

## Overview

This taxonomy defines the six primary content types used by the Inbox Triage Agent for classifying captured information. Each type has distinct characteristics, signals, and processing requirements.

The 6 content types are:

1. **Quote** - Direct quotation from source material
2. **Concept** - Definition or explanation of an idea, theory, or mental model
3. **Reference** - Pointer to external resource
4. **Reflection** - Personal thinking, analysis, or synthesis
5. **Question** - Interrogative statement expressing curiosity or uncertainty
6. **Observation** - Factual statement, empirical data, witnessed phenomenon

---

## 1. Quote

### Definition

Direct quotation from source material, typically attributed to a specific author or source.

### Characteristics

- Contains verbatim text from original source
- Usually enclosed in quotation marks
- Has clear attribution (author, speaker, or source)
- Preserves original wording and formatting
- Often extracted for future reference or citation

### Signals (for classification algorithm)

- **Strong signals:**
  - Enclosed in quotation marks (" " or block quotes)
  - Attribution present (author name, "- Author", "by X")
  - Phrases like "according to", "X said", "X writes"
  - Complete sentences with clear voice

- **Weak signals:**
  - First-person perspective (usually not quotes)
  - Questions without answers (could be question type)
  - No source attribution (might be observation)

### Examples

**Example 1:** Direct quote with attribution

```
"Knowledge work is about managing your attention, not your time." - Cal Newport
```

**Example 2:** Block quote from article

```
> The Zettelkasten method emphasizes creating "atomic" notes - each note should
> contain exactly one idea that can stand alone.
>
> — Sascha Fast, zettelkasten.de
```

**Example 3:** Quote from book highlight

```
"If you wish to make an apple pie from scratch, you must first invent the universe."
(Carl Sagan, Cosmos)
```

**Example 4:** Quote with context

```
In his essay on productivity, Newport argues: "The ability to perform deep work
is becoming increasingly rare at exactly the same time it is becoming increasingly
valuable in our economy."
```

**Example 5:** Dialogue quote

```
As my mentor once told me: "The best time to plant a tree was 20 years ago.
The second best time is now."
```

### Common Sources

- Book highlights (Kindle, Readwise, Literal)
- Article excerpts (web clippings, saved posts)
- Social media quotes (Twitter threads, LinkedIn posts)
- Academic papers (direct quotations)
- Meeting notes (attributed statements)
- Podcasts/interviews (transcribed quotes)

### Processing Recommendations

- Preserve original formatting and punctuation
- Always capture full attribution (author + source)
- Link to original source when possible
- Consider creating permanent note if quote is significant
- Tag with author name and topic
- Check if quote already exists in vault to prevent duplicates

---

## 2. Concept

### Definition

Explanation or definition of an idea, theory, mental model, framework, or principle. Educational content that teaches "what something is" or "how something works."

### Characteristics

- Explanatory in nature
- Defines terms or explains mechanisms
- Often includes examples or analogies
- Structured and informative
- Objective tone (not personal reflection)

### Signals (for classification algorithm)

- **Strong signals:**
  - Definitional language: "X is...", "X refers to...", "X means..."
  - Explanatory phrases: "how X works", "the principle of X"
  - Academic/educational tone
  - Describes mechanisms, processes, or frameworks
  - Includes examples to illustrate concept

- **Weak signals:**
  - Personal opinions (might be reflection)
  - Questions (might be question type)
  - Just a link with no explanation (reference type)

### Examples

**Example 1:** Zettelkasten definition

```
The Zettelkasten method uses atomic notes linked by concept relationships rather
than hierarchical folders. Each note captures a single idea and connects to related
notes through explicit links, creating an emergent knowledge structure.
```

**Example 2:** Mental model explanation

```
The Circle of Competence is a mental model where you identify the boundaries of
your knowledge and skills. Operating within your circle increases success probability,
while venturing outside requires acknowledging higher uncertainty.
```

**Example 3:** Technical concept

```
Bi-temporal versioning maintains two independent timelines: valid time (when the
fact was true in the real world) and transaction time (when the fact was recorded
in the database). This enables querying "what did we know when" and "what was
actually true when."
```

**Example 4:** Framework description

```
GTD's Five Stages of Workflow: (1) Capture everything, (2) Clarify what it means,
(3) Organize by category, (4) Reflect on priorities, (5) Engage with the work.
This systematic approach reduces cognitive load by externalizing task tracking.
```

**Example 5:** Algorithm explanation

```
Spaced repetition schedules reviews at increasing intervals based on recall strength.
First review at 1 day, then 3 days, then 7 days, then 14 days, and so on. This
exploits the spacing effect to optimize long-term retention.
```

### Common Sources

- Educational articles and tutorials
- Technical documentation
- Academic papers (methodology sections)
- Books explaining frameworks/theories
- Course materials and lecture notes
- Wiki pages and encyclopedias

### Processing Recommendations

- Create permanent note if concept is novel to vault
- Link to related concepts already in knowledge base
- Extract key terminology for tagging
- Consider creating examples or applications
- Link to original source for deep dive
- Add to concept map if using visual knowledge management

---

## 3. Reference

### Definition

Pointer to an external resource such as a URL, citation, bookmark, or recommendation to read/watch/explore something.

### Characteristics

- Primary purpose is pointing elsewhere
- Contains link, citation, or resource identifier
- May include brief description
- Action item implicit: "check this out", "read this", "watch this"
- Minimal analysis or synthesis

### Signals (for classification algorithm)

- **Strong signals:**
  - Contains URL or link
  - Phrases: "see also", "check out", "read more at", "source:"
  - Citation format (APA, MLA, etc.)
  - Minimal surrounding content (mostly the link)
  - Bookmark-like structure

- **Weak signals:**
  - Extensive quote or explanation (might be quote/concept)
  - Personal commentary (might be reflection)
  - Question about the resource (might be question)

### Examples

**Example 1:** Article recommendation

```
Research on spaced repetition effectiveness: https://www.gwern.net/Spaced-repetition
```

**Example 2:** Academic citation

```
Ahrens, S. (2017). *How to Take Smart Notes: One Simple Technique to Boost
Writing, Learning and Thinking*. CreateSpace Independent Publishing Platform.
```

**Example 3:** Tool recommendation

```
Obsidian Canvas plugin for visual knowledge mapping:
https://obsidian.md/canvas
```

**Example 4:** Video resource

```
Watch: Ali Abdaal's overview of the Zettelkasten method (15 min)
https://www.youtube.com/watch?v=XUltI4v_UU4
```

**Example 5:** Related reading

```
For more on atomic habits, see James Clear's website: https://jamesclear.com/atomic-habits
Also relevant: BJ Fogg's Tiny Habits framework
```

### Common Sources

- Browser bookmarks and read-later apps
- Bibliography and works cited sections
- Social media link shares
- Reading lists and recommendations
- Documentation links
- Tool and resource discoveries

### Processing Recommendations

- Verify link is accessible and not dead
- Capture page title and author if available
- Consider fetching full content if important
- Add to reading queue or research backlog
- Tag by topic and resource type (article, video, tool, paper)
- Set reminder to actually engage with resource
- Archive web page if link might break (use web archiving tools)

---

## 4. Reflection

### Definition

Personal thinking, analysis, synthesis, or interpretation. First-person insights connecting ideas, evaluating concepts, or developing original thoughts.

### Characteristics

- First-person perspective ("I think", "I notice", "I wonder")
- Personal voice and opinion
- Synthesis of multiple sources or ideas
- Analytical or interpretive
- Original thinking, not just reporting

### Signals (for classification algorithm)

- **Strong signals:**
  - First-person pronouns: "I", "my", "me"
  - Thinking verbs: "I think", "I believe", "I notice", "I realize"
  - Synthesis language: "connecting X and Y", "this relates to"
  - Evaluative language: "I agree/disagree", "this seems"
  - Questions you're asking yourself

- **Weak signals:**
  - Objective facts (observation type)
  - Direct quotes (quote type)
  - Simple links (reference type)

### Examples

**Example 1:** Pattern recognition

```
I'm noticing a pattern between GTD's inbox zero philosophy and the Zettelkasten
triage phase. Both emphasize that the initial capture point is not the final
destination - it's a processing queue. The real work happens in clarification
and organization, not capture.
```

**Example 2:** Synthesis across sources

```
Reading Newport and Ahrens back-to-back reveals a core truth: both deep work and
effective note-taking require focused attention. Newport's "deep work" is the
cognitive mode needed for Ahrens' "thinking with notes." They're describing the
same mental state from different angles.
```

**Example 3:** Evaluating an idea

```
I'm skeptical of the claim that "you should process your inbox daily." For creative
work, I think there's value in letting ideas marinate for a few days before processing.
Immediate processing might optimize for efficiency but sacrifice serendipitous connections.
```

**Example 4:** Personal application

```
Applying the Circle of Competence to my career: I'm clearly inside my circle with
Python and data analysis, at the edge with ML deployment, and well outside with
frontend development. This explains why frontend tasks feel so draining - I'm
operating outside my competence.
```

**Example 5:** Meta-cognitive observation

```
I realize I've been confusing "taking notes" with "thinking." Real thinking happens
when I put away my sources and try to explain an idea in my own words. The act
of retrieval and reformulation is where understanding happens.
```

### Common Sources

- Journal entries and personal notes
- Margin notes and annotations
- Post-meeting reflections
- Learning logs and study notes
- Thinking-out-loud captures
- Comments on articles or books

### Processing Recommendations

- Treat as primary source material (it's your original thought)
- Link to related notes and concepts
- Consider developing into essay or permanent note
- Tag with topics and mental models referenced
- Note the date - reflections evolve over time
- Revisit periodically to see how your thinking has changed
- Surface patterns in your reflection topics (what you think about most)

---

## 5. Question

### Definition

Interrogative statement expressing curiosity, uncertainty, or desire to learn. Questions you want to explore or answer.

### Characteristics

- Interrogative structure (question mark)
- Expresses gap in knowledge
- May be rhetorical or genuine
- Often motivates future research
- Can be simple or complex

### Signals (for classification algorithm)

- **Strong signals:**
  - Ends with question mark (?)
  - Interrogative words: who, what, when, where, why, how
  - Phrases: "I wonder", "curious about", "how does X work"
  - Expresses uncertainty or knowledge gap

- **Weak signals:**
  - Rhetorical question in the middle of analysis (reflection)
  - Question mark in exclamatory sentence ("Really?!")

### Examples

**Example 1:** Methodological question

```
How does bi-temporal versioning differ from event sourcing? Are they solving
the same problem with different techniques, or are they complementary approaches?
```

**Example 2:** Curiosity-driven question

```
Why do some people naturally build knowledge systems (like Zettelkasten) while
others resist external memory tools? Is it personality-driven, or is it about
past success/failure with note-taking?
```

**Example 3:** Research question

```
What are the optimal review intervals for spaced repetition? Does the answer
differ by content type (facts vs concepts vs procedures)?
```

**Example 4:** Tool exploration question

```
Can Obsidian's graph view be used for visual thinking, or is it primarily a
navigation tool? How do people actually use it in practice?
```

**Example 5:** Application question

```
How could I apply the Feynman Technique to my current project? What would be
the simplest explanation I could give to someone unfamiliar with the domain?
```

### Common Sources

- Margin notes while reading
- Post-lecture questions
- Research brainstorming sessions
- Conversation follow-ups
- Curiosity logs
- Problem-solving sessions

### Processing Recommendations

- Track questions in dedicated "open questions" note or tag
- Link to related concepts and potential resources
- Set intention to answer (add to research queue)
- Mark when answered, link to answer note
- Revisit unanswered questions periodically
- Consider which questions are most important/energizing
- Questions often lead to the most valuable research
- Group related questions to identify knowledge gaps

---

## 6. Observation

### Definition

Factual statement, empirical data, witnessed phenomenon, or objective record of something that occurred. The "what happened" without interpretation.

### Characteristics

- Objective language
- Factual and verifiable
- Often includes data, metrics, or measurements
- Describes what was observed, not why
- Minimal personal interpretation

### Signals (for classification algorithm)

- **Strong signals:**
  - Data points: numbers, metrics, measurements
  - Objective language: "occurred", "happened", "measured"
  - Time stamps and dates
  - Verifiable facts
  - Past tense reporting

- **Weak signals:**
  - Personal interpretation (reflection)
  - Explanatory language (concept)
  - First-person thinking (reflection)

### Examples

**Example 1:** Personal metrics

```
My note count increased from 487 to 523 notes this month (7.4% growth).
Average notes per day: 1.2
```

**Example 2:** Behavioral observation

```
Over the last week, I wrote 5 permanent notes on Monday and Tuesday, then
none for the rest of the week. Pattern: concentrated effort at week start,
then other work takes over.
```

**Example 3:** Reading log

```
Completed "How to Take Smart Notes" by Sönke Ahrens on 2025-11-04.
Reading time: 6 hours over 3 days. Highlights captured: 37.
```

**Example 4:** System observation

```
Obsidian vault sync failed 3 times today between 2pm-3pm. Error message:
"Connection timeout." Resolved after router restart at 3:15pm.
```

**Example 5:** Event record

```
Met with Sarah to discuss knowledge management strategy (2025-11-04, 10am-11am).
Attendees: me, Sarah. Location: Conference Room B. Topics: Zettelkasten implementation,
tool selection, training plan.
```

### Common Sources

- Personal tracking apps and logs
- Meeting minutes and event records
- Research data collection
- System logs and error reports
- Quantified self data
- Timeline and chronology notes

### Processing Recommendations

- Store in chronological log or timeline
- Link to related projects or topics
- Look for patterns over time (weekly/monthly reviews)
- Consider visualization (charts, graphs)
- Use as evidence for reflections or analysis
- Tag with date and relevant metrics
- Observations become valuable when aggregated and analyzed
- Consider automated tracking where possible

---

## Classification Decision Tree

When classifying content, follow this decision tree:

1. **Does it have quotation marks and attribution?** → **Quote**
2. **Does it primarily point to an external resource?** → **Reference**
3. **Does it end with a question mark and express curiosity?** → **Question**
4. **Does it contain first-person thinking or synthesis?** → **Reflection**
5. **Does it explain what something is or how it works?** → **Concept**
6. **Does it record factual data or events?** → **Observation**
7. **Still unsure?** → Default to **Observation** (lowest confidence)

---

## Ambiguous Cases and Edge Cases

### Quote + Reflection

If content has a quote followed by personal commentary:

- **Primary type:** Reflection
- **Confidence:** Medium (0.6-0.7)
- **Processing:** Extract quote separately if valuable

### Concept + Question

If content explains a concept but frames it as a question:

- **Primary type:** Concept
- **Confidence:** Medium (0.6-0.7)
- **Note:** Questions are often pedagogical devices in explanations

### Reference + Observation

If content links to a resource with metrics about it:

- **Primary type:** Reference
- **Confidence:** High (0.8+)
- **Processing:** The link is the primary value

### Multiple Content Types

If content genuinely contains multiple types:

- **Confidence:** Low (<0.7)
- **Flag for review:** true
- **Recommendation:** Consider splitting into multiple captures

---

## Usage in Classification Algorithm

The classification algorithm (implemented in `classify-content-type.md` task) uses this taxonomy as reference data. For each content type:

1. Check for strong signals (weight: high)
2. Check for weak signals (weight: low)
3. Count matching characteristics
4. Calculate confidence score
5. Flag ambiguous cases for review

The confidence score algorithm is defined in the Inbox Triage Agent persona and implemented in the classification task.

---

## Maintenance and Evolution

This taxonomy should be treated as living documentation:

- Add new examples as patterns emerge
- Refine signal definitions based on classification errors
- Update decision tree if new content types are needed
- Document edge cases encountered in production
- Review and update quarterly based on user feedback

**Last Updated:** 2025-11-04
**Version:** 1.0
