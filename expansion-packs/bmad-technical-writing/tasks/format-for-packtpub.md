<!-- Powered by BMAD™ Core -->

# Format for PacktPub Submission

---

task:
  id: format-for-packtpub
  name: Format Manuscript for PacktPub Submission
  description: Convert technical book manuscripts from Markdown to PacktPub-formatted Word documents with complete style application and validation
  persona_default: manuscript-formatter
  inputs:
    - manuscript_path (Markdown files or directory)
    - submission_type (chapter | full-manuscript)
    - author_bundle_path (PacktPub Author Bundle location)
  steps:
    - Validate prerequisite files and tools
    - Pre-convert validation of Markdown content
    - Execute Pandoc conversion with PacktPub template
    - Apply PACKT styles with Python post-processing
    - Validate converted document against PacktPub requirements
    - Execute PacktPub submission checklist
    - Generate validation report
  output: PacktPub-formatted .docx manuscript + validation report + checklist results

---

## Purpose

This task automates the conversion of technical book manuscripts from Markdown format to PacktPub's required Word document format with proper [PACKT] style application and comprehensive validation against PacktPub's official submission requirements.

## Prerequisites

### Required Files

1. **PacktPub Author Bundle** - Obtain from your PacktPub editor
   - Location: `manuscripts/research/AuthorBundle_updated/` (or custom path)
   - Required files:
     - `Sample Chapter.docx` - Template with all [PACKT] styles
     - `Packt_Image Guidelines.pdf` - Image specifications reference
     - `Writing codes in your chapter.pdf` - Code formatting reference
     - `Your Writing Checklist.pdf` - Submission checklist

2. **Manuscript in Markdown** - Your chapter/book content
   - Single file or multiple files
   - Standard Markdown syntax
   - Code blocks with language identifiers
   - Images referenced with relative paths

3. **Images Folder** - All images referenced in manuscript
   - Organized structure (e.g., `images/chapter-5/`)
   - Naming convention: descriptive names with figure numbers

### Required Tools

1. **Pandoc** (v2.x or higher)
   ```bash
   # Check installation
   pandoc --version

   # Install if needed:
   # macOS: brew install pandoc
   # Ubuntu: sudo apt-get install pandoc
   # Windows: download from https://pandoc.org/installing.html
   ```

2. **Python 3** with `python-docx` library
   ```bash
   # Check installation
   python3 --version

   # Install python-docx
   pip3 install python-docx
   ```

3. **GIMP** (optional, recommended for screenshot optimization)
   - Download from www.gimp.org
   - Used for 300 DPI screenshot creation

## Input Parameters

### manuscript_path
- **Type**: File path or directory path
- **Format**: `.md` file(s)
- **Example**: `manuscripts/chapters/chapter-05-react-hooks.md`
- **Multiple files**: `manuscripts/chapters/` (processes all .md files)

### submission_type
- **Options**: `chapter` | `full-manuscript`
- **chapter**: Single chapter submission (most common)
- **full-manuscript**: Complete book with multiple chapters

### author_bundle_path
- **Type**: Directory path
- **Default**: `manuscripts/research/AuthorBundle_updated/`
- **Contains**: PacktPub Author Bundle files

### output_path (optional)
- **Type**: Directory path
- **Default**: `manuscripts/formatted-for-packtpub/`
- **Contains**: Generated .docx file(s) and validation reports

## Workflow Steps

### Step 1: Validate Prerequisites

**Check required files exist:**

```bash
# Verify PacktPub template
test -f "${author_bundle_path}/Sample Chapter.docx" || echo "ERROR: Template not found"

# Verify manuscript
test -f "${manuscript_path}" || echo "ERROR: Manuscript not found"

# Verify tools
command -v pandoc >/dev/null 2>&1 || echo "ERROR: Pandoc not installed"
python3 -c "import docx" 2>/dev/null || echo "ERROR: python-docx not installed"
```

**Validation Checks**:
- [ ] Sample Chapter.docx template exists
- [ ] Manuscript file(s) exist and are readable
- [ ] Pandoc installed and accessible
- [ ] Python 3 + python-docx available
- [ ] Output directory writable

### Step 2: Pre-Convert Markdown Validation

**Validate manuscript content before conversion:**

#### 2.1 Code Block Validation

**PacktPub Requirement**: 20 lines ideal, 30 lines absolute maximum

```python
import re

def validate_code_blocks(markdown_content):
    """Check code block line counts"""
    code_blocks = re.findall(r'```[\s\S]*?```', markdown_content)

    violations = []
    warnings = []

    for i, block in enumerate(code_blocks, 1):
        lines = block.count('\n') - 2  # Subtract fence lines
        if lines > 30:
            violations.append(f"Code block #{i}: {lines} lines (MAX: 30)")
        elif lines > 20:
            warnings.append(f"Code block #{i}: {lines} lines (IDEAL: ≤20)")

    return violations, warnings
```

#### 2.2 Image Reference Validation

**PacktPub Requirements**:
- 300 DPI minimum
- 2000 pixels minimum on shortest edge
- PNG/TIFF format (NEVER JPG)

```python
from PIL import Image
import os

def validate_images(markdown_content, base_path):
    """Check image requirements"""
    # Extract image references
    images = re.findall(r'!\[.*?\]\((.*?)\)', markdown_content)

    issues = []

    for img_path in images:
        full_path = os.path.join(base_path, img_path)

        if not os.path.exists(full_path):
            issues.append(f"Image not found: {img_path}")
            continue

        # Check format
        if img_path.lower().endswith('.jpg') or img_path.lower().endswith('.jpeg'):
            issues.append(f"JPG format not allowed (use PNG/TIFF): {img_path}")

        # Check resolution
        try:
            with Image.open(full_path) as img:
                width, height = img.size
                dpi = img.info.get('dpi', (72, 72))

                shortest_edge = min(width, height)

                if shortest_edge < 2000:
                    issues.append(f"Image too small ({shortest_edge}px, need 2000px min): {img_path}")

                if dpi[0] < 300 or dpi[1] < 300:
                    issues.append(f"Image DPI too low ({dpi[0]}x{dpi[1]}, need 300 DPI): {img_path}")
        except Exception as e:
            issues.append(f"Cannot read image {img_path}: {e}")

    return issues
```

#### 2.3 Caption Placement Validation

**CRITICAL RULE**: Caption placement differs between tables and figures

**Tables**: Caption comes BEFORE the table
```markdown
Table 2.1: React Hooks comparison and use cases

| Hook | Purpose | When to Use | Returns |
|------|---------|-------------|---------|
| useState | State management | Simple state values | [state, setState] |
```

**Figures**: Caption comes AFTER the image
```markdown
![React component lifecycle diagram](images/lifecycle.png)

Figure 2.1: Component lifecycle phases
```

**Why This Matters**:
- Tables: Readers need context BEFORE scanning data
- Figures: Images are self-contained and viewed first, caption explains AFTER

**Common Mistake**:
```markdown
❌ WRONG - Table caption AFTER table:
| Hook | Purpose |
|------|---------|

Table 2.1: React Hooks comparison  ← INCORRECT PLACEMENT
```

**Caption Numbering Format**:
- Format: `Table X.Y: Description` or `Figure X.Y: Description`
- X = Chapter number
- Y = Table/Figure number within chapter
- Examples:
  - `Table 1.1: User authentication methods`
  - `Figure 2.3: Authentication workflow diagram`

**Alt Text vs Caption**:
- **Alt text** (for accessibility): Describes WHAT is IN the image
  ```markdown
  ![Component lifecycle flow showing mount, update, and unmount phases](images/lifecycle.png)
  ```
- **Caption** (for document reference): Label and brief description
  ```markdown
  Figure 1.1: React component lifecycle diagram
  ```

See `CAPTION-PLACEMENT-GUIDE.md` for comprehensive examples and validation rules.

#### 2.4 Structure Validation

**PacktPub Requirements**:
- Chapter opens with introduction + learning goals
- Bullet list of main topics
- Summary section at end
- Next chapter preview

```python
def validate_structure(markdown_content):
    """Check required structural elements"""
    issues = []

    # Check for intro section (first H2 should have intro before it)
    lines = markdown_content.split('\n')
    first_h2_index = next((i for i, line in enumerate(lines) if line.startswith('## ')), None)

    if first_h2_index and first_h2_index < 10:
        issues.append("Missing chapter introduction (should have intro before first H2)")

    # Check for bullet list in intro
    intro_section = '\n'.join(lines[:first_h2_index] if first_h2_index else lines[:20])
    if '- ' not in intro_section and '* ' not in intro_section:
        issues.append("Missing bullet list of topics in introduction")

    # Check for summary section
    if '## Summary' not in markdown_content and '## Conclusion' not in markdown_content:
        issues.append("Missing Summary or Conclusion section")

    # Check for consecutive headers (no text between)
    for i in range(len(lines) - 1):
        if lines[i].startswith('#') and lines[i+1].startswith('#'):
            issues.append(f"Consecutive headers found (line {i+1}): Need lead-in text")

    return issues
```

**Execute all pre-convert validations:**

```bash
python3 validate-manuscript.py \
  --manuscript "${manuscript_path}" \
  --images-dir "$(dirname ${manuscript_path})/images" \
  --report pre-convert-validation.md
```

### Step 3: Execute Pandoc Conversion

**Convert Markdown to Word using PacktPub template:**

```bash
pandoc "${manuscript_path}" \
  -o temp-converted.docx \
  --reference-doc="${author_bundle_path}/Sample Chapter.docx" \
  --standalone \
  --toc \
  --highlight-style=tango
```

**Pandoc Parameters Explained**:
- `--reference-doc`: Use PacktPub Sample Chapter as style template
- `--standalone`: Create complete document with metadata
- `--toc`: Generate table of contents (optional, can remove later)
- `--highlight-style`: Syntax highlighting for code blocks

**What Pandoc Handles**:
✓ Markdown parsing (headings, lists, code, emphasis, links)
✓ Table creation
✓ Image insertion
✓ Document structure
✓ Basic style application (Heading 1-6, Normal, Source Code)

**What Pandoc Doesn't Handle**:
✗ [PACKT] style application (uses built-in "Normal" not "Normal [PACKT]")
✗ Character style mapping (bold/italic don't use [PACKT] styles)
✗ Custom elements (info boxes, tips, warnings)

### Step 4: Apply PACKT Styles with Python Post-Processing

**Convert Pandoc's built-in styles to PacktPub [PACKT] styles:**

**Understanding PacktPub Style System**:
- **Headings**: Use standard "Heading 1-6" (NO [PACKT] suffix)
- **All other content**: Uses [PACKT] suffix

**Style Mapping**:
```
Pandoc Output          →  PacktPub Required
────────────────────────────────────────────
Heading 1              →  Heading 1 (unchanged - PacktPub standard)
Heading 2-6            →  Heading 2-6 (unchanged - PacktPub standard)
Normal                 →  Normal [PACKT]
Source Code            →  Code [PACKT]
List Bullet            →  Bullet [PACKT]
List Number            →  Numbered Bullet [PACKT]
Block Quote            →  Quote [PACKT]
Strong (character)     →  Key Word [PACKT]
Emphasis (character)   →  Italics [PACKT]
```

**Execute style application:**

```bash
python3 apply-packt-styles-v6.py \
  temp-converted.docx \
  "${output_path}/formatted-manuscript.docx"
```

**Python Script Logic** (see `apply-packt-styles-v6.py`):
1. Load converted document
2. Verify [PACKT] styles exist in document (from template)
3. **Split multi-line code blocks** into separate paragraphs:
   - Pandoc places entire code blocks in single paragraph with newlines
   - PacktPub requires separate paragraph per line
   - Apply "Code [PACKT]" to all lines except last
   - Apply "Code End [PACKT]" to last line
4. Skip headings (already correct - PacktPub uses standard "Heading 1-6")
5. Detect list items by checking numbering properties (numPr XML elements)
6. Distinguish bullet lists from numbered lists by examining numFmt attribute:
   - `numFmt="bullet"` → "Bullet [PACKT]"
   - `numFmt="decimal"/"lowerLetter"/etc.` → "Numbered Bullet [PACKT]"
7. **Detect and style captions**:
   - Table captions (format: `Table X.Y: Description`) → "Figure Caption [PACKT]"
   - Figure captions (paragraphs with embedded images or caption keywords) → "Figure Caption [PACKT]"
   - PacktPub uses single "Figure Caption [PACKT]" style for both tables and figures
8. **Style table cells**:
   - First row of each table → "Table Column Heading [PACKT]"
   - All other rows → "Table Column Content [PACKT]"
9. Map other styles according to STYLE_MAPPINGS dictionary
10. Apply character styles to runs (Strong → Key Word [PACKT], Emphasis → Italics [PACKT])
11. Save modified document with validation report

### Step 5: Post-Convert Validation

**Validate formatted Word document:**

#### 5.1 Style Verification

```python
from docx import Document

def verify_packt_styles(docx_path):
    """Verify all styles are PacktPub-compliant"""
    doc = Document(docx_path)

    style_usage = {}
    for para in doc.paragraphs:
        style_name = para.style.name
        style_usage[style_name] = style_usage.get(style_name, 0) + 1

    issues = []

    for style in style_usage:
        # Check for unmapped styles (neither [PACKT] nor standard Heading)
        if not style.startswith('Heading') and '[PACKT]' not in style:
            issues.append(f"Unmapped style found: {style} ({style_usage[style]} instances)")

    return issues
```

#### 5.2 Image Embedding Verification

```python
def verify_images_embedded(docx_path):
    """Check all images are properly embedded"""
    doc = Document(docx_path)

    image_count = 0
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_count += 1

    return image_count
```

#### 5.3 Code Block Line Count Verification

```python
def verify_code_blocks(docx_path):
    """Check code block line counts in Word document"""
    doc = Document(docx_path)

    violations = []
    warnings = []

    for i, para in enumerate(doc.paragraphs):
        if para.style.name == 'Code [PACKT]':
            line_count = para.text.count('\n') + 1

            if line_count > 30:
                violations.append(f"Code block at para {i}: {line_count} lines (MAX: 30)")
            elif line_count > 20:
                warnings.append(f"Code block at para {i}: {line_count} lines (IDEAL: ≤20)")

    return violations, warnings
```

### Step 6: Execute PacktPub Checklists

**Run official PacktPub checklists:**

#### 6.1 Generative AI Compliance Check

```bash
# Execute AI compliance checklist
execute-checklist \
  --checklist generative-ai-compliance-checklist.md \
  --context "${manuscript_path}" \
  --report "${output_path}/ai-detection-report.md"
```

**AI Detection Avoidance validates**:
- Content quality (accuracy, depth, value)
- Authenticity and personal voice
- Technical accuracy and specificity
- Writing style (avoiding AI patterns)
- Reader value and engagement

See `generative-ai-compliance-checklist.md` for complete checklist.

#### 6.2 Submission Requirements Check

```bash
# Execute submission checklist
execute-checklist \
  --checklist packtpub-submission-checklist.md \
  --context "${output_path}/formatted-manuscript.docx" \
  --report "${output_path}/submission-checklist-results.md"
```

**Submission Checklist validates**:
- Outline compliance (topics covered, page count, objectives met)
- Structure requirements (intro, bullet lists, headings, transitions, summary)
- Readability standards (audience consideration, visual variety, framing)
- Value proposition (hands-on examples, real-world application, learning reinforcement)
- Technical requirements (latest versions, code explanations, GitHub updates)

See `packtpub-submission-checklist.md` for complete checklist.

### Step 7: Generate Validation Report

**Create comprehensive validation report:**

```markdown
# PacktPub Formatting Validation Report

**Manuscript**: ${manuscript_path}
**Formatted Output**: ${output_path}/formatted-manuscript.docx
**Date**: $(date)

## Pre-Convert Validation

### Code Blocks
- ✓ 12 code blocks validated
- ⚠️ 2 warnings: blocks exceed 20 lines (21, 23 lines)
- ✗ 0 violations

### Images
- ✓ 8 images validated
- ✗ 1 issue: screenshot-01.jpg should be PNG format

### Structure
- ✓ Chapter introduction present
- ✓ Bullet list of topics present
- ✓ Summary section present

## Post-Convert Validation

### Style Application
- ✓ 100% PacktPub-compliant styles
  - Normal [PACKT]: 45 instances
  - Code [PACKT]: 12 instances
  - Bullet [PACKT]: 18 instances
  - Heading 1-3: 14 instances
- ✗ 0 unmapped styles

### Images
- ✓ 8 images embedded successfully

### Code Blocks (Word document)
- ✓ All code blocks within limits
- ⚠️ 2 warnings: consider splitting blocks

## Submission Checklist

**Overall Score**: 38/40 items passed

### Failures
- [ ] Update code files on GitHub with this chapter

### Warnings
- ⚠️ Consider adding more visual variety (tables, diagrams)

## Recommendations

1. **REQUIRED**: Convert screenshot-01.jpg to PNG format
2. **REQUIRED**: Update GitHub repository with code files
3. **SUGGESTED**: Split 2 long code blocks (21, 23 lines) into smaller sections
4. **SUGGESTED**: Add diagram for architecture section

## Ready for Submission?

🟡 **ALMOST READY** - Address 1 required issue before submission
```

## Success Criteria

The manuscript is ready for PacktPub submission when:

**Formatting**:
- [ ] All paragraphs use PacktPub styles (Heading 1-6 or [PACKT] styles)
- [ ] No unmapped or built-in Word styles remain
- [ ] Document uses Sample Chapter.docx template (styles preserved)

**Images**:
- [ ] All images embedded in document
- [ ] All images meet 300 DPI / 2000px minimum (or documented exceptions)
- [ ] No JPG format images (PNG/TIFF only)
- [ ] Full-screen + snippet pairs provided for detail images

**Code**:
- [ ] No code blocks exceed 30 lines (hard limit)
- [ ] Ideally all code blocks ≤20 lines
- [ ] All code blocks have explanatory text before/after
- [ ] No in-code comments (explanation in surrounding text)
- [ ] Code [PACKT] style applied to all code blocks

**Structure**:
- [ ] Chapter opens with introduction listing learning goals
- [ ] Bullet list of main topics present
- [ ] Summary section present at end
- [ ] Next chapter preview present (for multi-chapter books)
- [ ] No consecutive headers (lead-in text between all headings)
- [ ] No consecutive images (framing text around all images)

**Checklist**:
- [ ] PacktPub submission checklist passes (≥95% items)
- [ ] All "required" items addressed
- [ ] Warnings documented in validation report

**Validation**:
- [ ] Pre-convert validation passed (or issues documented)
- [ ] Post-convert validation passed
- [ ] Style verification passed
- [ ] Validation report generated

## Output Files

After successful completion, the following files are generated:

1. **formatted-manuscript.docx** - PacktPub-formatted Word document
   - Location: `${output_path}/`
   - Contains all [PACKT] styles properly applied
   - Ready for submission to PacktPub AuthorSight portal

2. **validation-report.md** - Comprehensive validation results
   - Pre-convert checks (Markdown content)
   - Post-convert checks (Word document)
   - Submission checklist results
   - Recommendations for improvement

3. **pre-convert-validation.md** - Markdown validation details
   - Code block analysis
   - Image validation results
   - Structure checks

4. **submission-checklist-results.md** - PacktPub checklist execution results
   - All 40+ checklist items with pass/fail/warning status
   - Detailed findings for failed items

5. **images/** (optional) - Optimized image folder
   - Images converted to PNG/TIFF if needed
   - Images resized to meet DPI requirements (if requested)

## Examples

### Example 1: Single Chapter Submission

```bash
# Format Chapter 5 for PacktPub
execute-task format-for-packtpub \
  --manuscript manuscripts/chapters/chapter-05-react-hooks.md \
  --submission-type chapter \
  --author-bundle manuscripts/research/AuthorBundle_updated/ \
  --output manuscripts/formatted-for-packtpub/
```

**Output**:
```
✓ Pre-convert validation: 2 warnings
✓ Pandoc conversion complete
✓ PACKT styles applied: 67 paragraphs
✓ Post-convert validation passed
✓ Submission checklist: 39/40 passed

📄 Output: manuscripts/formatted-for-packtpub/chapter-05-react-hooks.docx
📊 Report: manuscripts/formatted-for-packtpub/validation-report.md

🟢 READY FOR SUBMISSION (address 1 GitHub update reminder)
```

### Example 2: Full Manuscript Submission

```bash
# Format all chapters
execute-task format-for-packtpub \
  --manuscript manuscripts/chapters/ \
  --submission-type full-manuscript \
  --author-bundle manuscripts/research/AuthorBundle_updated/ \
  --output manuscripts/formatted-for-packtpub/
```

**Processes**:
- Converts all .md files in directory
- Generates separate .docx for each chapter
- Creates combined validation report
- Executes checklist for each chapter

### Example 3: With Image Optimization

```bash
# Format with automatic image optimization
execute-task format-for-packtpub \
  --manuscript manuscripts/chapters/chapter-05-react-hooks.md \
  --submission-type chapter \
  --author-bundle manuscripts/research/AuthorBundle_updated/ \
  --output manuscripts/formatted-for-packtpub/ \
  --optimize-images \
  --target-dpi 300
```

**Additional processing**:
- Converts JPG → PNG
- Scales images to meet 2000px minimum
- Sets DPI metadata to 300
- Backs up original images

## Common Issues and Solutions

### Issue 1: "No [PACKT] styles found in document"

**Cause**: Pandoc didn't use Sample Chapter.docx as reference

**Solution**:
```bash
# Ensure correct template path
pandoc manuscript.md -o output.docx \
  --reference-doc="manuscripts/research/AuthorBundle_updated/Sample Chapter.docx"
```

### Issue 2: "Code block exceeds 30 lines"

**Cause**: Code sample too long for PacktPub requirements

**Solution**:
1. Break code into logical sections (where you would normally comment)
2. Show key sections, reference full code on GitHub
3. Use "..." to indicate omitted code
4. Explain each section separately

### Issue 3: "Image format JPG not allowed"

**Cause**: Screenshots saved as JPG lose quality

**Solution**:
```bash
# Convert to PNG
magick screenshot.jpg screenshot.png

# Or use GIMP: File > Export As > PNG
```

### Issue 4: "Image resolution too low"

**Cause**: Screenshot taken at 72 DPI or low resolution

**Solution**:
1. Use GIMP screenshot tool: File > Create > Screenshot (auto 300 DPI)
2. Use 4K monitor for higher resolution screenshots
3. Use PrtScr in GIMP, paste to new document (auto-converts to 300 DPI)

### Issue 5: "Unmapped styles remain"

**Cause**: Markdown contains non-standard elements

**Solution**:
1. Check for HTML tags in Markdown (convert to Markdown)
2. Check for custom Markdown extensions
3. Manually apply [PACKT] styles in Word for special elements

## Integration with Workflows

This task integrates with:

- **chapter-development-workflow.yaml** - Final step before submission
- **book-planning-workflow.yaml** - Formatting after content approval
- **execute-checklist.md** - Runs PacktPub submission checklist
- **validate-manuscript.md** - Pre-submission validation

## Related Files

**Scripts**:
- `apply-packt-styles-v6.py` - Style application with caption and table support (in `data/packtpub-author-bundle/`)
- `validate-manuscript.py` - Pre-convert validation
- `verify-packtpub-doc.py` - Post-convert validation
- `format-for-packtpub.sh` - Wrapper script for complete workflow

**Checklists**:
- `generative-ai-compliance-checklist.md` - AI content compliance validation
- `packtpub-submission-checklist.md` - Official 40+ item checklist

**Templates**:
- `Sample Chapter.docx` (from Author Bundle) - PacktPub template

**Documentation**:
- `Generative_AI_Author_Guidelines.md` - Official PacktPub AI usage guidelines
- `packtpub-author-bundle-analysis.md` - Research findings
- `PANDOC-CONVERSION-FINDINGS.md` - Conversion workflow documentation
- `CAPTION-PLACEMENT-GUIDE.md` - Comprehensive caption placement rules and examples

## Notes

- **Template Location**: Sample Chapter.docx must be from PacktPub Author Bundle (contains all 77 [PACKT] styles)
- **Heading Styles**: PacktPub uses standard "Heading 1-6" without [PACKT] suffix
- **Character Styles**: Bold/italic need manual attention for first appearance terms (Key Word [PACKT])
- **Special Elements**: Info boxes, tips, warnings require manual application in Word
- **GitHub Integration**: Remember to update code repository with each chapter (checklist item)

## Author's Checklist

Before running this task:
- [ ] All code in manuscript tested and working
- [ ] All images created and referenced correctly
- [ ] Chapter follows outline and meets learning objectives
- [ ] Content reviewed and proofread
- [ ] Code repository updated with examples

After running this task:
- [ ] Review validation report
- [ ] Address all required issues
- [ ] Review warnings and suggestions
- [ ] Manual review in Word for special formatting
- [ ] Final proofread in formatted document
- [ ] Submit via PacktPub AuthorSight portal or email to editor
