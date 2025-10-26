<!-- Powered by BMAD™ Core -->

# Run Tests

---

task:
id: run-tests
name: Run Tests
description: Execute test suite with coverage reporting and provide debugging guidance for failures
persona_default: sample-code-maintainer
inputs: - test-path (path to test files or directory) - language (javascript, python, ruby, go, etc.) - framework (jest, pytest, rspec, go-test, etc.)
steps: - Detect test framework from project configuration - Install test dependencies if needed - Run tests with coverage enabled - Generate test report (HTML, JSON, or terminal output) - Identify failing tests - Provide debugging guidance for failures - Generate coverage report - Check coverage thresholds
output: Test execution report with pass/fail status, coverage metrics, and failure diagnostics

---

## Purpose

Validate code quality by running automated tests and ensuring all examples work as expected.

## Framework Detection

### JavaScript

```bash
# Check package.json for test framework
if grep -q "jest" package.json; then
  FRAMEWORK="jest"
elif grep -q "mocha" package.json; then
  FRAMEWORK="mocha"
elif grep -q "vitest" package.json; then
  FRAMEWORK="vitest"
fi
```

### Python

```bash
# Check for pytest or unittest
if [ -f "pytest.ini" ] || grep -q "pytest" requirements.txt; then
  FRAMEWORK="pytest"
else
  FRAMEWORK="unittest"
fi
```

## Workflow Steps

### 1. Install Dependencies

```bash
# JavaScript
npm install  # or npm ci for CI environments

# Python
pip install -r requirements.txt

# Ruby
bundle install
```

### 2. Run Tests

**Jest (JavaScript):**

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- path/to/test.js

# Run in watch mode (development)
npm test -- --watch
```

**pytest (Python):**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_api.py

# Verbose output
pytest -v
```

**RSpec (Ruby):**

```bash
# Run all tests
bundle exec rspec

# Run with coverage
bundle exec rspec --format documentation

# Run specific test
bundle exec rspec spec/models/user_spec.rb
```

**Go:**

```bash
# Run all tests
go test ./...

# Run with coverage
go test -cover ./...

# Generate coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### 3. Interpret Test Results

**All tests passing:**

```
PASS  tests/utils/helpers.test.js
PASS  tests/components/Button.test.js
PASS  tests/api/users.test.js

Test Suites: 3 passed, 3 total
Tests:       24 passed, 24 total
Time:        2.451 s
```

**Some tests failing:**

```
FAIL  tests/api/users.test.js
  ● getUserById › returns user when found

    expect(received).toEqual(expected)

    Expected: {"id": "123", "name": "John"}
    Received: {"id": "123", "name": "Jane"}

      at Object.<anonymous> (tests/api/users.test.js:15:23)

Test Suites: 1 failed, 2 passed, 3 total
Tests:       1 failed, 23 passed, 24 total
```

### 4. Generate Coverage Report

**Jest coverage output:**

```
----------|---------|----------|---------|---------|-------------------
File      | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
----------|---------|----------|---------|---------|-------------------
All files |   87.5  |   83.33  |   90.91 |   87.5  |
 api.js   |   100   |   100    |   100   |   100   |
 utils.js |   75    |   66.67  |   81.82 |   75    | 23-24,45-48
----------|---------|----------|---------|---------|-------------------
```

### 5. Debug Failing Tests

**Common failure patterns:**

**Assertion mismatch:**

```javascript
// Test expects "John" but gets "Jane"
// Check data fixtures or mock setup

// Fix:
const mockUser = { id: '123', name: 'John' }; // Was: 'Jane'
```

**Async timing issues:**

```javascript
// Test fails intermittently
// Missing await or not waiting for async operations

// Fix:
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});
```

**Missing dependencies:**

```bash
# Error: Cannot find module 'axios'
npm install axios
```

**Environment setup:**

```javascript
// Test fails due to missing env variable
// Add to .env.test file or mock

process.env.API_URL = 'http://localhost:3000';
```

### 6. Check Coverage Thresholds

**Configure thresholds (jest.config.js):**

```javascript
module.exports = {
  coverageThresholds: {
    global: {
      statements: 80,
      branches: 80,
      functions: 80,
      lines: 80,
    },
  },
};
```

**If coverage below threshold:**

```
Jest: "global" coverage threshold for statements (80%) not met: 75%
Jest: "global" coverage threshold for branches (80%) not met: 66.67%
```

**Action:** Add tests for uncovered code or adjust thresholds

## Success Criteria

- [ ] All tests execute successfully
- [ ] Test failures (if any) identified and documented
- [ ] Coverage report generated
- [ ] Coverage meets thresholds (typically 80%+)
- [ ] No console errors or warnings
- [ ] Performance acceptable (tests complete in <30s for small projects)

## Output Format

```markdown
# Test Execution Report

**Date:** 2024-01-15
**Project:** My Book Code Samples
**Framework:** Jest 29.7.0
**Node Version:** 20.10.0

## Summary

- ✅ Test Suites: 12 passed, 12 total
- ✅ Tests: 87 passed, 87 total
- ⏱️ Time: 8.234 s
- 📊 Coverage: 87.5% (statements)

## Coverage Breakdown

| File        | Statements | Branches   | Functions  | Lines     |
| ----------- | ---------- | ---------- | ---------- | --------- |
| api.js      | 100%       | 100%       | 100%       | 100%      |
| utils.js    | 75%        | 66.67%     | 81.82%     | 75%       |
| **Overall** | **87.5%**  | **83.33%** | **90.91%** | **87.5%** |

## Uncovered Lines

- `src/utils.js:23-24` - Error handling path not tested
- `src/utils.js:45-48` - Edge case not covered

## Recommendations

1. Add test for error handling in utils.js
2. Add edge case test for validateInput function
3. All other code paths well-covered
```

## Automation Script

```bash
#!/bin/bash
# run-tests.sh - Comprehensive test execution script

set -e

echo "🧪 Running test suite..."
echo ""

# Run tests with coverage
npm test -- --coverage --verbose

# Check exit code
if [ $? -eq 0 ]; then
  echo ""
  echo "✅ All tests passed!"

  # Generate coverage badge (optional)
  npx coverage-badge-creator

  # Open coverage report (optional)
  # open coverage/index.html

  exit 0
else
  echo ""
  echo "❌ Tests failed!"
  echo ""
  echo "Debug steps:"
  echo "1. Check error messages above"
  echo "2. Run specific failing test: npm test -- path/to/test.js"
  echo "3. Run in watch mode: npm test -- --watch"

  exit 1
fi
```
