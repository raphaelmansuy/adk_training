# Deep Research Agent Example

This example demonstrates how to use Google's Deep Research Agent via the Interactions API for autonomous, multi-step research tasks.

## Features

- Background execution for long-running research
- Streaming with progress updates (thought summaries)
- Custom formatting and steerability
- Follow-up conversations after research
- Error handling and retry patterns

## Prerequisites

```bash
# Install dependencies
make setup

# Set your API key
export GOOGLE_API_KEY="your-api-key-here"
```

## Quick Start

```bash
# Run tests to validate setup
make test

# Run research demo
make demo

# See all available commands
make help
```

## Key Concepts

### Background Execution

Deep Research requires `background=True` because research tasks can take several minutes:

```python
from google import genai

client = genai.Client()

# Start research (returns immediately)
interaction = client.interactions.create(
    input="Research the future of quantum computing.",
    agent="deep-research-pro-preview-12-2025",
    background=True
)

# Poll for completion
while interaction.status != "completed":
    interaction = client.interactions.get(interaction.id)
    time.sleep(10)

print(interaction.outputs[-1].text)
```

### Streaming with Thoughts

Get real-time progress updates:

```python
stream = client.interactions.create(
    input="Research AI trends in 2025.",
    agent="deep-research-pro-preview-12-2025",
    background=True,
    stream=True,
    agent_config={
        "type": "deep-research",
        "thinking_summaries": "auto"
    }
)

for chunk in stream:
    if chunk.event_type == "content.delta":
        if chunk.delta.type == "thought_summary":
            print(f"💭 {chunk.delta.content.text}")
        elif chunk.delta.type == "text":
            print(chunk.delta.text, end="")
```

### Custom Formatting

Steer output format with your prompt:

```python
prompt = """
Research electric vehicle adoption rates.

Format the output as:
1. Executive Summary (3 sentences)
2. Key Statistics (table format)
3. Regional Breakdown
4. Future Outlook
"""

interaction = client.interactions.create(
    input=prompt,
    agent="deep-research-pro-preview-12-2025",
    background=True
)
```

## Cost Analysis 💰

The Gemini Deep Research Agent uses the **Gemini 3 Pro Preview** model, which is charged based on token consumption and tool usage.

### Model Pricing (Batch Mode)

| Component | Cost | Notes |
|-----------|------|-------|
| **Input tokens** | $2.00 per 1M tokens | Text, image, video inputs |
| **Output tokens** | $12.00 per 1M tokens | Text responses and reasoning |
| **Context caching** | $0.20 per 1M tokens | For prompts ≤ 200K tokens |
| **Google Search grounding** | $35 per 1,000 queries* | After 5,000 free/month |

*Pricing starts January 5, 2026. Currently free but limited to available tier.

### Typical Research Cost Estimation

Based on a typical Deep Research query (20-minute research session):

| Metric | Value | Calculation |
|--------|-------|-------------|
| **Average input tokens per query** | ~2,000 tokens | Initial research prompt + context |
| **Average search queries** | 5-8 queries | Planning + iterative searching |
| **Estimated output tokens** | ~8,000-12,000 tokens | Comprehensive research report |
| **Total tokens for session** | ~50,000-80,000 tokens | Input + processing + output |
| **Estimated cost per research** | **$0.70-$1.20** | At standard batch rates |

### Cost Optimization Tips

1. **Use Batch Mode**: 50% cost reduction (not applicable to free tier)
2. **Be Specific**: Detailed queries reduce iterative searches
3. **Monitor Usage**: Check token counts in responses
4. **Free Tier Limits**: 
   - 5,000 search queries/month free (Grounding)
   - Generous free token allocation for testing

### Production Cost Scenarios

| Scenario | Monthly Estimate | Details |
|----------|-----------------|---------|
| **Light usage** (10 queries/month) | ~$8-12 | Development/testing |
| **Standard usage** (100 queries/month) | ~$70-120 | Regular research tasks |
| **Heavy usage** (500 queries/month) | ~$350-600 | Enterprise research pipeline |

### References

- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing) - Latest official pricing
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) - Enterprise options
- Pricing valid as of December 2025

## Troubleshooting

### Error 429: Quota Exceeded

**Symptom**: `Error code: 429 - You do not have enough quota to make this request`

**Causes**:
- Free tier rate limiting (typically 100-200 requests/day)
- Exceeded monthly quota allocation
- Too many concurrent requests

**Solutions**:

#### 1. **Wait for Quota Reset** (Immediate)
```bash
# Free tier quota resets every 24 hours
# Try again tomorrow
make demo  # Use mock mode instead (no quota needed)
```

#### 2. **Switch to Free Mock Mode** (Immediate)
```bash
make demo  # Demonstrates Deep Research without API calls
```

#### 3. **Upgrade to Paid Tier** (Recommended for Testing)

**Steps**:
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Get API Key" → "Create API Key in new Google Cloud project"
3. Enable billing in Google Cloud Console
4. Set environment variable:
   ```bash
   export GOOGLE_API_KEY="your-new-paid-api-key"
   ```
5. Retry: `make research`

**Benefits**:
- Higher rate limits (1000s of requests/day)
- Pay only for what you use
- Better quota management

#### 3b. **Use Vertex AI** (For GCP Users with Existing Projects)

If you already have a Google Cloud project with Vertex AI enabled:

**Steps**:
1. Authenticate with your GCP project:
   ```bash
   gcloud auth login
   gcloud config set project YOUR-PROJECT-ID
   ```

2. Set Vertex AI endpoint:
   ```bash
   export VERTEX_AI_PROJECT_ID="your-project-id"
   export VERTEX_AI_REGION="us-central1"  # or your preferred region
   ```

3. Update environment variables in `research_agent/.env`:
   ```bash
   # Use Vertex AI instead of free tier
   USE_VERTEX_AI=true
   GOOGLE_CLOUD_PROJECT=your-project-id
   ```

4. Modify `agent.py` to use Vertex AI client:
   ```python
   if os.getenv("USE_VERTEX_AI") == "true":
       from vertexai.generative_models import GenerativeModel
       client = GenerativeModel("gemini-2.0-flash-001", 
                              location=os.getenv("VERTEX_AI_REGION", "us-central1"))
   ```

5. Retry: `make research`

**Benefits**:
- Use existing GCP project quota
- Enterprise-grade quotas (typically higher)
- Audit trail in Cloud Logging
- Integration with other GCP services
- Potential volume discounts

**Pricing**:
- Same as Google AI Studio ($2.00 input, $12.00 output per 1M tokens)
- Billed to your GCP project
- Free tier quota may apply based on project setup

#### 4. **Request Higher Quota** (For Production)

If you have an existing Google Cloud project:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate: APIs & Services → Quotas
4. Find "Generative AI API"
5. Select "Daily quota" and request increase
6. Google reviews and approves (typically 1-3 days)

#### 5. **Contact Google Cloud Sales** (For Enterprise)

For large-scale production deployments:
- [Google Cloud Contact Page](https://cloud.google.com/contact)
- Discuss: dedicated quota, SLAs, support
- Get: Volume discounts, custom rate limits

### Other Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| `ImportError: cannot import name 'ResearchStatus'` | Missing dependency | Run: `make setup` |
| `GOOGLE_API_KEY not set` | Missing environment variable | Set key: `export GOOGLE_API_KEY='...'` |
| Research takes >60 minutes | Complex query too large | Simplify query, break into smaller parts |
| `connection timeout` | Network issue | Check internet, retry with `--max-wait 300` |

## Use Cases

| Use Case | Example Query |
|----------|--------------|
| Market Research | "Analyze the competitive landscape of AI code assistants" |
| Due Diligence | "Research company X's financial performance and market position" |
| Literature Review | "Survey recent advances in transformer architectures" |
| Competitive Analysis | "Compare pricing and features of cloud providers" |

## Project Structure

```
deep_research_agent/
├── Makefile                    # Build and run commands
├── README.md                   # This file
├── pyproject.toml             # Project configuration
├── requirements.txt           # Dependencies
├── research_agent/            # Main agent module
│   ├── __init__.py
│   ├── agent.py               # Deep Research implementation
│   ├── streaming.py           # Streaming utilities
│   └── .env.example           # Environment template
└── tests/                     # Test suite
    └── test_research.py       # Research agent tests
```

## Limitations

- Maximum research time: 60 minutes (most complete in ~20 minutes)
- No custom function calling tools
- Audio inputs not supported
- Structured output not yet supported

## Learn More

- [Deep Research Documentation](https://ai.google.dev/gemini-api/docs/deep-research)
- [Blog Post: Mastering Interactions API](/blog/interactions-api-deep-research)
- [Google AI Studio](https://aistudio.google.com/apikey)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Vertex AI Generative Models](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs)
