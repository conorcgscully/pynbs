#!/usr/bin/env python3
import os
import json
from google.cloud import storage

def setup_gcs_auth():
    """Setup GCS authentication from environment variable"""
    if 'GCS_SERVICE_ACCOUNT_KEY' not in os.environ:
        raise Exception("GCS_SERVICE_ACCOUNT_KEY environment variable not set")
    
    # Write credentials to temp file
    credentials_json = os.environ['GCS_SERVICE_ACCOUNT_KEY']
    with open('/tmp/gcs-key.json', 'w') as f:
        f.write(credentials_json)
    
    # Set environment variable for Google Cloud client libraries
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/tmp/gcs-key.json'
    print("✅ GCS authentication configured")

def upload_file_to_gcs(local_file_path, bucket_name, blob_name=None):
    """Upload a file to GCS bucket"""
    if blob_name is None:
        blob_name = os.path.basename(local_file_path)
    
    # Initialize the client
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Upload the file
    print(f"📤 Uploading {local_file_path} to gs://{bucket_name}/{blob_name}")
    blob.upload_from_filename(local_file_path)
    print(f"✅ Upload complete: gs://{bucket_name}/{blob_name}")
    
    return f"gs://{bucket_name}/{blob_name}"

def main():
    # Setup authentication
    setup_gcs_auth()
    
    # Create the test file
    test_file = "writeme.txt"
    with open(test_file, 'w') as f:
        f.write(f"Hello from Vast.ai instance!\n")
        f.write(f"Timestamp: {os.popen('date').read().strip()}\n")
        f.write(f"Hostname: {os.popen('hostname').read().strip()}\n")
    
    print(f"📝 Created {test_file}")
    
    # Upload to GCS
    bucket_name = "cs-datalake"
    remote_path = f"vast-uploads/{os.popen('hostname').read().strip()}/writeme.txt"
    
    gcs_url = upload_file_to_gcs(test_file, bucket_name, remote_path)
    print(f"🎉 File successfully uploaded to: {gcs_url}")
    
    # Cleanup
    os.remove('/tmp/gcs-key.json')
    print("🧹 Cleaned up temporary credentials")

if __name__ == "__main__":
    main()