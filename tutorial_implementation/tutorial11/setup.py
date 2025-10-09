from setuptools import setup, find_packages

setup(
    name="grounding_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-adk>=1.15.1",
        "google-genai>=1.15.0",
    ],
)