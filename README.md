# Django Marketplace

A Django-based marketplace application with user authentication, product management, and order processing.

## Setup with Poetry

This project uses Poetry for dependency management. Make sure you have Poetry installed:

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -
```

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd marketplace
```

2. Install dependencies with Poetry:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

### Poetry Commands

- **Install dependencies**: `poetry install`
- **Add a dependency**: `poetry add package-name`
- **Add a dev dependency**: `poetry add --group dev package-name`
- **Remove a dependency**: `poetry remove package-name`
- **Update dependencies**: `poetry update`
- **Activate virtual environment**: `poetry shell`
- **Run commands in virtual environment**: `poetry run python manage.py migrate`

### Development

- **Run tests**: `poetry run pytest`
- **Run with coverage**: `poetry run coverage run --source='.' manage.py test`
- **Generate coverage report**: `poetry run coverage report`
- **Start development server**: `poetry run python manage.py runserver`

### Project Structure

- `accounts/` - User authentication and seller profiles
- `products/` - Product management and catalog
- `orders/` - Shopping cart and order processing
- `marketplace/` - Main project settings and configuration

### Features

- User registration and authentication
- Seller profiles and store management
- Product catalog with categories
- Shopping cart functionality
- Order processing and history
- Multi-language support (English/Ukrainian)
- Responsive design with Bootstrap

### Environment Variables

Create a `.env` file in the project root with:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Database

The project uses SQLite by default. For production, update the database settings in `marketplace/settings.py`.
