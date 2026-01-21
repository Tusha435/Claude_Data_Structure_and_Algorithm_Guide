"""
OpenAPI/Swagger Parser Service
Specialized parser for API documentation (OpenAPI 3.0/3.1, Swagger 2.0)
"""
import json
import yaml
import requests
from typing import Dict, List, Any, Optional
from pydantic import BaseModel


class APIEndpoint(BaseModel):
    """Structured API endpoint information"""
    path: str
    method: str
    summary: Optional[str]
    description: Optional[str]
    parameters: List[Dict[str, Any]]
    request_body: Optional[Dict[str, Any]]
    responses: Dict[str, Any]
    security: Optional[List[Dict[str, Any]]]
    tags: List[str]


class APIAuthentication(BaseModel):
    """Authentication scheme information"""
    type: str  # apiKey, http, oauth2, openIdConnect
    name: Optional[str]
    in_location: Optional[str]  # header, query, cookie
    scheme: Optional[str]  # bearer, basic
    flows: Optional[Dict[str, Any]]


class OpenAPIParser:
    """Parse and analyze OpenAPI/Swagger specifications"""

    def __init__(self):
        self.spec = None
        self.version = None

    async def parse_from_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch and parse OpenAPI spec from URL

        Supports:
        - Direct OpenAPI spec URLs
        - GitHub raw URLs
        - Swagger UI URLs
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            content_type = response.headers.get('content-type', '')

            if 'application/json' in content_type or url.endswith('.json'):
                spec = response.json()
            elif 'yaml' in content_type or url.endswith(('.yaml', '.yml')):
                spec = yaml.safe_load(response.text)
            else:
                # Try JSON first, then YAML
                try:
                    spec = response.json()
                except:
                    spec = yaml.safe_load(response.text)

            return await self.parse_spec(spec)

        except Exception as e:
            raise Exception(f"Failed to parse OpenAPI spec from URL: {str(e)}")

    async def parse_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse OpenAPI specification and extract structured information

        Returns comprehensive API analysis:
        - Basic info (title, version, description)
        - All endpoints with details
        - Authentication schemes
        - Data models/schemas
        - Example requests/responses
        """
        self.spec = spec

        # Detect version
        if 'openapi' in spec:
            self.version = spec['openapi']  # 3.x
        elif 'swagger' in spec:
            self.version = spec['swagger']  # 2.0
        else:
            raise Exception("Not a valid OpenAPI/Swagger specification")

        # Extract information
        info = self._extract_info()
        servers = self._extract_servers()
        auth = self._extract_auth()
        endpoints = self._extract_endpoints()
        schemas = self._extract_schemas()
        examples = self._generate_examples(endpoints)

        return {
            'version': self.version,
            'info': info,
            'servers': servers,
            'authentication': auth,
            'endpoints': endpoints,
            'schemas': schemas,
            'examples': examples,
            'endpoint_count': len(endpoints),
            'tags': self._extract_tags()
        }

    def _extract_info(self) -> Dict[str, Any]:
        """Extract API metadata"""
        info = self.spec.get('info', {})

        return {
            'title': info.get('title', 'API Documentation'),
            'version': info.get('version', '1.0.0'),
            'description': info.get('description', ''),
            'contact': info.get('contact', {}),
            'license': info.get('license', {}),
            'terms_of_service': info.get('termsOfService', '')
        }

    def _extract_servers(self) -> List[Dict[str, str]]:
        """Extract API server URLs"""
        if self.version.startswith('3'):
            servers = self.spec.get('servers', [])
            return [
                {
                    'url': s.get('url', ''),
                    'description': s.get('description', '')
                }
                for s in servers
            ]
        else:
            # Swagger 2.0
            host = self.spec.get('host', '')
            base_path = self.spec.get('basePath', '')
            schemes = self.spec.get('schemes', ['https'])

            return [
                {
                    'url': f"{scheme}://{host}{base_path}",
                    'description': 'API Server'
                }
                for scheme in schemes
            ]

    def _extract_auth(self) -> List[Dict[str, Any]]:
        """Extract authentication schemes"""
        auth_schemes = []

        if self.version.startswith('3'):
            # OpenAPI 3.x
            components = self.spec.get('components', {})
            security_schemes = components.get('securitySchemes', {})

            for name, scheme in security_schemes.items():
                auth_schemes.append({
                    'name': name,
                    'type': scheme.get('type'),
                    'description': scheme.get('description', ''),
                    'in': scheme.get('in'),
                    'scheme': scheme.get('scheme'),
                    'bearer_format': scheme.get('bearerFormat'),
                    'flows': scheme.get('flows')
                })
        else:
            # Swagger 2.0
            security_defs = self.spec.get('securityDefinitions', {})

            for name, scheme in security_defs.items():
                auth_schemes.append({
                    'name': name,
                    'type': scheme.get('type'),
                    'description': scheme.get('description', ''),
                    'in': scheme.get('in'),
                    'flow': scheme.get('flow')
                })

        return auth_schemes

    def _extract_endpoints(self) -> List[Dict[str, Any]]:
        """Extract all API endpoints"""
        endpoints = []

        paths = self.spec.get('paths', {})

        for path, path_item in paths.items():
            # Handle path-level parameters
            path_params = path_item.get('parameters', [])

            # Each HTTP method
            for method in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']:
                if method not in path_item:
                    continue

                operation = path_item[method]

                # Combine path and operation parameters
                all_params = path_params + operation.get('parameters', [])

                endpoint = {
                    'path': path,
                    'method': method.upper(),
                    'summary': operation.get('summary', ''),
                    'description': operation.get('description', ''),
                    'operation_id': operation.get('operationId', ''),
                    'tags': operation.get('tags', []),
                    'parameters': self._parse_parameters(all_params),
                    'request_body': self._parse_request_body(operation.get('requestBody')),
                    'responses': self._parse_responses(operation.get('responses', {})),
                    'security': operation.get('security', []),
                    'deprecated': operation.get('deprecated', False)
                }

                endpoints.append(endpoint)

        return endpoints

    def _parse_parameters(self, params: List[Dict]) -> List[Dict[str, Any]]:
        """Parse parameter definitions"""
        parsed_params = []

        for param in params:
            if self.version.startswith('3'):
                # OpenAPI 3.x
                schema = param.get('schema', {})
                parsed_params.append({
                    'name': param.get('name'),
                    'in': param.get('in'),
                    'description': param.get('description', ''),
                    'required': param.get('required', False),
                    'type': schema.get('type'),
                    'format': schema.get('format'),
                    'default': schema.get('default'),
                    'example': param.get('example') or schema.get('example')
                })
            else:
                # Swagger 2.0
                parsed_params.append({
                    'name': param.get('name'),
                    'in': param.get('in'),
                    'description': param.get('description', ''),
                    'required': param.get('required', False),
                    'type': param.get('type'),
                    'format': param.get('format'),
                    'default': param.get('default')
                })

        return parsed_params

    def _parse_request_body(self, request_body: Optional[Dict]) -> Optional[Dict[str, Any]]:
        """Parse request body definition"""
        if not request_body:
            return None

        content = request_body.get('content', {})

        # Get first content type (usually application/json)
        for content_type, media_type in content.items():
            schema = media_type.get('schema', {})

            return {
                'content_type': content_type,
                'required': request_body.get('required', False),
                'description': request_body.get('description', ''),
                'schema': schema,
                'example': media_type.get('example') or schema.get('example')
            }

        return None

    def _parse_responses(self, responses: Dict) -> Dict[str, Any]:
        """Parse response definitions"""
        parsed_responses = {}

        for status_code, response in responses.items():
            if self.version.startswith('3'):
                content = response.get('content', {})

                # Get JSON response if available
                json_response = content.get('application/json', {})
                schema = json_response.get('schema', {})

                parsed_responses[status_code] = {
                    'description': response.get('description', ''),
                    'schema': schema,
                    'example': json_response.get('example') or schema.get('example')
                }
            else:
                # Swagger 2.0
                parsed_responses[status_code] = {
                    'description': response.get('description', ''),
                    'schema': response.get('schema', {}),
                    'example': response.get('examples', {}).get('application/json')
                }

        return parsed_responses

    def _extract_schemas(self) -> Dict[str, Any]:
        """Extract data model schemas"""
        if self.version.startswith('3'):
            components = self.spec.get('components', {})
            return components.get('schemas', {})
        else:
            # Swagger 2.0
            return self.spec.get('definitions', {})

    def _extract_tags(self) -> List[Dict[str, str]]:
        """Extract API tags/categories"""
        tags = self.spec.get('tags', [])

        return [
            {
                'name': tag.get('name', ''),
                'description': tag.get('description', '')
            }
            for tag in tags
        ]

    def _generate_examples(self, endpoints: List[Dict]) -> List[Dict[str, Any]]:
        """
        Generate code examples for key endpoints

        Returns examples in multiple languages
        """
        examples = []

        # Take first 5 endpoints for examples
        for endpoint in endpoints[:5]:
            example = {
                'endpoint': f"{endpoint['method']} {endpoint['path']}",
                'summary': endpoint['summary'],
                'languages': {}
            }

            # Generate cURL
            example['languages']['curl'] = self._generate_curl_example(endpoint)

            # Generate Python
            example['languages']['python'] = self._generate_python_example(endpoint)

            # Generate JavaScript
            example['languages']['javascript'] = self._generate_javascript_example(endpoint)

            examples.append(example)

        return examples

    def _generate_curl_example(self, endpoint: Dict) -> str:
        """Generate cURL example"""
        server = self.spec.get('servers', [{}])[0].get('url', 'https://api.example.com')
        path = endpoint['path']
        method = endpoint['method']

        curl = f"curl -X {method} \\\n  '{server}{path}'"

        # Add headers
        curl += " \\\n  -H 'Content-Type: application/json'"

        # Add auth header (example)
        if endpoint.get('security'):
            curl += " \\\n  -H 'Authorization: Bearer YOUR_API_KEY'"

        # Add body for POST/PUT/PATCH
        if method in ['POST', 'PUT', 'PATCH'] and endpoint.get('request_body'):
            curl += " \\\n  -d '{\"example\": \"data\"}'"

        return curl

    def _generate_python_example(self, endpoint: Dict) -> str:
        """Generate Python requests example"""
        server = self.spec.get('servers', [{}])[0].get('url', 'https://api.example.com')
        path = endpoint['path']
        method = endpoint['method'].lower()

        code = f"""import requests

url = '{server}{path}'
headers = {{
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
}}
"""

        if method in ['post', 'put', 'patch']:
            code += """
data = {
    'example': 'data'
}

response = requests.""" + method + """(url, headers=headers, json=data)
"""
        else:
            code += f"\nresponse = requests.{method}(url, headers=headers)\n"

        code += """
print(response.json())
"""

        return code

    def _generate_javascript_example(self, endpoint: Dict) -> str:
        """Generate JavaScript fetch example"""
        server = self.spec.get('servers', [{}])[0].get('url', 'https://api.example.com')
        path = endpoint['path']
        method = endpoint['method']

        code = f"""const url = '{server}{path}';

const options = {{
  method: '{method}',
  headers: {{
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  }}"""

        if method in ['POST', 'PUT', 'PATCH']:
            code += """,
  body: JSON.stringify({
    example: 'data'
  })"""

        code += """
};

fetch(url, options)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
"""

        return code

    def get_endpoint_by_path(self, path: str, method: str) -> Optional[Dict]:
        """Get specific endpoint details"""
        if not self.spec:
            return None

        paths = self.spec.get('paths', {})
        path_item = paths.get(path, {})
        operation = path_item.get(method.lower())

        if not operation:
            return None

        return {
            'path': path,
            'method': method.upper(),
            'operation': operation
        }
