from abc import ABC, abstractmethod

from botrun_ask_folder.models.collection_status import CollectionStatus


class CollectionStatusStore(ABC):
    @abstractmethod
    async def get_item(self, item_id: str):
        pass

    @abstractmethod
    async def init_collection_status(self, item: CollectionStatus):
        pass
