<!-- Powered by BMAD™ Core -->

# Security Audit

---

task:
id: security-audit
name: Security Audit
description: Perform comprehensive security audit on code examples to identify vulnerabilities and security issues
persona_default: code-curator
inputs: - code_path - language - security_standards
steps: - Identify target code files and language - Set up security scanning tools for the language - Run automated security scanners - Perform manual security code review - Review against security-best-practices-checklist.md - Identify vulnerabilities with severity levels - Document findings with remediation guidance - Generate security audit report
output: docs/security/security-audit-report.md

---

## Purpose

This task guides you through performing a comprehensive security audit of code examples to identify vulnerabilities, security anti-patterns, and risks. Technical books must demonstrate secure coding practices, so thorough security review is critical.

## Prerequisites

Before starting this task:

- Code examples have been created and are working
- Target programming language(s) identified
- Security scanning tools available for target language(s)
- Access to security-best-practices-checklist.md
- Understanding of OWASP Top 10 and common vulnerabilities

## Workflow Steps

### 1. Identify Code Scope and Language

Define what will be audited:

**Code Inventory:**

- List all code files to audit
- Identify programming language(s) and frameworks
- Note any third-party dependencies
- Identify code that handles sensitive data
- Flag code with authentication/authorization
- Identify code with user input handling

**Risk Assessment:**

- High risk: Authentication, authorization, data storage, user input
- Medium risk: API calls, file operations, database queries
- Low risk: Pure logic, calculations, data transformations

### 2. Set Up Security Scanning Tools

Install appropriate tools for the language:

**JavaScript/Node.js:**

```bash
# Install npm audit (built-in)
npm audit

# Install eslint-plugin-security
npm install --save-dev eslint-plugin-security

# Install OWASP Dependency-Check
npm install -g retire.js
```

**Python:**

```bash
# Install Bandit (security linter)
pip install bandit

# Install Safety (dependency checker)
pip install safety

# Install Semgrep (pattern-based scanner)
pip install semgrep
```

**Ruby:**

```bash
# Install Brakeman (Rails security scanner)
gem install brakeman

# Install bundler-audit (dependency checker)
gem install bundler-audit
```

**Go:**

```bash
# Install gosec (security scanner)
go install github.com/securego/gosec/v2/cmd/gosec@latest

# Install Nancy (dependency checker)
go install github.com/sonatype-nexus-community/nancy@latest
```

**Java:**

```bash
# Install SpotBugs with FindSecBugs plugin
# Add to Maven pom.xml or Gradle build.gradle

# Use OWASP Dependency-Check
# https://jeremylong.github.io/DependencyCheck/
```

**C#:**

```bash
# Install Security Code Scan
dotnet tool install --global security-scan

# Use built-in analyzers
dotnet add package Microsoft.CodeAnalysis.NetAnalyzers
```

**Rust:**

```bash
# Use cargo-audit (dependency checker)
cargo install cargo-audit

# Use clippy with security lints
rustup component add clippy
```

### 3. Run Automated Security Scanners

Execute automated tools:

**Step 1: Dependency Vulnerability Scanning**

Check for known vulnerabilities in dependencies:

```bash
# Node.js
npm audit
retire --path ./

# Python
safety check
pip-audit

# Ruby
bundle-audit check --update

# Go
nancy sleuth

# Rust
cargo audit
```

**Step 2: Static Code Analysis**

Scan code for security issues:

```bash
# Node.js
eslint --plugin security .
npm run lint:security  # if configured

# Python
bandit -r ./src
semgrep --config=auto .

# Ruby
brakeman --path .

# Go
gosec ./...

# Java
# Run SpotBugs/FindSecBugs in Maven/Gradle

# C#
security-scan analyze

# Rust
cargo clippy -- -W clippy::all
```

**Step 3: Document Scanner Output**

Capture all findings:

- Save scanner output to files
- Note severity levels from tools
- Identify false positives
- Prioritize findings for review

### 4. Perform Manual Security Review

Conduct manual code review using security-best-practices-checklist.md:

#### Credential Security Review

- [ ] Search for hardcoded secrets: `grep -r "password\|api_key\|secret\|token" --include=*.{js,py,rb,go,java,cs,rs}`
- [ ] Verify environment variables used for sensitive config
- [ ] Check no credentials in code comments or logs
- [ ] Verify secure credential storage patterns
- [ ] Check for exposed API keys in client-side code

#### Input Validation Review

- [ ] Identify all user input points
- [ ] Verify input validation exists
- [ ] Check type checking and sanitization
- [ ] Verify length limits enforced
- [ ] Check regex patterns are safe (no ReDoS vulnerabilities)
- [ ] Verify file upload restrictions

#### Injection Prevention Review

- [ ] Check SQL queries use parameterization (no string concat)
- [ ] Verify ORM usage is safe
- [ ] Check for XSS vulnerabilities in output
- [ ] Verify command execution is safe (no shell injection)
- [ ] Check LDAP queries are parameterized
- [ ] Verify XML parsing is secure (XXE prevention)

#### Authentication & Authorization Review

- [ ] Verify secure password hashing (bcrypt, Argon2, PBKDF2)
- [ ] Check password storage never plaintext
- [ ] Verify session management is secure
- [ ] Check JWT secrets properly managed
- [ ] Verify authorization checks on protected resources
- [ ] Check for broken authentication patterns
- [ ] Verify MFA patterns if demonstrated

#### Cryptography Review

- [ ] No use of MD5/SHA1 for security purposes
- [ ] Verify secure random number generation
- [ ] Check TLS/HTTPS recommended
- [ ] Verify certificate validation not disabled
- [ ] Check appropriate key lengths used
- [ ] Verify no custom crypto implementations

#### Data Protection Review

- [ ] Check sensitive data handling
- [ ] Verify no passwords/secrets in logs
- [ ] Check PII protection measures
- [ ] Verify data encryption where needed
- [ ] Check secure data transmission patterns

#### Error Handling Review

- [ ] Verify no sensitive data in error messages
- [ ] Check stack traces not exposed in production
- [ ] Verify appropriate error logging
- [ ] Check security events logged for audit

#### Dependency Security Review

- [ ] Check all dependencies are necessary
- [ ] Verify no known vulnerable packages
- [ ] Check version pinning strategy
- [ ] Verify dependency update recommendations

### 5. Classify Vulnerabilities by Severity

Rate each finding:

**CRITICAL** (Fix immediately, do not publish):

- Remote code execution vulnerabilities
- SQL injection vulnerabilities
- Authentication bypass
- Hardcoded credentials in published code
- Cryptographic failures exposing sensitive data

**HIGH** (Fix before publication):

- XSS vulnerabilities
- Insecure deserialization
- Security misconfiguration
- Known vulnerable dependencies
- Broken authorization

**MEDIUM** (Fix recommended):

- Information disclosure
- Insufficient logging
- Weak cryptography
- Missing security headers
- Non-critical dependency issues

**LOW** (Consider fixing):

- Security best practice violations
- Code quality issues with security implications
- Minor information leaks
- Documentation gaps

### 6. Document Findings with Remediation

For each vulnerability found, document:

**Vulnerability Record:**

````markdown
### [SEVERITY] Vulnerability Title

**Location:** file_path:line_number

**Description:**
Clear explanation of the vulnerability.

**Risk:**
What could an attacker do? What data/systems are at risk?

**Evidence:**

```code
// Vulnerable code snippet
```
````

**Remediation:**

```code
// Secure code example
```

**References:**

- CWE-XXX: Link to Common Weakness Enumeration
- OWASP reference if applicable
- Language-specific security guidance

**Status:** Open | Fixed | False Positive | Accepted Risk

````

### 7. Run Security-Best-Practices Checklist

Execute execute-checklist.md task with security-best-practices-checklist.md:

- Systematically verify each checklist item
- Cross-reference with manual review findings
- Document any gaps or additional issues
- Ensure comprehensive coverage

### 8. Generate Security Audit Report

Create comprehensive report:

**Report Structure:**

```markdown
# Security Audit Report

**Date:** YYYY-MM-DD
**Auditor:** [Name/Team]
**Code Version:** [Commit hash or version]
**Languages:** [JavaScript, Python, etc.]

## Executive Summary

- Total vulnerabilities found: X
- Critical: X | High: X | Medium: X | Low: X
- Must fix before publication: X issues
- Overall risk assessment: [Low/Medium/High]

## Audit Scope

- Files audited: [List]
- Tools used: [Scanner list]
- Manual review completed: [Yes/No]
- Checklist completed: [Yes/No]

## Findings Summary

### Critical Issues (X found)
1. [Issue title] - file:line
2. ...

### High Priority Issues (X found)
1. [Issue title] - file:line
2. ...

### Medium Priority Issues (X found)
[Summarized list]

### Low Priority Issues (X found)
[Summarized list]

## Detailed Findings

[Use Vulnerability Record format for each finding]

## Positive Security Practices

[Note good security patterns found in code]

## Recommendations

1. **Immediate actions** (Critical/High issues)
2. **Before publication** (Medium issues)
3. **Future improvements** (Low issues, best practices)

## Tools Output

### Dependency Scan Results
[Tool output or summary]

### Static Analysis Results
[Tool output or summary]

## Checklist Results

[Reference to security-best-practices-checklist.md completion]

## Sign-off

- [ ] All Critical issues resolved
- [ ] All High issues resolved or documented as exceptions
- [ ] Code examples safe for publication
- [ ] Security review complete

**Auditor Signature:** _____________
**Date:** _____________
````

### 9. Troubleshooting Common Issues

**False Positives:**

- Automated scanners may flag safe code
- Document why flagged code is actually safe
- Update scanner configuration if possible
- Add code comments explaining safety

**Tool Installation Issues:**

- Check language/runtime version compatibility
- Use virtual environments/containers
- Refer to tool documentation
- Try alternative tools if installation fails

**No Baseline for Comparison:**

- On first audit, everything is new
- Document current state as baseline
- Future audits compare against baseline
- Track security debt over time

**Dependency Conflicts:**

- Security scanner dependencies may conflict
- Use separate virtual environments per tool
- Consider containerized scanning approach
- Document any tool limitations

**Language-Specific Challenges:**

_JavaScript:_

- Large dependency trees create noise
- Focus on direct dependencies first
- Use `npm audit --production` for prod deps only

_Python:_

- Virtual environment setup crucial
- Bandit may have false positives on test code
- Use `# nosec` comments judiciously with explanation

_Ruby:_

- Brakeman is Rails-specific
- Use standard Ruby scanners for non-Rails code

_Go:_

- gosec sometimes flags safe uses of crypto/rand
- Review findings in context

_Java:_

- Tool configuration can be complex
- May need to adjust Maven/Gradle settings

### 10. Remediate and Retest

For each vulnerability:

**Remediation Process:**

1. Understand the vulnerability thoroughly
2. Research secure alternative approaches
3. Implement fix or update documentation
4. Test fix doesn't break functionality
5. Rerun security scan to verify fix
6. Update audit report status
7. Document fix in code comments if needed

**Verification:**

- Rerun all scanners after fixes
- Verify vulnerability no longer detected
- Check fix doesn't introduce new issues
- Update security audit report

## Success Criteria

A complete security audit has:

- [ ] All code files identified and scanned
- [ ] Automated security scanners run successfully
- [ ] Manual security review completed
- [ ] security-best-practices-checklist.md completed
- [ ] All findings documented with severity levels
- [ ] Remediation guidance provided for each issue
- [ ] Security audit report generated
- [ ] Critical and High issues resolved or documented
- [ ] Code safe for publication

## Common Pitfalls to Avoid

- **Relying only on automated tools**: Manual review is essential
- **Ignoring false positives**: Document why flagged code is safe
- **Not testing security fixes**: Ensure fixes work and don't break code
- **Missing dependency vulnerabilities**: Always check dependencies
- **Ignoring language-specific risks**: Each language has unique patterns
- **No severity classification**: Not all issues are equal
- **Poor documentation**: Future reviewers need context
- **Not updating checklists**: Security standards evolve
- **Publishing with critical issues**: Never acceptable
- **No retest after fixes**: Verify remediation worked

## Security Testing by Language

### JavaScript/Node.js

**Common Vulnerabilities:**

- Prototype pollution
- Regular expression DoS (ReDoS)
- Unsafe eval() usage
- XSS in templating
- Dependency vulnerabilities (large trees)

**Tools:**

- npm audit
- eslint-plugin-security
- retire.js
- NodeJsScan

### Python

**Common Vulnerabilities:**

- SQL injection (string formatting)
- Pickle deserialization
- YAML deserialization (yaml.load)
- Path traversal
- Command injection (subprocess)

**Tools:**

- Bandit
- Safety
- Semgrep
- pip-audit

### Ruby/Rails

**Common Vulnerabilities:**

- Mass assignment
- SQL injection
- XSS in ERB templates
- YAML deserialization
- Command injection

**Tools:**

- Brakeman
- bundler-audit
- RuboCop with security cops

### Go

**Common Vulnerabilities:**

- SQL injection
- Command injection
- Path traversal
- Unsafe reflection
- Integer overflow

**Tools:**

- gosec
- Nancy (dependencies)
- go vet
- staticcheck

### Java

**Common Vulnerabilities:**

- Deserialization attacks
- XXE in XML parsing
- SQL injection
- Path traversal
- Weak cryptography

**Tools:**

- SpotBugs + FindSecBugs
- OWASP Dependency-Check
- SonarQube
- Checkmarx

### C#/.NET

**Common Vulnerabilities:**

- SQL injection
- XSS
- Deserialization
- Path traversal
- Weak encryption

**Tools:**

- Security Code Scan
- Microsoft analyzers
- OWASP Dependency-Check
- SonarQube

### Rust

**Common Vulnerabilities:**

- Unsafe code blocks
- Integer overflow (unchecked)
- Dependency vulnerabilities
- Concurrent access issues

**Tools:**

- cargo-audit
- cargo-clippy
- cargo-geiger (unsafe usage detection)

## Next Steps

After security audit is complete:

1. **Remediate findings**: Fix all Critical and High issues
2. **Update documentation**: Add security notes to code examples
3. **Create security guide**: Document security patterns for readers
4. **Set up CI/CD security scanning**: Automate future scans
5. **Schedule regular audits**: Security is ongoing
6. **Update code examples**: Ensure all show secure patterns
7. **Review with technical reviewer**: Get second opinion on findings
8. **Document security decisions**: Explain security choices in book

## Reference Resources

**OWASP Resources:**

- OWASP Top 10: https://owasp.org/Top10/
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/

**CWE (Common Weakness Enumeration):**

- CWE Top 25: https://cwe.mitre.org/top25/

**Language-Specific Security:**

- Node.js Security Best Practices: https://nodejs.org/en/docs/guides/security/
- Python Security: https://python.readthedocs.io/en/stable/library/security_warnings.html
- Go Security: https://go.dev/doc/security/
- Rust Security: https://doc.rust-lang.org/nomicon/
