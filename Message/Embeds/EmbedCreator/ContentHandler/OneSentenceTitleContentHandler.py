from nltk import sent_tokenize

from Message.Embeds.EmbedCreator.MetaMessage import MetaMessage

from Message.Embeds.EmbedCreator.ContentHandler.ContentHandler import ContentHandler


class OneSentenceTitleContentHandler(ContentHandler):
    """Takes the content from a message and divides it into the title and description"""

    def __init__(self, meta: MetaMessage):
        super().__init__(meta=meta)

        if len(meta.message.attachments) == 0:
            # This is often a conversation, so make it all the same.
            self._title = None
            self._description = meta.message.content
        else:
            tokens = sent_tokenize(meta.message.content)  # Convert the message to sentences
            self._title = tokens[0]
            self._description = ' '.join(tokens[1:]) if len(tokens) > 1 else None

    @property
    def title(self) -> str:
        """Returns the title of the embed"""
        return self._title

    @property
    def description(self) -> str:
        """Returns the description of the embed"""
        return self._description
