import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("./.env/creds.json")
fb_app = firebase_admin.initialize_app(cred)
db = firestore.client()

class FirestoreDBWrapper():
    def __init__(self, database_url):
        self.database_url = database_url
        firebase_admin.initialize_app(database_url)
        self.db = firestore.client()

    def collection(self, collection_name):
        return self.db.collection(collection_name)

    def document(self, collection_name, document_id):
        return self.db.collection(collection_name).document(document_id)

    def get_document(self, collection_name, document_id):
        doc = self.document(collection_name, document_id)
        try:
            return doc.get().to_dict()
        except firestore.NotFoundError:
            return None

    def add_document(self, collection_name, data):
        doc_ref = self.document(collection_name, data.get('id', None))
        return doc_ref.set(data)

    def update_document(self, collection_name, document_id, data):
        doc_ref = self.document(collection_name, document_id)
        return doc_ref.update(data)

    def delete_document(self, collection_name, document_id):
        doc_ref = self.document(collection_name, document_id)
        return doc_ref.delete()

    def list_documents(self, collection_name):
        query = self.collection(collection_name).order_by('__name__')
        docs = query.get()
        return [doc.to_dict() for doc in docs]


        

app = Flask(__name__)

firestore_db = FirestoreDBWrapper('YOUR_FIRESTORE_DATABASE_URL')

@app.route('/')
def home():
    posts = firestore_db.list_documents('posts')
    return render_template('index.html', posts=posts)

@app.route('/add_post', methods=['POST'])
def add_post():
    post_data = request.form.to_dict()
    if not post_data:
        return render_template('error.html', message='Invalid data')

    result = firestore_db.add_document('posts', post_data)
    if result:
        return render_template('success.html', message='Post added successfully')
    else:
        return render_template('error.html', message='Error adding post')

if __name__ == '__main__':
    app.run(debug=True)
                  