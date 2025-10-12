"""Utility script to list available Live API models for the configured Vertex project."""

import os
import sys
from typing import List

try:
    from google.genai import Client
except ImportError:  # pragma: no cover
    print("google-genai package is required to query models.")
    raise


def _load_client() -> Client:
    """Create a Vertex-enabled client using environment configuration."""
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is not set")

    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    return Client(vertexai=True, project=project, location=location)


def list_live_models(client: Client) -> List[str]:
    """Return the identifiers of models that support Vertex Live API."""
    live_models: List[str] = []
    for model in client.models.list():
        name = getattr(model, "name", "") or ""
        if "live" in name.lower():
            live_models.append(name.split("/")[-1])
    return live_models


def _print_banner(message: str) -> None:
    print(f"   {message}")


def main() -> int:
    try:
        client = _load_client()
    except Exception as exc:  # pragma: no cover
        _print_banner(f"❌ Unable to initialize Vertex client: {exc}")
        return 1

    live_models = list_live_models(client)
    if not live_models:
        _print_banner("❌ No Live API models are currently visible in this project/region.")
        _print_banner("👉 Request Vertex Live access or switch to a supported region.")
        _print_banner("👉 Contact Google Cloud support to enable Live API publisher models if needed.")
        return 1

    _print_banner("✅ Live-capable models detected:")
    for model_name in live_models:
        print(f"      • {model_name}")
    _print_banner("ℹ️  If a required model is missing, verify entitlements and region availability.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
