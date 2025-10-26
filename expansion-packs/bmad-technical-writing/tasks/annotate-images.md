<!-- Powered by BMAD™ Core -->

# Annotate Images

---

task:
id: annotate-images
name: Annotate Images
description: Add professional annotations to screenshots including arrows, callouts, labels, highlights, and captions
persona_default: screenshot-specialist
inputs: - image-path (path to image file to annotate) - annotation-specs (description of what annotations to add) - output-path (optional: where to save annotated image)
steps: - Load image in annotation tool - Add numbered callouts for multi-step explanations - Add arrows to show relationships or flow - Add text labels for identification - Highlight important areas with boxes or overlays - Blur or redact sensitive information - Add figure caption and alt text - Save in appropriate format - Verify annotations are clear and professional
output: Annotated image with caption and alt text

---

## Purpose

This task helps you add clear, professional annotations to screenshots and images that guide readers' attention and explain key elements. Well-annotated images significantly improve comprehension and reduce reader confusion.

## Prerequisites

Before starting this task:

- Raw screenshot or image captured
- Screenshot plan with annotation specifications (or clear requirements)
- Annotation tool installed (Snagit, Skitch, Preview, GIMP, etc.)
- Understanding of what needs to be highlighted/explained

## Recommended Annotation Tools

### macOS

**Skitch (Free):**

- Pros: Simple, quick annotations
- Best for: Basic arrows, text, highlights
- Cons: Limited styling options

**Preview (Built-in):**

- Pros: Free, always available
- Best for: Basic shapes, text, arrows
- Cons: Limited advanced features

**Snagit ($50):**

- Pros: Professional features, templates
- Best for: Complex annotations, consistency
- Cons: Paid software

**Pixelmator Pro ($50):**

- Pros: Advanced image editing + annotations
- Best for: High-quality professional work
- Cons: Steeper learning curve

### Windows

**Snagit ($50):**

- Same as macOS version

**Snipping Tool / Snip & Sketch (Built-in):**

- Pros: Free, simple
- Best for: Basic annotations
- Cons: Limited features

**Paint.NET (Free):**

- Pros: More features than Paint
- Best for: Moderate complexity
- Cons: Not as polished as paid tools

**Greenshot (Free, Open Source):**

- Pros: Powerful, customizable
- Best for: Technical screenshots
- Cons: Interface takes learning

### Cross-Platform

**GIMP (Free, Open Source):**

- Pros: Fully-featured image editor
- Best for: Maximum control
- Cons: Complex for simple tasks

**Figma (Free tier available):**

- Pros: Vector-based, collaborative
- Best for: Design-heavy projects
- Cons: Requires account, online

## Annotation Types and Best Practices

### 1. Numbered Callouts

**Use when:** Explaining multiple elements in sequence

**Best practices:**

- Number in reading order (left-to-right, top-to-bottom)
- Use large, clear numbers (18-24pt)
- Use contrasting colors (white number on dark circle)
- Keep callout text concise (one sentence)
- Place callouts outside image area when possible

**Example:**

```
┌─────────────────────────────────┐
│  [Code Editor Window]           │
│                                 │
│  1━━━> function Button() {     │
│          return (              │
│  2━━━>     <button>Click</button> │
│          );                     │
│  3━━━> }                        │
│                                 │
└─────────────────────────────────┘

1. Function component declaration
2. JSX return statement
3. Export for reuse
```

### 2. Arrows

**Use when:** Showing relationships, flow, or pointing to specific elements

**Types:**

**Straight arrows:**

- Use for direct relationships
- Point from label to target

**Curved arrows:**

- Use when avoiding other elements
- Show flow or progression

**Styles:**

**Thick arrows (4-6px):**

- Use for primary emphasis
- Main workflow steps

**Thin arrows (2-3px):**

- Use for secondary information
- Supporting details

**Best practices:**

- Use bright, contrasting colors (red, orange, cyan)
- Ensure arrowhead is clearly visible
- Don't cross other arrows when possible
- Keep arrow paths simple

### 3. Highlights and Boxes

**Use when:** Drawing attention to specific areas

**Rectangle highlights:**

- Outline important sections
- Use colored borders (2-4px)
- No fill or semi-transparent fill (20-30% opacity)

**Rounded rectangles:**

- Softer, friendlier appearance
- Good for UI elements

**Circles/Ovals:**

- Draw attention to small elements
- Button, icon, or menu item

**Best practices:**

- Use semi-transparent fills to keep underlying content visible
- Choose colors that contrast with image but don't clash
- Common colors: Red/Orange (errors, warnings), Green (success, correct), Blue (information), Yellow (highlights)

**Example color scheme:**

```
Primary highlight: #FF6B6B (red) - Main focus
Secondary highlight: #4ECDC4 (cyan) - Supporting element
Success highlight: #95E1D3 (green) - Correct way
Warning highlight: #FFE66D (yellow) - Caution
```

### 4. Text Labels

**Use when:** Identifying elements simply

**Best practices:**

- Use clear, readable fonts (sans-serif)
- Font size: 14-18pt for labels
- Add background box for contrast (white with slight transparency)
- Keep text brief (1-5 words)
- Use title case or sentence case consistently

**Text box styling:**

```
Background: White with 80-90% opacity
Border: 1px gray or colored border
Padding: 4-8px around text
Font: Arial, Helvetica, or system sans-serif
Color: Dark gray (#333) or black
```

### 5. Blur and Redaction

**Use when:** Hiding sensitive information

**Blur:**

- Use for moderately sensitive info (usernames, non-critical data)
- Gaussian blur with 10-20px radius
- Ensure completely unreadable

**Pixelation:**

- Alternative to blur
- 8-16px block size
- More obvious redaction

**Solid overlay:**

- Use for highly sensitive info (passwords, API keys, personal data)
- Black or dark gray rectangle
- 100% opacity
- Add text: "[REDACTED]" or "[HIDDEN FOR SECURITY]"

**Best practices:**

- Never rely on blur alone for truly sensitive data
- Test readability: zoom in to verify unreadable
- Use black bars for critical security info
- Consider using placeholder data instead of redaction

### 6. Figure Captions

**Use when:** Every screenshot needs a caption

**Caption structure:**

```
Figure [number]: [Brief description of what the image shows]
```

**Examples:**

**Good captions:**

- "Figure 3.1: Button component code with props destructuring"
- "Figure 5.4: User dashboard showing active projects and notifications"
- "Figure 8.2: Error message displayed when authentication fails"

**Poor captions:**

- "Screenshot" (too vague)
- "The code" (not specific)
- "Button" (too brief)

**Best practices:**

- Be specific and descriptive
- Match chapter/section numbering
- Write in present tense
- Include key identifying information
- Keep to 1-2 lines

### 7. Alt Text

**Use when:** Always (for accessibility)

**Alt text guidelines:**

- Describe what the image shows
- Include relevant text from image
- Mention key visual elements
- Keep under 150 characters when possible
- Don't start with "Image of..." or "Picture of..."

**Examples:**

**Screenshot of code editor:**

```
Alt text: "React Button component function with props parameter,
          JSX return statement, and default export"
```

**Screenshot of UI:**

```
Alt text: "Dashboard interface showing three project cards,
          navigation sidebar, and user profile menu in top-right corner"
```

**Diagram:**

```
Alt text: "Flowchart showing user authentication process:
          login form, validate credentials, check database,
          issue token, redirect to dashboard"
```

## Workflow Steps

### 1. Load Image in Annotation Tool

**Preparation:**

- Create backup of original image (never annotate original)
- Open in annotation tool
- Set zoom to 100% for accurate placement
- Prepare annotation specifications

### 2. Add Numbered Callouts

**For multi-step explanations:**

**Step-by-step:**

1. Identify elements to call out (from annotation specs)
2. Determine numbering order (reading flow)
3. Place numbered markers on or near elements
4. Add callout text below or beside image

**Example workflow:**

```markdown
**Annotating code screenshot with 3 callouts:**

1. Add circle with number "1" pointing to function declaration
2. Add circle with number "2" pointing to return statement
3. Add circle with number "3" pointing to export statement
4. Add text box below image:
   "1. Function component declaration 2. JSX return statement 3. Export for use in other files"
```

**Callout placement tips:**

- Place in margin if possible (doesn't obscure content)
- Use leader lines/arrows if callout is far from target
- Maintain consistent callout style throughout book

### 3. Add Arrows

**For showing relationships:**

**Arrow creation:**

1. Identify start and end points
2. Choose arrow style (straight/curved)
3. Set arrow thickness and color
4. Draw from source to target
5. Ensure arrowhead clearly points to target

**Example scenarios:**

**Showing flow:**

```
[Input Field] ──> [Validation] ──> [Database] ──> [Response]
```

**Showing relationships:**

```
[Parent Component]
    ↓ (Props)
[Child Component]
```

**Pointing to specific element:**

```
"Click here" ──────> [Submit Button]
```

### 4. Add Text Labels

**For simple identification:**

**Label creation:**

1. Select text tool
2. Choose font (sans-serif, 14-18pt)
3. Add background box for contrast
4. Type concise label (1-5 words)
5. Position near target element

**Examples:**

```
┌─────────────────────┐
│ [Button Component]  │  ← Text label with background
│                     │
│  ┌─────────────┐    │
│  │   Submit    │    │
│  └─────────────┘    │
│   Primary Button    │  ← Label
└─────────────────────┘
```

### 5. Highlight Important Areas

**For emphasis:**

**Highlight creation:**

1. Select shape tool (rectangle/circle)
2. Set border color and thickness (3-4px)
3. Set fill to semi-transparent (20-30% opacity) or no fill
4. Draw around target area
5. Send to back layer (don't obscure content)

**Example highlighting:**

```
┌─────────────────────────────────┐
│  import React from 'react';     │
│  ╔═══════════════════════════╗  │  ← Red highlight box
│  ║ function Button({ text }) { ║  │
│  ║   return <button>{text}</button>; ║
│  ║ }                           ║  │
│  ╚═══════════════════════════╝  │
│  export default Button;         │
└─────────────────────────────────┘
```

### 6. Blur or Redact Sensitive Information

**For privacy/security:**

**Redaction workflow:**

1. Identify sensitive information
   - Passwords, API keys, tokens
   - Personal email addresses, phone numbers
   - Real usernames (use test data instead)
   - Internal URLs, IP addresses
2. Select redaction method:
   - Blur: Moderately sensitive (Gaussian blur 15px)
   - Pixelate: Alternative to blur (10px blocks)
   - Black bar: Highly sensitive (100% opacity rectangle)
3. Apply redaction
4. Zoom in to verify completely unreadable

**Example redaction:**

```
Before:
Username: john.doe@company.com
API Key: sk_live_51H8xF2KlP0...

After:
Username: john.doe@company.com
API Key: [████████████████] (REDACTED FOR SECURITY)
```

**Best practice:**
Use test/example data instead of redacting:

```
Better approach:
Username: demo-user@example.com
API Key: sk_test_example1234567890
```

### 7. Add Figure Caption

**For every image:**

**Caption format:**

```
Figure [Chapter].[Section]: [Description]

Example:
Figure 3.2: Button component with props destructuring and JSX return
```

**Caption placement:**

- Below image (standard)
- Consistent formatting throughout book
- Match publisher style guide

**Creating caption:**

1. Determine figure number (chapter.section.sequence)
2. Write descriptive caption (1-2 sentences)
3. Format consistently (font, size, style)
4. Place below image with proper spacing

### 8. Add Alt Text

**For accessibility:**

**Alt text creation:**

1. Describe image content
2. Include relevant text shown in image
3. Mention key visual elements
4. Keep concise but complete
5. Store in image metadata or documentation

**Example alt text for different image types:**

**Code screenshot:**

```
Alt: "JavaScript function named Button with props parameter,
     returning JSX button element with text from props"
```

**UI screenshot:**

```
Alt: "Web application dashboard with sidebar navigation on left,
     three project cards in main area, and user menu in top-right"
```

**Diagram:**

```
Alt: "Architecture diagram showing client connecting to API gateway,
     which routes to microservices for auth, users, and orders"
```

### 9. Save in Appropriate Format

**Format selection:**

**PNG (Recommended for most screenshots):**

- Lossless compression
- Supports transparency
- Best for text, UI, code
- Larger file size

**JPEG (For large images):**

- Lossy compression
- Smaller file size
- Good for photos, complex images
- NOT for text (artifacts)

**Saving workflow:**

1. Save annotated version
2. Use descriptive filename: `ch3-fig2-button-component-annotated.png`
3. Maintain original unannotated version
4. Check file size (optimize if needed)

**File naming convention:**

```
Pattern: ch[chapter]-fig[number]-[description]-annotated.[ext]

Examples:
ch3-fig1-project-structure-annotated.png
ch5-fig4-error-handling-annotated.png
ch7-fig2-api-response-annotated.png
```

### 10. Verify Annotations

**Quality check:**

- [ ] All annotations clearly visible
- [ ] Colors contrast well with image
- [ ] Text is readable (zoom to 100%)
- [ ] No spelling errors in labels/captions
- [ ] Annotations don't obscure important content
- [ ] Style consistent with other annotated images
- [ ] Numbered callouts in logical order
- [ ] Arrows point to correct targets
- [ ] Sensitive information properly redacted
- [ ] Figure caption and alt text added

## Success Criteria

Annotated image is complete when:

- [ ] All required annotations added per specification
- [ ] Annotations are clear and professional
- [ ] Text is readable and error-free
- [ ] Colors provide good contrast
- [ ] Important content not obscured
- [ ] Sensitive information redacted
- [ ] Figure caption added
- [ ] Alt text created
- [ ] Saved in appropriate format with descriptive filename
- [ ] Style consistent with other images in chapter/book

## Output Format

**Deliverables for each annotated image:**

1. **Annotated image file:**
   - Filename: `ch[X]-fig[Y]-[description]-annotated.png`
   - Format: PNG (or JPEG for large images)
   - Resolution: As specified in screenshot plan

2. **Figure caption:**

   ```
   Figure [X.Y]: [Description of what image shows]
   ```

3. **Alt text:**

   ```
   [Concise description of image content for accessibility]
   ```

4. **Metadata file (optional):**
   ```yaml
   figure_number: 3.2
   filename: ch3-fig2-button-component-annotated.png
   caption: 'Button component with props destructuring and JSX return'
   alt_text: 'React function component showing props parameter and JSX button element'
   annotations:
     - type: numbered_callout
       number: 1
       target: 'function Button({ text })'
       description: 'Props destructuring'
     - type: numbered_callout
       number: 2
       target: 'return statement'
       description: 'JSX return'
   ```

## Annotation Style Guide

**Consistency standards for professional appearance:**

### Color Palette

```
Primary annotations (main focus):
- Red/Orange: #FF6B6B or #FF8C42

Secondary annotations (supporting):
- Cyan/Teal: #4ECDC4 or #45B7D1

Success/Correct:
- Green: #95E1D3 or #6BCF7F

Warning/Caution:
- Yellow: #FFE66D or #FFCB47

Information:
- Blue: #5DA5DA or #4A90E2

Text:
- Dark gray: #333333
- White: #FFFFFF (for labels on dark backgrounds)
```

### Typography

```
Callout numbers:
- Font: Bold sans-serif
- Size: 20-24pt
- Color: White
- Background: Colored circle (use palette above)

Labels:
- Font: Sans-serif (Arial, Helvetica, system)
- Size: 14-18pt
- Color: #333333
- Background: White 80-90% opacity with 1px border

Captions:
- Font: Italic serif or sans-serif
- Size: 12-14pt
- Color: #666666
- Alignment: Center or left-align below image
```

### Spacing

```
Border thickness: 2-4px
Arrow thickness: 3-6px (thicker for emphasis)
Padding in text boxes: 4-8px
Margin around callouts: 8-12px from target
```

## Common Pitfalls to Avoid

**❌ Obscuring important content:**

```
[Annotation covering critical code]
```

✅ **Place annotations in margins:**

```
[Annotations outside main content area with leader lines]
```

**❌ Too many annotations:**

```
[Screenshot with 10+ callouts - overwhelming]
```

✅ **Break into multiple images:**

```
[Screenshot 1: Elements 1-3]
[Screenshot 2: Elements 4-6]
```

**❌ Inconsistent colors:**

```
Image 1: Red arrows
Image 2: Blue arrows
Image 3: Green arrows
```

✅ **Use consistent color scheme:**

```
All primary annotations: Red/Orange
All secondary annotations: Cyan
```

**❌ Unreadable text:**

```
[Small 10pt text on busy background]
```

✅ **Large text with background:**

```
[16pt text on semi-transparent white background]
```

**❌ Inadequate redaction:**

```
[Blurred text that's still partially readable]
```

✅ **Complete redaction:**

```
[Solid black bar or "[REDACTED]" label]
```

## Examples

### Example 1: Code Editor Screenshot

**Original image:** VS Code with React component code

**Annotations added:**

1. Numbered callout (1) → Function declaration: "Component definition"
2. Numbered callout (2) → Props parameter: "Props destructuring"
3. Numbered callout (3) → Return statement: "JSX return"
4. Highlight box (yellow, 30% opacity) → Entire function body
5. Text label (top-right) → "File: Button.jsx"

**Caption:** "Figure 3.2: React Button component with props destructuring and JSX return statement"

**Alt text:** "Code editor showing React function component named Button with destructured props parameter and JSX button element in return statement"

### Example 2: Browser UI Screenshot

**Original image:** Web dashboard interface

**Annotations added:**

1. Red box → Navigation sidebar
2. Cyan box → Main content area (3 project cards)
3. Green box → User profile menu
4. Arrow from "Projects" label → First project card
5. Text labels: "Sidebar", "Projects", "Profile"

**Caption:** "Figure 5.1: Dashboard interface with navigation, project cards, and user menu"

**Alt text:** "Web dashboard with left sidebar navigation, three project cards in center, and user profile menu in top-right corner"

### Example 3: API Request/Response

**Original image:** Postman showing API request and response

**Annotations added:**

1. Highlight → Request method (GET)
2. Highlight → Endpoint URL
3. Red box → Authentication header
4. Green box → 200 OK status
5. Numbered callouts → Response body fields
6. Blur → Actual API token value
7. Text overlay → "[TOKEN REDACTED FOR SECURITY]"

**Caption:** "Figure 7.3: GET request to /api/users endpoint with authentication header and successful response"

**Alt text:** "API client showing GET request to users endpoint with authorization header, returning 200 OK status and JSON array of user objects"

## Next Steps

After annotating images:

1. Review all annotations for consistency
2. Use `optimize-visuals.md` task to optimize file size
3. Run `execute-checklist.md` with `screenshot-quality-checklist.md`
4. Insert into chapter manuscript with captions
5. Update screenshot inventory/tracking
6. Archive original unannotated versions
