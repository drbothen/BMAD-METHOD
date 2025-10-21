# Migration Guide: v1.x → v2.0

This guide helps you migrate your existing technical writing projects from BMad Technical Writing Pack v1.x to v2.0.

## 🚨 Breaking Changes

### Directory Structure Change

**v1.x**: Used `docs/` directory for manuscript content
**v2.0**: Uses `manuscript/` directory for book content

This change provides semantic clarity - `manuscript/` clearly indicates "the book you're writing" using publishing industry standard terminology, while `docs/` typically means "technical documentation about the codebase" in software projects.

## 🔄 Migration Steps

### Quick Migration (Recommended)

If you're using standard structure with no customizations:

```bash
# 1. Navigate to your book project
cd /path/to/your-book-project

# 2. Rename the docs directory to manuscript
mv docs manuscript

# 3. Update any custom scripts or README files you created
# (See "Update Custom Scripts" section below)

# 4. Verify migration
ls -la manuscript/
```

That's it! Your project is now v2.0 compatible.

### Manual Migration (If you have non-standard structure)

If your project has custom organization or mixed content:

```bash
# 1. Create new manuscript directory
mkdir manuscript

# 2. Move book content subdirectories
mv docs/planning manuscript/planning
mv docs/sections manuscript/sections
mv docs/chapters manuscript/chapters
mv docs/outlines manuscript/outlines
mv docs/reviews manuscript/reviews

# 3. If you have project documentation, keep docs/ directory
# (Now docs/ is for project meta-documentation, which is semantically correct)
# Keep files like: docs/README.md, docs/publisher-notes.md, etc.
```

### Update Custom Scripts

If you created any custom bash scripts, Makefiles, or automation:

```bash
# Find all your custom scripts that reference the old paths
grep -r "docs/planning\|docs/sections\|docs/chapters\|docs/outlines\|docs/reviews" . \
  --include="*.sh" --include="*.md" --include="Makefile"

# Update them using sed (create backups first)
find . -name "*.sh" -o -name "Makefile" | while read file; do
  sed -i.bak 's|docs/planning|manuscript/planning|g' "$file"
  sed -i.bak 's|docs/sections|manuscript/sections|g' "$file"
  sed -i.bak 's|docs/chapters|manuscript/chapters|g' "$file"
  sed -i.bak 's|docs/outlines|manuscript/outlines|g' "$file"
  sed -i.bak 's|docs/reviews|manuscript/reviews|g' "$file"
done

# Review changes and delete backups when satisfied
rm *.bak
```

### Update Git Tracked Files

If you're using version control:

```bash
# Git will automatically track the rename if you use mv
git status  # You should see renames

# Or explicitly tell git about the rename
git mv docs manuscript

# Commit the migration
git add .
git commit -m "chore: migrate to v2.0 manuscript/ directory structure

Breaking change: Rename docs/ to manuscript/ for semantic clarity
and alignment with publishing industry terminology.

See: docs/MIGRATION-v2.md"

# Push changes
git push
```

## ✅ Verification Checklist

After migration, verify everything is working:

- [ ] `manuscript/planning/` directory exists with your book plans
- [ ] `manuscript/sections/` directory exists with your section drafts
- [ ] `manuscript/chapters/` directory exists with your chapter files
- [ ] `manuscript/outlines/` directory exists with your outlines
- [ ] `manuscript/reviews/` directory exists with your review reports
- [ ] No broken references in your custom scripts
- [ ] Git history preserved (if using version control)
- [ ] Documentation README files updated with new paths
- [ ] Workflows execute correctly with new paths

## 🔍 Troubleshooting

### Issue: "Command not found" or "File not found" errors

**Cause**: Custom scripts still reference old `docs/` paths

**Solution**: Run the "Update Custom Scripts" commands above to find and replace old paths

### Issue: Git shows deleted files instead of renames

**Cause**: Git didn't detect the rename automatically

**Solution**:
```bash
# Tell git explicitly about renames
git add manuscript/
git add -u  # Updates removed files
git status  # Should now show as renames
```

### Issue: Mixed content in docs/ directory

**Cause**: You have both manuscript content AND project documentation in `docs/`

**Solution**: Selectively move only manuscript-related subdirectories:
```bash
# Move only manuscript content
mv docs/planning manuscript/
mv docs/sections manuscript/
mv docs/chapters manuscript/
mv docs/outlines manuscript/
mv docs/reviews manuscript/

# Keep project documentation in docs/
# (Files like README.md, publisher-correspondence/, etc.)
```

### Issue: Workflows fail after migration

**Cause**: Old BMad expansion pack version still installed

**Solution**: Update to v2.0:
```bash
npx bmad-method install
# Select "Technical Writing Pack v2.0" to update
```

## 📊 What Changed in v2.0

### File Path Changes

| v1.x Path | v2.0 Path |
|-----------|-----------|
| `docs/planning/` | `manuscript/planning/` |
| `docs/sections/` | `manuscript/sections/` |
| `docs/chapters/` | `manuscript/chapters/` |
| `docs/outlines/` | `manuscript/outlines/` |
| `docs/reviews/` | `manuscript/reviews/` |

### What DIDN'T Change

- ✅ All workflows still work the same way
- ✅ All agent commands unchanged
- ✅ All templates unchanged (except file paths)
- ✅ All tasks unchanged (except file paths)
- ✅ No changes to workflow logic or agent behavior
- ✅ Section-driven development approach unchanged

### New Semantic Separation

**v2.0 introduces clear semantic boundaries**:

- `manuscript/` = Your book content (the deliverable)
- `code-examples/` = Supporting code
- `images/` = Supporting visuals
- `submission/` = Publisher-ready packages
- `docs/` = Optional project meta-documentation

## 🆘 Need Help?

If you encounter issues during migration:

1. **Check the FAQ**: [docs/faq.md](./faq.md#migration-questions)
2. **Troubleshooting Guide**: [docs/troubleshooting.md](./troubleshooting.md)
3. **Discord Support**: https://discord.gg/gk8jAdXWmj
4. **GitHub Issues**: https://github.com/bmadcode/bmad-method/issues

## 📝 Rollback (If Needed)

If you need to rollback to v1.x:

```bash
# Simple rollback
mv manuscript docs

# Or if you kept both directories
rm -rf manuscript  # Be careful!

# Reinstall v1.x expansion pack
npx bmad-method install
# Select "Technical Writing Pack v1.x"
```

**Note**: We recommend migrating to v2.0 as v1.x will be deprecated. Future features will only be added to v2.0+.

## 🎯 Migration Success!

Once you've completed the migration and verification checklist, you're ready to use all v2.0 features with the improved semantic clarity of the `manuscript/` directory structure.

Welcome to BMad Technical Writing Pack v2.0! 🎉
