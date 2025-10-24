<!-- Powered by BMAD™ Core -->

# Package for Publisher

---

task:
id: package-for-publisher
name: Package for Publisher
description: Prepare complete manuscript package according to publisher specifications
persona_default: book-publisher
inputs:

- publisher-name
- submission-guidelines
- manuscript-files
  steps:
- Identify target publisher (PacktPub/O'Reilly/Manning/Other)
- Gather all manuscript files (chapters, front matter, back matter)
- Collect all images and diagrams
- Verify code repository link or zip
- Format per publisher requirements
- Run publisher-specific checklist
- Create submission package (zip or folder structure)
- Include metadata file if required
- Verify all cross-references work
- Run execute-checklist.md with final-manuscript-checklist.md
  output: submissions/{{publisher}}-{{book-name}}-submission.zip

---

## Purpose

Prepare a complete, properly formatted manuscript package that meets publisher submission requirements.

## Workflow Steps

### 1. Publisher-Specific Requirements

**Manning:**

- Chapters in Microsoft Word (.docx)
- Separate folder for images (PNG, 300 DPI)
- Code samples in ZIP file
- Metadata in Author Questionnaire form

**O'Reilly:**

- AsciiDoc or Markdown preferred
- Images in separate folders
- Atlas platform submission
- Follows O'Reilly style guide

**Packt:**

- Microsoft Word (.docx)
- Images embedded or separate
- Code in GitHub repository
- Specific formatting template

### 2. Gather All Files

**Manuscript Components:**

```
submission-package/
├── front-matter/
│   ├── preface.docx
│   ├── acknowledgments.docx
│   └── about-author.docx
├── chapters/
│   ├── chapter-01.docx
│   ├── chapter-02.docx
│   └── ...
├── back-matter/
│   ├── appendix-a.docx
│   ├── glossary.docx
│   └── index.docx
├── images/
│   ├── chapter-01/
│   ├── chapter-02/
│   └── ...
├── code/
│   └── code-examples.zip
├── metadata.txt
└── README.txt
```

### 3. Format Per Publisher

Apply required formatting:

- Heading styles (Heading 1, 2, 3)
- Code block formatting
- Figure captions
- Cross-reference format
- Citation style

### 4. Create Submission Package

Final packaging:

```
book-title-author-submission.zip
├── manuscript/
├── images/
├── code/
├── metadata.txt
└── submission-checklist.pdf
```

## Success Criteria

- [ ] All files gathered
- [ ] Publisher format applied
- [ ] Images at required resolution
- [ ] Code repository included
- [ ] Metadata complete
- [ ] Cross-references validated
- [ ] Final manuscript checklist passed

## Next Steps

1. Upload to publisher portal
2. Notify acquisition editor
3. Track submission status
