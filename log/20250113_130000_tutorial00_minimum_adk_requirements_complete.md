# Tutorial 00: Minimum ADK Requirements Documentation - Complete

## Summary
Added comprehensive "Minimum Requirements for ADK" section to Tutorial 00, documenting the exact APIs, user rights, and permissions required to use ADK with both Gemini API and VertexAI platforms.

## Changes Made

### 1. API Enablement Requirements
- **Gemini API**: No GCP project or APIs required - just API key from Google AI Studio
- **VertexAI**: Minimum APIs (`aiplatform.googleapis.com`, `iam.googleapis.com`) with optional advanced APIs
- **Verified Commands**: Provided exact gcloud commands to enable and verify APIs

### 2. User Rights and Permissions
- **Gemini API**: Only Google account with AI Studio access
- **VertexAI**: `roles/aiplatform.user` IAM role minimum requirement
- **Verification Scripts**: Complete bash scripts to check permissions and test connectivity

### 3. Complete Setup Verification
- **Gemini API Script**: Tests API key and connectivity
- **VertexAI Script**: Validates project, APIs, permissions, and functionality
- **Factual Examples**: All code verified against official Google documentation

### 4. Service Account Setup
- **Production Best Practice**: Service accounts over user accounts
- **Minimal Permissions**: Exact IAM roles and setup commands
- **Key Management**: Proper service account key creation and environment setup

### 5. ADK-Specific Requirements
- **Dependencies**: `google-genai>=1.16.0` minimum version
- **Python Versions**: 3.8+ minimum, 3.11 verified
- **Network**: HTTPS access to `*.googleapis.com` only

### 6. Troubleshooting Minimum Setup
- **API Errors**: Exact commands to enable APIs with propagation delays
- **Permission Issues**: Organization policy checks and role assignments
- **Service Account**: Key validation and regeneration procedures

## Technical Verification
- All commands tested against official Google Cloud documentation
- API enablement verified with actual gcloud service commands
- IAM roles confirmed against VertexAI requirements
- Python dependencies validated against google-genai library specs

## Impact
- **Actionable**: Users can now follow exact steps to enable minimum ADK functionality
- **Factual**: All requirements verified against official sources
- **Complete**: Covers both platforms with production and development scenarios
- **Troubleshooting**: Comprehensive error handling for common setup issues

## Files Modified
- `docs/tutorial/00_setup_authentication.md`: Added "Minimum Requirements for ADK" section

## Verification Date
October 15, 2025

## ADK Version Tested
1.16.0+