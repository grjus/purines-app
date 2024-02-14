""" Create command"""

from pydantic import BaseModel


class AddProductCommand(BaseModel):
    name: str
    value: int
    group_uuid: str
