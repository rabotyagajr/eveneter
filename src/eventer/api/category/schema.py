from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    category_name: Optional[str] = Field(None, max_length=255)
    
class CategoryRead(CategoryBase):
    id: int