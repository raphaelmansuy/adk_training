#!/usr/bin/env python3
"""
Generate Synthetic Product Images - Tutorial 21 Enhancement

This script demonstrates the new synthetic image generation capability
using Gemini 2.5 Flash Image model. Perfect for:
- Prototyping product catalogs before photography
- Testing variations of existing products
- Generating mockups for client presentations
- Creating diverse product imagery quickly
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from vision_catalog_agent.agent import root_agent, load_image_from_file
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types


# Product mockup specifications
PRODUCT_MOCKUPS = [
    {
        'name': 'Minimalist Desk Lamp',
        'description': 'A sleek minimalist desk lamp with brushed aluminum finish, LED light source, adjustable arm, and modern geometric base. Clean lines, professional design.',
        'style': 'photorealistic product photography',
        'aspect_ratio': '1:1'
    },
    {
        'name': 'Premium Leather Wallet',
        'description': 'Luxury brown leather bi-fold wallet with gold stitching, multiple card slots visible, RFID protection badge, premium craftsmanship, elegant design.',
        'style': 'photorealistic product photography',
        'aspect_ratio': '4:3'
    },
    {
        'name': 'Wireless Gaming Mouse',
        'description': 'Futuristic gaming mouse with RGB lighting accents, ergonomic design, matte black finish with glossy side panels, high-precision sensor visible.',
        'style': 'photorealistic product photography with dramatic lighting',
        'aspect_ratio': '16:9'
    }
]


async def generate_mockups():
    """Generate synthetic product images and analyze them."""
    
    print("=" * 80)
    print("Synthetic Product Image Generation - Tutorial 21 Enhancement")
    print("=" * 80)
    print()
    print("This demo will:")
    print("1. Generate synthetic product images using Gemini 2.5 Flash Image")
    print("2. Analyze each generated image with the vision catalog agent")
    print("3. Create professional product catalog entries")
    print()
    print("=" * 80)
    print()
    
    # Create session service and runner
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="synthetic_generation_demo",
        agent=root_agent,
        session_service=session_service
    )
    
    # Create a session
    session_id = "generation_session"
    user_id = "demo_user"
    await session_service.create_session(
        session_id=session_id,
        user_id=user_id,
        app_name="synthetic_generation_demo"
    )
    
    # Generate and analyze each product
    for i, product in enumerate(PRODUCT_MOCKUPS, 1):
        print(f"\n{'=' * 80}")
        print(f"Product {i}/{len(PRODUCT_MOCKUPS)}: {product['name']}")
        print("=" * 80)
        print()
        print(f"Description: {product['description']}")
        print(f"Style: {product['style']}")
        print(f"Aspect Ratio: {product['aspect_ratio']}")
        print()
        
        # Step 1: Generate synthetic image
        print("🎨 Step 1: Generating synthetic product image...")
        print()
        
        generation_query = f"""
Please generate a synthetic product image using the generate_product_mockup tool:

Product Name: {product['name']}
Description: {product['description']}
Style: {product['style']}
Aspect Ratio: {product['aspect_ratio']}

After generating the image, please confirm the generation was successful.
        """.strip()
        
        try:
            # Create message content
            message = types.Content(
                parts=[types.Part(text=generation_query)],
                role="user"
            )
            
            # Execute generation
            generation_response = []
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message
            ):
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                generation_response.append(part.text)
            
            if generation_response:
                print('\n'.join(generation_response))
                print()
            else:
                print("❌ No generation confirmation received")
                continue
            
            # Small delay before analysis
            await asyncio.sleep(2)
            
            # Step 2: Load and analyze the generated image
            print()
            print("🔍 Step 2: Analyzing generated synthetic image...")
            print()
            
            # Find the generated image
            sample_dir = Path(__file__).parent / '_sample_images'
            safe_name = product['name'].lower().replace(' ', '_').replace('-', '_')
            generated_image_path = sample_dir / f"{safe_name}_generated.jpg"
            
            if not generated_image_path.exists():
                print(f"⚠️  Generated image not found at: {generated_image_path}")
                continue
            
            # Load the generated image
            image_part = load_image_from_file(str(generated_image_path))
            
            analysis_query = f"""
I'm uploading the synthetic image I just generated for {product['name']}.

Please analyze this synthetic product image and create a professional catalog entry.
Include:
1. Visual assessment of the generated image quality
2. Product features visible in the image
3. Design characteristics and aesthetic appeal
4. Suitability for marketing/e-commerce use
5. Professional product description

Note: This is a synthetically generated image, but analyze it as if it were a real product photo.
            """.strip()
            
            # Create message with image
            analysis_message = types.Content(
                parts=[
                    types.Part(text=analysis_query),
                    image_part
                ],
                role="user"
            )
            
            # Execute analysis
            analysis_response = []
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=analysis_message
            ):
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                analysis_response.append(part.text)
            
            if analysis_response:
                print('\n'.join(analysis_response))
                print()
            else:
                print("❌ No analysis result returned")
            
        except Exception as e:
            print(f"❌ Error processing {product['name']}: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
        
        # Delay between products
        if i < len(PRODUCT_MOCKUPS):
            await asyncio.sleep(2)
    
    print("=" * 80)
    print("✅ Synthetic Image Generation & Analysis Complete!")
    print("=" * 80)
    print()
    print("Generated images saved in: _sample_images/")
    print()
    print("Key Benefits:")
    print("- ✨ No photography equipment needed")
    print("- 🚀 Rapid prototyping and iteration")
    print("- 💰 Cost-effective product mockups")
    print("- 🎨 Consistent style and quality")
    print("- 📸 Professional product photography aesthetic")
    print()
    print("Next steps:")
    print("- Check generated images in _sample_images/")
    print("- Try the web interface: make dev")
    print("- Generate your own product mockups!")
    print()


async def main():
    """Main entry point."""
    try:
        await generate_mockups()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
