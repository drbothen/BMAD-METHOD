<!-- Powered by BMAD™ Core -->

# Assess Version Impact

---

task:
id: assess-version-impact
name: Assess Version Impact
description: Analyze the impact of upgrading from one version to another by identifying breaking changes and affected code
persona_default: version-manager
inputs:
  - current-version (current version being used)
  - target-version (version to upgrade to)
  - codebase-path (path to code samples or project)
steps:
  - Review official changelog for breaking changes
  - Identify deprecated features in target version
  - Scan codebase for patterns affected by changes
  - Generate impact report listing affected files
  - Estimate migration effort (hours/complexity)
  - Create prioritized migration checklist
  - Document required code changes
  - Identify testing requirements
output: Version migration impact report with affected files, effort estimate, and migration checklist

---

## Purpose

This task helps you systematically analyze the impact of upgrading to a new version, ensuring you understand what needs to change before starting migration. Proper impact assessment prevents surprises, estimates effort accurately, and creates a clear migration plan.

## Prerequisites

Before starting this task:

- Current and target versions identified
- Access to official changelog and migration guides
- Codebase available for analysis
- Understanding of features used in project

## Impact Assessment Components

### 1. Breaking Changes List

Changes that will cause code to fail:

```markdown
## Breaking Changes: Node 18 → Node 20

1. **DNS Resolution Order Changed**
   - Old: `ipv4first` (IPv4 preferred)
   - New: `verbatim` (use order from DNS)
   - Impact: Network code may behave differently

2. **Import Assertions Deprecated**
   - Old: `import json from './data.json' assert { type: 'json' }`
   - New: `import json from './data.json' with { type: 'json' }`
   - Impact: All JSON imports need syntax update

3. **Removed APIs**
   - `process.binding()` removed
   - Some experimental V8 flags removed
   - Impact: Code using removed APIs will fail
```

### 2. Affected Files Report

Scan results showing impacted code:

```markdown
## Affected Files

### High Impact (Code will break)

- `src/utils/network.js` - Uses removed DNS flag
- `src/config/loader.js` - Uses deprecated import assertions (3 occurrences)
- `tests/integration/api.test.js` - Uses removed API

### Medium Impact (Deprecated but still works)

- `src/modules/parser.js` - Uses deprecated URL API
- `lib/crypto.js` - Uses old crypto method (soft-deprecated)

### Low Impact (Warnings only)

- `package.json` - Engine version needs update
- `.nvmrc` - Node version needs update

**Total Files Affected:** 6
**Critical Files:** 3
```

### 3. Effort Estimate

Time and complexity assessment:

```markdown
## Migration Effort Estimate

| Category              | Files | Estimated Hours | Complexity |
| --------------------- | ----- | --------------- | ---------- |
| Breaking Changes      | 3     | 4-6 hours       | Medium     |
| Deprecation Fixes     | 2     | 2-3 hours       | Low        |
| Testing & Validation  | All   | 4-6 hours       | Medium     |
| Documentation Updates | N/A   | 1-2 hours       | Low        |

**Total Estimated Effort:** 11-17 hours
**Risk Level:** Medium
**Recommended Timeline:** 2-3 days
```

### 4. Migration Checklist

Actionable steps to complete migration:

```markdown
## Migration Checklist

### Pre-Migration

- [ ] Backup current codebase
- [ ] Create migration branch
- [ ] Review full changelog
- [ ] Update local Node.js to 20.x

### Code Changes

- [ ] Update import assertions to import attributes (3 files)
- [ ] Fix DNS resolution code (1 file)
- [ ] Replace removed APIs (1 file)
- [ ] Update deprecated crypto calls (1 file)

### Configuration Updates

- [ ] Update package.json engines field
- [ ] Update .nvmrc file
- [ ] Update CI/CD Node version
- [ ] Update Dockerfile base image

### Testing

- [ ] Run full test suite on Node 20
- [ ] Test network-dependent features
- [ ] Run integration tests
- [ ] Performance testing

### Deployment

- [ ] Update staging environment
- [ ] Monitor for issues
- [ ] Update production environment
- [ ] Update documentation
```

## Workflow Steps

### 1. Review Official Changelog

**Find and read changelog:**

**Node.js:**

- Changelog: https://github.com/nodejs/node/blob/main/CHANGELOG.md
- Breaking changes: https://github.com/nodejs/node/blob/main/doc/changelogs/CHANGELOG_V20.md

**Python:**

- What's New: https://docs.python.org/3/whatsnew/3.12.html
- Porting guide: https://docs.python.org/3/whatsnew/3.12.html#porting-to-python-3-12

**Extract breaking changes:**

```markdown
## Breaking Changes Research: Node 18 → 20

### From Changelog

**DNS Resolution:**

- Commit: [reference]
- Description: Changed default resolution from `ipv4first` to `verbatim`
- Reason: Better compliance with DNS standards
- Migration: Set `verbatim: false` if old behavior needed

**Import Syntax:**

- RFC: Import Attributes (replacing Import Assertions)
- Old syntax: `assert { type: 'json' }`
- New syntax: `with { type: 'json' }`
- Timeline: Assertions deprecated in 20.10, will be removed in future

**Removed APIs:**

- `process.binding()` - Internal API removed
- Some `--experimental` flags removed or stabilized
- Legacy stream methods removed
```

### 2. Identify Deprecated Features

**Find what's deprecated (but still works):**

```markdown
## Deprecated in Target Version (Node 20)

### Runtime Deprecations (DEP0XXX)

**DEP0018:** Unhandled promise rejections

- Status: Will become fatal errors in future
- Action: Ensure all promises have `.catch()` or try/catch

**DEP0147:** `fs.rmdir(path, { recursive: true })`

- Status: Deprecated
- Alternative: Use `fs.rm(path, { recursive: true })`
- Timeline: Will be removed in Node 22

**DEP0166:** Import assertions

- Status: Deprecated in favor of import attributes
- Timeline: Will be removed in future major version
```

### 3. Scan Codebase for Affected Patterns

**Automated scanning:**

**Scan for import assertions:**

```bash
# Find import assertions (deprecated syntax)
grep -r "assert { type:" src/

# Output:
# src/config/loader.js:import data from './data.json' assert { type: 'json' };
# src/utils/parser.js:import schema from './schema.json' assert { type: 'json' };
# tests/fixtures/loader.test.js:import mock from './mock.json' assert { type: 'json' };
```

**Scan for removed APIs:**

```bash
# Find process.binding() usage (removed)
grep -r "process\.binding" src/

# Find deprecated fs.rmdir with recursive
grep -r "rmdir.*recursive" src/
```

**Scan for DNS configuration:**

```bash
# Find DNS lookup configurations
grep -r "lookup\|resolve\|dns" src/
```

**Scan for experimental flags:**

```bash
# Check package.json scripts for experimental flags
grep "experimental" package.json

# Check .env or config files
grep "NODE_OPTIONS" .env
```

**Create scan report:**

```markdown
## Codebase Scan Results

### Import Assertions (Deprecated Syntax)

Found 3 occurrences:

1. `src/config/loader.js:12` - import data from './data.json' assert { type: 'json' };
2. `src/utils/parser.js:5` - import schema from './schema.json' assert { type: 'json' };
3. `tests/fixtures/loader.test.js:8` - import mock from './mock.json' assert { type: 'json' };

**Action Required:** Update to `with { type: 'json' }` syntax

### process.binding() Usage

Found 0 occurrences ✓

### fs.rmdir() with recursive option

Found 1 occurrence:

1. `src/utils/cleanup.js:45` - fs.rmdirSync(dir, { recursive: true });

**Action Required:** Replace with fs.rm()

### DNS Configuration

Found 2 occurrences:

1. `src/services/api-client.js:23` - dns.lookup() without options
2. `src/utils/network.js:67` - Custom DNS resolver

**Action Required:** Review DNS behavior, may need `verbatim: false` option
```

### 4. Generate Impact Report

**Categorize findings:**

```markdown
## Impact Report: Node 18 → Node 20 Migration

### Executive Summary

- **Affected Files:** 6 out of 142 files (4%)
- **Critical Issues:** 3 files will break
- **Warnings:** 2 files use deprecated APIs
- **Configuration:** 3 config files need updates
- **Estimated Effort:** 11-17 hours
- **Risk Level:** Medium

### Critical Impact (Code Will Break)

#### 1. Import Syntax Changes

**Files Affected:** 3

- src/config/loader.js
- src/utils/parser.js
- tests/fixtures/loader.test.js

**Issue:** Import assertions deprecated, must use import attributes
**Fix:** Replace `assert` with `with` keyword
**Effort:** 1 hour (straightforward find-replace)
**Risk:** Low (syntax change only)

#### 2. DNS Resolution Behavior

**Files Affected:** 2

- src/services/api-client.js
- src/utils/network.js

**Issue:** DNS resolution order changed from ipv4first to verbatim
**Fix:** May need explicit `verbatim: false` option or code review
**Effort:** 3-4 hours (requires testing)
**Risk:** Medium (behavior change may affect production)

#### 3. Deprecated fs API

**Files Affected:** 1

- src/utils/cleanup.js

**Issue:** fs.rmdir() with recursive option deprecated
**Fix:** Replace with fs.rm()
**Effort:** 30 minutes
**Risk:** Low (drop-in replacement)

### Medium Impact (Deprecation Warnings)

#### 4. Legacy Crypto Usage

**Files Affected:** 1

- lib/crypto.js

**Issue:** Uses soft-deprecated crypto method
**Fix:** Update to modern crypto API
**Effort:** 2-3 hours
**Risk:** Low (warnings only, still works)

### Low Impact (Configuration Only)

#### 5. Version Metadata

**Files Affected:** 3

- package.json (engines field)
- .nvmrc
- Dockerfile

**Issue:** Version numbers reference Node 18
**Fix:** Update to Node 20.x
**Effort:** 15 minutes
**Risk:** None

### Dependencies Impact

**package.json analysis:**

- **Total dependencies:** 42
- **Potentially incompatible:** 2
  - `node-fetch` v2.x (no longer needed, fetch is built-in)
  - `dotenv` v16.x (can use --env-file flag instead)
- **Upgrade recommended:** 5 packages have updates
```

### 5. Estimate Migration Effort

**Breakdown by task:**

```markdown
## Effort Estimation

### Development Tasks

| Task               | Description                              | Hours | Complexity | Risk   |
| ------------------ | ---------------------------------------- | ----- | ---------- | ------ |
| Code Analysis      | Review all affected files                | 2     | Low        | Low    |
| Import Syntax      | Update assert → with (3 files)           | 1     | Low        | Low    |
| DNS Testing        | Test DNS behavior, add options if needed | 4     | Medium     | Medium |
| fs API Update      | Replace rmdir with rm                    | 0.5   | Low        | Low    |
| Crypto Update      | Modernize crypto code                    | 2     | Low        | Low    |
| Dependency Cleanup | Remove node-fetch, update deps           | 1     | Low        | Low    |

**Subtotal Development:** 10.5 hours

### Testing Tasks

| Task                | Description                   | Hours | Complexity | Risk   |
| ------------------- | ----------------------------- | ----- | ---------- | ------ |
| Unit Tests          | Run existing test suite       | 1     | Low        | Low    |
| Integration Tests   | Test API and network features | 2     | Medium     | Medium |
| Manual Testing      | Test critical paths           | 1     | Low        | Low    |
| Performance Testing | Ensure no regressions         | 1     | Low        | Low    |

**Subtotal Testing:** 5 hours

### Documentation Tasks

| Task                   | Description               | Hours | Complexity | Risk |
| ---------------------- | ------------------------- | ----- | ---------- | ---- |
| Update README          | Node version requirements | 0.5   | Low        | Low  |
| Update CHANGELOG       | Document migration        | 0.5   | Low        | Low  |
| Update Deployment Docs | CI/CD changes             | 1     | Low        | Low  |

**Subtotal Documentation:** 2 hours

### Total Effort Estimate

**Optimistic (all goes well):** 14 hours (1.75 days)
**Realistic (some issues):** 17.5 hours (2.2 days)
**Pessimistic (complications):** 24 hours (3 days)

**Recommended Timeline:** Allocate 3 days with buffer for testing
```

### 6. Create Prioritized Migration Checklist

**Ordered by dependency and risk:**

```markdown
## Migration Checklist (Prioritized)

### Phase 1: Preparation (Day 1 Morning)

- [ ] **P0:** Create backup of current stable codebase
- [ ] **P0:** Create migration branch: `feature/node-20-migration`
- [ ] **P0:** Install Node 20.x locally
- [ ] **P1:** Review full Node 20 changelog
- [ ] **P1:** Communicate migration plan to team

### Phase 2: Configuration Updates (Day 1 Afternoon)

- [ ] **P0:** Update package.json engines: `"node": ">=20.6.0"`
- [ ] **P0:** Update .nvmrc: `20`
- [ ] **P1:** Update Dockerfile: `FROM node:20-alpine`
- [ ] **P1:** Update CI/CD workflow Node version
- [ ] **P2:** Update README with new Node requirement

### Phase 3: Code Changes (Day 1-2)

- [ ] **P0:** Fix import assertions → attributes (3 files)
  - [ ] src/config/loader.js
  - [ ] src/utils/parser.js
  - [ ] tests/fixtures/loader.test.js
- [ ] **P0:** Replace fs.rmdir with fs.rm (src/utils/cleanup.js)
- [ ] **P1:** Review DNS code and test (src/services/api-client.js, src/utils/network.js)
- [ ] **P2:** Update crypto code (lib/crypto.js)
- [ ] **P2:** Remove node-fetch dependency (use built-in fetch)

### Phase 4: Dependency Updates (Day 2)

- [ ] **P1:** Run `npm outdated` to check for updates
- [ ] **P1:** Update compatible dependencies
- [ ] **P1:** Test after each dependency update
- [ ] **P2:** Consider removing dotenv (use --env-file)

### Phase 5: Testing (Day 2-3)

- [ ] **P0:** Run unit test suite: `npm test`
- [ ] **P0:** Fix any failing tests
- [ ] **P0:** Run integration tests
- [ ] **P1:** Manual testing of critical features
- [ ] **P1:** Test DNS-dependent features specifically
- [ ] **P2:** Performance testing and comparison
- [ ] **P2:** Test on multiple platforms (Linux, macOS, Windows)

### Phase 6: Validation (Day 3)

- [ ] **P0:** Code review with team
- [ ] **P0:** Run full test suite on CI/CD
- [ ] **P1:** Deploy to staging environment
- [ ] **P1:** Run smoke tests on staging
- [ ] **P2:** Run execute-checklist.md with version-update-checklist.md

### Phase 7: Deployment (After validation)

- [ ] **P0:** Merge to main branch
- [ ] **P0:** Tag release
- [ ] **P1:** Deploy to production (with rollback plan)
- [ ] **P1:** Monitor for issues (24-48 hours)
- [ ] **P2:** Update team documentation
- [ ] **P2:** Announce completion

Priority Legend:

- P0: Critical (must complete before next phase)
- P1: Important (should complete, minor flexibility)
- P2: Nice-to-have (can defer if needed)
```

### 7. Document Required Code Changes

**Provide exact fix examples:**

````markdown
## Required Code Changes

### Change 1: Import Assertions → Import Attributes

**Location:** 3 files (loader.js, parser.js, loader.test.js)

**Before (Node 18):**

```javascript
import data from './data.json' assert { type: 'json' };
import config from './config.json' assert { type: 'json' };
```
````

**After (Node 20):**

```javascript
import data from './data.json' with { type: 'json' };
import config from './config.json' with { type: 'json' };
```

**Find & Replace:**

- Find: `assert { type: 'json' }`
- Replace: `with { type: 'json' }`

### Change 2: fs.rmdir → fs.rm

**Location:** src/utils/cleanup.js:45

**Before:**

```javascript
const fs = require('fs');

function cleanup(directory) {
  fs.rmdirSync(directory, { recursive: true });
}
```

**After:**

```javascript
const fs = require('fs');

function cleanup(directory) {
  fs.rmSync(directory, { recursive: true, force: true });
}
```

**Notes:**

- `fs.rm()` is the replacement for `fs.rmdir({ recursive: true })`
- Added `force: true` to suppress errors if directory doesn't exist
- Async version: `fs.rm()` instead of `fs.rmdir()`

### Change 3: DNS Resolution Behavior

**Location:** src/services/api-client.js:23

**Before (Node 18 - implicit ipv4first):**

```javascript
dns.lookup('example.com', (err, address) => {
  console.log(address); // IPv4 preferred
});
```

**After (Node 20 - explicit if old behavior needed):**

```javascript
dns.lookup('example.com', { verbatim: false }, (err, address) => {
  console.log(address); // IPv4 preferred (same as Node 18)
});
```

**Or accept new behavior:**

```javascript
dns.lookup('example.com', (err, address) => {
  console.log(address); // Uses DNS order (new default)
});
```

**Testing required:** Verify application behavior with both approaches

### Change 4: Remove node-fetch Dependency

**Location:** Multiple files using fetch

**Before:**

```javascript
const fetch = require('node-fetch');

async function getUser(id) {
  const response = await fetch(`https://api.example.com/users/${id}`);
  return response.json();
}
```

**After:**

```javascript
// No import needed - fetch is global in Node 18+

async function getUser(id) {
  const response = await fetch(`https://api.example.com/users/${id}`);
  return response.json();
}
```

**Cleanup:**

```bash
npm uninstall node-fetch
```

**Update package.json:**
Remove `"node-fetch": "^2.6.7"` from dependencies

````

### 8. Identify Testing Requirements

**Define what to test:**

```markdown
## Testing Requirements

### Unit Tests
- [ ] Run full test suite: `npm test`
- [ ] Verify all existing tests pass
- [ ] Test coverage remains >80%

### Integration Tests
- [ ] API endpoints function correctly
- [ ] Database connections work
- [ ] External service integrations work
- [ ] Authentication flow works

### Specific Feature Tests

#### DNS Resolution Testing
```bash
# Test with new default (verbatim)
node --eval "require('dns').lookup('example.com', console.log)"

# Test with old behavior (ipv4first)
node --eval "require('dns').lookup('example.com', {verbatim:false}, console.log)"
````

#### Import Attributes Testing

- [ ] All JSON imports load correctly
- [ ] No syntax errors in import statements
- [ ] Module resolution works in all environments

#### File System Testing

- [ ] Directory cleanup works (fs.rm)
- [ ] No errors when directory doesn't exist
- [ ] Recursive deletion functions correctly

### Performance Testing

- [ ] Application startup time
- [ ] API response times
- [ ] Memory usage comparison
- [ ] Build time comparison

### Regression Testing

- [ ] Test critical user paths
- [ ] Test error handling
- [ ] Test edge cases
- [ ] Test on production-like data

### Platform Testing

- [ ] Test on Linux (CI/CD)
- [ ] Test on macOS (development)
- [ ] Test on Windows (if supported)

````

## Success Criteria

Impact assessment is complete when:

- [ ] All breaking changes identified from changelog
- [ ] Codebase scanned for affected patterns
- [ ] Impact report generated with affected files
- [ ] Migration effort estimated (hours and complexity)
- [ ] Prioritized migration checklist created
- [ ] Exact code changes documented with examples
- [ ] Testing requirements defined
- [ ] Risk level assessed (low/medium/high)
- [ ] Timeline recommended
- [ ] Team informed of migration plan

## Output Format

```markdown
# Version Migration Impact Assessment

## Migration Summary

- **From Version:** [Current version]
- **To Version:** [Target version]
- **Affected Files:** [Count] out of [Total] ([Percentage]%)
- **Critical Issues:** [Count]
- **Estimated Effort:** [Range] hours ([Days] days)
- **Risk Level:** [Low/Medium/High]
- **Recommended Timeline:** [Timeframe]

## Breaking Changes

[List from changelog with impact]

## Affected Files Report

### Critical Impact
[Files that will break]

### Medium Impact
[Files with deprecation warnings]

### Low Impact
[Configuration files only]

## Effort Estimate

[Table with tasks, hours, complexity, risk]

## Migration Checklist

[Prioritized checklist by phase]

## Required Code Changes

### Change 1: [Description]
**Location:** [Files]
**Before:** [Code example]
**After:** [Code example]

[Repeat for all changes]

## Testing Requirements

[Detailed testing plan]

## Risk Assessment

[Potential issues and mitigation]

## Rollback Plan

[How to revert if migration fails]

## Resources

- Changelog: [URL]
- Migration Guide: [URL]
- Breaking Changes: [URL]
````

## Common Pitfalls to Avoid

**❌ Skipping changelog review:**

- Missing critical breaking changes
- Incomplete migration

✅ **Read full changelog:**

- Review all sections
- Check "breaking changes" specifically

**❌ Not testing DNS behavior:**

- Assuming network code will work the same

✅ **Test network features explicitly:**

- Verify DNS resolution
- Test with different network conditions

**❌ Underestimating effort:**

- Allocating insufficient time for testing

✅ **Add buffer for testing:**

- Plan for 30-50% of time on validation

**❌ No rollback plan:**

- Getting stuck if migration fails

✅ **Prepare rollback:**

- Keep old version deployable
- Document revert steps

## Next Steps

After assessing impact:

1. Present findings to team/stakeholders
2. Get approval for migration timeline
3. Use `update-dependencies.md` for package updates
4. Execute migration checklist
5. Run `execute-checklist.md` with `version-update-checklist.md`
6. Monitor post-migration for issues
7. Document lessons learned
