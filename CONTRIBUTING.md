# Contributing to OSU Course Planner

Thank you for your interest in contributing! This project is built by OSU students for OSU students.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/thedjpetersen/reglib.git
   cd reglib
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Run tests**
   ```bash
   pytest
   ```

## Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run quality checks**
   ```bash
   # Format code
   ruff format .

   # Lint
   ruff check .

   # Type check
   mypy reglib

   # Run tests
   pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub.

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public APIs
- Maximum line length: 100 characters
- Use `ruff` for formatting and linting

## Testing

- Write tests for new features
- Maintain >90% code coverage
- Use pytest fixtures for common setups
- Test edge cases

## Areas for Contribution

Check our [ROADMAP.md](ROADMAP.md) for planned features.

**High Priority:**
- [ ] Ecampus scraper implementation
- [ ] OSU API client (when keys available)
- [ ] iCal export functionality
- [ ] PDF schedule generation
- [ ] Course prerequisite parsing

**Documentation:**
- [ ] API documentation
- [ ] Usage tutorials
- [ ] Example scripts
- [ ] FAQ

**Testing:**
- [ ] Integration tests
- [ ] Performance benchmarks
- [ ] Edge case coverage

## Questions?

- Open an issue for bugs
- Use Discussions for questions
- Check existing issues/PRs first

## Code of Conduct

Be respectful, inclusive, and constructive. This is a student project for the OSU community.

---

Thank you for contributing! 🦫
