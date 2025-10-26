<!-- Powered by BMAD™ Core -->

# Troubleshoot Example

---

task:
id: troubleshoot-example
name: Troubleshoot Example
description: Debug code examples and create comprehensive troubleshooting guides for readers
persona_default: code-curator
inputs:

- code_path (file or directory containing code to troubleshoot)
- error_description (error message or problem description)
- language (programming language)
  steps:
- Parse and analyze error message or problem description
- Identify error type (syntax, runtime, logic, environment)
- Determine root cause category
- Research common patterns for this error type
- Develop step-by-step diagnostic workflow
- Create detailed solution with code corrections
- Add preventive guidance to avoid issue in future
- Document platform-specific considerations
- Build troubleshooting guide for readers
- Link to relevant documentation and resources
- Run execute-checklist.md with code-testing-checklist.md (focus on error handling and testing instructions sections)
  output: docs/troubleshooting/{{issue-name}}-troubleshooting-guide.md

---

## Purpose

This task helps create comprehensive troubleshooting guides for technical book readers. When code examples fail, readers need clear diagnostic steps and solutions. Good troubleshooting documentation anticipates common issues, explains root causes, provides actionable fixes, and helps readers learn debugging skills.

## Prerequisites

Before starting this task:

- Code example exists (working or broken)
- Error description or problem statement available
- Programming language identified
- Access to testing environment matching reader setup
- Understanding of common reader pain points

## Workflow Steps

### 1. Parse Error Message or Problem Description

Analyze the error/problem thoroughly:

**Error Message Analysis:**

Extract key information:

- **Error type**: What kind of error? (SyntaxError, RuntimeError, ImportError, etc.)
- **Error message**: Exact text of the error
- **Stack trace**: Where did the error occur? (file, line number, function)
- **Context**: What was the code trying to do?

**Example - Python Error:**

```
Traceback (most recent call last):
  File "example.py", line 12, in <module>
    result = process_data(input_file)
  File "example.py", line 7, in process_data
    with open(filename, 'r') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'data.txt'
```

**Extracted Information:**

- **Error Type**: FileNotFoundError
- **Error Message**: "No such file or directory: 'data.txt'"
- **Location**: Line 7, in `process_data()` function
- **Context**: Attempting to open a file for reading

**Problem Description Analysis (No Error Yet):**

If no error message exists, identify the symptom:

- What behavior is unexpected?
- What was expected to happen?
- What actually happened?
- When does the issue occur?

### 2. Identify Error Type

Categorize the error:

#### Syntax Errors

Code violates language grammar rules.

**Characteristics:**

- Detected before execution
- Prevents code from running
- Usually has clear error location

**Examples:**

```python
# Python - Missing colon
if x > 10
    print("Large")

# SyntaxError: invalid syntax
```

```javascript
// JavaScript - Missing closing brace
function greet(name) {
    console.log("Hello " + name);
// SyntaxError: Unexpected end of input
```

#### Runtime Errors

Code is syntactically valid but fails during execution.

**Characteristics:**

- Occurs while program is running
- Often caused by invalid operations or missing resources
- May be intermittent

**Examples:**

```python
# Python - Division by zero
result = 10 / 0
# ZeroDivisionError: division by zero
```

```javascript
// JavaScript - Null reference
let user = null;
console.log(user.name);
// TypeError: Cannot read property 'name' of null
```

#### Logic Errors

Code runs without errors but produces wrong results.

**Characteristics:**

- No error message
- Code executes completely
- Output is incorrect or unexpected
- Hardest to debug

**Examples:**

```python
# Python - Off-by-one error
def get_last_item(items):
    return items[len(items)]  # Should be len(items) - 1
# IndexError: list index out of range
```

#### Environment Errors

Code works in one environment but fails in another.

**Characteristics:**

- Platform-specific (Windows/Mac/Linux)
- Version-specific (Python 3.9 vs 3.11)
- Configuration-dependent (missing env vars)
- Dependency-related (wrong package version)

**Examples:**

```python
# Module not found - dependency not installed
import numpy as np
# ModuleNotFoundError: No module named 'numpy'
```

### 3. Determine Root Cause Category

Classify the underlying cause:

**Common Root Cause Categories:**

| Category                    | Description                                     | Common Symptoms                        |
| --------------------------- | ----------------------------------------------- | -------------------------------------- |
| **Missing Dependency**      | Required package/module not installed           | ImportError, ModuleNotFoundError       |
| **File/Path Issues**        | File doesn't exist, wrong path, wrong directory | FileNotFoundError, ENOENT              |
| **Version Incompatibility** | Code uses features from newer version           | SyntaxError, AttributeError            |
| **Platform Differences**    | OS-specific path separators, commands           | FileNotFoundError, command not found   |
| **Configuration Missing**   | Environment variables, config files not set     | KeyError, ValueError                   |
| **Typo/Copy Error**         | Reader mistyped code from book                  | SyntaxError, NameError                 |
| **Permissions**             | Insufficient file/directory permissions         | PermissionError, EACCES                |
| **Port/Resource Conflict**  | Port already in use, resource locked            | Address already in use, EADDRINUSE     |
| **API Changes**             | Library API changed between versions            | AttributeError, TypeError              |
| **Encoding Issues**         | Character encoding mismatches                   | UnicodeDecodeError, UnicodeEncodeError |

### 4. Research Common Patterns

Identify if this is a known common issue:

**Build Knowledge Base Entry:**

```markdown
### Common Issue Pattern: [Pattern Name]

**Frequency:** [Common|Occasional|Rare]

**Typical Error Message:**
```

[exact error text or pattern]

```

**Common Causes:**
1. [Cause 1]
2. [Cause 2]
3. [Cause 3]

**Quick Diagnosis:**
- Check [specific thing]
- Verify [specific condition]
- Test [specific scenario]

**Standard Solution:**
[step-by-step fix]

**Prevention:**
[how to avoid in future]
```

**Example Pattern:**

```markdown
### Common Issue Pattern: Module Not Found in Python

**Frequency:** Very Common (especially for beginners)

**Typical Error Message:**
```

ModuleNotFoundError: No module named 'package_name'
ImportError: No module named 'package_name'

```

**Common Causes:**
1. Package not installed
2. Wrong virtual environment active
3. Package installed for different Python version
4. Typo in package name

**Quick Diagnosis:**
- Run: `pip list | grep package_name`
- Check: `which python` and `which pip`
- Verify: Virtual environment is activated

**Standard Solution:**
1. Activate correct virtual environment
2. Install package: `pip install package_name`
3. Verify: `pip show package_name`

**Prevention:**
- Document all dependencies in `requirements.txt`
- Include setup instructions in README
- Remind readers to activate virtual environment
```

### 5. Develop Step-by-Step Diagnostic Workflow

Create systematic debugging process:

**Diagnostic Workflow Template:**

```markdown
## Debugging Workflow for [Error Name]

### Step 1: Verify the Error

**Action:** Reproduce the error to confirm the issue.

**How to reproduce:**

1. [Exact steps to trigger error]
2. [Expected vs actual behavior]

**What to look for:**

- [Specific error message]
- [Error location]

### Step 2: Check Common Causes

**Action:** Rule out the most frequent causes first.

**Common Cause 1: [Name]**

- **Check:** [What to verify]
- **Command:** `[diagnostic command]`
- **Expected Output:** [What success looks like]
- **If Failed:** [What this means]

**Common Cause 2: [Name]**
[Same structure]

### Step 3: Isolate the Issue

**Action:** Narrow down the exact source.

**Test 1:**

- **Try:** [Specific test]
- **If Succeeds:** [Conclusion]
- **If Fails:** [Next step]

### Step 4: Apply Solution

**Action:** Fix the identified issue.

**Solution:** [Detailed fix with code/commands]

### Step 5: Verify Fix

**Action:** Confirm the issue is resolved.

**Verification:**

1. [Test step 1]
2. [Test step 2]
3. [Expected successful outcome]
```

**Example Workflow:**

```markdown
## Debugging Workflow for FileNotFoundError

### Step 1: Verify the Error

**Action:** Confirm the file path and error message.

**How to reproduce:**

1. Run the code: `python example.py`
2. Observe the error message

**What to look for:**
```

FileNotFoundError: [Errno 2] No such file or directory: 'data.txt'

````

### Step 2: Check Common Causes

**Common Cause 1: Wrong Working Directory**
- **Check:** Current directory
- **Command:** `pwd` (Mac/Linux) or `cd` (Windows)
- **Expected:** Should be in the project directory
- **If Failed:** You're in the wrong directory

**Common Cause 2: File Doesn't Exist**
- **Check:** File exists in expected location
- **Command:** `ls data.txt` (Mac/Linux) or `dir data.txt` (Windows)
- **Expected:** File should be listed
- **If Failed:** File is missing or misnamed

**Common Cause 3: Typo in Filename**
- **Check:** Filename spelling and capitalization
- **Command:** `ls -la` to see all files
- **Expected:** Exact filename match (case-sensitive on Mac/Linux)
- **If Failed:** Fix filename in code or rename file

### Step 3: Isolate the Issue

**Test 1: Check if file exists anywhere in project**
- **Try:** `find . -name "data.txt"` (Mac/Linux) or `dir /s data.txt` (Windows)
- **If Succeeds:** File exists but in wrong location
- **If Fails:** File is completely missing

### Step 4: Apply Solution

**Solution A: File exists in wrong location**
```python
# Change path to correct location
with open('data/data.txt', 'r') as f:  # Add 'data/' prefix
    content = f.read()
````

**Solution B: File is missing**

1. Create the file: `touch data.txt` or create via editor
2. Add sample content
3. Verify: `ls -la data.txt`

**Solution C: Use absolute path (debugging only)**

```python
import os

# Print current directory
print(f"Current directory: {os.getcwd()}")

# Use absolute path temporarily
data_path = os.path.join(os.getcwd(), 'data', 'data.txt')
with open(data_path, 'r') as f:
    content = f.read()
```

### Step 5: Verify Fix

**Verification:**

1. Run code: `python example.py`
2. Should execute without FileNotFoundError
3. Check output is correct

````

### 6. Create Detailed Solution

Provide complete, actionable fix:

**Solution Template:**

```markdown
## Solution: [Problem Name]

### Quick Fix

**For readers who want to get code working immediately:**

```[language]
# Replace this:
[problematic code]

# With this:
[fixed code]
````

**Or run this command:**

```bash
[command to fix issue]
```

### Detailed Explanation

**What was wrong:**
[Clear explanation of the problem]

**Why it happened:**
[Root cause explanation]

**How the fix works:**
[Explanation of the solution]

### Step-by-Step Fix

1. **[Step 1 name]**

   ```bash
   [command or code]
   ```

   **Expected output:**

   ```
   [what you should see]
   ```

2. **[Step 2 name]**
   [instructions]

3. **[Verification]**
   ```bash
   [command to verify fix worked]
   ```

### Alternative Solutions

**Option 1: [Alternative approach]**

- **Pros:** [advantages]
- **Cons:** [disadvantages]
- **How to:** [instructions]

**Option 2: [Another alternative]**

- **Pros:** [advantages]
- **Cons:** [disadvantages]
- **How to:** [instructions]

````

### 7. Add Preventive Guidance

Help readers avoid the issue in future:

**Prevention Template:**

```markdown
## Prevention

### How to Avoid This Issue

1. **[Preventive Measure 1]**
   - [Specific action]
   - [Why this helps]

2. **[Preventive Measure 2]**
   - [Specific action]
   - [Why this helps]

### Best Practices

- ✅ **DO:** [Recommended practice]
- ❌ **DON'T:** [Practice to avoid]

### Checklist for Future Code

- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]
````

**Example Prevention:**

````markdown
## Prevention

### How to Avoid FileNotFoundError

1. **Use Absolute Paths for Critical Files**
   - Convert relative to absolute: `os.path.abspath('data.txt')`
   - Why: Eliminates ambiguity about file location

2. **Check File Exists Before Opening**

   ```python
   import os

   if os.path.exists('data.txt'):
       with open('data.txt', 'r') as f:
           content = f.read()
   else:
       print("Error: data.txt not found")
   ```
````

- Why: Provides better error message

3. **Document File Dependencies**
   - Create README with file structure
   - List all required files and their locations
   - Why: Helps readers set up correctly

### Best Practices

- ✅ **DO:** Include setup instructions with exact file locations
- ✅ **DO:** Provide sample data files in code repository
- ✅ **DO:** Use `os.path.join()` for cross-platform paths
- ❌ **DON'T:** Assume readers will create files from scratch
- ❌ **DON'T:** Use hardcoded absolute paths (not portable)
- ❌ **DON'T:** Rely on specific directory structure without documentation

### Checklist for Future Code Examples

- [ ] All required files listed in README
- [ ] Sample data files included in repository
- [ ] Paths are relative to project root
- [ ] File existence checks included (where appropriate)
- [ ] Error messages are reader-friendly

````

### 8. Document Platform-Specific Considerations

Address cross-platform issues:

**Platform Issues to Document:**

| Issue | Windows | Mac/Linux | Solution |
|-------|---------|-----------|----------|
| **Path Separators** | Backslash `\` | Forward slash `/` | Use `os.path.join()` |
| **Line Endings** | CRLF (`\r\n`) | LF (`\n`) | Open files with `newline` param |
| **Case Sensitivity** | Case-insensitive | Case-sensitive | Document exact casing |
| **Environment Variables** | `%VAR%` | `$VAR` | Use `os.getenv()` |
| **Shell Commands** | PowerShell/CMD | Bash | Provide both versions |
| **Executables** | `.exe` extension | No extension | Use `sys.executable` |

**Example Platform Documentation:**

```markdown
## Platform-Specific Notes

### File Paths

**Issue:** Path separators differ between platforms.

**Windows:**
```python
path = "data\\files\\example.txt"  # Backslashes
````

**Mac/Linux:**

```python
path = "data/files/example.txt"  # Forward slashes
```

**Cross-Platform Solution:**

```python
import os
path = os.path.join("data", "files", "example.txt")
# Automatically uses correct separator
```

### Running Commands

**Windows (PowerShell):**

```powershell
python example.py
Set-Item -Path env:API_KEY -Value "your_key"
```

**Windows (CMD):**

```cmd
python example.py
set API_KEY=your_key
```

**Mac/Linux:**

```bash
python3 example.py
export API_KEY="your_key"
```

````

### 9. Build Troubleshooting Guide for Readers

Create comprehensive reader-facing documentation:

**Troubleshooting Guide Template:**

```markdown
# Troubleshooting Guide: [Issue Name]

## Problem Description

**What readers see:**
[Description of the symptom/error from reader perspective]

**Example error message:**
````

[exact error text]

````

## Quick Diagnosis

**Most common causes (in order of frequency):**

1. ⚠️ **[Most Common Cause]** - [brief description]
2. ⚠️ **[Second Common Cause]** - [brief description]
3. ⚠️ **[Third Common Cause]** - [brief description]

## Step-by-Step Solution

### Solution 1: [Most Common Fix]

**When to use:** [when this solution applies]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Verification:** [how to verify it worked]

### Solution 2: [Alternative Fix]

**When to use:** [when this solution applies]

**Steps:**
[instructions]

## Still Not Working?

If none of the above solutions work:

1. **Double-check your setup:**
   - [ ] [Checklist item 1]
   - [ ] [Checklist item 2]

2. **Try minimal example:**
   ```[language]
   [simplest code that demonstrates issue]
````

3. **Get more information:**

   ```bash
   [diagnostic commands]
   ```

4. **Seek help:**
   - GitHub Issues: [link]
   - Discord/Forum: [link]
   - **When asking for help, include:**
     - Full error message
     - Your OS and language version
     - Output from diagnostic commands

## Prevention

**To avoid this issue in future:**

- [Prevention tip 1]
- [Prevention tip 2]

## Related Issues

- [Link to related troubleshooting guide 1]
- [Link to related troubleshooting guide 2]

````

### 10. Link to Relevant Documentation

Provide references for deeper learning:

**Documentation Links to Include:**

- **Official Language Docs**: Links to relevant API documentation
- **Library Docs**: Package-specific documentation
- **Stack Overflow**: High-quality Q&A threads (stable links only)
- **GitHub Issues**: Known issues and solutions
- **Blog Posts**: Detailed explanations (from reputable sources)
- **Related Book Sections**: Cross-references to relevant chapters

**Link Format:**

```markdown
## Further Reading

### Official Documentation
- [Python File I/O](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files) - Official Python docs on file operations
- [os.path module](https://docs.python.org/3/library/os.path.html) - Path manipulation functions

### Helpful Resources
- [Real Python: Reading and Writing Files](https://realpython.com/read-write-files-python/) - Comprehensive tutorial
- [Stack Overflow: FileNotFoundError despite file existing](https://stackoverflow.com/questions/xxxxx) - Common edge cases

### Related Book Sections
- Chapter 3, Section 3.2: "Working with File Paths"
- Chapter 7, Section 7.1: "Error Handling Best Practices"
- Appendix B: "Setting Up Your Development Environment"
````

## Success Criteria

Troubleshooting guide is complete when:

- [ ] Error/problem clearly identified and categorized
- [ ] Root cause determined
- [ ] Step-by-step diagnostic workflow created
- [ ] Detailed solution with code/commands provided
- [ ] Alternative solutions documented (if applicable)
- [ ] Preventive guidance included
- [ ] Platform-specific considerations addressed
- [ ] Reader-facing troubleshooting guide created
- [ ] Links to documentation included
- [ ] Guide tested with actual error scenario
- [ ] Solutions verified to work
- [ ] code-testing-checklist.md completed (especially error handling and testing instructions sections)

## Common Pitfalls to Avoid

- **Assuming knowledge**: Don't assume readers know how to use terminal, check versions, etc.
- **Vague instructions**: "Check your setup" is not helpful; provide exact commands
- **Missing verification**: Always include how to verify the fix worked
- **Only one solution**: Provide alternatives for different scenarios
- **No examples**: Show concrete examples, not abstract descriptions
- **Technical jargon**: Explain terms that might be unfamiliar to target audience
- **Incomplete command**: Show full command with all flags/parameters
- **No platform variants**: Provide Windows AND Mac/Linux instructions

## Common Error Catalog by Language

### Python

**Import/Module Errors:**

- `ModuleNotFoundError`: Package not installed
- `ImportError`: Package found but can't import (dependencies issue)

**File Errors:**

- `FileNotFoundError`: File doesn't exist at path
- `PermissionError`: Insufficient permissions
- `IsADirectoryError`: Tried to open directory as file

**Type Errors:**

- `TypeError`: Wrong type passed to function
- `AttributeError`: Object doesn't have attribute
- `KeyError`: Dictionary key doesn't exist

**Value Errors:**

- `ValueError`: Invalid value for operation
- `IndexError`: List index out of range

### JavaScript/Node.js

**Reference Errors:**

- `ReferenceError: X is not defined`: Variable not declared
- `ReferenceError: require is not defined`: Using CommonJS in ES modules

**Type Errors:**

- `TypeError: Cannot read property 'X' of undefined`: Accessing property on undefined
- `TypeError: X is not a function`: Calling non-function

**Syntax Errors:**

- `SyntaxError: Unexpected token`: Usually missing bracket/brace
- `SyntaxError: Unexpected end of input`: Unclosed block

**Module Errors:**

- `Error: Cannot find module 'X'`: Package not installed or wrong path

### Java

**Compilation Errors:**

- `error: cannot find symbol`: Typo or missing import
- `error: ';' expected`: Missing semicolon

**Runtime Errors:**

- `NullPointerException`: Accessing null object
- `ArrayIndexOutOfBoundsException`: Array access out of bounds
- `ClassNotFoundException`: Missing JAR dependency

### Ruby

**Name Errors:**

- `NameError: uninitialized constant`: Class/module not found
- `NameError: undefined local variable or method`: Typo or not defined

**Type Errors:**

- `NoMethodError`: Calling method on wrong type
- `TypeError`: Type mismatch

**Load Errors:**

- `LoadError: cannot load such file`: Gem not installed

## Troubleshooting Template Library

Reusable templates for common issues:

### Template: Dependency Not Installed

```markdown
# Troubleshooting: [Package Name] Not Found

## Problem
```

ModuleNotFoundError: No module named '[package]'

````

## Solution
1. Install the package:
   ```bash
   pip install [package]
````

2. Verify installation:

   ```bash
   pip show [package]
   ```

3. Run code again:
   ```bash
   python your_script.py
   ```

## Prevention

Add to `requirements.txt`:

```
[package]==[version]
```

````

### Template: Version Incompatibility

```markdown
# Troubleshooting: Feature Not Available in Your Version

## Problem
Code uses feature from newer version.

## Solution
1. Check your version:
   ```bash
   [language] --version
````

2. Upgrade if needed:

   ```bash
   [upgrade command]
   ```

3. Or modify code for older version:
   [alternative code]

```

## Next Steps

After creating troubleshooting guide:

1. Test guide with actual error scenarios
2. Verify all solutions work as documented
3. Add guide to book's troubleshooting appendix
4. Link from relevant code examples
5. Update based on reader feedback
6. Build catalog of common issues for quick reference
7. Create FAQ section in book documentation
```
