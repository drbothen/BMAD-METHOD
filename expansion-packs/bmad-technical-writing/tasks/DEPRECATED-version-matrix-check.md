<!-- Powered by BMAD™ Core -->

# Version Matrix Check

> **⚠️ DEPRECATED**: This task has been superseded by more comprehensive specialized tasks.
>
> **Use instead:**
> - `create-version-matrix.md` - Build comprehensive version compatibility matrix
> - `assess-version-impact.md` - Analyze migration impact between versions
> - `update-dependencies.md` - Update package dependencies with testing
>
> This file is maintained for backward compatibility only and will be removed in a future version.

---

task:
id: version-matrix-check
name: Version Matrix Check (DEPRECATED)
description: Test code examples across multiple versions and platforms for compatibility
persona_default: version-manager
inputs:

- target-versions
- target-platforms
- code-examples-location
  steps:
- Define target versions for testing
- Define target platforms (Windows/macOS/Linux as applicable)
- Set up testing environment for each version
- Run all code examples on version matrix
- Document version-specific behaviors
- Note breaking changes between versions
- Test platform-specific code (file paths, etc.)
- Create version compatibility matrix
- Update documentation with version requirements
- Document version-specific workarounds
- Run execute-checklist.md with version-compatibility-checklist.md
- Run execute-checklist.md with cross-platform-checklist.md
  output: docs/version-compatibility/{{book-name}}-version-matrix.md

---

## Purpose

This task ensures all code examples work correctly across specified versions and platforms. Version compatibility testing prevents reader frustration and builds confidence in your code examples.

## Prerequisites

Before starting this task:

- All code examples completed
- Target versions identified (e.g., Python 3.10, 3.11, 3.12)
- Access to testing environments for each version
- Understanding of platform-specific differences

## Workflow Steps

### 1. Define Target Versions

Specify which versions to support:

**Example Version Targets:**

```yaml
Language: Python
Versions:
  - 3.10 (minimum supported)
  - 3.11 (recommended)
  - 3.12 (latest)

Language: Node.js
Versions:
  - 18.x LTS
  - 20.x LTS
  - 21.x Current
```

**Version Selection Criteria:**

- Currently maintained versions (not EOL)
- Versions readers likely use
- Breaking changes between versions
- LTS (Long Term Support) versions preferred

### 2. Define Target Platforms

Identify platform requirements:

**Platform Matrix:**

```
✅ Windows 10/11
✅ macOS 12+ (Monterey or later)
✅ Linux (Ubuntu 20.04+, Fedora 35+)
```

**Platform-Specific Considerations:**

- File path separators (/ vs \)
- Line endings (LF vs CRLF)
- Case sensitivity (macOS/Linux vs Windows)
- Shell differences (bash vs PowerShell vs cmd)
- Platform-specific APIs

### 3. Set Up Testing Environment

Create isolated environments:

**Python - Using pyenv:**

```bash
# Install multiple Python versions
pyenv install 3.10.12
pyenv install 3.11.5
pyenv install 3.12.0

# Create virtual environments
pyenv virtualenv 3.10.12 book-py310
pyenv virtualenv 3.11.5 book-py311
pyenv virtualenv 3.12.0 book-py312
```

**Node.js - Using nvm:**

```bash
# Install multiple Node versions
nvm install 18
nvm install 20
nvm install 21

# Test on specific version
nvm use 18
npm test
```

**Docker - For cross-platform:**

```dockerfile
# Dockerfile.test-matrix
FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["pytest", "tests/"]
```

### 4. Run All Code Examples

Execute systematic testing:

**Testing Script Example:**

```bash
#!/bin/bash
# test-versions.sh

VERSIONS=("3.10" "3.11" "3.12")

for version in "${VERSIONS[@]}"; do
  echo "Testing on Python $version"
  pyenv local $version
  pip install -r requirements.txt
  pytest tests/ --verbose
  if [ $? -ne 0 ]; then
    echo "❌ Tests failed on Python $version"
  else
    echo "✅ Tests passed on Python $version"
  fi
done
```

**Automated Testing:**

```yaml
# GitHub Actions matrix testing
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
    os: [ubuntu-latest, windows-latest, macos-latest]
```

### 5. Document Version-Specific Behaviors

Note differences between versions:

**Example Documentation:**

````markdown
## Version-Specific Behaviors

### Python 3.10 vs 3.11

**Pattern Matching (3.10+):**

```python
# Works in 3.10+, syntax error in 3.9
match status:
    case 200:
        return "Success"
    case 404:
        return "Not Found"
```
````

**Improved Error Messages (3.11+):**
Python 3.11 provides more detailed traceback information.

### Python 3.11 vs 3.12

**ExceptionGroup (3.11+):**
New exception handling for multiple exceptions.

**Type Hinting Improvements (3.12+):**
Support for generic type aliases using `type` keyword.

````

### 6. Note Breaking Changes

Identify incompatibilities:

**Breaking Change Documentation:**

```markdown
## Breaking Changes

### Python 3.10 → 3.11

- ✅ **Backward Compatible**: All 3.10 code works in 3.11
- ⚠️ **Deprecations**: distutils deprecated, use setuptools

### Python 3.11 → 3.12

- ✅ **Backward Compatible**: All 3.11 code works in 3.12
- ⚠️ **Removed**: wstr removed from Unicode objects (internal change)

### Node.js 18 → 20

- ⚠️ **OpenSSL Update**: Updated to OpenSSL 3.0 (may affect crypto)
- ✅ **New Features**: V8 11.3, improved fetch() support
````

### 7. Test Platform-Specific Code

Verify cross-platform compatibility:

**File Path Handling:**

```python
# ❌ Platform-specific (breaks on Windows)
path = "data/files/example.txt"

# ✅ Cross-platform
from pathlib import Path
path = Path("data") / "files" / "example.txt"
```

**Environment Variables:**

```python
# ❌ Shell-specific
os.system("export API_KEY=secret")  # Unix only

# ✅ Cross-platform
os.environ["API_KEY"] = "secret"
```

**Line Endings:**

```python
# Always specify newline handling
with open("file.txt", "w", newline="\n") as f:
    f.write("text")
```

### 8. Create Version Compatibility Matrix

Build comprehensive matrix:

**Version Compatibility Matrix:**

```markdown
| Feature / Example            | Python 3.10 | Python 3.11 | Python 3.12 |
| ---------------------------- | ----------- | ----------- | ----------- |
| Chapter 1 Examples           | ✅          | ✅          | ✅          |
| Chapter 2 Examples           | ✅          | ✅          | ✅          |
| Chapter 3 (Pattern Matching) | ✅          | ✅          | ✅          |
| Chapter 4 (ExceptionGroup)   | ❌          | ✅          | ✅          |
| Chapter 5 (Type Aliases)     | ❌          | ❌          | ✅          |

| Platform Tests | Windows | macOS | Linux |
| -------------- | ------- | ----- | ----- |
| All Examples   | ✅      | ✅    | ✅    |
| File I/O       | ✅      | ✅    | ✅    |
| Networking     | ✅      | ✅    | ✅    |
| Subprocess     | ⚠️\*    | ✅    | ✅    |

\*Requires PowerShell-specific commands
```

### 9. Update Documentation

Add version requirements:

**Update README.md:**

```markdown
## Version Requirements

### Minimum Requirements

- Python 3.10 or higher

### Recommended

- Python 3.11+ (better error messages, improved performance)

### Version-Specific Chapters

- **Chapter 4**: Requires Python 3.11+ for ExceptionGroup examples
- **Chapter 5**: Requires Python 3.12+ for type alias syntax

### Platform Support

All examples tested on:

- ✅ Windows 10/11
- ✅ macOS 12+
- ✅ Linux (Ubuntu 20.04+)
```

### 10. Document Workarounds

Provide version-specific solutions:

**Workaround Documentation:**

````markdown
## Version-Specific Workarounds

### Using Pattern Matching on Python 3.9

If you must use Python 3.9, replace pattern matching with if/elif:

```python
# Python 3.10+ (preferred)
match status:
    case 200: return "Success"
    case 404: return "Not Found"

# Python 3.9 workaround
if status == 200:
    return "Success"
elif status == 404:
    return "Not Found"
```
````

### ExceptionGroup Backport for Python 3.10

```bash
pip install exceptiongroup  # Backport package
```

```

### 11. Run Quality Checklists

Validate compatibility:

- Run execute-checklist.md with version-compatibility-checklist.md
- Run execute-checklist.md with cross-platform-checklist.md

## Success Criteria

A completed version matrix check should have:

- [ ] Target versions clearly defined
- [ ] Target platforms identified
- [ ] All versions tested in isolated environments
- [ ] All code examples executed on version matrix
- [ ] Version-specific behaviors documented
- [ ] Breaking changes identified and noted
- [ ] Platform-specific code tested
- [ ] Complete compatibility matrix created
- [ ] Version requirements in README updated
- [ ] Workarounds documented for older versions
- [ ] All checklists passed

## Common Pitfalls to Avoid

- **Testing on one version only**: Readers use diverse environments
- **Ignoring platform differences**: File paths, line endings, shell commands
- **No version requirements**: Readers don't know what to install
- **Missing workarounds**: Forcing readers to upgrade unnecessarily
- **Outdated version testing**: Supporting EOL versions
- **No CI/CD for versions**: Manual testing is error-prone

## Next Steps

After completing version matrix check:

1. Update book's system requirements section
2. Add version badges to repository README
3. Set up CI/CD to test all versions automatically
4. Note version requirements in chapter introductions where relevant
5. Provide version-specific code variations where necessary
```
