"""
Document Parser Service
Handles fetching and parsing documentation from various sources
"""
import re
import requests
from typing import Dict, List, Any
from bs4 import BeautifulSoup
import markdown
from markdown.extensions import fenced_code, tables, toc


class DocumentParser:
    """Parse and structure documentation from various formats"""

    def __init__(self):
        self.md_parser = markdown.Markdown(
            extensions=['fenced_code', 'tables', 'toc', 'codehilite']
        )

    async def fetch_from_url(self, url: str) -> str:
        """
        Fetch documentation from a URL

        Supports:
        - GitHub README URLs
        - Raw documentation URLs
        - HTML documentation pages
        """
        try:
            # Handle GitHub URLs
            if 'github.com' in url and '/blob/' in url:
                url = url.replace('/blob/', '/raw/')

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            content_type = response.headers.get('content-type', '')

            if 'text/html' in content_type:
                # Parse HTML and extract main content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Try to find main content
                main_content = (
                    soup.find('article') or
                    soup.find('main') or
                    soup.find('div', class_='markdown-body') or
                    soup.find('div', id='readme') or
                    soup.body
                )

                if main_content:
                    # Extract text, preserving code blocks
                    return self._html_to_markdown(main_content)

            return response.text

        except Exception as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")

    def _html_to_markdown(self, soup) -> str:
        """Convert HTML to markdown-like text"""
        # Simple conversion - in production, use html2text or similar
        text_parts = []

        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'pre', 'code', 'ul', 'ol']):
            if element.name == 'h1':
                text_parts.append(f"\n# {element.get_text()}\n")
            elif element.name == 'h2':
                text_parts.append(f"\n## {element.get_text()}\n")
            elif element.name == 'h3':
                text_parts.append(f"\n### {element.get_text()}\n")
            elif element.name == 'pre':
                code = element.get_text()
                text_parts.append(f"\n```\n{code}\n```\n")
            elif element.name in ['p', 'ul', 'ol']:
                text_parts.append(element.get_text() + "\n")

        return '\n'.join(text_parts)

    def parse_markdown(self, content: str) -> Dict[str, Any]:
        """
        Parse markdown content and extract structure

        Returns:
        {
            'raw': original content,
            'html': HTML version,
            'sections': structured sections,
            'code_blocks': extracted code,
            'headings': document outline
        }
        """
        # Convert to HTML for structure
        html = self.md_parser.convert(content)

        # Extract sections
        sections = self._extract_sections(content)

        # Extract code blocks
        code_blocks = self._extract_code_blocks(content)

        # Extract headings for TOC
        headings = self._extract_headings(content)

        return {
            'raw': content,
            'html': html,
            'sections': sections,
            'code_blocks': code_blocks,
            'headings': headings,
            'metadata': self._extract_metadata(content)
        }

    def _extract_sections(self, content: str) -> List[Dict[str, Any]]:
        """Split document into logical sections based on headings"""
        sections = []
        current_section = None

        lines = content.split('\n')

        for line in lines:
            # Check for heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)

            if heading_match:
                # Save previous section
                if current_section:
                    sections.append(current_section)

                # Start new section
                level = len(heading_match.group(1))
                title = heading_match.group(2)

                current_section = {
                    'level': level,
                    'title': title,
                    'content': []
                }
            elif current_section:
                current_section['content'].append(line)

        # Add last section
        if current_section:
            current_section['content'] = '\n'.join(current_section['content'])
            sections.append(current_section)

        return sections

    def _extract_code_blocks(self, content: str) -> List[Dict[str, str]]:
        """Extract all code blocks with language information"""
        code_blocks = []

        # Match fenced code blocks
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            language = match.group(1) or 'text'
            code = match.group(2).strip()

            code_blocks.append({
                'language': language,
                'code': code
            })

        return code_blocks

    def _extract_headings(self, content: str) -> List[Dict[str, Any]]:
        """Extract all headings for table of contents"""
        headings = []

        for line in content.split('\n'):
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                title = match.group(2)

                headings.append({
                    'level': level,
                    'title': title,
                    'id': self._slugify(title)
                })

        return headings

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata like title, description, etc."""
        lines = content.split('\n')

        metadata = {
            'title': None,
            'description': None,
            'has_code': '```' in content,
            'has_tables': '|' in content,
            'line_count': len(lines)
        }

        # Get first H1 as title
        for line in lines:
            if line.startswith('# '):
                metadata['title'] = line[2:].strip()
                break

        # Get first paragraph as description
        for line in lines:
            if line.strip() and not line.startswith('#'):
                metadata['description'] = line.strip()
                break

        return metadata

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert heading to URL-friendly slug"""
        slug = text.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
