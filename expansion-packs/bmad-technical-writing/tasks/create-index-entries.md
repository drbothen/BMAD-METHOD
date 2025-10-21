<!-- Powered by BMAD™ Core -->

# Create Index Entries

---

task:
id: create-index-entries
name: Create Index Entries
description: Generate comprehensive book index with primary entries, secondary entries, and cross-references
persona_default: technical-editor
inputs:

- final-manuscript
- key-terms-list
- publisher-index-guidelines
  steps:
- Extract all key terms from manuscript
- Identify technical terms, concepts, APIs, methods
- Create primary index entries (main term)
- Create secondary entries (sub-topics under main term)
- Add cross-references ("See also...")
- Ensure consistent terminology
- Organize alphabetically
- Add page number placeholders
- Review for completeness (all important terms indexed)
- Format per publisher requirements
- Run execute-checklist.md with index-completeness-checklist.md
  output: docs/index/{{book-name}}-index.md

---

## Purpose

Create a comprehensive index that helps readers quickly locate information. A good index makes technical books significantly more useful as reference materials.

## Workflow Steps

### 1. Extract Key Terms

Identify indexable content:

- **Technical terms**: API, HTTP, REST, JSON
- **Concepts**: Authentication, caching, rate limiting
- **Tools/frameworks**: Express.js, Flask, Django
- **Methods/functions**: `app.get()`, `request.json()`
- **Patterns**: MVC, Singleton, Factory
- **Acronyms**: CRUD, JWT, CORS

### 2. Create Primary Entries

Main index entries:

```
API (Application Programming Interface), 23, 45-52, 89
  authentication, 105-112
  design principles, 67-74
  documentation, 156-163
  REST vs GraphQL, 91-98
  versioning, 142-149

Caching, 201-218
  cache invalidation, 210-212
  HTTP caching headers, 205-209
  Redis implementation, 213-218
```

### 3. Add Secondary Entries

Sub-topics under main terms:

```
Express.js, 34-82
  error handling, 76-82
  middleware, 48-55
  routing, 38-47
  testing, 171-180
```

### 4. Cross-References

Link related topics:

```
Authentication, 105-112
  See also Security, Authorization

JWT (JSON Web Tokens), 108-110
  See also Authentication, Tokens

Tokens
  access tokens, 110
  refresh tokens, 111
  See also JWT, Authentication
```

### 5. Ensure Consistency

Maintain uniform terminology:

```
✅ Correct - Consistent terminology:
API design, 67
REST API, 91
API authentication, 105

❌ Inconsistent:
API design, 67
Designing APIs, 67 (duplicate)
Rest api, 91 (capitalization inconsistent)
```

### 6. Format Per Publisher

Follow publisher guidelines:

**Manning/O'Reilly Style:**
```
Term, page numbers
  subterm, page numbers
  subterm, page numbers
```

**LaTeX Style:**
```
\index{API}
\index{API!authentication}
\index{API!design}
```

### 7. Add Page Placeholders

Structure for page numbering:

```
API (Application Programming Interface), [TK], [TK]-[TK]
  authentication, [TK]-[TK]
  design principles, [TK]-[TK]

Note: [TK] = "To Come" placeholder for page numbers
```

## Success Criteria

- [ ] All key terms indexed
- [ ] Primary and secondary entries created
- [ ] Cross-references added
- [ ] Consistent terminology
- [ ] Alphabetically organized
- [ ] Publisher format followed
- [ ] Index completeness checklist passed

## Next Steps

1. Submit index to publisher for page numbering
2. Review final index in page proofs
3. Update any missing entries
