# Google ADK JSON Extraction Implementation Guide

## Overview

This document explains how agents extract JSON according to Google ADK patterns, using Tutorial 34 as a practical example.

## Key Concepts

### 1. Output Schema Parameter

The primary mechanism for enforcing JSON output in ADK is the `output_schema` parameter on `LlmAgent`:

```python
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent

class MyOutput(BaseModel):
    """Structured output model."""
    name: str = Field(description="Name field")
    value: int = Field(description="Value field")

agent = LlmAgent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="Return your answer as structured JSON",
    output_schema=MyOutput,  # ← Enforces JSON structure
)
```

### 2. The set_model_response Tool

When both `output_schema` and `tools` are specified, ADK automatically adds a special tool:

- **Tool Name**: `set_model_response`
- **Purpose**: Allows the model to return the final structured output
- **Usage**: Model calls this tool with the JSON data matching the schema

### 3. How It Works

```
User Input
    ↓
Model processes input
    ↓
Model can use other tools (if provided) to gather info
    ↓
Model calls set_model_response with structured JSON
    ↓
ADK validates JSON against schema
    ↓
Returns validated structured output
```

## Implementation in Tutorial 34

### Sub-Agent Configuration

Each specialized agent enforces JSON output for its domain:

**Financial Agent**
```python
financial_agent = LlmAgent(
    name="financial_analyzer",
    model="gemini-2.5-flash",
    instruction="Return your analysis using the set_model_response tool...",
    output_schema=FinancialAnalysisOutput,  # Enforce JSON
)
```

**Technical Agent**
```python
technical_agent = LlmAgent(
    name="technical_analyzer",
    model="gemini-2.5-flash",
    instruction="Return your analysis using the set_model_response tool...",
    output_schema=TechnicalAnalysisOutput,  # Enforce JSON
)
```

(Same pattern for sales_agent and marketing_agent)

### Pydantic Schema Definition

```python
from pydantic import BaseModel, ConfigDict

class FinancialAnalysisOutput(BaseModel):
    """Structured output for financial document analysis."""
    
    model_config = ConfigDict(extra='forbid')  # Strict validation
    
    summary: DocumentSummary
    entities: EntityExtraction
    financial_metrics: FinancialMetrics
    fiscal_periods: list[str]
    recommendations: list[str]
```

**Key Features**:
- `ConfigDict(extra='forbid')`: Prevents extra fields in JSON
- Type hints: All fields have explicit types
- Descriptions: All fields have Field descriptions for LLM clarity
- Nested models: Can use other Pydantic models

## Best Practices

### 1. Clear Instructions

Tell the agent explicitly to use the structured format:

```python
instruction=(
    "Return your analysis using the set_model_response tool "
    "with the required JSON structure."
)
```

### 2. Nested Pydantic Models

Compose complex schemas from simpler models:

```python
class FinancialAnalysisOutput(BaseModel):
    summary: DocumentSummary      # Reuses DocumentSummary
    entities: EntityExtraction    # Reuses EntityExtraction
    financial_metrics: FinancialMetrics  # Reuses FinancialMetrics
    # ...
```

### 3. Optional Fields

Use `Field` with `default` for optional fields:

```python
class Deal(BaseModel):
    customer: str = Field(default="", description="Customer name")
    deal_value: str = Field(default="", description="Deal value")
    stage: str = Field(default="", description="Deal stage")
```

### 4. List Fields

Use list types with `default_factory`:

```python
class FinancialAnalysisOutput(BaseModel):
    fiscal_periods: list[str] = Field(
        default_factory=list,
        description="Fiscal periods mentioned"
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Financial recommendations"
    )
```

## Validation

All JSON output is automatically validated:

```python
# ADK validates the response matches FinancialAnalysisOutput schema
response = agent.run("Analyze this financial document...")
# response is guaranteed to be FinancialAnalysisOutput instance
```

## Testing JSON Schema Enforcement

```python
def test_agent_output_schema():
    from pubsub_agent.agent import financial_agent, FinancialAnalysisOutput
    
    # Verify schema is attached
    assert financial_agent.output_schema == FinancialAnalysisOutput
    
    # Run agent (requires API key)
    # response will be validated against schema
    # response = agent.run("Your prompt...")
```

## Real Example

### Input
```
Financial document about Q3 2024 earnings with $5.2M revenue, 
$1.3M profit, 25% growth rate
```

### Output (Validated JSON)
```json
{
  "summary": {
    "main_points": ["Q3 2024 revenue of $5.2M", "Profit of $1.3M", "25% growth"],
    "key_insight": "Strong Q3 performance with double-digit growth",
    "summary": "Q3 2024 showed strong financial performance with $5.2M revenue..."
  },
  "entities": {
    "dates": ["Q3 2024"],
    "currency_amounts": ["$5.2M", "$1.3M"],
    "percentages": ["25%"],
    "numbers": []
  },
  "financial_metrics": {
    "revenue": "$5.2M",
    "profit": "$1.3M",
    "margin": "25%",
    "growth_rate": "25%",
    "other_metrics": []
  },
  "fiscal_periods": ["Q3 2024"],
  "recommendations": ["Continue growth initiatives", "Monitor margins"]
}
```

## Common Patterns

### Pattern 1: Simple Schema
```python
class SimpleOutput(BaseModel):
    result: str = Field(description="The result")
```

### Pattern 2: Nested Schema
```python
class ComplexOutput(BaseModel):
    summary: SimpleSummary
    details: list[DetailItem]
    metadata: dict[str, str]
```

### Pattern 3: Union Types
```python
from typing import Union

class OutputA(BaseModel):
    type: str = "A"
    value_a: str

class OutputB(BaseModel):
    type: str = "B"
    value_b: int

class UnionOutput(BaseModel):
    result: Union[OutputA, OutputB]
```

## Advantages of ADK JSON Extraction

✅ **Automatic Validation**: Schema validation is built-in  
✅ **Type Safety**: Python type hints ensure correctness  
✅ **Clear API**: Pydantic models are self-documenting  
✅ **Composable**: Reuse schemas across agents  
✅ **LLM-Friendly**: Descriptions help LLM understand structure  
✅ **Error Handling**: ADK handles JSON parsing errors  

## References

- [ADK output_schema_with_tools Sample](https://github.com/google/adk-python/tree/main/contributing/samples/output_schema_with_tools)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Google ADK Documentation](https://github.com/google/adk-python)

## Summary

Google ADK makes JSON extraction simple and reliable:

1. Define output schema as Pydantic model
2. Pass to `output_schema` parameter
3. Tell agent to use `set_model_response` tool
4. ADK automatically validates JSON
5. Get typed, validated output

This pattern is used in Tutorial 34 with 4 specialized agents that each extract domain-specific JSON from documents.
