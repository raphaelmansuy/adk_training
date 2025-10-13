"""
Tutorial 20: YAML Configuration - Customer Support Agent

This module loads the agent configuration from root_agent.yaml
and exports it as root_agent for ADK web interface discovery.
"""

import os
from google.adk.agents import config_agent_utils


# Load agent from YAML configuration - path is relative to the package root
config_path = os.path.join(os.path.dirname(__file__), 'root_agent.yaml')
root_agent = config_agent_utils.from_config(config_path)

__all__ = ['root_agent']