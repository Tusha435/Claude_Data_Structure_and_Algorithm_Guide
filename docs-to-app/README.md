# 🚀 Docs-to-App - GenAI Documentation Platform

Transform any documentation into interactive learning experiences using GenAI.

## ✨ What is this?

This is a **GenAI-powered web application** that takes technical documentation (README files, API docs, SDK documentation) and automatically generates:

- 📚 **Interactive Learning Apps** - Turn static docs into engaging experiences
- 💻 **Code Playgrounds** - Live code editors with examples from the docs
- 📊 **Visual Diagrams** - Auto-generated Mermaid diagrams
- 🎓 **Step-by-Step Tutorials** - Guided learning paths
- 🔍 **Intelligent Analysis** - Claude AI extracts concepts, patterns, and structure

## 🎯 The Problem This Solves

**Real Problems:**
- Documentation is long, hard to navigate, and boring
- Developers want examples and interactive learning
- Onboarding takes too long
- Learning new frameworks/SDKs is tedious

**This Solution:**
- Paste any documentation → Get an interactive learning app
- Live code examples you can edit and run
- Visual diagrams generated automatically
- Personalized learning paths

## 🏗️ Architecture

```
docs-to-app/
├── backend/                 # FastAPI backend
│   ├── main.py             # API endpoints
│   ├── services/           # Core services
│   │   ├── doc_parser.py   # Parse markdown/HTML
│   │   ├── llm_service.py  # Claude AI integration
│   │   ├── code_generator.py # Generate apps
│   │   └── diagram_generator.py # Mermaid diagrams
│   └── requirements.txt
│
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js 14 app router
│   ├── components/        # React components
│   │   ├── DocumentUploader.tsx
│   │   ├── AnalysisView.tsx
│   │   ├── AppGenerator.tsx
│   │   └── CodePlayground.tsx
│   └── package.json
│
└── docker-compose.yml     # Docker deployment
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional)
- Anthropic API key (get one at https://console.anthropic.com)

### Option 1: Run with Docker (Recommended)

1. **Clone the repository**
   ```bash
   cd docs-to-app
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the app**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Run Locally

#### Backend Setup

1. **Navigate to backend**
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

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

5. **Run the server**
   ```bash
   python main.py
   # Or: uvicorn main:app --reload
   ```

Backend will be running at http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment**
   ```bash
   cp .env.local.example .env.local
   # Should contain: NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

Frontend will be running at http://localhost:3000

## 🎮 How to Use

### 1. Upload Documentation

Choose one of three methods:

- **Paste Text** - Copy/paste your README or documentation
- **From URL** - Provide a GitHub README URL or documentation link
- **Upload File** - Upload .md, .txt, or .rst files

**Try it with the DSA README!** Copy the content from the Data Structures & Algorithms README in the parent directory.

### 2. View Analysis

The AI will analyze your documentation and extract:

- Key concepts and topics
- Code examples with explanations
- Suggested learning path
- Difficulty levels
- Patterns and themes

### 3. Generate Interactive App

Choose your learning experience:

- **Interactive Playground** - Code editor with live execution
- **Step-by-Step Tutorial** - Guided learning with progress tracking
- **Demo Application** - Working demonstration of concepts

### 4. Learn!

- Edit and run code examples
- Follow the learning path
- View auto-generated diagrams
- Track your progress

## 🎨 Features

### Core Features

- ✅ **Multi-format Support** - Markdown, HTML, text, URLs
- ✅ **AI-Powered Analysis** - Claude Sonnet 4.5 for deep understanding
- ✅ **Code Playground** - Monaco editor with syntax highlighting
- ✅ **Visual Diagrams** - Mermaid diagram generation
- ✅ **Interactive UI** - Modern, responsive design with Tailwind CSS
- ✅ **Learning Paths** - Personalized progression through content
- ✅ **Real-time Code Execution** - Run examples in sandboxed environment

### Backend Features

- FastAPI REST API
- Document parsing (Markdown, HTML)
- Claude AI integration (Anthropic SDK)
- Code generation
- Diagram generation (Mermaid)
- CORS enabled for local development

### Frontend Features

- Next.js 14 with App Router
- React 18 with TypeScript
- Monaco Code Editor
- Tailwind CSS styling
- Lucide React icons
- Mermaid diagram rendering
- Responsive design

## 🔧 API Endpoints

### Documentation Parsing

```bash
POST /api/parse/url
POST /api/parse/text
POST /api/parse/file
```

### Generation

```bash
POST /api/generate/app
POST /api/generate/diagram
POST /api/generate/example
```

### Health

```bash
GET /
GET /api/health
```

Full API documentation available at http://localhost:8000/docs

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **Anthropic Claude** - Claude Sonnet 4.5 for AI
- **BeautifulSoup4** - HTML parsing
- **Markdown** - Markdown processing
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend

- **Next.js 14** - React framework
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Monaco Editor** - Code editor (same as VS Code)
- **Axios** - HTTP client
- **Lucide React** - Icons
- **Mermaid** - Diagram rendering

### Infrastructure

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 🎯 Use Cases

### For Developers

- Learn new frameworks/libraries faster
- Understand complex codebases
- Create interactive documentation for your projects
- Build internal developer tools

### For Companies

- Improve developer onboarding
- Create better documentation experiences
- Build interactive product demos
- Enhance API documentation

### For Educators

- Create interactive coding tutorials
- Transform textbooks into engaging apps
- Build student-friendly learning materials
- Generate practice exercises

### For Students

- Learn data structures & algorithms interactively
- Practice coding with immediate feedback
- Visualize complex concepts
- Follow personalized learning paths

## 🚦 Roadmap

### Current (MVP)

- ✅ Documentation parsing
- ✅ AI analysis with Claude
- ✅ Code playground generation
- ✅ Basic diagram generation
- ✅ Web interface

### Planned Features

- [ ] More app types (quiz apps, flashcards, mindmaps)
- [ ] Code execution sandboxing (Docker containers)
- [ ] Save and share generated apps
- [ ] Multi-language support (Java, JavaScript, Go, etc.)
- [ ] GitHub integration (auto-import repos)
- [ ] Collaborative learning features
- [ ] Progress tracking and analytics
- [ ] Export to standalone HTML
- [ ] API key management UI
- [ ] Template system for custom apps

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (if available)
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Claude](https://anthropic.com/claude) by Anthropic
- Inspired by the need for better developer documentation experiences
- Thanks to the open-source community

## 📧 Contact & Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check the API docs at `/docs`
- **Ideas**: Open a discussion or issue

## 🌟 Why This Matters

This project demonstrates the **real-world application of GenAI** beyond simple chatbots:

1. **Solves Real Problems** - Makes learning from documentation easier
2. **Production-Ready** - Built with industry-standard tools
3. **Scalable** - Dockerized, modular architecture
4. **Extensible** - Easy to add new features and app types
5. **Practical** - Actually useful for developers

## 🎓 Perfect For

- 📚 **Portfolio Projects** - Shows GenAI, full-stack, and system design skills
- 💼 **Startup Ideas** - Could be a SaaS product
- 🎯 **Technical Interviews** - Demonstrates architecture and problem-solving
- 🚀 **Hackathons** - Complete, working MVP
- 📖 **Learning** - Hands-on GenAI application development

---

**Ready to transform documentation into interactive experiences?** 🚀

Get started:
```bash
cd docs-to-app
cp .env.example .env
# Add your ANTHROPIC_API_KEY
docker-compose up
# Visit http://localhost:3000
```

Happy learning! 🎉
