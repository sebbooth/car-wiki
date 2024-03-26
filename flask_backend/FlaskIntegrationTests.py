import pytest
from flask.testing import FlaskClient
from datetime import datetime

from app import *

def create_documents(documents):
    document_ids = []
    for document in documents:
        _, doc_ref = db.add_document("testFlask", document)
        document_ids.append(doc_ref.id)
    return document_ids

def cleanup_documents(document_ids):
    for document_id in document_ids:
        db.delete_document("testFlask", document_id)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def document_id(client: FlaskClient):
    # Prepare test data
    user_id = "test_user"
    data = {"title": "Test Document", "content": "This is a test document"}

    # Make POST request to /documents/<user_id>
    response = client.post(f"/documents/{user_id}", json=data)

    # Return the document id
    return response.get_json()["document_id"]

def test_create_document(client: FlaskClient):
    # Prepare test data
    user_id = "test_user"
    data = {"title": "Test Document", "content": "This is a test document"}

    # Make POST request to /documents/<user_id>
    response = client.post(f"/documents/{user_id}", json=data)

    # Assert response status code is 201
    assert response.status_code == 201

    # Assert response data
    response_data = response.get_json()
    assert response_data["message"] == "Document created successfully"
    assert response_data["document_id"] is not None
    assert response_data["date_added"] is not None

    # Verify document was added to Firestore
    doc_ref = db.collection("testFlask").document(response_data["document_id"])
    doc = doc_ref.get()
    assert doc.exists
    assert doc.get("title") == data["title"]
    assert doc.get("content") == data["content"]

    data["posted_at"] = doc.get("posted_at")
    
    assert doc.get("_document_changes") == [
        {
            "user_id": "system",
            "datetime": doc.get("_document_changes")[0]["datetime"],
            "data": data
        }
    ]

    db.delete_document("testFlask", response_data["document_id"])

def test_delete_document(client: FlaskClient, document_id: str):
    # Make DELETE request to /documents/<document_id>
    response = client.delete(f"/documents/{document_id}")

    # Assert response status code is 201
    assert response.status_code == 201

    # Assert response data
    response_data = response.get_json()
    assert response_data["message"] == "Document deleted successfully"
    assert response_data["document_id"] == document_id
    assert response_data["date_deleted"] is not None

    # Verify document was deleted from Firestore
    doc_ref = db.collection("testFlask").document(document_id)
    doc = doc_ref.get()
    assert not doc.exists
                  
def test_delete_document_not_found(client: FlaskClient):
    # Make DELETE request to /documents/<document_id>
    response = client.delete("/documents/non_existent_document")

    # Assert response status code is 404
    assert response.status_code == 404

    # Assert response data
    response_data = response.get_json()
    assert response_data["message"] == "Document not found"
    assert response_data["document_id"] == "non_existent_document"

def test_update_document(client: FlaskClient, document_id: str):
    # Prepare test data
    user_id = "test_user"
    data = {"title": "Updated Test Document", "content": "This is an updated test document"}

    # Make PUT request to /documents/<document_id>/<user_id>
    response = client.put(f"/documents/{document_id}/{user_id}", json=data)

    # Assert response status code is 201
    assert response.status_code == 201

    # Assert response data
    response_data = response.get_json()
    assert response_data["message"] == "Document updated successfully"
    assert response_data["document_id"] == document_id

    # Verify document was updated in Firestore
    doc_ref = db.collection("testFlask").document(document_id)
    doc = doc_ref.get()
    assert doc.exists
    assert doc.get("title") == data["title"]
    assert doc.get("content") == data["content"]

    prev_document = doc_ref.get().to_dict()
    changes = prev_document["_document_changes"]
    assert changes[-1]["user_id"] == "system"
    assert changes[-1]["datetime"] is not None
    assert changes[-1]["data"] == data

    db.delete_document("testFlask", document_id)

def test_query_documents_order_by(client: FlaskClient):
    # Prepare test data
    documents = [
        {"number": 1, "name": "Document 1"},
        {"number": 2, "name": "Document 2"},
        {"number": 3, "name": "Document 3"}
    ]
    document_ids = create_documents(documents)

    # Prepare query rules
    query_rules = {
        "order_by": ["number", "ASCENDING"]
    }

    # Make GET request to /documents
    response = client.get("/documents", json=query_rules)

    # Assert response status code is 200
    assert response.status_code == 200

    # Assert response data
    response_data = response.get_json()
    
    assert response_data == sorted(response_data, key=lambda x: x["number"], reverse=False)

    cleanup_documents(document_ids)

def test_query_documents_limit(client: FlaskClient):
    # Prepare test data
    documents = [
        {"number": 1, "name": "Document 1"},
        {"number": 2, "name": "Document 2"},
        {"number": 3, "name": "Document 3"}
    ]
    document_ids = create_documents(documents)

    # Prepare query rules
    query_rules = {
        "limit": 2
    }

    # Make GET request to /documents
    response = client.get("/documents", json=query_rules)

    # Assert response status code is 200
    assert response.status_code == 200

    # Assert response data
    response_data = response.get_json()
    assert len(response_data) <= 2

    cleanup_documents(document_ids)

def test_query_documents_field_filter(client: FlaskClient):
    # Prepare test data
    documents = [
        {"number": 1, "name": "Document 1"},
        {"number": 2, "name": "Document 2"},
        {"number": 3, "name": "Document 3"}
    ]
    document_ids = create_documents(documents)


    # Prepare query rules
    query_rules = {
        "number": {
            ">=": 2
        }
    }

    # Make GET request to /documents
    response = client.get("/documents", json=query_rules)

    # Assert response status code is 200
    assert response.status_code == 200

    # Assert response data
    response_data = response.get_json()
    for data in response_data:
        assert data["number"] >= 2

    cleanup_documents(document_ids)
