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
├── Makefile                    # Standard build commands
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Package configuration
├── .env.example               # Environment variables template
├── vision_catalog_agent/      # Main agent package
│   ├── __init__.py
│   └── agent.py              # Vision catalog agent implementation
├── _sample_images/            # Sample product images (_ prefix avoids ADK discovery)
└── tests/                     # Comprehensive test suite
    ├── test_agent.py
    ├── test_imports.py
    ├── test_structure.py
    └── test_multimodal.py
```

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

### 1. Setup

```bash
# Install dependencies
make setup

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 2. Run Tests

```bash
# Run all tests
make test

# Run with coverage
make coverage
```

### 3. Start Development

```bash
# Start ADK web interface
make dev

# The agent will be available at http://localhost:8000
# Select "vision_catalog_agent" from the dropdown
```

### 4. View Demo Instructions

```bash
# See example prompts
make demo
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

### Tools

- `list_sample_images`: Discover available sample images
- `generate_product_mockup`: Generate synthetic product images ⭐ NEW
- `analyze_uploaded_image`: Analyze images from web UI
- `analyze_product_image`: Full analysis pipeline for files
- `compare_product_images`: Multi-image comparison
- `generate_catalog_entry`: Artifact creation

## Testing

Comprehensive test suite with 50+ tests:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_multimodal.py -v

# Run with coverage
pytest tests/ --cov=vision_catalog_agent --cov-report=html
```

### Test Categories

1. **Import Tests**: Verify all imports work
2. **Agent Configuration**: Check agent setup
3. **Structure Tests**: Validate project structure
4. **Multimodal Tests**: Test image processing

## Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional: Vertex AI
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
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
