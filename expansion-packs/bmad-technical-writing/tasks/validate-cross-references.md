<!-- Powered by BMAD™ Core -->

# Validate Cross References

---

task:
id: validate-cross-references
name: Validate Cross References
description: Verify all cross-references, internal links, external URLs, and citations are accurate
persona_default: technical-editor
inputs:

- manuscript-files
- reference-type
- validation-scope
  steps:
- Extract all cross-references (Chapter X, see Section Y, etc.)
- Verify chapter and section numbers are correct
- Check page number references (if used)
- Validate internal links work
- Verify external links (URLs) are accessible
- Check glossary references
- Validate index references
- Ensure bidirectional references (if A references B does B note A)
- Test all code repository links
- Update broken or outdated references
- Create cross-reference validation log
  output: docs/validation/cross-reference-validation-log.md

---

## Purpose

Ensure all references, links, and citations are accurate and functional, preventing reader frustration and maintaining book credibility.

## Workflow Steps

### 1. Extract All Cross-References

Find all references:

**Internal references:**

- "See Chapter 5"
- "As discussed in Section 3.2"
- "Refer to Figure 7.4"
- "Exercise 2.3 demonstrates..."
- "Appendix B contains..."

**External references:**

- URLs to documentation
- Code repository links
- API documentation links
- Tool download links

### 2. Verify Chapter/Section Numbers

Check accuracy:

```markdown
✅ Correct:
"In Chapter 3, we learned about REST APIs..." [Chapter 3 exists and covers REST]

❌ Incorrect:
"See Chapter 8 for deployment details" [Chapter 8 is about testing, not deployment]
```

**Validation script (conceptual):**

```python
# Check all "Chapter X" references
references = extract_references(manuscript, pattern=r'Chapter \d+')
for ref in references:
    chapter_num = ref.chapter_number
    if chapter_num > total_chapters:
        print(f"ERROR: Reference to non-existent {ref}")
```

### 3. Check Page References

Validate page numbers:

```markdown
⚠️ During manuscript phase:
"See page [TK]" or "See Chapter 3" (not page numbers)

✅ During page proof phase:
"See page 87 for details"
```

### 4. Validate Internal Links

Test document links:

**Markdown:**

```markdown
[Link to Section 3.2](#section-32)

# Check target exists:

<a name="section-32"></a>

## 3.2 API Design Patterns
```

**HTML/ePub:**

```html
<a href="#chapter-03">Chapter 3</a>

<!-- Verify target exists: -->
<div id="chapter-03">...</div>
```

### 5. Verify External Links

Test URL accessibility:

```python
# Check all URLs
import requests

urls = extract_urls(manuscript)
broken_links = []

for url in urls:
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code >= 400:
            broken_links.append((url, response.status_code))
    except requests.RequestException as e:
        broken_links.append((url, str(e)))

# Report broken links
for url, error in broken_links:
    print(f"BROKEN: {url} - {error}")
```

**Common issues:**

- 404 Not Found (page removed)
- Moved permanently (update URL)
- SSL certificate errors
- Timeout (site down)

### 6. Check Glossary References

Verify glossary terms:

```markdown
The API uses JWT (see Glossary) for authentication.

[Verify "JWT" entry exists in glossary]
```

### 7. Validate Index References

Cross-check index:

```markdown
Index entry: "Authentication, 45, 78, 103"

[Verify pages 45, 78, and 103 actually discuss authentication]
```

### 8. Ensure Bidirectional References

Check both directions:

```markdown
Chapter 3 says: "Authentication is covered in Chapter 7"

[Verify Chapter 7 mentions being referenced from Chapter 3, if appropriate]

✅ Chapter 7: "As introduced in Chapter 3, authentication..."
```

### 9. Test Code Repository Links

Validate repo access:

```markdown
Code for this chapter: https://github.com/author/book/tree/main/chapter-03

[Test link opens correctly]
[Verify chapter-03 folder exists]
[Check README.md in folder is accurate]
```

### 10. Create Validation Log

Document findings:

```markdown
# Cross-Reference Validation Log

Date: 2024-01-15
Validator: [Name]
Manuscript Version: Draft 3.2

## Summary

- Total references checked: 247
- Valid references: 239 (96.8%)
- Broken references: 8 (3.2%)

## Issues Found

### High Priority (Broken Links)

1. Chapter 5, Line 234: "See Chapter 9" → Chapter 9 doesn't exist (was split into Ch 9-10)
   - **Fix**: Update to "See Chapters 9 and 10"

2. Chapter 7, Line 89: https://oldapi.example.com/docs → 404 Not Found
   - **Fix**: Update to https://api.example.com/v2/docs

### Medium Priority (Outdated References)

3. Chapter 3, Line 145: "Appendix A" → Content moved to Appendix B
   - **Fix**: Update reference

### Low Priority (Inconsistencies)

4. Chapter 4: Uses "Section 3.2" and "section 3.2" inconsistently
   - **Fix**: Standardize capitalization

## Verification Status

| Reference Type  | Total | Valid | Broken |
| --------------- | ----- | ----- | ------ |
| Chapter refs    | 87    | 85    | 2      |
| Section refs    | 64    | 64    | 0      |
| Figure refs     | 42    | 40    | 2      |
| External URLs   | 31    | 27    | 4      |
| Code repo links | 18    | 18    | 0      |
| Glossary refs   | 5     | 5     | 0      |

## Next Steps

1. Fix all high-priority broken references
2. Update outdated references
3. Standardize reference formatting
4. Re-validate after changes
```

## Success Criteria

- [ ] All cross-references extracted
- [ ] Chapter/section numbers verified
- [ ] Page references validated (if applicable)
- [ ] Internal links tested
- [ ] External URLs checked for accessibility
- [ ] Glossary references confirmed
- [ ] Index references validated
- [ ] Bidirectional references verified
- [ ] Code repository links tested
- [ ] Validation log created with findings

## Next Steps

1. Fix all broken references
2. Update outdated links
3. Standardize reference formatting
4. Re-validate after corrections
5. Include validation in revision process
