# 🚀 Quick Start Guide

Get the Docs-to-App platform running in 5 minutes!

## Prerequisites

You need:
- **Anthropic API Key** - Get one at https://console.anthropic.com
- **Docker & Docker Compose** - For easy deployment
  - OR Python 3.11+ and Node.js 20+ for local development

## Fastest Way (Docker)

### Step 1: Get Your API Key

1. Go to https://console.anthropic.com
2. Sign up / Log in
3. Create an API key
4. Copy the key (starts with `sk-ant-`)

### Step 2: Configure Environment

```bash
cd docs-to-app
cp .env.example .env
```

Edit `.env` and add your API key:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Step 3: Start the Application

```bash
./start.sh
```

Or manually:
```bash
docker-compose up --build
```

### Step 4: Open Your Browser

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## What to Try First

### Example 1: Use the DSA README

1. Go to http://localhost:3000
2. Click "Paste Text"
3. Copy the content from the parent directory's README.md (the DSA guide)
4. Click "Analyze Documentation"
5. Wait 10-20 seconds for AI analysis
6. Explore the concepts, sections, and examples
7. Click "Generate Interactive Learning App"
8. Choose "Interactive Playground"
9. Click "Generate"
10. Try editing and running the code examples!

### Example 2: Use Any GitHub README

1. Go to any GitHub repository
2. Find the README.md file
3. Click "Raw" to get the raw markdown
4. Copy the URL
5. In the app, click "From URL"
6. Paste the URL
7. Click "Analyze Documentation"

### Example 3: Upload Your Own Docs

1. Create a markdown file with your documentation
2. In the app, click "Upload File"
3. Select your .md file
4. Click "Analyze Documentation"

## Understanding the Output

### Analysis View

You'll see:
- **Key Concepts**: Main topics extracted by AI
- **Sections**: Document structure with difficulty levels
- **Code Examples**: Extracted code with explanations
- **Learning Path**: Recommended order to learn concepts

### Generated Apps

Three types available:

1. **Interactive Playground**
   - Live code editor (Monaco)
   - Run examples in real-time
   - Multiple examples to try
   - Syntax highlighting

2. **Step-by-Step Tutorial**
   - Guided learning experience
   - Progress tracking
   - Next/Previous navigation
   - Completion tracking

3. **Demo Application**
   - Working demonstration
   - Based on documentation
   - Interactive examples

## Common Issues

### "API key not configured"

**Solution**: Make sure you added your key to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### "Connection refused" or "Network error"

**Solution**: Check if backend is running:
```bash
docker-compose ps
# Should show both backend and frontend as "Up"
```

### "Analysis taking too long"

**Reason**: Claude API can take 10-30 seconds for analysis

**What's happening**: The AI is reading your entire documentation, extracting concepts, analyzing code examples, and creating a structured learning path.

### Docker not starting

**Solution**: Check Docker is running:
```bash
docker --version
docker-compose --version
```

If not installed, visit https://docs.docker.com/get-docker/

## Local Development (Without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
python main.py
```

Backend runs at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Frontend runs at http://localhost:3000

## Tips for Best Results

### Documentation Tips

**Good Documentation for Analysis:**
- Has clear structure (headings)
- Includes code examples
- Has explanations, not just code
- Uses markdown formatting
- Contains practical examples

**Examples:**
- GitHub README files
- API documentation
- Tutorial content
- SDK guides
- Technical blog posts

### Optimal Length

- **Too short** (< 500 words): Not enough content for meaningful analysis
- **Good** (500-5000 words): Perfect for analysis
- **Too long** (> 10,000 words): May hit context limits

### Best Practices

1. **Start Simple**: Try the DSA README first
2. **Experiment**: Try different types of documentation
3. **Iterate**: Analyze multiple docs to see patterns
4. **Customize**: The generated code is editable!

## What to Expect

### Analysis Time

- Small docs (< 1000 words): 5-10 seconds
- Medium docs (1000-3000 words): 10-20 seconds
- Large docs (> 3000 words): 20-40 seconds

### Quality

The AI will:
- Extract key concepts accurately
- Identify patterns and themes
- Generate working code examples
- Create meaningful learning paths
- Adapt to content difficulty

## Next Steps

1. ✅ Run the application
2. ✅ Try the DSA README example
3. ✅ Experiment with different docs
4. ✅ Explore the code playground
5. 📚 Check out ARCHITECTURE.md for technical details
6. 🛠️ Read README.md for full documentation
7. 🎨 Customize the frontend styling
8. 🚀 Deploy to production

## Getting Help

- **API Errors**: Check http://localhost:8000/docs
- **Frontend Issues**: Check browser console (F12)
- **Backend Logs**: `docker-compose logs backend`
- **Frontend Logs**: `docker-compose logs frontend`

## Stop the Application

```bash
docker-compose down
```

## Congratulations! 🎉

You now have a working GenAI documentation platform!

Try analyzing different types of documentation and see what amazing learning experiences you can create.

---

**Questions?** Check the full README.md or ARCHITECTURE.md

**Ready to customize?** All code is in `backend/` and `frontend/` directories

**Want to contribute?** See the Contributing section in README.md
