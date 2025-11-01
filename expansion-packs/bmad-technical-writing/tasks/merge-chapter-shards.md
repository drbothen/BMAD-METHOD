<!-- Powered by BMAD™ Core -->

# Merge Chapter Shards

---

task:
id: merge-chapter-shards
name: Merge Chapter Shards
description: Reassemble sharded chapter files with consistency checking and validation
persona_default: tutorial-architect
inputs: - shard-directory-path - shard-index-file
steps: - Read shard index to identify all shard files - Validate all shards exist and are in correct order - Check for conflicting modifications across shards - Concatenate shards in proper sequence - Remove shard metadata headers - Validate merged content completeness and formatting - Create backup of original if it exists - Save merged chapter file
output: Reassembled chapter file with all shard content merged

---

## Purpose

This task reassembles a sharded chapter back into a single complete chapter file with:

- Content integrity validation
- Consistency checking across shards
- Formatting preservation
- Conflict detection for modified shards
- Quality assurance before final merge

## When to Use This Task

**Merge shards when:**

- Editing of individual shards is complete
- Ready for full chapter review
- Preparing chapter for publication
- Need complete chapter for formatting/layout
- Final review requires full chapter context

**Don't merge when:**

- Still actively editing individual shards
- Reviewers working on specific shards
- Shards have conflicting unresolved changes

## Prerequisites

Before merging:

- All shard files exist and are accessible
- Shard index file is complete and accurate
- All shard edits are saved and committed
- Any shard-specific reviews are complete
- Backup of original chapter exists (if applicable)

## Workflow Steps

**Note:** This task references config paths (e.g., {{config.manuscript.*}}). Load `.bmad-technical-writing/config.yaml` at the start to resolve these paths, or use defaults: `manuscript/{type}`, `code-examples`.

### 1. Read Shard Index

Load and parse the shard index file:

**Locate index file:**

- Look for `{chapter-name}-shards-index.md` in shard directory
- Example: `chapter-7-shards/chapter-7-shards-index.md`

**Extract key information:**

```markdown
Original File: chapter-7-advanced-queries.md
Total Pages: 32
Shard Count: 6
Split Date: 2025-10-26
```

**Build shard file list:**

1. Read "Shards" section from index
2. Extract filenames in order
3. Note page ranges for validation
4. Document section assignments

**Example extracted data:**

```
Shard List:
1. chapter-7-shard-1.md (pages 1-6)
2. chapter-7-shard-2.md (pages 7-12)
3. chapter-7-shard-3.md (pages 13-17)
4. chapter-7-shard-4.md (pages 18-23)
5. chapter-7-shard-5.md (pages 24-29)
6. chapter-7-shard-6.md (pages 30-32)
```

### 2. Validate Shards

Verify all shards are present and properly formatted:

**Existence check:**

- [ ] All shard files exist at expected paths
- [ ] No shards are missing from sequence
- [ ] No extra unexpected shard files present
- [ ] Shard numbering is sequential (1, 2, 3... not 1, 3, 5)

**Metadata validation:**

For each shard, check metadata header:

```markdown
<!-- SHARD METADATA -->
<!-- Original: chapter-7-advanced-queries.md -->
<!-- Shard: 1 of 6 -->
<!-- Pages: 1-6 of 32 -->
<!-- Sections: Introduction, Setup -->
<!-- Split Date: 2025-10-26 -->
<!-- END METADATA -->
```

- [ ] Metadata header present
- [ ] Shard number matches position
- [ ] Original filename consistent across shards
- [ ] Total shard count matches index
- [ ] Page ranges are sequential and non-overlapping

**Order validation:**

- [ ] Shard 1 comes first
- [ ] Shard N comes last
- [ ] No gaps in sequence

**If validation fails:**

- HALT and report missing/misordered shards
- Do not proceed with merge
- Fix shard issues before retrying

### 3. Check for Conflicts

Detect potential issues from shard modifications:

**Modification check:**

Compare modification dates:

1. Check file modification timestamps
2. Compare to Split Date in metadata
3. Identify which shards were modified

**Report modifications:**

```
Modified Shards:
- shard-2.md: Modified 2025-10-27 (1 day after split)
- shard-4.md: Modified 2025-10-28 (2 days after split)
- shard-6.md: Modified 2025-10-26 (same day as split)
```

**Conflict detection:**

Look for potential conflicts:

- [ ] Duplicate section headings introduced
- [ ] Cross-references that may now be broken
- [ ] Inconsistent terminology across modified shards
- [ ] Heading level mismatches at shard boundaries
- [ ] Code block fence mismatches (opened in one shard, closed in another)

**Heading continuity check:**

```
Shard 1 ends with: ### Setting Up PostgreSQL
Shard 2 starts with: ## Complex Joins
✓ Valid - proper heading progression
```

**Cross-reference validation:**

Check references documented in index:

- Do cross-shard references still make sense?
- Were any referenced sections renamed/removed?
- Are section numbers still accurate?

**Manual review trigger:**

If conflicts detected, prompt for manual review:

```
⚠️ Potential conflicts detected:
- Shard 3 references "Section 2.1" but Shard 2 was modified
- Shard 5 modified heading "Query Optimization" → "Performance Tuning"
- Cross-reference in Shard 6 may be affected

Recommended: Review modified shards before merging.
Proceed with merge? (yes/no)
```

### 4. Merge Shards

Concatenate shard content in proper order:

**Merge algorithm:**

```
1. Initialize empty merged_content string
2. For each shard in order (1, 2, 3...):
   a. Read shard file content
   b. Remove metadata header section
   c. Append content to merged_content
   d. Add newline separator between shards
3. Return merged_content
```

**Metadata removal:**

Remove lines between and including:

```markdown
<!-- SHARD METADATA -->

...

<!-- END METADATA -->
```

**Content preservation:**

- Keep ALL content after metadata header
- Preserve exact formatting (spaces, tabs, newlines)
- Don't modify heading levels
- Don't adjust cross-references
- Don't reformat code blocks
- Keep all markdown exactly as written

**Shard boundary handling:**

Ensure smooth transitions:

- Check that headings connect logically
- No duplicate content at boundaries
- Proper spacing between sections
- Code blocks not split across boundary

**Example merge:**

```markdown
<!-- From shard 1 (after removing metadata) -->

# Chapter 7: Advanced PostgreSQL Queries

## Introduction

[content...]

## Setting Up the Environment

[content...]

<!-- From shard 2 (after removing metadata) -->

## Complex Joins

[content...]

## Subqueries

[content...]
```

### 5. Validate Merged Chapter

Verify merged content quality:

**Completeness check:**

- [ ] Total page count approximately matches original estimate
- [ ] All major sections from index present
- [ ] All ## headings accounted for
- [ ] No missing content (compare to shard index section list)

**Formatting check:**

- [ ] No duplicate headings from merge artifacts
- [ ] Code blocks properly closed (every `has matching`)
- [ ] No broken tables
- [ ] Lists properly formatted
- [ ] No extra blank lines at shard boundaries

**Heading hierarchy check:**

Validate heading structure:

```
# (should be only one - chapter title)
## (major sections)
### (subsections)
#### (sub-subsections)
```

- [ ] No H2 following H4 (skipping levels)
- [ ] Logical progression maintained
- [ ] Heading levels consistent throughout

**Code block validation:**

For each code block:

- [ ] Opening ``` present
- [ ] Closing ``` present
- [ ] Language tag present (if used originally)
- [ ] Content intact

**Cross-reference validation:**

Check references are still valid:

- [ ] Section references point to existing sections
- [ ] Chapter references accurate
- [ ] Code file references match actual files
- [ ] URL links valid (if any)

**Quick validation commands:**

````bash
# Check for unclosed code blocks
grep -c '^```' merged-chapter.md
# Should be even number

# Find all headings
grep '^#' merged-chapter.md

# Check for duplicate section titles
grep '^##' merged-chapter.md | sort | uniq -d
````

### 6. Save Merged Chapter

Write the merged content to final file:

**Backup original (if exists):**

If original chapter file exists:

```bash
cp chapter-7-advanced-queries.md chapter-7-advanced-queries.md.backup-2025-10-26
```

- Use date-stamped backup name
- Keep in same directory or backups/ folder
- Document backup in merge notes

**Save merged chapter:**

Write to original filename:

- Location: `{{config.manuscript.chapters}}/chapter-7-advanced-queries.md`
- Format: UTF-8 Markdown
- Line endings: LF (Unix-style)
- Final newline: Yes

**Document merge:**

Add note at bottom of merged file (optional):

```markdown
---

<!-- Merge Info -->
<!-- Merged from 6 shards on 2025-10-26 -->
<!-- Original shards: chapter-7-shards/ -->
<!-- Shard edits: shards 2, 4, 6 modified -->
<!-- END Merge Info -->
```

**Post-merge organization:**

Option 1 - Archive shards:

```
{{config.manuscript.chapters}}/
├── chapter-7-advanced-queries.md           # Merged
├── chapter-7-advanced-queries.md.backup    # Original backup
└── chapter-7-shards/                       # Archive (keep for reference)
    ├── chapter-7-shards-index.md
    ├── chapter-7-shard-1.md
    └── ...
```

Option 2 - Remove shards (if confident):

```
{{config.manuscript.chapters}}/
├── chapter-7-advanced-queries.md           # Merged
└── chapter-7-advanced-queries.md.backup    # Original backup
```

**Recommendation:** Keep shard directory for at least one review cycle before removing.

### 7. Report Merge Results

Provide summary of merge operation:

```markdown
✅ Merge Completed Successfully

**Source:**

- Shard Directory: {{config.manuscript.chapters}}/chapter-7-shards/
- Shard Count: 6
- Shards Merged: chapter-7-shard-1.md through chapter-7-shard-6.md

**Output:**

- Merged File: {{config.manuscript.chapters}}/chapter-7-advanced-queries.md
- Total Pages: ~32 (estimated)
- Total Sections: 8 major sections
- Total Code Blocks: 12

**Modified Shards:**

- Shard 2: Modified 2025-10-27 (complex joins section updated)
- Shard 4: Modified 2025-10-28 (window functions examples added)
- Shard 6: Modified 2025-10-26 (exercises refined)

**Validation:**

- ✓ All shards present and in order
- ✓ Metadata headers removed
- ✓ Heading hierarchy validated
- ✓ Code blocks properly closed
- ✓ Cross-references checked
- ✓ No duplicate content detected

**Backup:**

- Original backed up to: chapter-7-advanced-queries.md.backup-2025-10-26

**Next Steps:**

1. Review merged chapter for quality
2. Run full chapter validation
3. Commit merged chapter to repository
4. Archive or remove shard directory
```

## Output

The merge produces:

**Merged chapter file:**

- Format: Markdown (.md)
- Location: Original chapter path
- Content: All shards concatenated without metadata
- Validation: Formatting and completeness checked

**Backup file:**

- Original chapter (if existed) backed up with timestamp
- Preserves pre-merge state

**Merge report:**

- Summary of merge operation
- List of modified shards
- Validation results
- Any warnings or issues

## Quality Standards

A successful merge has:

✓ All shards included in correct order
✓ Metadata headers completely removed
✓ No duplicate or missing content
✓ Formatting fully preserved
✓ Heading hierarchy validated
✓ Code blocks properly closed
✓ Cross-references intact
✓ Original backed up (if existed)

## Common Issues

**Issue: Shard missing from sequence**

- Symptom: Shard 1, 2, 4, 5 exist but shard 3 missing
- Solution: Locate missing shard or re-shard original chapter

**Issue: Heading level jump**

- Symptom: H2 directly followed by H4 (skipping H3)
- Solution: Review shard modifications, adjust heading levels

**Issue: Unclosed code block**

- Symptom: Odd number of ``` markers
- Solution: Find and close code block, check shard boundaries

**Issue: Duplicate section heading**

- Symptom: Same ## heading appears twice
- Solution: Review shard edits, rename or merge duplicate sections

**Issue: Broken cross-reference**

- Symptom: Reference to "Section 2.1" but no such section exists
- Solution: Update cross-reference to match actual section

**Issue: Content mismatch**

- Symptom: Merged content doesn't match expected page count
- Solution: Validate each shard, check for missing content

## Merge Consistency Checks

**Heading continuity:**

```python
# Pseudocode
headings = extract_all_headings(merged_chapter)
for i in range(len(headings) - 1):
    current_level = heading_level(headings[i])
    next_level = heading_level(headings[i+1])
    if next_level > current_level + 1:
        warn(f"Skipped heading level: {headings[i]} → {headings[i+1]}")
```

**Code block balance:**

````bash
# Must be even (every opening has closing)
fence_count=$(grep -c '^```' merged-chapter.md)
if [ $((fence_count % 2)) -ne 0 ]; then
    echo "ERROR: Unclosed code block detected"
fi
````

**Section completeness:**

```python
# Compare index to merged
index_sections = extract_sections_from_index()
merged_sections = extract_sections_from_chapter()
missing = set(index_sections) - set(merged_sections)
extra = set(merged_sections) - set(index_sections)
if missing:
    warn(f"Missing sections: {missing}")
if extra:
    warn(f"Unexpected sections: {extra}")
```

## Best Practices

**Before merging:**

- Commit all shard changes
- Review shard index for accuracy
- Note any significant shard modifications
- Create checkpoint backup

**During merge:**

- Validate each step
- Don't skip consistency checks
- Preserve formatting exactly
- Document any issues found

**After merge:**

- Review merged chapter thoroughly
- Run linting/validation tools
- Test all code examples
- Verify cross-references
- Keep shards until merge validated

## Troubleshooting

**Merge produces unexpected content:**

1. Check shard order in index matches actual order
2. Verify no shards were skipped
3. Review shard modifications
4. Compare merged output to shard preview

**Formatting issues after merge:**

1. Check metadata removal was complete
2. Verify no extra newlines at shard boundaries
3. Ensure code blocks not split at boundaries
4. Review heading levels at transitions

**Cross-references broken:**

1. Check if referenced sections were renamed in shards
2. Update references to match current section names
3. Document cross-shard dependencies in index

**Content appears duplicated:**

1. Check for overlapping page ranges in shards
2. Verify each shard has unique content
3. Review merge algorithm for duplicate concatenation

## Advanced: Conflict Resolution

When modified shards have conflicts:

**Terminology conflicts:**

```
Shard 2: Uses "database" throughout
Shard 5: Uses "DB" throughout
→ Choose one term, update for consistency
```

**Cross-reference conflicts:**

```
Shard 3 references "Section 2: Joins"
But Shard 2 now titled "Section 2: SQL Joins"
→ Update reference in shard 3 before merging
```

**Code example conflicts:**

```
Shard 4 shows example using "users" table
Shard 5 shows example using "customers" table
Both meant to be same entity
→ Standardize table naming before merging
```

## Next Steps

After merging the chapter:

1. Review merged chapter for quality and flow
2. Run technical-review-chapter.md on complete chapter
3. Test all code examples end-to-end
4. Validate cross-references and links
5. Run copy-edit-chapter.md for editorial polish
6. Commit final merged chapter to repository
7. Archive or remove shard directory after validation period

## Related Resources

- Task: shard-large-chapter.md - Creating chapter shards
- Task: technical-review-chapter.md - Reviewing complete chapters
- Task: validate-cross-references.md - Checking chapter references
- Task: copy-edit-chapter.md - Editorial review
