<!-- Powered by BMAD™ Core -->

# Create Diagram Specification

---

task:
id: create-diagram-spec
name: Create Diagram Specification
description: Design technical diagram specifications for visual documentation
persona_default: screenshot-specialist
inputs: - concept or process to visualize - chapter-section where diagram will appear - target-audience
steps: - Identify concept or process that needs visualization - Choose appropriate diagram type (flowchart, sequence, architecture, etc.) - List all key elements and components - Define relationships and flows between elements - Plan labels and annotations - Specify style requirements (colors, shapes, etc.) - Write alternative text description for accessibility - Define size and format requirements - Review for clarity and completeness - Validate diagram supports text explanation - Use template diagram-spec-tmpl.yaml with create-doc.md task - Run execute-checklist.md with diagram-clarity-checklist.md
output: docs/diagrams/{{diagram_id}}-spec.md

---

## Purpose

This task guides you through creating comprehensive diagram specifications that visual designers or diagram tools can use to create clear, effective technical diagrams. The result is a complete specification that ensures diagrams clarify concepts and meet accessibility standards.

## Prerequisites

Before starting this task:

- Have clear understanding of concept to visualize
- Know where diagram will appear in book
- Access to technical-writing-standards.md knowledge base
- Understand target audience's technical level

## Workflow Steps

### 1. Identify Concept to Visualize

Determine what needs a diagram:

- Complex process or workflow
- System architecture or components
- Data flow or transformation
- Decision tree or algorithm
- Timeline or sequence
- Comparison or relationship

**Ask:**

- What concept is hard to explain with text alone?
- Where do readers get confused?
- What mental model are you building?
- Would a visual clarify this immediately?

### 2. Choose Diagram Type

Select the most effective diagram type:

**Process/Flow Diagrams:**

- **Flowchart**: Decision trees, algorithms, step-by-step processes
  - Use for: Control flow, decision logic, sequential processes
- **Sequence diagram**: Interactions over time, API calls, message passing
  - Use for: Time-based interactions, protocol flows, object communication
- **Activity diagram**: Workflows, user journeys, parallel processes
  - Use for: Complex workflows, concurrent activities, swimlane responsibilities
- **Data flow diagram**: Data movement through systems
  - Use for: Data transformations, ETL processes, information flow

**Structure Diagrams:**

- **Architecture diagram**: System components and relationships
  - Use for: High-level system design, microservices, deployment
- **Class diagram**: Object-oriented design, relationships
  - Use for: Code structure, inheritance, composition
- **Entity-relationship diagram**: Database schemas
  - Use for: Data models, database design, relationships
- **Component diagram**: Software architecture
  - Use for: Module dependencies, package structure, interfaces

**Other:**

- **State diagram**: State machines, lifecycle
  - Use for: Object states, transitions, event-driven behavior
- **Network diagram**: Infrastructure, deployment topology
  - Use for: Server architecture, network topology, cloud resources
- **Timeline**: Historical progression, versioning
  - Use for: Evolution of technology, release history, migration paths

**Selection criteria:**

- What type best represents this concept?
- What conventions will readers recognize?
- What tools are available for creation?

### 3. List Key Elements

Identify all components that must appear:

**Actors/Entities:**

- Users, systems, services
- External integrations
- Data stores

**Processes/Functions:**

- Operations, transformations
- Business logic, calculations
- API calls, functions

**Data:**

- Databases, caches, files
- Messages, requests, responses
- Configuration, state

**Control:**

- Decision points (if/else, switch)
- Loops (for, while)
- Error handlers, fallbacks
- Start and end points

For each element, specify:

- Name/label text
- Shape or symbol (rectangle, circle, diamond, etc.)
- Color or styling (if it conveys meaning)
- Size relative to other elements

### 4. Define Relationships and Flows

Map how elements connect:

**Connection types:**

- Solid arrow: Direct flow, data transfer, control flow
- Dashed arrow: Indirect relationship, optional flow
- Bidirectional arrow: Two-way communication
- No arrow (line only): Association, grouping

For each connection:

- Start and end points
- Direction of flow
- Sequence or order (number steps if needed)
- Conditions or triggers
- Labels (what's flowing: data type, message, protocol)

**Example:**
"User → (HTTP POST) → API Gateway → (JWT validation) → Auth Service → (SQL query) → Database → (AuthToken) → User"

### 5. Plan Labels and Annotations

Specify all text elements:

**Element labels:**

- Keep concise (2-4 words max)
- Use consistent terminology
- Match glossary terms

**Edge labels:**

- Data types (JSON, XML, binary)
- Protocols (HTTP, WebSocket, gRPC)
- Methods (GET, POST, publish, subscribe)
- Conditions ("if authenticated", "on error")

**Callout boxes:**

- Important notes that don't fit in main flow
- Timing information ("~200ms")
- Error conditions
- External constraints

**Step numbers:**

- For sequential processes
- Match numbered steps in text if applicable

**Legend:**

- Define special symbols
- Explain color coding
- Clarify line types

Keep labels brief - detailed explanation belongs in body text.

### 6. Specify Style Requirements

Define visual styling:

**Color scheme:**

- Consistent with other book diagrams
- Sufficient contrast for accessibility (WCAG AA: 4.5:1 for text)
- Meaningful use (green=success, red=error, blue=external system)
- Consider grayscale printing

**Shape conventions:**

- Rectangles: Processes, operations
- Rounded rectangles: Start/end points
- Diamonds: Decisions
- Cylinders: Databases
- Clouds: External services
- Stick figures: Actors

**Line styles:**

- Solid: Primary flow
- Dashed: Secondary or optional
- Dotted: Boundary or grouping
- Bold: Critical path

**Typography:**

- Font family (consistent with book)
- Minimum font size (10-12pt for readability)
- Bold for emphasis
- Monospace for code/variables

**Layout:**

- Left-to-right, top-to-bottom flow (Western reading)
- Adequate spacing (no cramming)
- Alignment and grid structure
- Balanced composition

### 7. Define Size and Format Requirements

Specify technical requirements:

**Dimensions:**

- Width × height (pixels for digital, inches for print)
- Aspect ratio
- Margins and padding

**Resolution:**

- 300 DPI minimum for print
- 150 DPI acceptable for web
- Vector format preferred (SVG, PDF)

**File format:**

- SVG: Scalable, best for web and print
- PNG: Raster with transparency
- PDF: Vector, preserves fonts
- Format depends on publisher requirements

**Placement:**

- Full page landscape
- Half page inline
- Wrap with text
- Facing page reference

### 8. Write Alternative Text Description

Create complete alt text for accessibility:

**Include:**

- Diagram purpose and context
- Main flow or structure
- Key components listed
- Important relationships
- Outcome or end state

**Example:**
"Sequence diagram showing OAuth2 authentication flow: User initiates login at web app. Web app redirects to OAuth provider. User enters credentials at OAuth provider. OAuth provider validates credentials and returns authorization code to web app. Web app exchanges code for access token. User is now authenticated with access token stored."

Alt text should enable someone who can't see the diagram to understand the concept.

**Guidelines:**

- Describe diagram type first
- Follow the flow logically
- Mention all critical elements
- Keep it concise but complete (100-200 words)
- Avoid "This diagram shows..." (screen readers already say "image")

### 9. Review for Clarity

Validate the specification:

- [ ] Does every element have a purpose?
- [ ] Are labels clear and concise?
- [ ] Is the flow easy to follow?
- [ ] Will this clarify the text explanation?
- [ ] Is complexity appropriate for audience?
- [ ] Is a legend needed?
- [ ] Does it meet accessibility standards?

### 10. Generate Diagram Specification

Use the create-doc.md task with diagram-spec-tmpl.yaml template to create the structured diagram specification document.

### 11. Validate with Checklist

Run checklist:

- diagram-clarity-checklist.md - Ensure diagram will be clear and effective

## Success Criteria

Completed diagram specification should have:

- [ ] Clear purpose and context defined
- [ ] Appropriate diagram type selected
- [ ] All elements listed with labels
- [ ] Relationships and flows defined
- [ ] Style requirements specified
- [ ] Size and format requirements defined
- [ ] Complete alternative text written
- [ ] Accessibility requirements met
- [ ] Clarity checklist passed
- [ ] Sufficient detail for designer/tool to create diagram

## Common Pitfalls to Avoid

- **Too complex**: Simplify, split into multiple diagrams if needed
- **Illegible labels**: Text too small or colors too similar
- **Missing legend**: Don't assume readers know your symbols
- **Poor flow direction**: Arrows should guide eye naturally
- **Inconsistent styling**: Use same shapes/colors for same concepts
- **No alt text**: Accessibility is required, not optional
- **Overcrowded**: Leave white space, don't cram everything in
- **Unclear purpose**: Diagram should clarify one specific concept

## Notes and Warnings

- **Accessibility is mandatory**: Alt text and color contrast are not optional
- **Test in grayscale**: Ensure diagram works without color
- **Keep it simple**: One diagram = one concept
- **Follow conventions**: Don't invent new symbol meanings
- **High resolution**: Low-res diagrams look unprofessional in print
- **Version control**: Maintain source files (not just rendered images)

## Next Steps

After creating diagram specification:

1. Create diagram using design tool or diagram software
2. Review rendered diagram against specification
3. Validate alt text accurately describes final diagram
4. Test accessibility (color contrast, screen reader)
5. Insert into chapter with figure number and caption
6. Reference diagram in body text ("see Figure 3.2")
