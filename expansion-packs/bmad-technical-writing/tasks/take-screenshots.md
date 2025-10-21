<!-- Powered by BMAD™ Core -->

# Take Screenshots

---

task:
id: take-screenshots
name: Take Screenshots
description: Capture, annotate, and prepare high-quality screenshots for technical documentation
persona_default: screenshot-specialist
inputs:

- screenshot-specifications
- required-resolution
- annotation-requirements
  steps:
- Review screenshot specifications from diagram specs
- Prepare clean demonstration environment
- Capture screenshots at required resolution (300 DPI minimum)
- Add annotations (arrows, callouts, highlights)
- Crop to relevant area
- Ensure text is readable
- Apply consistent styling (border, shadow, etc.)
- Save in required format (PNG, JPEG)
- Name files descriptively (chapter-02-figure-03.png)
- Run execute-checklist.md with screenshot-quality-checklist.md
- Run execute-checklist.md with accessibility-checklist.md
  output: images/screenshots/{{descriptive-name}}.png

---

## Purpose

Create professional, readable screenshots that enhance understanding. Quality screenshots are essential for UI documentation, tutorials, and step-by-step guides.

## Workflow Steps

### 1. Prepare Clean Environment

Set up for capture:

- Use clean desktop (no personal info)
- Close unnecessary windows
- Use default theme unless demonstrating customization
- Zoom to appropriate level (125-150% for clarity)
- Use realistic but safe demo data

### 2. Capture at High Resolution

Quality requirements:

- **Minimum 300 DPI** for print
- **Retina/HiDPI** for web (2x resolution)
- **Full window** vs **focused area** based on context
- **Consistent dimensions** for similar screenshots

### 3. Annotate Effectively

Add helpful annotations:

- **Arrows**: Point to specific UI elements
- **Numbered callouts**: Reference in text
- **Highlights**: Draw attention to key areas
- **Red boxes**: Emphasize important elements

### 4. Apply Consistent Styling

Visual consistency:

- Same annotation colors across book
- Consistent border/shadow treatment
- Uniform font for labels
- Matching screenshot dimensions for similar content

### 5. Name Files Descriptively

File naming convention:

```
chapter-02-django-admin-login.png
chapter-03-api-response-json.png
chapter-05-error-message-detail.png
```

## Success Criteria

- [ ] High resolution (300 DPI minimum)
- [ ] Readable text
- [ ] Clear annotations
- [ ] Consistent styling
- [ ] Descriptive file names
- [ ] Screenshot quality checklist passed
- [ ] Accessibility checklist passed

## Next Steps

1. Add screenshots to manuscript
2. Reference in figure captions
3. Include alt text for accessibility
