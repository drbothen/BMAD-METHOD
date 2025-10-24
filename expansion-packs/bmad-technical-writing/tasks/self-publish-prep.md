<!-- Powered by BMAD™ Core -->

# Self-Publish Prep

---

task:
id: self-publish-prep
name: Self-Publish Prep
description: Prepare book for self-publishing on Leanpub, Amazon KDP, or Gumroad
persona_default: book-publisher
inputs:

- target-platform
- book-files
- cover-design
  steps:
- Choose platform (Leanpub/Amazon KDP/Gumroad)
- Format manuscript for platform (Markdown/DOCX/PDF)
- Optimize images for platform requirements
- Create book metadata (title, description, keywords, categories)
- Design or acquire cover image
- Set pricing strategy
- Create ISBN if needed (KDP provides free ISBNs)
- Format for ePub/PDF/Kindle
- Verify platform-specific requirements
- Upload and test preview
- Run execute-checklist.md with self-publishing-standards-checklist.md
  output: self-publish/{{platform}}/{{book-name}}-ready/

---

## Purpose

Prepare a complete, professional book package for self-publishing platforms, ensuring quality presentation and discoverability.

## Workflow Steps

### 1. Choose Platform

**Leanpub:**

- Markdown-based
- Good for technical books
- Built-in email marketing
- Flexible pricing (minimum/suggested/maximum)

**Amazon KDP:**

- Largest audience
- Print-on-demand available
- Kindle format required
- Free ISBN provided

**Gumroad:**

- Simple, flexible
- PDF/ePub distribution
- Direct customer relationships
- No review requirements

### 2. Format for Platform

**Leanpub (Markdown):**

````markdown
# Chapter 1: Introduction

{book: true, sample: true}

This chapter introduces...

## Section 1.1

Content here...

{class: code}

```python
# Code example
```
````

**KDP (Word/ePub):**

- Use heading styles
- Insert page breaks
- Format code blocks
- Embed images

### 3. Create Metadata

**Title and Description:**

```
Title: Mastering Web APIs: A Practical Guide to REST and GraphQL

Subtitle: Build, Secure, and Scale Production-Ready APIs

Description:
Learn to design, build, and deploy production-ready APIs with this hands-on guide.
Covers REST, GraphQL, authentication, rate limiting, and more. Includes 50+ code
examples in Python and Node.js.

What you'll learn:
• RESTful API design principles
• GraphQL schema design
• JWT authentication
• Rate limiting and caching
• Production deployment strategies
```

**Keywords/Categories:**

```
Keywords: API, REST, GraphQL, web development, Python, Node.js, authentication

Categories:
- Computers > Programming > Internet
- Computers > Web > Web Services
- Computers > Languages > Python
```

### 4. Cover Design

Requirements:

- **KDP**: 2560 x 1600 px minimum
- **Leanpub**: 1600 x 2400 px recommended
- **Readable thumbnail**: Text visible at small sizes
- **Professional**: Use Canva, 99designs, or hire designer

### 5. Set Pricing

Pricing strategy:

**Leanpub Pricing Model:**

```
Minimum: $9.99 (reader can pay more)
Suggested: $29.99
Maximum: $99
```

**KDP Pricing:**

```
eBook: $9.99 - $29.99 (70% royalty tier)
Print: $39.99 (based on page count + margin)
```

### 6. ISBN (Optional)

- **KDP**: Provides free ISBN
- **Self-purchase**: $125 for single ISBN from Bowker (US)
- **Not required** for eBooks on most platforms

### 7. Format for Distribution

**ePub (KDP, Gumroad):**

- Use Calibre or Pandoc for conversion
- Test on multiple e-readers
- Validate with ePub validator

**PDF (Leanpub, Gumroad):**

- High-quality PDF export
- Embedded fonts
- Optimized images

**Kindle (KDP):**

- Upload DOCX or use Kindle Create tool
- KDP converts to .mobi/.azw

### 8. Platform-Specific Requirements

**KDP:**

- Copyright page required
- Table of contents with links
- "Look Inside" preview (first 10%)

**Leanpub:**

- Subset.txt for sample chapters
- Book.txt for chapter ordering
- Metadata in Book.txt

### 9. Upload and Preview

Test before publishing:

- Upload to platform
- Generate preview
- Test on multiple devices (Kindle app, iPad, PDF reader)
- Check formatting, images, code blocks
- Verify table of contents links

### 10. Run Quality Checklist

- Run execute-checklist.md with self-publishing-standards-checklist.md

## Success Criteria

- [ ] Platform selected
- [ ] Manuscript formatted correctly
- [ ] Images optimized
- [ ] Metadata complete (title, description, keywords)
- [ ] Professional cover design
- [ ] Pricing set
- [ ] ISBN acquired (if needed)
- [ ] ePub/PDF/Kindle formats created
- [ ] Preview tested on target devices
- [ ] Self-publishing checklist passed

## Next Steps

1. Publish to platform
2. Set up marketing (email list, social media)
3. Monitor sales and reviews
4. Plan updates and revisions
