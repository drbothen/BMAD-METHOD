<!-- Powered by BMAD™ Core -->

# Plan Screenshots

---

task:
id: plan-screenshots
name: Plan Screenshots
description: Create a comprehensive plan for screenshots including what to capture, when, and how to annotate
persona_default: screenshot-specialist
inputs:

- chapter-outline (outline or content of chapter/section needing screenshots)
- ui-components (optional: list of UI elements to demonstrate)
- target-format (optional: book, documentation, tutorial
- affects screenshot style)
  steps:
- Review chapter content and learning objectives
- Identify UI states and workflows to capture
- Define screenshot sequence and narrative flow
- Specify annotation requirements for each screenshot
- Plan before/after comparisons where applicable
- Determine optimal resolution and format
- Create screenshot checklist with specifications
- Document capture instructions
  output: Screenshot plan with detailed specifications and capture checklist

---

## Purpose

This task helps you create a systematic plan for capturing screenshots, ensuring comprehensive visual coverage that aligns with chapter content and enhances reader understanding. Proper planning prevents missed screenshots, reduces re-work, and maintains visual consistency.

## Prerequisites

Before starting this task:

- Chapter outline or draft content available
- Understanding of chapter learning objectives
- Knowledge of application/UI to be captured
- Target publication format defined (print, web, both)

## Screenshot Planning Principles

### 1. Screenshot Purpose Categories

**Instructional Screenshots:**

- Show step-by-step procedures
- Highlight specific UI elements
- Demonstrate workflows
- One screenshot per major step

**Reference Screenshots:**

- Show complete interfaces
- Provide visual overview
- Document all available options
- Wider, overview captures

**Comparison Screenshots:**

- Before/after states
- Different configuration options
- Version differences
- Side-by-side or sequential

**Error/Warning Screenshots:**

- Show error messages
- Document edge cases
- Demonstrate problem scenarios
- Include solution in annotations

### 2. Screenshot Frequency Guidelines

**Chapter introduction:** 0-1 screenshots (overview)
**Concept explanation:** 1-2 screenshots per concept
**Step-by-step tutorial:** 1 screenshot per 2-3 steps
**Reference section:** 1 screenshot per UI screen
**Troubleshooting:** 1 screenshot per issue

### 3. Quality Standards

**Resolution:**

- Web: 1200-1600px width (Retina-ready)
- Print: 300 DPI at final size
- UI mockups: Native resolution

**Format:**

- PNG: UI screenshots, diagrams
- JPEG: Photos, complex images (smaller file size)
- SVG: Diagrams, illustrations (scalable)

**Consistency:**

- Same window size throughout chapter
- Consistent UI theme (light/dark)
- Same zoom level for similar captures
- Uniform annotation style

## Workflow Steps

### 1. Review Chapter Content and Objectives

Read through chapter and extract:

**Key learning objectives:**

```markdown
## Chapter 3: Building React Components

Learning Objectives:

- Understand functional vs class components
- Create reusable button component
- Implement component props
- Add event handlers
- Style components with CSS modules
```

**Concepts requiring visual demonstration:**

- Component file structure ✓
- JSX syntax highlighting ✓
- Browser rendering result ✓
- React DevTools inspection ✓
- Props being passed ✓

### 2. Identify UI States and Workflows

List all UI states and workflows to capture:

**Example: React Component Tutorial**

**UI States to Capture:**

1. Empty project structure (before)
2. Component file created (code editor)
3. Component imported in App.js (code editor)
4. Default button rendered (browser)
5. Styled button rendered (browser)
6. Button with props (code + browser)
7. Button click handler (code + browser DevTools)
8. Button in different states (hover, active, disabled)

**Workflows to Demonstrate:**

- Creating new component file (3 screenshots)
- Adding props to component (2 screenshots)
- Styling component (3 screenshots)
- Testing component (2 screenshots)

### 3. Define Screenshot Sequence and Flow

Create ordered list matching chapter narrative:

**Screenshot Sequence Plan:**

```markdown
## Screenshot Sequence: Chapter 3

### Section 3.1: Component Basics (4 screenshots)

**Screenshot 3.1.1: Empty Component File**

- Capture: VS Code with empty `Button.jsx` file
- Highlight: File name in sidebar, empty editor
- Annotation: "Create new Button.jsx file in src/components/"
- Resolution: 1400px width
- Format: PNG

**Screenshot 3.1.2: Basic Component Code**

- Capture: VS Code with basic component code
- Highlight: Function declaration, return statement, export
- Annotation: Numbered callouts
  1. "Function component declaration"
  2. "JSX return statement"
  3. "Export for use in other files"
- Resolution: 1400px width
- Format: PNG

**Screenshot 3.1.3: Component Import**

- Capture: App.js showing import statement
- Highlight: Import line, component usage in JSX
- Annotation: Arrow showing import → usage connection
- Resolution: 1400px width
- Format: PNG

**Screenshot 3.1.4: Rendered Button**

- Capture: Browser showing rendered button
- Highlight: Button element in DOM inspector
- Annotation: "Basic button rendered in browser"
- Resolution: 1200px width
- Format: PNG

### Section 3.2: Adding Props (3 screenshots)

**Screenshot 3.2.1: Props Destructuring**

- Capture: Button.jsx with props parameter
- Highlight: Destructuring syntax
- Annotation: "Props allow customization"
- Resolution: 1400px width
- Format: PNG

**Screenshot 3.2.2: Passing Props**

- Capture: App.js passing props to Button
- Highlight: text and variant props
- Annotation: "Pass props from parent component"
- Resolution: 1400px width
- Format: PNG

**Screenshot 3.2.3: Dynamic Rendering**

- Capture: Browser with multiple styled buttons
- Highlight: Primary, secondary, danger variants
- Annotation: "Props change button appearance"
- Resolution: 1200px width
- Format: PNG

[Continue for all sections...]
```

### 4. Specify Annotation Requirements

Plan what annotations each screenshot needs:

**Annotation Types:**

**Numbered Callouts:**

- Use when explaining multiple elements
- Number in reading order (top-left to bottom-right)
- Keep numbers large and clear

**Arrows:**

- Use to show relationships or flow
- Point from label to target
- Use contrasting colors

**Highlights/Boxes:**

- Use to draw attention to specific areas
- Use colored rectangles or rounded boxes
- Semi-transparent for overlays

**Text Labels:**

- Use for simple identification
- Keep concise (3-5 words max)
- Place near target without obscuring

**Example Annotation Plan:**

```markdown
**Screenshot 3.1.2 Annotations:**

Numbered callouts:

1. Point to `function Button()` → "Function component declaration"
2. Point to `return (...)` → "JSX return statement"
3. Point to `export default Button` → "Export for use in other files"

Highlight:

- Yellow box around entire function body
- Label: "Component definition"

Text box:

- Top-right corner
- "File: src/components/Button.jsx"
```

### 5. Plan Before/After Comparisons

Identify transformations to demonstrate:

**Example: Styling Comparison**

```markdown
**Before/After: Button Styling**

Screenshot 3.3A (BEFORE):

- Unstyled button with default browser styles
- Label: "Before: Default browser button"
- Dimensions: 600px width

Screenshot 3.3B (AFTER):

- Styled button with custom CSS
- Label: "After: Custom styled button"
- Dimensions: 600px width

Layout: Side-by-side in final book
```

**Example: State Changes**

```markdown
**State Sequence: Button Interactions**

Screenshot 3.4A: Normal state
Screenshot 3.4B: Hover state (cursor visible)
Screenshot 3.4C: Active/clicked state
Screenshot 3.4D: Disabled state

Layout: 2×2 grid in final book
Note: Cursor must be visible in hover screenshot
```

### 6. Determine Optimal Resolution and Format

Specify technical requirements:

**Resolution Calculation:**

**Print books:**

```
Final printed width: 5 inches
Print DPI requirement: 300 DPI
Required pixels: 5 × 300 = 1500px minimum
Capture at: 1800px (120% for safety)
```

**Web documentation:**

```
Content area width: 800px
Retina display (2×): 1600px
Capture at: 1600-2000px
```

**Both print and web:**

```
Capture at highest requirement: 1800-2000px
Optimize for web: Resize to 1600px
Keep original for print
```

**Format Selection:**

```markdown
| Screenshot Type | Format     | Reason                             |
| --------------- | ---------- | ---------------------------------- |
| Code editor     | PNG        | Text clarity, transparency         |
| Browser UI      | PNG        | Sharp text and icons               |
| Full webpage    | JPEG       | Smaller file size for large images |
| Diagrams        | SVG or PNG | Scalable or high-quality raster    |
| Photos          | JPEG       | Better compression                 |
```

### 7. Create Screenshot Checklist

Generate comprehensive checklist:

```markdown
## Screenshot Capture Checklist: Chapter 3

### Pre-Capture Setup

- [ ] Set VS Code theme to "Light+" (consistency)
- [ ] Set browser zoom to 100%
- [ ] Clear browser cache/cookies (clean state)
- [ ] Use test data (not real user information)
- [ ] Close unnecessary browser tabs
- [ ] Set window size to 1600×1000px
- [ ] Disable notifications
- [ ] Use consistent user profile ("John Doe", "john@example.com")

### Section 3.1: Component Basics

- [ ] Screenshot 3.1.1: Empty Button.jsx file
  - File visible in sidebar
  - Editor shows empty file with cursor
  - No errors in console
- [ ] Screenshot 3.1.2: Basic component code
  - Code syntax highlighted
  - No scroll bars visible
  - Line numbers visible
- [ ] Screenshot 3.1.3: Component import in App.js
  - Import statement at top
  - Component usage visible
  - Auto-import indicator (if relevant)
- [ ] Screenshot 3.1.4: Rendered button in browser
  - Browser DevTools open (Elements tab)
  - Button element highlighted in DOM tree
  - No console errors

### Section 3.2: Adding Props

- [ ] Screenshot 3.2.1: Props destructuring in code
  - Syntax highlighting clear
  - Type hints visible (TypeScript)
- [ ] Screenshot 3.2.2: Passing props from parent
  - Both prop name and value visible
  - JSX syntax highlighted
- [ ] Screenshot 3.2.3: Multiple button variants
  - All three variants visible (primary, secondary, danger)
  - Adequate spacing between buttons
  - Consistent rendering

[Continue for all sections...]

### Post-Capture Quality Check

- [ ] All screenshots captured at specified resolution
- [ ] No personal/sensitive information visible
- [ ] Consistent window size across screenshots
- [ ] No typos in code samples
- [ ] Clean, professional appearance
- [ ] Saved with descriptive filenames (chapter-section-description.png)
- [ ] Organized into chapter folders
```

### 8. Document Capture Instructions

Provide step-by-step instructions for capturing:

````markdown
## Capture Instructions: Chapter 3

### Setup Environment

1. **Code Editor Setup:**

   ```bash
   # Clone sample project
   git clone https://github.com/example/react-tutorial.git
   cd react-tutorial
   git checkout chapter-3-start

   # Install dependencies
   npm install

   # Start development server
   npm start
   ```
````

2. **VS Code Configuration:**
   - Theme: "Light+ (default light)"
   - Font: "Fira Code", size 14
   - Window size: 1600×1000px
   - Zoom: 100%
   - Minimap: Disabled
   - Activity bar: Visible

3. **Browser Configuration:**
   - Browser: Chrome
   - Window size: 1400×900px
   - Zoom: 100%
   - Extensions: React DevTools only
   - Profile: "Tutorial User"

### Capturing Process

**For Code Editor Screenshots:**

1. Open file in VS Code
2. Adjust scroll position (relevant code at top)
3. Clear selection (click empty area)
4. Hide terminal panel (Cmd+J)
5. Capture with: Cmd+Shift+4 (macOS) or Snipping Tool (Windows)
6. Save as: `ch3-1-component-code.png`

**For Browser Screenshots:**

1. Navigate to: http://localhost:3000
2. Open DevTools (F12)
3. Position DevTools (dock right, 400px width)
4. Select relevant element in Elements tab
5. Ensure no hover states active
6. Capture browser window
7. Save as: `ch3-4-rendered-button.png`

**For Before/After Comparisons:**

1. Capture "before" state first
2. Save immediately with "-before" suffix
3. Make change (apply CSS, modify code)
4. Wait for hot reload (if applicable)
5. Capture "after" state
6. Save with "-after" suffix
7. Verify both files have identical dimensions

### Special Captures

**Hover States:**

- Activate hover by positioning cursor
- Use screenshot tool with timer (5 sec delay)
- Keep cursor visible in screenshot
- Filename: `*-hover.png`

**Error States:**

- Trigger error condition
- Ensure error message fully visible
- Capture console output if relevant
- Filename: `*-error.png`

**Responsive Layouts:**

- Set browser to specific width (375px mobile, 768px tablet)
- Use Chrome DevTools device emulation
- Show device frame if helpful
- Filename: `*-mobile.png` or `*-tablet.png`

````

## Success Criteria

Screenshot plan is complete when:

- [ ] All chapter sections have screenshot specifications
- [ ] Each screenshot has clear purpose stated
- [ ] Annotation requirements specified for each screenshot
- [ ] Capture sequence matches chapter narrative flow
- [ ] Resolution and format defined for each screenshot
- [ ] Before/after comparisons identified
- [ ] Complete capture checklist created
- [ ] Environment setup instructions documented
- [ ] File naming convention defined
- [ ] Quality standards specified

## Output Format

```markdown
# Screenshot Plan: [Chapter Title]

## Overview

- **Chapter:** [Number and title]
- **Total Screenshots:** [Count]
- **Estimated Capture Time:** [Hours]
- **Target Format:** [Print/Web/Both]
- **Standard Resolution:** [Width×Height]
- **Annotation Tool:** [Snagit/Skitch/Other]

## Environment Setup

[Setup instructions]

## Screenshot Specifications

### Section [X.X]: [Section Title]

**Screenshot [X.X.X]: [Description]**
- **Purpose:** [Why this screenshot is needed]
- **Capture:** [What to show]
- **Highlight:** [Elements to emphasize]
- **Annotations:** [Callouts, arrows, labels]
- **Resolution:** [Dimensions]
- **Format:** [PNG/JPEG/SVG]
- **Filename:** [Naming pattern]
- **Notes:** [Special instructions]

[Repeat for all screenshots]

## Capture Checklist

[Comprehensive checklist]

## Quality Standards

- Resolution: [Standard]
- Format: [Standard]
- Annotation style: [Standard]
- File naming: [Convention]
- Organization: [Folder structure]

## Appendix

### File Naming Convention
`ch[chapter]-[section]-[sequence]-[description].[ext]`

Example: `ch3-2-1-props-destructuring.png`

### Folder Structure
````

screenshots/
├── chapter-03/
│ ├── raw/ # Original captures
│ ├── annotated/ # With annotations
│ └── optimized/ # Final web-optimized

```

```

## Common Pitfalls to Avoid

**❌ Capturing screenshots after writing chapter:**

- Results in missing shots, inconsistent style
- Requires re-setting up environment

✅ **Plan before capturing:**

- Complete plan ensures nothing missed
- Maintains consistency

**❌ Inconsistent window sizes:**

- Screenshots look unprofessional
- Difficult to format in book

✅ **Standardize capture dimensions:**

- Same window size for all code editor shots
- Same browser size for all UI shots

**❌ No annotation planning:**

- Inconsistent annotation styles
- Missed important callouts

✅ **Specify annotations in plan:**

- Consistent visual language
- Clear communication

**❌ Capturing with real user data:**

- Privacy concerns
- Unprofessional appearance

✅ **Use test data:**

- "John Doe", "jane.smith@example.com"
- Placeholder images

## Examples

### Example 1: Tutorial Chapter Screenshot Plan

**Chapter:** "Building a Todo App with React"

**Screenshot Plan Summary:**

- Total screenshots: 18
- Breakdown: 12 code editor, 6 browser UI
- Estimated time: 3 hours
- Target: Print (300 DPI) and web

**Key Screenshots:**

1. Project structure (VS Code sidebar)
2. App.jsx initial code
3. TodoItem component
4. TodoList component
5. Add todo form
6. Browser: Empty todo list
7. Browser: List with 3 todos
8. Browser: Completed todo (strikethrough)
9. Browser: Delete confirmation
10. Chrome DevTools: React component tree

**Before/After Comparisons:**

- Unstyled vs styled todo list (2 screenshots)
- Empty state vs populated state (2 screenshots)

### Example 2: API Documentation Screenshot Plan

**Chapter:** "REST API Endpoints"

**Screenshot Plan Summary:**

- Total screenshots: 12
- Breakdown: 8 API tool, 4 code samples
- Tool: Postman
- Format: PNG, 1600px width

**Key Screenshots:**

1. Postman: GET /users request
2. Postman: Response with user array
3. Postman: POST /users request body
4. Postman: 201 Created response
5. Postman: Authentication header
6. Postman: 401 Unauthorized error
7. Code: Express route handler
8. Code: Middleware chain

**Annotations:**

- Request method highlighted in color
- Response status code in large callout
- Authentication token redacted

## Next Steps

After creating screenshot plan:

1. Review plan with chapter content author
2. Set up environment per specifications
3. Use `annotate-images.md` task for adding annotations
4. Use `optimize-visuals.md` task for final optimization
5. Run `execute-checklist.md` with `screenshot-quality-checklist.md`
6. Update chapter draft with screenshot placeholders
7. Organize screenshots per folder structure
