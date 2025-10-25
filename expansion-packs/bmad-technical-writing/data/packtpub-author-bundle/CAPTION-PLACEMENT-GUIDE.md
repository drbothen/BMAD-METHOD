# PacktPub Caption Placement Guide

## Critical Rule: Table vs Figure Caption Placement

In technical writing for PacktPub, caption placement follows strict conventions:

### ✅ CORRECT Placement

**Tables: Caption BEFORE the table**
```markdown
Table 1.1: User authentication methods

| Method | Security | Ease of Use |
|--------|----------|-------------|
| Password | Medium | Easy |
| 2FA | High | Moderate |
| Biometric | Very High | Easy |
```

**Figures: Caption AFTER the image**
```markdown
![User login flow diagram](images/login-flow.png)

Figure 1.1: User authentication workflow
```

### ❌ INCORRECT Placement

**Tables: Caption AFTER table (WRONG)**
```markdown
| Method | Security | Ease of Use |
|--------|----------|-------------|
| Password | Medium | Easy |

Table 1.1: User authentication methods  ← WRONG POSITION
```

**Figures: Caption BEFORE image (WRONG)**
```markdown
Figure 1.1: User authentication workflow  ← WRONG POSITION

![User login flow diagram](images/login-flow.png)
```

## Why This Matters

### Tables
- **Readers need context BEFORE scanning data**
- Table caption tells readers what they're about to examine
- Industry standard: APA, Chicago Manual of Style, IEEE all place table captions BEFORE

### Figures
- **Images are self-contained and viewed first**
- Caption provides explanation AFTER viewing the visual
- Follows natural reading flow: see image → read explanation

## PacktPub Conversion Process

The `apply-packt-styles-v6.py` script applies **"Figure Caption [PACKT]"** style to both table and figure captions, but YOU must place them correctly in your markdown.

### Markdown Structure

**For Tables:**
```markdown
## Section Heading

Introductory paragraph explaining the table's purpose.

Table X.Y: Descriptive caption

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |

Text following the table.
```

**For Figures:**
```markdown
## Section Heading

Introductory paragraph explaining the diagram.

![Alt text for accessibility](images/diagram.png)

Figure X.Y: Descriptive caption

Text following the figure.
```

## Numbering Convention

### Table Numbers
- Format: `Table X.Y: Description`
- X = Chapter number
- Y = Table number within chapter
- Examples:
  - `Table 1.1: React Hook comparison`
  - `Table 2.3: Performance benchmarks`

### Figure Numbers
- Format: `Figure X.Y: Description`
- X = Chapter number
- Y = Figure number within chapter
- Examples:
  - `Figure 1.1: Component lifecycle diagram`
  - `Figure 3.2: Authentication flow`

## Alt Text vs Caption

### Images (Figures)

**Alt text** (in markdown image syntax):
```markdown
![Component lifecycle flow showing mount, update, and unmount phases](images/lifecycle.png)
```
- Purpose: Accessibility for screen readers
- Content: Describe what's IN the image
- Placement: Inside `![]()` markdown syntax

**Caption** (separate paragraph):
```markdown
Figure 1.1: React component lifecycle diagram
```
- Purpose: Reference and context in document
- Content: Label and brief description
- Placement: AFTER the image

### Tables

**Caption only** (no alt text needed):
```markdown
Table 1.1: Comparison of state management libraries

| Library | Bundle Size | Learning Curve |
|---------|-------------|----------------|
| Redux   | 2.6 KB      | Steep          |
```
- Placement: BEFORE the table
- Format: `Table X.Y: Description`

## Common Mistakes

### ❌ Mistake 1: Table Caption After Table
```markdown
| Feature | React | Vue |
|---------|-------|-----|
| Speed   | Fast  | Fast |

Table 1.1: Framework comparison  ← WRONG
```

**✅ Fix:**
```markdown
Table 1.1: Framework comparison  ← CORRECT

| Feature | React | Vue |
|---------|-------|-----|
| Speed   | Fast  | Fast |
```

### ❌ Mistake 2: Figure Caption Before Image
```markdown
Figure 1.1: Architecture diagram  ← WRONG

![System architecture](images/arch.png)
```

**✅ Fix:**
```markdown
![System architecture](images/arch.png)

Figure 1.1: Architecture diagram  ← CORRECT
```

### ❌ Mistake 3: Missing Caption Numbers
```markdown
Table: State management comparison  ← Missing X.Y

| Library | Size |
```

**✅ Fix:**
```markdown
Table 1.1: State management comparison  ← Includes chapter.table number

| Library | Size |
```

### ❌ Mistake 4: Using Image Alt Text as Figure Caption
```markdown
![Figure 1.1: Architecture diagram](images/arch.png)  ← Caption in wrong place
```

**✅ Fix:**
```markdown
![System architecture overview](images/arch.png)

Figure 1.1: Architecture diagram  ← Separate caption paragraph
```

## Validation

The `validate-manuscript.py` script will check for:
- Table captions with "Table X.Y:" format
- Figure captions with "Figure X.Y:" format (future enhancement)
- Correct caption placement relative to tables/figures (future enhancement)

## Word Document Output

After conversion, PacktPub Word document will show:
- Both table and figure captions styled as **"Figure Caption [PACKT]"**
- Table headers styled as **"Table Column Heading [PACKT]"**
- Table content styled as **"Table Column Content [PACKT]"**

PacktPub's template uses a single caption style for both tables and figures, but the PLACEMENT rules still apply in your source markdown.

## Summary Checklist

- [ ] Table captions appear BEFORE tables
- [ ] Figure captions appear AFTER images
- [ ] All captions use numbering format: `Table/Figure X.Y: Description`
- [ ] Alt text describes image content (for accessibility)
- [ ] Captions provide reference labels and context
- [ ] Consistent numbering throughout chapter
- [ ] Captions are concise (< 100 characters ideal)

## Examples from This Project

See working examples:
- `sample-chapter.md` - Figure captions (images)
- `table-test-chapter.md` - Table captions (corrected version)

## References

- PacktPub Author Guidelines (in `packtpub-author-bundle/`)
- Chicago Manual of Style: Tables and Figures
- APA Style: Table and Figure Guidelines
