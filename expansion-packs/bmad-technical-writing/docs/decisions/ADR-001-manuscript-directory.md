# ADR-001: Use `manuscript/` Directory for Book Content

**Status**: Accepted
**Date**: 2025-10-21
**Decision Makers**: BMad Technical Writing Pack Core Team
**Version**: v2.0.0

## Context

The BMad Technical Writing Expansion Pack v1.x used `docs/` as the primary directory for storing book content (chapters, sections, outlines, etc.). This naming choice mirrored the BMad Core framework's use of `docs/` for software development artifacts (PRD, architecture, stories).

However, user feedback and semantic analysis revealed that `docs/` creates confusion in the technical book authoring context:

1. **Semantic Confusion**: In software projects, `docs/` typically means "technical documentation about the codebase" (API docs, architecture diagrams, setup guides), NOT the primary deliverable content
2. **Industry Misalignment**: Publishers and authors use "manuscript" terminology ("submit your manuscript," "working on my manuscript"), not "docs"
3. **Content Separation Issues**: Users couldn't clearly separate book manuscript from project meta-documentation
4. **GitHub Contributor Confusion**: Contributors expected `docs/` to contain project documentation, not book chapters

## Decision

**We will rename `docs/` to `manuscript/` for all book content storage in v2.0.**

This applies to:
- `docs/planning/` → `manuscript/planning/`
- `docs/sections/` → `manuscript/sections/`
- `docs/chapters/` → `manuscript/chapters/`
- `docs/outlines/` → `manuscript/outlines/`
- `docs/reviews/` → `manuscript/reviews/`

The expansion pack's own documentation (in `expansion-packs/bmad-technical-writing/docs/`) remains as `docs/` since these ARE documentation about the expansion pack itself.

## Rationale

### Why `manuscript/` is Better

1. **Industry Standard Terminology**:
   - Publishers say "manuscript submission" not "docs submission"
   - Authors think "I'm working on my manuscript" not "I'm working on my docs"
   - Aligns with professional publishing vocabulary

2. **Semantic Clarity**:
   - `manuscript/` = the book content you're writing (the deliverable)
   - `docs/` = optional project meta-documentation (about the project)
   - Clear separation allows both to coexist when needed

3. **Professional Credibility**:
   - Technical book authors are professionals in the publishing industry
   - Using industry-standard terminology increases perceived professionalism
   - Better aligns with publisher workflows and terminology

4. **GitHub/OSS Clarity**:
   - Contributors immediately understand `manuscript/` contains the book
   - No confusion about whether `docs/` means project docs or book content
   - Follows principle of least surprise

### Why NOT Keep `docs/` for Consistency with BMad Core

**Different Domains, Different Conventions**:

| Domain | BMad Component | Appropriate Directory | Rationale |
|--------|---------------|---------------------|-----------|
| Software Development | BMad Core | `docs/` | Software artifacts (PRD, architecture) ARE documentation |
| Technical Writing | Technical Writing Pack | `manuscript/` | Book content is a manuscript, not documentation |
| Game Development | Game Dev Pack | `game/` or `project/` | Game assets are projects, not documentation |
| Infrastructure | DevOps Pack | `docs/` or `infrastructure/` | Config/diagrams can be docs |

**Design Principle**: Expansion packs should use domain-appropriate terminology, not blindly copy BMad core conventions.

## Consequences

### Positive

✅ **Clear Semantic Separation**: Users can now have both `manuscript/` (book content) and `docs/` (project meta-docs) without confusion

✅ **Industry Alignment**: Professional terminology matches publisher expectations and workflows

✅ **Reduced Confusion**: New users immediately understand what `manuscript/` contains

✅ **Better GitHub UX**: Contributors see familiar, unambiguous directory names

✅ **Scalability**: Establishes pattern for future expansion packs to use domain-appropriate directories

### Negative

❌ **Breaking Change**: Requires v2.0 major version bump

❌ **Migration Required**: Existing v1.x users must update their projects

❌ **Documentation Updates**: All examples, tutorials, and guides need path updates

❌ **Inconsistency with Core**: BMad core uses `docs/`, Technical Writing pack uses `manuscript/`

### Neutral

⚡ **Learning Curve**: Users need to learn new directory structure, but migration is straightforward

⚡ **Divergence from Core**: This is intentional - domain-appropriate naming trumps consistency

## Alternatives Considered

### Alternative 1: Keep `docs/`

**Pros**:
- No breaking change
- Consistent with BMad core
- No migration needed

**Cons**:
- Perpetuates semantic confusion
- Misaligned with publishing industry
- Can't clearly separate book content from project docs
- User feedback indicates confusion

**Decision**: Rejected - semantic clarity and industry alignment are more important than avoiding breaking changes

### Alternative 2: Use `content/`

**Pros**:
- Generic and neutral
- No domain-specific terminology

**Cons**:
- Not publishing industry standard
- Too generic - could mean anything
- Doesn't convey "this is a manuscript"

**Decision**: Rejected - `manuscript/` is more precise and industry-appropriate

### Alternative 3: Use `book/`

**Pros**:
- Clear and simple
- Distinguishes from `docs/`

**Cons**:
- Less professional than "manuscript"
- Not standard publisher terminology
- "Book" is the final product, "manuscript" is what you work on

**Decision**: Rejected - `manuscript/` better matches publishing workflow terminology

## Migration Path

1. **Clear Migration Guide**: `docs/MIGRATION-v2.md` provides step-by-step instructions
2. **Simple Automated Migration**: Single `mv docs manuscript` command for most users
3. **Backward Compatibility**: v1.x documentation archived and accessible
4. **Version Bump**: Clear v2.0.0 version signals breaking change
5. **Deprecation Notice**: v1.x marked as deprecated with upgrade path

## Success Metrics

- ✅ Zero broken file paths in workflows after migration
- ✅ User feedback indicates improved clarity
- ✅ Successful migrations by 90%+ of v1.x users within 6 months
- ✅ Reduced "where do I put my chapters?" support questions

## Related Decisions

- **ADR-002** (future): Directory structure patterns for other expansion packs
- **ADR-003** (future): When to diverge from BMad core conventions

## References

- User feedback threads: Discord #technical-writing-pack (Sept-Oct 2024)
- Publisher terminology research: PacktPub, O'Reilly, Manning submission guidelines
- BMad Design Principles: "Domain-appropriate terminology over framework consistency"
- Migration guide: [docs/MIGRATION-v2.md](../MIGRATION-v2.md)

## Notes

This decision establishes an important precedent: **Expansion packs should use vocabulary appropriate to their target domain**, even if it differs from BMad core conventions. The core framework serves software development, but expansion packs serve diverse domains with their own professional terminology.

This ADR specifically addresses technical book authoring. Future expansion packs (creative writing, game development, etc.) should similarly analyze their domain's conventions and choose appropriate directory names.

---

**Last Updated**: 2025-10-21
**Supersedes**: N/A (First ADR)
**Superseded By**: N/A (Current)
