"""
ADK Tutorial 19: Artifacts and File Management

This agent demonstrates comprehensive artifact storage, versioning, and retrieval
capabilities for document processing workflows.

Features:
- Document text extraction and storage
- Summarization with artifact versioning
- Multi-language translation
- Final report generation combining all artifacts
- Built-in artifact loading tool for conversational access
"""

from typing import Dict, Any, Optional
from google.adk.agents import Agent
from google.adk.tools.load_artifacts_tool import load_artifacts_tool
from google.adk.tools.tool_context import ToolContext
from google.genai import types


async def extract_text_tool(document_content: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Extract and store document text as an artifact.

    This tool takes raw document content, processes it, and saves the
    extracted text as a versioned artifact for future reference.

    Args:
        document_content: Raw document text to process and store

    Returns:
        Dict with status, report, and extracted text information
    """
    try:
        # Basic text extraction (in a real implementation, this might involve
        # PDF parsing, OCR, or other document processing)
        extracted_text = document_content.strip()

        # Validate extracted content
        if not extracted_text:
            return {
                'status': 'error',
                'error': 'No text content found in document',
                'report': 'Failed to extract text from document'
            }

        # Create artifact part
        text_part = types.Part.from_text(text=extracted_text)

        # Save as artifact
        version = await tool_context.save_artifact(
            filename='document_extracted.txt',
            artifact=text_part
        )

        return {
            'status': 'success',
            'report': f'Successfully extracted {len(extracted_text)} characters of text and saved as version {version}',
            'data': {
                'filename': 'document_extracted.txt',
                'version': version,
                'content': extracted_text,
                'word_count': len(extracted_text.split()),
                'character_count': len(extracted_text)
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to extract document text: {str(e)}'
        }


async def summarize_document_tool(document_text: Optional[str], tool_context: ToolContext) -> Dict[str, Any]:
    """
    Generate and store a document summary as an artifact.

    Creates a concise summary of the provided document text and saves it
    as a versioned artifact. If no text is provided, attempts to load
    the most recent extracted document.

    Args:
        document_text: Text to summarize (optional - loads from artifacts if not provided)
        tool_context: Tool context for artifact operations

    Returns:
        Dict with status, report, and summary information
    """
    try:
        # If no text provided, try to load the extracted document
        if not document_text:
            artifact = await tool_context.load_artifact('document_extracted.txt')
            if artifact and artifact.text:
                document_text = artifact.text
            else:
                return {
                    'status': 'error',
                    'error': 'No document text provided',
                    'report': 'Please provide document text or ensure extracted text is available'
                }

        # Basic summarization (in practice, this would use LLM)
        words = document_text.split()
        if len(words) <= 50:
            summary = document_text
        else:
            summary = ' '.join(words[:50]) + '...'

        # Create artifact part
        summary_part = types.Part.from_text(text=summary)

        # Save as artifact
        version = await tool_context.save_artifact(
            filename='document_summary.txt',
            artifact=summary_part
        )

        return {
            'status': 'success',
            'report': f'Generated summary ({len(summary)} characters) and saved as version {version}',
            'data': {
                'filename': 'document_summary.txt',
                'version': version,
                'content': summary,
                'original_length': len(document_text),
                'summary_length': len(summary)
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to generate document summary: {str(e)}'
        }


async def translate_document_tool(text: str, target_language: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Translate document text to a target language and store as artifact.

    Args:
        text: Text to translate
        target_language: Target language (e.g., 'Spanish', 'French', 'German')
        tool_context: Tool context for artifact operations

    Returns:
        Dict with status, report, and translation information
    """
    try:
        if not text:
            return {
                'status': 'error',
                'error': 'No text provided for translation',
                'report': 'Please provide text to translate'
            }

        # Basic translation simulation (in practice, this would use translation API)
        # For demo purposes, we'll just mark the text as "translated"
        translated_text = f"[Translated to {target_language}] {text}"

        # Create artifact part
        translation_part = types.Part.from_text(text=translated_text)

        # Save as artifact
        filename = f'document_{target_language.lower()}.txt'
        version = await tool_context.save_artifact(
            filename=filename,
            artifact=translation_part
        )

        return {
            'status': 'success',
            'report': f'Translated {len(text)} characters to {target_language} and saved as version {version}',
            'data': {
                'filename': filename,
                'version': version,
                'content': translated_text,
                'source_language': 'English',
                'target_language': target_language
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to translate document: {str(e)}'
        }


async def create_final_report_tool(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Create a comprehensive final report combining all document artifacts.

    Generates a final report that references and combines all processed
    document artifacts into a single comprehensive document.

    Args:
        tool_context: Tool context for artifact operations

    Returns:
        Dict with status, report, and final report information
    """
    try:
        # Load all artifacts
        all_artifacts = await tool_context.list_artifacts()
        
        # Build report content
        report_content = """# Document Processing Final Report

## Processing Summary

This report combines all document processing artifacts from the current session.

## Artifacts Processed

"""
        
        artifacts_list = []
        for filename in all_artifacts:
            if filename.startswith('document_') and not filename.endswith('FINAL_REPORT.md'):
                artifact = await tool_context.load_artifact(filename)
                if artifact:
                    report_content += f"- {filename}: {len(artifact.text)} characters\n"
                    artifacts_list.append(filename)

        report_content += """
## Recommendations

All document processing completed successfully. Artifacts are versioned and
available for future reference.

## Next Steps

- Review individual artifacts for detailed content
- Generate additional translations if needed
- Archive or export final results
"""

        # Create artifact part
        report_part = types.Part.from_text(text=report_content)

        # Save as artifact
        version = await tool_context.save_artifact(
            filename='document_FINAL_REPORT.md',
            artifact=report_part
        )

        return {
            'status': 'success',
            'report': f'Generated comprehensive final report combining {len(artifacts_list)} artifacts (version {version})',
            'data': {
                'filename': 'document_FINAL_REPORT.md',
                'version': version,
                'content': report_content,
                'artifacts_combined': artifacts_list
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to create final report: {str(e)}'
        }


async def list_artifacts_tool(tool_context: ToolContext) -> Dict[str, Any]:
    """
    List all available artifacts in the current session.

    Args:
        tool_context: Tool context for artifact operations

    Returns:
        Dict with status, report, and list of available artifacts
    """
    try:
        # Load all artifacts from the artifact service
        artifacts = await tool_context.list_artifacts()

        return {
            'status': 'success',
            'report': f'Found {len(artifacts)} artifacts',
            'data': {
                'artifacts': artifacts,
                'count': len(artifacts)
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to list artifacts: {str(e)}'
        }


async def load_artifact_tool(filename: str, tool_context: ToolContext, version: Optional[int] = None) -> Dict[str, Any]:
    """
    Load a specific artifact by filename and optional version.

    Args:
        filename: Name of the artifact to load
        tool_context: Tool context for artifact operations
        version: Specific version to load (optional - loads latest if not specified)

    Returns:
        Dict with status, report, and artifact content
    """
    try:
        if not filename:
            return {
                'status': 'error',
                'error': 'No filename provided',
                'report': 'Please specify an artifact filename to load'
            }

        # Load artifact from the artifact service
        artifact = await tool_context.load_artifact(filename, version=version)

        if not artifact:
            return {
                'status': 'error',
                'error': f'Artifact {filename} not found',
                'report': f'Could not find artifact {filename}' + (f' version {version}' if version else '')
            }

        return {
            'status': 'success',
            'report': f'Loaded artifact {filename}' + (f' version {version}' if version else ' (latest)'),
            'data': {
                'filename': filename,
                'version': version,
                'content': artifact.text if artifact.text else '[Binary content]'
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to load artifact {filename}: {str(e)}'
        }


def main():
    """Main entry point for running the agent directly."""
    import asyncio
    from google.adk.runners import Runner
    from google.adk.artifacts import InMemoryArtifactService
    from google.adk.sessions import InMemorySessionService

    async def run_agent():
        # Configure artifact service
        artifact_service = InMemoryArtifactService()

        # Create runner with artifact support
        runner = Runner(
            agent=root_agent,
            session_service=InMemorySessionService(),
            artifact_service=artifact_service
        )

        print("🤖 Artifact Agent Ready!")
        print("📄 This agent can process documents and store them as artifacts.")
        print("💡 Try: 'Process this document: [paste some text]'")

        # In a real CLI, you would handle user input here
        # For now, just show that the agent is configured
        print(f"Agent: {root_agent.name}")
        print(f"Tools: {len(root_agent.tools)} available")
        print("Artifact service: Configured ✓")

    asyncio.run(run_agent())


if __name__ == "__main__":
    main()


# Export the root agent as required by ADK
root_agent = Agent(
    name="artifact_agent",
    model="gemini-2.5-flash",
    description="Document processing agent with comprehensive artifact storage and versioning capabilities",
    instruction="""You are an advanced document processing agent with artifact storage capabilities.

Your primary functions:
1. Extract and store document text as artifacts
2. Generate summaries and save them as versioned artifacts
3. Translate content into multiple languages
4. Create comprehensive reports combining all processed artifacts
5. List and retrieve previously stored artifacts

When processing documents:
- Always save extracted text as 'document_extracted.txt'
- Save summaries as 'document_summary.txt' with versioning
- Save translations as 'document_LANGUAGE.txt' (where LANGUAGE is the target language)
- Create final reports as 'document_FINAL_REPORT.md'

Use the load_artifacts tool when users ask about previously processed documents.
Maintain artifact provenance by referencing previous versions in new artifacts.

Available tools:
- save_artifact: Store files with automatic versioning
- load_artifact: Retrieve specific artifact versions
- list_artifacts: Show all available artifacts
- load_artifacts_tool: Built-in tool for conversational artifact access
""",
    tools=[
        extract_text_tool,
        summarize_document_tool,
        translate_document_tool,
        create_final_report_tool,
        list_artifacts_tool,
        load_artifact_tool,
        load_artifacts_tool,  # Built-in ADK tool for conversational access
    ],
)