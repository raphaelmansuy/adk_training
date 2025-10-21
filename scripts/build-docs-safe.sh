#!/bin/bash
# Safe Docusaurus Build Script
# This script ensures builds run without PTY issues
# Works from any terminal, including VSCode

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOCS_DIR="/Users/raphaelmansuy/Github/03-working/adk_training/docs"
BUILD_LOG="$DOCS_DIR/build.log"
NODE_MEMORY="4096"

# Function to print colored messages
print_status() {
  echo -e "${BLUE}[BUILD]${NC} $1"
}

print_success() {
  echo -e "${GREEN}✓${NC} $1"
}

print_error() {
  echo -e "${RED}✗${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}⚠${NC} $1"
}

# Function to check if running from VSCode terminal
is_vscode_terminal() {
  # Check for VSCode terminal indicators
  [[ -n "${TERM_PROGRAM:-}" && "$TERM_PROGRAM" == "vscode" ]] && return 0
  [[ -n "${TERM:-}" && "$TERM" == "xterm-256color" ]] && return 0
  return 1
}

# Function to run build properly detached
run_build_detached() {
  print_status "Setting up environment..."
  export NODE_OPTIONS=--max-old-space-size=${NODE_MEMORY}
  print_success "Node memory set to ${NODE_MEMORY}MB"

  print_status "Starting build process..."
  cd "$DOCS_DIR"

  # Use nohup for proper detachment
  nohup npm run build > "$BUILD_LOG" 2>&1 &
  local BUILD_PID=$!

  print_success "Build started (PID: $BUILD_PID)"
  print_status "Build output: tail -f $BUILD_LOG"
  echo ""
  print_warning "Build running in background. You can close this terminal."
  echo ""

  # Show initial output
  sleep 2
  tail -20 "$BUILD_LOG"
  echo ""
  print_status "Monitoring build progress..."
  echo ""

  # Wait for build to complete
  while kill -0 $BUILD_PID 2>/dev/null; do
    sleep 5
    # Show dots to indicate progress
    echo -n "."
  done

  echo ""
  echo ""

  # Check build status
  if [ -f "$BUILD_LOG" ]; then
    if grep -q "SUCCESS\|Generated static files" "$BUILD_LOG"; then
      print_success "Build completed successfully!"
      echo ""
      print_status "Build output (last 20 lines):"
      tail -20 "$BUILD_LOG"
      return 0
    else
      print_error "Build may have failed. Check log:"
      tail -50 "$BUILD_LOG"
      return 1
    fi
  else
    print_error "Build log not found"
    return 1
  fi
}

# Function to show VSCode terminal warning
show_vscode_warning() {
  echo ""
  echo -e "${RED}════════════════════════════════════════════════════════════════${NC}"
  echo -e "${RED}⚠  CRITICAL: Running from VSCode Integrated Terminal${NC}"
  echo -e "${RED}════════════════════════════════════════════════════════════════${NC}"
  echo ""
  print_warning "VSCode integrated terminal detected!"
  echo ""
  echo "This can cause PTY host disconnect during the build."
  echo ""
  echo "OPTIONS:"
  echo ""
  echo "1. RECOMMENDED: Use external terminal"
  echo "   - Open Terminal.app (Command+Space > Terminal)"
  echo "   - Run: bash $0"
  echo ""
  echo "2. Continue anyway (May crash)"
  echo "   - Type: yes"
  echo ""
  echo -e "${RED}════════════════════════════════════════════════════════════════${NC}"
  echo ""

  read -p "Continue from VSCode terminal? (yes/no): " response

  if [ "$response" = "yes" ]; then
    print_warning "Proceeding at your own risk..."
    return 0
  else
    print_status "Please run this script from an external terminal:"
    echo "  1. Open Terminal.app (Command+Space > Terminal)"
    echo "  2. Run: bash $0"
    exit 0
  fi
}

# Main execution
main() {
  print_status "Docusaurus Safe Build Script"
  echo ""

  # Check if running from VSCode terminal
  if is_vscode_terminal; then
    show_vscode_warning
  fi

  # Run the build
  run_build_detached

  echo ""
  print_status "Next steps:"
  echo "  1. Verify links: python3 scripts/verify_links.py --skip-external"
  echo "  2. Check build: ls -lh $DOCS_DIR/build/ | head -10"
  echo ""
  print_success "Build script completed!"
}

# Run main function
main "$@"
