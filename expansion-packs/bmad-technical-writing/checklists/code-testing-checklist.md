# Code Testing Checklist

Use this checklist to ensure all code examples are thoroughly tested.

## Basic Testing

- [ ] Every code example has been executed successfully
- [ ] Code runs on specified version(s) (e.g., Python 3.11+, Node 18+)
- [ ] Output matches documentation
- [ ] No errors or exceptions occur during execution
- [ ] All dependencies install correctly

## Version Compatibility

- [ ] Code tested on minimum supported version
- [ ] Code tested on latest stable version
- [ ] Version-specific behaviors documented
- [ ] Deprecated features avoided
- [ ] Version matrix created and validated

## Platform Testing

- [ ] Code tested on target platforms (Windows/Mac/Linux as applicable)
- [ ] Platform-specific issues identified and documented
- [ ] Path separators handled correctly
- [ ] Line endings appropriate
- [ ] Platform differences noted in documentation

## Edge Cases

- [ ] Empty input tested
- [ ] Null/None values tested
- [ ] Boundary values tested
- [ ] Large datasets tested (if relevant)
- [ ] Error conditions tested

## Error Handling

- [ ] Error cases execute as documented
- [ ] Error messages match documentation
- [ ] Exceptions are caught appropriately
- [ ] Error handling doesn't hide bugs
- [ ] Recovery mechanisms work as expected

## Testing Instructions

- [ ] Setup instructions are complete and accurate
- [ ] Test commands are provided and work
- [ ] Expected output is documented
- [ ] Verification steps are clear
- [ ] Troubleshooting guidance provided

## Dependencies

- [ ] All dependencies are documented
- [ ] Dependency versions are specified
- [ ] Installation instructions are correct
- [ ] No undocumented dependencies
- [ ] Dependency conflicts resolved

## Reproducibility

- [ ] Fresh environment setup works from documented instructions
- [ ] Results are consistent across multiple runs
- [ ] No environment-specific assumptions
- [ ] Configuration steps are complete
- [ ] Verification of setup is possible
