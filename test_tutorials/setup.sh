#!/bin/bash
# Setup script for ADK tutorial tests

echo "🔧 Setting up ADK Tutorial Tests"
echo "================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing..."
    pip install pytest pytest-json-report httpx
else
    echo "✓ pytest is installed"
fi

echo ""
echo "📦 Installing dependencies for each tutorial..."
echo ""

# Tutorial 29
if [ -d "tutorial29_test/backend" ]; then
    echo "→ Tutorial 29"
    cd tutorial29_test/backend
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt -q
        echo "  ✓ Dependencies installed"
    fi
    cd ../..
fi

# Tutorial 30
if [ -d "tutorial30_test/backend" ]; then
    echo "→ Tutorial 30"
    cd tutorial30_test/backend
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt -q
        echo "  ✓ Dependencies installed"
    fi
    cd ../..
fi

# Tutorial 31
if [ -d "tutorial31_test/backend" ]; then
    echo "→ Tutorial 31"
    cd tutorial31_test/backend
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt -q
        echo "  ✓ Dependencies installed"
    fi
    cd ../..
fi

# Tutorial 32
if [ -d "tutorial32_test/backend" ]; then
    echo "→ Tutorial 32"
    cd tutorial32_test/backend
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt -q
        echo "  ✓ Dependencies installed"
    fi
    cd ../..
fi

# Tutorial 33
if [ -d "tutorial33_test/backend" ]; then
    echo "→ Tutorial 33"
    cd tutorial33_test/backend
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt -q
        echo "  ✓ Dependencies installed"
    fi
    cd ../..
fi

# Tutorial 34
if [ -d "tutorial34_test/backend" ]; then
    echo "→ Tutorial 34"
    cd tutorial34_test/backend
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt -q
        echo "  ✓ Dependencies installed"
    fi
    cd ../..
fi

# Tutorial 35
if [ -d "tutorial35_test/backend" ]; then
    echo "→ Tutorial 35"
    cd tutorial35_test/backend
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt -q
        echo "  ✓ Dependencies installed"
    fi
    cd ../..
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run tests:"
echo "  python run_all_tests.py"
echo ""
echo "Or run individual tutorial tests:"
echo "  cd tutorial29_test/backend && pytest test_agent.py -v"
echo "  cd tutorial30_test/backend && pytest test_agent.py -v"
