"""
Tutorial 22: Model Selection & Optimization
A framework for selecting, benchmarking, and comparing AI models.
"""

import asyncio
import time
from dataclasses import dataclass
from typing import Dict, List, Any
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ModelBenchmark:
    """Benchmark results for a model."""
    model: str
    avg_latency: float
    avg_tokens: int
    quality_score: float
    cost_estimate: float
    success_rate: float


# ============================================================================
# MODEL SELECTOR CLASS
# ============================================================================

class ModelSelector:
    """Framework for selecting and benchmarking models."""

    def __init__(self):
        """Initialize model selector."""
        self.benchmarks: Dict[str, ModelBenchmark] = {}

    async def benchmark_model(
        self,
        model: str,
        test_queries: List[str],
        instruction: str
    ) -> ModelBenchmark:
        """
        Benchmark a model on test queries.

        Args:
            model: Model to test
            test_queries: List of test queries
            instruction: Agent instruction

        Returns:
            ModelBenchmark with results
        """
        from google.genai import Client

        print(f"\n{'='*70}")
        print(f"BENCHMARKING: {model}")
        print(f"{'='*70}\n")

        # Create client for direct model calls (simpler than Runner for benchmarking)
        client = Client()

        latencies = []
        token_counts = []
        successes = 0

        for query in test_queries:
            try:
                start = time.time()

                # Direct model call for benchmarking
                response = await client.aio.models.generate_content(
                    model=model,
                    contents=f"{instruction}\n\n{query}",
                    config=types.GenerateContentConfig(
                        temperature=0.5,
                        max_output_tokens=1024
                    )
                )

                latency = time.time() - start
                latencies.append(latency)

                # Use actual token count from response metadata if available, else estimate
                text = response.text if hasattr(response, 'text') else ""
                if hasattr(response, "usage_metadata") and response.usage_metadata and "total_tokens" in response.usage_metadata:
                    token_count = response.usage_metadata["total_tokens"]
                else:
                    token_count = len(text.split())
                token_counts.append(token_count)

                successes += 1

                print(f"✅ Query: {query[:50]}...")
                print(f"   Latency: {latency:.2f}s, Tokens: ~{token_count}")

            except Exception as e:
                print(f"❌ Query failed: {query[:50]}... - {e}")

        # Calculate metrics
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0
        success_rate = successes / len(test_queries)

        # Estimate cost (simplified pricing as of 2025)
        cost_per_1k_tokens = {
            'gemini-2.5-flash': 0.00008,
            'gemini-2.5-flash-lite': 0.00004,
            'gemini-2.5-pro': 0.0005,
            'gemini-2.0-flash': 0.0001,
            'gemini-2.0-flash-live': 0.00015,
        }

        cost_estimate = (avg_tokens / 1000) * cost_per_1k_tokens.get(model, cost_per_1k_tokens['gemini-2.5-flash'])
        # Quality score (based on success rate and latency)
        quality_score = success_rate * (1.0 / (1.0 + avg_latency))

        benchmark = ModelBenchmark(
            model=model,
            avg_latency=avg_latency,
            avg_tokens=int(avg_tokens),
            quality_score=quality_score,
            cost_estimate=cost_estimate,
            success_rate=success_rate
        )

        self.benchmarks[model] = benchmark

        print("\n📊 RESULTS:")
        print(f"   Avg Latency: {avg_latency:.2f}s")
        print(f"   Avg Tokens: {avg_tokens:.0f}")
        print(f"   Success Rate: {success_rate*100:.1f}%")
        print(f"   Cost Estimate: ${cost_estimate:.6f} per query")
        print(f"   Quality Score: {quality_score:.3f}")

        return benchmark

    async def compare_models(
        self,
        models: List[str],
        test_queries: List[str],
        instruction: str
    ):
        """
        Compare multiple models on same queries.

        Args:
            models: List of models to compare
            test_queries: Test queries
            instruction: Agent instruction
        """

        print(f"\n{'#'*70}")
        print("MODEL COMPARISON")
        print(f"{'#'*70}\n")

        for model in models:
            await self.benchmark_model(model, test_queries, instruction)
            await asyncio.sleep(2)

        self._print_comparison()

    def _print_comparison(self):
        """Print comparison table."""

        print(f"\n\n{'='*70}")
        print("COMPARISON SUMMARY")
        print(f"{'='*70}\n")

        print(f"{'Model':<30} {'Latency':>10} {'Tokens':>8} {'Cost':>10} {'Quality':>10}")
        print(f"{'-'*70}")

        for model, bench in self.benchmarks.items():
            print(f"{model:<30} {bench.avg_latency:>9.2f}s {bench.avg_tokens:>8} "
                  f"${bench.cost_estimate:>9.6f} {bench.quality_score:>10.3f}")

        print(f"\n{'='*70}")

        # Recommendations
        print("\n🎯 RECOMMENDATIONS:\n")

        fastest = min(self.benchmarks.items(), key=lambda x: x[1].avg_latency)
        print(f"⚡ Fastest: {fastest[0]} ({fastest[1].avg_latency:.2f}s)")

        cheapest = min(self.benchmarks.items(), key=lambda x: x[1].cost_estimate)
        print(f"💰 Cheapest: {cheapest[0]} (${cheapest[1].cost_estimate:.6f})")

        best_quality = max(self.benchmarks.items(), key=lambda x: x[1].quality_score)
        print(f"🏆 Best Quality: {best_quality[0]} ({best_quality[1].quality_score:.3f})")


# ============================================================================
# TOOL FUNCTIONS (for use with ADK agent)
# ============================================================================

def recommend_model_for_use_case(
    use_case: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Recommend model based on use case description.

    Args:
        use_case: Use case description (e.g., "real-time voice assistant")
        tool_context: ADK tool context

    Returns:
        Dict with status, report, and recommended model
    """
    use_case_lower = use_case.lower()

    # Rule-based recommendations (Gemini 2.5 series)
    if 'real-time' in use_case_lower or 'voice' in use_case_lower:
        recommendation = 'gemini-2.0-flash-live'
        reason = 'Real-time bidirectional streaming support'

    elif 'complex' in use_case_lower or 'reasoning' in use_case_lower or 'stem' in use_case_lower:
        recommendation = 'gemini-2.5-pro'
        reason = 'Best for complex problems and advanced reasoning'

    elif 'high-volume' in use_case_lower or 'simple' in use_case_lower or 'ultra-fast' in use_case_lower:
        recommendation = 'gemini-2.5-flash-lite'
        reason = 'Fastest and cheapest for high-volume simple tasks'

    elif 'critical' in use_case_lower or 'important' in use_case_lower:
        recommendation = 'gemini-2.5-pro'
        reason = 'Highest quality for critical business operations'

    elif 'extended context' in use_case_lower or 'large document' in use_case_lower:
        recommendation = 'gemini-2.5-pro'
        reason = '2M token context window for large documents'

    else:
        recommendation = 'gemini-2.5-flash'
        reason = 'Best price-performance balance for general use'

    return {
        'status': 'success',
        'report': f'Recommended {recommendation} for use case: {use_case}',
        'model': recommendation,
        'reason': reason,
        'use_case': use_case
    }


def get_model_info(
    model_name: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Get detailed information about a specific model.

    Args:
        model_name: Name of the model
        tool_context: ADK tool context

    Returns:
        Dict with status, report, and model information
    """
    models_info = {
        'gemini-2.5-flash': {
            'context_window': '1M tokens',
            'features': ['Multimodal', 'Fast', 'Efficient'],
            'best_for': 'General purpose, recommended for most use cases',
            'pricing': 'Low',
            'speed': 'Fast'
        },
        'gemini-2.5-flash-lite': {
            'context_window': '1M tokens',
            'features': ['Ultra-fast', 'Simple tasks', 'High volume'],
            'best_for': 'High-volume simple tasks, content moderation',
            'pricing': 'Very Low',
            'speed': 'Ultra-fast'
        },
        'gemini-2.5-pro': {
            'context_window': '2M tokens',
            'features': ['Advanced reasoning', 'Complex problems', 'High quality'],
            'best_for': 'Complex reasoning, STEM, critical business operations',
            'pricing': 'High',
            'speed': 'Moderate'
        },
        'gemini-2.0-flash': {
            'context_window': '1M tokens',
            'features': ['Multimodal', 'Balanced', 'Legacy support'],
            'best_for': 'General purpose with legacy compatibility',
            'pricing': 'Low',
            'speed': 'Fast'
        },
        'gemini-2.0-flash-live': {
            'context_window': '1M tokens',
            'features': ['Real-time', 'Bidirectional streaming', 'Voice'],
            'best_for': 'Real-time voice applications and streaming',
            'pricing': 'Medium',
            'speed': 'Real-time'
        }
    }

    if model_name not in models_info:
        return {
            'status': 'error',
            'report': f'Model {model_name} not found in database',
            'error': 'Model not found'
        }

    info = models_info[model_name]
    return {
        'status': 'success',
        'report': f'Information for {model_name}',
        'model': model_name,
        'info': info
    }


# ============================================================================
# ROOT AGENT (required by ADK)
# ============================================================================

root_agent = Agent(
    name="model_selector_agent",
    model="gemini-2.5-flash",
    description="Expert agent for selecting and comparing AI models",
    instruction="""
You are an expert AI model selection advisor. You help users:
1. Choose the right model for their use case
2. Understand model capabilities and limitations
3. Optimize costs and performance
4. Compare different models

When recommending models:
- Consider the use case requirements carefully
- Explain the reasoning behind recommendations
- Mention tradeoffs (cost vs performance vs features)
- Suggest alternatives when appropriate

Available models (2025):
- gemini-2.5-flash: RECOMMENDED - Best price-performance for general use
- gemini-2.5-flash-lite: Ultra-fast and cheapest for simple/high-volume tasks
- gemini-2.5-pro: Highest quality for complex reasoning and critical tasks
- gemini-2.0-flash-live: Real-time bidirectional streaming for voice apps
- gemini-2.0-flash: General purpose with legacy compatibility

Always be helpful, clear, and provide actionable recommendations.
    """.strip(),
    tools=[
        recommend_model_for_use_case,
        get_model_info
    ]
)


# ============================================================================
# STANDALONE DEMO FUNCTION
# ============================================================================

async def demo_model_comparison():
    """Standalone demo function for comparing models."""
    selector = ModelSelector()

    # Test queries
    test_queries = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms",
        "Write a haiku about artificial intelligence",
        "Calculate the compound interest on $10,000 at 5% for 10 years",
        "List the top 5 programming languages in 2025"
    ]

    instruction = """
You are a helpful assistant. Answer questions accurately and concisely.
    """.strip()

    # Compare models (using available models in 2025)
    models_to_test = [
        'gemini-2.5-flash',      # NEW DEFAULT - Best price-performance
        'gemini-2.0-flash',      # Legacy but still available
        'gemini-2.5-flash-lite', # Ultra-fast for simple tasks
    ]

    await selector.compare_models(models_to_test, test_queries, instruction)

    # Use case recommendations
    print(f"\n\n{'='*70}")
    print("USE CASE RECOMMENDATIONS")
    print(f"{'='*70}\n")

    use_cases = [
        "Real-time voice assistant",
        "Complex strategic planning",
        "High-volume content moderation",
        "Critical business decision support",
        "General customer service"
    ]

    for use_case in use_cases:
        result = recommend_model_for_use_case(use_case, None)
        print(f"📌 {use_case}")
        print(f"   → Recommended: {result['model']}")
        print(f"   → Reason: {result['reason']}\n")


def compare_models_detailed():
    """
    Synchronous wrapper for model comparison.
    Returns a dict with comparison results and key findings.
    """
    import asyncio

    async def run_comparison():
        selector = ModelSelector()

        test_queries = [
            "What is the capital of France?",
            "Explain quantum computing in simple terms",
            "Write a haiku about artificial intelligence"
        ]

        instruction = "You are a helpful assistant. Answer questions accurately and concisely."

        models_to_test = [
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-2.5-flash-lite'
        ]

        await selector.compare_models(models_to_test, test_queries, instruction)

        # Generate key findings based on benchmarks
        key_findings = []
        if selector.benchmarks:
            fastest = min(selector.benchmarks.items(), key=lambda x: x[1].avg_latency)
            slowest = max(selector.benchmarks.items(), key=lambda x: x[1].avg_latency)
            best_quality = max(selector.benchmarks.items(), key=lambda x: x[1].quality_score)
            cheapest = min(selector.benchmarks.items(), key=lambda x: x[1].cost_estimate)

            key_findings = [
                f"{fastest[0]} is {slowest[1].avg_latency/fastest[1].avg_latency:.1f}x faster than {slowest[0]}",
                f"{best_quality[0]} provides the highest quality score ({best_quality[1].quality_score:.3f})",
                f"{cheapest[0]} is the most cost-effective option",
                "gemini-2.5-flash offers the best price-performance balance"
            ]

        return {
            'key_findings': key_findings,
            'benchmarks': {k: v.__dict__ for k, v in selector.benchmarks.items()}
        }

    return asyncio.run(run_comparison())


if __name__ == '__main__':
    # Run standalone demo
    asyncio.run(demo_model_comparison())
