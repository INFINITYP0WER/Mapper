# Changelog

All notable changes to the SBS Mapping System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Arabic language support improvements
- Web-based user interface
- API endpoints for system integration
- Advanced ML-based matching algorithms
- Automated testing suite
- Performance benchmarks

---

## [2.0.0] - 2026-02-07

### Added
- Complete AI-powered mapping system
- Jaccard similarity algorithm for keyword matching
- Levenshtein distance algorithm for character-level matching
- Weighted similarity scoring system
- Five-level confidence classification system
- Automatic ambiguity detection
- Command-line interface (CLI)
- Interactive Jupyter notebook
- Batch processing capabilities
- Multiple export formats (Excel, JSON)
- Comprehensive mapping reports
- Statistical analysis and visualizations
- Review list generation
- High-confidence match filtering
- Customizable similarity thresholds
- Flexible column name mapping
- Progress indicators for long-running operations
- Error handling and validation
- Complete documentation suite
- Quick start guide
- Code examples and templates

### Changed
- Complete rewrite of matching engine
- Improved text normalization
- Better keyword extraction
- Enhanced error messages
- Optimized performance for large datasets

### Fixed
- Memory usage with large files
- Unicode handling in descriptions
- Column name case sensitivity
- Duplicate detection

---

## [1.2.0] - 2024-11-15

### Added
- Improved Arabic text handling
- Better medical terminology recognition
- Enhanced code similarity detection

### Changed
- Updated similarity calculation weights
- Improved performance on large datasets

### Fixed
- Issue with special characters in descriptions
- Memory leak in batch processing

---

## [1.1.0] - 2024-08-20

### Added
- Batch processing capabilities
- CSV file support
- Basic visualization charts
- Progress indicators

### Changed
- Improved text normalization
- Better keyword extraction

### Fixed
- File encoding issues
- Column detection bugs

---

## [1.0.0] - 2024-06-01

### Added
- Initial release
- Basic text matching functionality
- Excel file support
- Simple command-line interface
- Basic documentation

---

## Version Numbering

- **Major version** (X.0.0): Incompatible API changes
- **Minor version** (0.X.0): New features, backwards compatible
- **Patch version** (0.0.X): Bug fixes, backwards compatible

## Types of Changes

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

---

## Migration Guides

### Upgrading from 1.x to 2.0

**Breaking Changes:**
- API method signatures changed
- Configuration format updated
- Output file structure modified

**Migration Steps:**

1. **Update code imports**:
   ```python
   # Old (v1.x)
   from sbs_mapper import Mapper
   
   # New (v2.0)
   from sbs_ai_mapping_system import SBSMappingEngine
   ```

2. **Update method calls**:
   ```python
   # Old (v1.x)
   mapper = Mapper()
   results = mapper.map(file1, file2)
   
   # New (v2.0)
   engine = SBSMappingEngine()
   engine.load_sbs_v2_v3_mapping(file1)
   engine.load_price_list(file2)
   results = engine.map_to_price_list(...)
   ```

3. **Update configuration**:
   - Review new threshold options
   - Update column name parameters
   - Check output file locations

4. **Test thoroughly**:
   - Run with sample data first
   - Compare results with v1.x
   - Validate high-confidence matches

---

## Support for Old Versions

- **v2.x**: Active development, full support
- **v1.x**: Security fixes only until 2026-12-31
- **v0.x**: No longer supported

---

## Release Schedule

- **Major releases**: Annually
- **Minor releases**: Quarterly
- **Patch releases**: As needed for critical fixes

---

## How to Report Issues

Found a bug or have a feature request?

1. Check existing issues on GitHub
2. Create new issue with template
3. Include version number and system details
4. Provide sample data if possible (anonymized)

---

[Unreleased]: https://github.com/yourusername/sbs-mapping-system/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/yourusername/sbs-mapping-system/compare/v1.2.0...v2.0.0
[1.2.0]: https://github.com/yourusername/sbs-mapping-system/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/yourusername/sbs-mapping-system/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/yourusername/sbs-mapping-system/releases/tag/v1.0.0
