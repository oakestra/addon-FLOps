from typing import Optional

from pydantic import BaseModel


def get_matching_type(matching_caller_object: Optional[BaseModel]) -> str:
    return (type(matching_caller_object).__name__ if matching_caller_object else "") + " "
