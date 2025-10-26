<!-- Powered by BMAD™ Core -->

# Organize Code Repository

---

task:
id: organize-code-repo
name: Organize Code Repository
description: Create a well-structured code repository with clear organization, documentation, and professional presentation
persona_default: sample-code-maintainer
inputs:

- code-files (list of code files to organize)
- organization-strategy (by-chapter, by-topic, by-feature, monorepo)
- repo-name (name for the repository)
  steps:
- Analyze code files and determine optimal structure
- Create folder hierarchy based on strategy
- Organize code files into appropriate folders
- Create README.md for repository root
- Create README.md files for each major folder
- Add .gitignore for language-specific artifacts
- Create LICENSE file
- Add CONTRIBUTING.md guidelines
- Create example .env.example if needed
- Validate structure meets quality standards
  output: Organized repository structure with documentation files

---

## Purpose

Organize code samples into a professional, easy-to-navigate repository structure that helps readers find and understand code examples.

## Organization Strategies

### By Chapter (Book Code Samples)

```
book-code-samples/
├── chapter-01-introduction/
│   ├── README.md
│   ├── hello-world.js
│   └── setup-verification.js
├── chapter-02-basics/
│   ├── README.md
│   ├── variables.js
│   └── functions.js
├── chapter-03-advanced/
│   ├── README.md
│   ├── async-patterns.js
│   └── error-handling.js
└── README.md
```

### By Topic (Tutorial Series)

```
react-tutorial/
├── components/
│   ├── README.md
│   ├── Button.jsx
│   └── Card.jsx
├── hooks/
│   ├── README.md
│   ├── useState-example.jsx
│   └── useEffect-example.jsx
├── routing/
│   ├── README.md
│   └── Router.jsx
└── README.md
```

### Monorepo (Multiple Projects)

```
fullstack-examples/
├── frontend/
│   ├── package.json
│   ├── src/
│   └── README.md
├── backend/
│   ├── package.json
│   ├── src/
│   └── README.md
├── shared/
│   └── types/
└── README.md
```

## Workflow Steps

### 1. Analyze and Plan Structure

- Review all code files
- Group by logical category (chapter, feature, topic)
- Plan folder hierarchy (max 3 levels deep)

### 2. Create Folder Structure

```bash
mkdir -p chapter-{01..10}
mkdir -p {tests,docs,assets}
```

### 3. Move Files into Structure

```bash
mv hello-world.js chapter-01/
mv api-client.js chapter-05/
```

### 4. Create Root README.md

Include:

- Project description
- Prerequisites
- Installation instructions
- Folder structure overview
- How to run examples
- License info

### 5. Create Folder READMEs

For each major folder:

- What this folder contains
- How to run code in this folder
- Key concepts demonstrated

### 6. Add .gitignore

```
node_modules/
.env
dist/
*.log
.DS_Store
```

### 7. Add LICENSE

Common choices:

- MIT (permissive)
- Apache 2.0 (patent protection)
- GPL (copyleft)

### 8. Run Quality Checklist

- [ ] Logical folder names
- [ ] Consistent naming convention
- [ ] READMEs for all major folders
- [ ] .gitignore present
- [ ] LICENSE file included
- [ ] No sensitive data committed

## Success Criteria

- [ ] Clear, logical folder structure
- [ ] All code files organized
- [ ] Root README with overview
- [ ] Folder READMEs where needed
- [ ] .gitignore appropriate for language
- [ ] LICENSE file present
- [ ] Easy to navigate and understand
