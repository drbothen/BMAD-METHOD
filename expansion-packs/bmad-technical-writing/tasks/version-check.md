<!-- Powered by BMAD™ Core -->

# Version Check

---

task:
id: version-check
name: Version Check
description: Verify code compatibility across multiple language versions with automated testing
persona_default: code-curator
inputs: - code_path (file or directory to test) - language (javascript|python|ruby|java|go) - version_matrix (e.g., "Node 16,18,20" or "Python 3.9,3.10,3.11")
steps: - Parse target versions from version_matrix input - Set up testing environments for each version (Docker or version managers) - Execute code on each version - Capture output, errors, and warnings - Compare results across versions - Identify version-specific issues (deprecated APIs, syntax changes, breaking changes) - Generate compatibility matrix report - Run execute-checklist.md with version-compatibility-checklist.md - Document recommendations for version support
output: docs/testing/version-compatibility-report.md

---

## Purpose

This task ensures code examples work correctly across multiple versions of programming languages and runtimes. Version compatibility is critical for technical books because readers use different environments. A thorough version check catches breaking changes, deprecated APIs, and version-specific behaviors before readers encounter them.

## Prerequisites

Before starting this task:

- Code examples have been created and are ready to test
- Target versions identified (e.g., Node 16/18/20, Python 3.9/3.10/3.11)
- Docker installed for isolated testing environments (recommended)
- OR version managers installed (nvm, pyenv, rbenv, SDKMAN, etc.)
- version-compatibility-checklist.md available
- Basic understanding of the language being tested

## Workflow Steps

### 1. Parse Version Matrix

Extract target versions from input:

**Input Format Examples:**

- JavaScript: `"Node 16.20.0, 18.16.0, 20.2.0"` or `"Node 16,18,20"` (latest minor)
- Python: `"Python 3.9, 3.10, 3.11"` or `"Python 3.9.18, 3.10.13, 3.11.5"`
- Ruby: `"Ruby 2.7, 3.0, 3.1"`
- Java: `"OpenJDK 11, 17, 21"`
- Go: `"Go 1.19, 1.20, 1.21"`

**Parsing Steps:**

1. Split version string by commas
2. Trim whitespace
3. Validate version format
4. Determine if full version (3.9.18) or major.minor (3.9)
5. For major.minor, use latest patch version available

### 2. Set Up Testing Environments

Choose testing approach based on requirements:

#### Option A: Docker-Based Testing (Recommended)

**Benefits:**

- Clean, isolated environments
- No system pollution
- Reproducible across machines
- Easy CI/CD integration
- Platform independence

**JavaScript/Node Example:**

```bash
# Test Node 16
docker run --rm -v $(pwd):/app -w /app node:16 node example.js

# Test Node 18
docker run --rm -v $(pwd):/app -w /app node:18 node example.js

# Test Node 20
docker run --rm -v $(pwd):/app -w /app node:20 node example.js
```

**Python Example:**

```bash
# Test Python 3.9
docker run --rm -v $(pwd):/app -w /app python:3.9 python example.py

# Test Python 3.10
docker run --rm -v $(pwd):/app -w /app python:3.10 python example.py

# Test Python 3.11
docker run --rm -v $(pwd):/app -w /app python:3.11 python example.py
```

#### Option B: Version Managers

**JavaScript/Node: nvm**

```bash
# Install versions
nvm install 16
nvm install 18
nvm install 20

# Test each version
nvm use 16 && node example.js
nvm use 18 && node example.js
nvm use 20 && node example.js
```

**Python: pyenv**

```bash
# Install versions
pyenv install 3.9.18
pyenv install 3.10.13
pyenv install 3.11.5

# Test each version
pyenv shell 3.9.18 && python example.py
pyenv shell 3.10.13 && python example.py
pyenv shell 3.11.5 && python example.py
```

**Ruby: rbenv**

```bash
# Install versions
rbenv install 2.7.8
rbenv install 3.0.6
rbenv install 3.1.4

# Test each version
rbenv shell 2.7.8 && ruby example.rb
rbenv shell 3.0.6 && ruby example.rb
rbenv shell 3.1.4 && ruby example.rb
```

**Java: SDKMAN**

```bash
# Install versions
sdk install java 11.0.20-tem
sdk install java 17.0.8-tem
sdk install java 21.0.0-tem

# Test each version
sdk use java 11.0.20-tem && java Example.java
sdk use java 17.0.8-tem && java Example.java
sdk use java 21.0.0-tem && java Example.java
```

**Go: Direct Docker (Go doesn't need system-wide version manager)**

```bash
docker run --rm -v $(pwd):/app -w /app golang:1.19 go run example.go
docker run --rm -v $(pwd):/app -w /app golang:1.20 go run example.go
docker run --rm -v $(pwd):/app -w /app golang:1.21 go run example.go
```

### 3. Execute Code on Each Version

For every version in the matrix:

**Step 1: Install Dependencies**

```bash
# JavaScript/Node
npm install

# Python
pip install -r requirements.txt

# Ruby
bundle install

# Java
mvn install

# Go
go mod download
```

**Step 2: Run Code**

Execute the code exactly as documented:

```bash
# Capture stdout, stderr, and exit code
<command> > output.txt 2> error.txt
echo $? > exitcode.txt
```

**Step 3: Record Results**

Capture:

- Exit code (0 = success, non-zero = failure)
- Standard output
- Standard error (including warnings)
- Execution time
- Any deprecation warnings

### 4. Compare Results Across Versions

Analyze differences between versions:

**Comparison Checklist:**

- [ ] **Exit codes**: Do all versions succeed (exit 0)?
- [ ] **Output**: Is output identical across versions?
- [ ] **Warnings**: Are there deprecation warnings in some versions?
- [ ] **Errors**: Do any versions produce errors?
- [ ] **Performance**: Are there significant speed differences?
- [ ] **Features**: Are any features unavailable in older versions?

**Common Version Issues:**

1. **New Features**: Feature added in newer version (e.g., Fetch API in Node 18+)
2. **Deprecated Features**: Feature works but shows deprecation warning
3. **Breaking Changes**: API changed between versions
4. **Syntax Changes**: Language syntax evolved (e.g., Python 3.10 match-case)
5. **Performance**: Algorithm or runtime improvements in newer versions
6. **Bug Fixes**: Bug present in older version, fixed in newer

### 5. Identify Version-Specific Issues

For each incompatibility found:

**Document:**

1. **Which versions are affected?** (e.g., "Node 16 only", "Python 3.9 and below")
2. **What is the symptom?** (error message, warning, different output)
3. **What is the cause?** (API change, new feature, deprecation)
4. **What is the impact?** (code doesn't run, works with warning, different behavior)
5. **What is the solution?** (upgrade requirement, polyfill, conditional code, separate examples)

**Example Issue Documentation:**

```markdown
### Issue: Fetch API Not Available in Node 16

**Affected Versions:** Node 16.x
**Working Versions:** Node 18+, Node 20+

**Symptom:**
```

ReferenceError: fetch is not defined

```

**Cause:** The global `fetch()` API was added in Node 18.0.0. Node 16 requires a polyfill like `node-fetch`.

**Impact:** Code example using `fetch()` will fail on Node 16.

**Solutions:**
1. **Option A**: Require Node 18+ (recommended for new books)
2. **Option B**: Use `node-fetch` polyfill for Node 16 support
3. **Option C**: Provide separate examples for Node 16 and Node 18+

**Recommendation:** Update book requirements to Node 18+ LTS.
```

### 6. Generate Compatibility Matrix

Create visual compatibility report:

**Compatibility Matrix Template:**

```markdown
## Version Compatibility Report

**Code Path:** `examples/chapter-03/`
**Languages Tested:** JavaScript (Node.js)
**Versions Tested:** Node 16.20.0, 18.16.0, 20.2.0
**Test Date:** 2024-10-24
**Tester:** code-curator agent

### Summary

| Metric                | Value   |
| --------------------- | ------- |
| Total Examples        | 12      |
| Fully Compatible      | 8 (67%) |
| Partial Compatibility | 3 (25%) |
| Incompatible          | 1 (8%)  |

### Detailed Results

| Example                | Node 16    | Node 18    | Node 20 | Notes                                |
| ---------------------- | ---------- | ---------- | ------- | ------------------------------------ |
| `hello-world.js`       | ✅ PASS    | ✅ PASS    | ✅ PASS | Fully compatible                     |
| `async-await.js`       | ✅ PASS    | ✅ PASS    | ✅ PASS | Fully compatible                     |
| `fetch-api.js`         | ❌ FAIL    | ✅ PASS    | ✅ PASS | Requires Node 18+                    |
| `top-level-await.js`   | ⚠️ PARTIAL | ✅ PASS    | ✅ PASS | Needs --experimental flag in Node 16 |
| `import-assertions.js` | ⚠️ PARTIAL | ⚠️ PARTIAL | ✅ PASS | Stabilized in Node 20                |
| `crypto-webcrypto.js`  | ✅ PASS    | ✅ PASS    | ✅ PASS | Available all versions               |

### Legend

- ✅ **PASS**: Works without modification or warnings
- ⚠️ **PARTIAL**: Works with modifications or shows warnings
- ❌ **FAIL**: Does not work on this version

### Version-Specific Issues

#### Issue 1: Fetch API Unavailable (Node 16)

- **Affected Examples:** `fetch-api.js`, `http-client.js`
- **Impact:** 2 examples fail on Node 16
- **Recommendation:** Require Node 18+ or provide polyfill

#### Issue 2: Top-Level Await Requires Flag (Node 16)

- **Affected Examples:** `top-level-await.js`
- **Impact:** Works with `--experimental-top-level-await` flag
- **Recommendation:** Add note about flag requirement for Node 16 users

### Recommendations

1. **Minimum Version**: Set Node 18 as minimum requirement
2. **Update Documentation**: Add version compatibility table to README
3. **Code Changes**: Update `fetch-api.js` to check for fetch availability
4. **Reader Guidance**: Add troubleshooting section for version issues
```

### 7. Run Version-Compatibility Checklist

Execute checklist validation:

```bash
# Using execute-checklist.md task
execute-checklist version-compatibility-checklist.md
```

Ensure:

- [ ] All target versions tested
- [ ] Compatibility matrix created
- [ ] Version-specific issues documented
- [ ] Recommendations provided
- [ ] Minimum version requirement clear
- [ ] Troubleshooting guidance included

### 8. Document Recommendations

Provide actionable next steps:

**For Book Requirements:**

- Should minimum version be raised?
- Should polyfills be added?
- Should version-specific examples be created?

**For Code Updates:**

- Which examples need fixes?
- Which need version checks?
- Which need alternative implementations?

**For Documentation:**

- What version notes should be added?
- What troubleshooting guidance is needed?
- What should the version support policy state?

## Success Criteria

Version check is complete when:

- [ ] All versions in matrix tested successfully
- [ ] Every code example tested on every version
- [ ] Results captured (output, errors, warnings, exit codes)
- [ ] Differences between versions identified
- [ ] Version-specific issues documented with causes and solutions
- [ ] Compatibility matrix generated and reviewed
- [ ] version-compatibility-checklist.md completed
- [ ] Recommendations provided for version support strategy
- [ ] Testing approach documented for future updates

## Common Pitfalls to Avoid

- **Incomplete testing**: Test ALL versions, not just newest/oldest
- **Ignoring warnings**: Deprecation warnings signal future problems
- **Cached dependencies**: Use clean environments to avoid false positives
- **Platform assumptions**: Docker images may differ from native installations
- **Missing exit codes**: Check exit codes, not just output
- **No automation**: Manual testing is error-prone; automate where possible
- **Undocumented workarounds**: Document all flags, polyfills, or workarounds needed
- **Ignoring performance**: Significant performance differences may affect examples

## Language-Specific Considerations

### JavaScript/Node.js

**Key Version Milestones:**

- Node 16: LTS until 2023-09-11 (end of life)
- Node 18: Current LTS (until 2025-04-30)
- Node 20: Active LTS (until 2026-04-30)

**Common Compatibility Issues:**

- Fetch API (18+)
- Top-level await (16.14+, stabilized in 18)
- Import assertions (17+, stabilized in 20)
- WebCrypto API (15+)
- AbortController (15+)

### Python

**Key Version Milestones:**

- Python 3.9: Security fixes until 2025-10
- Python 3.10: Security fixes until 2026-10
- Python 3.11: Security fixes until 2027-10

**Common Compatibility Issues:**

- Match-case statements (3.10+)
- Union types with `|` (3.10+)
- Exception groups (3.11+)
- tomllib module (3.11+)
- F-string improvements (3.12+)

### Ruby

**Key Version Milestones:**

- Ruby 2.7: End of life (upgrade recommended)
- Ruby 3.0: Pattern matching, other features
- Ruby 3.1: Current stable

**Common Compatibility Issues:**

- Pattern matching (2.7+, improved in 3.0)
- Endless method definitions (3.0+)
- Keyword argument changes (3.0)

### Java

**Key Version Milestones:**

- Java 11: LTS (until 2026)
- Java 17: LTS (until 2029)
- Java 21: Latest LTS (until 2031)

**Common Compatibility Issues:**

- Records (16+)
- Pattern matching for switch (17+)
- Virtual threads (21+)
- String templates (21+)

### Go

**Key Version Policy:** Last 2 major versions supported

**Common Compatibility Issues:**

- Generics (1.18+)
- Workspace mode (1.18+)
- Enhanced fuzzing (1.18+)

## Automation Example

**GitHub Actions Workflow for Multi-Version Testing:**

```yaml
name: Version Compatibility Check

on: [push, pull_request]

jobs:
  test-node:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm install
      - run: npm test

  test-python:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest
```

## Next Steps

After completing version check:

1. Fix incompatible examples or update requirements
2. Add version compatibility table to README
3. Update book/documentation with minimum version requirements
4. Add troubleshooting sections for version-specific issues
5. Set up CI/CD for automated version testing
6. Retest when new language versions are released
7. Review version support policy annually
