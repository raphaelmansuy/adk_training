"""
Demo script for Tutorial 21: Multimodal and Image Processing
Demonstrates vision-based product catalog analysis

NOTE: For uploaded images, use the ADK web interface:
1. Run: adk web
2. Open http://localhost:8000
3. Select 'vision_catalog_agent' from dropdown
4. Drag and drop or paste images directly into the chat
5. Ask: "Analyze this product and create a catalog entry"

This demo script shows file-based image processing.
"""

import asyncio
import os
from pathlib import Path

from google.adk.runners import Runner
from vision_catalog_agent import root_agent
from vision_catalog_agent.agent import create_sample_image


async def setup_demo_images():
    """Create sample images for demonstration."""
    print("Setting up demo images...")
    
    sample_dir = Path(__file__).parent / '_sample_images'
    sample_dir.mkdir(exist_ok=True)
    
    sample_images = [
        ('laptop.jpg', (100, 120, 140), 'Professional Laptop'),
        ('headphones.jpg', (50, 50, 50), 'Wireless Headphones'),
        ('smartwatch.jpg', (80, 100, 120), 'Smart Watch')
    ]
    
    created = []
    for filename, color, description in sample_images:
        path = sample_dir / filename
        if not path.exists():
            create_sample_image(str(path), color)
            created.append(f"  ✓ {filename} ({description})")
        else:
            created.append(f"  • {filename} ({description}) [exists]")
    
    print("\nDemo images ready:")
    for item in created:
        print(item)
    
    return sample_dir


async def demo_basic_analysis():
    """Demo 1: Basic image analysis."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Image Analysis")
    print("="*70)
    
    sample_dir = await setup_demo_images()
    laptop_path = sample_dir / 'laptop.jpg'
    
    runner = Runner()
    
    query = f"Analyze the image at {laptop_path} and describe what you see."
    
    print(f"\nQuery: {query}")
    print("\nProcessing...\n")
    
    result = await runner.run_async(query, agent=root_agent)
    
    print("RESULT:")
    print(result.content.parts[0].text)
    print("\n" + "="*70)


async def demo_catalog_entry():
    """Demo 2: Generate catalog entry."""
    print("\n" + "="*70)
    print("DEMO 2: Generate Product Catalog Entry")
    print("="*70)
    
    sample_dir = await setup_demo_images()
    headphones_path = sample_dir / 'headphones.jpg'
    
    runner = Runner()
    
    query = f"""
Analyze the image at {headphones_path} and create a professional 
product catalog entry with description, features, and specifications.
    """.strip()
    
    print(f"\nQuery: {query}")
    print("\nProcessing...\n")
    
    result = await runner.run_async(query, agent=root_agent)
    
    print("RESULT:")
    print(result.content.parts[0].text)
    print("\n" + "="*70)


async def demo_compare_images():
    """Demo 3: Compare multiple images."""
    print("\n" + "="*70)
    print("DEMO 3: Compare Multiple Product Images")
    print("="*70)
    
    sample_dir = await setup_demo_images()
    laptop_path = sample_dir / 'laptop.jpg'
    smartwatch_path = sample_dir / 'smartwatch.jpg'
    
    runner = Runner()
    
    query = f"""
Compare these two product images:
1. {laptop_path}
2. {smartwatch_path}

Identify similarities, differences, and unique features of each.
    """.strip()
    
    print(f"\nQuery: {query}")
    print("\nProcessing...\n")
    
    result = await runner.run_async(query, agent=root_agent)
    
    print("RESULT:")
    print(result.content.parts[0].text)
    print("\n" + "="*70)


async def demo_batch_processing():
    """Demo 4: Batch process multiple products."""
    print("\n" + "="*70)
    print("DEMO 4: Batch Process Product Catalog")
    print("="*70)
    
    sample_dir = await setup_demo_images()
    
    runner = Runner()
    
    query = f"""
Analyze all product images in {sample_dir}/ and create a summary 
catalog with entries for each product.
    """.strip()
    
    print(f"\nQuery: {query}")
    print("\nProcessing...\n")
    
    result = await runner.run_async(query, agent=root_agent)
    
    print("RESULT:")
    print(result.content.parts[0].text)
    print("\n" + "="*70)


async def main():
    """Main demo runner."""
    print("\n" + "="*70)
    print("Tutorial 21: Multimodal and Image Processing - Demo")
    print("="*70)
    
    # Show uploaded images info
    print("\n💡 TIP: For the best experience with uploaded images:")
    print("   1. Run: adk web")
    print("   2. Open: http://localhost:8000")
    print("   3. Select: 'vision_catalog_agent' from dropdown")
    print("   4. Drag and drop or paste images directly into chat")
    print("   5. Ask: 'Analyze this product and create a catalog entry'")
    print("\n   This demo shows file-based image processing.")
    
    # Check environment
    if not os.getenv('GOOGLE_API_KEY') and not os.getenv('GOOGLE_GENAI_USE_VERTEXAI'):
        print("\n⚠️  WARNING: GOOGLE_API_KEY not set!")
        print("Set your API key: export GOOGLE_API_KEY=your_key")
        print("\nRunning in demo mode with mock data...\n")
    
    demos = [
        ("Basic Image Analysis", demo_basic_analysis),
        ("Generate Catalog Entry", demo_catalog_entry),
        ("Compare Images", demo_compare_images),
        ("Batch Processing", demo_batch_processing)
    ]
    
    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    
    print("\nSelect demo (1-4, or 'all' to run all): ", end='')
    
    try:
        choice = input().strip().lower()
        
        if choice == 'all':
            for name, demo_func in demos:
                try:
                    await demo_func()
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"\n❌ Error in {name}: {e}")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            name, demo_func = demos[int(choice) - 1]
            await demo_func()
        else:
            print("Invalid choice. Running all demos...")
            for name, demo_func in demos:
                try:
                    await demo_func()
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"\n❌ Error in {name}: {e}")
    
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "="*70)
    print("Demo Complete!")
    print("="*70)
    print("\nNext Steps:")
    print("  • Run 'make dev' to start ADK web interface")
    print("  • Try your own images with the agent")
    print("  • Check README.md for more examples")
    print("  • Run 'make test' to verify functionality")
    print()


if __name__ == '__main__':
    asyncio.run(main())
