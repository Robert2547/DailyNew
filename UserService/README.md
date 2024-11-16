# User Service

A microservice for managing user profiles and preferences, part of the Daily Summarizer platform.

## 🚀 Features

- ✅ Extended user profile management
- ✅ User preferences storage
- ✅ Integration with Auth Service
- ✅ PostgreSQL database
- ✅ FastAPI REST endpoints
- ✅ Docker support
- ✅ Alembic migrations

## 🏗️ Architecture

```mermaid
graph TD
    Client[Client] --> US[User Service]
    US --> AS[Auth Service]
    US --> DB[(PostgreSQL)]
    
    subgraph User Service
        API[API Layer] --> Service[Service Layer]
        Service --> Repository[Data Layer]
    end
```

## 🛠️ Tech Stack

- **FastAPI**: Modern web framework
- **SQLAlchemy**: ORM
- **PostgreSQL**: Primary database
- **Pydantic**: Data validation
- **Alembic**: Database migrations
- **Docker**: Containerization
- **HTTPX**: HTTP client for service communication

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL
- Auth Service running

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/user-service.git
   cd user-service
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configurations:
   ```env
   PROJECT_NAME=User Service
   VERSION=1.0.0
   HOST=0.0.0.0
   PORT=8003
   DATABASE_URL=postgresql://user:password@localhost:5432/user_db
   AUTH_SERVICE_URL=http://localhost:8001
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

   # Run migrations
   alembic upgrade head

   # Start the service
   uvicorn app.main:app --reload --port 8003
   ```

## 🚀 Usage

### API Endpoints

```plaintext
POST /api/v1/profiles
- Create user profile
- Requires authentication
- Request body:
  {
    "full_name": "John Doe",
    "preferences": {},
    "settings": {}
  }

GET /api/v1/profiles/me
- Get current user profile
- Requires authentication

PATCH /api/v1/profiles/me
- Update user profile
- Requires authentication
- Request body:
  {
    "full_name": "Updated Name",
    "preferences": {
      "theme": "dark"
    }
  }
```

### Example Usage

```python
import httpx

# Assuming you have an auth token
headers = {
    "Authorization": f"Bearer {token}"
}

# Create profile
response = httpx.post(
    "http://localhost:8003/api/v1/profiles",
    json={
        "full_name": "John Doe",
        "preferences": {"theme": "light"}
    },
    headers=headers
)

# Get profile
profile = httpx.get(
    "http://localhost:8003/api/v1/profiles/me",
    headers=headers
)
```

## 📊 Database Schema

```sql
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    auth_user_id INTEGER UNIQUE NOT NULL,
    full_name VARCHAR,
    preferences JSONB DEFAULT '{}',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## 🔄 Service Integration

### Auth Service Integration
```python
# Verify token with Auth Service
async def verify_token(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.AUTH_SERVICE_URL}/verify-token",
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_profiles.py
```

## 📦 Project Structure

```
user_service/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configuration
│   ├── db/            # Database setup
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   └── services/      # Business logic
```

## 🚀 Deployment

1. **Build and run with Docker**
   ```bash
   docker-compose up -d --build
   ```

2. **Run migrations**
   ```bash
   docker-compose exec user_service alembic upgrade head
   ```

## 🔍 Monitoring

- Health check: `GET /health`
- Metrics: `GET /metrics`
- OpenAPI docs: `GET /docs`

## 🐛 Troubleshooting

1. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose ps db
   
   # View database logs
   docker-compose logs db
   ```

2. **Auth Service Connection**
   ```bash
   # Check Auth Service status
   curl http://localhost:8001/health
   
   # View User Service logs
   docker-compose logs user_service
   ```

## 🔒 Security

- Authentication via Auth Service
- Input validation using Pydantic
- SQL injection protection via SQLAlchemy
- CORS protection
- Rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

