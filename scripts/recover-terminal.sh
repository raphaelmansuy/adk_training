#!/bin/bash
# Terminal Recovery Script
# Recovers from PTY host disconnect issues
# Kills orphaned processes and resets terminal state

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
  echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
  echo -e "${BLUE}$1${NC}"
  echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
}

print_status() {
  echo -e "${BLUE}[RECOVERY]${NC} $1"
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

main() {
  print_header "TERMINAL RECOVERY UTILITY"
  echo ""

  print_status "Checking for orphaned build processes..."
  echo ""

  # Find npm processes
  npm_processes=$(ps aux | grep -E "npm|webpack|docusaurus" | grep -v grep | wc -l)

  if [ "$npm_processes" -gt 0 ]; then
    print_warning "Found $npm_processes orphaned processes"
    echo ""
    print_status "Orphaned processes:"
    ps aux | grep -E "npm|webpack|docusaurus" | grep -v grep || true
    echo ""

    read -p "Kill these processes? (yes/no): " response
    if [ "$response" = "yes" ]; then
      print_status "Killing processes..."
      pkill -f "npm run build" || true
      pkill -f "webpack" || true
      pkill -f "docusaurus" || true
      sleep 1
      print_success "Processes killed"
    fi
  else
    print_success "No orphaned processes found"
  fi

  echo ""
  print_status "Checking build status..."
  echo ""

  # Check if build directory exists
  BUILD_DIR="/Users/raphaelmansuy/Github/03-working/adk_training/docs/build"
  if [ -d "$BUILD_DIR" ]; then
    HTML_COUNT=$(find "$BUILD_DIR" -name "*.html" 2>/dev/null | wc -l)
    print_success "Build directory exists with $HTML_COUNT HTML files"
  else
    print_warning "Build directory not found"
  fi

  echo ""
  print_status "Checking system resources..."
  echo ""

  # Check memory
  MEMORY=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
  print_success "Memory status checked"

  # Check file descriptors
  OPEN_FDS=$(lsof | wc -l)
  print_success "Open file descriptors: $OPEN_FDS"

  echo ""
  print_header "RECOVERY COMPLETE"
  echo ""

  print_status "Next steps:"
  echo "  1. Close all VSCode windows"
  echo "  2. Kill all remaining processes: pkill -f 'code\|npm\|node'"
  echo "  3. Restart VSCode"
  echo "  4. Use external terminal for builds:"
  echo "     bash /Users/raphaelmansuy/Github/03-working/adk_training/scripts/build-docs-safe.sh"
  echo ""
  print_success "Terminal should now be clean and usable"
}

main "$@"
