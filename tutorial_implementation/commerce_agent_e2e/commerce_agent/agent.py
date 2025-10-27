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

"""Commerce Agent - Simplified and Clean Architecture.

This agent helps users find sports products with Google Search grounding.
Following official ADK sample patterns for simplicity and maintainability.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .config import MODEL_NAME, AGENT_NAME
from .tools.search import search_products
from .tools.preferences import save_preferences, get_preferences
from .prompt import commerce_agent_instruction

root_agent = Agent(
    model=MODEL_NAME,
    name=AGENT_NAME,
    instruction=commerce_agent_instruction,
    tools=[
        search_products,  # AgentTool wrapping Google Search
        FunctionTool(func=save_preferences),
        FunctionTool(func=get_preferences),
    ],
)
