from re import S
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    first_name:str
    last_name:str
    age:int
    sex:Optional[str]=None
    
    