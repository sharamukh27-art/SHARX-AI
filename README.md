# SHAR-X AI
## "The Future of Intelligent Assistance. A Machine-Mind, Awakened."

SHAR-X AI is a flagship, production-grade intelligent assistant application combining advanced AI capabilities, local memory management, and a sleek cyberpunk-inspired interface.

**This is NOT a prototype. This is NOT a demo.**

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- Ollama with neural-chat model (for local AI)

### Without Docker

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env

# Initialize database
python -c "from app.db import init_database; init_database()"

# Start backend server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### With Docker

```bash
# Build and start all services
docker-compose up --build

# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
```

---

## Architecture

### Backend (FastAPI)

```
backend/
├── app/
│   ├── ai/                 # AI provider abstraction
│   │   ├── base.py        # Provider interface
│   │   ├── ollama.py      # Ollama implementation
│   │   ├── gemini.py      # Google Gemini implementation
│   │   ├── openai.py      # OpenAI implementation
│   │   └── factory.py     # Provider factory
│   ├── memory/            # Semantic memory with ChromaDB
│   │   └── chroma.py
│   ├── db/                # Database layer
│   │   ├── database.py    # Connection management
│   │   └── models.py      # SQLAlchemy models
│   ├── api/               # API endpoints
│   │   ├── chat.py        # Chat routes
│   │   ├── notes.py       # Notes management
│   │   ├── memory.py      # Memory operations
│   │   └── system.py      # System/health endpoints
│   ├── config/            # Configuration management
│   │   └── settings.py
│   ├── utils/             # Utilities
│   │   └── logger.py
│   └── main.py            # FastAPI application
└── requirements.txt       # Python dependencies
```

### Frontend (React + TypeScript + Vite)

```
frontend/
├── src/
│   ├── components/        # Reusable components
│   ├── pages/            # Page components
│   │   ├── Chat.tsx      # Main chat interface
│   │   ├── Notes.tsx     # Notes management
│   │   └── Settings.tsx  # Settings & system info
│   ├── services/         # API client
│   │   └── api.ts
│   ├── context/          # Global state (Zustand)
│   │   └── store.ts
│   ├── types/            # TypeScript interfaces
│   │   └── index.ts
│   ├── utils/            # Utility functions
│   ├── styles/           # Global styles
│   ├── App.tsx
│   └── main.tsx
├── vite.config.ts
├── tailwind.config.js
└── package.json
```

---

## Configuration

### Environment Variables

Create `.env` in the backend directory:

```env
# FastAPI
FASTAPI_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# AI Provider (ollama, gemini, openai)
AI_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=neural-chat

# Gemini Configuration (optional)
GEMINI_API_KEY=your-api-key
GEMINI_MODEL=gemini-pro

# OpenAI Configuration (optional)
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4-turbo-preview

# Database
DATABASE_URL=sqlite:///./sharx_ai.db

# ChromaDB
CHROMA_PERSIST_DIR=./chroma_data

# CORS Origins
API_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### AI Provider Selection

Switch providers by changing a single configuration value:

```env
AI_PROVIDER=ollama    # Local LLM
AI_PROVIDER=gemini    # Google Gemini
AI_PROVIDER=openai    # OpenAI GPT
```

---

## API Endpoints

### Chat
- `POST /api/chat/` - Send message and get response
- `GET /api/chat/conversations` - List all conversations
- `GET /api/chat/conversations/{id}` - Get specific conversation with history

### System
- `GET /api/system/health` - Health check
- `GET /api/system/stats` - System resource usage
- `GET /api/system/info` - Application information

### Notes
- `POST /api/notes/` - Create note
- `GET /api/notes/` - List all notes
- `GET /api/notes/{id}` - Get specific note
- `PUT /api/notes/{id}` - Update note
- `DELETE /api/notes/{id}` - Delete note

### Memory (Semantic)
- `POST /api/memory/add` - Add to semantic memory
- `POST /api/memory/query` - Query semantic memory
- `GET /api/memory/all` - Get all stored memories

---

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: SQLAlchemy + SQLite
- **Semantic Memory**: ChromaDB
- **Validation**: Pydantic
- **Configuration**: python-dotenv + pydantic-settings
- **AI Providers**: Ollama, Google Gemini, OpenAI
- **Code Quality**: Black, Ruff

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Animation**: Framer Motion
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Routing**: React Router
- **Code Quality**: ESLint, Prettier

---

## Phase 1 Implementation

✓ Project structure
✓ Backend FastAPI setup
✓ Frontend React + Vite setup
✓ Provider abstraction (Ollama, Gemini, OpenAI)
✓ Database models (SQLAlchemy)
✓ ChromaDB semantic memory
✓ API endpoints (Chat, Notes, Memory, System)
✓ Global state management (Zustand)
✓ Basic UI components
✓ Docker support
✓ Configuration management

---

## Future Phases

### Phase 2: Core Features
- Streaming chat responses
- Markdown rendering with syntax highlighting
- Conversation history management
- Long-term memory integration
- Reminders and notifications
- Weather integration
- Calculator utilities
- System monitoring

### Phase 3: Automation
- Application launcher
- Website opener
- Browser control
- File operations
- Safe terminal execution
- Clipboard management
- System notifications

### Phase 4: UI/UX Enhancement
- Cyberpunk design (Blade Runner 2049 inspired)
- Animated HUD elements
- Glassmorphism effects
- Neon cyan + magenta color scheme
- Particle background animations
- Robotic orb avatar
- Waveform ring visualization
- Real-time telemetry display
- GPU-accelerated animations

### Phase 5: Advanced Features
- Vision capabilities
- OCR
- Face recognition
- PDF assistant
- Coding assistant
- Plugin system
- Spotify integration
- Calendar management
- Email assistance
- Browser AI

---

## Development Commands

### Backend

```bash
# Format code
black app/

# Lint
ruff check app/

# Tests
pytest

# Run server
python -m uvicorn app.main:app --reload
```

### Frontend

```bash
# Format code
npm run format

# Lint
npm run lint

# Type check
npm run type-check

# Build
npm run build

# Dev server
npm run dev
```

---

## Database

### Models
- **Conversation** - Chat conversation metadata
- **Message** - Individual chat messages
- **Memory** - Long-term memory storage
- **Note** - User notes
- **Reminder** - Scheduled reminders
- **Settings** - Application settings

### Initialization

```python
from app.db import init_database
init_database()
```

---

## Logging

Logs are stored in `logs/sharx_ai.log` with:
- Rotating file handler (10MB max per file, 10 backups)
- Console output
- Configurable log level

---

## Contributing

This is a production-grade application. All code must:
- Follow type-safe principles
- Include proper error handling
- Be thoroughly tested
- Maintain clean architecture
- Have clear documentation

---

## License

Proprietary - All rights reserved

---

**SHAR-X AI: The Future of Intelligent Assistance**

*A Machine-Mind, Awakened.*
