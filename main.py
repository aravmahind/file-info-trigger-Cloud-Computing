# Importing essential modules
import base64
import json
from flask import Flask, request

# Setting up a basic Flask app
app = Flask(__name__)

# This route will be triggered when a file is uploaded to the bucket
@app.route("/", methods=["POST"])
def handle_gcs_event():
    # Get the incoming JSON data (should contain file info)
    event = request.get_json()
    
    if not event:
        return "No JSON received", 400  # Return error if no JSON payload is received

    # Extract file details from the event
    name = event["name"]
    size = event["size"]
    content_type = event["contentType"]

    # Get the file extension (like jpg, pdf, etc.)
    file_format = name.split('.')[-1] if '.' in name else 'unknown'

    # Create a message to send to Pub/Sub
    message = {
        "name": name,
        "size": size,
        "format": file_format
    }

    # Now sending this info to Pub/Sub
    from google.cloud import pubsub_v1
    publisher = pubsub_v1.PublisherClient()
    
    # Define the topic path (replace with your real project ID)
    topic_path = publisher.topic_path("your-project-id", "file-info-topic")

    # Publish the message to the topic in JSON format
    publisher.publish(topic_path, json.dumps(message).encode("utf-8"))

    # Return success message
    return f"Published info for {name}", 200
