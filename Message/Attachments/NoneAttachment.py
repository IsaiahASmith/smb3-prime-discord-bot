from typing import Optional, List

from discord import Message, File

from Message.Attachments.Attachment import Attachment


class NoneAttachment(Attachment):
    """Creates attachments from a message"""

    def __init__(self, message: Message):
        self.message = message

    @property
    def file(self) -> Optional[File]:
        return None

    @property
    def files(self) -> Optional[List[File]]:
        return None
