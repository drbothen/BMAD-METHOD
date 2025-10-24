<!-- Powered by BMAD™ Core -->

# Design Diagram Set

---

task:
id: design-diagram-set
name: Design Diagram Set
description: Plan comprehensive set of diagrams for a chapter with consistent visual style
persona_default: tutorial-architect
inputs:

- chapter-number
- chapter-content
- concepts-to-visualize
  steps:
- Review chapter concepts needing visualization
- Identify diagram types needed (architecture, flow, sequence, class, ER)
- Create diagram spec for each using create-diagram-spec task
- Determine common visual style (colors, fonts, shapes)
- Plan diagram progression (simple → complex)
- Ensure diagrams support text not replace it
- Write alternative text for accessibility
- Plan for diagram updates (editable source files)
- Run execute-checklist.md with diagram-clarity-checklist.md
- Run execute-checklist.md with accessibility-checklist.md
- Create implementation plan
  output: docs/diagrams/chapter-{{n}}-diagram-plan.md

---

## Purpose

Design a cohesive set of diagrams that enhance chapter understanding through consistent visual communication.

## Workflow Steps

### 1. Review Concepts Needing Visualization

Identify what to diagram:

**Good candidates for diagrams:**

- System architecture
- Data flow
- Process workflows
- Class relationships
- Database schemas
- API request/response cycles
- Component interactions

**Poor candidates:**

- Simple lists (use bullets)
- Linear sequences (use numbered steps)
- Obvious concepts (text is clearer)

### 2. Identify Diagram Types

**Common Technical Diagram Types:**

- **Architecture diagrams**: System components and relationships
- **Flowcharts**: Decision trees and process flows
- **Sequence diagrams**: Interaction over time
- **Class diagrams**: Object-oriented relationships
- **ER diagrams**: Database entity relationships
- **State diagrams**: State transitions
- **Network diagrams**: Infrastructure and connections

### 3. Determine Visual Style

**Consistency elements:**

```yaml
Visual Style Guide:
  Colors:
    primary: "#2563EB" (blue)
    secondary: "#10B981" (green)
    warning: "#F59E0B" (orange)
    error: "#EF4444" (red)
    neutral: "#6B7280" (gray)

  Fonts:
    headings: "Inter, sans-serif"
    labels: "Inter, sans-serif"
    code: "JetBrains Mono, monospace"

  Shapes:
    services: Rounded rectangles
    databases: Cylinders
    users: Stick figures/icons
    external-systems: Dashed borders

  Arrows:
    data-flow: Solid lines
    optional-flow: Dashed lines
    bidirectional: Double-headed arrows
```

### 4. Plan Diagram Progression

Build complexity incrementally:

**Example progression for API chapter:**

```markdown
1. Figure 3.1: Simple HTTP request/response (2 boxes)
2. Figure 3.2: Client-Server architecture (4 components)
3. Figure 3.3: Multi-tier architecture with database (6 components)
4. Figure 3.4: Complete system with caching and load balancer (10+ components)
```

### 5. Ensure Diagrams Support Text

Diagrams complement, not replace:

```markdown
✅ Good integration:
"The client sends a request to the API server (Figure 3.1), which queries the
database before returning a response. This request-response cycle..."

❌ Poor integration:
"See Figure 3.1." [end of explanation]
```

### 6. Write Alternative Text

Accessibility requirement:

```markdown
![Alternative text: Sequence diagram showing client sending HTTP GET request
to API server, server querying database, database returning data, and server
sending JSON response back to client]
```

### 7. Plan for Updates

Use editable sources:

**Recommended tools:**

- draw.io (free, open format)
- Lucidchart (professional)
- PlantUML (code-based, version-controllable)
- Mermaid (markdown-based)

**Save source files:**

```
diagrams/
├── sources/
│   ├── chapter-03-architecture.drawio
│   ├── chapter-03-sequence.puml
│   └── chapter-03-er-diagram.drawio
└── exports/
    ├── chapter-03-architecture.png
    ├── chapter-03-sequence.png
    └── chapter-03-er-diagram.png
```

### 8. Create Implementation Plan

**Diagram Set Plan Template:**

```markdown
# Chapter 3 Diagram Plan

## Diagram 3.1: Simple Request-Response

- **Type**: Sequence diagram
- **Purpose**: Introduce HTTP basics
- **Complexity**: Simple (2 actors)
- **Tool**: PlantUML
- **Alt text**: "HTTP request-response between client and server"

## Diagram 3.2: API Architecture

- **Type**: Architecture diagram
- **Purpose**: Show system components
- **Complexity**: Intermediate (5 components)
- **Tool**: draw.io
- **Alt text**: "Three-tier architecture with client, API server, and database"

## Diagram 3.3: Authentication Flow

- **Type**: Flowchart
- **Purpose**: Illustrate JWT authentication
- **Complexity**: Advanced (decision points, multiple paths)
- **Tool**: Lucidchart
- **Alt text**: "Flowchart showing login, token generation, and API access"

## Visual Consistency

- All diagrams use same color scheme
- Same font (Inter) for labels
- Consistent icon style
- 300 DPI export resolution
```

## Success Criteria

- [ ] Concepts needing visualization identified
- [ ] Diagram types selected appropriately
- [ ] Diagram specs created for each
- [ ] Visual style guide defined
- [ ] Progression from simple to complex
- [ ] Diagrams complement text
- [ ] Alternative text written
- [ ] Editable source files planned
- [ ] Diagram clarity checklist passed
- [ ] Accessibility checklist passed

## Next Steps

1. Create individual diagrams using create-diagram-spec task
2. Review diagrams with technical reviewer
3. Export at required resolution
4. Integrate into chapter
