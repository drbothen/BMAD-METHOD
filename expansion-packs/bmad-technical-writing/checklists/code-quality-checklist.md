# Code Quality Checklist

Use this checklist to ensure code examples meet quality standards for technical books.

## Style Guide Compliance

- [ ] Code follows language-specific style guide (PEP 8, Airbnb JS, Google Java, etc.)
- [ ] Indentation is consistent and correct
- [ ] Naming conventions are followed
- [ ] Line length limits respected
- [ ] Formatting is consistent throughout

## Naming

- [ ] Variable names are descriptive and meaningful
- [ ] Function/method names clearly describe their purpose
- [ ] No single-letter variables (except in loops/lambdas where conventional)
- [ ] Constants use appropriate naming (UPPER_CASE typically)
- [ ] Class names follow conventions (PascalCase typically)

## Comments

- [ ] Comments explain WHY, not WHAT
- [ ] Complex logic is explained
- [ ] Design decisions are documented
- [ ] Inline comments are used sparingly and purposefully
- [ ] No commented-out code left in examples

## Code Structure

- [ ] No hardcoded values (use constants or configuration)
- [ ] Code is DRY (Don't Repeat Yourself) - unless repetition aids clarity
- [ ] Functions are focused and do one thing well
- [ ] Code is organized logically
- [ ] Imports/dependencies are clearly listed

## Error Handling

- [ ] Appropriate error handling is demonstrated
- [ ] Error messages are meaningful
- [ ] Edge cases are considered
- [ ] Errors are caught at appropriate levels
- [ ] Error handling pattern is language-appropriate

## Best Practices

- [ ] Follows current language best practices
- [ ] Uses modern language features appropriately
- [ ] Avoids deprecated features
- [ ] Security best practices followed (no hardcoded credentials, SQL injection prevention, etc.)
- [ ] Performance considerations addressed where relevant

## Educational Value

- [ ] Code prioritizes clarity over cleverness
- [ ] Examples are simple enough to understand but realistic
- [ ] Code demonstrates the concept clearly
- [ ] No unnecessary complexity
- [ ] Production-ready patterns shown where appropriate
