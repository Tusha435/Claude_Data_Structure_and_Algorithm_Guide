"""
GenAI Docs-to-App Web Application
Main FastAPI Backend
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

from services.doc_parser import DocumentParser
from services.llm_service import LLMService
from services.code_generator import CodeGenerator
from services.diagram_generator import DiagramGenerator
from services.openapi_parser import OpenAPIParser

load_dotenv()

app = FastAPI(
    title="Docs-to-App GenAI Platform",
    description="Transform documentation into interactive learning experiences",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
doc_parser = DocumentParser()
openapi_parser = OpenAPIParser()
llm_service = LLMService(api_key=os.getenv("ANTHROPIC_API_KEY"))
code_generator = CodeGenerator(llm_service)
diagram_generator = DiagramGenerator(llm_service)


# Request/Response Models
class DocumentURLRequest(BaseModel):
    url: HttpUrl
    doc_type: Optional[str] = "readme"


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


class GenerateAppRequest(BaseModel):
    analysis_id: str
    app_type: str  # "playground", "tutorial", "demo"
    features: List[str]


class GeneratedApp(BaseModel):
    app_id: str
    frontend_code: str
    backend_code: Optional[str]
    diagrams: List[str]
    explanation: str


# Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Docs-to-App GenAI Platform",
        "version": "1.0.0"
    }


@app.post("/api/parse/url", response_model=AnalysisResponse)
async def parse_documentation_url(request: DocumentURLRequest):
    """
    Parse documentation from a URL

    This endpoint:
    1. Fetches content from the URL
    2. Parses and structures the documentation
    3. Analyzes with LLM to extract concepts and patterns
    4. Returns structured analysis
    """
    try:
        # Fetch and parse document
        doc_content = await doc_parser.fetch_from_url(str(request.url))
        parsed_doc = doc_parser.parse_markdown(doc_content)

        # Analyze with LLM
        analysis = await llm_service.analyze_documentation(
            content=parsed_doc,
            doc_type=request.doc_type
        )

        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/parse/text", response_model=AnalysisResponse)
async def parse_documentation_text(request: DocumentTextRequest):
    """
    Parse documentation from raw text/markdown

    Perfect for pasting README content directly
    """
    try:
        # Parse document
        parsed_doc = doc_parser.parse_markdown(request.content)

        # Analyze with LLM
        analysis = await llm_service.analyze_documentation(
            content=parsed_doc,
            doc_type=request.doc_type,
            title=request.title
        )

        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/parse/file")
async def parse_documentation_file(file: UploadFile = File(...)):
    """
    Parse documentation from uploaded file

    Supports: .md, .txt, .rst
    """
    try:
        content = await file.read()
        content_str = content.decode('utf-8')

        # Parse document
        parsed_doc = doc_parser.parse_markdown(content_str)

        # Analyze with LLM
        analysis = await llm_service.analyze_documentation(
            content=parsed_doc,
            doc_type="readme",
            title=file.filename
        )

        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/app", response_model=GeneratedApp)
async def generate_application(request: GenerateAppRequest):
    """
    Generate interactive application from documentation analysis

    Takes the analysis and generates:
    - Interactive frontend code
    - Backend API (if needed)
    - Visual diagrams
    - Step-by-step explanations
    """
    try:
        # This would typically fetch stored analysis
        # For MVP, we'll generate based on provided ID

        generated_app = await code_generator.generate_app(
            analysis_id=request.analysis_id,
            app_type=request.app_type,
            features=request.features
        )

        return generated_app
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/diagram")
async def generate_diagram(concept: str, context: str):
    """
    Generate Mermaid diagram for a specific concept
    """
    try:
        diagram = await diagram_generator.generate_mermaid_diagram(
            concept=concept,
            context=context
        )

        return {"diagram": diagram, "type": "mermaid"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/example")
async def generate_code_example(concept: str, language: str = "python"):
    """
    Generate executable code example for a concept
    """
    try:
        example = await code_generator.generate_example(
            concept=concept,
            language=language
        )

        return example
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/parse/openapi")
async def parse_openapi_spec(url: str = None, spec: Dict[str, Any] = None):
    """
    Parse OpenAPI/Swagger specification

    Supports:
    - OpenAPI 3.0/3.1
    - Swagger 2.0
    - From URL or direct JSON/YAML

    Perfect for API documentation!
    """
    try:
        if url:
            # Parse from URL
            api_analysis = await openapi_parser.parse_from_url(url)
        elif spec:
            # Parse from provided spec
            api_analysis = await openapi_parser.parse_spec(spec)
        else:
            raise HTTPException(
                status_code=400,
                detail="Must provide either 'url' or 'spec'"
            )

        # Enhance with LLM analysis
        enhanced_analysis = await llm_service.analyze_api_documentation(
            api_data=api_analysis
        )

        return {
            **api_analysis,
            'ai_insights': enhanced_analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/api-playground")
async def generate_api_playground(endpoints: List[Dict[str, Any]], auth_config: Dict[str, Any]):
    """
    Generate interactive API playground

    Creates a full testing interface for API endpoints
    """
    try:
        playground_code = await code_generator.generate_api_playground(
            endpoints=endpoints,
            auth_config=auth_config
        )

        return playground_code

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/sdk-example")
async def generate_sdk_example(
    endpoint: Dict[str, Any],
    language: str = "python"
):
    """
    Generate SDK code example for specific endpoint

    Supports: python, javascript, curl, ruby, php, go, java
    """
    try:
        sdk_code = await code_generator.generate_sdk_code(
            endpoint=endpoint,
            language=language
        )

        return {
            'language': language,
            'code': sdk_code,
            'endpoint': endpoint
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "llm": "connected" if llm_service.client else "disconnected",
            "parser": "ready",
            "openapi_parser": "ready",
            "generator": "ready"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
