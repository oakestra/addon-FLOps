from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flops_manager.classes.base import FlOpsBaseClass


def get_matching_type(matching_caller_object: FlOpsBaseClass) -> str:
    return (type(matching_caller_object).__name__ if matching_caller_object else "") + " "
