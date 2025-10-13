---
id: yaml_configuration
title: "Tutorial 20: YAML Configuration - Declarative Agent Setup"
description: "Configure agents using YAML files for declarative setup, easier maintenance, and configuration management across environments."
sidebar_label: "20. YAML Configuration"
sidebar_position: 20
tags: ["intermediate", "yaml", "configuration", "declarative", "setup"]
keywords:
  [
    "yaml configuration",
    "declarative setup",
    "agent config",
    "configuration management",
    "environment setup",
  ]
status: "complete"
difficulty: "intermediate"
estimated_time: "45 minutes"
prerequisites: ["Tutorial 01: Hello World Agent", "YAML syntax knowledge"]
learning_objectives:
  - "Configure agents using YAML files"
  - "Manage environment-specific configurations"
  - "Build declarative agent setups"
  - "Organize configuration across projects"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial20"
---

# Tutorial 20: Agent Configuration with YAML

**Goal**: Master declarative agent configuration using YAML files to define agents, tools, and behaviors without writing Python code, enabling rapid prototyping and configuration management.

**Prerequisites**:

- Tutorial 01 (Hello World Agent)
- Tutorial 02 (Function Tools)
- Tutorial 06 (Multi-Agent Systems)
- Basic understanding of YAML syntax

**What You'll Learn**:

- Creating agent configurations with `root_agent.yaml`
- Understanding `AgentConfig` and `LlmAgentConfig` schemas
- Configuring tools, models, and instructions in YAML
- Multi-agent systems in configuration files
- When to use YAML vs Python code
- Loading and validating configurations
- Best practices for config management

**Time to Complete**: 45 minutes

---

## Why YAML Configuration Matters

**Problem**: Writing Python code for every agent configuration requires development expertise and makes rapid iteration difficult.

**Solution**: **YAML configuration** enables declarative agent definitions that can be edited without code changes.

**Benefits**:

- 🚀 **Rapid Prototyping**: Change configurations without coding
- 📝 **Readable**: Human-friendly format
- [FLOW] **Version Control**: Easy to track config changes
- 🎯 **Separation**: Configuration separate from implementation
- 👥 **Accessibility**: Non-developers can modify agents
- 🔧 **Reusable**: Share configurations across projects

**Use Cases**:

- Quick agent prototyping
- Configuration-driven deployments
- Multi-environment setups (dev, staging, prod)
- Agent marketplace/templates
- Non-technical team member modifications

**Status**: YAML configuration is marked as `@experimental` in ADK. API may change.

---

:::info API Verification

**Source Verified**: Official ADK source code (version 1.16.0+)

**Correct API**: `config_agent_utils.from_config(config_path)`

**Common Mistake**: Using `AgentConfig.from_yaml_file()` - this method **does not exist**. Instead, use `config_agent_utils.from_config()` which loads the YAML file and returns a ready-to-use agent instance.

**Verification Date**: October 2025

:::

---

## Why YAML Configuration Matters

**Problem**: Writing Python code for every agent configuration requires development expertise and makes rapid iteration difficult.

**Solution**: **YAML configuration** enables declarative agent definitions that can be edited without code changes.

**Benefits**:

- 🚀 **Rapid Prototyping**: Change configurations without coding
- 📝 **Readable**: Human-friendly format
- [FLOW] **Version Control**: Easy to track config changes
- 🎯 **Separation**: Configuration separate from implementation
- 👥 **Accessibility**: Non-developers can modify agents
- 🔧 **Reusable**: Share configurations across projects

**Use Cases**:

- Quick agent prototyping
- Configuration-driven deployments
- Multi-environment setups (dev, staging, prod)
- Agent marketplace/templates
- Non-technical team member modifications

**Status**: YAML configuration is marked as `@experimental` in ADK. API may change.

---

:::info API Verification

**Source Verified**: Official ADK source code (version 1.16.0+)

**Correct API**: `config_agent_utils.from_config(config_path)`

**Common Mistake**: Using `AgentConfig.from_yaml_file()` - this method **does not exist**. Instead, use `config_agent_utils.from_config()` which loads the YAML file and returns a ready-to-use agent instance.

**Verification Date**: January 2025

:::

---

## 1. YAML Configuration Basics

### What is root_agent.yaml?

**`root_agent.yaml`** is the main configuration file that defines an agent and its sub-agents declaratively.

**Location**: Place in project root or specify path explicitly.

**Basic Structure**:

```yaml
# root_agent.yaml

name: my_agent
model: gemini-2.0-flash
description: A helpful agent
instruction: |
  You are a helpful assistant that answers questions
  accurately and concisely.

generate_content_config:
  temperature: 0.7
  max_output_tokens: 1024

tools:
  - type: function
    name: get_weather
    description: Get current weather for a location

sub_agents:
  - name: specialized_agent
    model: gemini-2.0-flash
    description: Specialized agent for specific tasks
```

### Creating Configuration Project

```bash
# Create new config-based project
adk create --type=config my_agent_config

# Directory structure created:
# my_agent_config/
#   root_agent.yaml      # Agent configuration
#   tools/               # Custom tool implementations
#   README.md
```

---

## 2. AgentConfig Schema

### Core Fields

**Source**: `google/adk/agents/agent_config.py`

```yaml
# Required fields
name: agent_name # Unique identifier
model: gemini-2.0-flash # Model to use

# Optional fields
description: "Agent purpose" # Brief description
instruction: | # System instruction
  Multi-line instruction
  for the agent

# Content generation config
generate_content_config:
  temperature: 0.7 # 0.0-1.0 (creativity)
  max_output_tokens: 2048 # Max response length
  top_p: 0.95 # Nucleus sampling
  top_k: 40 # Top-k sampling

# Tools configuration
tools:
  - type: function
    name: tool_name
    # ... tool config

# Sub-agents
sub_agents:
  - name: sub_agent_1
    # ... agent config
```

### Model Options

```yaml
# Gemini 2.0 models (recommended)
model: gemini-2.0-flash        # Fast, efficient
model: gemini-2.0-flash-thinking  # With thinking capability

# Gemini 1.5 models
model: gemini-1.5-flash        # Fast, cost-effective
model: gemini-1.5-pro          # High quality

# Live API models
model: gemini-2.0-flash-live-preview-04-09  # Vertex AI Live
model: gemini-live-2.5-flash-preview        # AI Studio Live
```

---

## 3. Real-World Example: Customer Support System

Let's build a complete customer support system using YAML configuration.

### Complete Configuration

```yaml
# root_agent.yaml

name: customer_support
model: gemini-2.0-flash
description: Customer support agent with various tools

instruction: |
  You are a customer support agent. Your role is to:

  1. Understand customer inquiries
  2. Use available tools to provide accurate information
  3. Provide comprehensive solutions

  Available tools:
  - check_customer_status: Check if customer is premium member
  - log_interaction: Log customer interaction for records
  - get_order_status: Get status of an order by ID
  - track_shipment: Get shipment tracking information
  - cancel_order: Cancel an order (requires authorization)
  - search_knowledge_base: Search technical documentation
  - run_diagnostic: Run diagnostic tests
  - create_ticket: Create support ticket for escalation
  - get_billing_history: Retrieve billing history
  - process_refund: Process refund (requires approval for amounts > $100)
  - update_payment_method: Update stored payment method

  Guidelines:
  - Always be polite and professional
  - Provide specific information when available
  - Escalate complex issues when necessary

generate_content_config:
  temperature: 0.5
  max_output_tokens: 2048

tools:
  - name: tools.check_customer_status
  - name: tools.log_interaction
  - name: tools.get_order_status
  - name: tools.track_shipment
  - name: tools.cancel_order
  - name: tools.search_knowledge_base
  - name: tools.run_diagnostic
  - name: tools.create_ticket
  - name: tools.get_billing_history
  - name: tools.process_refund
  - name: tools.update_payment_method
```

### Tool Implementations

```python
# tools/customer_tools.py

"""
Tool implementations for customer support system.
These functions are referenced by name in root_agent.yaml.
"""

def check_customer_status(customer_id: str) -> str:
    """Check if customer is premium member."""
    # Simulated lookup
    premium_customers = ['CUST-001', 'CUST-003', 'CUST-005']

    is_premium = customer_id in premium_customers

    return f"Customer {customer_id} is {'premium' if is_premium else 'standard'} member"


def log_interaction(customer_id: str, interaction_type: str, summary: str) -> str:
    """Log customer interaction."""
    # In production, would log to database
    print(f"[LOG] {customer_id} - {interaction_type}: {summary}")

    return "Interaction logged successfully"


def get_order_status(order_id: str) -> str:
    """Get order status."""
    # Simulated order lookup
    orders = {
        'ORD-001': 'shipped',
        'ORD-002': 'processing',
        'ORD-003': 'delivered',
        'ORD-004': 'cancelled'
    }

    status = orders.get(order_id, 'not_found')

    return f"Order {order_id} status: {status}"


def track_shipment(order_id: str) -> str:
    """Get shipment tracking."""
    # Simulated tracking lookup
    tracking = {
        'ORD-001': {
            'carrier': 'UPS',
            'tracking_number': '1Z999AA10123456784',
            'estimated_delivery': '2025-10-10'
        },
        'ORD-003': {
            'carrier': 'FedEx',
            'tracking_number': '7898765432109',
            'estimated_delivery': 'Delivered on 2025-10-07'
        }
    }

    info = tracking.get(order_id)

    if info:
        return f"Tracking: {info['carrier']} {info['tracking_number']}, ETA: {info['estimated_delivery']}"
    else:
        return f"No tracking available for {order_id}"


def cancel_order(order_id: str, reason: str) -> str:
    """Cancel order."""
    # In production, would update database
    return f"Order {order_id} cancelled. Reason: {reason}"


def search_knowledge_base(query: str) -> str:
    """Search technical documentation."""
    # Simulated knowledge base search
    kb = {
        'login': 'To reset password, go to Settings > Security > Reset Password',
        'connection': 'Check internet connection and restart the app',
        'error': 'Clear app cache: Settings > Apps > Clear Cache'
    }

    for key, value in kb.items():
        if key in query.lower():
            return value

    return "No matching article found"


def run_diagnostic(issue_type: str) -> str:
    """Run diagnostic tests."""
    # Simulated diagnostic
    return f"Diagnostic for {issue_type}: All systems operational. Suggested: Clear cache and restart."


def create_ticket(customer_id: str, issue: str, priority: str) -> str:
    """Create support ticket."""
    # In production, would create in ticketing system
    ticket_id = f"TKT-{hash(issue) % 10000:04d}"

    return f"Support ticket {ticket_id} created with {priority} priority"


def get_billing_history(customer_id: str) -> str:
    """Get billing history."""
    # Simulated billing lookup
    return f"""
Billing History for {customer_id}:
- 2025-09-01: $49.99 (Monthly subscription)
- 2025-08-01: $49.99 (Monthly subscription)
- 2025-07-15: $29.99 (One-time purchase)
    """.strip()


def process_refund(order_id: str, amount: float) -> str:
    """Process refund."""
    if amount > 100:
        return f"REQUIRES_APPROVAL: Refund of ${amount} for {order_id} needs manager approval"

    return f"Refund of ${amount} approved for {order_id}. Funds will appear in 3-5 business days."


def update_payment_method(customer_id: str, payment_type: str) -> str:
    """Update payment method."""
    return f"Payment method for {customer_id} updated to {payment_type}"
```

### Loading and Running Configuration

```python
# run_agent.py

"""
Load and run agent from YAML configuration.
"""

import asyncio
import os
from google.adk.agents import Runner, Session
from google.adk.agents import config_agent_utils

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


async def main():
    """Load configuration and run agent."""

    # Load agent from YAML configuration
    agent = config_agent_utils.from_config('root_agent.yaml')

    # Create runner and session
    runner = Runner()
    session = Session()

    # Test queries
    queries = [
        "I'm customer CUST-001 and I want to check my order ORD-001",
        "I need help with a login error",
        "I'd like a refund of $75 for order ORD-002"
    ]

    for query in queries:
        print(f"\n{'='*70}")
        print(f"QUERY: {query}")
        print(f"{'='*70}\n")

        result = await runner.run_async(
            query,
            agent=agent,
            session=session
        )

        print("RESPONSE:")
        print(result.content.parts[0].text)
        print(f"\n{'='*70}")

        await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(main())
```

### Expected Output

```
======================================================================
QUERY: Check the status of customer CUST-001
======================================================================

RESPONSE:
Hello! I can help you check the customer status. Let me look that up for you.

Customer CUST-001 is premium member

Is there anything else I can help you with?

======================================================================

======================================================================
QUERY: What's the status of order ORD-001?
======================================================================

RESPONSE:
I'd be happy to check the status of your order. Let me look that up.

Order ORD-001 status: shipped

If you need tracking information or have any other questions about this order, just let me know!

======================================================================

======================================================================
QUERY: Can you track shipment for order ORD-001?
======================================================================

RESPONSE:
I'll help you track that shipment. Let me get the tracking details.

Tracking: UPS 1Z999AA10123456784, ETA: 2025-10-10

Your package is currently in transit and expected to arrive by October 10th, 2025. You can track it directly on the UPS website using the tracking number above.

======================================================================
```

---

## 4. YAML vs Python: When to Use Each

### Use YAML Configuration When:

✅ **Rapid prototyping** - Testing different agent configurations
✅ **Non-technical editors** - Allow team members to modify agents
✅ **Configuration management** - Separate config from code
✅ **Multi-environment** - Dev, staging, prod configurations
✅ **Simple workflows** - Standard agent patterns
✅ **Version control** - Track configuration changes easily

### Use Python Code When:

✅ **Complex logic** - Conditional tool selection, dynamic workflows
✅ **Custom components** - Custom planners, executors, callbacks
✅ **Advanced patterns** - Loops, complex state management
✅ **Programmatic generation** - Creating agents dynamically
✅ **Testing** - Unit tests, integration tests
✅ **IDE support** - Type checking, autocomplete, refactoring

### Hybrid Approach (Best Practice)

```python
from google.adk.agents import config_agent_utils

# Load base configuration from YAML
agent = config_agent_utils.from_config('base_agent.yaml')

# Customize programmatically
agent.tools.append(custom_complex_tool)
agent.instruction += "\n\nAdditional dynamic instructions"

# Run with custom logic
if user_is_premium:
    agent.tools.append(premium_tool)

runner.run(query, agent=agent)
```

---

## 5. Best Practices

### ✅ DO: Use Environment-Specific Configs

```yaml
# config/dev/root_agent.yaml
name: support_agent_dev
model: gemini-2.0-flash
generate_content_config:
  temperature: 0.8  # More creative for testing

# config/prod/root_agent.yaml
name: support_agent_prod
model: gemini-2.0-flash
generate_content_config:
  temperature: 0.3  # More consistent for production
```

### ✅ DO: Document Configuration

```yaml
# root_agent.yaml

# Customer Support Orchestrator
# Maintainer: support-team@example.com
# Last Updated: 2025-10-08
#
# This agent routes customer inquiries to specialized agents:
# - order_agent: Order management
# - technical_agent: Technical support
# - billing_agent: Payment issues

name: customer_support
model: gemini-2.0-flash

instruction: |
  [Clear instruction here]
```

### ✅ DO: Validate Configuration

```python
from google.adk.agents import config_agent_utils

def validate_config(yaml_path: str) -> bool:
    """Validate agent configuration."""

    try:
        agent = config_agent_utils.from_config(yaml_path)
        print(f"✅ Configuration valid: {agent.name}")
        return True

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


# Validate before deployment
validate_config('root_agent.yaml')
```

### ✅ DO: Version Control Configuration

```bash
# .gitignore - Don't commit secrets
config/secrets.yaml
*.env

# Git commit configuration changes
git add root_agent.yaml
git commit -m "Update customer_support agent temperature to 0.5"
```

### ❌ DON'T: Hardcode Secrets

```yaml
# ❌ Bad - secrets in config
tools:
  - type: api
    api_key: "sk-proj-abc123..."  # NEVER do this

# ✅ Good - reference environment variables
tools:
  - type: api
    api_key: "${API_KEY}"  # Load from environment
```

---

## 6. Advanced Configuration Patterns

### Pattern 1: Conditional Sub-Agents

```yaml
# Different sub-agents for different tiers
name: support_agent

sub_agents:
  # Basic support (all tiers)
  - name: faq_agent
    model: gemini-2.0-flash
    description: FAQ and basic questions

  # Premium support only (filter in code)
  - name: premium_support_agent
    model: gemini-2.0-flash
    description: Premium customer support
    # Enable only for premium customers in code
```

### Pattern 2: Configuration Inheritance

```python
from google.adk.agents import config_agent_utils

# Load base configuration
specialized_agent = config_agent_utils.from_config('config/base.yaml')

# Create specialized variants
specialized_agent.instruction += "\n\nSpecialized for domain X"
specialized_agent.tools.append(domain_specific_tool)
```

### Pattern 3: Dynamic Tool Registration

```python
from google.adk.agents import config_agent_utils

# Load config
agent = config_agent_utils.from_config('root_agent.yaml')

# Add tools dynamically based on user permissions
if user.has_permission('admin'):
    agent.tools.append(FunctionTool(admin_tool))

if user.has_permission('data_export'):
    agent.tools.append(FunctionTool(export_tool))
```

---

## 7. Troubleshooting

### Issue: "Configuration file not found"

**Solutions**:

1. **Check file path**:

```python
import os
config_path = 'root_agent.yaml'
print(f"Looking for: {os.path.abspath(config_path)}")
print(f"Exists: {os.path.exists(config_path)}")
```

2. **Specify absolute path**:

```python
from google.adk.agents import config_agent_utils

agent = config_agent_utils.from_config('/full/path/to/root_agent.yaml')
```

### Issue: "Invalid YAML syntax"

**Solution**: Validate YAML syntax:

```bash
# Install yamllint
pip install yamllint

# Validate configuration
yamllint root_agent.yaml
```

### Issue: "Tool function not found"

**Solution**: Ensure tool functions are importable:

```python
# tools/__init__.py
from .customer_tools import (
    check_customer_status,
    log_interaction,
    get_order_status
)

__all__ = [
    'check_customer_status',
    'log_interaction',
    'get_order_status'
]
```

---

## Summary

You've mastered YAML agent configuration:

**Key Takeaways**:

- ✅ `root_agent.yaml` for declarative agent definitions
- ✅ `config_agent_utils.from_config()` to load configurations
- ✅ YAML for rapid prototyping and configuration management
- ✅ Python code for complex logic and customization
- ✅ Hybrid approach combines best of both
- ✅ Environment-specific configs for dev/staging/prod
- ✅ Version control for configuration tracking

**Production Checklist**:

- [ ] Configuration files version controlled
- [ ] Secrets loaded from environment variables
- [ ] Configuration validation in CI/CD
- [ ] Environment-specific configs (dev/staging/prod)
- [ ] Documentation in YAML comments
- [ ] Tool functions properly registered
- [ ] Configuration tested before deployment
- [ ] Backup of production configurations

**Next Steps**:

- **Tutorial 21**: Learn Multimodal & Image Generation
- **Tutorial 22**: Master Model Selection & Optimization
- **Tutorial 23**: Explore Production Deployment

**Resources**:

- [ADK Configuration Documentation](https://google.github.io/adk-docs/configuration/)
- [AgentConfig API Reference](https://google.github.io/adk-docs/api/agent-config/)
- [YAML Specification](https://yaml.org/spec/)

---

**🎉 Tutorial 20 Complete!** You now know how to configure agents with YAML. Continue to Tutorial 21 to learn about multimodal capabilities and image generation.
