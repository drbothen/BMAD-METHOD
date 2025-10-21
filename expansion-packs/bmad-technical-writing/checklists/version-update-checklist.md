# Version Update Quality Checklist

Use this checklist when updating a chapter for a new technology version (e.g., Python 3.9 → 3.12, Node 16 → 20).

## Import Statements

- [ ] All import statements reviewed for version compatibility
- [ ] Deprecated import paths updated to current equivalents
- [ ] New import patterns adopted where applicable (e.g., Python 3.10+ built-in generics)
- [ ] Import organization follows existing book patterns
- [ ] No warnings about deprecated imports when code runs

## Deprecated Methods/APIs

- [ ] All deprecated methods identified and replaced
- [ ] Replacement methods functionally equivalent
- [ ] Breaking changes addressed (behavior differences handled)
- [ ] Deprecation warnings eliminated
- [ ] Documentation links updated to current API docs

## New Syntax Features

- [ ] New syntax features considered for adoption (match/case, type hints, etc.)
- [ ] New syntax used only where pedagogically appropriate
- [ ] New syntax doesn't obscure the concept being taught
- [ ] Explanatory text updated to explain new syntax
- [ ] Syntax level appropriate for target audience

## Code Testing

- [ ] All code examples tested on exact target version
- [ ] Code runs without errors
- [ ] Code runs without warnings (or warnings are explained)
- [ ] Output matches what's shown in book text
- [ ] Code tested on all relevant platforms (if multi-platform book)
- [ ] Edge cases tested
- [ ] Performance characteristics verified (if performance-sensitive)

## Text Accuracy

- [ ] Version references updated throughout (Python 3.12, not 3.9)
- [ ] Explanations revised for any behavior changes
- [ ] Best practices updated to reflect current standards
- [ ] Security guidance current for target version
- [ ] Performance notes updated if characteristics changed
- [ ] Feature availability notes accurate (when features were introduced)

## Migration Notes

- [ ] Migration notes added if changes are significant
- [ ] Breaking changes documented
- [ ] Migration tips provided for readers with old code
- [ ] Links to official migration guides included (if helpful)
- [ ] Backward compatibility notes where relevant

## Cross-References

- [ ] All "see Chapter X" references still accurate
- [ ] Section number references verified
- [ ] Forward references still correct
- [ ] Backward references still correct
- [ ] Page number references updated (if present)
- [ ] Index entries reflect version changes

## Version-Specific Content

- [ ] Version-specific features clearly noted
- [ ] Minimum version requirements stated
- [ ] Version compatibility ranges specified where needed
- [ ] Deprecated features marked clearly
- [ ] Future deprecation warnings included where known

## Consistency

- [ ] Updated code follows extracted code patterns
- [ ] Voice and tone consistent with existing content
- [ ] Terminology consistent throughout chapter
- [ ] Formatting matches book standards
- [ ] Comment styles match existing examples

## Documentation

- [ ] Chapter change log updated with version update details
- [ ] Testing notes documented (which version(s) tested)
- [ ] Major changes summarized for readers
- [ ] Date of update recorded
- [ ] Reviewer name documented

## Examples of Good Version Updates

**✅ Good Update:**
```python
# Python 3.12 - Modern Type Hints
def process_items(items: list[str]) -> dict[str, int]:
    """Process items and return counts (Python 3.9+)."""
    return {item: items.count(item) for item in set(items)}
```
- Uses modern syntax
- Documents minimum version
- Clear and concise

**❌ Bad Update:**
```python
# Just changed version number but code uses old syntax
def process_items(items: List[str]) -> Dict[str, int]:
    # Still importing from typing (old way)
    return {item: items.count(item) for item in set(items)}
```
- Inconsistent (claims new version but uses old syntax)
- Missed opportunity to demonstrate new features

## Red Flags

- Version number changed in text but code unchanged
- Code uses deprecated features without migration plan
- No testing on actual target version
- Breaking changes ignored
- Cross-references broken by chapter renumbering
- Inconsistent version references (some old, some new)
