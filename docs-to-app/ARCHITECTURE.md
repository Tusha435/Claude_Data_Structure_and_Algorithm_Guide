# Architecture Overview

## System Design

This document explains the architecture and design decisions for the Docs-to-App GenAI platform.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                          │
│                    (React / Next.js App)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                     FastAPI Backend                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Parser    │  │  LLM Service │  │  Generator   │       │
│  │   Service   │  │   (Claude)   │  │   Service    │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────┬───────────────────────────────────────┘
                      │ Anthropic API
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Anthropic Claude API                         │
│                  (Sonnet 4.5 Model)                          │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Frontend (Next.js + React)

**Purpose**: User interface for uploading docs and interacting with generated apps

**Key Features**:
- Document upload (text, URL, file)
- Analysis visualization
- Code playground
- Interactive tutorials

**Technology Choices**:
- **Next.js 14**: Modern React framework with App Router
- **TypeScript**: Type safety and better DX
- **Tailwind CSS**: Rapid UI development
- **Monaco Editor**: Professional code editing experience

**Component Structure**:
```
app/
├── page.tsx              # Main application page
├── layout.tsx            # Root layout
└── globals.css           # Global styles

components/
├── DocumentUploader.tsx  # Upload interface
├── AnalysisView.tsx      # Show analysis results
├── AppGenerator.tsx      # Generate app selector
└── CodePlayground.tsx    # Interactive code editor
```

### 2. Backend (FastAPI)

**Purpose**: API server for document processing and AI orchestration

**Key Features**:
- RESTful API endpoints
- Document parsing (Markdown, HTML)
- Claude AI integration
- Code and diagram generation

**Technology Choices**:
- **FastAPI**: Modern, fast Python web framework
- **Pydantic**: Data validation and serialization
- **Anthropic SDK**: Official Claude API client
- **BeautifulSoup4**: HTML parsing
- **Markdown**: Markdown processing

**Service Architecture**:
```
services/
├── doc_parser.py         # Parse various doc formats
├── llm_service.py        # Claude AI integration
├── code_generator.py     # Generate app code
└── diagram_generator.py  # Create Mermaid diagrams
```

### 3. LLM Integration (Claude)

**Purpose**: AI-powered analysis and generation

**Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250514)

**Key Operations**:
1. **Documentation Analysis**
   - Extract concepts and patterns
   - Identify code examples
   - Structure learning paths
   - Assess difficulty levels

2. **Code Generation**
   - Create interactive playgrounds
   - Generate tutorial steps
   - Produce demo applications

3. **Diagram Generation**
   - Convert concepts to Mermaid syntax
   - Create flowcharts and architecture diagrams

**Prompt Engineering**:
- Structured JSON responses
- Context-aware generation
- Educational focus
- Clear, actionable outputs

## Data Flow

### Document Upload Flow

```
1. User uploads documentation
   ↓
2. Frontend sends to /api/parse/{method}
   ↓
3. Backend parses document structure
   ↓
4. LLM analyzes content (Claude API)
   ↓
5. Structured analysis returned to frontend
   ↓
6. User views analysis and concepts
```

### App Generation Flow

```
1. User selects app type (playground/tutorial/demo)
   ↓
2. Frontend sends to /api/generate/app
   ↓
3. Backend retrieves analysis
   ↓
4. LLM generates app code (Claude API)
   ↓
5. Generated code returned to frontend
   ↓
6. Frontend renders interactive app
```

## API Design

### REST Principles

- **Resource-based URLs**: `/api/parse/text`, `/api/generate/app`
- **HTTP Methods**: POST for operations with side effects
- **Status Codes**: Proper use of 200, 400, 500
- **JSON Responses**: Consistent data format

### Endpoints

```
POST /api/parse/url       - Parse from URL
POST /api/parse/text      - Parse from text
POST /api/parse/file      - Parse from uploaded file
POST /api/generate/app    - Generate interactive app
POST /api/generate/diagram - Generate diagram
POST /api/generate/example - Generate code example
GET  /api/health          - Health check
```

### Request/Response Models

All models use Pydantic for validation:

```python
class DocumentTextRequest(BaseModel):
    content: str
    doc_type: Optional[str] = "readme"
    title: Optional[str] = "Documentation"

class AnalysisResponse(BaseModel):
    title: str
    sections: List[Dict[str, Any]]
    concepts: List[str]
    examples: List[Dict[str, Any]]
    summary: str
```

## Security Considerations

### Current Implementation

1. **CORS**: Enabled for local development (localhost:3000)
2. **Input Validation**: Pydantic models validate all inputs
3. **API Key Security**: Environment variables for sensitive data
4. **Code Execution**: Currently simulated (security risk)

### Production Recommendations

1. **Code Sandboxing**
   - Use Docker containers for code execution
   - Implement timeout limits
   - Resource constraints (CPU, memory)
   - Network isolation

2. **Rate Limiting**
   - Implement per-user/IP rate limits
   - Protect against API abuse
   - Claude API cost control

3. **Authentication**
   - Add user authentication
   - API key management
   - Usage tracking

4. **Input Sanitization**
   - Validate uploaded files
   - Sanitize URLs
   - Prevent injection attacks

## Scalability

### Current Limitations

- Single instance deployment
- No caching
- No database for persistence
- Synchronous processing

### Scaling Strategy

1. **Horizontal Scaling**
   - Stateless backend (easy to replicate)
   - Load balancer (nginx/HAProxy)
   - Multiple backend instances

2. **Caching**
   - Redis for analysis results
   - CDN for frontend static assets
   - Claude API response caching

3. **Database**
   - PostgreSQL for persistent storage
   - Store analyses for reuse
   - User data and preferences

4. **Async Processing**
   - Celery for background tasks
   - Queue long-running operations
   - WebSocket for real-time updates

5. **Infrastructure**
   - Kubernetes for orchestration
   - Auto-scaling based on load
   - Multi-region deployment

## Development Workflow

### Local Development

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Docker Development

```bash
docker-compose up --build
```

### Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with orchestration
kubectl apply -f k8s/
```

## Design Decisions

### Why FastAPI?

- Modern, fast Python framework
- Automatic API documentation (Swagger)
- Async support for scalability
- Type hints and validation
- Great developer experience

### Why Next.js?

- Server-side rendering (SSR)
- Great developer experience
- Built-in optimization
- Easy deployment (Vercel)
- TypeScript support

### Why Claude?

- Excellent code understanding
- Long context window (200K tokens)
- Structured output support
- Safety and reliability
- Latest model (Sonnet 4.5)

### Why Monaco Editor?

- Same editor as VS Code
- Excellent syntax highlighting
- IntelliSense support
- Highly customizable
- Great performance

## Testing Strategy

### Backend Testing

```python
# Unit tests
pytest tests/test_doc_parser.py
pytest tests/test_llm_service.py

# Integration tests
pytest tests/test_api.py

# Coverage
pytest --cov=services tests/
```

### Frontend Testing

```bash
# Component tests
npm test

# E2E tests
npm run test:e2e
```

## Monitoring & Observability

### Recommended Tools

1. **Logging**
   - Structured logging (JSON)
   - Log aggregation (ELK stack)
   - Error tracking (Sentry)

2. **Metrics**
   - Prometheus for metrics
   - Grafana for visualization
   - Claude API usage tracking

3. **Tracing**
   - OpenTelemetry
   - Distributed tracing
   - Performance monitoring

## Future Architecture

### Microservices Evolution

```
┌─────────────────────────────────────────┐
│           API Gateway (Kong)             │
└─────────────┬───────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼────┐ ┌─▼──────┐
│Parser │ │  AI   │ │Generator│
│Service│ │Service│ │ Service │
└───────┘ └───────┘ └─────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼────┐ ┌─▼──────┐ ┌▼───────┐
│PostgreSQL│ │ Redis  │ │RabbitMQ│
└──────────┘ └────────┘ └────────┘
```

### Key Improvements

1. Service isolation
2. Independent scaling
3. Language flexibility
4. Fault tolerance
5. Better monitoring

## Conclusion

This architecture provides:

- **Modularity**: Clear separation of concerns
- **Scalability**: Designed to scale horizontally
- **Maintainability**: Clean code structure
- **Extensibility**: Easy to add features
- **Production-ready**: With recommended improvements

The system demonstrates real-world GenAI application beyond simple chatbots, with practical architecture suitable for production deployment.
