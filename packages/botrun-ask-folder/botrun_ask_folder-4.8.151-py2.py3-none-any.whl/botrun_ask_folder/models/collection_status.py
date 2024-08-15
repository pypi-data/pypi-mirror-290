from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from .collection_item import CollectionItem


class CollectionStatusEnum(str, Enum):
    """
    Enumeration of possible collection statuses.
    """

    PROCESSING = "PROCESSING"
    DONE = "DONE"


class CollectionStatus(BaseModel):
    """
    Represents the status of a collection.

    Attributes:
        id (str): Unique identifier for the collection.
        status (CollectionStatusEnum): Current status of the collection.
        items (List[CollectionItem]): List of items in the collection.
    """

    id: str = Field(..., description="Unique identifier for the collection")
    status: CollectionStatusEnum = Field(
        ..., description="Current status of the collection"
    )
    items: List[CollectionItem] = Field(
        default_factory=list, description="List of items in the collection"
    )

    @classmethod
    def model_validate_json(cls, json_data: str) -> "CollectionStatus":
        """
        Create a CollectionStatus instance from a JSON string.

        Args:
            json_data (str): JSON string representing a CollectionStatus.

        Returns:
            CollectionStatus: An instance of CollectionStatus.
        """
        return super().model_validate_json(json_data)

    def model_dump_json(self, **kwargs) -> str:
        """
        Convert the CollectionStatus instance to a JSON string.

        Returns:
            str: JSON representation of the CollectionStatus.
        """
        return super().model_dump_json(**kwargs)


# Example usage:
# json_data = '{"id": "collection123", "status": "PROCESSING", "items": [...]}'
# collection_status = CollectionStatus.model_validate_json(json_data)
# json_output = collection_status.model_dump_json()
# print(collection_status.status)  # Output: CollectionStatusEnum.PROCESSING
# print(collection_status.status == CollectionStatusEnum.PROCESSING)  # Output: True
