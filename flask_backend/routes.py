from flask import jsonify, request
from datetime import datetime

from app import app
from database import *

@app.route('/')
def index():
    return 'Hello World'

@app.route('/documents', methods=['GET'])
def get_documents():
    documents = db.collection('testFlask').get()
    document_data = [{'id': doc.id, **doc.to_dict()} for doc in documents]
    return jsonify(document_data)

@app.route('/documents', methods=['POST'])
def create_document():
    data = request.get_json()
    data['posted_at'] = datetime.now().isoformat()
    _ , doc_ref = db.collection('testFlask').add(data)
    return jsonify({"message": "Document created successfully", "document_id": doc_ref.id}), 201
                  

@app.route('/documents/<document_id>', methods=['PUT'])
def update_document(document_id):
    data = request.get_json()
    db.collection('testFlask').document(document_id).update(data)
    return jsonify({"message": "Document updated successfully"}), 200

@app.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    db.collection('testFlask').document(document_id).delete()
    return jsonify({"message": "Document deleted successfully"}), 200