# Tutorial 37: Enterprise Compliance & Policy Navigator

**Using Google ADK with Gemini File Search API for Native RAG**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Google ADK](https://img.shields.io/badge/google--adk-1.16.0+-green.svg)](https://github.com/google/adk-python)

## 🎯 Overview

This tutorial implements a **production-ready multi-agent system** for managing, searching, and analyzing company policies using **Google's Gemini File Search API** for native Retrieval Augmented Generation (RAG).

**📖 Full Tutorial**: [Tutorial 37: Native RAG with File Search](https://github.com/raphaelmansuy/adk_training/tree/main/docs/docs/37_file_search_policy_navigator.md)

### Business Value

- **$150K-$200K annual savings** for mid-sized companies
- **$4K-$5K implementation cost** (10-day payback period)
- **3000%+ ROI** on first year investment
- **99% faster** policy access (45 minutes → 30 seconds)
- **Audit-ready** with built-in citation tracking and compliance trails

### Key Features

✅ **Native File Search Integration** - Persistent document storage with semantic search  
✅ **Multi-Agent Architecture** - Document Manager, Search Specialist, Compliance Advisor, Report Generator  
✅ **Metadata Management** - Organize policies by department, type, jurisdiction, sensitivity  
✅ **Citation Tracking** - Automatic source attribution for compliance  
✅ **Audit Trails** - Track all policy access and decisions  
✅ **Production Ready** - Error handling, logging, and observability  

## 📁 Project Structure

```
tutorial37/
├── policy_navigator/           # Main package
│   ├── __init__.py            # Package exports
│   ├── agent.py               # Multi-agent system
│   ├── tools.py               # Core File Search tools (8 functions)
│   ├── stores.py              # Store management utilities
│   ├── config.py              # Configuration and environment
│   ├── metadata.py            # Metadata schemas and filters
│   └── utils.py               # Helper utilities
├── sample_policies/           # Example policy documents
│   ├── hr_handbook.md
│   ├── it_security_policy.md
│   ├── remote_work_policy.md
│   └── code_of_conduct.md
├── tests/                     # Comprehensive test suite
│   └── test_core.py          # Unit and integration tests
├── demos/                     # Demo scripts
│   ├── demo_upload.py        # Upload policies
│   ├── demo_search.py        # Search examples
│   └── demo_full_workflow.py  # Complete workflow
├── docs/                      # Documentation
│   ├── architecture.md
│   ├── roi_calculator.md
│   └── deployment_guide.md
├── Makefile                   # Standard build commands
├── pyproject.toml             # Python project configuration
├── requirements.txt           # Dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google API key with Gemini access
- ~10 MB free storage for sample policies

### Setup & Run Complete Workflow

```bash
# 1. Navigate to tutorial directory
cd tutorial_implementation/tutorial37

# 2. Install dependencies
make setup

# 3. Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Create File Search stores and upload policies
python demos/demo_upload.py

# 5. Search policies (after stores are created)
python demos/demo_search.py

# 6. Run complete workflow
python demos/demo_full_workflow.py
```

### Important Note: File Search Setup

File Search requires that stores be created and populated with documents **before** searching. The workflow is:

1. **Create stores**: `client.file_search_stores.create()`
2. **Upload documents**: `client.file_search_stores.upload_to_file_search_store()`
3. **Search**: Use the model with file_search configuration

The `demo_upload.py` script handles steps 1-2. Run it first before running `demo_search.py`.

### Interactive Use

Start the ADK web interface for interactive testing:

```bash
make dev
# Opens http://localhost:8000
```

## 📚 Core Concepts

### File Search vs Traditional RAG

| Feature | File Search | External Vector DB |
|---------|-------------|-------------------|
| **Setup** | Simple (1 function) | Complex (embed → index → search) |
| **Cost** | $0.15/M tokens (index only) | $0.15/M + $25+/month DB |
| **Storage** | Persistent (indefinite) | External (requires management) |
| **Citations** | Built-in | Manual extraction |
| **Search Quality** | Excellent (Gemini embeddings) | Varies (custom embeddings) |

### Architecture

```
User Query
    ↓
Root Agent (Orchestrator)
    ├─→ Document Manager Agent
    │   └─ Upload & organize policies
    ├─→ Search Specialist Agent  
    │   └─ Semantic search, filtering
    ├─→ Compliance Advisor Agent
    │   └─ Risk assessment, comparison
    └─→ Report Generator Agent
        └─ Summaries, audit trails
    ↓
File Search Store(s)
    └─ Policy documents (indexed & searchable)
    ↓
Gemini 2.5-Flash LLM
    └─ Semantic search, analysis, synthesis
    ↓
Response with Citations
```

## 🛠️ Core Tools

The system provides **8 specialized tools**:

### 1. upload_policy_documents()
Upload and index multiple policies to File Search stores.

```python
from policy_navigator.tools import upload_policy_documents

result = upload_policy_documents(
    file_paths=["hr_handbook.md", "it_security_policy.md"],
    store_name="policy-navigator-hr",
    metadata_list=[metadata1, metadata2]
)
```

### 2. search_policies()
Semantic search across policy documents with citations.

```python
result = search_policies(
    query="What are the vacation day policies?",
    store_name="policy-navigator-hr"
)
# Returns: answer + citations from source documents
```

### 3. filter_policies_by_metadata()
Filter policies by department, type, jurisdiction, sensitivity.

```python
result = filter_policies_by_metadata(
    store_name="policy-navigator-hr",
    department="HR",
    policy_type="handbook"
)
```

### 4. compare_policies()
Compare policies across multiple stores or documents.

```python
result = compare_policies(
    query="Compare vacation policies across departments",
    store_names=["policy-navigator-hr", "policy-navigator-it"]
)
```

### 5. check_compliance_risk()
Assess compliance risks and provide recommendations.

```python
result = check_compliance_risk(
    query="Can employees work from another country?",
    store_name="policy-navigator-hr"
)
```

### 6. extract_policy_requirements()
Extract specific requirements in structured format.

```python
result = extract_policy_requirements(
    query="password requirements",
    store_name="policy-navigator-it"
)
```

### 7. generate_policy_summary()
Generate concise summaries of policy information.

```python
result = generate_policy_summary(
    query="remote work benefits",
    store_name="policy-navigator-hr"
)
```

### 8. create_audit_trail()
Create audit trail entries for compliance and governance.

```python
result = create_audit_trail(
    action="search",
    user="john.doe@company.com",
    query="remote work policy",
    result_summary="Retrieved remote work policy"
)
```

## 📖 Usage Examples

### Example 1: Employee Asks About Remote Work

```python
from policy_navigator.agent import root_agent

question = "Can I work from home? What do I need to do?"

response = root_agent(question)
# Agent:
# 1. Searches HR policies
# 2. Finds remote work policy
# 3. Returns requirements with citations
```

### Example 2: Compliance Team Compares Policies

```python
from policy_navigator.tools import compare_policies

result = compare_policies(
    query="How do vacation policies differ across departments?",
    store_names=["policy-navigator-hr", "policy-navigator-it"]
)

# Returns structured comparison with differences and recommendations
```

### Example 3: Manager Needs Quick Brief

```python
from policy_navigator.tools import generate_policy_summary

result = generate_policy_summary(
    query="What are the key points of our benefits package?",
    store_name="policy-navigator-hr"
)

# Returns: Executive summary with key points and action items
```

## 🧪 Testing

Run comprehensive test suite:

```bash
# All tests
make test

# Unit tests only
make test-unit

# Integration tests (requires API key)
make test-int

# Check coverage
pytest tests/ --cov=policy_navigator --cov-report=html
```

## 📊 Configuration

### Environment Variables (.env)

```env
# Required
GOOGLE_API_KEY=your-api-key

# Optional
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# File Search Stores
HR_STORE_NAME=policy-navigator-hr
IT_STORE_NAME=policy-navigator-it
LEGAL_STORE_NAME=policy-navigator-legal
SAFETY_STORE_NAME=policy-navigator-safety

# Model
DEFAULT_MODEL=gemini-2.5-flash

# Debug
DEBUG=false
```

### Metadata Schema

Documents can be tagged with metadata for advanced filtering:

```python
from policy_navigator.metadata import MetadataSchema

metadata = MetadataSchema.create_metadata(
    department="HR",
    policy_type="handbook",
    effective_date="2025-01-01",
    jurisdiction="US",
    sensitivity="internal",
    version=1,
    owner="hr@company.com",
    review_cycle_months=12
)
```

## 🔍 Advanced Features

### Multiple Stores

Organize policies by type or department:

```python
from policy_navigator.stores import create_policy_store

hr_store = create_policy_store("company-hr-policies")
it_store = create_policy_store("company-it-procedures")
legal_store = create_policy_store("legal-compliance")
```

### Metadata Filtering

Find specific policies using AIP-160 filter syntax:

```python
from policy_navigator.metadata import MetadataSchema

# Build filter
filter_str = MetadataSchema.build_metadata_filter(
    department="IT",
    sensitivity="confidential",
    jurisdiction="US"
)

# Use in search
result = search_policies(
    query="security policies",
    store_name="policy-navigator-it",
    metadata_filter=filter_str
)
```

### Audit Trail

Track all policy access for compliance:

```python
from policy_navigator.tools import create_audit_trail

create_audit_trail(
    action="search",
    user="manager@company.com",
    query="remote work approval criteria",
    result_summary="Found remote work policy with approval process"
)
```

## 📈 Performance & Costs

### Indexing Costs

- **One-time**: ~$37.50 for 1 GB of documents (indexed at $0.15/1M tokens)
- **Query cost**: ~$3-5/month for 1,000 queries/month

### Response Times

- **First query**: 2-3 seconds (initialization)
- **Subsequent queries**: 500ms - 1s

### Storage

- **Persistent**: Documents stored indefinitely (FREE)
- **Max store size**: Recommended < 20 GB for optimal performance
- **Total Year 1 Cost**: ~$4,000 setup + ~$37 queries = $4,037

**Pricing Verification**: All costs verified against official Google Gemini API documentation. See `log/pricing_verification_official_sources.md` for details.

## 🔐 Security & Compliance

### Data Protection

✅ HTTPS encryption for all API calls  
✅ API key managed via environment variables  
✅ No keys in source code or git history  
✅ Audit trail for all policy access  

### Compliance

✅ Citation tracking for accountability  
✅ Audit trail with timestamp and user  
✅ Metadata tags for data classification  
✅ Role-based store organization  

## 📝 Documentation

- **[Architecture Guide](docs/architecture.md)** - Detailed system design
- **[ROI Calculator](docs/roi_calculator.md)** - Business case analysis
- **[Deployment Guide](docs/deployment_guide.md)** - Production deployment

## 🤝 Contributing

Issues and contributions welcome!

- Fork the repository
- Create a feature branch
- Submit a pull request

## 📄 License

Licensed under Apache License 2.0 - see LICENSE file

## 🎓 Learning Resources

- **[Tutorial 37 Documentation](https://github.com/raphaelmansuy/adk_training/tree/main/docs/docs/37_file_search_policy_navigator.md)** - Complete tutorial with WHY→WHAT→HOW structure
- [Google ADK Documentation](https://github.com/google/adk-python)
- [Gemini File Search API](https://ai.google.dev/gemini-api/docs/file-search)
- [Tutorial Series](https://github.com/raphaelmansuy/adk_training)

## 🚀 Next Steps

1. ✅ Complete quick start above
2. **Read the full tutorial**: [Tutorial 37 Documentation](https://github.com/raphaelmansuy/adk_training/tree/main/docs/docs/37_file_search_policy_navigator.md)
3. Run demos to see all features
4. Adapt sample policies to your organization
5. Deploy to production (see deployment guide)
6. Integrate with Slack/Teams (see tutorial 33)
7. Monitor usage and iterate

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Training**: ADK Training Project Documentation

---

**Created**: November 8, 2025  
**Last Updated**: November 8, 2025  
**Status**: Production Ready ✅

Tutorial 37 is part of the **Google ADK Training Project**:  
https://github.com/raphaelmansuy/adk_training
