from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CollectionItem(BaseModel):
    """
    Represents an item in a collection, typically a file or folder.

    Attributes:
        id (str): Google file id
        name (str): 檔案名字，如果是處理過後的檔案，會存split過後的檔名
        mimeType (str): MIME type of the item.
        modifiedTime (datetime): Last modification time of the item.
        size (str): Size of the item, typically in bytes.
        parent (str): 在 Google Drive 上的 parent
        path (str): 在 Google Drive 上的 parent Full path
        gen_page_imgs 針對這個檔案有沒有產截圖
        ori_file_name (Optional[str]): 這個檔案是從哪個檔案 split 來的
        page_number (Optional[int]): split 過後它是屬於第幾頁
    """

    id: str
    name: str
    mimeType: str
    modifiedTime: datetime
    size: str
    parent: str
    path: str
    gen_page_imgs: Optional[bool] = None
    ori_file_name: Optional[str] = None
    page_number: Optional[int] = None

    @classmethod
    def from_json(cls, json_str: str) -> "CollectionItem":
        return cls.model_validate_json(json_str)

    def to_json(self) -> str:
        return self.model_dump_json(exclude_none=True)

    @classmethod
    def from_list(cls, item_list: List[dict]) -> List["CollectionItem"]:
        return [cls(**item) for item in item_list]

    @classmethod
    def to_list(cls, items: List["CollectionItem"]) -> List[dict]:
        return [item.model_dump(exclude_none=True) for item in items]


# Example usage:
# json_data = '{"id": "...", "name": "...", ...}'
# item = CollectionItem.from_json(json_data)
# json_output = item.to_json()
#
# item_list = [{"id": "...", "name": "...", ...}, ...]
# collection_items = CollectionItem.from_list(item_list)
# list_output = CollectionItem.to_list(collection_items)
