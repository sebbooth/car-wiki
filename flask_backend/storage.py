import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

class FirebaseStorageWrapper:
    def __init__(self, app):
        self.app = app

    def bucket(self, bucket_name):
        return storage.bucket(bucket_name)

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        bucket = self.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(f'File {source_file_name} uploaded to {destination_blob_name}')

    def download_blob(self, bucket_name, source_blob_name, destination_file_name):
        bucket = self.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f'File {source_blob_name} downloaded to {destination_file_name}')
    
fb_app = firebase_admin.initialize_app(credentials.Certificate("./.env/creds.json"))
fb_store = FirebaseStorageWrapper(fb_app)

bucket = fb_store.bucket("testFolder")
print(bucket)
fb_store.upload_blob("testFolder", "app.py", "testAdd")