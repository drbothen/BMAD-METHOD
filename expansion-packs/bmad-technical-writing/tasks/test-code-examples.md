<!-- Powered by BMAD™ Core -->

# Test Code Examples

---

task:
id: test-{{config.codeExamples.root}}
name: Test Code Examples
description: Run automated tests on all code examples in chapter or book
persona_default: code-curator
inputs:

- chapter-number (or "all" for entire book)
- target-versions
  steps:
- Identify all code examples in specified scope
- Set up testing environment with target versions
- For each code example, run the code
- Verify output matches documentation
- Test on specified platforms (Windows/Mac/Linux if applicable)
- Check edge cases and error handling
- Document any version-specific behaviors
- Update code-testing-checklist.md as you test
- Fix any failing examples
- Document testing results
  output: docs/testing/code-test-results.md

---

## Purpose

This task ensures all code examples work correctly across specified versions and platforms. Technical books lose credibility if code doesn't work, so thorough testing is critical.

## Prerequisites

Before starting this task:

- Code examples have been created
- Target versions identified (e.g., Python 3.11-3.12, Node 18-20)
- Access to testing environments for target versions
- code-testing-checklist.md available

## Workflow Steps

### 0. Load Configuration

- Read `.bmad-technical-writing/config.yaml` to resolve directory paths
- Extract: `config.codeExamples.root`
- If config not found, use default: `code-examples`

### 1. Identify Code Examples

Collect all code examples in scope:

**For Single Chapter:**

- List all code files in chapter's code folder
- Identify inline code snippets that should be tested
- Note any setup dependencies between examples

**For Entire Book:**

- Scan all chapter folders
- Create comprehensive list of examples
- Group by language/framework
- Identify shared dependencies

### 2. Set Up Testing Environment

Prepare testing infrastructure:

**Environment Requirements:**

- [ ] Target language versions installed (e.g., Python 3.11, 3.12, 3.13)
- [ ] Package managers available (pip, npm, maven, etc.)
- [ ] Virtual environments or containers ready
- [ ] Required platforms (Windows/Mac/Linux) if multi-platform
- [ ] CI/CD pipeline configured (optional but recommended)

**Environment Setup Example (Python):**

```bash
# Create test environment for Python 3.11
pyenv install 3.11.5
pyenv virtualenv 3.11.5 book-test-3.11

# Create test environment for Python 3.12
pyenv install 3.12.0
pyenv virtualenv 3.12.0 book-test-3.12
```

### 3. Test Each Example

For every code example:

**Step 1: Fresh Environment**

- Start with clean environment
- Install only documented dependencies
- Use exact versions from requirements

**Step 2: Run Code**

- Execute code exactly as documented
- Capture output
- Note execution time
- Watch for warnings

**Step 3: Verify Output**

- Compare output to documentation
- Check for expected results
- Verify error messages (if testing error cases)
- Ensure no unexpected warnings

**Step 4: Test Edge Cases**

- Empty inputs
- Boundary values
- Invalid inputs
- Error conditions
- Large datasets (if applicable)

**Step 5: Document Results**

- ✅ PASS: Works as documented
- ⚠️ WARNING: Works but with warnings
- ❌ FAIL: Does not work as documented
- 📝 NOTE: Version-specific behavior

### 4. Platform Testing

If book targets multiple platforms:

**Test on Each Platform:**

- Windows (PowerShell and CMD if relevant)
- macOS (latest 2 versions)
- Linux (Ubuntu/Debian typical)

**Platform-Specific Issues:**

- Path separators (/ vs \)
- Line endings (LF vs CRLF)
- Case sensitivity
- Default encodings
- Command syntax

### 5. Version Compatibility Testing

Test across supported versions:

**For Each Target Version:**

- Run full test suite
- Document version-specific behaviors
- Note deprecated features
- Identify breaking changes
- Update version compatibility matrix

**Version Matrix Example:**

| Example          | Python 3.11 | Python 3.12 | Python 3.13 |
| ---------------- | ----------- | ----------- | ----------- |
| basic-server.py  | ✅ PASS     | ✅ PASS     | ✅ PASS     |
| async-handler.py | ✅ PASS     | ✅ PASS     | ⚠️ WARNING  |
| type-hints.py    | ✅ PASS     | ✅ PASS     | ✅ PASS     |

### 6. Handle Test Failures

When code fails:

**Step 1: Diagnose**

- What is the error message?
- Is it environment-related or code-related?
- Does it fail on all versions/platforms?
- Is documentation incorrect?

**Step 2: Fix**

- Update code if bug found
- Update documentation if instructions wrong
- Add troubleshooting section if common issue
- Update requirements if dependency changed

**Step 3: Retest**

- Verify fix works
- Test on all affected versions/platforms
- Update test results

### 7. Update Code-Testing Checklist

As you test, mark items on code-testing-checklist.md:

- [ ] Every example tested
- [ ] Runs on specified versions
- [ ] Output matches documentation
- [ ] Edge cases considered
- [ ] Error cases demonstrated
- [ ] Testing instructions provided
- [ ] Platform-specific issues documented

### 8. Document Testing Results

Create comprehensive test report:

**Report Structure:**

1. **Summary**: Total examples, pass/fail/warning counts
2. **Environment**: Versions tested, platforms, date
3. **Results**: Detailed results for each example
4. **Issues Found**: List of problems and fixes
5. **Recommendations**: Suggested improvements
6. **Version Notes**: Version-specific behaviors

### 9. Fix Failing Examples

For each failure:

1. Document the issue
2. Fix code or documentation
3. Retest to confirm fix
4. Update code repository
5. Note fix in change log

### 10. Continuous Testing

Set up automated testing (optional):

- Create CI/CD pipeline (GitHub Actions, GitLab CI, etc.)
- Run tests on every commit
- Test across version matrix
- Generate test reports automatically

## Success Criteria

Testing is complete when:

- [ ] All code examples identified
- [ ] Testing environment set up for all target versions
- [ ] Every example tested successfully
- [ ] Output verified against documentation
- [ ] Edge cases tested
- [ ] Platform-specific testing done (if applicable)
- [ ] Version compatibility matrix created
- [ ] All failures fixed and retested
- [ ] code-testing-checklist.md completed
- [ ] Test results documented

## Common Pitfalls to Avoid

- **Testing in wrong environment**: Use clean environments
- **Skipping versions**: Test ALL supported versions
- **Ignoring warnings**: Warnings can become errors
- **No edge case testing**: Test boundary conditions
- **Missing dependencies**: Document ALL requirements
- **Platform assumptions**: Test on all target platforms
- **Stale documentation**: Update docs when code changes
- **No automation**: Manual testing is error-prone and slow

## Testing Tools by Language

**Python:**

- pytest (unit testing)
- tox (multi-version testing)
- coverage.py (code coverage)

**JavaScript/Node:**

- Jest (testing framework)
- nvm (version management)
- npm test (standard test runner)

**Java:**

- JUnit (testing framework)
- Maven/Gradle (build and test)
- jenv (version management)

## Next Steps

After testing is complete:

1. Fix any failing examples
2. Update documentation with any clarifications
3. Add troubleshooting sections where needed
4. Set up CI/CD for continuous testing
5. Retest before each book edition
6. Test again when new language versions released
