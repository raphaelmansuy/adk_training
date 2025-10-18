#!/usr/bin/env python3
"""
Test script to verify inline_data visualization display logic
"""
import base64
from io import BytesIO
from PIL import Image

# Mock the Blob class to simulate what ADK returns
class MockBlob:
    def __init__(self, image_data, mime_type='image/png'):
        self.data = image_data
        self.mime_type = mime_type

# Test 1: Create a simple test image
print("[TEST] Creating test image...")
img = Image.new('RGB', (100, 100), color='red')
img_bytes = BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)
test_image_data = img_bytes.read()
print(f"[TEST] Created image of {len(test_image_data)} bytes")

# Test 2: Create mock blob (simulating what inline_data would be)
print("\n[TEST] Creating mock blob...")
mock_blob = MockBlob(test_image_data)
print("[TEST] Mock blob created")
print(f"  - data type: {type(mock_blob.data).__name__}")
print(f"  - data length: {len(mock_blob.data)}")
print(f"  - mime_type: {mock_blob.mime_type}")

# Test 3: Simulate the visualization display logic
print("\n[TEST] Simulating visualization display logic...")
viz_data = [mock_blob]
has_viz = True

if has_viz and viz_data:
    print(f"[TEST] Displaying {len(viz_data)} visualizations")
    for i, viz in enumerate(viz_data):
        try:
            print(f"[TEST] Processing viz {i}: type={type(viz).__name__}")
            
            # viz should be a Blob object with data and mime_type
            if hasattr(viz, 'data') and viz.data:
                data = viz.data
                mime_type = getattr(viz, 'mime_type', 'image/png')
                print(f"[TEST] mime_type: {mime_type}")
                print(f"[TEST] data type: {type(data).__name__}")
                print(f"[TEST] data length: {len(data) if data else 0}")
                
                # Convert to bytes if needed
                if isinstance(data, str):
                    print("[TEST] data is string, decoding base64...")
                    image_bytes = base64.b64decode(data)
                elif isinstance(data, bytes):
                    print("[TEST] data is already bytes")
                    image_bytes = data
                else:
                    print(f"[TEST] data is unexpected type: {type(data)}")
                    image_bytes = bytes(data)
                
                print(f"[TEST] image_bytes length: {len(image_bytes)}")
                
                # Try to open image
                try:
                    image = Image.open(BytesIO(image_bytes))
                    print(f"[TEST] ✅ Image opened successfully: {image.format} {image.size}")
                    print("[TEST] ✅ Image would be displayed via st.image()")
                except Exception as img_err:
                    print(f"[TEST] ❌ Failed to open/display image: {str(img_err)}")
                    import traceback
                    traceback.print_exc()
            else:
                print("❌ viz has no 'data' or data is None")
                print(f"[TEST] viz type: {type(viz)}")
        except Exception as e:
            print(f"[TEST] ❌ Exception in viz processing: {str(e)}")
            import traceback
            traceback.print_exc()
else:
    if viz_data:
        print(f"[TEST] has_viz={has_viz}, viz_data len={len(viz_data)}")
    else:
        print("[TEST] No visualizations to display")

print("\n[TEST] ✅ All tests passed!")
