# Code Example Checklist

Use this checklist to validate individual code examples for technical books. Focuses on specific example quality, not general code quality.

## Purpose and Clarity

- [ ] Example has clear learning purpose
- [ ] Demonstrates specific concept/technique
- [ ] Not too simple (trivial) or too complex
- [ ] Appropriate for target audience

## Code Quality

- [ ] Code follows language conventions
- [ ] Variable names are descriptive
- [ ] No magic numbers (use constants)
- [ ] Comments explain WHY, not WHAT
- [ ] Code is concise but not cryptic

## Completeness

- [ ] Example is runnable as-is
- [ ] No missing imports/dependencies
- [ ] No assumed context
- [ ] File structure clear
- [ ] Setup instructions provided (if needed)

## Testing

- [ ] Example has been tested
- [ ] Tests included (unit tests or verification script)
- [ ] Expected output documented
- [ ] Edge cases considered
- [ ] Error handling demonstrated (where appropriate)

## Progressive Complexity

- [ ] Builds on previous examples
- [ ] Introduces 1-2 new concepts (not overwhelming)
- [ ] Shows evolution of approach
- [ ] Complexity appropriate for chapter position

## Best Practices

- [ ] Security considerations addressed
- [ ] Performance implications noted
- [ ] Common mistakes highlighted
- [ ] Real-world applicability shown

## Documentation

- [ ] Code includes inline comments
- [ ] Explanation text accompanies code
- [ ] Expected output shown
- [ ] Troubleshooting notes provided

## Integration

- [ ] Fits section learning objectives
- [ ] Referenced in narrative text
- [ ] Part of progressive example sequence
- [ ] Supports hands-on learning

## Usage

- **When to use**: After creating code example, before integrating in section (code-example-workflow step 2)
- **Who executes**: Code curator
- **Integration**: Quality gate in code-example-workflow
- **On failure**: Revise code for clarity, add tests, improve documentation
- **Difference from code-quality-checklist**: This validates specific pedagogical examples; code-quality-checklist validates general code standards
