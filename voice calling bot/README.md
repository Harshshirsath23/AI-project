# Enterprise AI Calling Platform

A production-ready, multi-tenant AI voice agent platform built with enterprise-grade architecture. Designed to support millions of calls, thousands of concurrent AI agents, and multiple organizations.

## Technology Stack

### Backend
- **Python 3.13** - Programming language
- **FastAPI** - Async web framework
- **SQLAlchemy 2.0** - ORM with async support
- **Alembic** - Database migrations
- **Pydantic v2** - Data validation
- **PostgreSQL + pgvector** - Database with vector support
- **Redis** - Caching and message broker
- **Celery** - Background task processing
- **Uvicorn** - ASGI server

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **React Router** - Routing
- **TanStack Query** - Data fetching
- **Zustand** - State management
- **React Hook Form** - Form handling
- **Zod** - Schema validation

## Project Structure

```
Projects-AI/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── services/         # Business logic services
│   │   ├── database/         # Database connections
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── repositories/     # Data access layer
│   │   ├── ai/              # AI integrations
│   │   ├── telephony/       # Telephony providers
│   │   ├── authentication/  # Authentication logic
│   │   ├── campaigns/       # Campaign management
│   │   ├── agents/          # AI agent logic
│   │   ├── analytics/       # Analytics and reporting
│   │   ├── core/            # Core utilities
│   │   ├── config/          # Configuration management
│   │   ├── middleware/      # Custom middleware
│   │   ├── workers/         # Background workers
│   │   ├── websockets/      # WebSocket handlers
│   │   └── integrations/    # Third-party integrations
│   ├── alembic/             # Database migrations
│   ├── tests/               # Test suite
│   ├── scripts/             # Utility scripts
│   ├── requirements.txt     # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── store/          # State management
│   │   ├── types/          # TypeScript types
│   │   ├── utils/          # Utility functions
│   │   └── hooks/          # Custom hooks
│   └── package.json        # Node dependencies
```

## Database Architecture

The platform uses a multi-tenant architecture with the following core models:

### Core Models
- **Organization** - Multi-tenant organization management
- **OrganizationSettings** - Organization-specific configurations
- **User** - User accounts with role-based access
- **Role** - Role and permission management
- **Agent** - AI voice agent configurations
- **AgentVoiceProfile** - TTS voice settings
- **AgentConfiguration** - Agent behavior and capabilities
- **Campaign** - Outbound calling campaigns
- **Lead** - Campaign target contacts
- **KnowledgeBase** - RAG knowledge bases
- **KnowledgeDocument** - Document metadata for RAG
- **Prompt** - AI prompt templates
- **PromptVersion** - Prompt version control
- **AIProviderConfig** - Provider-specific configurations

## Prerequisites

- Python 3.13+
- Node.js 20+
- PostgreSQL 16+ with pgvector extension
- Redis 7+

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the development server**
```bash
python run.py
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Environment Variables

### Backend (.env)

```env
# Application
APP_NAME=Enterprise AI Calling Platform
APP_ENV=development
APP_DEBUG=true
APP_VERSION=0.1.0
API_PREFIX=/api/v1

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_calling_platform
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=false

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=20

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# AI Providers
GEMINI_API_KEY=
SARVAM_API_KEY=
NVIDIA_API_KEY=

# Telephony
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```

## API Documentation

Once the backend is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Health Check

Check system health status:
```bash
curl http://localhost:8000/api/v1/health
```

## Database Migrations

### Create a new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Development Guidelines

### Backend
- Follow async/await patterns for database operations
- Use type hints for all functions
- Implement proper error handling
- Write comprehensive docstrings
- Follow SOLID principles
- Use dependency injection

### Frontend
- Use TypeScript for type safety
- Follow React best practices
- Implement proper error boundaries
- Use TanStack Query for data fetching
- Follow component composition patterns

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Code Quality

### Backend
```bash
cd backend
black .           # Code formatting
ruff check .       # Linting
mypy .            # Type checking
```

### Frontend
```bash
cd frontend
npm run lint       # ESLint
```

## Deployment

### Production Build

**Backend:**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm run build
```

## Architecture Decisions

1. **Multi-tenant by Design**: All core models are organization-scoped for true multi-tenancy
2. **Async-First**: Built on async/await for high concurrency
3. **Provider Abstraction**: AI providers are abstracted to avoid vendor lock-in
4. **Soft Deletes**: Critical data uses soft deletes for data recovery
5. **UUID Primary Keys**: UUIDs for distributed system compatibility
6. **Audit Trail**: All models track creation and modification
7. **Version Control**: Prompts support versioning for A/B testing
8. **RAG-Ready**: Knowledge base structure designed for RAG implementation

## Security Considerations

- All API endpoints require authentication (to be implemented)
- Environment variables for sensitive configuration
- CORS configuration for frontend-backend communication
- SQL injection prevention through ORM
- Input validation via Pydantic schemas

## Performance Considerations

- Database connection pooling
- Redis caching for frequently accessed data
- Async operations for I/O-bound tasks
- Celery for background task processing
- Indexed database columns for query optimization

## Future Roadmap

- [ ] Authentication and authorization (JWT)
- [ ] AI provider integrations (Gemini, Sarvam, NVIDIA)
- [ ] Telephony provider integrations (Twilio, Plivo)
- [ ] Real-time call monitoring (WebSockets)
- [ ] Analytics dashboard
- [ ] Call recording and transcription
- [ ] RAG implementation
- [ ] Advanced agent personality customization
- [ ] Multi-language support
- [ ] Advanced scheduling and time zone handling

## License

Proprietary - All rights reserved

## Support

For technical support, contact the development team.
