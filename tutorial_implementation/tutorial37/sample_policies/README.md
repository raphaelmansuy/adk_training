# Sample Policy Documents

This directory contains sample policy documents for use in the Tutorial 37:
Enterprise Compliance & Policy Navigator.

## Overview

These documents serve as examples for the File Search integration tutorial and
demonstrate how company policies can be uploaded, indexed, and searched using
Google's Gemini File Search API.

---

## Documents Included

### 1. code_of_conduct.md

**Source**: Contributor Covenant 2.0  
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Link**: https://www.contributor-covenant.org/

**Description**: A professional code of conduct document adapted from the widely-adopted
Contributor Covenant. This policy establishes community standards, prohibited conduct,
and enforcement procedures for workplace conduct.

**Use Case**: Demonstrates how File Search can find and enforce code of conduct
standards within an organization.

**Key Sections**:
- Community commitment and standards
- Examples of acceptable and unacceptable behavior
- Enforcement responsibilities and guidelines
- Scope and attribution

---

### 2. hr_handbook.md

**Source**: Original template based on best practices  
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Description**: A comprehensive HR employee handbook covering employment policies,
benefits, compensation, and workplace conduct.

**Use Case**: Demonstrates how File Search can help employees find answers to HR
questions quickly (vacation days, benefits, onboarding, etc.).

**Key Sections**:
- At-will employment
- Equal opportunity employment
- Work hours and remote work
- Compensation and payroll
- Benefits (health insurance, 401k, life insurance, disability)
- Paid time off (vacation, personal days, sick leave)
- Holidays
- Workplace conduct and dress code
- Anti-harassment policy
- Communication guidelines

**Tutorial Application**:
- Query: "How many vacation days do I get?"
- Query: "What benefits are available to me?"
- Query: "What is the remote work policy?"

---

### 3. it_security_policy.md

**Source**: SANS Institute Security Policy Templates (adapted)  
**License**: Public use with attribution  
**Original**: https://www.sans.org/information-security-policy/

**Description**: An IT security policy covering information classification, access
control, data protection, endpoint security, and incident response procedures.

**Use Case**: Demonstrates how File Search can help employees understand security
requirements and IT compliance procedures.

**Key Sections**:
- Information classification
- Access control and authentication
- Password policies
- Data protection and encryption
- Backup and recovery
- Endpoint security
- Network and wireless security
- Software and patch management
- Vulnerability management
- Third-party and vendor management
- Incident response procedures
- Acceptable use policies
- Security awareness training
- Remote work security

**Tutorial Application**:
- Query: "What are the password requirements?"
- Query: "How do I report a security incident?"
- Query: "What should I do with a found USB drive?"
- Query: "Can I use my personal phone for work?"

---

### 4. remote_work_policy.md

**Source**: Original template based on best practices  
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Description**: A comprehensive remote work policy covering eligibility, approval
process, security requirements, and performance expectations.

**Use Case**: Demonstrates how File Search can answer employee questions about remote
work arrangements and compliance requirements.

**Key Sections**:
- Remote work eligibility and types
- Request and approval process
- Core hours and availability
- Workspace and equipment requirements
- Security and confidentiality
- Communication and collaboration
- Performance management
- Office access
- Travel and relocation guidelines
- Time off policies
- Equipment return procedures
- Frequently asked questions

**Tutorial Application**:
- Query: "Am I eligible to work remotely?"
- Query: "What are the core hours for remote workers?"
- Query: "Do I need to use a VPN when working from home?"
- Query: "Can I travel and work remotely from another country?"

---

## Using These Documents with Tutorial 37

### Step 1: Upload Documents to File Search Store

```python
from google import genai

client = genai.Client(api_key='your-api-key')

# Create store
hr_store = client.file_search_stores.create(
    config={'display_name': 'hr-policies'}
)

# Upload sample policies
policies = [
    'code_of_conduct.md',
    'hr_handbook.md',
    'it_security_policy.md',
    'remote_work_policy.md'
]

for policy in policies:
    with open(f'sample_policies/{policy}', 'rb') as f:
        operation = client.file_search_stores.upload_to_file_search_store(
            file=f,
            file_search_store_name=hr_store.name,
            config={'display_name': policy}
        )
```

### Step 2: Test Queries

Once uploaded, test these queries:

**HR-Related**:
- "How many vacation days do I get?"
- "What benefits are included in my employment?"
- "When are holidays observed?"
- "What is the dress code?"

**Remote Work**:
- "Can I work from home?"
- "What are the core hours?"
- "Do I need VPN for remote work?"
- "How do I request a remote work arrangement?"

**Security**:
- "What are the password requirements?"
- "How do I report a security incident?"
- "What should I encrypt?"
- "Can I use public WiFi for work?"

**Code of Conduct**:
- "What is harassment?"
- "How do I report misconduct?"
- "What is the enforcement process?"

---

## Metadata for File Search Organization

When uploading these documents, consider using the following metadata:

```python
# Metadata example
metadata = {
    'department': 'string',        # HR, IT, All
    'policy_type': 'string',       # handbook, procedure, code_of_conduct
    'effective_date': 'date',      # YYYY-MM-DD
    'jurisdiction': 'string',      # US
    'sensitivity': 'string',       # internal, confidential
    'version': 'numeric',          # 1, 2, 3
    'owner': 'string',             # dept@company.com
    'review_cycle': 'numeric'      # Months between reviews
}

# Example for HR Handbook
hr_metadata = [
    {'key': 'department', 'string_value': 'HR'},
    {'key': 'policy_type', 'string_value': 'handbook'},
    {'key': 'effective_date', 'string_value': '2025-11-08'},
    {'key': 'jurisdiction', 'string_value': 'US'},
    {'key': 'sensitivity', 'string_value': 'internal'},
    {'key': 'version', 'numeric_value': 1},
    {'key': 'owner', 'string_value': 'hr@company.com'},
    {'key': 'review_cycle', 'numeric_value': 12}
]
```

---

## Customizing for Your Organization

These documents are provided as templates and examples. To adapt them for your organization:

1. **Replace company name**: Update all instances of "our company" with your actual company name
2. **Update contact information**: Replace placeholder emails and phone numbers
3. **Customize policies**: Modify terms to match your actual policies
4. **Add company-specific sections**: Include department procedures, codes, or requirements
5. **Update effective dates**: Set appropriate effective dates for your deployment
6. **Add your logo**: Include company branding if desired
7. **Legal review**: Have legal counsel review before deployment

---

## Licensing and Attribution

### Creative Commons Attribution 4.0 (CC BY 4.0)

Files licensed under CC BY 4.0 can be:
- Used commercially
- Modified and adapted
- Distributed to others
- Used for any purpose

**Requirements**:
- Give appropriate attribution to the original creator
- Include a copy of the license
- Indicate if changes were made

### Attribution Examples

For HR Handbook:
```
Original template based on best practices.
Licensed under Creative Commons Attribution 4.0 International.
https://creativecommons.org/licenses/by/4.0/
```

For Code of Conduct:
```
Adapted from Contributor Covenant 2.0
https://www.contributor-covenant.org/
Licensed under Creative Commons Attribution 4.0 International.
```

For IT Security Policy:
```
Based on SANS Institute Security Policy Templates
https://www.sans.org/information-security-policy/
Adapted for tutorial purposes.
```

---

## Resources and References

### Contributor Covenant
- **Website**: https://www.contributor-covenant.org/
- **GitHub**: https://github.com/ethicalsource/contributor_covenant
- **License**: Creative Commons Attribution 4.0

### SANS Institute Security Policies
- **Website**: https://www.sans.org/information-security-policy/
- **Description**: Free security policy templates
- **Templates**: 36+ ready-to-use security policies

### Creative Commons Licenses
- **Website**: https://creativecommons.org/
- **CC BY 4.0**: https://creativecommons.org/licenses/by/4.0/

### Best Practices References
- Employee handbooks: SHRM, NFIB, SBA resources
- Remote work: GitLab, Automattic, Basecamp public resources
- Security: NIST, CIS, ISO 27001

---

## Legal Disclaimer

These sample documents are provided for educational and tutorial purposes only.
They are NOT legal advice and should NOT be used as-is in a production environment.

**Before deploying any policy in your organization**:

1. ✅ Have legal counsel review all policies
2. ✅ Ensure compliance with applicable laws and regulations
3. ✅ Customize to reflect your actual organizational practices
4. ✅ Consider state and local employment law requirements
5. ✅ Obtain management and board approval
6. ✅ Communicate changes clearly to all employees
7. ✅ Maintain documentation of all policy updates

The creators and providers of these documents are not responsible for any legal,
financial, or business consequences resulting from their use.

---

## Tutorial Progress

These sample documents are used throughout Tutorial 37:

- **Part 2**: Upload documents to File Search Store
- **Part 3**: Search and extract citations from policies
- **Part 4**: Multi-agent system demonstrates cross-document queries
- **Part 5**: Advanced features show policy comparison and conflict detection
- **Part 6**: Production deployment with real policy documents

---

## File Sizes and Details

| Document | Size | Sections | Words | Format |
|----------|------|----------|-------|--------|
| code_of_conduct.md | 5.1 KB | 7 | ~1,200 | Markdown |
| hr_handbook.md | 8.3 KB | 10 | ~1,800 | Markdown |
| it_security_policy.md | 9.5 KB | 13 | ~2,200 | Markdown |
| remote_work_policy.md | 13 KB | 15 | ~3,100 | Markdown |
| **TOTAL** | **36 KB** | **45** | **~8,300** | **Markdown** |

---

## Conversion to PDF

To convert these markdown documents to PDF for use in production:

```bash
# Using pandoc (install first: brew install pandoc)
pandoc code_of_conduct.md -o code_of_conduct.pdf
pandoc hr_handbook.md -o hr_handbook.pdf
pandoc it_security_policy.md -o it_security_policy.pdf
pandoc remote_work_policy.md -o remote_work_policy.pdf
```

Then upload the PDF files to File Search for production use.

---

## Questions or Contributions

For questions about these sample documents or contributions to the tutorial:

- GitHub Issues: https://github.com/raphaelmansuy/adk_training/issues
- Tutorial Repo: https://github.com/raphaelmansuy/adk_training
- Main Project: Google ADK Training

---

**Created**: November 8, 2025  
**Last Updated**: November 8, 2025  
**Status**: Ready for Tutorial 37 Implementation

Sample documents are part of the **Google ADK Training Project**:  
https://github.com/raphaelmansuy/adk_training
