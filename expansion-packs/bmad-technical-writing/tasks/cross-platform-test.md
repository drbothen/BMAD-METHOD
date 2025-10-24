<!-- Powered by BMAD™ Core -->

# Cross-Platform Test

---

task:
id: cross-platform-test
name: Cross-Platform Test
description: Test code examples across multiple platforms to ensure cross-platform compatibility
persona_default: code-curator
inputs: - code_path - target_platforms - language
steps: - Identify target platforms and code to test - Review cross-platform-checklist.md for platform-specific concerns - Set up testing environments (Windows, macOS, Linux) - Test code on each platform - Document platform-specific behaviors - Identify compatibility issues - Provide platform-specific fixes or workarounds - Generate cross-platform compatibility report
output: docs/testing/cross-platform-report.md

---

## Purpose

This task guides you through testing code examples across Windows, macOS, and Linux to ensure they work correctly on all target platforms. Technical books often have readers on different operating systems, so cross-platform compatibility is essential for reader success.

## Prerequisites

Before starting this task:

- Code examples have been created and work on at least one platform
- Target platforms identified (Windows, macOS, Linux, or specific versions)
- Access to testing environments for each platform
- Access to cross-platform-checklist.md
- Understanding of common cross-platform issues

## Workflow Steps

### 1. Identify Target Platforms and Scope

Define testing scope:

**Platform Selection:**

Choose based on target audience:

- **Windows**: Windows 10, Windows 11
- **macOS**: Latest 2-3 versions (e.g., Sonoma, Ventura)
- **Linux**: Ubuntu 22.04 LTS, Debian, Fedora, or relevant distros

**Code Inventory:**

- List all code files to test
- Identify platform-sensitive code (file I/O, paths, shell commands)
- Note system-level operations
- Flag code with OS-specific APIs
- Identify GUI or terminal applications

**Priority Assessment:**

- **High priority**: Code with file paths, shell commands, environment variables
- **Medium priority**: Code with networking, process management
- **Low priority**: Pure logic, calculations (still test to verify)

### 2. Review Cross-Platform Concerns

Use cross-platform-checklist.md to identify potential issues:

**File Path Issues:**

- [ ] Path separators (/ vs \)
- [ ] Drive letters (C:\ on Windows)
- [ ] Case sensitivity differences
- [ ] Path length limits
- [ ] Special characters in filenames
- [ ] Home directory references

**Line Ending Issues:**

- [ ] LF (Unix/Mac) vs CRLF (Windows)
- [ ] File reading/writing modes
- [ ] Git line ending handling
- [ ] Text vs binary mode

**Environment Variables:**

- [ ] Setting environment variables differs
- [ ] Variable name casing (case-sensitive on Unix)
- [ ] Path separators in PATH variable
- [ ] Default environment variables differ

**Shell Commands:**

- [ ] bash (Unix/Mac) vs cmd/PowerShell (Windows)
- [ ] Command availability differences
- [ ] Command syntax differences
- [ ] Path to executables

**Platform Detection:**

- [ ] Code needs to detect platform
- [ ] Platform-specific code branches
- [ ] Graceful fallbacks

### 3. Set Up Testing Environments

Create testing environments for each platform:

#### Option A: Physical/Virtual Machines

**Windows Testing:**

```bash
# Use Windows 10/11 machine or VM
# Install required runtimes
# - Python: python.org installer
# - Node.js: nodejs.org installer
# - Ruby: RubyInstaller
# - Go: golang.org installer
```

**macOS Testing:**

```bash
# Use Mac machine or VM (requires Apple hardware)
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install runtimes via Homebrew
brew install python node ruby go
```

**Linux Testing:**

```bash
# Use Ubuntu 22.04 LTS (most common)
# Update system
sudo apt update && sudo apt upgrade

# Install runtimes
sudo apt install python3 python3-pip nodejs npm ruby golang
```

#### Option B: Docker Containers (Recommended)

Create Dockerfiles for each platform:

**Windows Container (using Wine or Windows Server Core):**

```dockerfile
FROM mcr.microsoft.com/windows/servercore:ltsc2022
# Install required runtimes
# Note: Windows containers require Windows host
```

**Linux Container:**

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    nodejs npm \
    ruby \
    golang \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
```

**macOS Testing:**

- Docker Desktop on Mac tests Linux behavior
- Use physical Mac or CI/CD for true macOS testing

#### Option C: CI/CD Matrix Testing (Best for automation)

**GitHub Actions Example:**

```yaml
name: Cross-Platform Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        language-version: ['3.11', '3.12']

    steps:
      - uses: actions/checkout@v3
      - name: Set up language
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.language-version }}
      - name: Run tests
        run: python test_examples.py
```

### 4. Test Code on Each Platform

For each platform, systematically test all code:

#### Testing Checklist Per Platform

**Pre-Test Setup:**

- [ ] Fresh environment (clean install or new container)
- [ ] Document exact OS version
- [ ] Document runtime version
- [ ] Install only documented dependencies
- [ ] Note installation commands used

**Test Execution:**

**Step 1: Dependency Installation**

```bash
# Test that installation commands work
# Windows (PowerShell)
PS> pip install -r requirements.txt

# macOS/Linux
$ pip3 install -r requirements.txt

# Document any platform-specific installation issues
```

**Step 2: Run Code Examples**

```bash
# Execute each code example exactly as documented
# Windows
PS> python example.py

# macOS/Linux
$ python3 example.py

# Capture full output
```

**Step 3: Verify Output**

- Compare output across platforms
- Check for differences in formatting
- Verify functionality works correctly
- Note any platform-specific output

**Step 4: Test Edge Cases**

- Test with paths containing spaces
- Test with special characters
- Test with long paths
- Test with non-ASCII characters (Unicode)
- Test with symlinks (on platforms that support them)

**Step 5: Document Results**

Use this format:

```markdown
## Test Results: [Platform Name]

**Platform Details:**

- OS: Windows 11 / macOS 14 Sonoma / Ubuntu 22.04
- Runtime: Python 3.11.5
- Date: YYYY-MM-DD

**Example: example.py**

- Status: ✅ PASS / ⚠️ WARNING / ❌ FAIL
- Output matches documentation: Yes/No
- Platform-specific notes: [Any differences]
- Issues found: [List any issues]
```

### 5. Identify Platform-Specific Issues

Common cross-platform issues to watch for:

#### Path-Related Issues

**Issue: Hardcoded path separators**

```python
# ❌ Fails on Windows
file_path = "data/files/example.txt"  # Uses /

# ✅ Cross-platform
from pathlib import Path
file_path = Path("data") / "files" / "example.txt"
```

**Issue: Absolute paths**

```python
# ❌ Unix-only
file_path = "/home/user/data.txt"

# ❌ Windows-only
file_path = "C:\\Users\\user\\data.txt"

# ✅ Cross-platform
from pathlib import Path
file_path = Path.home() / "data.txt"
```

#### Line Ending Issues

**Issue: File writing without newline parameter**

```python
# ❌ Platform-dependent line endings
with open("file.txt", "w") as f:
    f.write("line1\n")

# ✅ Explicit line ending handling
with open("file.txt", "w", newline="\n") as f:
    f.write("line1\n")
```

#### Shell Command Issues

**Issue: Platform-specific commands**

```python
# ❌ Unix-only
import subprocess
subprocess.run(["ls", "-la"])

# ✅ Cross-platform using Python
import os
for item in os.listdir("."):
    print(item)

# Or provide platform-specific alternatives
import platform
if platform.system() == "Windows":
    subprocess.run(["dir"], shell=True)
else:
    subprocess.run(["ls", "-la"])
```

#### Environment Variable Issues

**Issue: Setting environment variables**

```bash
# ❌ Unix-only syntax in documentation
export API_KEY="secret"

# ✅ Document both
# Unix/macOS:
export API_KEY="secret"

# Windows (PowerShell):
$env:API_KEY="secret"

# Windows (cmd):
set API_KEY=secret
```

#### Unicode and Encoding Issues

**Issue: Platform default encodings differ**

```python
# ❌ Uses platform default encoding
with open("file.txt", "r") as f:
    content = f.read()

# ✅ Explicit encoding
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### 6. Document Platform-Specific Behaviors

Note legitimate platform differences:

**Expected Differences:**

- Performance variations
- File system operation speeds
- Default installed tools
- System paths and locations
- Available system resources

**Unexpected Differences (require fixing):**

- Code works on one platform, fails on another
- Different outputs for same input
- Missing functionality on a platform
- Crashes or errors

### 7. Provide Fixes and Workarounds

For each incompatibility found:

**Fix Documentation Template:**

````markdown
### Platform Incompatibility: [Issue Title]

**Affected Platforms:** Windows / macOS / Linux

**Issue:**
[Describe what doesn't work]

**Root Cause:**
[Explain why the issue occurs]

**Fix Option 1: Cross-Platform Code**

```python
# Recommended fix that works on all platforms
```
````

**Fix Option 2: Platform-Specific Code**

```python
import platform
if platform.system() == "Windows":
    # Windows-specific code
elif platform.system() == "Darwin":  # macOS
    # macOS-specific code
else:  # Linux and others
    # Unix-like code
```

**Fix Option 3: Update Documentation**
[If code is correct but docs need platform-specific instructions]

**Testing:**

- [x] Tested on Windows
- [x] Tested on macOS
- [x] Tested on Linux

````

### 8. Run Cross-Platform Checklist

Execute execute-checklist.md task with cross-platform-checklist.md:

- Systematically verify each checklist item
- Document any issues found
- Ensure comprehensive coverage
- Update checklist if new issues discovered

### 9. Generate Cross-Platform Compatibility Report

Create comprehensive report:

**Report Structure:**

```markdown
# Cross-Platform Compatibility Report

**Date:** YYYY-MM-DD
**Tester:** [Name]
**Code Version:** [Commit hash or version]
**Languages:** [JavaScript, Python, etc.]

## Executive Summary

- Total code examples tested: X
- Platforms tested: Windows 11, macOS 14, Ubuntu 22.04
- Pass rate: X% (Y examples work on all platforms)
- Issues found: X
- Critical issues: X (code fails on platform)
- Minor issues: X (works but with differences)

## Testing Scope

**Target Platforms:**
- Windows 11 (Version XX)
- macOS 14 Sonoma
- Ubuntu 22.04 LTS

**Code Examples Tested:**
1. example1.py
2. example2.js
3. ...

**Testing Method:**
- [ ] Physical machines
- [ ] Virtual machines
- [ ] Docker containers
- [ ] CI/CD pipeline

## Platform Test Results

### Windows 11

**Environment:**
- OS Version: Windows 11 Pro 22H2
- Python: 3.11.5
- Node.js: 18.17.0

**Results:**
| Example | Status | Notes |
|---------|--------|-------|
| example1.py | ✅ PASS | |
| example2.py | ❌ FAIL | Path separator issue |
| example3.js | ⚠️ WARNING | Works but shows warning |

**Issues Found:**
1. [Issue description and fix]

### macOS 14 Sonoma

**Environment:**
- OS Version: macOS 14.0
- Python: 3.11.5
- Node.js: 18.17.0

**Results:**
| Example | Status | Notes |
|---------|--------|-------|
| example1.py | ✅ PASS | |
| example2.py | ✅ PASS | |
| example3.js | ✅ PASS | |

**Issues Found:**
None

### Ubuntu 22.04 LTS

**Environment:**
- OS Version: Ubuntu 22.04.3 LTS
- Python: 3.11.5
- Node.js: 18.17.0

**Results:**
| Example | Status | Notes |
|---------|--------|-------|
| example1.py | ✅ PASS | |
| example2.py | ✅ PASS | |
| example3.js | ✅ PASS | |

**Issues Found:**
None

## Detailed Findings

### Critical Issues

**[Issue 1: Path Separator Hardcoding]**
- **Severity:** Critical
- **Affected:** example2.py
- **Platforms:** Windows only
- **Description:** Code uses forward slashes, fails on Windows
- **Fix:** Use pathlib.Path
- **Status:** Fixed

### Minor Issues

**[Issue 2: Performance Difference]**
- **Severity:** Minor
- **Affected:** example5.py
- **Platforms:** All (varies)
- **Description:** Execution time varies by platform
- **Fix:** None needed (expected behavior)
- **Status:** Documented

## Platform-Specific Installation Notes

### Windows
```powershell
# Special installation notes for Windows
pip install -r requirements.txt
````

### macOS

```bash
# Special installation notes for macOS
brew install xyz
pip3 install -r requirements.txt
```

### Linux

```bash
# Special installation notes for Linux
sudo apt-get install xyz
pip3 install -r requirements.txt
```

## Cross-Platform Best Practices Applied

- [x] Using pathlib for file paths
- [x] Explicit encoding specified (UTF-8)
- [x] Platform-specific code properly branched
- [x] Environment variable instructions for all platforms
- [x] No hardcoded paths
- [x] No shell-specific commands (or alternatives provided)

## Recommendations

1. **Immediate fixes:** [List critical issues to fix]
2. **Documentation updates:** [Platform-specific instructions to add]
3. **Future testing:** [Set up CI/CD for automated testing]
4. **Reader guidance:** [Add platform-specific troubleshooting section]

## Checklist Results

[Reference to cross-platform-checklist.md completion]

## Sign-off

- [ ] All critical issues resolved
- [ ] Code works on all target platforms
- [ ] Platform-specific documentation complete
- [ ] Cross-platform testing complete

**Tester Signature:** ******\_******
**Date:** ******\_******

```

### 10. Troubleshooting Common Issues

**Cannot Access Platform:**
- Use cloud-based testing services (BrowserStack, LambdaTest)
- Use GitHub Actions or similar CI/CD
- Use Docker for Linux testing
- Ask beta readers to test on their platforms

**Dependency Installation Fails:**
- Document platform-specific dependencies
- Provide alternative packages if available
- Use virtual environments to isolate
- Document exact error messages and solutions

**Intermittent Failures:**
- May be race conditions or timing issues
- Test multiple times
- Check for platform-specific timing differences
- Add appropriate delays if needed

**Permission Issues:**
- Linux/macOS: May need sudo for some operations
- Windows: May need Administrator
- Document privilege requirements clearly
- Avoid requiring elevated privileges if possible

**Path Too Long (Windows):**
- Windows has 260-character path limit (unless modified)
- Use shorter paths in examples
- Document workaround (enable long paths in Windows)
- Test with realistic path lengths

**File Locking Differences:**
- Windows locks files more aggressively
- Ensure files closed properly
- Use context managers (with statement)
- Test file operations thoroughly on Windows

## Success Criteria

A complete cross-platform test has:

- [ ] All target platforms tested
- [ ] Testing environments documented
- [ ] Every code example tested on every platform
- [ ] Platform-specific behaviors documented
- [ ] Incompatibilities identified and fixed
- [ ] cross-platform-checklist.md completed
- [ ] Installation instructions verified on all platforms
- [ ] Cross-platform compatibility report generated
- [ ] All critical issues resolved
- [ ] Code works correctly on all target platforms

## Common Pitfalls to Avoid

- **Testing only on your primary platform**: Test on ALL targets
- **Using platform-specific features without checking**: Always verify
- **Hardcoding paths**: Use path manipulation libraries
- **Assuming case sensitivity**: Windows is case-insensitive, Unix is not
- **Not documenting platform differences**: Readers need to know
- **Using shell commands without alternatives**: Provide cross-platform options
- **Ignoring line endings**: Can cause subtle bugs
- **Not testing installation**: Installation often fails first
- **Skipping edge cases**: Test special characters, spaces, etc.
- **No CI/CD automation**: Manual testing is error-prone

## Cross-Platform Testing Tools

**Multi-Platform CI/CD:**
- GitHub Actions (Windows, macOS, Linux)
- GitLab CI (Windows, macOS, Linux)
- CircleCI (Windows, macOS, Linux)
- Azure Pipelines (Windows, macOS, Linux)

**Containerization:**
- Docker (Linux containers, Windows containers)
- Podman (alternative to Docker)
- LXC/LXD (Linux containers)

**Virtualization:**
- VirtualBox (free, all platforms)
- VMware (Windows, Linux)
- Parallels (macOS)
- QEMU (all platforms)

**Cloud Testing:**
- AWS EC2 (Windows, Linux)
- Azure VMs (Windows, Linux)
- Google Cloud (Windows, Linux)

**Language-Specific Tools:**

*Python:*
- tox (multi-environment testing)
- nox (flexible testing)

*Node.js:*
- nvm (version management)
- package.json scripts (cross-platform)

*Ruby:*
- rbenv (version management)
- bundler (dependency management)

## Next Steps

After cross-platform testing is complete:

1. **Fix all incompatibilities**: Ensure code works on all platforms
2. **Update documentation**: Add platform-specific instructions
3. **Create troubleshooting guide**: Document common issues
4. **Set up CI/CD**: Automate future testing
5. **Add platform badges**: Show supported platforms in README
6. **Test on version updates**: Retest when OS versions update
7. **Gather reader feedback**: Beta readers often find edge cases
8. **Document known limitations**: If platform can't be supported

## Platform-Specific Resources

**Windows Development:**
- Windows Subsystem for Linux (WSL)
- PowerShell documentation
- Windows Terminal
- Chocolatey package manager

**macOS Development:**
- Homebrew package manager
- Xcode command-line tools
- macOS developer documentation

**Linux Development:**
- Distribution-specific package managers (apt, yum, dnf)
- Linux Foundation documentation
- Distribution release notes
```
