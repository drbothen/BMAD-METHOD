# Version Compatibility Checklist

Use this checklist to ensure code examples support specified versions and version information is clear.

## Version Specification

- [ ] Target versions are explicitly specified (e.g., "Python 3.11+")
- [ ] Minimum version is stated clearly
- [ ] Maximum version tested is documented (if applicable)
- [ ] Version ranges use clear notation (+, -, specific list)
- [ ] Language/framework versions are unambiguous

## Version Testing

- [ ] Code tested on minimum supported version
- [ ] Code tested on latest stable version at time of writing
- [ ] Code tested on intermediate versions where breaking changes exist
- [ ] All specified versions confirmed working
- [ ] Test results documented

## Version-Specific Features

- [ ] Use of version-specific features is noted
- [ ] Features available only in certain versions are documented
- [ ] Backward compatibility considerations addressed
- [ ] Alternative approaches for older versions provided (if supporting multiple)
- [ ] Deprecation warnings acknowledged and addressed

## Deprecated Features

- [ ] No use of deprecated features
- [ ] If deprecated features necessary, warnings included
- [ ] Migration path to current features shown
- [ ] Future compatibility considered
- [ ] Deprecated features only used with explicit justification

## Version Matrix

- [ ] Version compatibility matrix created
- [ ] Matrix includes all target platforms if relevant
- [ ] Known issues documented per version
- [ ] Testing date included in matrix
- [ ] Matrix is up-to-date

## Dependency Versions

- [ ] Dependency versions specified explicitly
- [ ] Dependency version compatibility tested
- [ ] Dependency version ranges documented
- [ ] Lock files provided where appropriate (package-lock.json, Pipfile.lock, etc.)
- [ ] Dependency updates strategy noted

## Migration Notes

- [ ] Guidance for readers on different versions provided
- [ ] Version-specific code variations shown when necessary
- [ ] Breaking changes between versions documented
- [ ] Upgrade path described for version changes
- [ ] Version migration risks identified

## Future-Proofing

- [ ] Code uses stable, well-established features where possible
- [ ] Experimental features are flagged as such
- [ ] Anticipated version changes noted
- [ ] Update strategy for book code discussed
- [ ] Code repository version branches (if supporting multiple versions)

## Documentation

- [ ] README or setup docs specify versions clearly
- [ ] Version numbers in all example code comments
- [ ] Testing environment versions documented
- [ ] Version verification commands provided
- [ ] Troubleshooting for version mismatches included
