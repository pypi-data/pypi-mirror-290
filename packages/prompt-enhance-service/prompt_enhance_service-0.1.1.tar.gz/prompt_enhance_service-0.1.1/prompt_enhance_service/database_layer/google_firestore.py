from google.cloud import firestore
from database_layer.database_connection import DatabaseConnection

class FirestoreConnection(DatabaseConnection):
    def __init__(self, project_id=None, database_id=None):
        self.client = None
        self.project_id = project_id
        self.database_id = database_id

    def connect(self):
        if self.project_id:
            self.client = firestore.Client(project=self.project_id, database=self.database_id)
        else:
            self.client = firestore.Client(database=self.database_id)

    def close(self):
        # Firestore does not require an explicit close operation
        self.client = None

    def execute_query(self, **kwargs):
        if not self.client:
            raise Exception("Firestore client is not connected.")
        
        collection_name = kwargs.get('collection_name')
        field_name = kwargs.get('field_name')
        field_value = kwargs.get('field_value')
        
        if not collection_name or not field_name or not field_value:
            raise ValueError("Missing collection_name, field_name, or field_value in query parameters")
        
        collection_ref = self.client.collection(collection_name)
        query = collection_ref.where(field_name, '==', field_value)
        docs = query.stream()

        results = []
        for doc in docs:
            results.append(doc.to_dict())

        return results
    
    def add_document(self, collection_name, data):
        if not self.client:
            raise Exception("Firestore client is not connected.")
        
        if not collection_name or not data:
            raise ValueError("Missing collection_name or data in add_document parameters")
        
        collection_ref = self.client.collection(collection_name)
        try:
            collection_ref.add(data)
            return True
        except Exception as e:
            raise Exception(f"Error adding document to Firestore: {e}")

    def document_exists(self, collection_name, field_name, field_value):
        """
        Checks if a document with a specific field value exists in the collection.
        """
        results = self.execute_query(
            collection_name=collection_name,
            field_name=field_name,
            field_value=field_value
        )
        return len(results) > 0
