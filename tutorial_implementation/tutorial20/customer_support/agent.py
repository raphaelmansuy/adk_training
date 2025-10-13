"""
Customer Support Agent - ADK Web Interface

This agent loads configuration from root_agent.yaml and provides
customer support functionality through the ADK web interface.
"""

from google.adk.agents import config_agent_utils
import os

# Load agent from YAML configuration
config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'root_agent.yaml')
root_agent = config_agent_utils.from_config(config_path)