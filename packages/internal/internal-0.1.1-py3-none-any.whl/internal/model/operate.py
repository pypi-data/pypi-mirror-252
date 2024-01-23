from typing import Optional

from src.internal.model.base_model import InternalBaseModel


class Operate(InternalBaseModel):
    add: Optional[dict] = None
    remove: Optional[dict] = None
    change: Optional[dict] = None
