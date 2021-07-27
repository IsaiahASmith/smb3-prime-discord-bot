from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from discord import File


class Attachment(ABC):
    """Provides the files to be attached to a message"""

    @property
    @abstractmethod
    def file(self) -> Optional[File]:
        """Provides a single file to be used as an attachment"""

    @property
    @abstractmethod
    def files(self) -> Optional[List[File]]:
        """Provides a series of files to be attached"""

    async def create_attachments(self) -> Tuple[Optional[File], Optional[List[File]]]:
        """Creates the files for the attachment"""
        return self.file, self.files
