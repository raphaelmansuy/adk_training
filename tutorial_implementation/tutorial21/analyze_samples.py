#!/usr/bin/env python3
"""
Analyze all sample images using the Vision Catalog Agent.

This script demonstrates the multimodal capabilities by analyzing
the three sample product images: laptop, headphones, and smartwatch.
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


async def analyze_all_samples():
    """Analyze all three sample images."""
    
    # Get sample images directory
    sample_dir = Path(__file__).parent / '_sample_images'
    
    if not sample_dir.exists():
        print("❌ Sample images directory not found!")
        print(f"Expected: {sample_dir}")
        print("\nRun: make download-images")
        return
    
    # Define sample images with product IDs
    samples = [
        {
            'product_id': 'LAPTOP-001',
            'filename': 'laptop.jpg',
            'name': 'Professional Laptop'
        },
        {
            'product_id': 'AUDIO-001',
            'filename': 'headphones.jpg',
            'name': 'Premium Headphones'
        },
        {
            'product_id': 'WATCH-001',
            'filename': 'smartwatch.jpg',
            'name': 'Smart Watch'
        }
    ]
    
    print("=" * 80)
    print("Vision Catalog Agent - Sample Image Analysis")
    print("=" * 80)
    print()
    
    # Create session service and runner
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="vision_catalog_demo",
        agent=root_agent,
        session_service=session_service
    )
    
    # Create a session
    session_id = "analysis_session"
    user_id = "demo_user"
    await session_service.create_session(
        session_id=session_id,
        user_id=user_id,
        app_name="vision_catalog_demo"
    )
    
    # Analyze each sample image
    for i, sample in enumerate(samples, 1):
        image_path = sample_dir / sample['filename']
        
        if not image_path.exists():
            print(f"⚠️  Image not found: {image_path}")
            continue
        
        print(f"\n{'=' * 80}")
        print(f"Image {i}/3: {sample['name']} ({sample['filename']})")
        print(f"Product ID: {sample['product_id']}")
        print(f"Path: {image_path}")
        print("=" * 80)
        print()
        
        # Load the image
        try:
            image_part = load_image_from_file(str(image_path))
        except Exception as e:
            print(f"❌ Failed to load image: {e}")
            continue
        
        # Create a query for analysis with the image
        query_text = f"""
I'm uploading an image of a product for you to analyze.

Product ID: {sample['product_id']}
Product Name: {sample['name']}

Please analyze this image and create a professional product catalog entry.
Include:
1. Product identification and category
2. Visual features (colors, design, materials)
3. Quality indicators
4. Distinctive features
5. Market positioning and target audience

Provide a complete, marketing-ready description.
        """.strip()
        
        try:
            # Run the agent with the query
            print("🔍 Analyzing image...")
            print()
            
            # Create message content with both text and image
            message = types.Content(
                parts=[
                    types.Part(text=query_text),
                    image_part
                ],
                role="user"
            )
            
            # Execute the query using the ADK Runner
            response_text = []
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message
            ):
                # Collect text from events
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response_text.append(part.text)
            
            # Display the result
            if response_text:
                print('\n'.join(response_text))
                print()
            else:
                print("❌ No analysis result returned")
            
        except Exception as e:
            print(f"❌ Error analyzing {sample['filename']}: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
        
        # Small delay between analyses
        if i < len(samples):
            await asyncio.sleep(1)
    
    print("=" * 80)
    print("✅ Analysis Complete!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("- Try the web interface: make dev")
    print("- Upload your own images for analysis")
    print("- Compare multiple images: compare_product_images()")
    print()


async def main():
    """Main entry point."""
    try:
        await analyze_all_samples()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
