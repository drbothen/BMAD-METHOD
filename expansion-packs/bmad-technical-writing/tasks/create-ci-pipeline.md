<!-- Powered by BMAD™ Core -->

# Create CI Pipeline

---

task:
id: create-ci-pipeline
name: Create CI Pipeline  
 description: Set up continuous integration pipeline to automatically test code on every commit
persona_default: sample-code-maintainer
inputs: - language (programming language: javascript, python, ruby, go) - test-framework (jest, pytest, rspec, go-test, etc.) - platform (github-actions, gitlab-ci, circleci, travis)
steps: - Choose CI platform based on repository host - Create CI configuration file (.github/workflows/\*.yml, .gitlab-ci.yml, etc.) - Define test job with language runtime setup - Configure dependency installation - Add test execution command - Add linting/formatting checks (optional) - Add code coverage reporting (optional) - Add status badge to README - Test CI pipeline with sample commit
output: CI configuration file(s) and status badge in README

---

## Purpose

Automate testing of code samples to catch bugs early and maintain code quality across all examples.

## Platform Selection

### GitHub Actions (Recommended for GitHub repos)

**File:** `.github/workflows/test.yml`
**Pros:** Free for public repos, native GitHub integration
**Cons:** None for most use cases

### GitLab CI

**File:** `.gitlab-ci.yml`
**Pros:** Free, powerful features
**Cons:** GitLab-only

### CircleCI

**File:** `.circleci/config.yml`
**Pros:** Fast, good free tier
**Cons:** Requires separate account

## Workflow Steps

### 1. Create Configuration File

**GitHub Actions (Node.js example):**

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

**Python example:**

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest
```

### 2. Add Linting Job (Optional)

```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: 20.x
    - run: npm ci
    - run: npm run lint
```

### 3. Add Coverage Reporting (Optional)

```yaml
coverage:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci
    - run: npm test -- --coverage
    - uses: codecov/codecov-action@v3
```

### 4. Add Status Badge to README

```markdown
# My Project

![Test Status](https://github.com/username/repo/actions/workflows/test.yml/badge.svg)

Code samples for my book...
```

### 5. Test Pipeline

```bash
git add .github/workflows/test.yml
git commit -m "ci: add GitHub Actions test pipeline"
git push

# Check Actions tab in GitHub to see pipeline run
```

## Success Criteria

- [ ] CI configuration file created
- [ ] Tests run automatically on push
- [ ] Tests pass on all target versions
- [ ] Status badge added to README
- [ ] Pipeline tested with sample commit
- [ ] Team notified of CI setup

## Common Configurations

### Multi-OS Testing

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node-version: [18.x, 20.x]
runs-on: ${{ matrix.os }}
```

### Caching Dependencies

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```
