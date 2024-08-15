from datetime import datetime
from pathlib import Path
from typing import List, Union

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

import jrsync.conf as settings
from jrsync.utils import str_parser
from jrsync.utils import str_validator


class Jsync(BaseModel):
    date_to_sync: datetime
    src_host: str = Field(None)
    dst_host: str = Field(None)
    source_dir: Path
    dest_dir: Path
    file_to_sync: List[str] | str = Field([settings.ALL_DIRECTORY])
    day: str = Field("*")

    @field_validator("src_host", "dst_host", mode="before")
    @classmethod
    def check_address(cls, v):
        if not str_validator.is_valid_address(v):
            raise ValueError(f"Invalid address: {v}")

    @field_validator("source_dir", "dest_dir", mode="before")
    @classmethod
    def resolve_path(cls, v: str, info: ValidationInfo) -> Path:
        """Replace placeholders and global variables"""
        resolved_str_path = str_parser.resolve_str(v, info.data["date_to_sync"])
        return Path(resolved_str_path)

    @field_validator("file_to_sync", mode="before")
    @classmethod
    def resolve_filenames(cls, v: str, info: ValidationInfo) -> List[str]:
        """Replace placeholders and global variables"""
        date = info.data["date_to_sync"]
        return [str_parser.resolve_str(f, date) for f in v]

    def override_hosts(
        self, src_host: Union[str, None] = None, dst_host: Union[str, None] = None
    ):
        """Method to override src_host and dst_host."""
        if src_host is not None:
            self.src_host = src_host
        if dst_host is not None:
            self.dst_host = dst_host

    def get_files_to_sync(self, include_not_exists=False) -> List[str]:
        """Return the list of files to sync, filtering out non-existent files if src_host is None."""
        if self.src_host is None:
            # Filter files to include only existing ones in source_dir
            exist = [f for f in self.file_to_sync if (self.source_dir / f).exists()]
            not_exists = [f for f in self.file_to_sync if f not in exist]

            if include_not_exists:
                exist.extend(not_exists)

            return exist
        else:
            return self.file_to_sync

    def get_src(self) -> str:
        if self.src_host is None:
            return self.source_dir.as_posix()

        return f"{self.src_host}:{self.source_dir.as_posix()}"

    def get_dst(self) -> str:
        if self.dst_host is None:
            return self.dest_dir.as_posix()

        return f"{self.dst_host}:{self.dest_dir.as_posix()}"
