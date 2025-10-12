"""Validate that the configured Live model is available in the Vertex project."""

import os
import sys

from google.genai import Client, errors


def _load_environment() -> tuple[str, str, str]:
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is not set")

    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model = os.environ.get("VOICE_ASSISTANT_LIVE_MODEL")
    if not model:
        raise RuntimeError("VOICE_ASSISTANT_LIVE_MODEL is not set")

    return project, location, model


def main() -> int:
    try:
        project, location, model = _load_environment()
    except RuntimeError as exc:  # pragma: no cover
        print(f"   ❌ {exc}")
        return 1

    try:
        client = Client(vertexai=True, project=project, location=location)
        client.models.get(model=model)
    except errors.ClientError as exc:
        message = str(exc)
        print(f"   ❌ Live model lookup failed: {message}")
        if "Publisher Model" in message or "NOT_FOUND" in message:
            print("   👉 The selected model is not enabled for this project/region.")
            print("   👉 Run `make live_models_doc` for supported IDs or request Vertex Live access.")
            print("   👉 After access is granted, rerun `make live_models_list` to confirm availability.")
        return 1
    except Exception as exc:  # pragma: no cover
        print(f"   ❌ Unexpected error validating live model: {exc}")
        return 1

    print("   ✅ Live model is discoverable in this project/region.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
