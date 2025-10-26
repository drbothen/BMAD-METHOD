<!-- Powered by BMAD™ Core -->

# Update Dependencies

---

task:
id: update-dependencies
name: Update Dependencies
description: Safely update project dependencies by checking for updates, testing incrementally, and documenting changes
persona_default: version-manager
inputs:

- package-file (path to package.json, requirements.txt, Gemfile, go.mod, etc.)
- update-strategy (conservative, balanced, aggressive)
- test-command (optional: command to run tests after updates)
  steps:
- Parse dependency file to list current versions
- Check for available updates (npm outdated, pip list --outdated, etc.)
- Categorize updates (patch, minor, major, breaking)
- Apply updates based on strategy (incremental or batched)
- Run tests after each update or batch
- Document breaking changes and required code fixes
- Update lockfile (package-lock.json, requirements.lock, etc.)
- Generate change report
  output: Updated dependency file, lockfile, and change report documenting all updates

---

## Purpose

This task helps you systematically update project dependencies while minimizing risk of breaking changes. Proper dependency management keeps projects secure, performant, and compatible with modern tooling.

## Prerequisites

Before starting this task:

- Dependency file committed to version control (clean working tree)
- Test suite available to validate updates
- Understanding of update strategy based on project stability needs
- Backup or branch for testing updates

## Update Strategies

### Conservative Strategy

**When to use:** Production systems, stable releases, risk-averse projects

**Approach:**

- Only patch updates (1.2.3 → 1.2.4)
- Security updates regardless of version jump
- Thoroughly test each update
- One dependency at a time

**Example:**

```
react: 18.2.0 → 18.2.1 ✅ (patch)
express: 4.18.2 → 4.19.0 ❌ (minor, skip for now)
lodash: 4.17.19 → 4.17.21 ✅ (patch + security fix)
```

### Balanced Strategy (Recommended)

**When to use:** Most projects, active development, quarterly maintenance

**Approach:**

- Patch and minor updates (1.2.3 → 1.3.0)
- Major updates for critical dependencies only
- Batch compatible updates
- Test after each batch

**Example:**

```
react: 18.2.0 → 18.3.1 ✅ (minor)
express: 4.18.2 → 4.19.2 ✅ (minor)
typescript: 5.1.6 → 5.4.5 ✅ (minor)
webpack: 5.88.0 → 6.0.0 ⚠️ (major, careful review)
```

### Aggressive Strategy

**When to use:** New projects, pre-release, keeping bleeding edge

**Approach:**

- All available updates including major versions
- Batch updates by category
- Accept some breaking changes
- Rapid iteration

**Example:**

```
All packages → latest versions
May require significant code changes
High test coverage essential
```

## Workflow Steps

### 1. Parse Current Dependencies

**Check current versions:**

**Node.js (npm):**

```bash
# List all dependencies with versions
npm list --depth=0

# Check for outdated packages
npm outdated

# Output format:
# Package    Current  Wanted  Latest  Location
# react      18.2.0   18.2.1  18.3.1  node_modules/react
# express    4.18.2   4.18.2  4.19.2  node_modules/express
```

**Python (pip):**

```bash
# List installed packages
pip list

# Check for outdated packages
pip list --outdated

# Output format:
# Package    Version  Latest   Type
# requests   2.28.0   2.31.0   wheel
# flask      2.2.0    3.0.0    wheel
```

**Ruby (bundler):**

```bash
# List dependencies
bundle list

# Check for outdated gems
bundle outdated

# Output format:
# Gem          Current  Latest  Requested  Groups
# rails        7.0.8    7.1.3   ~> 7.0.0   default
```

### 2. Categorize Updates

**Classify by semantic versioning:**

```markdown
## Available Updates

### Patch Updates (Low Risk)

- lodash: 4.17.19 → 4.17.21 (bug fixes, security)
- axios: 1.6.0 → 1.6.8 (bug fixes)
- dotenv: 16.3.1 → 16.3.2 (patch)

### Minor Updates (Medium Risk)

- react: 18.2.0 → 18.3.1 (new features, backward compatible)
- typescript: 5.1.6 → 5.4.5 (new features)
- eslint: 8.48.0 → 8.57.0 (new rules, compatible)

### Major Updates (High Risk)

- webpack: 5.88.0 → 6.0.0 (breaking changes)
- node-sass: 7.0.3 → 9.0.0 (breaking changes)
- jest: 28.1.0 → 29.7.0 (breaking changes)

### Security Updates (Critical - Any Version Jump)

- express: 4.17.1 → 4.18.2 (CVE-2022-24999)
- trim: 0.0.1 → 1.0.1 (CVE-2020-7753)
```

### 3. Apply Updates Based on Strategy

**Conservative approach (one at a time):**

```bash
# Update one package
npm install lodash@latest
npm test
git commit -m "chore: update lodash 4.17.19 → 4.17.21"

# Repeat for each package
```

**Balanced approach (batch compatible):**

```bash
# Update all patch versions
npm update

# Test batch
npm test

# If tests pass, commit
git add package.json package-lock.json
git commit -m "chore: update patch versions"

# Update minor versions one at a time or in small batches
npm install react@latest react-dom@latest
npm test
git commit -m "chore: update react 18.2.0 → 18.3.1"
```

**Aggressive approach (update all):**

```bash
# Update all to latest (use with caution)
npm update --latest  # or use npm-check-updates (ncu)

# Using npm-check-updates tool:
npx npm-check-updates -u
npm install
npm test
```

### 4. Run Tests After Updates

**Test after each update or batch:**

```bash
# Run test suite
npm test

# If tests fail:
# 1. Review error messages
# 2. Check package changelog
# 3. Fix breaking changes or revert update
```

**Example test workflow:**

```bash
#!/bin/bash
# update-and-test.sh

PACKAGE=$1
VERSION=$2

echo "Updating $PACKAGE to $VERSION..."
npm install "$PACKAGE@$VERSION"

echo "Running tests..."
if npm test; then
  echo "✅ Tests passed. Committing..."
  git add package.json package-lock.json
  git commit -m "chore: update $PACKAGE to $VERSION"
else
  echo "❌ Tests failed. Reverting..."
  git checkout package.json package-lock.json
  npm install
  exit 1
fi
```

### 5. Document Breaking Changes

**Track what broke and how to fix:**

```markdown
## Update Change Log

### 2024-01-15: Dependency Updates

#### webpack 5.88.0 → 6.0.0

**Breaking Changes:**

- `optimization.splitChunks.cacheGroups` syntax changed
- Node.js 18+ required

**Fixes Applied:**

- Updated webpack.config.js splitChunks configuration
- Updated CI/CD to Node 18

**Files Modified:**

- webpack.config.js
- .github/workflows/test.yml

#### jest 28.1.0 → 29.7.0

**Breaking Changes:**

- `jest-environment-jsdom` now separate package
- `describe.only.each` syntax changed

**Fixes Applied:**

- Installed jest-environment-jsdom separately
- Updated test files using describe.only.each

**Files Modified:**

- package.json (added jest-environment-jsdom)
- tests/components/Button.test.js
```

### 6. Update Lockfile

**Ensure lockfile is regenerated:**

```bash
# npm - automatically updates package-lock.json
npm install

# Yarn - updates yarn.lock
yarn install

# pnpm - updates pnpm-lock.yaml
pnpm install

# Python pip - generate/update requirements.lock
pip freeze > requirements.lock

# Commit lockfile with package file
git add package.json package-lock.json
git commit -m "chore: update dependencies"
```

### 7. Generate Change Report

**Document all changes:**

````markdown
# Dependency Update Report

Generated: 2024-01-15

## Summary

- **Total Updates:** 12
- **Patch:** 6
- **Minor:** 4
- **Major:** 2
- **Security Fixes:** 2
- **Breaking Changes:** 2
- **Test Status:** All passing ✅

## Updated Packages

### Patch Updates (6)

| Package              | From    | To      | Type     |
| -------------------- | ------- | ------- | -------- |
| lodash               | 4.17.19 | 4.17.21 | Security |
| axios                | 1.6.0   | 1.6.8   | Patch    |
| dotenv               | 16.3.1  | 16.3.2  | Patch    |
| prettier             | 3.0.3   | 3.0.5   | Patch    |
| eslint-config-airbnb | 19.0.4  | 19.0.5  | Patch    |
| @types/node          | 20.8.0  | 20.8.9  | Patch    |

### Minor Updates (4)

| Package    | From   | To     | Type  |
| ---------- | ------ | ------ | ----- |
| react      | 18.2.0 | 18.3.1 | Minor |
| react-dom  | 18.2.0 | 18.3.1 | Minor |
| typescript | 5.1.6  | 5.4.5  | Minor |
| eslint     | 8.48.0 | 8.57.0 | Minor |

### Major Updates (2)

| Package | From   | To     | Breaking Changes        |
| ------- | ------ | ------ | ----------------------- |
| webpack | 5.88.0 | 6.0.0  | Config syntax, Node 18+ |
| jest    | 28.1.0 | 29.7.0 | jsdom separate package  |

## Security Fixes

### CVE-2022-24999 (express)

- **Severity:** High
- **Package:** express
- **Fixed in:** 4.18.2
- **Impact:** Prototype pollution vulnerability
- **Action:** Updated to 4.19.2

### CVE-2020-7753 (trim)

- **Severity:** High
- **Package:** trim (via lodash)
- **Fixed in:** lodash 4.17.21
- **Impact:** ReDoS vulnerability
- **Action:** Updated lodash

## Breaking Changes & Fixes

### webpack 6.0.0

**Config changes required:**

```javascript
// Before (webpack 5)
optimization: {
  splitChunks: {
    cacheGroups: {
      vendor: {
        test: /[\\/]node_modules[\\/]/,
        name: 'vendors',
        chunks: 'all'
      }
    }
  }
}

// After (webpack 6)
optimization: {
  splitChunks: {
    cacheGroups: {
      defaultVendors: {  // renamed from 'vendor'
        test: /[\\/]node_modules[\\/]/,
        name: 'vendors',
        chunks: 'all'
      }
    }
  }
}
```
````

### jest 29.0.0

**New dependency required:**

```bash
npm install -D jest-environment-jsdom
```

**jest.config.js:**

```javascript
module.exports = {
  testEnvironment: 'jest-environment-jsdom', // now explicit package
};
```

## Test Results

- Unit tests: 142/142 passed ✅
- Integration tests: 28/28 passed ✅
- E2E tests: 12/12 passed ✅
- Coverage: 87% (no change)

## Files Modified

- package.json
- package-lock.json
- webpack.config.js
- jest.config.js
- .github/workflows/test.yml

## Recommendations

1. Monitor application for 24-48 hours after deployment
2. Next update cycle: 3 months (April 2024)
3. Consider upgrading to Node 20 LTS in next cycle

````

## Success Criteria

Dependency update is complete when:

- [ ] All available updates reviewed and categorized
- [ ] Updates applied according to chosen strategy
- [ ] Tests pass after all updates
- [ ] Lockfile regenerated and committed
- [ ] Breaking changes documented with fixes
- [ ] Change report generated
- [ ] Security vulnerabilities addressed
- [ ] No new warnings or errors introduced

## Update Workflow Scripts

### npm Update Script

```bash
#!/bin/bash
# safe-update.sh - Conservative update approach

echo "🔍 Checking for outdated packages..."
npm outdated

echo ""
echo "📦 Updating patch versions only..."
npm update

echo ""
echo "🧪 Running tests..."
if npm test; then
  echo "✅ Tests passed!"
  echo ""
  echo "📝 Committing changes..."
  git add package.json package-lock.json
  git commit -m "chore: update patch versions"
  echo "✅ Update complete!"
else
  echo "❌ Tests failed. Reverting..."
  git checkout package.json package-lock.json
  npm install
  exit 1
fi
````

### Aggressive Update with npm-check-updates

```bash
#!/bin/bash
# aggressive-update.sh

# Install ncu if not available
if ! command -v ncu &> /dev/null; then
  npm install -g npm-check-updates
fi

# Create backup branch
git checkout -b dependency-updates-$(date +%Y%m%d)

# Show what would be updated
echo "🔍 Checking for all available updates..."
ncu

# Update package.json to latest versions
echo ""
echo "📦 Updating to latest versions..."
ncu -u

# Install new versions
npm install

# Run tests
echo ""
echo "🧪 Running tests..."
if npm test; then
  echo "✅ Tests passed!"
  git add package.json package-lock.json
  git commit -m "chore: update all dependencies to latest"
else
  echo "❌ Tests failed. Review changes needed."
  echo "Branch created: dependency-updates-$(date +%Y%m%d)"
fi
```

## Common Pitfalls to Avoid

**❌ Updating all at once without testing:**

- Can't identify which update broke tests

✅ **Update incrementally or in batches:**

- Test after each update or small batch

**❌ Ignoring lockfile changes:**

- Inconsistent dependencies across environments

✅ **Always commit lockfile:**

- Ensures reproducible installs

**❌ Skipping changelog review:**

- Missing breaking changes, new features

✅ **Read changelogs for major updates:**

- Understand what changed and why

**❌ Not testing thoroughly:**

- Breaking changes slip into production

✅ **Run full test suite:**

- Unit, integration, and E2E tests

## Next Steps

After updating dependencies:

1. Run `execute-checklist.md` with `version-update-checklist.md`
2. Deploy to staging environment for validation
3. Monitor for issues before production deployment
4. Schedule next update cycle (monthly/quarterly)
5. Document any manual testing performed
6. Update documentation if APIs changed
