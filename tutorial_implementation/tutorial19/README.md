# Tutorial 19: Artifacts and File Management

This implementation demonstrates comprehensive artifact storage, versioning, and retrieval capabilities for document processing workflows using Google ADK.

## Overview

The **artifact_agent** showcases how to build document processing pipelines that leverage ADK's artifact system for persistent file storage across sessions. Key features include:

- **Document Text Extraction**: Extract and store document content as artifacts
- **Intelligent Summarization**: Generate summaries with automatic versioning
- **Multi-language Translation**: Translate content and store translations as artifacts
- **Final Report Generation**: Create comprehensive reports combining all artifacts
- **Artifact Management**: List, load, and manage stored artifacts
- **Built-in Artifact Tools**: Use ADK's built-in `load_artifacts_tool` for conversational access

## Architecture

```
Document Processing Pipeline:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Input Document │───▶│  extract_text    │───▶│  Artifact:      │
│                 │    │  (save artifact) │    │  extracted.txt  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Summarize      │───▶│  summarize_doc   │───▶│  Artifact:      │
│  (extracted)    │    │  (save artifact) │    │  summary.txt    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Translate      │───▶│  translate_doc   │───▶│  Artifact:      │
│  (summary)      │    │  (save artifact) │    │  spanish.txt    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Create Report  │───▶│  create_report   │───▶│  Artifact:      │
│  (all artifacts)│    │  (save artifact) │    │  FINAL_REPORT.md│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Key Components

### Agent Configuration

The `root_agent` is configured with:
- **Model**: `gemini-2.5-flash` for optimal performance
- **Tools**: 7 specialized tools for document processing and artifact management
- **Instructions**: Comprehensive guidance for artifact-based workflows

### Tool Functions

1. **`extract_text_tool`**: Extracts and stores document text
2. **`summarize_document_tool`**: Generates summaries with versioning
3. **`translate_document_tool`**: Translates content to target languages
4. **`create_final_report_tool`**: Combines all artifacts into final reports
5. **`list_artifacts_tool`**: Lists all available artifacts
6. **`load_artifact_tool`**: Loads specific artifacts by filename/version
7. **`load_artifacts_tool`**: Built-in ADK tool for conversational artifact access

### Artifact Storage

- **In-Memory Service**: Used for development and testing
- **Version Control**: Automatic versioning (0, 1, 2, ...) for each save
- **Session Scoping**: Artifacts are scoped to user sessions
- **Metadata Tracking**: Automatic timestamp and context tracking

## Quick Start

### Prerequisites

1. **Python 3.9+** installed
2. **Google AI API Key** from [AI Studio](https://aistudio.google.com/app/apikey)

### Setup

```bash
# Clone and navigate to tutorial
cd tutorial_implementation/tutorial19

# Install dependencies
make setup

# Set your API key
export GOOGLE_API_KEY=your_api_key_here

# Start the agent
make dev
```

### Demo Workflow

1. **Open** http://localhost:8000 in your browser
2. **Select** "artifact_agent" from the dropdown
3. **Try these prompts**:

```
Process this document: The quick brown fox jumps over the lazy dog. This is a sample document for testing artifact storage and retrieval capabilities.

Show me all saved artifacts

Summarize the document I just processed

Translate the summary to Spanish

Create a final report combining all artifacts
```

## Tool Details

### Document Processing Tools

#### `extract_text_tool(document_content: str)`

Extracts text from documents and saves as `document_extracted.txt`:

```python
result = extract_text_tool("Sample document text...")
# Returns: {'status': 'success', 'report': '...', 'data': {...}}
```

#### `summarize_document_tool(document_text: str)`

Generates summaries and saves as `document_summary.txt`:

```python
result = summarize_document_tool("Long document text...")
# Creates versioned artifact with summary
```

#### `translate_document_tool(text: str, target_language: str)`

Translates text and saves as `document_{language}.txt`:

```python
result = translate_document_tool("Hello world", "Spanish")
# Saves: document_spanish.txt
```

### Artifact Management Tools

#### `list_artifacts_tool()`

Lists all artifacts in current session:

```python
result = list_artifacts_tool()
# Returns: ['document_extracted.txt', 'document_summary.txt', ...]
```

#### `load_artifact_tool(filename: str, version: Optional[int])`

Loads specific artifact:

```python
result = load_artifact_tool('document_summary.txt', version=0)
# Loads first version of summary
```

#### `load_artifacts_tool` (Built-in)

ADK's built-in tool for conversational artifact access. Automatically loads artifacts when users ask about them.

## Configuration

### Environment Variables

Create a `.env` file (never commit it):

```bash
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY
```

### Artifact Service

The agent uses `InMemoryArtifactService` for development. For production:

```python
from google.adk.artifacts import GcsArtifactService

# Production configuration
artifact_service = GcsArtifactService(bucket_name='your-gcs-bucket')
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ -v --cov=artifact_agent --cov-report=html
```

### Test Coverage

- **Agent Configuration**: Validates agent setup and tools
- **Import Validation**: Ensures all dependencies are available
- **Project Structure**: Verifies correct file organization
- **Tool Functions**: Tests all document processing tools
- **Error Handling**: Validates proper error responses

## API Reference

### Agent Methods

- `save_artifact(filename, artifact)`: Save artifact, returns version
- `load_artifact(filename, version=None)`: Load artifact (latest if no version)
- `list_artifacts()`: List all artifact filenames

### Tool Return Format

All tools return structured dictionaries:

```python
{
    'status': 'success' | 'error',
    'report': 'Human-readable message',
    'data': {  # Only present on success
        'filename': 'artifact_name.txt',
        'content': 'artifact content',
        # ... additional metadata
    }
}
```

## Advanced Usage

### Custom Artifact Workflows

```python
# Example: Multi-step document processing
async def process_document(context, document):
    # Extract text
    extracted = await context.save_artifact('doc.txt', types.Part.from_text(document))

    # Generate summary
    summary = await context.save_artifact('summary.txt', types.Part.from_text("Summary..."))

    # Create report
    report = await context.save_artifact('report.md', types.Part.from_text("Final report..."))

    return [extracted, summary, report]
```

### Version Management

```python
# Save multiple versions
v1 = await context.save_artifact('report.txt', part1)  # v0
v2 = await context.save_artifact('report.txt', part2)  # v1
v3 = await context.save_artifact('report.txt', part3)  # v2

# Load specific versions
latest = await context.load_artifact('report.txt')      # v2
version1 = await context.load_artifact('report.txt', 1)  # v1
```

## Troubleshooting

### Common Issues

1. **"Artifacts tab is empty" (UI Display Issue)**
   - **This is expected behavior with InMemoryArtifactService**
   - Artifacts ARE being saved correctly (check server logs for HTTP 200 responses)
   - Artifacts ARE accessible via blue buttons in chat (click "display document_xxx.txt")
   - **Workaround**: Use the blue artifact buttons that appear in chat responses
   - **Alternative**: Ask agent "Show me all saved artifacts" to list them in chat
   - **Root cause**: ADK web UI's sidebar expects metadata that InMemoryArtifactService doesn't provide
   - **Production**: This limitation doesn't exist with GcsArtifactService in production

2. **"Artifact service is not initialized"**
   - Ensure artifact service is configured in Runner
   - Check that `artifact_service` parameter is passed

3. **"No artifacts found"**
   - Verify artifacts were saved in same session
   - Check filename spelling and case

4. **Import errors**
   - Run `make setup` to install dependencies
   - Check Python version (3.9+ required)

### Debug Mode

Enable debug logging:

```bash
export PYTHONPATH=/path/to/adk-python/src:$PYTHONPATH
# Run with verbose logging
```

### Verifying Artifacts Are Working

Even though the Artifacts sidebar is empty, you can verify artifacts work correctly:

1. **Check server logs** for `HTTP/1.1" 200 OK` responses when saving/loading artifacts
2. **Click blue buttons** in chat that say "display document_xxx.txt"
3. **Ask the agent**: "Show me all saved artifacts" - it will list them in chat
4. **Ask the agent**: "Load document_extracted.txt" - it will show the content

## File Structure

```
tutorial19/
├── artifact_agent/
│   ├── __init__.py          # Package marker
│   └── agent.py             # Main agent implementation
├── tests/
│   ├── __init__.py
│   ├── test_agent.py        # Agent configuration tests
│   ├── test_imports.py      # Import validation tests
│   ├── test_structure.py    # Project structure tests
│   └── test_tools.py        # Tool function tests
├── pyproject.toml           # Modern Python packaging
├── requirements.txt         # Dependencies
├── Makefile                 # Build and run commands
├── .env.example             # Environment template
└── README.md               # This documentation
```

## Related Tutorials

- **Tutorial 01**: Hello World Agent - Basic agent setup
- **Tutorial 02**: Function Tools - Tool development patterns
- **Tutorial 08**: State & Memory - Session state management
- **Tutorial 09**: Callbacks & Guardrails - Advanced agent patterns

## Contributing

When extending this implementation:

1. Add new tools following the return format pattern
2. Update tests for new functionality
3. Maintain artifact naming conventions
4. Document new features in this README

## License

This implementation follows the same license as the ADK project.