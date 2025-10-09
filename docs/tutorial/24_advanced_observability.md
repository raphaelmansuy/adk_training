---
id: advanced_observability
title: "Tutorial 24: Advanced Observability - Enterprise Monitoring"
description: "Implement enterprise-grade observability with metrics, traces, logs, and alerting for production agent systems at scale."
sidebar_label: "24. Advanced Observability"
sidebar_position: 24
tags: ["advanced", "observability", "monitoring", "enterprise", "production"]
keywords: ["enterprise observability", "metrics", "traces", "logs", "alerting", "production monitoring"]
status: "draft"
difficulty: "advanced"
estimated_time: "2.5 hours"
prerequisites: ["Tutorial 18: Events & Observability", "Tutorial 23: Production Deployment", "Monitoring tools experience"]
learning_objectives:
  - "Implement enterprise observability patterns"
  - "Set up metrics, traces, and logs"
  - "Configure alerting and dashboards"
  - "Monitor agent performance at scale"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial24"
---

# Tutorial 24: Advanced Observability & Monitoring

**Goal**: Master advanced observability patterns including plugin systems, Cloud Trace integration, custom metrics, distributed tracing, and production monitoring dashboards.

**Prerequisites**:

- Tutorial 18 (Events & Observability)
- Tutorial 23 (Production Deployment)
- Understanding of observability concepts

**What You'll Learn**:

- ADK plugin system for monitoring
- Cloud Trace integration (`trace_to_cloud`)
- SaveFilesAsArtifactsPlugin for debugging
- Custom observability plugins
- Distributed tracing across agents
- Performance metrics collection
- Production monitoring dashboards
- Alerting and incident response

**Time to Complete**: 55-70 minutes

---

## Why Advanced Observability Matters

**Problem**: Production agents require deep visibility into behavior, performance, and failures for debugging and optimization.

**Solution**: **Advanced observability** with plugins, distributed tracing, and custom metrics provides comprehensive system insight.

**Benefits**:

- 🔍 **Deep Visibility**: Understand complex agent behaviors
- 🐛 **Faster Debugging**: Quickly identify root causes
- 📊 **Performance Insights**: Optimize based on real data
- 🚨 **Proactive Alerting**: Detect issues before users
- 📈 **Trend Analysis**: Identify patterns over time
- 🎯 **Bottleneck Identification**: Find performance constraints

**Observability Pillars**:

- **Traces**: Request flow through system
- **Metrics**: Quantitative measurements
- **Logs**: Detailed event records
- **Events**: State changes and actions

---

## 1. ADK Plugin System

### What Are Plugins?

**Plugins** are modular extensions that intercept and observe agent execution without modifying core logic.

**Source**: `google/adk/plugins/`

**Use Cases**:

- Saving artifacts automatically
- Sending traces to Cloud Trace
- Custom metrics collection
- Performance profiling
- Compliance logging

### Built-in Plugins

#### SaveFilesAsArtifactsPlugin

Automatically saves agent outputs as artifacts.

```python
"""
SaveFilesAsArtifactsPlugin example.
"""

import asyncio
import os
from google.adk.agents import Agent, Runner, RunConfig
from google.adk.plugins import SaveFilesAsArtifactsPlugin
from google.genai import types

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


async def main():
    """Demonstrate SaveFilesAsArtifactsPlugin."""
    
    # Create agent
    agent = Agent(
        model='gemini-2.0-flash',
        name='artifact_agent',
        instruction="Generate reports and save them automatically."
    )
    
    # Create plugin
    artifact_plugin = SaveFilesAsArtifactsPlugin(
        output_dir='./artifacts',  # Where to save files
        save_all_responses=True    # Save all agent responses
    )
    
    # Configure run with plugin
    run_config = RunConfig(
        plugins=[artifact_plugin]
    )
    
    # Run agent
    runner = Runner()
    result = await runner.run_async(
        "Generate a brief report about AI agents",
        agent=agent,
        run_config=run_config
    )
    
    print("✅ Response saved as artifact")
    print(f"Response: {result.content.parts[0].text[:200]}...")


if __name__ == '__main__':
    asyncio.run(main())
```

---

## 2. Cloud Trace Integration

### Enabling Cloud Trace

**Cloud Trace** provides distributed tracing for Google Cloud applications.

```python
"""
Cloud Trace integration example.
"""

import asyncio
import os
from google.adk.agents import Agent, Runner, RunConfig
from google.genai import types

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


async def main():
    """Agent with Cloud Trace enabled."""
    
    agent = Agent(
        model='gemini-2.0-flash',
        name='traced_agent',
        instruction="You are a helpful assistant."
    )
    
    # Enable Cloud Trace
    run_config = RunConfig(
        trace_to_cloud=True  # Send traces to Cloud Trace
    )
    
    runner = Runner()
    
    # Run agent - traces automatically sent to Cloud Trace
    result = await runner.run_async(
        "What is machine learning?",
        agent=agent,
        run_config=run_config
    )
    
    print(f"Response: {result.content.parts[0].text}")
    print("\n✅ Trace sent to Cloud Trace")
    print("View traces at: https://console.cloud.google.com/traces")


if __name__ == '__main__':
    asyncio.run(main())
```

### Viewing Traces in Cloud Console

```bash
# View traces in Cloud Console
https://console.cloud.google.com/traces?project=your-project-id

# Filter traces by agent name
# Analyze latency, spans, and errors
# Identify performance bottlenecks
```

---

## 3. Real-World Example: Production Monitoring System

Let's build a comprehensive production monitoring system with custom plugins and metrics.

### Complete Implementation

```python
"""
Production Monitoring System
Custom plugins for metrics, tracing, and alerting.
"""

import asyncio
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from google.adk.agents import Agent, Runner, RunConfig, Session
from google.adk.plugins import BasePlugin
from google.adk.events import Event
from google.genai import types

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


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
    
    def __init__(self):
        """Initialize metrics collector."""
        super().__init__()
        self.metrics = AggregateMetrics()
        self.current_requests: Dict[str, RequestMetrics] = {}
    
    async def on_request_start(self, request_id: str, agent: Agent, query: str):
        """Called when request starts."""
        
        request_metrics = RequestMetrics(
            request_id=request_id,
            agent_name=agent.name,
            start_time=time.time()
        )
        
        self.current_requests[request_id] = request_metrics
        
        print(f"📊 [METRICS] Request {request_id} started")
    
    async def on_request_complete(self, request_id: str, result):
        """Called when request completes."""
        
        if request_id not in self.current_requests:
            return
        
        metrics = self.current_requests[request_id]
        metrics.end_time = time.time()
        metrics.latency = metrics.end_time - metrics.start_time
        
        # Estimate token count
        text = result.content.parts[0].text
        metrics.token_count = len(text.split())
        
        # Update aggregates
        self.metrics.total_requests += 1
        self.metrics.successful_requests += 1
        self.metrics.total_latency += metrics.latency
        self.metrics.total_tokens += metrics.token_count
        self.metrics.requests.append(metrics)
        
        print(f"✅ [METRICS] Request {request_id} completed: {metrics.latency:.2f}s, ~{metrics.token_count} tokens")
        
        del self.current_requests[request_id]
    
    async def on_request_error(self, request_id: str, error: Exception):
        """Called when request fails."""
        
        if request_id not in self.current_requests:
            return
        
        metrics = self.current_requests[request_id]
        metrics.end_time = time.time()
        metrics.latency = metrics.end_time - metrics.start_time
        metrics.success = False
        metrics.error = str(error)
        
        # Update aggregates
        self.metrics.total_requests += 1
        self.metrics.failed_requests += 1
        self.metrics.requests.append(metrics)
        
        print(f"❌ [METRICS] Request {request_id} failed: {error}")
        
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
    
    def __init__(self, latency_threshold: float = 5.0, error_threshold: int = 3):
        """
        Initialize alerting plugin.
        
        Args:
            latency_threshold: Alert if latency exceeds this (seconds)
            error_threshold: Alert if consecutive errors exceed this
        """
        super().__init__()
        self.latency_threshold = latency_threshold
        self.error_threshold = error_threshold
        self.consecutive_errors = 0
    
    async def on_request_complete(self, request_id: str, result):
        """Check for latency anomalies."""
        
        # Reset error counter
        self.consecutive_errors = 0
    
    async def on_request_error(self, request_id: str, error: Exception):
        """Alert on errors."""
        
        self.consecutive_errors += 1
        
        print(f"🚨 [ALERT] Error in request {request_id}: {error}")
        
        if self.consecutive_errors >= self.error_threshold:
            print(f"🚨🚨 [CRITICAL ALERT] {self.consecutive_errors} consecutive errors!")
            # In production: send to PagerDuty, Slack, etc.


class PerformanceProfilerPlugin(BasePlugin):
    """Plugin for detailed performance profiling."""
    
    def __init__(self):
        """Initialize profiler."""
        super().__init__()
        self.profiles: List[Dict] = []
    
    async def on_tool_call_start(self, tool_name: str, args: dict):
        """Profile tool call start."""
        
        profile = {
            'tool': tool_name,
            'start_time': time.time(),
            'args': args
        }
        
        self.profiles.append(profile)
        
        print(f"⚙️ [PROFILER] Tool call started: {tool_name}")
    
    async def on_tool_call_complete(self, tool_name: str, result):
        """Profile tool call completion."""
        
        # Find matching profile
        for profile in reversed(self.profiles):
            if profile['tool'] == tool_name and 'end_time' not in profile:
                profile['end_time'] = time.time()
                profile['duration'] = profile['end_time'] - profile['start_time']
                profile['result_size'] = len(str(result))
                
                print(f"✅ [PROFILER] Tool call completed: {tool_name} ({profile['duration']:.2f}s)")
                break
    
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


class ProductionMonitoringSystem:
    """Comprehensive production monitoring system."""
    
    def __init__(self):
        """Initialize monitoring system."""
        
        # Create plugins
        self.metrics_plugin = MetricsCollectorPlugin()
        self.alerting_plugin = AlertingPlugin(latency_threshold=3.0, error_threshold=2)
        self.profiler_plugin = PerformanceProfilerPlugin()
        
        # Create run config with all plugins
        self.run_config = RunConfig(
            plugins=[
                self.metrics_plugin,
                self.alerting_plugin,
                self.profiler_plugin
            ],
            trace_to_cloud=True  # Also send to Cloud Trace
        )
        
        # Create agent
        self.agent = Agent(
            model='gemini-2.0-flash',
            name='monitored_agent',
            instruction="""
You are a production assistant helping with customer inquiries.
Always be helpful and accurate.
            """.strip(),
            generate_content_config=types.GenerateContentConfig(
                temperature=0.5,
                max_output_tokens=1024
            )
        )
        
        self.runner = Runner()
        self.session = Session()
    
    async def process_query(self, query: str):
        """Process query with full monitoring."""
        
        print(f"\n{'='*70}")
        print(f"QUERY: {query}")
        print(f"{'='*70}\n")
        
        try:
            result = await self.runner.run_async(
                query,
                agent=self.agent,
                session=self.session,
                run_config=self.run_config
            )
            
            print(f"\n📄 RESPONSE:\n{result.content.parts[0].text}\n")
            print(f"{'='*70}\n")
        
        except Exception as e:
            print(f"\n❌ ERROR: {e}\n")
            print(f"{'='*70}\n")
    
    def get_full_report(self) -> str:
        """Get comprehensive monitoring report."""
        
        report = "\n\n"
        report += "="*70 + "\n"
        report += "COMPREHENSIVE MONITORING REPORT\n"
        report += "="*70 + "\n\n"
        
        report += self.metrics_plugin.get_summary() + "\n\n"
        report += self.profiler_plugin.get_profile_summary() + "\n"
        
        return report


async def main():
    """Main entry point."""
    
    monitor = ProductionMonitoringSystem()
    
    # Process queries
    queries = [
        "What is artificial intelligence?",
        "Explain machine learning in simple terms",
        "What are the applications of AI?",
        "How does deep learning work?",
        "What is the future of AI?"
    ]
    
    for query in queries:
        await monitor.process_query(query)
        await asyncio.sleep(1)
    
    # Print comprehensive report
    print(monitor.get_full_report())


if __name__ == '__main__':
    asyncio.run(main())
```

### Expected Output

```
======================================================================
QUERY: What is artificial intelligence?
======================================================================

📊 [METRICS] Request req-001 started
✅ [METRICS] Request req-001 completed: 1.23s, ~85 tokens

📄 RESPONSE:
Artificial intelligence (AI) is a branch of computer science that focuses
on creating systems capable of performing tasks that typically require 
human intelligence. These tasks include learning, reasoning, problem-solving,
perception, and language understanding.

======================================================================

======================================================================
QUERY: Explain machine learning in simple terms
======================================================================

📊 [METRICS] Request req-002 started
✅ [METRICS] Request req-002 completed: 1.45s, ~112 tokens

📄 RESPONSE:
Machine learning is a subset of AI where computers learn from data without
being explicitly programmed. Instead of following fixed instructions, machine
learning systems identify patterns in data and improve their performance over
time through experience.

======================================================================

[... more queries ...]


======================================================================
COMPREHENSIVE MONITORING REPORT
======================================================================

METRICS SUMMARY
======================================================================

Total Requests:       5
Successful:           5
Failed:               0
Success Rate:         100.0%

Average Latency:      1.35s
Average Tokens:       95
Total Tool Calls:     0

======================================================================


PERFORMANCE PROFILE
======================================================================

No tools called in this session.

======================================================================
```

---

## 4. Custom Monitoring Dashboard

### Prometheus Metrics Export

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response

app = FastAPI()

# Metrics
request_counter = Counter('agent_requests_total', 'Total agent requests')
request_duration = Histogram('agent_request_duration_seconds', 'Request duration')
active_requests = Gauge('agent_active_requests', 'Currently active requests')
error_counter = Counter('agent_errors_total', 'Total errors')


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type="text/plain")


@app.middleware("http")
async def track_metrics(request, call_next):
    """Middleware to track metrics."""
    
    active_requests.inc()
    request_counter.inc()
    
    with request_duration.time():
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            error_counter.inc()
            raise
        finally:
            active_requests.dec()
```

---

## Summary

You've mastered advanced observability:

**Key Takeaways**:

- ✅ ADK plugin system for modular observability
- ✅ SaveFilesAsArtifactsPlugin for automatic saving
- ✅ Cloud Trace integration with `trace_to_cloud=True`
- ✅ Custom plugins for metrics, alerting, profiling
- ✅ Prometheus metrics export
- ✅ Production monitoring dashboards
- ✅ Comprehensive error tracking

**Production Checklist**:

- [ ] Cloud Trace enabled
- [ ] Custom metrics collected
- [ ] Alerting configured
- [ ] Performance profiling enabled
- [ ] Monitoring dashboard deployed
- [ ] SLI/SLO defined
- [ ] Incident response runbook created
- [ ] Regular metrics review scheduled

**Next Steps**:

- **Tutorial 25**: Master Best Practices & Patterns (Final Tutorial!)

**Resources**:

- [Cloud Trace Documentation](https://cloud.google.com/trace/docs)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Grafana Dashboards](https://grafana.com/docs/)

---

**🎉 Tutorial 24 Complete!** You now know advanced observability patterns. Continue to Tutorial 25 for best practices and the completion of the series!
