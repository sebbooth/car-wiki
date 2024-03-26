import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

class FirestoreDBWrapper:
    def __init__(self):
        self.app = firebase_admin.initialize_app(credentials.Certificate("./.env/creds.json"))
        self.db = firestore.client()

    def collection(self, collection_name):
        return self.db.collection(collection_name)

    def add_document(self, collection_name, data):
        now = datetime.now().isoformat()
        document = dict(data)
        document["_document_changes"]=[
                {
                    "user_id": "system",
                    "datetime": now,
                    "data": data
                }
            ]
        print(document)
        return self.collection(collection_name).add(document)

    def update_document(self, collection_name, document_id, data):
        now = datetime.now().isoformat()
        doc_ref = self.document(collection_name, document_id)
        document = dict(data)
        prev_document = doc_ref.get().to_dict()
        changes = prev_document["_document_changes"]
        changes.append({
                    "user_id": "system",
                    "datetime": now,
                    "data": data
                })
        document["_document_changes"] = changes

        return doc_ref.update(document)
    
    def query_documents(self, collection_name, query_rules):
        query = self.collection(collection_name)

        for key, value in query_rules.items():
            if key == "order_by":
                field_name, direction = value
                direction = firestore.Query.ASCENDING if direction == "ASCENDING" else firestore.Query.DESCENDING
                query = query.order_by(field_name, direction=direction)
            elif key == "limit":
                query = query.limit(value)
            else:
                for operator, num in value.items():
                    query = query.where(filter=firestore.FieldFilter(key, operator, num))

        snapshots = query.stream()
        return [{'id': doc.id, **doc.to_dict()} for doc in snapshots]
    
    def document(self, collection_name, document_id):
        return self.db.collection(collection_name).document(document_id)

    def get_document(self, collection_name, document_id):
        doc_ref = self.document(collection_name, document_id)
        return doc_ref.get().to_dict()

    def delete_document(self, collection_name, document_id):
        doc_ref = self.document(collection_name, document_id)
        if (doc_ref.get().exists):
            return doc_ref.delete()
        else:
            return False