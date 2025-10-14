"""
Vision Catalog Agent - Tutorial 21: Multimodal and Image Processing
"""
import io
import os
from typing import List, Dict, Any
from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

try:
    from PIL import Image
except ImportError:
    Image = None


# ============================================================================
# Image Utilities
# ============================================================================


def load_image_from_file(path: str) -> types.Part:
    """
    Load image from local file.
    
    Args:
        path: Path to image file
        
    Returns:
        types.Part with image data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If unsupported format
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image file not found: {path}")
    
    with open(path, 'rb') as f:
        image_bytes = f.read()
    
    # Determine MIME type from extension
    extension = path.lower().split('.')[-1]
    mime_types = {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'webp': 'image/webp',
        'heic': 'image/heic',
        'heif': 'image/heif',
    }
    
    mime_type = mime_types.get(extension)
    if not mime_type:
        raise ValueError(f"Unsupported image format: {extension}")
    
    return types.Part(
        inline_data=types.Blob(
            data=image_bytes,
            mime_type=mime_type
        )
    )


def optimize_image(image_bytes: bytes, max_size_kb: int = 500) -> bytes:
    """
    Optimize image size for API calls.
    
    Args:
        image_bytes: Original image bytes
        max_size_kb: Maximum size in KB
        
    Returns:
        Optimized image bytes
    """
    if Image is None:
        return image_bytes
    
    image = Image.open(io.BytesIO(image_bytes))
    
    # Resize if too large
    max_dimension = 1024
    if max(image.size) > max_dimension:
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
    
    # Convert to RGB if necessary
    if image.mode in ('RGBA', 'P'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'RGBA':
            background.paste(image, mask=image.split()[3])
        else:
            background.paste(image)
        image = background
    
    # Save with compression
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=85, optimize=True)
    
    return output.getvalue()


def create_sample_image(path: str, color: tuple = (73, 109, 137)) -> str:
    """
    Create a sample placeholder image for testing.
    
    Args:
        path: Path to save image
        color: RGB color tuple
        
    Returns:
        Path to created image
    """
    if Image is None:
        raise ImportError("PIL/Pillow required for creating sample images")
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.new('RGB', (400, 400), color=color)
    img.save(path)
    return path


# ============================================================================
# Vision Catalog Agent Components
# ============================================================================


# Vision Analysis Agent
vision_analyzer = Agent(
    model='gemini-2.0-flash-exp',
    name='vision_analyzer',
    description='Analyzes product images and extracts visual information',
    instruction="""
You are a product vision analyst. When analyzing product images:

1. Identify the product type and category
2. Describe key visual features (color, size, material, design)
3. Note any visible text (brand names, labels, specs)
4. Assess product condition and quality
5. Identify unique selling points

Provide structured, detailed analysis focusing on:
- Product identification
- Visual characteristics
- Design elements
- Quality indicators
- Target market insights

Be specific and thorough in your observations.
    """.strip(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,
        max_output_tokens=1024
    )
)


# Tool for generating catalog entries
async def generate_catalog_entry(
    product_name: str,
    analysis: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Generate and save a marketing-ready catalog entry.
    
    Args:
        product_name: Name/ID of the product
        analysis: Vision analysis results
        tool_context: Context for artifact management
        
    Returns:
        Dict with status, report, and artifact version
    """
    try:
        # Generate catalog entry content
        entry = f"""# {product_name}

## Description

{analysis}

## Key Features

- High-quality construction
- Modern design
- Versatile use cases

## Visual Analysis

Based on detailed image analysis, this product demonstrates professional-grade
quality and contemporary design elements suitable for discerning customers.

---

*Catalog entry generated from AI vision analysis*
"""
        
        # Save as artifact
        part = types.Part.from_text(text=entry)
        version = await tool_context.save_artifact(
            filename=f"{product_name}_catalog.md",
            part=part
        )
        
        return {
            'status': 'success',
            'report': f'Catalog entry created for {product_name}',
            'version': version,
            'filename': f"{product_name}_catalog.md"
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'report': f'Failed to generate catalog entry: {str(e)}',
            'error': str(e)
        }


# Catalog Generator Agent
catalog_generator = Agent(
    model='gemini-2.0-flash-exp',
    name='catalog_generator',
    description='Creates professional product catalog entries from visual analysis',
    instruction="""
You are a product catalog content creator. Generate professional,
marketing-ready product descriptions based on visual analysis.

Focus on:
- Compelling product descriptions
- Key features and benefits
- Technical specifications when available
- Customer-friendly language
- Professional tone

Use the generate_catalog_entry tool to save catalog entries as artifacts.
Always provide the product name and the complete visual analysis.
    """.strip(),
    tools=[FunctionTool(generate_catalog_entry)],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.6,
        max_output_tokens=1536
    )
)


# Tool for analyzing product images
async def analyze_product_image(
    product_id: str,
    image_path: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Analyze a product image and generate catalog entry.
    
    Args:
        product_id: Product identifier
        image_path: Path to product image file
        tool_context: Context for sub-agent execution
        
    Returns:
        Dict with analysis results and catalog entry info
    """
    try:
        # Load image
        if not os.path.exists(image_path):
            return {
                'status': 'error',
                'report': f'Image file not found: {image_path}',
                'error': 'File not found'
            }
        
        image_part = load_image_from_file(image_path)
        
        # Step 1: Vision analysis
        analysis_query = [
            types.Part.from_text(text=f"Analyze this product image for {product_id}:"),
            image_part
        ]
        
        analysis_result = await tool_context.run_agent(
            vision_analyzer,
            analysis_query
        )
        
        if not analysis_result.content or not analysis_result.content.parts:
            return {
                'status': 'error',
                'report': 'Failed to analyze image',
                'error': 'No analysis result'
            }
        
        analysis_text = analysis_result.content.parts[0].text
        
        # Step 2: Generate catalog entry
        catalog_query = f"""
Based on this visual analysis, create a professional catalog entry for {product_id}:

{analysis_text}

Use the generate_catalog_entry tool to save the entry.
        """.strip()
        
        catalog_result = await tool_context.run_agent(
            catalog_generator,
            catalog_query
        )
        
        return {
            'status': 'success',
            'report': f'Successfully analyzed {product_id}',
            'product_id': product_id,
            'analysis': analysis_text,
            'catalog_result': catalog_result.content.parts[0].text if catalog_result.content else ''
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'report': f'Failed to analyze product: {str(e)}',
            'error': str(e)
        }


# Tool for comparing multiple images
async def compare_product_images(
    image_paths: List[str],
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Compare multiple product images.
    
    Args:
        image_paths: List of image file paths
        tool_context: Context for agent execution
        
    Returns:
        Dict with comparison results
    """
    try:
        if len(image_paths) < 2:
            return {
                'status': 'error',
                'report': 'Need at least 2 images to compare',
                'error': 'Insufficient images'
            }
        
        # Load all images
        query_parts = [
            types.Part.from_text(text="Compare these product images and identify similarities and differences:")
        ]
        
        for i, path in enumerate(image_paths, 1):
            if not os.path.exists(path):
                return {
                    'status': 'error',
                    'report': f'Image not found: {path}',
                    'error': 'File not found'
                }
            
            query_parts.append(types.Part.from_text(text=f"\nImage {i}:"))
            query_parts.append(load_image_from_file(path))
        
        query_parts.append(types.Part.from_text(text="\nProvide a structured comparison."))
        
        # Run comparison
        result = await tool_context.run_agent(vision_analyzer, query_parts)
        
        if not result.content or not result.content.parts:
            return {
                'status': 'error',
                'report': 'Failed to compare images',
                'error': 'No comparison result'
            }
        
        return {
            'status': 'success',
            'report': f'Successfully compared {len(image_paths)} images',
            'comparison': result.content.parts[0].text,
            'image_count': len(image_paths)
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'report': f'Failed to compare images: {str(e)}',
            'error': str(e)
        }


# Tool for generating synthetic product mockups
async def generate_product_mockup(
    product_description: str,
    product_name: str,
    tool_context: ToolContext,
    style: str = "photorealistic product photography",
    aspect_ratio: str = "1:1"
) -> Dict[str, Any]:
    """
    Generate synthetic product images using Gemini 2.5 Flash Image.
    
    Perfect for creating product mockups when you don't have real photos yet.
    Great for prototyping, testing, or generating variations of existing products.
    
    Args:
        product_description: Detailed description of the product to generate
        product_name: Name/ID for saving the generated image
        style: Photography/illustration style (default: photorealistic product photography)
        aspect_ratio: Image aspect ratio (default: 1:1, options: 16:9, 4:3, 3:2, etc.)
        tool_context: Context for tool execution
        
    Returns:
        Dict with status, generated image path, and description
        
    Examples:
        - "A sleek wireless mouse, matte black finish, ergonomic design, on white background"
        - "Premium leather wallet, brown color, gold stitching, with credit cards visible"
        - "Minimalist desk lamp, brushed aluminum, LED light, modern design"
    """
    try:
        from google import genai as genai_client
        from google.genai import types as genai_types
        from PIL import Image
        from io import BytesIO
        
        # Create detailed prompt for product photography
        detailed_prompt = f"""
A {style} of {product_description}.

The image should be:
- High-resolution and professional quality
- Well-lit with studio lighting
- Sharp focus on the product
- Clean composition
- Suitable for e-commerce or marketing materials

Background: Clean, minimal, professional backdrop that enhances the product.
Lighting: Soft, even lighting that highlights the product's features and quality.
Angle: Flattering perspective that shows the product clearly.
        """.strip()
        
        # Initialize client
        client = genai_client.Client(api_key=os.environ.get('GOOGLE_API_KEY'))
        
        # Generate image
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=[detailed_prompt],
            config=genai_types.GenerateContentConfig(
                response_modalities=['Image'],
                image_config=genai_types.ImageConfig(
                    aspect_ratio=aspect_ratio
                )
            )
        )
        
        # Save the generated image
        generated_image_path = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Save to _sample_images directory
                sample_dir = Path(__file__).parent.parent / '_sample_images'
                sample_dir.mkdir(exist_ok=True)
                
                # Create filename
                safe_name = product_name.lower().replace(' ', '_').replace('-', '_')
                image_path = sample_dir / f"{safe_name}_generated.jpg"
                
                # Save image
                image = Image.open(BytesIO(part.inline_data.data))
                image.save(image_path, 'JPEG', quality=95)
                generated_image_path = str(image_path)
                
                break
        
        if not generated_image_path:
            return {
                'status': 'error',
                'report': 'No image was generated',
                'error': 'No image data in response'
            }
        
        return {
            'status': 'success',
            'report': f'Generated synthetic product mockup for {product_name}',
            'image_path': generated_image_path,
            'description': product_description,
            'style': style,
            'aspect_ratio': aspect_ratio,
            'usage_tip': f'You can now analyze this image with analyze_product_image("{product_name}", "{generated_image_path}")'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'report': f'Failed to generate product mockup: {str(e)}',
            'error': str(e)
        }


# Tool for listing available sample images
async def list_sample_images(
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    List available sample product images in the _sample_images directory.
    
    Use this when users ask what images are available or want to see examples.
    
    Args:
        tool_context: Context for tool execution
        
    Returns:
        Dict with list of available images and their details
    """
    try:
        # Get the sample images directory
        sample_dir = Path(__file__).parent.parent / '_sample_images'
        
        if not sample_dir.exists():
            return {
                'status': 'info',
                'report': 'Sample images directory not found. You can create it or upload your own images.',
                'available_images': []
            }
        
        # Find all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.heic'}
        images = []
        
        for img_file in sorted(sample_dir.iterdir()):
            if img_file.suffix.lower() in image_extensions:
                # Get file size
                size_bytes = img_file.stat().st_size
                size_kb = size_bytes / 1024
                
                # Try to get image dimensions if PIL is available
                dimensions = None
                if Image is not None:
                    try:
                        with Image.open(img_file) as img:
                            dimensions = f"{img.width}x{img.height}"
                    except Exception:
                        pass
                
                images.append({
                    'filename': img_file.name,
                    'path': str(img_file),
                    'size': f"{size_kb:.1f} KB",
                    'dimensions': dimensions or 'unknown',
                    'format': img_file.suffix[1:].upper()
                })
        
        if not images:
            return {
                'status': 'info',
                'report': 'No sample images found. Upload your own images or run: python download_images.py',
                'available_images': []
            }
        
        return {
            'status': 'success',
            'report': f'Found {len(images)} sample image(s) in _sample_images/',
            'available_images': images,
            'directory': str(sample_dir),
            'usage_hint': 'Use analyze_product_image(product_id, image_path) to analyze any of these images'
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'report': f'Failed to list sample images: {str(e)}',
            'error': str(e)
        }


# Tool for analyzing uploaded images directly from query
async def analyze_uploaded_image(
    product_name: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Analyze an image that was uploaded directly in the query.
    
    This tool provides guidance for analyzing uploaded images that are already
    visible to the root agent's vision model. It does NOT require sub-agent calls.
    
    Args:
        product_name: Name or ID for the product
        tool_context: Context for tool execution
        
    Returns:
        Dict with structured analysis guidance
    """
    try:
        # Since the root agent has vision capabilities and can see uploaded images,
        # we return a structured prompt to guide its analysis
        return {
            'status': 'success',
            'report': f'Acknowledged: Analyzing uploaded image for product "{product_name}"',
            'product_name': product_name,
            'analysis_framework': {
                'product_identification': [
                    'Product type and category',
                    'Brand or manufacturer (if visible)',
                    'Model number or SKU (if visible)'
                ],
                'visual_features': [
                    'Primary and secondary colors',
                    'Design style and aesthetics',
                    'Materials and textures',
                    'Dimensions and proportions (if discernible)'
                ],
                'quality_indicators': [
                    'Construction quality',
                    'Finish and craftsmanship',
                    'Condition assessment',
                    'Packaging (if shown)'
                ],
                'distinctive_features': [
                    'Unique selling points',
                    'Innovative design elements',
                    'Special features or capabilities',
                    'Comparison to typical products in category'
                ],
                'market_positioning': [
                    'Target audience',
                    'Use cases and applications',
                    'Market segment (entry/mid/premium)',
                    'Competitive positioning'
                ]
            },
            'instruction_for_agent': f"""
Based on the uploaded image visible in this conversation, provide a comprehensive
analysis of {product_name} following the analysis_framework above.

Then create a professional product catalog entry in markdown format including:

# {product_name}

## Product Overview
[Compelling 2-3 sentence description]

## Key Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Specifications
- **Category**: [Product category]
- **Design**: [Design characteristics]
- **Materials**: [Materials used]
- **Color**: [Color options]

## Description
[Detailed 2-3 paragraph description highlighting benefits and use cases]

## Target Market
[Who this product is for]

---
*Analysis based on visual inspection*
            """.strip()
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'report': f'Failed to prepare uploaded image analysis: {str(e)}',
            'error': str(e)
        }


# ============================================================================
# Root Agent
# ============================================================================


root_agent = Agent(
    model='gemini-2.0-flash-exp',
    name='vision_catalog_coordinator',
    description='Vision-based product catalog coordinator with multimodal capabilities',
    instruction="""
You are a vision-based product catalog coordinator with multimodal capabilities.
You can see and analyze images directly.

**AVAILABLE SAMPLE IMAGES**:
- There are sample product images in the _sample_images/ directory
- Use list_sample_images() tool to see what's available
- Sample images include: laptop, headphones, smartwatch, etc.
- Users can also upload their own images

**SYNTHETIC IMAGE GENERATION** ⭐ NEW:
- Use generate_product_mockup() to create synthetic product images
- Perfect when users don't have product photos yet
- Great for prototyping, testing variations, or generating ideas
- Examples: "Generate a mockup of a minimalist desk lamp" or "Create a synthetic image of a leather backpack"
- After generation, you can analyze the synthetic image like any other

**WORKFLOW FOR UPLOADED IMAGES** (Most Common):
1. When user uploads/pastes an image, first call analyze_uploaded_image(product_name)
2. The tool will return an analysis_framework and instruction_for_agent
3. YOU then analyze the image you can see, following that framework
4. Provide the comprehensive analysis and catalog entry directly to the user

**WORKFLOW FOR SAMPLE/FILE PATH IMAGES**:
- If user asks what images are available → Use list_sample_images()
- If user wants to analyze a sample image → Use analyze_product_image(product_id, image_path)
- For comparing multiple files → Use compare_product_images(image_paths)
- Sample images are in: tutorial_implementation/tutorial21/_sample_images/

**Key Points**:
- You have vision capabilities and can see uploaded images directly
- The analyze_uploaded_image tool provides structure, but YOU do the actual analysis
- For uploaded images, follow the analysis_framework returned by the tool
- Create detailed, professional catalog entries
- Be specific about what you observe in the image
- Suggest using sample images if user is exploring capabilities

**Your Analysis Should Include**:
1. Product identification (type, category, brand if visible)
2. Visual features (colors, design, materials, dimensions)
3. Quality indicators (construction, finish, condition)
4. Distinctive features (unique selling points, innovations)
5. Market positioning (target audience, use cases, segment)

**Helpful Suggestions**:
- If user asks "what can you do?", mention sample images and list_sample_images tool
- If user is unsure, suggest: "Try 'list sample images' to see examples"
- Always be helpful and guide users to available resources

Always provide clear, detailed responses based on what you can actually see.
    """.strip(),
    tools=[
        FunctionTool(list_sample_images),
        FunctionTool(generate_product_mockup),
        FunctionTool(analyze_uploaded_image),
        FunctionTool(analyze_product_image),
        FunctionTool(compare_product_images)
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=2048
    )
)


# ============================================================================
# Main Entry Point (for testing)
# ============================================================================


async def main():
    """Main entry point for standalone testing."""
    print("Vision Catalog Agent initialized")
    print(f"Agent: {root_agent.name}")
    print(f"Model: {root_agent.model}")
    print(f"Tools: {len(root_agent.tools)}")
    
    # Create sample images if they don't exist
    sample_dir = Path(__file__).parent.parent / '_sample_images'
    sample_dir.mkdir(exist_ok=True)
    
    sample_images = [
        ('laptop.jpg', (100, 120, 140)),
        ('headphones.jpg', (50, 50, 50)),
        ('smartwatch.jpg', (80, 100, 120))
    ]
    
    for filename, color in sample_images:
        path = sample_dir / filename
        if not path.exists():
            create_sample_image(str(path), color)
            print(f"Created sample image: {path}")
    
    print("\nReady to process product images!")


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
