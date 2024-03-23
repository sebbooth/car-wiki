import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("./.env/creds.json")
fb_app = firebase_admin.initialize_app(cred)
db = firestore.client()


class FirestoreDBWrapper:
    def __init__(self, app):
        self.app = app
        self.db = firestore.client()

    def collection(self, collection_name):
        return self.db.collection(collection_name)

    def document(self, collection_name, document_id):
        return self.db.document(f'{collection_name}/{document_id}')

    def add_document(self, collection_name, data):
        """Add a new document to the specified collection."""
        return self.collection(collection_name).add(data)

    def get_document(self, collection_name, document_id):
        """Get the data for a specific document."""
        doc_ref = self.document(collection_name, document_id)
        return doc_ref.get().to_dict()

    def get_documents(self, collection_name, limit=None, order_by=None, order_direction=None):
        """Get multiple documents from a collection."""
        query = self.collection(collection_name)

        if limit is not None:
            query = query.limit(limit)

        if order_by is not None and order_direction is not None:
            query = query.order_by(order_by, order_direction)

        snapshots = query.stream()
        return [doc.to_dict() for doc in snapshots]

    def update_document(self, collection_name, document_id, data):
        """Update existing document."""
        doc_ref = self.document(collection_name, document_id)
        return doc_ref.update(data)

    def delete_document(self, collection_name, document_id):
        """Delete a document from the database."""
        doc_ref = self.document(collection_name, document_id)
        return doc_ref.delete()
    
from flask import Flask
from flask_firestore import Firestore

app = Flask(__name__)
app.config['FIRESTORE_SETTINGS'] = {
    'project_id': 'your-project-id',
    'database_url': 'your-firestore-database-url'
}

firestore = Firestore(app)

class User(object):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

# Now, use the FirestoreDBWrapper class
db = FirestoreDBWrapper(app)

@app.route('/add_user', methods=['POST'])
def add_user():
    user_data = request.get_json()
    new_user = User(**user_data)
    collection_name = 'users'
    return db.add_document(collection_name, new_user.__dict__)

@app.route('/get_users')
def get_all_users():
    collection_name = 'users'
    users = db.get_documents(collection_name)
    return jsonify(users)