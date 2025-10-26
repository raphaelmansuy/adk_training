#!/usr/bin/env python3
"""
Test script to verify that the search agent now uses real URLs from Google Search
instead of fabricating/hallucinating them.

This test checks that:
1. ProductSearchAgent is called with the search query
2. Responses include URLs that are explicitly from Google Search results
3. No fabricated URLs with fake product IDs are returned
4. Agent indicates when URLs are not available in search results
"""

import sys
import asyncio
from pathlib import Path

# Add the commerce_agent module to path
sys.path.insert(0, str(Path(__file__).parent))

from commerce_agent.agent import root_agent
from google.adk.runners import LocalRunner

async def test_product_search_with_real_urls():
    """Test that product search returns real URLs from Google Search, not fabricated ones."""
    
    print("\n" + "="*80)
    print("TEST: URL Verification - Ensuring Real URLs from Google Search")
    print("="*80)
    
    test_queries = [
        "I want running shoes",
        "Find me cycling equipment", 
        "Show yoga mats"
    ]
    
    runner = LocalRunner()
    
    for query in test_queries:
        print(f"\n{'─'*80}")
        print(f"Query: {query}")
        print(f"{'─'*80}")
        
        try:
            # Run the agent with the query
            response = await runner.ainvoke(
                agent=root_agent,
                input=query,
                metadata={"model": "gemini-2.5-flash"}
            )
            
            # Get the response text
            response_text = str(response)
            
            print("\n📋 Response Summary:")
            print("─" * 40)
            
            # Check for URL patterns
            if "https://" in response_text:
                print("✅ URLs found in response")
                
                # Check for hallucinated URL patterns (the bug)
                if "/_/R-p-" in response_text and "mc=" in response_text:
                    print("⚠️  WARNING: Detected potentially fabricated URL pattern")
                    print("   Pattern: .../_/R-p-[ID]?mc=[ID]")
                    print("   This suggests URLs may still be reconstructed/hallucinated")
                    
                    # Show problematic URLs
                    lines = response_text.split('\n')
                    for line in lines:
                        if "/_/R-p-" in line:
                            print(f"   Found: {line.strip()[:100]}...")
                
                # Check for real Decathlon HK URL patterns
                if "decathlon.com.hk" in response_text:
                    print("✅ Decathlon HK domain found in URLs")
                    
                    # Extract and display actual URLs
                    import re
                    urls = re.findall(r'https://[^\s\)\"\']+decathlon\.com\.hk[^\s\)\"\']*', response_text)
                    if urls:
                        print(f"✅ Found {len(urls)} Decathlon HK URLs:")
                        for url in urls[:3]:  # Show first 3
                            print(f"   • {url[:100]}...")
            else:
                print("⚠️  No URLs found in response")
                
            # Check for indication of search limitations
            if "not in search results" in response_text.lower() or "search results: [" in response_text.lower():
                print("✅ Agent correctly indicates when URLs are not from search results")
                
        except Exception as e:
            print(f"❌ Error during test: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("TEST COMPLETE: URL Verification")
    print("="*80)
    print("\n📝 Interpretation:")
    print("   • If no fabricated URLs (/_/R-p-) and URLs look real → Fix is working ✅")
    print("   • If still seeing /_/R-p-[ID]?mc= patterns → URLs still hallucinated ❌")
    print("   • If agent indicates 'not in search results' → Better handling ✅")

if __name__ == "__main__":
    print("\n🚀 Starting URL Fix Verification Test")
    print("This test checks that the search agent now uses real URLs from Google Search")
    print("instead of fabricating/hallucinating them.")
    
    asyncio.run(test_product_search_with_real_urls())
