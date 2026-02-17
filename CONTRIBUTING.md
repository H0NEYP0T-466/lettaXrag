# 🤝 Contributing to LettaXRAG

Thank you for your interest in contributing to LettaXRAG! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Format](#commit-message-format)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)

## 🚀 Getting Started

1. **Fork the Repository**
   ```bash
   # Click the 'Fork' button on GitHub
   # Then clone your fork
   git clone https://github.com/YOUR_USERNAME/lettaXrag.git
   cd lettaXrag
   ```

2. **Add Upstream Remote**
   ```bash
   git remote add upstream https://github.com/H0NEYP0T-466/lettaXrag.git
   git fetch upstream
   ```

3. **Keep Your Fork Updated**
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

## 🛠 Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

### Frontend Setup

```bash
# From root directory
npm install

# Create .env file
cp .env.example .env
```

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+
- **MongoDB** (local or remote)
- **LongCat API Key** ([Get one here](https://longcat.chat))

## 🌿 Branch Naming Conventions

Use descriptive branch names with the following prefixes:

- `feat/` - New features
  - Example: `feat/add-dark-mode`
- `fix/` - Bug fixes
  - Example: `fix/mongodb-connection-error`
- `docs/` - Documentation changes
  - Example: `docs/update-readme`
- `refactor/` - Code refactoring
  - Example: `refactor/simplify-rag-service`
- `test/` - Adding or updating tests
  - Example: `test/add-unit-tests-for-llm-service`
- `chore/` - Maintenance tasks
  - Example: `chore/update-dependencies`
- `perf/` - Performance improvements
  - Example: `perf/optimize-vector-search`

## 💬 Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```bash
# Simple commit
git commit -m "feat(chat): add markdown rendering support"

# With body
git commit -m "fix(rag): improve context retrieval accuracy

- Increased chunk overlap to 100 characters
- Adjusted similarity threshold to 0.75
- Added logging for debug purposes"

# Breaking change
git commit -m "feat(api)!: change chat endpoint response format

BREAKING CHANGE: Response now includes metadata object"
```

## 🔄 Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Frontend linting
   npm run lint
   
   # Backend testing (if tests exist)
   cd backend
   pytest
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: your descriptive commit message"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feat/your-feature-name
   ```

6. **Create Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template
   - Link related issues (e.g., "Closes #123")

7. **Code Review**
   - Address reviewer feedback
   - Make requested changes
   - Push updates to your branch (PR will update automatically)

8. **Merge**
   - Once approved, a maintainer will merge your PR
   - Delete your feature branch after merge

## 🎨 Code Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use docstrings for classes and functions:
  ```python
  def retrieve_context(self, query: str, k: int = 5) -> List[str]:
      """
      Retrieve relevant context from FAISS index.
      
      Args:
          query: User query string
          k: Number of results to return (default: 5)
          
      Returns:
          List of relevant text chunks
      """
  ```

### TypeScript/JavaScript (Frontend)

- ESLint configuration is in `eslint.config.js`
- Run linter before committing:
  ```bash
  npm run lint
  ```
- Use TypeScript strict mode
- Prefer functional components with hooks
- Use descriptive variable and function names

### General Guidelines

- **DRY (Don't Repeat Yourself)**: Extract common logic into functions
- **Clear naming**: Use descriptive names for variables, functions, and classes
- **Small functions**: Keep functions focused on a single task
- **Comments**: Add comments for complex logic, but prefer self-documenting code
- **Error handling**: Always handle potential errors gracefully

## ✅ Testing Requirements

### Backend Testing

If adding new features to the backend:

1. Write unit tests for new functions
2. Test error cases and edge conditions
3. Ensure existing tests still pass
4. Add integration tests for API endpoints

### Frontend Testing

For UI changes:

1. Test in different browsers (Chrome, Firefox, Safari)
2. Test responsive design on different screen sizes
3. Verify accessibility (keyboard navigation, screen readers)
4. Test with different data scenarios (empty state, loading, errors)

### Manual Testing Checklist

Before submitting PR:

- [ ] Application starts without errors
- [ ] All new features work as expected
- [ ] Existing features still work correctly
- [ ] No console errors or warnings
- [ ] Documentation is updated
- [ ] Code is properly formatted

## 📚 Documentation

Update documentation when:

- Adding new features
- Changing existing functionality
- Adding new API endpoints
- Modifying configuration options
- Updating dependencies

### Documentation Files

- `README.md` - Main project documentation
- `API.md` - API endpoint documentation
- `ARCHITECTURE.md` - System architecture details
- `GETTING_STARTED.md` - Quick start guide
- `TESTING.md` - Testing guidelines
- `LETTA_INFO.md` - Letta integration details
- `SECURITY.md` - Security considerations

## 🐛 Reporting Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml) and include:

- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Node.js version, Python version)
- Relevant logs or error messages

## 💡 Suggesting Features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml) and include:

- Problem statement
- Proposed solution
- Alternative solutions considered
- Additional context or mockups

## 🔒 Security Issues

**Do not report security vulnerabilities through public GitHub issues.**

See [SECURITY.md](SECURITY.md) for reporting security vulnerabilities.

## 📜 Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🙏 Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Project README (for major features)

## 💬 Questions?

- Open a [Discussion](https://github.com/H0NEYP0T-466/lettaXrag/discussions)
- Create an issue with the "question" label
- Reach out to maintainers

---

Thank you for contributing to LettaXRAG! 🎉
