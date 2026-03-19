# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Single `VERSION` file for app + installer; Git tag `v*` overrides in CI.
- `CHANGELOG.md`, `LICENSE` (MIT), Dependabot, CI test workflow.
- Optional Authenticode signing script and docs.

## [1.0.4] - 2025-03-20

### Changed
- CI: dedupe concurrent installer builds for the same commit.
- Installer `AppVersion` follows `VERSION` / release tag.
- Tracked `packaging/grabby.spec` so GitHub Actions can build the installer.

## [1.0.3] - 2025-03-20

### Fixed
- PyInstaller/Inno CI failure: `grabby.spec` was gitignored and missing on runners.

[Unreleased]: https://github.com/jampat000/Grabby/compare/v1.0.4...HEAD
[1.0.4]: https://github.com/jampat000/Grabby/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/jampat000/Grabby/releases/tag/v1.0.3
