from fastapi import FastAPI, HTTPException, Query, APIRouter, Body
from typing import Dict
from botrun_ask_folder.models.collection_status import CollectionStatus
from botrun_ask_folder.stores.collection_status_fs_store import CollectionStatusFsStore

collection_status_api_router = APIRouter(
    prefix="/botrun_ask_folder", tags=["botrun_ask_folder"]
)


def get_collection_status_store() -> CollectionStatusFsStore:
    return CollectionStatusFsStore()


@collection_status_api_router.post("/init_collection_status")
async def init_collection_status(collection_status: CollectionStatus = Body(...)):
    try:
        store = get_collection_status_store()
        await store.init_collection_status(collection_status)
        return {
            "message": "Collection status initialized successfully",
            "collection_status": collection_status,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error initializing collection status: {str(e)}"
        )


@collection_status_api_router.get("/get_collection_status/{collection_id}")
async def get_collection_status(collection_id: str):
    try:
        store = get_collection_status_store()
        collection_status = await store.get_item(collection_id)
        if collection_status is None:
            raise HTTPException(status_code=404, detail="Collection status not found")
        return collection_status
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving collection status: {str(e)}"
        )
