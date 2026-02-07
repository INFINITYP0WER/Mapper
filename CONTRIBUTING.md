# Contributing to SBS Mapping System

Thank you for your interest in contributing to the SBS Mapping System! This document provides guidelines for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sbs-mapping-system.git
   cd sbs-mapping-system
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Sample data (if applicable, anonymized)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- Clear use case
- Why this enhancement would be useful
- Possible implementation approach

### Code Contributions

We welcome contributions in these areas:

1. **Bug fixes**
2. **Performance improvements**
3. **New matching algorithms**
4. **Additional export formats**
5. **Better documentation**
6. **Test coverage**
7. **Arabic language support**

## Development Setup

### Prerequisites

- Python 3.7+
- Git
- pip

### Setup Steps

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install development dependencies** (optional):
   ```bash
   pip install pytest black pylint mypy
   ```

4. **Verify installation**:
   ```bash
   python -c "from sbs_ai_mapping_system import SBSMappingEngine; print('OK')"
   ```

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable names
- Add docstrings to all functions and classes
- Keep functions focused and small (<50 lines)
- Use type hints where appropriate

### Example

```python
def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two text strings.
    
    Args:
        text1: First text string
        text2: Second text string
    
    Returns:
        Similarity score between 0 and 1
    
    Example:
        >>> calculate_similarity("hello", "hallo")
        0.85
    """
    # Implementation here
    pass
```

### Code Formatting

Before committing, format your code:

```bash
black sbs_ai_mapping_system.py
black sbs_mapping_cli.py
```

### Linting

Check your code:

```bash
pylint sbs_ai_mapping_system.py
```

## Testing

### Running Tests

```bash
pytest tests/
```

### Writing Tests

- Write tests for all new features
- Aim for >80% code coverage
- Use descriptive test names
- Include edge cases

Example test:

```python
def test_jaccard_similarity_identical_strings():
    """Test that identical strings return 1.0 similarity"""
    result = SimilarityCalculator.jaccard_similarity("test", "test")
    assert result == 1.0

def test_jaccard_similarity_different_strings():
    """Test that completely different strings return 0.0"""
    result = SimilarityCalculator.jaccard_similarity("abc", "xyz")
    assert result == 0.0
```

### Test Data

- Use anonymized/synthetic data only
- Never commit real patient or healthcare data
- Include test fixtures in `tests/fixtures/`

## Pull Request Process

### Before Submitting

1. ✅ Update documentation if needed
2. ✅ Add tests for new features
3. ✅ Run all tests and ensure they pass
4. ✅ Format code with `black`
5. ✅ Update CHANGELOG.md
6. ✅ Ensure no merge conflicts

### PR Checklist

- [ ] Clear description of changes
- [ ] Reference to related issue (if applicable)
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code formatted with `black`
- [ ] All tests passing
- [ ] No breaking changes (or clearly documented)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update
- [ ] Other (please describe)

## Related Issue
Fixes #(issue number)

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

### Review Process

1. Submit PR
2. Automated checks run (if configured)
3. Code review by maintainers
4. Address feedback
5. Approval and merge

## Project Structure

```
sbs-mapping-system/
├── sbs_ai_mapping_system.py    # Core engine
├── sbs_mapping_cli.py           # CLI interface
├── sbs_mapping_notebook.ipynb  # Interactive notebook
├── tests/                       # Test files
│   ├── test_engine.py
│   ├── test_similarity.py
│   └── fixtures/                # Test data
├── docs/                        # Documentation
│   ├── README.md
│   ├── QUICK_START_GUIDE.md
│   └── SBS_MAPPING_DOCUMENTATION.md
├── examples/                    # Usage examples
│   ├── basic_usage.py
│   └── advanced_usage.py
├── requirements.txt             # Dependencies
├── .gitignore
├── LICENSE
└── CONTRIBUTING.md             # This file
```

## Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(engine): add support for Arabic text normalization

Implement Arabic-specific text preprocessing including:
- Arabic letter normalization
- Diacritic removal
- Number conversion

Closes #42
```

```
fix(cli): handle missing price column gracefully

Previously crashed when price column was not found.
Now continues with warning message.

Fixes #15
```

## Areas for Contribution

### High Priority

1. **Arabic Language Support**
   - Improve Arabic text normalization
   - Add Arabic-specific similarity metrics
   - Support RTL text handling

2. **Performance Optimization**
   - Batch processing improvements
   - Memory usage optimization
   - Parallel processing support

3. **Testing**
   - Increase test coverage
   - Add integration tests
   - Performance benchmarks

### Medium Priority

4. **Export Formats**
   - JSON export
   - SQL script generation
   - API-ready formats

5. **Matching Algorithms**
   - Add semantic similarity
   - ML-based matching
   - Custom weighting options

6. **User Interface**
   - Web-based UI
   - Desktop application
   - Progress indicators

### Documentation

7. **Tutorials**
   - Video tutorials
   - Step-by-step guides
   - Best practices

8. **API Documentation**
   - Auto-generated docs
   - Code examples
   - Use case scenarios

## Questions?

- Create an issue with the `question` label
- Check existing documentation
- Review closed issues for similar questions

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to SBS Mapping System! 🎉
