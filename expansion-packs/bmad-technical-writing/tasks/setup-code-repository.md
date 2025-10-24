<!-- Powered by BMAD™ Core -->

# Setup Code Repository

---

task:
id: setup-code-repository
name: Setup Code Repository
description: Initialize and structure GitHub repository for book code examples
persona_default: sample-code-maintainer
inputs:

- book-name
- programming-language
- target-platforms
  steps:
- Initialize GitHub repository
- Create chapter-based folder structure
- Add README.md with repository overview
- Create requirements or package files per chapter
- Set up testing infrastructure
- Create .gitignore for language-specific files
- Add LICENSE file
- Document version and platform requirements
- Create CI/CD pipeline (optional)
- Add contribution guidelines if open-source
- Run execute-checklist.md with repository-quality-checklist.md
  output: Code repository at https://github.com/{{org}}/{{repo-name}}

---

## Purpose

This task guides you through creating a well-organized, professional code repository that accompanies your technical book. Readers should be able to clone the repository and immediately start working with the code examples.

## Prerequisites

Before starting this task:

- GitHub account created
- Git installed locally
- Book outline with chapter structure
- Understanding of target programming language ecosystem
- Knowledge of target platforms (Windows/Mac/Linux)

## Workflow Steps

### 1. Initialize GitHub Repository

Create the repository:

**Steps:**

1. Go to GitHub.com and create new repository
2. Choose repository name (e.g., `mastering-web-apis-code`)
3. Add description: "Code examples for [Book Title]"
4. Choose public or private (usually public for published books)
5. Initialize with README (we'll replace it)
6. Clone locally: `git clone https://github.com/yourusername/repo-name.git`

**Naming Conventions:**

- Use book title or abbreviation
- Append `-code` or `-examples`
- Use lowercase with hyphens
- Examples: `python-data-science-code`, `react-book-examples`

### 2. Create Chapter-Based Folder Structure

Organize by chapters:

**Standard Structure:**

```
repo-root/
├── chapter-01/
│   ├── example-01-hello-world/
│   ├── example-02-variables/
│   └── README.md
├── chapter-02/
│   ├── example-01-functions/
│   ├── example-02-classes/
│   └── README.md
├── chapter-03/
│   └── ...
├── appendix-a/
├── bonus-content/
├── tests/
├── .github/
│   └── workflows/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt (or package.json, etc.)
```

**Alternative Structure (for small books):**

```
repo-root/
├── src/
│   ├── ch01_example1.py
│   ├── ch01_example2.py
│   ├── ch02_example1.py
│   └── ...
├── tests/
├── README.md
└── requirements.txt
```

**Create Folders:**

```bash
mkdir -p chapter-{01..12}
mkdir -p tests
mkdir -p .github/workflows
```

### 3. Add README.md with Repository Overview

Create comprehensive README:

**README Template:**

````markdown
# [Book Title] - Code Examples

Code examples and exercises from **[Book Title]** by [Author Name].

## About This Repository

This repository contains all code examples from the book, organized by chapter. Each example is self-contained and includes:

- Working code with comments
- Setup instructions
- Expected output
- Common troubleshooting tips

## Prerequisites

- [Language] version X.X or higher
- [Tool/Framework] (optional)
- Basic understanding of [concepts]

## Installation

### Option 1: Clone Entire Repository

```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```
````

### Option 2: Download Specific Chapter

Navigate to the chapter folder and download individual examples.

## Setup

1. Install dependencies:

   ```bash
   [package manager install command]
   ```

2. Verify installation:

   ```bash
   [verification command]
   ```

3. Run tests (optional):
   ```bash
   [test command]
   ```

## Repository Structure

- `chapter-01/` - Introduction and basics
- `chapter-02/` - [Chapter topic]
- `chapter-03/` - [Chapter topic]
- ...
- `tests/` - Automated tests for code examples
- `appendix-a/` - Additional resources

## Usage

Each chapter folder contains a README with:

- Learning objectives for that chapter
- Setup instructions specific to examples
- How to run the code
- Expected output

Navigate to a chapter and follow its README.

## Requirements

- [Language]: [Version]
- [Framework/Library]: [Version]
- [Platform]: [Supported platforms]

See `requirements.txt` (or `package.json`, `Gemfile`, etc.) for complete dependency list.

## Running Examples

```bash
cd chapter-03/example-01-api-basics
[command to run example]
```

## Testing

```bash
[command to run all tests]
```

## Contributing

Found a bug or improvement? Please [open an issue](link) or submit a pull request.

## License

[License type - MIT, Apache 2.0, etc.]

## About the Book

**[Book Title]**
By [Author Name]
Published by [Publisher]
[Purchase link]

## Support

- [Book website](link)
- [Author contact](link)
- [Errata page](link)

```

### 4. Create Requirements/Package Files Per Chapter

Define dependencies:

**For Python:**

Create `requirements.txt` in root and per-chapter if dependencies differ:

```

# requirements.txt (root)

requests==2.31.0
pytest==7.4.0
black==23.7.0

# chapter-03/requirements.txt (if different)

requests==2.31.0
flask==2.3.0

````

**For Node.js:**

Create `package.json`:

```json
{
  "name": "book-code-examples",
  "version": "1.0.0",
  "description": "Code examples for [Book Title]",
  "scripts": {
    "test": "jest",
    "lint": "eslint ."
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "eslint": "^8.43.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
````

**For Java:**

Create `pom.xml` (Maven) or `build.gradle` (Gradle)

**Version Pinning:**

- Pin exact versions for reproducibility
- Document why specific versions are required
- Test with version ranges if supporting multiple versions

### 5. Set Up Testing Infrastructure

Add automated tests:

**Python (pytest):**

```python
# tests/test_chapter01.py
import pytest
from chapter01.example01 import hello_world

def test_hello_world():
    result = hello_world()
    assert result == "Hello, World!"
```

**Node.js (Jest):**

```javascript
// tests/chapter01.test.js
const { helloWorld } = require('../chapter-01/example-01/index');

test('returns hello world', () => {
  expect(helloWorld()).toBe('Hello, World!');
});
```

**Test Structure:**

```
tests/
├── test_chapter01.py
├── test_chapter02.py
├── test_chapter03.py
└── conftest.py (pytest configuration)
```

### 6. Create .gitignore

Exclude unnecessary files:

**Python .gitignore:**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
```

**Node.js .gitignore:**

```
# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/

# OS
.DS_Store

# Testing
coverage/
.nyc_output/
```

### 7. Add LICENSE File

Choose appropriate license:

**MIT License (permissive):**

```
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

**Apache 2.0 (permissive with patent grant):**

Use for enterprise-friendly code.

**Creative Commons (for content):**

Consider for tutorials/documentation.

**How to Choose:**

- MIT: Simple, permissive, widely used
- Apache 2.0: Patent protection, enterprise-friendly
- GPL: Copyleft, requires derivative works to be open source
- Proprietary: All rights reserved (unusual for book code)

### 8. Document Version and Platform Requirements

Specify compatibility:

**Create REQUIREMENTS.md or include in README:**

```markdown
## System Requirements

### Supported Platforms

- ✅ macOS 11+ (Big Sur or later)
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 20.04+, Fedora 35+, Debian 11+)

### Software Requirements

- Python 3.11 or higher (tested on 3.11, 3.12)
- pip 23.0+
- Git 2.30+

### Optional Tools

- Docker 20.10+ (for containerized examples)
- VS Code 1.75+ (recommended IDE)
```

### 9. Create CI/CD Pipeline (Optional but Recommended)

Automate testing:

**GitHub Actions (.github/workflows/test.yml):**

```yaml
name: Test Code Examples

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.11', '3.12']

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest tests/
```

**Benefits of CI/CD:**

- Catch breaking changes immediately
- Verify cross-platform compatibility
- Test multiple language versions
- Build confidence for readers

### 10. Add Contribution Guidelines

If open-source:

**Create CONTRIBUTING.md:**

```markdown
# Contributing

Thank you for your interest in improving these code examples!

## Reporting Issues

- Check existing issues first
- Provide code example and error message
- Specify your platform and version

## Submitting Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Submit pull request with clear description

## Code Style

- Follow [language-specific style guide]
- Run linter before committing
- Add comments for complex logic
```

### 11. Validate Repository Quality

Run checklist:

- Run execute-checklist.md with repository-quality-checklist.md

## Success Criteria

A completed code repository should have:

- [ ] GitHub repository initialized and cloned
- [ ] Logical folder structure (chapter-based or src-based)
- [ ] Comprehensive README.md
- [ ] Dependencies documented (requirements.txt, package.json, etc.)
- [ ] Testing infrastructure set up
- [ ] Proper .gitignore for language
- [ ] LICENSE file included
- [ ] Version and platform requirements documented
- [ ] CI/CD pipeline configured (optional)
- [ ] Contribution guidelines (if open-source)
- [ ] Repository quality checklist passed

## Common Pitfalls to Avoid

- **No structure**: Dumping all code in root directory
- **Missing dependencies**: Not documenting required packages
- **No README**: Readers don't know how to use the repository
- **Untested code**: Code works on author's machine only
- **No license**: Legal uncertainty for readers
- **Platform assumptions**: Code only works on one OS
- **Outdated dependencies**: Using deprecated package versions

## Next Steps

After setting up the repository:

1. Add code examples as you write chapters
2. Test on all supported platforms
3. Update README as repository grows
4. Set up GitHub Pages for documentation (optional)
5. Link repository prominently in book's front matter
