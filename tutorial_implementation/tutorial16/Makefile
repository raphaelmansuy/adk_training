.PHONY: help setup dev test clean demo check-node create-sample-files clean-samples about

help:
	@echo "Tutorial 16: MCP Integration - Available commands:"
	@echo "  make setup             - Install dependencies and setup environment"
	@echo "  make dev               - Start ADK development server"
	@echo "  make test              - Run all tests"
	@echo "  make demo              - Show demo prompts and usage examples"
	@echo "  make about             - Show detailed agent capabilities"
	@echo "  make create-sample-files - Create sample files for testing organization"
	@echo "  make clean-samples     - Remove sample files directory"
	@echo "  make clean             - Remove cache files and artifacts"
	@echo "  make check-node        - Verify Node.js and npx are installed"

setup: check-node
	@echo "Setting up Tutorial 16: MCP Integration..."
	pip install -r requirements.txt
	pip install -e .
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Copy mcp_agent/.env.example to mcp_agent/.env"
	@echo "  2. Add your GOOGLE_API_KEY to mcp_agent/.env"
	@echo "  3. Run 'make dev' to start the ADK server"
	@echo "  4. Open http://localhost:8000 in your browser"

check-node:
	@echo "Checking Node.js and npx installation..."
	@command -v node >/dev/null 2>&1 || { echo "❌ Error: Node.js not found. Install from https://nodejs.org/"; exit 1; }
	@command -v npx >/dev/null 2>&1 || { echo "❌ Error: npx not found. Install Node.js from https://nodejs.org/"; exit 1; }
	@echo "✅ Node.js: $$(node --version)"
	@echo "✅ npx: $$(npx --version)"

dev:
	@echo "╔═══════════════════════════════════════════════════════════════╗"
	@echo "║         Starting MCP Filesystem Agent - ADK Server           ║"
	@echo "╚═══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "🚀 Server will start at: http://localhost:8000"
	@echo ""
	@echo "📂 File Organization Examples (try these prompts):"
	@echo ""
	@echo "1. Basic Organization:"
	@echo "   'Organize the sample_files directory by file type'"
	@echo "   'Create folders for code, docs, and config files'"
	@echo "   'Move all .txt files to a documents folder'"
	@echo ""
	@echo "2. Project Structure:"
	@echo "   'Create a standard Python project structure'"
	@echo "   'Organize files into src/, tests/, and docs/ folders'"
	@echo "   'Set up a web project with public/, src/, and config/ folders'"
	@echo ""
	@echo "3. Content-Based Organization:"
	@echo "   'Group all Python files together in a code folder'"
	@echo "   'Move all configuration files to a config directory'"
	@echo "   'Organize markdown files into a documentation folder'"
	@echo ""
	@echo "4. Advanced Organization:"
	@echo "   'Sort files by date modified into yearly folders'"
	@echo "   'Create backup folders and move old files'"
	@echo "   'Organize by file size (small, medium, large)'"
	@echo ""
	@echo "5. Cleanup Operations:"
	@echo "   'Remove all temporary files (*.tmp, *.bak)'"
	@echo "   'Consolidate duplicate files'"
	@echo "   'Archive old log files into compressed folders'"
	@echo ""
	@echo "💡 Tips for File Organization:"
	@echo "  • Agent can create folders automatically"
	@echo "  • Use natural language like 'group by type' or 'sort by date'"
	@echo "  • Agent will explain actions before executing"
	@echo "  • Try 'make create-sample-files' first for test data"
	@echo ""
	@echo "🎯 Quick Test Commands:"
	@echo "  make create-sample-files    # Create test files to organize"
	@echo "  make demo                   # See all available prompts"
	@echo "  make about                  # Full agent capabilities"
	@echo ""
	@echo "Starting server..."
	@echo ""
	@adk web

test:
	@echo "Running tests for Tutorial 16..."
	@echo ""
	SKIP_MCP_INTEGRATION=false pytest tests/ -v
	@echo ""
	@echo "✅ All tests passed!"

demo:
	@echo "╔═══════════════════════════════════════════════════════════════╗"
	@echo "║         Tutorial 16: MCP Integration - Demo Prompts          ║"
	@echo "╚═══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  1. make setup              # Install dependencies"
	@echo "  2. make create-sample-files # Create test files (optional)"
	@echo "  3. make dev                # Start ADK server"
	@echo "  4. Open http://localhost:8000"
	@echo ""
	@echo "📝 Demo Prompts (try these in ADK UI):"
	@echo ""
	@echo "1. List Files:"
	@echo "   'List all files in the current directory'"
	@echo "   'Show me all Python files in this project'"
	@echo ""
	@echo "2. Read File:"
	@echo "   'Read the contents of README.md'"
	@echo "   'What's in the requirements.txt file?'"
	@echo ""
	@echo "3. Create File:"
	@echo "   'Create a new file called test.txt with content: Hello MCP!'"
	@echo "   'Write a Python script that prints the current date'"
	@echo ""
	@echo "4. File Search:"
	@echo "   'Search for all Python files containing TODO'"
	@echo "   'Find all markdown files in this directory'"
	@echo ""
	@echo "5. File Info:"
	@echo "   'What is the size and last modified date of requirements.txt?'"
	@echo "   'Give me details about the Makefile'"
	@echo ""
	@echo "6. File Organization:"
	@echo "   'Organize the sample_files/mixed_content folder by file type'"
	@echo "   'Create folders for code, docs, and config files'"
	@echo "   'Move all .txt files to a documents folder'"
	@echo ""
	@echo "7. Advanced Operations:"
	@echo "   'Create a project structure with src, tests, and docs folders'"
	@echo "   'Analyze all Python files and list their main functions'"
	@echo "   'Generate a summary of all markdown files in this directory'"
	@echo ""
	@echo "💡 Tips:"
	@echo "  - MCP server automatically connects to filesystem"
	@echo "  - Agent can read, write, move, and organize files"
	@echo "  - Use natural language for file operations"
	@echo "  - Agent explains actions before executing"
	@echo "  - Try 'make about' for detailed capabilities"
	@echo ""
	@echo "📚 Learn More:"
	@echo "  - Tutorial: docs/tutorial/16_mcp_integration.md"
	@echo "  - MCP Spec: https://spec.modelcontextprotocol.io/"
	@echo "  - Official Servers: https://github.com/modelcontextprotocol/servers"
	@echo ""
	@echo "🎓 Commands:"
	@echo "  make about              - Show full agent capabilities"
	@echo "  make create-sample-files - Create test files to organize"
	@echo "  make clean-samples      - Remove sample files"

about:
	@echo "╔═══════════════════════════════════════════════════════════════╗"
	@echo "║     MCP Filesystem Agent - Capabilities & Features           ║"
	@echo "╚═══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "🤖 Agent Overview:"
	@echo "  This AI agent has direct filesystem access through the Model Context"
	@echo "  Protocol (MCP), enabling it to perform file operations using natural"
	@echo "  language commands. No manual file handling needed!"
	@echo ""
	@echo "📂 Core Capabilities:"
	@echo ""
	@echo "  1. File Reading:"
	@echo "     • Read text files (code, docs, configs)"
	@echo "     • Read media files (images, PDFs - metadata)"
	@echo "     • Smart encoding detection"
	@echo "     Example: 'Read the contents of config.json'"
	@echo ""
	@echo "  2. File Writing:"
	@echo "     • Create new files with content"
	@echo "     • Update existing files"
	@echo "     • Automatic directory creation"
	@echo "     Example: 'Create a Python script that prints hello world'"
	@echo ""
	@echo "  3. Directory Operations:"
	@echo "     • List directory contents"
	@echo "     • Create nested directories"
	@echo "     • Recursive directory scanning"
	@echo "     Example: 'List all Python files in this directory'"
	@echo ""
	@echo "  4. File Management:"
	@echo "     • Move/rename files"
	@echo "     • Copy files (via read + write)"
	@echo "     • Get file metadata (size, dates, permissions)"
	@echo "     Example: 'Move all .txt files to a docs folder'"
	@echo ""
	@echo "  5. Search & Discovery:"
	@echo "     • Search files by pattern (glob)"
	@echo "     • Find files by content (grep)"
	@echo "     • Filter by file type or extension"
	@echo "     Example: 'Find all TODO comments in Python files'"
	@echo ""
	@echo "  6. File Organization:"
	@echo "     • Auto-organize files by type"
	@echo "     • Create structured directories"
	@echo "     • Batch rename operations"
	@echo "     Example: 'Organize these files into folders by type'"
	@echo ""
	@echo "🎯 Use Cases:"
	@echo "  • Code generation and file creation"
	@echo "  • Project scaffolding and setup"
	@echo "  • File organization and cleanup"
	@echo "  • Documentation generation"
	@echo "  • Configuration file management"
	@echo "  • Build artifact organization"
	@echo "  • Log file analysis"
	@echo ""
	@echo "🔒 Security Features:"
	@echo "  • Scoped to specific directory (no system access)"
	@echo "  • Agent explains actions before execution"
	@echo "  • Read-only mode available"
	@echo "  • User confirmation for destructive operations"
	@echo ""
	@echo "⚡ Performance:"
	@echo "  • Async/await for non-blocking operations"
	@echo "  • 30-second timeout for MCP initialization"
	@echo "  • Efficient file streaming for large files"
	@echo "  • Connection pooling and reuse"
	@echo ""
	@echo "🚀 Try it now:"
	@echo "  make create-sample-files  # Create test files"
	@echo "  make dev                  # Start the agent"
	@echo "  Then ask: 'Organize the sample_files directory by file type'"
	@echo ""

create-sample-files:
	@echo "Creating sample files for testing..."
	@mkdir -p sample_files
	@# Create text documents
	@echo "This is a sample text document.\nYou can ask the agent to read or organize this file." > sample_files/document1.txt
	@echo "Another text file with different content.\nUseful for testing file operations." > sample_files/notes.txt
	@echo "Meeting notes from 2025-10-10\n- Discussed MCP integration\n- Reviewed file operations" > sample_files/meeting_notes.txt
	@# Create code files
	@echo "def hello_world():\n    print('Hello from MCP!')\n\nif __name__ == '__main__':\n    hello_world()" > sample_files/script.py
	@echo "function greet(name) {\n    return \`Hello, \$${name}!\`;\n}\n\nconsole.log(greet('MCP'));" > sample_files/app.js
	@echo "package main\n\nimport \"fmt\"\n\nfunc main() {\n    fmt.Println(\"Hello, MCP!\")\n}" > sample_files/main.go
	@# Create config files
	@echo "{\n  \"name\": \"sample-project\",\n  \"version\": \"1.0.0\",\n  \"description\": \"Sample project for MCP testing\"\n}" > sample_files/package.json
	@echo "debug = true\nport = 8080\nhost = localhost\n\n[database]\nurl = postgres://localhost/db" > sample_files/config.toml
	@echo "# Sample YAML Configuration\napp_name: MCP Demo\nenvironment: development\nfeatures:\n  - file_operations\n  - organization\n" > sample_files/settings.yaml
	@# Create markdown files
	@echo "# Project README\n\nThis is a sample project for testing MCP file operations.\n\n## Features\n- File reading\n- File writing\n- Organization" > sample_files/README.md
	@echo "# TODO List\n\n- [ ] Organize files by type\n- [ ] Create folder structure\n- [x] Test MCP agent\n" > sample_files/TODO.md
	@# Create CSV and data files
	@echo "name,age,city\nAlice,30,NYC\nBob,25,SF\nCharlie,35,LA" > sample_files/data.csv
	@echo "{\n  \"users\": [\n    {\"id\": 1, \"name\": \"Alice\"},\n    {\"id\": 2, \"name\": \"Bob\"}\n  ]\n}" > sample_files/users.json
	@# Create a messy mix to organize
	@mkdir -p sample_files/mixed_content
	@echo "Random file 1" > sample_files/mixed_content/file1.txt
	@echo "console.log('test');" > sample_files/mixed_content/test.js
	@echo "# Notes" > sample_files/mixed_content/notes.md
	@echo "x = 42" > sample_files/mixed_content/calc.py
	@echo "key=value" > sample_files/mixed_content/config.env
	@echo ""
	@echo "✅ Sample files created successfully!"
	@echo ""
	@echo "📂 Created structure:"
	@echo "  sample_files/"
	@echo "    ├── Text files: document1.txt, notes.txt, meeting_notes.txt"
	@echo "    ├── Code files: script.py, app.js, main.go"
	@echo "    ├── Config files: package.json, config.toml, settings.yaml"
	@echo "    ├── Docs: README.md, TODO.md"
	@echo "    ├── Data files: data.csv, users.json"
	@echo "    └── mixed_content/ (unsorted files to organize)"
	@echo ""
	@echo "🎯 Try these prompts with the agent:"
	@echo "  • 'List all files in the sample_files directory'"
	@echo "  • 'Read the contents of README.md'"
	@echo "  • 'Organize the mixed_content folder by file type'"
	@echo "  • 'Find all Python files in sample_files'"
	@echo "  • 'Create a summary of all text documents'"
	@echo "  • 'Move all config files to a new config/ folder'"
	@echo ""

clean-samples:
	@echo "Removing sample files..."
	@rm -rf sample_files
	@echo "✅ Sample files removed!"

clean:
	@echo "Cleaning up build artifacts and cache..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete!"
	@echo ""
	@echo "💡 To also remove sample files, run: make clean-samples"
