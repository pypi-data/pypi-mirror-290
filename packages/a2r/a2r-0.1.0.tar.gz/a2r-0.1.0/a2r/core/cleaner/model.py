import logging
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

logger = logging.getLogger("a2r")


class SafeRm(BaseModel):
    to_keep: int = Field(ge=0)
    reference_paths: List[Path]


class ConditionalRm(BaseModel):
    to_keep: int = Field(ge=0)
    expected_files: set[str] = Field([])


class ForceRm(BaseModel):
    to_keep: int = Field(ge=0)


class CleanPath(BaseModel):
    path: Path
    fmt: str
    safe: SafeRm = Field(None)
    conditional: ConditionalRm = Field(None)
    force: ForceRm = Field(None)

    @property
    def fmt(self) -> str:
        return self._fmt

    @property
    def safe_to_keep(self) -> int:
        return self.safe.to_keep

    @property
    def conditional_to_keep(self) -> int:
        return self.conditional.to_keep

    @property
    def force_to_keep(self) -> int:
        return self.force.to_keep

    @property
    def conditional_expected_files(self) -> set[str]:
        return self.conditional.expected_files

    @property
    def safe_reference_paths(self) -> List[Path]:
        return self.safe.reference_paths

    def force_clean_is_active(self):
        return self.force is not None

    def safe_clean_is_active(self):
        return self.safe is not None

    def conditional_clean_is_active(self):
        return self.conditional is not None
