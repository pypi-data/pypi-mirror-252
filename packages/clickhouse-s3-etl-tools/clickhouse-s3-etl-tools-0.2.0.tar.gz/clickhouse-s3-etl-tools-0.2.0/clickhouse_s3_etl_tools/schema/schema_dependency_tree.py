from typing import Optional
from pydantic import BaseModel


class DependencyTreeConfig(BaseModel):
    CH_URL: str
    DATABASES: str
    FILE_OUTPUT: Optional[str] = None
    EXCLUDED_DATABASES: Optional[str] = None
    LOG_LEVEL: Optional[str] = "INFO"
