"""
Simple result formatter for Policy Navigator demos.
"""

from typing import List, Any


def format_answer(question: str, answer: str, citations: List[Any], store_name: str) -> str:
    """Format search result for display."""
    dept = store_name.replace("policy-navigator-", "").upper()
    
    result = f"\n[{dept}] {question}\n"
    result += "─" * 70 + "\n"
    result += f"✓ Found {len(citations)} sources\n\n"
    result += f"{answer}\n"
    
    if citations:
        result += "Sources:\n"
        for i, cite in enumerate(citations[:3], 1):
            # Extract text from citation dict or object
            if isinstance(cite, dict):
                text = cite.get("text", str(cite)[:100])
            else:
                text = str(cite)[:100]
            
            # Clean up text
            text = text.replace("...", "").strip()[:100]
            result += f"  {i}. {text}...\n"
    
    result += "─" * 70 + "\n"
    
    return result
