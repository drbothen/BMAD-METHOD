# Repository Quality Checklist

Use this checklist to ensure your code repository is professional, organized, and user-friendly.

## Repository Basics

- [ ] Clear README.md in root directory
- [ ] Repository name descriptive and professional
- [ ] Description accurate in repository settings
- [ ] Topics/tags added for discoverability
- [ ] Repository is public (unless there's a reason for private)

## README.md Quality

- [ ] Title clearly states repository purpose
- [ ] "About This Repository" section explains context
- [ ] Prerequisites listed explicitly
- [ ] Installation instructions step-by-step
- [ ] Usage examples provided
- [ ] Links to book or related resources
- [ ] Repository structure explained
- [ ] Contact/support information included

## Folder Structure

- [ ] Logical organization (by chapter, topic, or feature)
- [ ] Consistent naming conventions (chapter-01, ch01, or 01-chapter-name)
- [ ] Each chapter/section has its own folder
- [ ] Separate folders for tests, docs, images (if applicable)
- [ ] No cluttered root directory

## Code Quality

- [ ] All code follows language-specific style guide
- [ ] Code is well-commented
- [ ] No commented-out code left in repository
- [ ] No debugging print statements left in code
- [ ] Code examples are self-contained and runnable
- [ ] Each example includes necessary imports/dependencies

## Dependencies

- [ ] Requirements file present (requirements.txt, package.json, Gemfile, etc.)
- [ ] Dependencies pinned to specific versions
- [ ] No unnecessary dependencies
- [ ] Instructions for installing dependencies in README
- [ ] Separate dev dependencies if applicable

## Documentation

- [ ] Each chapter folder has its own README (optional but helpful)
- [ ] Code examples explained in comments or accompanying markdown
- [ ] Expected output documented
- [ ] Common issues/troubleshooting noted
- [ ] API documentation if applicable

## Testing

- [ ] Unit tests included (if appropriate)
- [ ] Test instructions in README
- [ ] Tests pass before committing
- [ ] CI/CD set up to run tests automatically (optional)
- [ ] Test coverage reasonable for educational repository

## Git Hygiene

- [ ] .gitignore appropriate for language/framework
- [ ] No sensitive data committed (API keys, passwords, credentials)
- [ ] No large binary files (unless necessary)
- [ ] No IDE-specific files (.vscode/, .idea/ ignored)
- [ ] No OS-specific files (.DS_Store, Thumbs.db ignored)
- [ ] Commit messages are descriptive
- [ ] No merge conflict markers in code

## Licensing

- [ ] LICENSE file present
- [ ] License appropriate for educational code (MIT, Apache 2.0 common)
- [ ] License year and copyright holder correct
- [ ] License compatible with book's license

## Cross-Platform Support

- [ ] Code works on Windows, macOS, Linux (as applicable)
- [ ] File paths use cross-platform methods
- [ ] Installation instructions for all platforms
- [ ] Platform-specific issues documented

## Accessibility

- [ ] Code examples run out-of-the-box (no complex setup)
- [ ] Error messages are helpful
- [ ] Installation doesn't require expensive tools
- [ ] Alternative approaches provided if dependencies are heavy

## GitHub/GitLab Features

- [ ] Repository topics/tags set
- [ ] Issues enabled (if accepting feedback)
- [ ] Discussions enabled (if building community)
- [ ] Security policy (SECURITY.md) if applicable
- [ ] Contributing guidelines (CONTRIBUTING.md) if accepting PRs

## CI/CD (Optional but Recommended)

- [ ] GitHub Actions or equivalent set up
- [ ] Tests run automatically on push/PR
- [ ] Linting checks automated
- [ ] Build status badge in README
- [ ] Multi-platform testing (if applicable)

## Release Management

- [ ] Tagged releases for book versions (v1.0, v2.0, etc.)
- [ ] Release notes describing changes
- [ ] Stable branch for published version
- [ ] Development branch for updates (if applicable)

## Reader Experience

- [ ] Clone and run test: can a reader clone and run immediately?
- [ ] Instructions are clear to someone unfamiliar with the repository
- [ ] No "works on my machine" problems
- [ ] Examples produce expected output
- [ ] Repository organized logically from reader's perspective

## Maintenance

- [ ] Dependencies not outdated (security vulnerabilities)
- [ ] Deprecated features noted
- [ ] Updates planned for major language/framework changes
- [ ] Errata or known issues documented
- [ ] Responsive to issues and questions (if accepting them)

## Integration with Book

- [ ] Repository linked prominently in book's front matter
- [ ] Repository URL easy to type (short, memorable)
- [ ] Chapter code maps clearly to book chapters
- [ ] Repository supports book's learning objectives
- [ ] Code in repository matches code in book (or noted if intentionally different)
