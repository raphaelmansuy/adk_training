# Expensive Build Documentation (Docusaurus Build)

**Date**: 2025-10-21 12:04:00

## Summary
Documented comprehensive patterns for running expensive Docusaurus builds in separate shell processes without blocking the main VSCode terminal or development workflow.

## Changes Made
Updated `.github/copilot-instructions.md` with a new section "Running Expensive Builds (Docusaurus Build)" that includes:

### Three Build Patterns
1. **Pattern 1: Run in Background and Wait (Simple)**
   - Simple background job with wait
   - Useful for fire-and-forget builds

2. **Pattern 2: Capture Exit Status with PIPESTATUS (Recommended for zsh)**
   - Uses `set -o pipefail` to capture exit codes
   - Shows `echo $pipestatus` and `echo $status` for verification
   - Best for verifying build success

3. **Pattern 3: Disown and Track Job (Advanced)**
   - Uses `&!` to fully detach from current shell
   - Allows continuing work while build runs in background
   - Shows how to track with `jobs -l` and wait for specific job

### Typical Build Workflow
5-step workflow included:
- Open separate terminal
- Run build with output capture
- Wait for completion
- Check exit status
- Run link verification after build

### Link Verification Section
Added guidance on running `scripts/verify_links.py`:
- `--skip-external` for quick internal link check
- Full verification for internal + external links
- `--json-output` for analysis export

## Context
This documentation emerged from successfully running the Docusaurus build in the background and conducting link verification. The patterns ensure:
- Non-blocking builds in VSCode terminal
- Proper exit status capture in zsh
- Clean workflow for build + verification cycle

## Related Files
- `.github/copilot-instructions.md` - Updated with new section
- `scripts/verify_links.py` - Link verification script referenced
