                    
import unittest
import requests

class TestFlaskAPI(unittest.TestCase):

    def test_index(self):
        response = requests.get('http://localhost:5000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Index Page')

    def test_hello(self):
        response = requests.get('http://localhost:5000/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hello, World')

    def test_get_documents(self):
        response = requests.get('http://localhost:5000/documents')
        self.assertEqual(response.status_code, 200)
        # Assuming there are no documents in the collection, the response should be an empty list
        # self.assertEqual(response.json(), [])

    def test_create_document(self):
        data = {'key': 'value'}
        response = requests.post('http://localhost:5000/documents', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Document created successfully"})

    def test_update_document(self):
        # Create a document first
        data = {'key': 'value'}
        response = requests.post('http://localhost:5000/documents', json=data)
        print(response.json())
        document_id = response.json()['id']

        # Then update the document
        updated_data = {'key': 'updated_value'}
        response = requests.put('http://localhost:5000/documents/{}'.format(document_id), json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Document updated successfully"})

    def test_delete_document(self):
        # Create a document first
        data = {'key': 'value'}
        response = requests.post('http://localhost:5000/documents', json=data)
        document_id = response.json()['id']

        # Then delete the document
        response = requests.delete('http://localhost:5000/documents/{}'.format(document_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Document deleted successfully"})

if __name__ == '__main__':
    unittest.main()