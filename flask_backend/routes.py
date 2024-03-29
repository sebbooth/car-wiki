from flask import jsonify, request
from datetime import datetime

from app import app, fb_app
from database import *

db = FirestoreDBWrapper(fb_app)

@app.route('/documents', methods=['GET'])
def query_documents():
    query_rules = request.get_json()
    documents_data = db.query_documents('testFlask', query_rules)
    return jsonify(documents_data)

@app.route('/documents/<user_id>', methods=['POST'])
def create_document(user_id):
    data = request.get_json()
    data['posted_at'] = datetime.now().isoformat()
    date, doc_ref = db.add_document('testFlask', data)
    print(date)
    return jsonify({"message": "Document created successfully", "document_id": doc_ref.id, "date_added": date}), 201
                  
@app.route('/documents/<document_id>/<user_id>', methods=['PUT'])
def update_document(document_id, user_id):
    data = request.get_json()
    db.update_document("testFlask", document_id, data)
    return jsonify({"message": "Document updated successfully", "document_id": document_id}), 201

@app.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    date = db.delete_document("testFlask", document_id)
    if (date):
        return jsonify({"message": "Document deleted successfully", "document_id": document_id, "date_deleted": date}), 201
    else:
        return jsonify({"message": "Document not found", "document_id": document_id}), 404 
