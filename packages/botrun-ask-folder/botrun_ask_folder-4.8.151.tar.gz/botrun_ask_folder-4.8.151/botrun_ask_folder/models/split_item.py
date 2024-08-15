from pydantic import BaseModel
from typing import Optional


class SplitItem(BaseModel):
    """
    Represents a split item from a collection item.

    Attributes:
        id (str): Unique identifier for the split item
        name (str): Name of the split item
        gen_page_imgs (Optional[bool]): Whether page images have been generated for this item
        ori_file_name (Optional[str]): Original file name this item was split from
        page_number (Optional[int]): Page number of this split item
    """

    id: str
    name: str
    gen_page_imgs: Optional[bool] = None
    ori_file_name: Optional[str] = None
    page_number: Optional[int] = None

    @classmethod
    def from_json(cls, json_str: str) -> "SplitItem":
        return cls.model_validate_json(json_str)

    def to_json(self) -> str:
        return self.model_dump_json(exclude_none=True)
