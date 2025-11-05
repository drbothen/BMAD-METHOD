# Pandoc Conversion Findings for PacktPub

## Test Results: Pandoc + Sample Chapter Reference Doc

**Date**: 2025-10-25
**Tested**: Pandoc 3.x with `--reference-doc="Sample Chapter.docx"`

### What Works

✅ **Basic Conversion**: Markdown → Word with Sample Chapter template
✅ **Built-in Styles**: Pandoc successfully maps to:

- Heading 1, Heading 2, Heading 3, Heading 4
- Normal (paragraph style)
- Source Code (code blocks)

✅ **Template Preservation**:

- Page layout (margins, size)
- Font definitions
- All [PACKT] styles remain in document (available but not auto-applied)

### What Doesn't Work Out-of-the-Box

❌ **[PACKT] Style Auto-Application**: Pandoc maps to built-in "Heading 1" not "Heading 1 [PACKT]"
❌ **Custom Style Mapping**: Lua filters have limitations with paragraph-level custom-style attributes
❌ **Character Styles**: Inline code, bold, italic map to built-in styles, not [PACKT] character styles

### Why This Happens

Pandoc uses **hardcoded mappings**:

- `# Heading` → style named "Heading 1" (exact match)
- Bold → "Strong" character style
- Italic → "Emphasis" character style
- Code block → "Source Code" or "Code" paragraph style

These are **built-in Word style names**, not the [PACKT] variants.

## Solution Options

### Option A: Manual Post-Processing (Simplest)

**Workflow**:

1. Convert with Pandoc using Sample Chapter as reference
2. Open in Word
3. Find/Replace styles:
   - Find all "Heading 1" → Replace with "Heading 1 [PACKT]"
   - Find all "Heading 2" → Replace with "Heading 2 [PACKT]"
   - Find all "Normal" → Replace with "Normal [PACKT]"
   - Find all "Source Code" → Replace with "Code [PACKT]"

**Pros**: Reliable, no custom scripting
**Cons**: Manual step required

### Option B: Rename Styles in Reference Template (Recommended)

**Workflow**:

1. Copy Sample Chapter.docx → packtpub-pandoc-template.docx
2. Open in Word, modify styles:
   - Rename "Heading 1" → Point to "Heading 1 [PACKT]" as base
   - OR: Delete "Heading 1", rename "Heading 1 [PACKT]" to "Heading 1"
3. Save modified template
4. Use with Pandoc: `--reference-doc=packtpub-pandoc-template.docx`

**Pros**: Fully automated, no post-processing
**Cons**: Requires template customization

### Option C: Python Post-Processing (Most Flexible)

**Workflow**:

1. Convert with Pandoc (gets structure right)
2. Run Python script with python-docx:

   ```python
   from docx import Document

   doc = Document('converted.docx')

   style_mappings = {
       'Heading 1': 'Heading 1 [PACKT]',
       'Heading 2': 'Heading 2 [PACKT]',
       'Normal': 'Normal [PACKT]',
       'Source Code': 'Code [PACKT]',
   }

   for para in doc.paragraphs:
       if para.style.name in style_mappings:
           para.style = style_mappings[para.style.name]

   doc.save('packtpub-formatted.docx')
   ```

**Pros**: Fully automated, scriptable, extensible
**Cons**: Requires Python dependency

### Option D: Direct Python Conversion (Full Control)

**Workflow**:

1. Skip Pandoc entirely
2. Parse Markdown with Python (mistune, markdown-it-py)
3. Create Word document with python-docx
4. Apply [PACKT] styles directly during creation

**Pros**: Complete control, no Pandoc limitations
**Cons**: Most complex, need to implement full Markdown parser logic

## Recommendation for format-for-packtpub Task

**Use Option C (Pandoc + Python Post-Processing)**:

**Rationale**:

- Pandoc handles complex Markdown parsing (tables, nested lists, etc.)
- Python post-processing is simple and reliable
- Fully automatable in single command/script
- Easy to extend for additional validations

**Implementation**:

```bash
# Step 1: Convert with Pandoc
pandoc manuscript.md -o temp.docx --reference-doc="Sample Chapter.docx"

# Step 2: Apply PACKT styles with Python
python3 apply-packt-styles.py temp.docx output-packtpub.docx

# Step 3: Validate
python3 validate-packtpub.py output-packtpub.docx
```

## Test Results Summary

**File**: `test-manuscript.md` (Sample React Hooks chapter)
**Conversion Method**: Pandoc + Sample Chapter reference
**Output**: `test-output-with-packt-styles.docx`

**Style Mapping Results**:

- 49 paragraphs → "Normal" (should be "Normal [PACKT]")
- 9 code blocks → "Source Code" (should be "Code [PACKT]")
- 7 H3 headings → "Heading 3" (should be "Heading 3 [PACKT]")
- 6 H2 headings → "Heading 2" (should be "Heading 2 [PACKT]")
- 1 H1 heading → "Heading 1" (should be "Heading 1 [PACKT]")

**Conclusion**: Conversion structure is perfect, just need style name substitution.

## Next Steps

1. Create `apply-packt-styles.py` script for style substitution
2. Test with full manuscript
3. Integrate into `format-for-packtpub.md` task
4. Add validation checks for:
   - Code block line counts (≤20-30 lines)
   - Image references (300 DPI, PNG/TIFF)
   - Structure (intro, bullets, summary)
