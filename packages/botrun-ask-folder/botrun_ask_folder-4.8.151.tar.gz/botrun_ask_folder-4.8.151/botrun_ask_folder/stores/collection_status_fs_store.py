from botrun_ask_folder.models.collection_status import CollectionStatus
from botrun_ask_folder.stores.collection_status_store import CollectionStatusStore
from google.cloud import firestore
from google.oauth2 import service_account
import os


class CollectionStatusFsStore(CollectionStatusStore):
    """
    Firestore實作的 CollectionStatusStore
    """

    def __init__(self):
        google_service_account_key_path = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
            "/app/keys/scoop-386004-d22d99a7afd9.json",
        )
        credentials = service_account.Credentials.from_service_account_file(
            google_service_account_key_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        db = firestore.Client(credentials=credentials)
        self.collection = db.collection("collection-status")

    async def get_item(self, item_id: str):
        # Implement Firestore get logic
        pass

    async def init_collection_status(self, item: CollectionStatus):
        doc_ref = self.collection.document(item.id)
        doc_ref.set(item.model_dump())
        return item
