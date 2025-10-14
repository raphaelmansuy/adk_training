"""
ADK Tutorial 24: Advanced Observability & Monitoring

This agent demonstrates comprehensive observability patterns including:
- SaveFilesAsArtifactsPlugin for automatic file saving
- MetricsCollectorPlugin for request/response tracking
- AlertingPlugin for error detection and alerts
- PerformanceProfilerPlugin for detailed performance analysis
- ProductionMonitoringSystem for complete monitoring solution

Features:
- Plugin-based architecture for modular observability
- Real-time metrics collection and reporting
- Error detection and alerting
- Performance profiling and analysis
- Production-ready monitoring patterns
"""

import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from google.adk.agents import Agent
from google.adk.plugins import BasePlugin
from google.adk.events import Event
from google.genai import types


@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    request_id: str
    agent_name: str
    start_time: float
    end_time: Optional[float] = None
    latency: Optional[float] = None
    success: bool = True
    error: Optional[str] = None
    token_count: int = 0
    tool_calls: int = 0


@dataclass
class AggregateMetrics:
    """Aggregate metrics across requests."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency: float = 0.0
    total_tokens: int = 0
    total_tool_calls: int = 0
    requests: List[RequestMetrics] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests

    @property
    def avg_latency(self) -> float:
        """Calculate average latency."""
        if self.total_requests == 0:
            return 0.0
        return self.total_latency / self.total_requests

    @property
    def avg_tokens(self) -> float:
        """Calculate average tokens."""
        if self.total_requests == 0:
            return 0.0
        return self.total_tokens / self.total_requests


class MetricsCollectorPlugin(BasePlugin):
    """Plugin to collect request metrics."""

    def __init__(self, name: str = 'metrics_collector_plugin'):
        """Initialize metrics collector."""
        super().__init__(name)
        self.metrics = AggregateMetrics()
        self.current_requests: Dict[str, RequestMetrics] = {}

    async def on_event_callback(self, *, invocation_context, event: Event) -> Optional[Event]:
        """Handle agent events for metrics collection."""
        # Track events (implementation simplified for tutorial)
        if hasattr(event, 'event_type'):
            if event.event_type == 'request_start':
                request_id = str(time.time())
                metrics = RequestMetrics(
                    request_id=request_id,
                    agent_name='observability_agent',
                    start_time=time.time()
                )
                self.current_requests[request_id] = metrics
                print(f"📊 [METRICS] Request started at {datetime.now().strftime('%H:%M:%S')}")
            
            elif event.event_type == 'request_complete':
                if self.current_requests:
                    request_id = list(self.current_requests.keys())[0]
                    metrics = self.current_requests[request_id]
                    metrics.end_time = time.time()
                    metrics.latency = metrics.end_time - metrics.start_time
                    
                    # Update aggregates
                    self.metrics.total_requests += 1
                    self.metrics.successful_requests += 1
                    self.metrics.total_latency += metrics.latency
                    self.metrics.requests.append(metrics)
                    
                    print(f"✅ [METRICS] Request completed: {metrics.latency:.2f}s")
                    del self.current_requests[request_id]

    def get_summary(self) -> str:
        """Get metrics summary."""
        m = self.metrics

        summary = f"""
METRICS SUMMARY
{'='*70}

Total Requests:       {m.total_requests}
Successful:           {m.successful_requests}
Failed:               {m.failed_requests}
Success Rate:         {m.success_rate*100:.1f}%

Average Latency:      {m.avg_latency:.2f}s
Average Tokens:       {m.avg_tokens:.0f}
Total Tool Calls:     {m.total_tool_calls}

{'='*70}
        """.strip()

        return summary


class AlertingPlugin(BasePlugin):
    """Plugin for alerting on anomalies."""

    def __init__(self, name: str = 'alerting_plugin', latency_threshold: float = 5.0, error_threshold: int = 3):
        """
        Initialize alerting plugin.

        Args:
            name: Plugin name
            latency_threshold: Alert if latency exceeds this (seconds)
            error_threshold: Alert if consecutive errors exceed this
        """
        super().__init__(name)
        self.latency_threshold = latency_threshold
        self.error_threshold = error_threshold
        self.consecutive_errors = 0

    async def on_event_callback(self, *, invocation_context, event: Event) -> Optional[Event]:
        """Handle agent events for alerting."""
        if hasattr(event, 'event_type'):
            if event.event_type == 'request_complete':
                # Reset error counter on success
                self.consecutive_errors = 0
            
            elif event.event_type == 'request_error':
                self.consecutive_errors += 1
                print("🚨 [ALERT] Error detected")
                
                if self.consecutive_errors >= self.error_threshold:
                    print(f"🚨🚨 [CRITICAL ALERT] {self.consecutive_errors} consecutive errors!")


class PerformanceProfilerPlugin(BasePlugin):
    """Plugin for detailed performance profiling."""

    def __init__(self, name: str = 'performance_profiler_plugin'):
        """Initialize profiler."""
        super().__init__(name)
        self.profiles: List[Dict] = []
        self.current_profile: Optional[Dict] = None

    async def on_event_callback(self, *, invocation_context, event: Event) -> Optional[Event]:
        """Handle agent events for profiling."""
        if hasattr(event, 'event_type'):
            if event.event_type == 'tool_call_start':
                self.current_profile = {
                    'tool': getattr(event, 'tool_name', 'unknown'),
                    'start_time': time.time()
                }
                print("⚙️ [PROFILER] Tool call started")
            
            elif event.event_type == 'tool_call_complete':
                if self.current_profile:
                    self.current_profile['end_time'] = time.time()
                    self.current_profile['duration'] = (
                        self.current_profile['end_time'] - self.current_profile['start_time']
                    )
                    self.profiles.append(self.current_profile)
                    print(f"✅ [PROFILER] Tool call completed: {self.current_profile['duration']:.2f}s")
                    self.current_profile = None

    def get_profile_summary(self) -> str:
        """Get profiling summary."""
        if not self.profiles:
            return "No profiles collected"

        summary = f"\nPERFORMANCE PROFILE\n{'='*70}\n\n"

        tool_stats = {}

        for profile in self.profiles:
            if 'duration' not in profile:
                continue

            tool = profile['tool']

            if tool not in tool_stats:
                tool_stats[tool] = {
                    'calls': 0,
                    'total_duration': 0.0,
                    'min_duration': float('inf'),
                    'max_duration': 0.0
                }

            stats = tool_stats[tool]
            stats['calls'] += 1
            stats['total_duration'] += profile['duration']
            stats['min_duration'] = min(stats['min_duration'], profile['duration'])
            stats['max_duration'] = max(stats['max_duration'], profile['duration'])

        for tool, stats in tool_stats.items():
            avg_duration = stats['total_duration'] / stats['calls']

            summary += f"Tool: {tool}\n"
            summary += f"  Calls:        {stats['calls']}\n"
            summary += f"  Avg Duration: {avg_duration:.3f}s\n"
            summary += f"  Min Duration: {stats['min_duration']:.3f}s\n"
            summary += f"  Max Duration: {stats['max_duration']:.3f}s\n\n"

        summary += f"{'='*70}\n"

        return summary


# Create the observability agent with all plugins
root_agent = Agent(
    model='gemini-2.5-flash',
    name='observability_agent',
    description="""Production assistant with comprehensive observability including metrics collection, 
alerting, and performance profiling for enterprise monitoring.""",
    instruction="""
You are a production assistant helping with customer inquiries about AI and technology.

Key behaviors:
- Provide accurate, helpful responses
- Keep responses concise but informative
- Use clear, simple language
- Stay on topic and focused

Your responses are being monitored for quality, performance, and reliability.
Always be helpful and accurate.
    """.strip(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,
        max_output_tokens=1024
    )
)


def main():
    """
    Main entry point for demonstration.
    
    This function demonstrates how to use the observability agent with the ADK web interface.
    The actual monitoring plugins are registered at the runner level (see tests for examples).
    """
    print("🚀 Tutorial 24: Advanced Observability & Monitoring")
    print("=" * 70)
    print("\n📊 Observability Agent Features:")
    print("  • SaveFilesAsArtifactsPlugin - automatic file saving")
    print("  • MetricsCollectorPlugin - request/response metrics")
    print("  • AlertingPlugin - error detection and alerts")
    print("  • PerformanceProfilerPlugin - detailed profiling")
    print("\n💡 To see the agent in action:")
    print("  1. Run: adk web")
    print("  2. Open http://localhost:8000")
    print("  3. Select 'observability_agent' from dropdown")
    print("  4. Try various prompts and observe console metrics")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
