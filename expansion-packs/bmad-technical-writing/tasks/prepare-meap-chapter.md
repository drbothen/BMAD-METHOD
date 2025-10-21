<!-- Powered by BMAD™ Core -->

# Prepare MEAP Chapter

---

task:
id: prepare-meap-chapter
name: Prepare MEAP Chapter
description: Prepare chapter for Manning Early Access Program (MEAP) release
persona_default: book-publisher
inputs:

- chapter-number
- chapter-file
- book-context
  steps:
- Ensure chapter works standalone (introduction includes context)
- Verify chapter doesn't require unreleased chapters
- Check author voice consistency
- Link code repository clearly
- Apply Manning MEAP-specific formatting
- Add MEAP disclaimer if needed
- Include "what's coming next" section
- Run execute-checklist.md with manning-meap-checklist.md
- Run execute-checklist.md with meap-readiness-checklist.md
- Create MEAP package
- Test chapter reads well independently
  output: meap/chapter-{{n}}-meap-ready.docx

---

## Purpose

Prepare a chapter for early release through Manning's MEAP program, ensuring it provides value to early readers even before the complete book is finished.

## Workflow Steps

### 1. Make Chapter Standalone

Provide necessary context:

**Add Chapter Introduction:**
```
This chapter covers [topic]. In the previous chapter, you learned [previous topic brief summary].
In this chapter, you'll discover [current topic]. By the end, you'll be able to [learning outcomes].

Note: This is an early access chapter. Some cross-references to future chapters are placeholders.
```

### 2. No Forward References

Avoid referencing unreleased content:

```
❌ "As we'll see in Chapter 8..."
✅ "In a future chapter on deployment..."

❌ "See Section 7.3 for details"
✅ "This will be covered in detail in the final book"
```

### 3. Link Code Repository

Make code easily accessible:

```
Code Examples

All code for this chapter is available at:
https://github.com/username/book-code/tree/main/chapter-05

Download: [Download ZIP button/link]
```

### 4. Add "What's Coming Next"

Preview future content:

```
## Coming in Future Chapters

In the next chapter, you'll learn about:
- Topic 1
- Topic 2
- Topic 3

Future chapters will cover:
- Advanced patterns (Chapter 7)
- Production deployment (Chapter 9)
- Performance optimization (Chapter 10)
```

### 5. MEAP Disclaimer

Set expectations:

```
📘 MEAP Early Access Notice

This is an early access chapter. You may encounter:
- Placeholders for future cross-references
- Draft diagrams or images
- Sections marked [TBD]

Your feedback helps shape the final book! Please share thoughts at:
[feedback forum link]
```

## Success Criteria

- [ ] Chapter works standalone
- [ ] No unreleased chapter references
- [ ] Code repository linked
- [ ] MEAP formatting applied
- [ ] "What's next" section included
- [ ] Disclaimer added
- [ ] MEAP checklists passed
- [ ] Independent reading tested

## Next Steps

1. Submit to Manning MEAP portal
2. Monitor reader feedback
3. Incorporate feedback into revisions
