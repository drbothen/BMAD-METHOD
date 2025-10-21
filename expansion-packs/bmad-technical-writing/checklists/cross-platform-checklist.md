# Cross-Platform Checklist

Use this checklist to ensure code examples work correctly across Windows, macOS, and Linux.

## File Path Handling

- [ ] Use `pathlib.Path` (Python) or equivalent cross-platform path library
- [ ] Avoid hardcoded path separators (/ or \)
- [ ] Handle path case sensitivity differences
- [ ] Use `os.path.join()` or `Path()` for path construction
- [ ] Test absolute vs relative paths on all platforms

## Line Endings

- [ ] Specify newline handling explicitly when reading/writing files
- [ ] Don't assume LF (Unix) or CRLF (Windows) line endings
- [ ] Use `newline=''` parameter in Python `open()` or equivalent
- [ ] Git `.gitattributes` configured if code includes text files

## Environment Variables

- [ ] Use cross-platform environment variable methods
- [ ] Avoid shell-specific export syntax in documentation
- [ ] Provide instructions for setting env vars on all platforms
- [ ] Handle missing environment variables gracefully

## Shell Commands

- [ ] Avoid platform-specific shell commands (PowerShell vs bash)
- [ ] Provide equivalent commands for Windows, Mac, Linux
- [ ] Use Python/Node.js/etc. libraries instead of shell when possible
- [ ] Document shell differences clearly

## Platform-Specific Code

- [ ] Use `platform.system()` or equivalent to detect OS
- [ ] Provide platform-specific implementations where necessary
- [ ] Document which platforms require special handling
- [ ] Test platform detection logic

## Testing

- [ ] Code tested on Windows 10/11
- [ ] Code tested on macOS 12+ (or latest)
- [ ] Code tested on Linux (Ubuntu 20.04+ or equivalent)
- [ ] CI/CD tests on all target platforms
- [ ] Platform-specific edge cases handled

## Installation Instructions

- [ ] Installation steps provided for Windows
- [ ] Installation steps provided for macOS
- [ ] Installation steps provided for Linux
- [ ] Package manager differences documented (apt vs brew vs choco)
- [ ] Platform-specific prerequisites noted

## Dependencies

- [ ] All dependencies available on target platforms
- [ ] Platform-specific dependency installation documented
- [ ] Binary dependencies noted (may require compilation)
- [ ] Alternative packages suggested if platform-specific

## User Interface

- [ ] Console output works on all platforms
- [ ] Unicode/emoji support considered
- [ ] Color output handled (may not work in all terminals)
- [ ] Terminal size/width differences handled

## Documentation

- [ ] README includes platform-specific notes
- [ ] Known platform limitations documented
- [ ] Workarounds provided for platform issues
- [ ] Platform support explicitly stated
