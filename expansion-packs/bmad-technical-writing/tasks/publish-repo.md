<!-- Powered by BMAD™ Core -->

# Publish Repository

---

task:
id: publish-repo
name: Publish Repository
description: Publish code repository to GitHub/GitLab with proper configuration and documentation
persona_default: sample-code-maintainer
inputs:
  - repo-path (local path to repository)
  - platform (github, gitlab, bitbucket)
  - visibility (public, private)
steps:
  - Initialize Git repository if not already initialized
  - Create .gitignore file
  - Make initial commit
  - Create remote repository on platform (GitHub/GitLab)
  - Add remote origin
  - Push to remote
  - Configure repository settings (description, topics, etc.)
  - Add CONTRIBUTING.md for collaboration guidelines
  - Enable issue templates (optional)
  - Enable discussions (optional)
output: Published repository URL with proper configuration

---

## Purpose

Publish code repository to hosting platform making it accessible to readers and contributors.

## Workflow Steps

### 1. Initialize Git Repository

```bash
cd /path/to/your/code
git init
```

### 2. Create .gitignore

```bash
# For Node.js
cat > .gitignore << 'IGNORE'
node_modules/
.env
.env.local
dist/
build/
*.log
.DS_Store
IGNORE
```

### 3. Make Initial Commit

```bash
git add .
git commit -m "Initial commit: book code samples"
```

### 4. Create Remote Repository

**GitHub (via CLI):**

```bash
# Install GitHub CLI if needed
brew install gh

# Authenticate
gh auth login

# Create repository
gh repo create my-book-code --public --source=. --remote=origin --push

# Or for private repo
gh repo create my-book-code --private --source=. --remote=origin --push
```

**GitHub (via web):**

1. Go to https://github.com/new
2. Enter repository name
3. Choose public/private
4. Don't initialize with README (already have one)
5. Click "Create repository"

### 5. Add Remote and Push

```bash
# Add remote (if not done via gh CLI)
git remote add origin https://github.com/username/my-book-code.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 6. Configure Repository Settings

**Description and Topics:**

```bash
# Via GitHub CLI
gh repo edit --description "Code samples for My Awesome Book" \
  --add-topic javascript \
  --add-topic tutorial \
  --add-topic book-code
```

**Via web:**

- Go to repository settings
- Add description: "Code samples for My Awesome Book"
- Add topics: javascript, tutorial, book-code, react
- Add website URL (book link if available)

### 7. Add CONTRIBUTING.md

```markdown
# Contributing

Thank you for your interest in contributing!

## Reporting Issues

- Check existing issues first
- Provide clear description and steps to reproduce
- Include relevant code samples

## Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b fix/issue-123`)
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass (`npm test`)
6. Commit changes (`git commit -m "fix: resolve issue 123"`)
7. Push to your fork (`git push origin fix/issue-123`)
8. Open a Pull Request

## Code Style

- Follow existing code style
- Run linter before committing (`npm run lint`)
- Use meaningful commit messages

## Questions?

Open an issue for questions or discussions.
```

### 8. Enable Issue Templates (Optional)

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug Report
about: Report a bug in the code samples
title: '[BUG] '
labels: bug
---

## Description

A clear description of the bug.

## Steps to Reproduce

1. Go to chapter X
2. Run code sample Y
3. See error

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened.

## Environment

- OS: [e.g., macOS, Windows, Linux]
- Node version: [e.g., 18.16.0]
- npm version: [e.g., 9.5.1]
```

### 9. Add Repository Badges to README

```markdown
# My Book Code Samples

![GitHub stars](https://img.shields.io/github/stars/username/repo?style=social)
![GitHub forks](https://img.shields.io/github/forks/username/repo?style=social)
![License](https://img.shields.io/github/license/username/repo)
![Test Status](https://github.com/username/repo/actions/workflows/test.yml/badge.svg)

Code samples for "My Awesome Book"...
```

### 10. Verify Publication

```bash
# Check repository is accessible
gh repo view username/my-book-code --web

# Or visit URL
open https://github.com/username/my-book-code
```

## Success Criteria

- [ ] Repository initialized and committed
- [ ] Remote repository created
- [ ] Code pushed successfully
- [ ] Description and topics configured
- [ ] README displays correctly
- [ ] CONTRIBUTING.md added
- [ ] Repository is accessible at URL
- [ ] All documentation files present

## Post-Publication Tasks

### Link from Book

Add repository URL to book:

```markdown
**Code Samples:** https://github.com/username/my-book-code
```

### Announce to Readers

- Tweet repository URL
- Add to book website
- Include in book introduction

### Monitor Repository

- Watch for issues
- Review pull requests
- Keep examples updated

## Security Considerations

**Before Publishing:**

- [ ] No API keys or secrets committed
- [ ] No passwords or tokens in code
- [ ] .env files in .gitignore
- [ ] No real user data
- [ ] Sample data only

**If Secrets Leaked:**

```bash
# Remove from history (use carefully)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret.env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (destructive)
git push origin --force --all

# Better: Rotate leaked secrets immediately
```
