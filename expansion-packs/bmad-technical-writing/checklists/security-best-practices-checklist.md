# Security Best Practices Checklist

Use this checklist to ensure code examples and recommendations follow security best practices.

## Credential Security

- [ ] No hardcoded passwords or API keys in code examples
- [ ] Environment variables or configuration files used for secrets
- [ ] Credential management best practices demonstrated
- [ ] Examples show proper secret rotation patterns
- [ ] No credentials in version control examples

## Input Validation

- [ ] Input validation demonstrated in user-facing code
- [ ] Type checking shown where applicable
- [ ] Length limits enforced on user inputs
- [ ] Regex patterns used safely
- [ ] Sanitization techniques explained

## Injection Prevention

- [ ] SQL injection prevention shown (parameterized queries, ORMs)
- [ ] No string concatenation for SQL queries
- [ ] XSS (Cross-Site Scripting) prevention demonstrated
- [ ] Command injection risks avoided
- [ ] LDAP injection prevention shown where relevant

## Authentication & Authorization

- [ ] Secure authentication patterns demonstrated
- [ ] Password hashing used (bcrypt, Argon2, PBKDF2)
- [ ] Never store passwords in plaintext
- [ ] Session management follows best practices
- [ ] JWT secrets properly managed
- [ ] Authorization checks shown in protected routes

## Cryptography

- [ ] No deprecated crypto functions (MD5, SHA1 for security)
- [ ] Secure random number generation demonstrated
- [ ] HTTPS/TLS usage recommended
- [ ] Certificate validation not disabled
- [ ] Appropriate key lengths used

## Data Protection

- [ ] Sensitive data handling explained
- [ ] No logging of passwords or secrets
- [ ] Personal information protected appropriately
- [ ] Data encryption demonstrated where needed
- [ ] Secure data transmission shown

## Security Headers

- [ ] Security headers recommended where applicable
- [ ] CORS configured properly
- [ ] Content Security Policy mentioned for web apps
- [ ] X-Frame-Options discussed for clickjacking prevention

## Dependencies

- [ ] Dependency security mentioned
- [ ] No use of packages with known vulnerabilities
- [ ] Version pinning or ranges explained
- [ ] Regular updates recommended

## Error Handling

- [ ] No sensitive information in error messages
- [ ] Stack traces not exposed to users in production
- [ ] Appropriate error logging demonstrated
- [ ] Security events logged for audit trail

## Reference to Standards

- [ ] OWASP guidelines referenced where applicable
- [ ] Industry standards followed
- [ ] Common vulnerability patterns (CWE) avoided
- [ ] Security resources provided for further reading
