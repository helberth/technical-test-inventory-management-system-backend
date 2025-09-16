# Inventory Management System - Backend

A robust backend service for managing inventory products with user authentication, built with FastAPI and SQL database.

## 🚀 Features

- **User Authentication**
  - JWT-based authentication system
  - Secure user registration and login
  - Protected API endpoints

- **Product Management (CRUD)**
  - Create, Read, Update, and Delete products
  - List all products with pagination
  - Get product details by ID
  - Search and filter products
  - Image upload and management

- **Data Models**
  - User model with authentication details
  - Product model with comprehensive attributes

- **Architecture**
  - Repository pattern implementation
  - Clear separation of concerns
  - Asynchronous API endpoints

## 🛠️ Technology Stack

- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Database**: PostgreSQL / SQLite
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: Pytest
- **Code Quality**: Black, isort, flake8

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/technical-test-inventory-management-system-backend.git
   cd technical-test-inventory-management-system-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## 🚦 Running the Application

Start the development server:
```bash
fastapi dev main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## 🧪 Running Tests

```bash
pytest
```

## 🏗️ Project Structure

```
├── app/
│   ├── api/              # API routes
│   ├── core/             # Core functionality
│   ├── db/               # Database configuration
│   ├── models/           # Database models
│   ├── repositories/     # Repository implementations
│   ├── schemas/          # Pydantic models
│   ├── services/         # Business logic
│   └── main.py           # Application entry point
├── static/               # Static files (images, etc.)
│   └── images/           # Product images storage
├── tests/                # Test cases
├── alembic/              # Database migrations
├── .env.example          # Example environment variables
└── requirements.txt      # Project dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Made with ❤️ for the Technical Test
</div>