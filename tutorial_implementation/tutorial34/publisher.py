import os
import json
from google.cloud import pubsub_v1
from datetime import datetime

project_id = os.environ.get("GCP_PROJECT")
topic_id = "document-uploads"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_document(document_id: str, content: str):
    """Publish a document for processing."""
    message_data = {
        "document_id": document_id,
        "content": content,
        "uploaded_at": datetime.now().isoformat(),
    }

    data = json.dumps(message_data).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()

    print(f"✅ Published {document_id} (message ID: {message_id})")
    return message_id

# Example
if __name__ == "__main__":
    publish_document(
        "DOC-001",
        "Q4 2024 Financial Report: Revenue $1.2M, Profit 33%"
    )

