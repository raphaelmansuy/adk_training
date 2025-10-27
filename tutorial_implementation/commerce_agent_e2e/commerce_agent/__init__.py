# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Commerce Agent - A specialized e-commerce assistant using Google ADK.

This agent handles:
- Product searches and recommendations
- Price comparisons
- Technical specifications
- Delivery information
- User preferences management

The agent uses Google Search for grounding (source attribution) and maintains
user preferences across sessions.
"""

from .agent import root_agent
from .callbacks import create_grounding_callback
from .types import ToolResult, UserPreferences, GroundingMetadata, GroundingSource

__all__ = [
    "root_agent",
    "create_grounding_callback",
    "ToolResult",
    "UserPreferences",
    "GroundingMetadata",
    "GroundingSource",
]
