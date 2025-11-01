# Repository Integration Checklist

Use this checklist when integrating a code repository with a book chapter for Manning MEAP or similar early-access programs. This checklist focuses on ensuring the repository is properly linked to the chapter and can be used independently by readers who may read chapters out of order.

**Purpose**: Validate that chapter code is properly set up in a repository, accessible to readers, and works independently without requiring previous chapters' code.

**When to Use**: Before submitting a chapter to Manning MEAP or when adding a code repository link to any technical book chapter.

---

## Repository Organization

- [ ] Chapter code in dedicated folder with consistent naming (e.g., `chapter-05/`, `ch05/`, `05-chapter-name/`)
- [ ] Folder naming consistent with book's chapter numbering scheme
- [ ] Source code separated from {{config.manuscript.root}}/book files
- [ ] Code examples organized by section (if chapter has multiple major sections)
- [ ] No build artifacts committed (`node_modules/`, `__pycache__/`, `*.class`, `target/`, `dist/`, etc.)
- [ ] No IDE-specific files committed (`.vscode/`, `.idea/`, `.vs/`, etc.)
- [ ] Clear separation between chapter code and shared/common utilities (if any)
- [ ] `.gitignore` properly configured for the programming language used

## README.md Completeness

- [ ] README.md present in chapter folder
- [ ] Project title clearly states chapter number and topic
- [ ] Brief description of what the code demonstrates
- [ ] Prerequisites explicitly listed (language version, required tools, OS requirements)
- [ ] Step-by-step installation instructions (from clone to ready-to-run)
- [ ] How to run each code example with exact commands
- [ ] Expected output documented (what reader should see when running code)
- [ ] Troubleshooting section for common issues (installation, runtime, platform-specific)
- [ ] Link back to book/chapter
- [ ] License information clearly stated
- [ ] README assumes reader may not have read previous chapters (MEAP-specific)

## Dependency Documentation

- [ ] Dependency file present (language-appropriate: `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, `pom.xml`, etc.)
- [ ] All dependencies with specific versions or version ranges
- [ ] Lock file included for reproducibility (`package-lock.json`, `Pipfile.lock`, `Gemfile.lock`, `go.sum`, etc.)
- [ ] No known security vulnerabilities (run `npm audit`, `pip check`, `bundle audit`, etc.)
- [ ] Dependencies match exactly what's used in chapter examples
- [ ] Development dependencies separated from runtime dependencies (if applicable)
- [ ] Dependency installation instructions included in README

## Test Coverage

- [ ] Tests included for all major code examples
- [ ] Test runner documented in README with exact commands
- [ ] All tests passing (verified before chapter submission)
- [ ] Test output matches what's documented in README
- [ ] Basic edge cases covered (empty input, error conditions, boundary cases)
- [ ] Tests are self-contained (don't depend on other chapters' code)
- [ ] Test dependencies included in dependency file
- [ ] Instructions for interpreting test results provided

## Repository Linking

- [ ] Repository link added to chapter introduction (visible to readers early)
- [ ] Link format follows publisher guidelines (check Manning/publisher style guide)
- [ ] Link tested and accessible (repository is public or accessible to readers)
- [ ] Direct link to chapter folder provided (e.g., `github.com/username/repo/tree/main/chapter-05`)
- [ ] Commit hash or tag referenced for version-specific code (e.g., `v1.0-chapter-05`, `meap-ch05`)
- [ ] License clearly stated in repository
- [ ] Repository name is professional and discoverable
- [ ] Repository description accurately reflects book/chapter content

## Code Independence

- [ ] Code runs without any code from other chapters
- [ ] No imports or references to other chapter directories
- [ ] No hard-coded absolute paths (use relative paths or environment variables)
- [ ] Cross-platform compatible (Windows/macOS/Linux) or platform requirements documented
- [ ] All required data files included in chapter folder
- [ ] Configuration files or examples provided (no external config dependencies)
- [ ] Self-contained: `git clone` → install dependencies → run = works
- [ ] No assumptions about reader's prior code setup or environment
- [ ] Code works independently even if reader skipped earlier chapters

## Integration Validation

- [ ] **Fresh Environment Test**: Clone repository in fresh directory and follow README instructions
- [ ] **Dependency Installation**: Verify all dependencies install without errors
- [ ] **Code Execution**: Run all code examples and verify expected output
- [ ] **Test Execution**: Run test suite and verify all tests pass
- [ ] **Link Verification**: Click repository link in chapter and verify it goes to correct folder
- [ ] **Reader Perspective**: Can someone unfamiliar with the project get code running from README alone?
- [ ] **Cross-Reference**: Code in repository matches code shown in chapter text
- [ ] **Version Sync**: Repository state matches chapter version (no ahead/behind mismatches)

## Manning MEAP Specific

- [ ] Repository organized by chapter (MEAP releases chapters incrementally)
- [ ] Each chapter folder is standalone (readers may skip chapters)
- [ ] README doesn't assume previous chapters were read
- [ ] Code examples work without prior chapter context
- [ ] Repository link in chapter front matter or introduction
- [ ] Code quality suitable for publication (not draft/placeholder code)
- [ ] Repository prepared for reader feedback and potential updates

---

## Post-Integration

- [ ] Repository synchronized with chapter revisions (if chapter updated based on feedback)
- [ ] Known issues documented in README or GitHub Issues
- [ ] Plan for maintaining repository if dependencies/frameworks update
- [ ] Author has verified repository is accessible and functional
