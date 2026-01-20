# Changelog

## v0.2.0 — 2026-01-21

### Added
- Level-2 Audit Mode (advanced / beta) via `forward_detailed`
- Boundary vector decomposition (calibration, stability)
- Prediction stability boundary with sensitivity validation
- Statistical utilities for audit analysis
- Forensic audit test coverage

### Fixed
- Renamed internal logging module to avoid Python stdlib shadowing
- Safe handling of forward hooks in no-grad contexts

### Notes
- The original CDI production path (`forward_with_cdi`) is unchanged
- Level-2 audit mode is opt-in and does not affect inference performance
