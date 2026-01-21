"""
Code Generator Service
Generates interactive applications from documentation analysis
"""
from typing import Dict, List, Any
import uuid
from .llm_service import LLMService


class CodeGenerator:
    """Generate code for interactive learning apps"""

    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def generate_app(
        self,
        analysis_id: str,
        app_type: str,
        features: List[str]
    ) -> Dict[str, Any]:
        """
        Generate complete application code

        App types:
        - playground: Interactive code editor
        - tutorial: Step-by-step guided learning
        - demo: Working demonstration app
        """
        app_id = str(uuid.uuid4())

        if app_type == "playground":
            return await self._generate_playground(app_id, features)
        elif app_type == "tutorial":
            return await self._generate_tutorial(app_id, features)
        elif app_type == "demo":
            return await self._generate_demo(app_id, features)
        else:
            raise ValueError(f"Unknown app type: {app_type}")

    async def _generate_playground(
        self,
        app_id: str,
        features: List[str]
    ) -> Dict[str, Any]:
        """
        Generate interactive code playground

        Features like: code execution, syntax highlighting, examples
        """
        frontend_code = """
import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import { Play, RotateCcw, BookOpen } from 'lucide-react';

export default function CodePlayground() {
  const [code, setCode] = useState(`def example():
    print("Hello from the playground!")
    return True

example()`);
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);

  const runCode = async () => {
    setIsRunning(true);
    try {
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language: 'python' })
      });
      const result = await response.json();
      setOutput(result.output);
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    }
    setIsRunning(false);
  };

  const resetCode = () => {
    setCode(`def example():
    print("Hello from the playground!")
    return True

example()`);
    setOutput('');
  };

  return (
    <div className="h-screen flex flex-col bg-gray-900">
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <BookOpen className="w-6 h-6 text-blue-400" />
            <h1 className="text-xl font-bold text-white">Interactive Code Playground</h1>
          </div>
          <div className="flex gap-2">
            <button
              onClick={resetCode}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg flex items-center gap-2 transition"
            >
              <RotateCcw className="w-4 h-4" />
              Reset
            </button>
            <button
              onClick={runCode}
              disabled={isRunning}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2 transition disabled:opacity-50"
            >
              <Play className="w-4 h-4" />
              {isRunning ? 'Running...' : 'Run Code'}
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Code Editor */}
        <div className="flex-1 border-r border-gray-700">
          <Editor
            height="100%"
            defaultLanguage="python"
            theme="vs-dark"
            value={code}
            onChange={(value) => setCode(value || '')}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              lineNumbers: 'on',
              scrollBeyondLastLine: false,
              automaticLayout: true,
            }}
          />
        </div>

        {/* Output Panel */}
        <div className="w-1/3 bg-gray-800 flex flex-col">
          <div className="p-3 border-b border-gray-700">
            <h2 className="text-sm font-semibold text-gray-300">Output</h2>
          </div>
          <div className="flex-1 p-4 overflow-auto">
            <pre className="text-sm text-gray-100 font-mono whitespace-pre-wrap">
              {output || 'Run code to see output...'}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
"""

        backend_code = """
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
from io import StringIO
import contextlib

app = FastAPI()

class CodeExecutionRequest(BaseModel):
    code: str
    language: str

@app.post("/api/execute")
async def execute_code(request: CodeExecutionRequest):
    if request.language != "python":
        raise HTTPException(status_code=400, detail="Only Python supported")

    # Capture output
    output_buffer = StringIO()

    try:
        with contextlib.redirect_stdout(output_buffer):
            # Execute in sandbox
            exec(request.code, {"__builtins__": __builtins__})

        return {"output": output_buffer.getvalue(), "error": None}
    except Exception as e:
        return {"output": "", "error": str(e)}
"""

        return {
            "app_id": app_id,
            "frontend_code": frontend_code,
            "backend_code": backend_code,
            "diagrams": [],
            "explanation": "Interactive code playground with live execution. Users can write code, run it, and see output in real-time."
        }

    async def _generate_tutorial(
        self,
        app_id: str,
        features: List[str]
    ) -> Dict[str, Any]:
        """
        Generate step-by-step tutorial interface
        """
        frontend_code = """
import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, CheckCircle } from 'lucide-react';

const tutorialSteps = [
  {
    title: "Introduction",
    content: "Welcome to this interactive tutorial!",
    code: "# Step 1: Getting started\\nprint('Hello, World!')"
  },
  // More steps...
];

export default function TutorialApp() {
  const [currentStep, setCurrentStep] = useState(0);
  const [completed, setCompleted] = useState(new Set());

  const markComplete = () => {
    setCompleted(new Set([...completed, currentStep]));
  };

  const step = tutorialSteps[currentStep];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto p-6">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium">Progress</span>
            <span className="text-sm text-gray-600">
              {currentStep + 1} / {tutorialSteps.length}
            </span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full">
            <div
              className="h-2 bg-blue-600 rounded-full transition-all"
              style={{ width: `${((currentStep + 1) / tutorialSteps.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Content */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h1 className="text-3xl font-bold mb-4">{step.title}</h1>
          <div className="prose max-w-none mb-6">
            <p>{step.content}</p>
          </div>

          {/* Code Example */}
          {step.code && (
            <div className="bg-gray-900 rounded-lg p-4 mb-6">
              <pre className="text-gray-100 text-sm overflow-x-auto">
                {step.code}
              </pre>
            </div>
          )}

          {/* Navigation */}
          <div className="flex justify-between items-center mt-8">
            <button
              onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
              disabled={currentStep === 0}
              className="px-4 py-2 flex items-center gap-2 border rounded-lg disabled:opacity-50"
            >
              <ChevronLeft className="w-4 h-4" />
              Previous
            </button>

            <button
              onClick={markComplete}
              className="px-6 py-2 bg-green-600 text-white rounded-lg flex items-center gap-2"
            >
              <CheckCircle className="w-4 h-4" />
              Complete Step
            </button>

            <button
              onClick={() => setCurrentStep(Math.min(tutorialSteps.length - 1, currentStep + 1))}
              disabled={currentStep === tutorialSteps.length - 1}
              className="px-4 py-2 flex items-center gap-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
            >
              Next
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
"""

        return {
            "app_id": app_id,
            "frontend_code": frontend_code,
            "backend_code": None,
            "diagrams": [],
            "explanation": "Step-by-step tutorial with progress tracking and interactive examples."
        }

    async def _generate_demo(
        self,
        app_id: str,
        features: List[str]
    ) -> Dict[str, Any]:
        """
        Generate working demonstration app
        """
        return {
            "app_id": app_id,
            "frontend_code": "// Demo app code",
            "backend_code": "# Demo API code",
            "diagrams": [],
            "explanation": "Working demonstration of the concepts"
        }

    async def generate_example(
        self,
        concept: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Generate standalone code example for a concept
        """
        prompt = f"""Generate a clear, executable code example demonstrating: {concept}

Language: {language}

Requirements:
1. Include helpful comments
2. Show input/output
3. Demonstrate the concept clearly
4. Keep it under 30 lines

Return JSON:
{{
    "code": "the code",
    "explanation": "what it does",
    "input": "example input",
    "output": "expected output"
}}"""

        try:
            response = await self.llm.client.messages.create(
                model=self.llm.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            content_text = response.content[0].text

            # Extract JSON
            import json
            if "```json" in content_text:
                json_text = content_text.split("```json")[1].split("```")[0]
            elif "```" in content_text:
                json_text = content_text.split("```")[1].split("```")[0]
            else:
                json_text = content_text

            return json.loads(json_text.strip())

        except Exception as e:
            raise Exception(f"Example generation failed: {str(e)}")

    async def generate_api_playground(
        self,
        endpoints: List[Dict[str, Any]],
        auth_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate interactive API testing playground

        This is the killer feature for API companies!
        """
        frontend_code = """
import React, { useState } from 'react';
import { Play, Key, Globe, ChevronRight } from 'lucide-react';

export default function APIPlayground({ endpoints, authConfig }) {
  const [selectedEndpoint, setSelectedEndpoint] = useState(endpoints[0]);
  const [apiKey, setApiKey] = useState('');
  const [requestParams, setRequestParams] = useState({});
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const makeRequest = async () => {
    setIsLoading(true);
    try {
      const headers = {
        'Content-Type': 'application/json',
      };

      if (authConfig.type === 'apiKey') {
        headers[authConfig.headerName || 'Authorization'] =
          `${authConfig.prefix || 'Bearer'} ${apiKey}`;
      }

      const url = `${authConfig.baseUrl}${selectedEndpoint.path}`;

      const options = {
        method: selectedEndpoint.method,
        headers,
      };

      if (['POST', 'PUT', 'PATCH'].includes(selectedEndpoint.method)) {
        options.body = JSON.stringify(requestParams);
      }

      const res = await fetch(url, options);
      const data = await res.json();

      setResponse({
        status: res.status,
        statusText: res.statusText,
        data,
      });
    } catch (error) {
      setResponse({
        status: 0,
        statusText: 'Error',
        data: { error: error.message },
      });
    }
    setIsLoading(false);
  };

  return (
    <div className="h-screen flex bg-gray-50">
      {/* Sidebar - Endpoints */}
      <div className="w-80 bg-white border-r overflow-y-auto">
        <div className="p-4 border-b">
          <h2 className="font-bold text-lg">API Endpoints</h2>
          <p className="text-sm text-gray-600">{endpoints.length} available</p>
        </div>
        <div className="p-2">
          {endpoints.map((endpoint, i) => (
            <button
              key={i}
              onClick={() => setSelectedEndpoint(endpoint)}
              className={`w-full text-left p-3 rounded-lg mb-1 transition ${
                selectedEndpoint === endpoint
                  ? 'bg-blue-50 border-2 border-blue-500'
                  : 'hover:bg-gray-50 border-2 border-transparent'
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <span className={`px-2 py-0.5 text-xs font-semibold rounded ${
                  endpoint.method === 'GET' ? 'bg-green-100 text-green-700' :
                  endpoint.method === 'POST' ? 'bg-blue-100 text-blue-700' :
                  endpoint.method === 'PUT' ? 'bg-yellow-100 text-yellow-700' :
                  endpoint.method === 'DELETE' ? 'bg-red-100 text-red-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {endpoint.method}
                </span>
                <span className="text-sm font-mono">{endpoint.path}</span>
              </div>
              <p className="text-xs text-gray-600 truncate">{endpoint.summary}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Main Area */}
      <div className="flex-1 flex flex-col">
        {/* Auth Header */}
        <div className="bg-white border-b p-4">
          <div className="max-w-4xl mx-auto flex items-center gap-4">
            <Key className="w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder={`Enter your ${authConfig.name || 'API key'}...`}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
            <span className="text-sm text-gray-600">
              {authConfig.type || 'API Key'} Authentication
            </span>
          </div>
        </div>

        {/* Request Builder */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto">
            {/* Endpoint Info */}
            <div className="bg-white rounded-lg border p-6 mb-4">
              <div className="flex items-center gap-3 mb-3">
                <span className={`px-3 py-1 text-sm font-semibold rounded ${
                  selectedEndpoint.method === 'GET' ? 'bg-green-100 text-green-700' :
                  selectedEndpoint.method === 'POST' ? 'bg-blue-100 text-blue-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {selectedEndpoint.method}
                </span>
                <code className="text-lg font-mono">{selectedEndpoint.path}</code>
              </div>
              <p className="text-gray-700 mb-4">{selectedEndpoint.description}</p>

              {/* Parameters */}
              {selectedEndpoint.parameters && selectedEndpoint.parameters.length > 0 && (
                <div className="mb-4">
                  <h3 className="font-semibold mb-2">Parameters:</h3>
                  <div className="space-y-2">
                    {selectedEndpoint.parameters.map((param, i) => (
                      <div key={i} className="flex items-center gap-3">
                        <label className="w-40 text-sm font-medium">
                          {param.name}
                          {param.required && <span className="text-red-500">*</span>}
                        </label>
                        <input
                          type="text"
                          placeholder={param.type}
                          className="flex-1 px-3 py-2 border rounded"
                          onChange={(e) => setRequestParams({
                            ...requestParams,
                            [param.name]: e.target.value
                          })}
                        />
                        <span className="text-xs text-gray-500 w-32">{param.description}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Send Request Button */}
              <button
                onClick={makeRequest}
                disabled={isLoading || !apiKey}
                className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold flex items-center justify-center gap-2 disabled:opacity-50 transition"
              >
                {isLoading ? (
                  <>Sending...</>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Send Request
                  </>
                )}
              </button>
            </div>

            {/* Response */}
            {response && (
              <div className="bg-white rounded-lg border p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold">Response</h3>
                  <span className={`px-3 py-1 rounded text-sm font-semibold ${
                    response.status >= 200 && response.status < 300
                      ? 'bg-green-100 text-green-700'
                      : 'bg-red-100 text-red-700'
                  }`}>
                    {response.status} {response.statusText}
                  </span>
                </div>
                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                  {JSON.stringify(response.data, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
"""

        return {
            "component_code": frontend_code,
            "usage_instructions": "Import and use this component with your API endpoints",
            "features": [
                "Live API testing",
                "Authentication support",
                "Request/response visualization",
                "Multi-endpoint support"
            ]
        }

    async def generate_sdk_code(
        self,
        endpoint: Dict[str, Any],
        language: str = "python"
    ) -> str:
        """
        Generate SDK code example in specified language

        Supports: python, javascript, curl, ruby, php, go, java
        """
        templates = {
            "python": self._generate_python_sdk,
            "javascript": self._generate_javascript_sdk,
            "curl": self._generate_curl_sdk,
            "ruby": self._generate_ruby_sdk,
            "php": self._generate_php_sdk,
            "go": self._generate_go_sdk,
            "java": self._generate_java_sdk
        }

        generator = templates.get(language.lower())
        if not generator:
            raise ValueError(f"Unsupported language: {language}")

        return generator(endpoint)

    def _generate_python_sdk(self, endpoint: Dict[str, Any]) -> str:
        """Generate Python SDK example"""
        method = endpoint['method'].lower()
        path = endpoint['path']

        code = f"""import requests

# Configure your API client
API_BASE_URL = "https://api.example.com"
API_KEY = "your_api_key_here"

headers = {{
    "Authorization": f"Bearer {{API_KEY}}",
    "Content-Type": "application/json"
}}

# {endpoint.get('summary', 'API Request')}
url = f"{{API_BASE_URL}}{path}"
"""

        if method in ['post', 'put', 'patch']:
            code += """
data = {
    # Add your request parameters here
}

response = requests.""" + method + """(url, headers=headers, json=data)
"""
        else:
            code += f"\nresponse = requests.{method}(url, headers=headers)\n"

        code += """
if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
"""

        return code

    def _generate_javascript_sdk(self, endpoint: Dict[str, Any]) -> str:
        """Generate JavaScript SDK example"""
        method = endpoint['method']
        path = endpoint['path']

        code = f"""// {endpoint.get('summary', 'API Request')}
const API_BASE_URL = "https://api.example.com";
const API_KEY = "your_api_key_here";

const url = `${{API_BASE_URL}}{path}`;

const options = {{
  method: '{method}',
  headers: {{
    'Authorization': `Bearer ${{API_KEY}}`,
    'Content-Type': 'application/json'
  }}"""

        if method in ['POST', 'PUT', 'PATCH']:
            code += """,
  body: JSON.stringify({
    // Add your request parameters here
  })"""

        code += """
};

fetch(url, options)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('Success:', data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
"""

        return code

    def _generate_curl_sdk(self, endpoint: Dict[str, Any]) -> str:
        """Generate cURL example"""
        method = endpoint['method']
        path = endpoint['path']

        code = f"""# {endpoint.get('summary', 'API Request')}
curl -X {method} \\
  'https://api.example.com{path}' \\
  -H 'Authorization: Bearer YOUR_API_KEY' \\
  -H 'Content-Type: application/json'"""

        if method in ['POST', 'PUT', 'PATCH']:
            code += """ \\
  -d '{
    "key": "value"
  }'"""

        return code

    def _generate_ruby_sdk(self, endpoint: Dict[str, Any]) -> str:
        """Generate Ruby SDK example"""
        return "# Ruby SDK example - Coming soon!"

    def _generate_php_sdk(self, endpoint: Dict[str, Any]) -> str:
        """Generate PHP SDK example"""
        return "// PHP SDK example - Coming soon!"

    def _generate_go_sdk(self, endpoint: Dict[str, Any]) -> str:
        """Generate Go SDK example"""
        return "// Go SDK example - Coming soon!"

    def _generate_java_sdk(self, endpoint: Dict[str, Any]) -> str:
        """Generate Java SDK example"""
        return "// Java SDK example - Coming soon!"
