# Tutorial 21: Multimodal and Image Processing

Complete implementation of Tutorial 21 demonstrating vision-based AI agents with image processing capabilities.

## Overview

This implementation showcases:
- Processing images with Gemini vision models
- Using `types.Part` for multimodal content
- Building vision-based product catalog analyzer
- Working with multiple image inputs
- Artifact management for catalog entries

## Project Structure

```
tutorial21/
├── Makefile                    # User-friendly build automation with help system
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Package configuration
├── .env.example               # Environment variables template
├── vision_catalog_agent/      # Main agent package
│   ├── __init__.py
│   └── agent.py              # Vision catalog agent (5 tools)
├── _sample_images/            # Sample product images (_ prefix avoids ADK discovery)
├── download_images.py         # Download sample images from Unsplash
├── analyze_samples.py         # Batch analyze all sample images
├── generate_mockups.py        # Generate synthetic product mockups ⭐
├── demo.py                    # Interactive demo script
└── tests/                     # Comprehensive test suite (70 tests)
    ├── test_agent.py          # Agent configuration tests
    ├── test_imports.py        # Import validation
    ├── test_structure.py      # Project structure validation
    └── test_multimodal.py     # Multimodal functionality tests
```

### Automation Scripts

**download_images.py**: Downloads sample product images from Unsplash
- Gets high-quality product photos (laptop, headphones, smartwatch)
- Saves to `_sample_images/` directory
- Free to use under Unsplash License
- Run via: `make download-images` or `python download_images.py`

**analyze_samples.py**: Batch analyzes all sample images
- Loads each image with proper multimodal content handling
- Analyzes with Gemini 2.0 Flash Exp vision model
- Generates professional catalog entries
- Displays formatted results with product details
- Run via: `make analyze` or `python analyze_samples.py`

**generate_mockups.py**: Generates synthetic product mockups ⭐ NEW
- Uses Gemini 2.5 Flash Image for text-to-image
- Creates 3 products: desk lamp, leather wallet, gaming mouse
- Different aspect ratios for each (1:1, 4:3, 16:9)
- Automatically analyzes generated images
- End-to-end workflow demonstration
- Run via: `make generate` or `python generate_mockups.py`

**demo.py**: Interactive demo script (legacy)
- Command-line demonstration of agent capabilities
- Note: Prefer `make demo` for comprehensive examples

## Features

### 🎨 Synthetic Image Generation ⭐ NEW
- Generate product mockups using Gemini 2.5 Flash Image
- Perfect for prototyping before photography
- Text-to-image with professional product photography style
- Multiple aspect ratios (1:1, 16:9, 4:3, 3:2, etc.)
- Ideal for testing catalog designs and concepts

### Image Processing
- Load images from files (PNG, JPEG, WEBP, HEIC)
- Optimize images for API efficiency
- Handle multiple image formats
- Create sample images for testing

### Vision Analysis
- Analyze product images with Gemini vision
- Extract visual features and characteristics
- Identify products and their attributes
- Compare multiple images

### Catalog Generation
- Generate professional product descriptions
- Save catalog entries as artifacts
- Structured markdown output
- Marketing-ready content

### Multi-Agent Workflow
1. **Vision Analyzer**: Analyzes images and extracts information
2. **Catalog Generator**: Creates professional catalog entries
3. **Image Generator**: Creates synthetic product mockups
4. **Coordinator**: Orchestrates the workflow

## Quick Start

### First Time Setup

```bash
# 1. See all available commands
make                # or: make help

# 2. Install dependencies
make setup

# 3. Set your API key (choose one method)
export GOOGLE_API_KEY=your_api_key_here

# 4. Download sample images
make download-images

# 5. Start the agent
make dev
```

The Makefile includes a comprehensive help system. Just run `make` to see all available commands!

### Available Commands

```bash
make                  # Show help (default)
make setup            # Install dependencies
make download-images  # Get sample product images from Unsplash
make dev              # Start ADK web interface (http://localhost:8000)
make demo             # Show comprehensive usage examples

# Image Analysis
make analyze          # Batch analyze all sample images
make generate         # Generate synthetic product mockups ⭐

# Development & Testing
make test             # Run all tests
make coverage         # Run tests with coverage report
make lint             # Run code linters
make clean            # Clean up generated files
```

### Environment Validation

The Makefile automatically checks for authentication before running commands that need it. If not configured, you'll see helpful error messages with setup instructions.

**Authentication Methods:**

1. **API Key (Recommended for development)**:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   # Get a free key at: https://aistudio.google.com/app/apikey
   ```

2. **Service Account (For production)**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
   export GOOGLE_CLOUD_PROJECT=your_project_id
   ```

## Usage Examples

### Analyze Single Product Image

```python
from google.adk.agents import Runner
from vision_catalog_agent import root_agent

runner = Runner()
result = await runner.run_async(
    "Analyze sample_images/laptop.jpg and create a catalog entry",
    agent=root_agent
)
print(result.content.parts[0].text)
```

### Compare Multiple Images

```python
result = await runner.run_async(
    "Compare the laptop and headphones images in sample_images/",
    agent=root_agent
)
```

### Batch Process Products

The agent can analyze multiple products sequentially:

```python
result = await runner.run_async(
    "Analyze all images in sample_images/ directory",
    agent=root_agent
)
```

## Example Prompts

Try these in the ADK web interface:

### Using Uploaded Images (Recommended)

The easiest way to use this agent is by uploading images directly in the web UI:

1. **Upload and Analyze** (drag-and-drop or paste image):

   ```text
   Analyze this laptop image and create a catalog entry
   ```

   - Simply drag and drop an image into the chat
   - Or paste an image from your clipboard
   - The agent will automatically analyze the uploaded image

2. **Multiple Uploaded Images**:

   ```text
   Compare these two product images
   ```

   - Upload multiple images by dragging them together
   - The agent can compare and analyze them

3. **Professional Catalog**:

   ```text
   Create a professional product catalog entry for this item
   ```

   - Upload a product image
   - Get marketing-ready descriptions

### Using File Paths

If you have images saved locally, you can reference them by path:

1. **Basic Analysis**:

   ```text
   Analyze the laptop image and describe what you see
   ```

2. **Catalog Entry**:

   ```text
   Create a professional catalog entry for the headphones image
   ```

3. **Comparison**:

   ```text
   Compare the laptop and smartwatch images
   ```

4. **Batch Processing**:

   ```text
   Analyze all product images and generate catalog entries
   ```

### Automated Batch Analysis

For analyzing all sample images programmatically, use the provided script:

```bash
# Analyze all sample images with one command
python analyze_samples.py
```

This script will:
- Analyze all three sample product images (laptop, headphones, smartwatch)
- Generate professional catalog entries for each
- Display detailed visual analysis and market positioning
- Show results in a clean, formatted output

**Output includes**:
- Product identification and category
- Visual features (colors, design, materials)
- Quality indicators and construction details
- Distinctive features and selling points
- Market positioning and target audience
- Professional marketing-ready descriptions

**Example Output**:

```
================================================================================
Image 1/3: Professional Laptop (laptop.jpg)
Product ID: LAPTOP-001
================================================================================

Product Analysis: Professional Laptop (LAPTOP-001)

1. Product Identification: High-end laptop computer for professional use

2. Visual Features:
   - Color: Sleek silver/gray aluminum finish, black keyboard
   - Design: Modern, minimalist, thin profile (13-15 inch)
   - Materials: Aluminum alloy chassis, high-quality keyboard
   
3. Quality Indicators: Robust construction, smooth finish, sturdy hinge

4. Distinctive Features: Thin bezels, premium look, high-resolution display

5. Market Positioning: High-end segment for professionals and creatives

Catalog Entry:
[Professional marketing description follows...]
```

**Benefits**:
- One command analyzes all samples
- No manual web interface interaction needed
- Perfect for demonstrations and testing
- Generates production-ready catalog entries
- Shows agent's multimodal capabilities

### Synthetic Image Generation ⭐ NEW

Generate professional product mockups when you don't have real photos yet:

```bash
# Generate synthetic product images
python generate_mockups.py

# Or use the Makefile target
make generate
```

This feature uses **Gemini 2.5 Flash Image** to create photorealistic product images from text descriptions.

**What gets generated**:
- Minimalist Desk Lamp (modern, aluminum, LED)
- Premium Leather Wallet (brown leather, gold stitching)
- Wireless Gaming Mouse (RGB lighting, ergonomic)

**In ADK Web Interface**:

```text
Generate a synthetic image of a minimalist desk lamp with brushed aluminum finish
```

The agent will:
1. Use `generate_product_mockup()` tool
2. Create a photorealistic product image
3. Save it to `_sample_images/`
4. Automatically analyze the generated image
5. Provide a professional catalog entry

**Use Cases**:
- 🎨 **Rapid Prototyping**: Test catalog designs before investing in photography
- 💡 **Concept Visualization**: Show clients what products could look like
- 🔄 **Variations**: Generate multiple style/color variations quickly
- 📐 **Layout Testing**: Create mockups for different aspect ratios
- 💰 **Cost Savings**: No need for studio equipment or photographers

**Example Prompts**:
```text
• "Generate a mockup of a premium leather backpack with laptop compartment"
• "Create a synthetic image of a smart water bottle with LED display"
• "Generate product photography for a minimalist wireless charger"
• "Make a mockup of noise-canceling earbuds in matte black"
```

**Supported Styles**:
- Photorealistic product photography (default)
- Studio lighting with white/clean background
- Lifestyle/contextual photography
- Artistic/creative product shots
- Custom lighting and angles

**Aspect Ratios Available**:
- 1:1 (1024x1024) - Perfect for social media
- 16:9 (1344x768) - Wide product shots
- 4:3 (1184x864) - Standard product photos
- 3:2 (1248x832) - Professional photography
- And more (see Gemini 2.5 Flash Image docs)

## Architecture

### Components

1. **Image Utilities**
   - `load_image_from_file()`: Load images as types.Part
   - `optimize_image()`: Optimize image size
   - `create_sample_image()`: Generate test images

2. **Vision Analyzer Agent**
   - Model: `gemini-2.0-flash-exp`
   - Temperature: 0.3 (factual analysis)
   - Analyzes product images
   - Extracts visual features

3. **Catalog Generator Agent**
   - Model: `gemini-2.0-flash-exp`
   - Temperature: 0.6 (creative writing)
   - Generates marketing content
   - Saves artifacts

4. **Root Agent (Coordinator)**
   - Orchestrates workflow
   - Routes requests to appropriate tools
   - Manages multi-image operations

### Tools (5 Available)

The `vision_catalog_agent` provides 5 specialized tools:

1. **`list_sample_images()`**: Discover available sample images
   - Lists images in `_sample_images/` directory
   - Shows file names and paths
   - Helps users explore available samples
   - Example: "What sample images do you have?"

2. **`generate_product_mockup()`**: Generate synthetic product images ⭐ NEW
   - Uses Gemini 2.5 Flash Image model
   - Creates photorealistic product photography
   - Configurable aspect ratios (1:1, 16:9, 4:3, 3:2, etc.)
   - Customizable styles (photorealistic, studio, lifestyle)
   - Saves to `_sample_images/` directory
   - Returns image path for further analysis
   - Example: "Generate a mockup of a minimalist desk lamp"

3. **`analyze_uploaded_image()`**: Analyze images from web UI
   - Provides guidance for drag-and-drop uploads
   - Instructs users on web interface usage
   - Best method for interactive analysis
   - No file path needed
   - Example: [Upload image] "Analyze this product"

4. **`analyze_product_image(path: str)`**: Full analysis pipeline for files
   - Takes file path as input
   - Loads image with multimodal content handling
   - Analyzes with Gemini 2.0 Flash Exp vision
   - Generates professional catalog entry
   - Saves result as artifact
   - Returns detailed product information
   - Example: "Analyze _sample_images/laptop.jpg"

5. **`compare_product_images(paths: List[str])`**: Multi-image comparison
   - Compares multiple product images
   - Identifies similarities and differences
   - Analyzes visual features across products
   - Provides comparative insights
   - Useful for product line analysis
   - Example: "Compare laptop and headphones images"

### Sub-Agents

The coordinator uses specialized sub-agents for different tasks:

- **Vision Analyzer Agent**: Analyzes images and extracts visual information
  - Model: `gemini-2.0-flash-exp`
  - Temperature: 0.3 (factual, precise analysis)
  - Focuses on objective visual features

- **Catalog Generator Agent**: Creates professional catalog entries
  - Model: `gemini-2.0-flash-exp`
  - Temperature: 0.6 (creative, engaging content)
  - Generates marketing-ready descriptions
  - Saves results as artifacts

## Testing

Comprehensive test suite with **70 tests** and **63% coverage**:

```bash
# Run all tests (with environment validation)
make test

# Run with detailed coverage report
make coverage

# Manual test execution
pytest tests/ -v

# Run specific test file
pytest tests/test_multimodal.py -v

# Run with coverage (manual)
pytest tests/ --cov=vision_catalog_agent --cov-report=html --cov-report=term
```

### Test Categories

1. **Import Tests** (`test_imports.py`): 
   - Verify all imports work
   - Validate tool function imports
   - Check agent availability

2. **Agent Configuration** (`test_agent.py`):
   - Check agent setup and properties
   - Validate tool count (5 tools)
   - Test tool signatures and callability
   - Verify model configuration

3. **Structure Tests** (`test_structure.py`):
   - Validate project structure
   - Check required files exist
   - Verify package installation

4. **Multimodal Tests** (`test_multimodal.py`):
   - Test image processing utilities
   - Validate multimodal content handling
   - Check image format support

### Test Results

```bash
$ make test
🧪 Running tests...
pytest tests/ -v --tb=short

======================== test session starts =========================
collected 70 items

tests/test_agent.py::TestAgentConfig::test_agent_exists PASSED    [  1%]
tests/test_agent.py::TestAgentConfig::test_agent_type PASSED      [  2%]
...
tests/test_multimodal.py::TestMultimodal::test_all PASSED         [100%]

========================= 70 passed in 2.45s =========================
```

### Coverage Report

Run `make coverage` to generate detailed HTML coverage report:

```bash
$ make coverage
🧪 Running tests with coverage...

Coverage: 63%
✅ Coverage report generated!
📊 Open htmlcov/index.html to view detailed report
```

## Makefile Features

The tutorial includes a comprehensive Makefile with:

### 🚀 Help System

Run `make` or `make help` to see all available commands organized into:

- **Quick Start Commands**: Setup, download samples, start agent
- **Image Analysis Commands**: Batch analyze, generate synthetic mockups
- **Advanced Commands**: Testing, coverage, linting, cleanup

### ✅ Environment Validation

The Makefile automatically validates authentication before running commands:

- Checks for `GOOGLE_API_KEY` or `GOOGLE_APPLICATION_CREDENTIALS`
- Shows clear error messages with setup instructions
- Supports both Gemini API and Vertex AI authentication
- Prevents common configuration errors

### 📊 Visual Output

All commands provide clear, emoji-enhanced feedback:

- Progress indicators during operations
- Success confirmations with next steps
- Detailed workflow descriptions
- Example prompts for interactive commands

### 🎯 Example Workflows

**First-Time User Path:**
```bash
make                      # See all commands
make setup                # Install dependencies
export GOOGLE_API_KEY=... # Set authentication
make download-images      # Get sample images
make dev                  # Start interactive agent
```

**Development Workflow:**
```bash
make generate    # Generate synthetic mockups
make analyze     # Analyze all samples
make test        # Run tests
make coverage    # Check coverage
```

**Production Workflow:**
```bash
make lint        # Validate code
make test        # Run full test suite
make clean       # Clean up artifacts
```

## Configuration

### Environment Variables

```bash
# Required (choose one)
GOOGLE_API_KEY=your_api_key_here

# OR for Vertex AI
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_CLOUD_PROJECT=your-project-id

# Optional: Vertex AI region
GOOGLE_CLOUD_LOCATION=us-central1
```

### Model Selection

Current models:

- `gemini-2.0-flash-exp`: Latest with vision support
- Alternative: `gemini-1.5-pro`, `gemini-1.5-flash`

## Best Practices

### Image Optimization

- Keep images under 500KB
- Resize large images (max 1024px)
- Use JPEG for optimized size
- Convert RGBA to RGB when needed

### Multimodal Content

- Provide clear context for images
- Use structured query format
- Label multiple images clearly
- Test with various image formats

### Error Handling

- Validate file existence
- Check MIME types
- Handle PIL/Pillow gracefully
- Provide meaningful error messages

## Troubleshooting

### Common Issues

**Issue**: Import errors for PIL/Pillow

```bash
pip install Pillow
```

**Issue**: Agent not found in ADK web

```bash
pip install -e .
```

**Issue**: ADK tries to load directories as agents

- Solution: Use `_` prefix for non-agent directories (`_sample_images`)
- ADK automatically ignores directories starting with `_` or `.`
- Select `vision_catalog_agent` from the dropdown

**Issue**: Image format not supported

- Ensure file extension matches content
- Convert to PNG or JPEG
- Check MIME type detection

**Issue**: API key not set

```bash
export GOOGLE_API_KEY=your_key
```

## Performance Considerations

- Image optimization reduces API costs
- Batch processing for multiple images
- Cache analysis results when appropriate
- Monitor token usage for large images

## Limitations

- Maximum image size: ~20MB
- Supported formats: PNG, JPEG, WEBP, HEIC
- API rate limits apply
- Token limits for large images

## Future Enhancements

- [ ] Image generation with Imagen
- [ ] Video frame analysis
- [ ] Real-time camera integration
- [ ] Advanced OCR capabilities
- [ ] Custom vision models

## Sample Images

The `_sample_images/` directory contains sample product images for
demonstration purposes:

- **laptop.jpg**: Modern laptop computer
- **headphones.jpg**: Wireless headphones
- **smartwatch.jpg**: Smart watch device

**Image Credits**: Sample images sourced from [Unsplash](https://unsplash.com).
Free to use under the [Unsplash License](https://unsplash.com/license).

To download fresh sample images, run:

```bash
python download_images.py
```

## Resources

- [Tutorial Documentation](../../docs/tutorial/21_multimodal_image.md)
- [Gemini Vision Docs](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/overview)
- [ADK Documentation](https://github.com/google/adk-python)
- [Types.Part Reference](https://ai.google.dev/api/python/google/generativeai/protos/Part)
- [Unsplash](https://unsplash.com) - Free high-quality images

## License

Part of the ADK Training project. See main repository for license details.

Sample images are from Unsplash and used under the Unsplash License.

## Support

For issues or questions:

1. Check existing tests for examples
2. Review tutorial documentation
3. Consult ADK documentation
4. Open an issue in the main repository
