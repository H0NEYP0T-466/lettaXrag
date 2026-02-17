# Contributing to LettaXRAG

Thank you for your interest in contributing to LettaXRAG! We welcome contributions from the community and are grateful for your support.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork the Repository**
   ```bash
   # Click the "Fork" button on GitHub
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

## Development Setup

### Backend Setup

1. **Create a Virtual Environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start MongoDB**
   ```bash
   # Make sure MongoDB is running on your system
   sudo systemctl start mongodb  # Linux
   brew services start mongodb-community  # macOS
   ```

5. **Run the Backend**
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   # From the root directory
   npm install
   ```

2. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

3. **Run the Frontend**
   ```bash
   npm run dev
   ```

### Development Tools

- **Linting (Frontend)**
  ```bash
  npm run lint
  ```

- **Type Checking (Frontend)**
  ```bash
  npm run build  # TypeScript will check types during build
  ```

## How to Contribute

### Reporting Bugs

1. **Check Existing Issues**: Search the [issue tracker](https://github.com/H0NEYP0T-466/lettaXrag/issues) to avoid duplicates
2. **Create a Bug Report**: Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml)
3. **Provide Details**: Include steps to reproduce, expected behavior, actual behavior, and your environment

### Suggesting Enhancements

1. **Check Existing Issues**: Search for similar feature requests
2. **Create a Feature Request**: Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml)
3. **Explain Your Idea**: Describe the problem, proposed solution, and alternatives considered

### Code Contributions

1. **Pick an Issue**: Look for issues labeled `good first issue` or `help wanted`
2. **Comment on the Issue**: Let others know you're working on it
3. **Follow the Development Workflow**: See below

## Branch Naming Conventions

Use descriptive branch names following this pattern:

```
<type>/<short-description>
```

**Types:**
- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `style/` - Code style changes (formatting, no logic change)
- `refactor/` - Code refactoring
- `perf/` - Performance improvements
- `test/` - Adding or updating tests
- `chore/` - Maintenance tasks

**Examples:**
```bash
feat/add-user-authentication
fix/mongodb-connection-error
docs/update-api-documentation
refactor/simplify-rag-service
```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

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
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

```bash
feat(api): add document upload endpoint

Add new POST /api/upload endpoint for document uploads.
Supports .txt, .md, .pdf, and .docx files.

Closes #123
```

```bash
fix(rag): resolve FAISS index initialization error

Fix issue where FAISS index was not being properly initialized
when the storage directory didn't exist.

Fixes #456
```

```bash
docs(readme): update installation instructions

Add detailed MongoDB setup instructions for different platforms.
```

### Commit Message Rules

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Keep the subject line under 50 characters
- Capitalize the subject line
- Don't end the subject line with a period
- Separate subject from body with a blank line
- Wrap the body at 72 characters
- Use the body to explain what and why, not how

## Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, readable code
   - Follow the code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Frontend
   npm run lint
   npm run build
   
   # Backend
   python -m pytest  # If tests exist
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feat/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template completely
   - Link related issues

7. **Address Review Comments**
   - Respond to all review comments
   - Make requested changes
   - Push additional commits to your branch

8. **Merge Requirements**
   - All CI checks must pass
   - At least one approval from a maintainer
   - No merge conflicts
   - All conversations resolved

## Code Style Guidelines

### TypeScript/JavaScript (Frontend)

- **Use TypeScript**: Always use TypeScript, avoid `any` types
- **ESLint**: Follow the ESLint configuration in `eslint.config.js`
- **Formatting**: Use consistent formatting (2 spaces for indentation)
- **Naming Conventions**:
  - Components: PascalCase (`ChatMessage.tsx`)
  - Files: camelCase or kebab-case
  - Variables/Functions: camelCase
  - Constants: UPPER_SNAKE_CASE
  - Interfaces/Types: PascalCase with `I` prefix for interfaces

**Example:**
```typescript
interface IMessage {
  id: string;
  content: string;
  timestamp: Date;
}

const formatMessage = (message: IMessage): string => {
  return `${message.content} (${message.timestamp})`;
};
```

### Python (Backend)

- **PEP 8**: Follow [PEP 8 style guide](https://pep8.org/)
- **Type Hints**: Use type hints for function parameters and return values
- **Docstrings**: Use docstrings for classes and functions
- **Naming Conventions**:
  - Classes: PascalCase
  - Functions/Variables: snake_case
  - Constants: UPPER_SNAKE_CASE
  - Private members: Prefix with underscore

**Example:**
```python
from typing import List, Optional

class RAGService:
    """Service for managing RAG (Retrieval-Augmented Generation) operations."""
    
    def __init__(self, index_path: str):
        """Initialize the RAG service.
        
        Args:
            index_path: Path to the FAISS index file
        """
        self.index_path = index_path
    
    def retrieve_context(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant context for a query.
        
        Args:
            query: The search query
            k: Number of results to return
            
        Returns:
            List of relevant context strings
        """
        # Implementation here
        pass
```

### General Guidelines

- **Keep it Simple**: Write clear, simple code over clever code
- **DRY Principle**: Don't Repeat Yourself
- **Single Responsibility**: Functions/classes should do one thing well
- **Meaningful Names**: Use descriptive variable and function names
- **Comments**: Write comments for complex logic, not obvious code
- **Error Handling**: Handle errors gracefully with proper error messages

## Testing Requirements

### Frontend Testing

Currently, the frontend doesn't have automated tests. When adding tests:
- Use React Testing Library
- Test user interactions and component behavior
- Aim for meaningful test coverage, not 100% coverage

### Backend Testing

When adding backend tests:
- Use `pytest` for testing
- Mock external dependencies (MongoDB, LLM APIs)
- Test both success and error cases
- Include integration tests for critical paths

### Testing Checklist

Before submitting a PR:
- [ ] All existing tests pass
- [ ] New features have tests (when applicable)
- [ ] Edge cases are covered
- [ ] Error handling is tested
- [ ] Manual testing completed

## Documentation

### Code Documentation

- **Comments**: Explain why, not what
- **Docstrings**: Use for all public functions and classes
- **Type Hints**: Help others understand function signatures

### User Documentation

When adding new features, update:
- [ ] README.md - If it affects usage
- [ ] API.md - If it adds/changes API endpoints
- [ ] ARCHITECTURE.md - If it changes architecture
- [ ] Inline help text/tooltips in the UI

### Documentation Style

- Use clear, concise language
- Include code examples where helpful
- Add screenshots for UI changes
- Keep documentation up-to-date with code changes

## Getting Help

If you need help:

1. **Check Documentation**: Review README, ARCHITECTURE, and API docs
2. **Search Issues**: Look for similar questions in closed issues
3. **Ask Questions**: Open a discussion in [GitHub Discussions](https://github.com/H0NEYP0T-466/lettaXrag/discussions)
4. **Contact Maintainers**: For sensitive issues, contact maintainers directly

## Recognition

Contributors will be recognized in:
- The project README (if significant contribution)
- Git history
- Release notes (for features and major fixes)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to LettaXRAG! 🎉
