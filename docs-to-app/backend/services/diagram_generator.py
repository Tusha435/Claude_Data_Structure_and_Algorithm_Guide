"""
Diagram Generator Service
Creates visual diagrams using Mermaid syntax
"""
from typing import Dict, Any
from .llm_service import LLMService


class DiagramGenerator:
    """Generate Mermaid diagrams for visualization"""

    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def generate_mermaid_diagram(
        self,
        concept: str,
        context: str
    ) -> str:
        """
        Generate Mermaid diagram for a concept

        Mermaid supports:
        - Flowcharts
        - Sequence diagrams
        - Class diagrams
        - State diagrams
        - And more!
        """
        prompt = f"""Create a Mermaid diagram to visualize this concept:

Concept: {concept}

Context:
{context[:2000]}

Choose the most appropriate diagram type (flowchart, sequence, class, state, etc.)
Return ONLY the Mermaid syntax, no explanation.

Example format:
```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```

Generate the diagram:"""

        try:
            response = await self.llm.client.messages.create(
                model=self.llm.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            content_text = response.content[0].text

            # Extract Mermaid code
            if "```mermaid" in content_text:
                mermaid_code = content_text.split("```mermaid")[1].split("```")[0].strip()
            elif "```" in content_text:
                mermaid_code = content_text.split("```")[1].split("```")[0].strip()
            else:
                mermaid_code = content_text.strip()

            return mermaid_code

        except Exception as e:
            raise Exception(f"Diagram generation failed: {str(e)}")

    async def generate_architecture_diagram(
        self,
        components: list,
        relationships: list
    ) -> str:
        """
        Generate system architecture diagram
        """
        prompt = f"""Create a Mermaid architecture diagram with these components:

Components: {components}
Relationships: {relationships}

Use graph TD format. Return only Mermaid syntax."""

        try:
            response = await self.llm.client.messages.create(
                model=self.llm.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            content_text = response.content[0].text

            if "```mermaid" in content_text:
                return content_text.split("```mermaid")[1].split("```")[0].strip()
            elif "```" in content_text:
                return content_text.split("```")[1].split("```")[0].strip()
            else:
                return content_text.strip()

        except Exception as e:
            raise Exception(f"Architecture diagram generation failed: {str(e)}")

    async def generate_flow_diagram(
        self,
        steps: list
    ) -> str:
        """
        Generate process flow diagram
        """
        # Build Mermaid flowchart
        mermaid_lines = ["graph TD"]

        for i, step in enumerate(steps):
            node_id = f"N{i}"
            next_id = f"N{i+1}" if i < len(steps) - 1 else None

            mermaid_lines.append(f"    {node_id}[{step}]")

            if next_id:
                mermaid_lines.append(f"    {node_id} --> {next_id}")

        return "\n".join(mermaid_lines)
