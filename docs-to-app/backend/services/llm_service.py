"""
LLM Service - Claude Integration
Handles all LLM interactions for documentation analysis and generation
"""
import anthropic
from typing import Dict, List, Any, Optional
import json


class LLMService:
    """Service for interacting with Claude API"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"  # Using latest Sonnet

    async def analyze_documentation(
        self,
        content: Dict[str, Any],
        doc_type: str = "readme",
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze documentation and extract structured information

        This is the core intelligence - Claude reads the docs and extracts:
        - Main concepts
        - Code examples
        - Learning structure
        - Key patterns
        """
        # Prepare context
        sections_text = "\n\n".join([
            f"{'#' * s['level']} {s['title']}\n{s['content']}"
            for s in content.get('sections', [])
        ])

        prompt = f"""You are analyzing technical documentation to create an interactive learning experience.

Document Title: {title or content.get('metadata', {}).get('title', 'Documentation')}
Type: {doc_type}

Content:
{sections_text[:15000]}  # Limit context

Your task:
1. Identify the main concepts/topics covered
2. Extract code examples with explanations
3. Identify patterns or recurring themes
4. Create a summary suitable for learners
5. Suggest what interactive features would help understanding

Return a JSON object with this structure:
{{
    "title": "string",
    "summary": "string (2-3 sentences)",
    "concepts": ["array of key concepts"],
    "sections": [
        {{
            "title": "string",
            "description": "string",
            "key_points": ["array"],
            "difficulty": "beginner|intermediate|advanced"
        }}
    ],
    "examples": [
        {{
            "title": "string",
            "code": "string",
            "language": "string",
            "explanation": "string",
            "concepts": ["related concepts"]
        }}
    ],
    "suggested_features": ["interactive playground", "step-by-step tutorial", etc],
    "learning_path": ["ordered list of what to learn first"]
}}

Be thorough but concise. Focus on creating an excellent learning experience."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse response
            content_text = response.content[0].text

            # Extract JSON from response
            json_match = content_text
            if "```json" in content_text:
                json_match = content_text.split("```json")[1].split("```")[0]
            elif "```" in content_text:
                json_match = content_text.split("```")[1].split("```")[0]

            analysis = json.loads(json_match.strip())

            return analysis

        except Exception as e:
            raise Exception(f"LLM analysis failed: {str(e)}")

    async def generate_explanation(
        self,
        concept: str,
        context: str,
        level: str = "beginner"
    ) -> str:
        """
        Generate detailed explanation for a concept

        Makes complex topics accessible
        """
        prompt = f"""Explain this concept clearly for a {level} level learner:

Concept: {concept}

Context:
{context[:3000]}

Provide:
1. Clear definition
2. Why it matters
3. How it works
4. Common use cases
5. Simple analogy

Keep it conversational and practical."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text

        except Exception as e:
            raise Exception(f"Explanation generation failed: {str(e)}")

    async def improve_code_example(
        self,
        code: str,
        language: str,
        goal: str = "make it educational"
    ) -> Dict[str, str]:
        """
        Improve code example for learning purposes

        Adds comments, improves structure, makes it clearer
        """
        prompt = f"""Improve this code example to {goal}:

Language: {language}

```{language}
{code}
```

Return JSON:
{{
    "improved_code": "code with helpful comments",
    "explanation": "what makes this code good",
    "key_concepts": ["concepts demonstrated"]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )

            content_text = response.content[0].text

            # Extract JSON
            if "```json" in content_text:
                json_text = content_text.split("```json")[1].split("```")[0]
            elif "```" in content_text:
                json_text = content_text.split("```")[1].split("```")[0]
            else:
                json_text = content_text

            return json.loads(json_text.strip())

        except Exception as e:
            raise Exception(f"Code improvement failed: {str(e)}")

    async def generate_quiz_questions(
        self,
        content: str,
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate interactive quiz questions from content

        Helps reinforce learning
        """
        prompt = f"""Create {count} multiple choice questions from this content:

{content[:3000]}

Return JSON array:
[
    {{
        "question": "string",
        "options": ["A", "B", "C", "D"],
        "correct": 0,
        "explanation": "why this is correct"
    }}
]

Make questions test understanding, not just memorization."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )

            content_text = response.content[0].text

            # Extract JSON
            if "```json" in content_text:
                json_text = content_text.split("```json")[1].split("```")[0]
            elif "```" in content_text:
                json_text = content_text.split("```")[1].split("```")[0]
            else:
                json_text = content_text

            return json.loads(json_text.strip())

        except Exception as e:
            raise Exception(f"Quiz generation failed: {str(e)}")
