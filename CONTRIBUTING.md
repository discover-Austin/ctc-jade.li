# Contributing to Vehicle Repair Database

Thank you for your interest in contributing to the Vehicle Repair Database! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Data Contributions](#data-contributions)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

There are many ways to contribute to this project:

### 1. Report Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, browser, etc.)

### 2. Suggest Features

Feature requests are welcome! Please include:
- Detailed description of the feature
- Use case and benefits
- Possible implementation approach

### 3. Submit Code

- Fix bugs
- Add new features
- Improve documentation
- Optimize performance
- Add tests

### 4. Contribute Data

As a mechanic or technician, you can contribute:
- Repair procedures with photos
- Torque specifications
- Wiring diagrams
- Common problem reports
- Diagnostic procedures

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker and Docker Compose
- Git

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/your-org/vehicle-db.git
cd vehicle-db

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload

# Frontend setup (in a new terminal)
cd frontend
npm install
npm run dev
```

### Using Docker

```bash
# Start all services
docker-compose up -d

# Initialize database
docker-compose exec api python scripts/init_db.py

# View logs
docker-compose logs -f api
```

## Contribution Guidelines

### Code Style

#### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use docstrings for all functions and classes
- Format code with Black: `black .`
- Lint with Flake8: `flake8 app`
- Type check with mypy: `mypy app`

Example:

```python
from typing import List, Optional

def calculate_torque(
    force_pounds: float,
    distance_feet: float
) -> float:
    """
    Calculate torque in pound-feet.

    Args:
        force_pounds: Force applied in pounds
        distance_feet: Distance from pivot in feet

    Returns:
        Torque value in pound-feet
    """
    return force_pounds * distance_feet
```

#### TypeScript/React (Frontend)

- Use TypeScript for all new code
- Follow Airbnb React/JSX Style Guide
- Use functional components with hooks
- Format code with Prettier
- Lint with ESLint: `npm run lint`

Example:

```typescript
interface VehicleProps {
  year: number;
  make: string;
  model: string;
}

const VehicleCard: React.FC<VehicleProps> = ({ year, make, model }) => {
  return (
    <Card>
      <Typography>
        {year} {make} {model}
      </Typography>
    </Card>
  );
};
```

### Git Commit Messages

Write clear, descriptive commit messages:

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:

```
feat: Add VIN decoder API endpoint

Implement VIN decoding using NHTSA API with validation
using ISO 3779 check digit algorithm.

Closes #123
```

```
fix: Correct torque spec query for diesel engines

The previous query was excluding diesel engine torque specs
due to incorrect filter logic.

Fixes #456
```

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

## Data Contributions

### Repair Procedures

When contributing repair procedures, include:

1. **Complete Information**
   - Vehicle make, model, year range
   - System and subsystem
   - Difficulty level
   - Estimated time

2. **Step-by-Step Instructions**
   - Clear, numbered steps
   - Safety precautions
   - Special tools required
   - Torque specifications

3. **Visual Documentation**
   - High-quality photos
   - Diagrams if applicable
   - Video walkthroughs (optional)

4. **Source Verification**
   - OEM service manual reference
   - Your professional credentials
   - Years of experience

### Torque Specifications

Torque specs must include:
- Component name and description
- Torque value (lb-ft and Nm)
- Tightening sequence
- Thread locker requirements
- Lubrication requirements
- Source (OEM manual, certification)

### Data Accuracy Requirements

All technical data must:
- Be verified from OEM sources when possible
- Include source references
- Be peer-reviewed by certified mechanics
- Include applicable year ranges
- Note any exceptions or conditions

## Testing

### Backend Tests

```bash
# Run all tests
pytest backend/tests/ -v

# Run with coverage
pytest backend/tests/ --cov=app --cov-report=html

# Run specific test file
pytest backend/tests/test_api.py -v
```

### Frontend Tests

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# E2E tests
npm run test:e2e
```

### Required Test Coverage

- New features: Minimum 80% coverage
- Bug fixes: Include test that reproduces the bug
- API endpoints: Test all response codes
- Data validation: Test edge cases

## Pull Request Process

### Before Submitting

1. **Update your fork**
   ```bash
   git remote add upstream https://github.com/your-org/vehicle-db.git
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**
   ```bash
   pytest backend/tests/
   npm test
   ```

3. **Check code style**
   ```bash
   black backend/app
   flake8 backend/app
   npm run lint
   ```

4. **Update documentation** if needed

### Submitting

1. Push your changes to your fork
2. Create a Pull Request with:
   - Clear title describing the change
   - Detailed description
   - Reference to related issues
   - Screenshots for UI changes
   - Test results

3. Request review from maintainers

### PR Review Process

Maintainers will review for:
- Code quality and style
- Test coverage
- Documentation completeness
- Performance implications
- Security considerations
- Data accuracy (for technical contributions)

### After Approval

- Squash commits if requested
- Rebase on latest main
- Maintainer will merge

## Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- About page in the application

### Contribution Levels

- **Bronze**: 1-5 contributions
- **Silver**: 6-20 contributions
- **Gold**: 21-50 contributions
- **Platinum**: 51+ contributions or significant features

### Mechanic Certification

Certified mechanics can display credentials:
- ASE Certification
- Manufacturer certifications
- Years of experience

## Questions?

- Open an issue for questions
- Join our Discord community
- Email: contribute@vehiclerepairdb.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to making automotive repair information accessible to everyone!
