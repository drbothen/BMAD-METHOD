# BMAD Obsidian 2nd Brain - Transcript Processing & Task Management Requirements

**Document Version:** 1.0
**Created:** 2025-11-04
**Status:** Draft
**Related Epic:** EPIC-001 Obsidian 2nd Brain with Temporal RAG
**Phase:** Phase 1.5 (Post-MVP Enhancement)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Transcript Processing Requirements](#2-transcript-processing-requirements)
3. [Task Management Requirements](#3-task-management-requirements)
4. [Agent Specifications](#4-agent-specifications)
5. [Task Specifications](#5-task-specifications)
6. [Template Specifications](#6-template-specifications)
7. [Checklist Specifications](#7-checklist-specifications)
8. [Workflow Specifications](#8-workflow-specifications)
9. [Integration Specifications](#9-integration-specifications)
10. [Implementation Roadmap](#10-implementation-roadmap)

---

## 1. Overview

### 1.1 Purpose

This document extends the BMAD Obsidian 2nd Brain system with two critical capabilities:

1. **Transcript Processing**: Intelligent processing of audio/video transcripts, meeting notes, and voice memos
2. **Task Management**: Extraction, tracking, and management of action items and todos from any content source

### 1.2 Business Value

**Transcript Processing:**

- Convert unstructured meeting recordings into actionable knowledge
- Extract key insights, decisions, and action items automatically
- Create speaker-attributed summaries
- Link meeting insights to existing knowledge base
- Enable temporal tracking of decisions and their context

**Task Management:**

- Never lose action items buried in notes
- Automatic extraction from meetings, brainstorms, and research
- GTD-compatible workflow integration
- Task-to-project linking
- Temporal tracking of task creation and completion

### 1.3 User Personas

**Primary Users:**

- Knowledge workers attending frequent meetings
- Managers tracking team action items
- Researchers conducting interviews
- Content creators recording ideas via voice
- GTD practitioners managing complex workflows

### 1.4 Success Metrics

**Transcript Processing:**

- 95%+ speaker identification accuracy
- 90%+ key point extraction relevance
- Action item detection rate > 85%
- Processing time < 2 minutes per hour of audio

**Task Management:**

- 90%+ action item extraction accuracy
- Task completion tracking accuracy 100%
- Task-to-context linking > 80%
- User task completion rate increase 30%+

---

## 2. Transcript Processing Requirements

### 2.1 Input Sources

**Supported Formats:**

- Audio files: MP3, WAV, M4A, OGG
- Video files: MP4, MOV, AVI (audio extraction)
- Text transcripts: Already transcribed content (various formats)
- Live recordings: Real-time transcription (optional)

**Transcript Sources:**

- Whisper ASR (local transcription via Obsidian Transcription plugin)
- Deepgram API (cloud transcription via Audio Notes plugin)
- Google Gemini API (via Captain's Log plugin)
- OpenAI Whisper API (via Whisper Obsidian plugin)
- Manual transcripts (pasted or imported)
- Automated meeting bots (Otter.ai, Fireflies.ai, etc.)

### 2.2 Processing Capabilities

**Core Processing:**

1. **Speaker Diarization**: Identify and label different speakers
2. **Key Point Extraction**: Identify main topics, decisions, and insights
3. **Action Item Extraction**: Detect tasks, todos, and commitments
4. **Question Extraction**: Identify unresolved questions and open loops
5. **Decision Logging**: Track decisions made and their context
6. **Topic Segmentation**: Break transcript into logical sections
7. **Timestamp Annotation**: Link content to specific time points
8. **Entity Extraction**: Identify people, projects, concepts mentioned

**Advanced Processing:** 9. **Sentiment Analysis**: Detect agreement, disagreement, concern 10. **Follow-up Identification**: Detect references to past meetings/decisions 11. **Commitment Tracking**: Who committed to what by when 12. **Summary Generation**: Create executive summary and detailed summaries 13. **Quote Extraction**: Identify quotable statements

### 2.3 Output Structure

**Meeting Note Structure:**

- Frontmatter: Meeting metadata (date, attendees, duration, type)
- Executive Summary: 2-3 sentence overview
- Attendees: List with roles
- Key Topics: Main discussion areas
- Decisions Made: List of decisions with context
- Action Items: Extracted tasks with owners and deadlines
- Open Questions: Unresolved issues
- Key Quotes: Notable statements
- Next Steps: Planned follow-ups
- Timestamp Index: Jump links to audio/video
- Full Transcript: Speaker-attributed text
- Related Notes: Links to relevant knowledge base notes

**Temporal Tracking:**

- Create MeetingEvent nodes in Neo4j
- Link to participants (Person nodes)
- Link to mentioned concepts/projects (Note nodes)
- Track decision timeline
- Enable queries: "What decisions were made about X?"

---

## 3. Task Management Requirements

### 3.1 Task Sources

**Content Sources:**

- Meeting transcripts (extracted action items)
- Research notes (todos and next steps)
- Brainstorm notes (ideas requiring action)
- Email captures (action items from correspondence)
- Daily notes (task creation)
- Project notes (project-specific tasks)
- Inbox notes (captured tasks)

**Extraction Patterns:**

- Markdown checkboxes: `- [ ] Task description`
- Action verbs: "Need to...", "Should...", "Must...", "TODO:", "Action:"
- Commitment language: "I will...", "We need to...", "X will..."
- Deadline patterns: "by Friday", "due tomorrow", "before EOD"
- Assignment patterns: "@person needs to", "assigned to X"

### 3.2 Task Structure

**Task Properties:**

- **Description**: Clear, actionable statement
- **Status**: todo, in-progress, waiting, blocked, completed, cancelled
- **Priority**: critical, high, medium, low
- **Due Date**: Optional deadline
- **Created Date**: When task was identified
- **Completed Date**: When task was finished
- **Owner**: Person responsible (if multi-user)
- **Source**: Original note/meeting where task was created
- **Context**: Related project, epic, or area
- **Dependencies**: Other tasks that must complete first
- **Tags**: Categories, labels
- **Estimates**: Time or effort estimate

**GTD Properties:**

- **Context**: @home, @work, @errands, @computer, @phone
- **Energy**: high, medium, low
- **Time Available**: 5min, 15min, 30min, 1hr, 2hr+
- **Waiting For**: External blocker
- **Someday/Maybe**: Future consideration flag

### 3.3 Task Management Capabilities

**Core Capabilities:**

1. **Task Extraction**: Auto-detect tasks from any content
2. **Task Creation**: Create task notes with proper structure
3. **Task Linking**: Link tasks to source notes and projects
4. **Task Status Tracking**: Update status, completion dates
5. **Task Dashboard**: Aggregate view of all tasks
6. **Task Filtering**: By status, priority, due date, context, project
7. **Task Searching**: Full-text and semantic search
8. **Task Archiving**: Complete tasks → archive with timestamps

**Advanced Capabilities:** 9. **Project Task Lists**: Aggregate all tasks for a project 10. **Daily Planning**: Surface relevant tasks for today 11. **Weekly Review**: Review all tasks, update status 12. **Dependency Management**: Track task dependencies, flag blockers 13. **Recurring Tasks**: Create repeating tasks 14. **Task Templates**: Standard tasks for common workflows 15. **Task Metrics**: Track completion rates, velocity, aging tasks

**GTD Workflow:** 16. **Capture**: Quick task capture from anywhere 17. **Clarify**: Process inbox tasks, add details 18. **Organize**: Assign context, priority, project 19. **Reflect**: Weekly review of all tasks 20. **Engage**: Daily planning and task execution

### 3.4 Integration Requirements

**Obsidian Plugin Integration:**

- **Tasks Plugin**: Compatible task format (DataviewJS queries)
- **TODO Plugin**: Aggregate tasks across vault
- **Calendar Plugin**: Due date visualization
- **Periodic Notes**: Integration with daily/weekly notes

**Neo4j Integration:**

- Create Task nodes with temporal metadata
- Link tasks to source notes (EXTRACTED_FROM)
- Link tasks to projects (PART_OF)
- Link tasks to people (ASSIGNED_TO, CREATED_BY)
- Track task state changes over time (status transitions)
- Enable queries: "What tasks were created from this meeting?"

---

## 4. Agent Specifications

### 4.1 Transcript Processing Agent

**Agent Name:** Transcript Processing Agent
**Agent ID:** transcript-processor-agent
**Icon:** 🎙️
**Title:** Transcript & Meeting Note Specialist

**When to Use:**

- Processing audio/video transcripts
- Creating structured meeting notes
- Extracting insights from interviews
- Processing voice memos
- Analyzing recorded discussions

**Persona:**

- **Role**: Transcript Analyst & Meeting Note Specialist
- **Style**: Analytical, detail-oriented, systematic, conversational
- **Identity**: Specialist in extracting structure and actionable insights from unstructured audio/video content
- **Focus**: Speaker identification, key point extraction, action item detection, decision logging

**Core Capabilities:**

- Process transcripts from multiple sources (Whisper, Deepgram, Gemini, manual)
- Identify and label speakers
- Extract key points, decisions, action items, questions
- Segment transcript by topic
- Generate executive summaries
- Create speaker-attributed notes
- Link insights to existing knowledge base
- Create temporal Neo4j records

**Commands:**

- `*help`: Show available commands
- `*process-transcript {file}`: Process a transcript file
- `*extract-speakers`: Identify and label speakers
- `*extract-key-points`: Identify main topics and insights
- `*extract-action-items`: Detect tasks and commitments
- `*extract-decisions`: Identify decisions made
- `*create-meeting-note`: Generate structured meeting note
- `*link-to-knowledge`: Suggest links to existing notes
- `*generate-summary`: Create executive summary
- `*yolo`: Toggle auto-approval mode
- `*exit`: Exit agent

**Dependencies:**

- **Tasks:**
  - process-transcript.md
  - identify-speakers.md
  - extract-key-points.md
  - extract-action-items-from-transcript.md
  - extract-decisions.md
  - segment-transcript.md
  - create-meeting-note.md
  - link-transcript-insights.md
- **Templates:**
  - meeting-note-tmpl.yaml
  - transcript-note-tmpl.yaml
  - interview-note-tmpl.yaml
- **Checklists:**
  - transcript-processing-checklist.md
  - meeting-note-completeness-checklist.md

---

### 4.2 Task Management Agent

**Agent Name:** Task Management Agent
**Agent ID:** task-manager-agent
**Icon:** ✅
**Title:** Action Item & Todo Specialist

**When to Use:**

- Extracting action items from any content
- Creating and tracking tasks
- Managing project task lists
- Daily planning and weekly reviews
- GTD workflow execution

**Persona:**

- **Role**: Task Extraction & GTD Workflow Specialist
- **Style**: Organized, proactive, systematic, accountability-focused
- **Identity**: Specialist in detecting, tracking, and managing action items across entire knowledge base
- **Focus**: Task extraction, GTD methodology, project task management, completion tracking

**Core Capabilities:**

- Extract action items from any content (meetings, notes, emails)
- Create structured task notes
- Link tasks to source notes and projects
- Track task status and completion
- Generate task dashboards and views
- Support GTD workflow (capture, clarify, organize, reflect, engage)
- Manage dependencies and blockers
- Create recurring tasks
- Weekly review facilitation

**Commands:**

- `*help`: Show available commands
- `*extract-action-items {note}`: Extract tasks from a note
- `*create-task`: Create a new task note
- `*update-task-status {task} {status}`: Update task status
- `*link-task-to-project {task} {project}`: Link task to project
- `*generate-task-dashboard`: Create task overview
- `*daily-planning`: Surface today's tasks
- `*weekly-review`: Facilitate GTD weekly review
- `*find-stale-tasks`: Identify aging tasks
- `*archive-completed`: Archive finished tasks
- `*yolo`: Toggle auto-approval mode
- `*exit`: Exit agent

**Dependencies:**

- **Tasks:**
  - extract-action-items.md
  - create-task-note.md
  - update-task-status.md
  - link-task-to-project.md
  - generate-task-dashboard.md
  - daily-task-planning.md
  - weekly-task-review.md
  - identify-stale-tasks.md
  - archive-completed-tasks.md
- **Templates:**
  - task-tmpl.yaml
  - project-task-list-tmpl.yaml
  - daily-todo-tmpl.yaml
  - weekly-review-tmpl.yaml
- **Checklists:**
  - task-extraction-checklist.md
  - task-completeness-checklist.md
  - weekly-review-checklist.md

---

## 5. Task Specifications

### 5.1 Transcript Processing Tasks

#### Task: process-transcript.md

**Purpose:** Process raw transcript and extract structured information

**Input:**

- Transcript text (raw or formatted)
- Metadata: date, source, participants (optional)
- Audio/video file reference (optional)

**Process:**

1. Load transcript text
2. Detect format (plain text, SRT, VTT, JSON)
3. Parse timestamps if present
4. Identify speaker patterns
5. Segment by topic changes
6. Run extraction tasks (speakers, key points, action items, decisions)
7. Generate structured output

**Output:**

- Structured transcript data object
- Speaker list with labels
- Topic segments with timestamps
- Key points list
- Action items list
- Decisions list
- Questions list

**Algorithms:**

- Speaker diarization: Pattern matching for "Speaker 1:", "John:", etc.
- Topic segmentation: Semantic similarity analysis between paragraphs
- Timestamp parsing: Regex for common timestamp formats

---

#### Task: identify-speakers.md

**Purpose:** Identify and label speakers in transcript

**Input:**

- Transcript text
- Known participant names (optional)

**Process:**

1. Detect speaker labels in transcript (Speaker 1, A, John, etc.)
2. Analyze speech patterns and context clues
3. Match to known participants if provided
4. Assign consistent labels throughout transcript
5. Create speaker metadata (speaking time, turn count)

**Output:**

- Speaker list with labels and identities
- Speaker-attributed transcript segments
- Speaking time statistics

---

#### Task: extract-key-points.md

**Purpose:** Identify main topics, insights, and important statements

**Input:**

- Processed transcript with speaker attribution

**Process:**

1. Identify topic sentences and thesis statements
2. Detect decision language ("we decided", "we will", "the plan is")
3. Identify insight markers ("interesting", "key point", "important")
4. Extract statements with high information density
5. Group related points by topic
6. Rank by importance (frequency, speaker emphasis, position)

**Output:**

- List of key points with context
- Topic groupings
- Importance rankings
- Quote attributions

---

#### Task: extract-action-items-from-transcript.md

**Purpose:** Detect tasks, commitments, and action items

**Input:**

- Processed transcript with speaker attribution

**Process:**

1. Detect action verbs: "will", "should", "need to", "must", "going to"
2. Identify commitment language: "I'll", "we'll", "X will", "assigned to"
3. Extract deadline phrases: "by Friday", "before next meeting", "EOW"
4. Identify ownership: Who committed to what
5. Classify urgency: Critical, high, medium, low
6. Extract context: Why this action is needed

**Output:**

- List of action items with:
  - Description (what)
  - Owner (who)
  - Deadline (when)
  - Context (why)
  - Source (speaker, timestamp)
  - Priority

**Patterns:**

- Action: "John will send the report by Friday"
  - Owner: John
  - Task: Send the report
  - Deadline: Friday
- Action: "We need to schedule a follow-up meeting"
  - Owner: TBD (group responsibility)
  - Task: Schedule follow-up meeting
  - Deadline: None specified

---

#### Task: extract-decisions.md

**Purpose:** Identify and log decisions made during discussion

**Input:**

- Processed transcript with speaker attribution

**Process:**

1. Detect decision language:
   - "we decided", "we're going with", "let's go with"
   - "the decision is", "we agreed", "consensus is"
   - "approved", "rejected", "selected", "chose"
2. Extract decision context:
   - What was decided
   - Why (rationale)
   - When (meeting date/time)
   - Who participated in decision
   - Alternatives considered
3. Link to related decisions (if part of series)
4. Create decision log entry

**Output:**

- List of decisions with:
  - Decision statement
  - Rationale
  - Participants
  - Timestamp
  - Alternatives considered
  - Related decisions

---

#### Task: create-meeting-note.md

**Purpose:** Generate structured meeting note from processed transcript

**Input:**

- Processed transcript data
- Extracted speakers, key points, action items, decisions
- Meeting metadata

**Process:**

1. Use meeting-note-tmpl.yaml template
2. Populate frontmatter (date, attendees, duration, type)
3. Generate executive summary (2-3 sentences)
4. Create attendees list
5. Organize key topics by theme
6. List decisions with context
7. List action items with owners
8. List open questions
9. Extract key quotes
10. Create timestamp index
11. Append full transcript
12. Suggest links to related notes

**Output:**

- Structured meeting note in Obsidian
- Created in appropriate folder (e.g., /meetings)
- With proper frontmatter and sections

---

### 5.2 Task Management Tasks

#### Task: extract-action-items.md

**Purpose:** Extract action items from any content source

**Input:**

- Note content (meeting notes, research notes, brainstorms, etc.)
- Note metadata (title, created date, author)

**Process:**

1. Scan for markdown checkboxes: `- [ ] Task`
2. Detect action verb patterns:
   - "TODO:", "Action:", "Next step:", "Need to:", "Should:", "Must:"
   - "I will", "We need to", "X should", "Y must"
3. Identify commitment language with deadlines:
   - "by Friday", "before meeting", "end of week", "tomorrow"
4. Extract assignment patterns:
   - "@person", "assigned to X", "X will handle", "responsibility: Y"
5. Classify priority:
   - Critical: "urgent", "asap", "critical", "immediately"
   - High: "soon", "high priority", "important"
   - Medium: "should", "when possible"
   - Low: "nice to have", "someday", "consider"
6. Extract context (surrounding sentences)
7. Determine status (if already marked as in-progress or complete)

**Output:**

- List of action items with:
  - Description
  - Priority
  - Due date (if specified)
  - Owner (if specified)
  - Source note (link back)
  - Context (why needed)
  - Status (default: todo)

**Patterns:**

- "TODO: Update documentation by Friday" → Task: Update documentation, Deadline: Friday, Priority: medium
- "URGENT: Call client about contract issue" → Task: Call client about contract, Priority: critical
- "@john needs to review PR #123" → Task: Review PR #123, Owner: john, Priority: medium

---

#### Task: create-task-note.md

**Purpose:** Create structured task note using template

**Input:**

- Task description
- Task properties (priority, due date, owner, context, project)

**Process:**

1. Use task-tmpl.yaml template
2. Populate frontmatter:
   - Title: Task description
   - Status: todo (default)
   - Priority: From input or medium default
   - Due date: From input or null
   - Created date: Now
   - Owner: From input or current user
   - Source: Link to originating note
   - Project: From input or null
   - Tags: From input or auto-generated
3. Create task note sections:
   - Description (detailed task explanation)
   - Context (why needed, related information)
   - Dependencies (blockers, prerequisites)
   - Notes (progress updates)
4. Save in appropriate location (/tasks or /projects/{project}/tasks)
5. Create Neo4j Task node with metadata
6. Create relationships: EXTRACTED_FROM source, PART_OF project

**Output:**

- Task note file in Obsidian
- Neo4j Task node
- Relationships established

---

#### Task: update-task-status.md

**Purpose:** Update task status and record transition

**Input:**

- Task note ID
- New status (in-progress, waiting, blocked, completed, cancelled)
- Update notes (optional)

**Process:**

1. Load task note
2. Update status in frontmatter
3. Add timestamp for status change
4. If completed: Set completed_date
5. If blocked: Record blocker reason
6. Add note to progress history section
7. Update Neo4j Task node status property
8. Create Neo4j temporal edge: Task -[STATUS_CHANGED]-> Date
9. If part of project: Update project task counts

**Output:**

- Updated task note
- Updated Neo4j Task node
- Status change recorded in temporal graph

---

#### Task: link-task-to-project.md

**Purpose:** Associate task with project or epic

**Input:**

- Task note ID
- Project note ID

**Process:**

1. Load task note and project note
2. Update task frontmatter: project field
3. Add bidirectional wikilink:
   - Task note → Project note
   - Project note → Task note (in task list section)
4. Create Neo4j relationship: Task -[PART_OF]-> Project
5. Update project task counts in frontmatter
6. If project has MOC: Add task to MOC task list

**Output:**

- Updated task note with project link
- Updated project note with task link
- Neo4j relationship created

---

#### Task: generate-task-dashboard.md

**Purpose:** Create comprehensive task overview

**Input:**

- Filter criteria: project, status, priority, due date range, owner

**Process:**

1. Query all task notes matching filters
2. Group by status (todo, in-progress, waiting, blocked)
3. Sort by priority within each status
4. Calculate metrics:
   - Total tasks: Count
   - By status: Breakdown
   - By priority: Breakdown
   - Overdue: Count (due_date < today, status != completed)
   - Completed this week: Count
   - Average completion time: Days from created to completed
5. Create dashboard note using Dataview queries
6. Include visualizations:
   - Status pie chart (if plugin available)
   - Priority distribution
   - Completion trend graph

**Output:**

- Task dashboard note with:
  - Summary metrics
  - Tasks grouped by status
  - Priority highlights
  - Overdue warnings
  - Recent completions
  - Dataview queries for dynamic updates

---

#### Task: daily-task-planning.md

**Purpose:** Surface relevant tasks for today's work

**Input:**

- Today's date
- Current user (for multi-user systems)
- Context preferences (GTD contexts)

**Process:**

1. Query tasks with:
   - Status: todo or in-progress
   - Due date: Today or overdue
   - Owner: Current user (if specified)
2. Query tasks by GTD context (if specified):
   - @work, @home, @computer, @phone, etc.
3. Query tasks by energy level (if specified):
   - High energy tasks for morning
   - Low energy tasks for later
4. Sort by:
   - Overdue (highest priority)
   - Due today
   - High priority
   - Quick wins (< 15 min)
5. Create daily todo list in daily note
6. Group by:
   - Overdue (urgent)
   - Due today
   - Priority tasks (no deadline but important)
   - Quick wins
7. Estimate total time for all tasks

**Output:**

- Daily todo list in daily note
- Time estimate
- Context-organized tasks
- Energy-level organized tasks

---

#### Task: weekly-task-review.md

**Purpose:** Facilitate GTD weekly review workflow

**Input:**

- Week date range
- Current user

**Process:**

1. **Collect:**
   - All inbox items
   - All tasks created this week
   - All tasks completed this week
   - All tasks still open
2. **Review:**
   - Stale tasks (created > 30 days ago, still todo)
   - Blocked tasks (need resolution)
   - Waiting tasks (check if unblocked)
   - Recurring tasks (create next instance)
3. **Update:**
   - Mark completed tasks that weren't updated
   - Update priorities based on current context
   - Update due dates if changed
   - Archive completed tasks
4. **Plan:**
   - Next week priorities
   - Big rocks (important tasks)
   - Quick wins (momentum builders)
5. **Generate Weekly Review Note:**
   - Tasks completed this week (wins)
   - Tasks created this week
   - Open tasks by project
   - Stale task warnings
   - Blocked task list
   - Next week priorities

**Output:**

- Weekly review note
- Updated task statuses
- Archived completed tasks
- Next week planning list

---

## 6. Template Specifications

### 6.1 meeting-note-tmpl.yaml

**Purpose:** Structure for meeting notes created from transcripts

```yaml
name: meeting-note-tmpl
description: Template for meeting notes with transcript processing
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: type
        type: select
        options: [meeting_note]
        default: meeting_note
      - name: meeting_type
        type: select
        options: [standup, 1on1, planning, review, brainstorm, client, team, all-hands]
        required: true
      - name: date
        type: datetime
        format: ISO8601
        required: true
      - name: duration
        type: number
        description: Duration in minutes
      - name: attendees
        type: list
        description: List of attendees
        required: true
      - name: recording_url
        type: url
        description: Link to audio/video recording
      - name: transcript_source
        type: select
        options: [whisper, deepgram, gemini, manual, otter, fireflies]
      - name: processed_by
        type: select
        options: [transcript-processor-agent, manual]
        default: transcript-processor-agent
      - name: created
        type: datetime
        required: true
      - name: project
        type: link
        description: Related project

  - id: executive_summary
    title: Executive Summary
    instructions: 2-3 sentence overview of meeting

  - id: attendees_detail
    title: Attendees
    instructions: |
      List attendees with roles:
      - Name (Role/Department)

  - id: key_topics
    title: Key Topics Discussed
    instructions: |
      Main discussion areas:
      1. Topic name
         - Key points
         - Discussion summary

  - id: decisions
    title: Decisions Made
    instructions: |
      Format:
      - **Decision**: Statement
        - **Rationale**: Why
        - **Participants**: Who decided
        - **Alternatives Considered**: What else was discussed
        - **Timestamp**: When in recording

  - id: action_items
    title: Action Items
    instructions: |
      Format:
      - [ ] **Task description** (@owner, due: date)
        - Context: Why needed
        - Source: Speaker, timestamp

  - id: open_questions
    title: Open Questions
    instructions: |
      Unresolved issues:
      - Question statement?
        - Context
        - Who raised it
        - Follow-up needed

  - id: key_quotes
    title: Key Quotes
    instructions: |
      Notable statements:
      > "Quote text" — Speaker Name (timestamp)

  - id: next_steps
    title: Next Steps
    instructions: |
      Planned follow-ups:
      - Action
      - Timeline
      - Responsible party

  - id: timestamp_index
    title: Timestamp Index
    instructions: |
      Quick navigation:
      - [00:05:23] Topic A discussion
      - [00:15:45] Decision on Feature X
      - [00:32:10] Action item assignments
    required: false

  - id: related_notes
    title: Related Notes
    instructions: |
      Links to relevant knowledge base notes:
      - [[Note A]]: Reason for relevance
    required: false

  - id: full_transcript
    title: Full Transcript
    instructions: |
      Speaker-attributed transcript:
      **Speaker Name** (00:00:00):
      Transcript text...
```

---

### 6.2 task-tmpl.yaml

**Purpose:** Structure for task/todo tracking

```yaml
name: task-tmpl
description: Template for actionable tasks and todos
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: type
        type: select
        options: [task]
        default: task
      - name: status
        type: select
        options: [todo, in-progress, waiting, blocked, completed, cancelled]
        default: todo
        required: true
      - name: priority
        type: select
        options: [critical, high, medium, low]
        default: medium
        required: true
      - name: due_date
        type: date
        description: Deadline for completion
      - name: created_date
        type: datetime
        required: true
      - name: completed_date
        type: datetime
        description: When task was completed
      - name: owner
        type: text
        description: Person responsible
      - name: source
        type: link
        description: Note where task was created
        required: true
      - name: project
        type: link
        description: Related project or epic
      - name: tags
        type: list
        description: Categories and labels
      - name: estimate
        type: text
        description: Time or effort estimate (e.g., "2h", "1d")
      - name: gtd_context
        type: select
        options: [@home, @work, @errands, @computer, @phone, @online, @offline]
        description: GTD context for task execution
      - name: energy_level
        type: select
        options: [high, medium, low]
        description: Energy required for task
      - name: time_available
        type: select
        options: [5min, 15min, 30min, 1hr, 2hr+]
        description: Time needed for task

  - id: description
    title: Task Description
    instructions: |
      Detailed explanation of what needs to be done
      Include:
      - Specific deliverables
      - Success criteria
      - Any relevant constraints

  - id: context
    title: Context
    instructions: |
      Why this task is needed:
      - Background
      - Related information
      - Links to relevant notes

  - id: dependencies
    title: Dependencies
    instructions: |
      Prerequisites and blockers:
      - Tasks that must complete first: [[Task A]], [[Task B]]
      - External blockers: Waiting for approval, resource, etc.
    required: false

  - id: progress_notes
    title: Progress Notes
    instructions: |
      Updates as task progresses:
      - YYYY-MM-DD: Status update or note
    required: false

  - id: completion_notes
    title: Completion Notes
    instructions: |
      When completed:
      - What was accomplished
      - Any deviations from plan
      - Lessons learned
    required: false
```

---

### 6.3 project-task-list-tmpl.yaml

**Purpose:** Aggregate task view for a project

````yaml
name: project-task-list-tmpl
description: Template for project task aggregation
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: type
        type: select
        options: [project_task_list]
        default: project_task_list
      - name: project
        type: link
        description: Project this task list belongs to
        required: true
      - name: created
        type: datetime
        required: true
      - name: last_updated
        type: datetime
        required: true

  - id: summary
    title: Task Summary
    instructions: |
      Task counts:
      - Total: X
      - Todo: X
      - In Progress: X
      - Waiting: X
      - Blocked: X
      - Completed: X

  - id: critical_tasks
    title: Critical Tasks
    instructions: |
      Urgent tasks requiring immediate attention:
      - [ ] [[Task A]] (due: date)

  - id: in_progress_tasks
    title: In Progress
    instructions: |
      Currently being worked on:
      - [ ] [[Task B]] (@owner)

  - id: todo_tasks
    title: To Do
    instructions: |
      Not yet started:
      - [ ] [[Task C]]

  - id: waiting_tasks
    title: Waiting
    instructions: |
      Blocked on external factors:
      - [ ] [[Task D]] (waiting for: X)

  - id: completed_tasks
    title: Recently Completed
    instructions: |
      Finished tasks:
      - [x] [[Task E]] (completed: date)

  - id: dataview_queries
    title: Dynamic Task Views
    instructions: |
      Dataview queries for automatic task aggregation:
      ```dataview
      TASK
      FROM "tasks"
      WHERE contains(project, this.file.link)
      WHERE status != "completed" AND status != "cancelled"
      SORT priority DESC, due_date ASC
      ```
````

---

## 7. Checklist Specifications

### 7.1 transcript-processing-checklist.md

**Purpose:** Validate transcript processing completeness

**Items:**

- [ ] Transcript source identified (Whisper, Deepgram, manual, etc.)
- [ ] Meeting metadata recorded (date, duration, attendees, type)
- [ ] Speakers identified and labeled consistently
- [ ] Timestamps preserved and indexed
- [ ] Key topics identified and organized
- [ ] Decisions extracted with context
- [ ] Action items extracted with owners and deadlines
- [ ] Open questions identified
- [ ] Executive summary generated (2-3 sentences)
- [ ] Related notes suggested and linked
- [ ] Neo4j MeetingEvent node created (if using Neo4j)
- [ ] Attendees linked as participants in Neo4j

**Pass Criteria:** All required items checked (items 1, 2, 3, 6, 7, 9)

---

### 7.2 task-extraction-checklist.md

**Purpose:** Validate task extraction completeness

**Items:**

- [ ] All markdown checkboxes converted to tasks
- [ ] Action verb patterns detected
- [ ] Commitment language identified
- [ ] Deadlines extracted where specified
- [ ] Assignment/ownership identified where specified
- [ ] Priority classified appropriately
- [ ] Context captured (why task is needed)
- [ ] Source note linked
- [ ] No duplicate tasks created
- [ ] Task description is actionable and clear
- [ ] Tasks created in appropriate location

**Pass Criteria:** All required items checked (items 1, 2, 6, 7, 8, 10, 11)

---

### 7.3 weekly-review-checklist.md

**Purpose:** Guide GTD weekly review process

**Items:**

- [ ] All inbox items processed (empty inbox)
- [ ] All new tasks reviewed and organized
- [ ] All completed tasks marked and archived
- [ ] Stale tasks reviewed (> 30 days old)
- [ ] Blocked tasks checked for resolution
- [ ] Waiting tasks checked for unblocking
- [ ] Task priorities updated based on current context
- [ ] Due dates adjusted if needed
- [ ] Recurring tasks instantiated for next week
- [ ] Next week priorities identified (top 3)
- [ ] Big rocks scheduled (important tasks)
- [ ] Project task lists reviewed for completeness
- [ ] Weekly review note generated

**Pass Criteria:** All items checked

---

## 8. Workflow Specifications

### 8.1 Transcript Processing Workflow

**Workflow Name:** `transcript-to-knowledge-workflow`

**Purpose:** Convert audio/video recordings into actionable knowledge

**Steps:**

1. **Capture Recording** (User)
   - Record meeting/interview
   - Upload audio/video to transcription service
   - OR paste existing transcript

2. **Transcribe** (External Service)
   - Whisper ASR (local)
   - Deepgram API (cloud)
   - Google Gemini (cloud)
   - Manual transcription

3. **Process Transcript** (Transcript Processing Agent)
   - `*process-transcript {file}`
   - Agent identifies speakers
   - Agent extracts key points
   - Agent extracts action items
   - Agent extracts decisions
   - Agent generates summary

4. **Create Meeting Note** (Transcript Processing Agent)
   - `*create-meeting-note`
   - Agent uses meeting-note-tmpl.yaml
   - Agent populates all sections
   - Agent creates Neo4j MeetingEvent node

5. **Extract Action Items** (Task Management Agent)
   - `*extract-action-items {meeting_note}`
   - Agent converts action items to tasks
   - Agent creates task notes
   - Agent links tasks to meeting note

6. **Link to Knowledge** (Semantic Linker Agent)
   - `*suggest-links {meeting_note}`
   - Agent finds related notes
   - User approves links
   - Agent creates bidirectional links

7. **Review & Refine** (User)
   - User reviews meeting note
   - User refines key points
   - User clarifies action items
   - User adds additional context

**Duration:** 15-30 minutes per hour of audio

**Frequency:** Per meeting/recording

---

### 8.2 Task Management Workflow (GTD)

**Workflow Name:** `gtd-task-management-workflow`

**Purpose:** Implement GTD methodology for task management

**GTD Phases:**

**Phase 1: Capture**

- Quick capture from anywhere (inbox, daily note, meeting)
- No processing, just capture
- Task Management Agent: `*extract-action-items`

**Phase 2: Clarify**

- Process inbox (daily or weekly)
- Add details to tasks (context, project, priority)
- Task Management Agent: `*create-task` for each item

**Phase 3: Organize**

- Assign GTD context (@work, @home, etc.)
- Assign priority and due date
- Link to projects
- Task Management Agent: `*link-task-to-project`

**Phase 4: Reflect (Weekly Review)**

- Review all open tasks
- Update status and priorities
- Archive completed
- Plan next week
- Task Management Agent: `*weekly-review`

**Phase 5: Engage (Daily Planning)**

- Select today's tasks
- Organize by context and energy
- Execute
- Task Management Agent: `*daily-planning`

**Duration:**

- Daily: 10-15 minutes
- Weekly: 45-60 minutes

---

### 8.3 Meeting-to-Tasks Workflow

**Workflow Name:** `meeting-action-items-workflow`

**Purpose:** Ensure all meeting action items become tracked tasks

**Steps:**

1. **Record Meeting** (User)
   - Use recording tool
   - Or take live notes

2. **Process Transcript** (Transcript Processing Agent)
   - `*process-transcript {recording}`
   - `*create-meeting-note`

3. **Extract Action Items** (Task Management Agent)
   - `*extract-action-items {meeting_note}`
   - Creates task note for each action item
   - Links task to meeting note
   - Links task to project (if identified)

4. **Assign & Schedule** (User + Task Management Agent)
   - User confirms assignments
   - User sets deadlines
   - Task Management Agent: `*update-task-status`

5. **Track to Completion** (Task Management Agent)
   - Surfaces in daily planning
   - Tracks status changes
   - Alerts on overdue
   - Archives when complete

6. **Report Back** (Optional)
   - Generate meeting follow-up with status
   - Share with attendees

**Duration:** 10-20 minutes post-meeting

---

## 9. Integration Specifications

### 9.1 Transcript Service Integration

**Supported Services:**

1. **Obsidian Transcription Plugin (Whisper ASR)**
   - Local transcription (privacy-focused)
   - High quality
   - No API key required
   - Integration: Read transcription output files

2. **Audio Notes Plugin (Deepgram)**
   - Cloud transcription
   - Very fast
   - Requires Deepgram API key
   - Integration: Read plugin-generated notes

3. **Captain's Log Plugin (Google Gemini)**
   - Cloud transcription + AI summarization
   - Requires Google AI Studio API key
   - Integration: Read plugin-generated notes

4. **Obsidian Whisper Plugin (OpenAI)**
   - Cloud transcription
   - Requires OpenAI API key
   - Integration: Read plugin-generated notes

**Integration Approach:**

- Transcript Processing Agent reads output from these plugins
- Standardizes format for processing
- Adds additional structure and extraction

---

### 9.2 Task Plugin Integration

**Supported Plugins:**

1. **Tasks Plugin**
   - Industry standard for Obsidian task management
   - DataviewJS compatible
   - Integration: Create tasks in compatible format

2. **TODO Plugin (Text-based GTD)**
   - Aggregates tasks across vault
   - GTD workflow support
   - Integration: Use compatible task format

3. **Calendar Plugin**
   - Visualize due dates
   - Integration: Provide due_date in frontmatter

4. **Dataview Plugin**
   - Dynamic task queries
   - Integration: Provide queryable frontmatter

**Task Format Compatibility:**

```markdown
- [ ] Task description (due:: YYYY-MM-DD) (priority:: high) #task
```

---

### 9.3 Neo4j Integration (Temporal Tracking)

**Meeting Event Tracking:**

```cypher
(:MeetingEvent {
  id: string,
  date: datetime,
  duration: integer,
  type: string,
  recording_url: string,
  transcript_source: string
})

(:MeetingEvent)-[:HAD_PARTICIPANT]->(:Person)
(:MeetingEvent)-[:DISCUSSED]->(:Concept)
(:MeetingEvent)-[:RESULTED_IN_DECISION]->(:Decision)
(:MeetingEvent)-[:CREATED_TASK]->(:Task)
(:MeetingEvent)-[:REFERENCED_NOTE]->(:Note)
```

**Task Tracking:**

```cypher
(:Task {
  id: string,
  description: string,
  status: string,
  priority: string,
  created_date: datetime,
  due_date: datetime,
  completed_date: datetime,
  owner: string,
  project: string
})

(:Task)-[:EXTRACTED_FROM]->(:Note)
(:Task)-[:PART_OF]->(:Project)
(:Task)-[:ASSIGNED_TO]->(:Person)
(:Task)-[:DEPENDS_ON]->(:Task)
(:Task)-[STATUS_CHANGED {from, to, timestamp}]->(:Date)
```

**Temporal Queries:**

- "What tasks were created from this meeting?"
- "What decisions led to this task?"
- "Show task completion velocity by project"
- "What meetings discussed concept X?"

---

## 10. Implementation Roadmap

### Phase 1.5: Transcript Processing (2-3 weeks)

**Deliverables:**

- 1 Agent: Transcript Processing Agent
- 8 Tasks: process-transcript, identify-speakers, extract-key-points, extract-action-items-from-transcript, extract-decisions, segment-transcript, create-meeting-note, link-transcript-insights
- 3 Templates: meeting-note-tmpl, transcript-note-tmpl, interview-note-tmpl
- 2 Checklists: transcript-processing-checklist, meeting-note-completeness-checklist
- 1 Workflow: transcript-to-knowledge-workflow
- Integration with 4 transcript plugins

**Acceptance Criteria:**

- Process 1-hour meeting transcript in < 5 minutes
- Speaker identification accuracy > 95%
- Action item extraction rate > 85%
- Key point extraction relevance > 90%
- All meetings create structured notes
- All action items become tracked tasks

---

### Phase 1.5: Task Management (2-3 weeks)

**Deliverables:**

- 1 Agent: Task Management Agent
- 9 Tasks: extract-action-items, create-task-note, update-task-status, link-task-to-project, generate-task-dashboard, daily-task-planning, weekly-task-review, identify-stale-tasks, archive-completed-tasks
- 4 Templates: task-tmpl, project-task-list-tmpl, daily-todo-tmpl, weekly-review-tmpl
- 3 Checklists: task-extraction-checklist, task-completeness-checklist, weekly-review-checklist
- 3 Workflows: gtd-task-management-workflow, meeting-action-items-workflow, daily-planning-workflow
- Integration with Tasks plugin, TODO plugin, Dataview

**Acceptance Criteria:**

- Task extraction accuracy > 90%
- Zero lost action items from meetings
- Daily planning takes < 10 minutes
- Weekly review takes < 60 minutes
- Task-to-project linking accuracy 100%
- GTD workflow fully supported

---

### Testing & Validation

**Test Scenarios:**

1. Process 10 diverse meeting transcripts (different lengths, topics, speaker counts)
2. Extract tasks from 20 different content sources
3. Execute complete GTD workflow (capture → clarify → organize → reflect → engage)
4. Test Neo4j temporal tracking queries
5. Test integration with all supported plugins
6. Measure processing time, extraction accuracy, user satisfaction

**Success Metrics:**

- All transcripts processed successfully
- > 90% task extraction accuracy
- User task completion rate increases 30%+
- Time to process meetings reduces 70%+
- Zero lost action items

---

## Appendices

### Appendix A: Example Meeting Note

```markdown
---
type: meeting_note
meeting_type: planning
date: 2025-11-04T14:00:00Z
duration: 60
attendees: [Alice, Bob, Carol]
recording_url: https://example.com/recording.mp4
transcript_source: whisper
processed_by: transcript-processor-agent
created: 2025-11-04T15:30:00Z
project: [[Q4 Product Launch]]
---

# Q4 Product Launch - Sprint Planning Meeting

## Executive Summary

Team aligned on Q4 priorities, decided to push Feature X to Q1 due to resource constraints, and assigned action items for upcoming sprint with focus on stability and user feedback integration.

## Attendees

- Alice (Product Manager)
- Bob (Engineering Lead)
- Carol (Designer)

## Key Topics Discussed

1. **Q4 Roadmap Review**
   - Reviewed original Q4 commitments
   - Assessed current progress (80% complete)
   - Discussed resource constraints

2. **Feature X Scope Discussion**
   - Technical complexity higher than estimated
   - Dependencies on external API not yet ready
   - User research suggests alternative approach

3. **Sprint Goals**
   - Focus on stability and bug fixes
   - Integrate user feedback from beta
   - Prepare for Q1 feature work

## Decisions Made

- **Decision**: Push Feature X to Q1 2026
  - **Rationale**: Technical dependencies not ready, alternative approach requires more research
  - **Participants**: Alice, Bob, Carol (unanimous)
  - **Alternatives Considered**: Reduce Feature X scope (rejected due to poor UX), hire contractor (rejected due to timeline)
  - **Timestamp**: 00:15:30

- **Decision**: Prioritize bug fixes in current sprint
  - **Rationale**: 15 critical bugs reported by beta users
  - **Participants**: Bob, Alice
  - **Timestamp**: 00:32:10

## Action Items

- [ ] **Research alternative UX approach for Feature X** (@carol, due: 2025-11-11)
  - Context: Needed to inform Q1 planning
  - Source: Carol, 00:18:45

- [ ] **Create bug fix prioritization list** (@bob, due: 2025-11-06)
  - Context: 15 critical bugs need triage
  - Source: Bob, 00:33:20

- [ ] **Schedule Q1 planning meeting** (@alice, due: 2025-11-08)
  - Context: Need to align team on Q1 priorities
  - Source: Alice, 00:55:10

## Open Questions

- **What is timeline for external API availability?**
  - Context: Needed for Feature X implementation
  - Who raised it: Bob
  - Follow-up needed: Contact API vendor

## Key Quotes

> "We can't compromise on user experience just to hit a deadline. Let's do this right in Q1." — Alice (00:16:45)

> "The beta feedback has been overwhelmingly positive, but these bugs are blockers for launch." — Bob (00:32:45)

## Next Steps

- Bug triage meeting on Friday
- Weekly check-ins on Q1 planning progress
- External API vendor call next week

## Timestamp Index

- [00:05:00] Q4 roadmap review begins
- [00:15:30] Decision on Feature X
- [00:25:00] Sprint goals discussion
- [00:32:10] Decision on bug priority
- [00:45:00] Action item assignments
- [00:55:00] Wrap-up and next steps

## Related Notes

- [[Q4 Product Launch Plan]]: Original roadmap
- [[Feature X Design Doc]]: Technical specifications
- [[Beta User Feedback Summary]]: User research informing decisions

## Full Transcript

**Alice** (00:00:15):
Okay, let's get started. Thanks everyone for joining. Today we need to finalize our Q4 roadmap and make some decisions about Feature X...

[Transcript continues...]
```

---

### Appendix B: Example Task Note

```markdown
---
type: task
status: todo
priority: high
due_date: 2025-11-11
created_date: 2025-11-04T15:30:00Z
owner: carol
source: [[Q4 Product Launch - Sprint Planning Meeting]]
project: [[Q4 Product Launch]]
tags: [research, ux, feature-x]
estimate: 1d
gtd_context: @work
energy_level: high
time_available: 2hr+
---

# Research alternative UX approach for Feature X

## Task Description

Research and propose 2-3 alternative UX approaches for Feature X that:

1. Do not rely on external API (can work standalone)
2. Provide comparable user value
3. Can be implemented in Q1 2026 timeline
4. Address user feedback from beta testing

Deliverables:

- 2-3 UX approach proposals with wireframes
- Pros/cons analysis for each approach
- User flow diagrams
- Technical feasibility assessment from engineering

## Context

Feature X was originally planned for Q4 but pushed to Q1 due to external API dependencies. Team decided in sprint planning meeting that we need alternative approach that doesn't rely on external API. This research will inform Q1 planning and ensure we can deliver value to users without external blockers.

See meeting notes: [[Q4 Product Launch - Sprint Planning Meeting]]

## Dependencies

- [ ] Access to beta user feedback summary (completed)
- [ ] Engineering assessment of API alternatives
- Waiting for: Technical feasibility input from Bob

## Progress Notes

- 2025-11-04: Task created from sprint planning meeting
- 2025-11-05: Reviewed beta user feedback, identified 3 key pain points
- 2025-11-06: Sketched initial wireframes for 2 approaches

## Completion Notes

_(To be filled when task completed)_
```

---

**End of Requirements Document**
