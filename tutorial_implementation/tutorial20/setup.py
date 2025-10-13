from setuptools import setup, find_packages

setup(
    name="tutorial20",
    version="0.1.0",
    packages=find_packages(include=["tutorial20", "tutorial20.*", "customer_support", "customer_support.*"]),
    install_requires=["google-adk>=1.15.1"],
    description="Tutorial 20: YAML Configuration - Declarative Agent Setup",
    python_requires=">=3.9",
)