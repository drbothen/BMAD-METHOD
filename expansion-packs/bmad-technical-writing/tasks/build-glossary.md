<!-- Powered by BMAD™ Core -->

# Build Glossary

---

task:
id: build-glossary
name: Build Glossary
description: Compile comprehensive glossary of technical terms with clear definitions
persona_default: api-documenter
inputs: - chapter-content or full manuscript - existing-glossary (if updating)
steps: - Extract technical terms from all chapters - Define each term clearly and concisely - Provide context where term is used - Add cross-references to related terms - Organize alphabetically - Verify accuracy of definitions - Check for consistency across book - Add first-use markers if required by publisher - Format per publisher requirements - Review for completeness - Run execute-checklist.md with glossary-accuracy-checklist.md
output: docs/glossary.md or Appendix: Glossary

---

## Purpose

This task guides you through creating a comprehensive, accurate glossary that helps readers quickly look up technical terms and concepts. The result is a reference resource that improves book usability and reader comprehension.

## Prerequisites

Before starting this task:

- Have chapter content available
- Access to technical-writing-standards.md knowledge base
- Know publisher's glossary requirements
- Have list of domain-specific terminology

## Workflow Steps

### 1. Extract Technical Terms

Identify terms that need definitions:

**Include:**

- Domain-specific technical terms (API, microservice, container)
- Framework/library-specific terms (React hooks, Django ORM)
- Acronyms and abbreviations (REST, CRUD, JWT)
- Jargon that may be unfamiliar (idempotent, immutable, memoization)
- Concepts central to the book (dependency injection, event sourcing)
- Tool or product names (Docker, Kubernetes, PostgreSQL)

**Exclude:**

- Common programming terms (if, loop, function) unless domain uses them uniquely
- General English words
- Terms used only once and explained inline
- Obvious concepts for target audience

**Extraction methods:**

**Manual extraction:**

- Read through each chapter
- Note terms that might confuse readers
- Mark terms used across multiple chapters
- Identify inconsistent terminology

**Pattern search:**

- Search for capitalized terms
- Find acronyms (all-caps words)
- Look for italicized or bolded terms
- Check code comments for technical terms

**First-use indicators:**

- Many books mark first use of glossary terms
- Look for italic or parenthetical definitions
- Note chapter where term first appears

### 2. Define Each Term Clearly

Write precise, concise definitions:

**Format:**

**Term (Pronunciation if non-obvious)**
_Part of speech_

Clear, concise definition in 1-3 sentences. Focus on what the term means in the context of this book's domain.

**Example used in this book:** Brief example or usage context.

**See also:** Related terms

---

**Examples:**

**API (Application Programming Interface)**
_noun_

A set of rules and protocols that define how software components communicate with each other. APIs expose specific functionality while hiding implementation details, enabling developers to use services without understanding their internal workings.

**Example used in this book:** In Chapter 5, you built a RESTful API that exposes endpoints for creating and retrieving user data.

**See also:** RESTful API, endpoint, HTTP methods

---

**Idempotent**
_adjective (eye-dem-POH-tent)_

A property of an operation where performing it multiple times has the same effect as performing it once. Idempotent operations are crucial for building reliable distributed systems that can safely retry failed requests.

**Example used in this book:** The PUT and DELETE HTTP methods are idempotent - sending the same PUT request twice produces the same final state.

**See also:** HTTP methods, RESTful API, side effects

---

**Guidelines:**

- Define in plain language first, then technical precision
- Avoid circular definitions ("X is a type of X that...")
- Use analogies if helpful ("like a telephone switchboard")
- Specify the context (database context vs. general programming)
- Keep definitions under 100 words
- Write for target audience's level

**Good vs. Bad:**

- ✅ "A container bundles an application with its dependencies into an isolated environment"
- ❌ "Containerization technology" (defines nothing)
- ✅ "JWT (JSON Web Token) is a compact, URL-safe token format for transmitting authentication claims between parties"
- ❌ "JWT is used for auth" (too vague)

### 3. Provide Context and Usage

Show where/how the term appears:

**Chapter reference:**
"First introduced in Chapter 3: Database Design"

**Usage context:**
"Used throughout Part II when discussing asynchronous operations"

**Code example:**

```python
# Example of idempotent operation
PUT /users/123  # Updates user 123 to specific state
PUT /users/123  # Repeated request produces same result
```

**Practical scenario:**
"When debugging container networking issues (Chapter 7), you'll use these commands to inspect bridge networks."

**Why context matters:**

- Helps readers find where concept is explained
- Connects definition to practical use
- Provides memory aid for later recall

### 4. Add Cross-References

Link related terms:

**Format:**

**See also:** Related term 1, Related term 2, Related term 3

**Types of relationships:**

**Broader/narrower:**

- "See also: HTTP methods (broader concept), GET, POST (specific methods)"

**Related concepts:**

- "See also: authentication, authorization, session management"

**Alternatives or contrasts:**

- "See also: SQL (contrast with), relational database"

**Prerequisites:**

- "See also: function, scope (required understanding)"

**Cross-reference guidelines:**

- 2-5 related terms maximum
- Order by relevance
- Link terms actually in glossary
- Use consistent term naming

### 5. Organize Alphabetically

Structure for easy lookup:

**Format:**

```
# Glossary

## A

**API (Application Programming Interface)**
...

**Asynchronous**
...

## B

**Backend**
...

**Bearer Token**
...
```

**Alphabetization rules:**

- Ignore "A", "An", "The" prefixes
- Acronyms alphabetize as single words (API comes before Application)
- Case-insensitive sorting
- Numbers spell out (2FA becomes "Two-factor authentication")

**Symbols and numbers:**

- Create separate "Symbols" or "Numbers" section
- Or integrate: "@ (at sign)", "# (hashtag)"

### 6. Verify Accuracy of Definitions

Validate each definition:

- [ ] Is the definition factually correct?
- [ ] Does it match how the term is used in the book?
- [ ] Is it appropriate for target audience?
- [ ] Have I avoided circular definitions?
- [ ] Are acronyms expanded correctly?
- [ ] Are examples accurate?
- [ ] Have I cited sources for external definitions?

**Validation methods:**

- Cross-check with authoritative sources (official docs, RFCs, standards)
- Verify against book content usage
- Have subject matter expert review
- Test definitions with target audience

**Common errors to fix:**

- Outdated definitions (old version of technology)
- Too narrow (only covers one use case)
- Too broad (loses specific meaning)
- Inconsistent with book usage

### 7. Check for Consistency Across Book

Ensure uniform terminology:

**Consistency checks:**

**Spelling variations:**

- "email" vs. "e-mail"
- "login" vs. "log in" vs. "log-in"
- "setup" (noun) vs. "set up" (verb)

**Terminology:**

- "function" vs. "method" (be precise)
- "argument" vs. "parameter"
- "client" vs. "user" vs. "caller"

**Capitalization:**

- "Internet" vs. "internet"
- "Boolean" vs. "boolean"
- "Web" vs. "web"

**Hyphenation:**

- "multi-tenant" vs. "multitenant"
- "open-source" vs. "open source"

**Process:**

1. List all variants of term usage
2. Choose canonical form
3. Define in glossary
4. Note variants if common
5. Update book chapters for consistency

**Example entry:**
**Log in** (verb), **login** (noun/adjective)

_verb:_ To authenticate and access a system by providing credentials.

_noun/adjective:_ The process or screen for authentication (e.g., "login page").

**Note:** This book uses "log in" as two words for the verb ("users log in") and "login" as one word for the noun ("the login failed").

### 8. Add First-Use Markers

If required by publisher:

**Techniques:**

**In-text marker:**
First occurrence of term in chapter is italicized or bolded:

"The _application programming interface_ (API) defines..."

**Footnote reference:**
"The API³ defines..."
³ See glossary

**Parenthetical:**
"The API (see glossary) defines..."

**Publisher-specific requirements:**

- PacktPub: Italic on first use per chapter
- O'Reilly: Bold on first use, no special marker
- Manning: Italic with index entry
- Self-publish: Choose consistent approach

### 9. Format Per Publisher Requirements

Apply publisher formatting:

**Standard format:**

```markdown
# Glossary

**Term**
Definition text here.

**Another term**
Definition text here.
```

**With categorization (if required):**

```markdown
# Glossary

## Core Concepts

...

## Tools and Technologies

...

## HTTP and Networking

...
```

**With pronunciation (if needed):**

```markdown
**Kubernetes** (koo-ber-NET-eez)
```

**With etymology (optional):**

```markdown
**Idempotent** (from Latin _idem_ "same" + _potent_ "power")
```

**Publisher-specific:**

- Check style guide
- Follow existing book examples
- Match formatting conventions

### 10. Review for Completeness

Final validation:

- [ ] All chapter-specific terms included?
- [ ] All acronyms expanded?
- [ ] Cross-references accurate?
- [ ] Definitions clear and concise?
- [ ] Alphabetization correct?
- [ ] Consistent terminology throughout?
- [ ] Publisher requirements met?
- [ ] Target audience appropriate?

**Completeness check:**

- Read random chapter section
- Note unfamiliar terms
- Verify they're in glossary
- If not, add them

### 11. Run Glossary Accuracy Checklist

Validate using checklist:

- glossary-accuracy-checklist.md - Ensure all terms defined, accurate, and consistent

## Success Criteria

A completed glossary should have:

- [ ] All technical terms from book included
- [ ] Clear, concise definitions (1-3 sentences each)
- [ ] Usage context or examples provided
- [ ] Cross-references to related terms
- [ ] Alphabetical organization
- [ ] Definitions verified for accuracy
- [ ] Consistent terminology across book
- [ ] First-use markers (if required)
- [ ] Publisher formatting applied
- [ ] Glossary accuracy checklist passed

## Common Pitfalls to Avoid

- **Incomplete coverage**: Missing terms readers might not know
- **Circular definitions**: Defining term using itself
- **Too technical**: Definitions harder to understand than term
- **Inconsistent usage**: Term defined differently than used in book
- **Missing acronym expansions**: "JWT" without "JSON Web Token"
- **No context**: Definition without usage example
- **Outdated definitions**: Not reflecting current version of technology
- **Poor organization**: Difficult to find terms

## Notes and Warnings

- **Living document**: Update glossary as chapters evolve
- **Consistency is key**: Glossary should match book content exactly
- **Target audience matters**: Beginner book needs more terms defined
- **Cross-references add value**: Help readers understand relationships
- **Examples clarify**: Usage context makes definitions concrete
- **Verify accuracy**: Incorrect definitions erode trust
- **Publisher requirements**: Check style guide early

## Next Steps

After building glossary:

1. Review with technical editor for accuracy
2. Check consistency with main content
3. Add to appendix or back matter
4. Create index entries for glossary terms (if separate index exists)
5. Update as new terms added in revisions
6. Consider adding glossary terms to book index
