"""Guidance for activating Gemini Live API access on Vertex AI."""

from __future__ import annotations

import textwrap


_STEPS = [
    "Verify your Google Cloud project has billing enabled and Vertex AI API activated (gcloud services enable aiplatform.googleapis.com).",
    "Upgrade to a paid Vertex AI plan (standard or enterprise) if you are still on the free tier.",
    "Open a Google Cloud support case or contact your account team requesting Gemini Live API publisher model access for your project and region (example: us-central1).",
    "In your request, include the exact model ids you plan to use (e.g., gemini-live-2.5-flash-preview-native-audio or other native audio variants) and confirm required regions.",
    "After Google enables the models, run 'make live_models_list' to confirm they are discoverable and update VOICE_ASSISTANT_LIVE_MODEL accordingly.",
]


def main() -> int:
    print("📡 Steps to activate Gemini Live API on Vertex AI:")
    for idx, step in enumerate(_STEPS, start=1):
        wrapped = textwrap.fill(step, width=88, subsequent_indent="     ")
        print(f"  {idx}. {wrapped}")
    print("\nℹ️  Tip: approval typically takes 1-2 business days; follow up with support if access is delayed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
