# Authentication Microservice

A robust, production-ready authentication microservice built with FastAPI, PostgreSQL, and JWT authentication.

## 🚀 Features

- ✅ User registration and authentication
- ✅ JWT token-based authentication
- ✅ Password reset functionality
- ✅ Email verification
- ✅ Rate limiting
- ✅ Comprehensive logging
- ✅ Docker support
- ✅ Database migrations
- ✅ API documentation
- ✅ Test coverage

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Primary database
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **JWT**: Token-based authentication
- **Docker**: Containerization
- **Alembic**: Database migrations
- **Poetry/Pip**: Dependency management

## 📋 Prerequisites

- Python 3.10+
- Docker and Docker Compose
- PostgreSQL (if running locally)
- Make (optional, for using Makefile commands)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/auth-service.git
   cd auth-service
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configurations:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/auth_db
   SECRET_KEY=your-secret-key
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   DEBUG=False
   ```

3. **Using Docker (Recommended)**
   ```bash
   docker-compose up -d
   ```

4. **Local Development Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development

   # Run migrations
   alembic upgrade head

   # Start the application
   uvicorn app.main:app --reload
   ```

## 🚀 Usage

### API Endpoints

```plaintext
POST /api/v1/auth/signup
- Create a new user account
- Body: { "email": "user@example.com", "password": "securepassword" }

POST /api/v1/auth/login
- Authenticate user and get token
- Body: { "username": "user@example.com", "password": "securepassword" }

POST /api/v1/auth/password-reset-request
- Request password reset
- Body: { "email": "user@example.com" }

POST /api/v1/auth/password-reset
- Reset password using token
- Body: { "token": "reset_token", "new_password": "newpassword" }

GET /api/v1/auth/me
- Get current user info
- Header: Authorization: Bearer <token>
```

### Example Usage

```python
import requests

# Sign up
response = requests.post(
    "http://localhost:8000/api/v1/auth/signup",
    json={"email": "user@example.com", "password": "securepassword"}
)

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "user@example.com", "password": "securepassword"}
)
token = response.json()["access_token"]

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/api/v1/auth/me", headers=headers)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/api/test_auth.py
```

## 📦 Project Structure

```plaintext
auth_service/
├── alembic/                # Database migrations
├── app/
│   ├── api/               # API endpoints
│   ├── core/              # Core configuration
│   ├── db/                # Database setup
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   └── utils/             # Utility functions
├── tests/                 # Test files
└── docker/                # Docker configuration
```

## 🔒 Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Rate limiting on sensitive endpoints
- CORS protection
- SQL injection protection via SQLAlchemy
- Input validation using Pydantic

## 🚀 Deployment

1. **Docker Deployment**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Manual Deployment**
   ```bash
   # Set production configs
   export $(cat .env.prod | xargs)

   # Run migrations
   alembic upgrade head

   # Start the application
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## 📈 Monitoring

- Access logs: `docker-compose logs -f web`
- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Metrics: `http://localhost:8000/metrics`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## ❓ FAQ

**Q: How do I reset my database?**
```bash
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

**Q: How do I run specific tests?**
```bash
pytest tests/api/test_auth.py -k "test_login"
```

**Q: How do I update dependencies?**
```bash
pip install -U -r requirements.txt
pip freeze > requirements.txt
```

## 🐛 Troubleshooting

Common issues and solutions:

1. **Database connection issues**
   - Check if PostgreSQL is running
   - Verify database credentials in .env
   - Ensure database exists

2. **Email sending fails**
   - Check SMTP credentials
   - Verify email settings in .env
   - Check firewall settings

3. **Docker issues**
   - Run `docker-compose down -v`
   - Rebuild images: `docker-compose build --no-cache`
   - Check logs: `docker-compose logs -f`