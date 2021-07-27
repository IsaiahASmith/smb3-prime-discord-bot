from typing import Set, Optional

from discord.ext.commands import Cog

from database import Channel, ChannelGroup

from Message.MessageCreator import MessageCopyCreator


class Sender(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_message_to_channel(self, channel: Channel, message_creator: MessageCopyCreator):
        """Sends a message through the embed creator to a channel"""
        await message_creator.post_message(client=self.bot, channel=channel)

    async def send_once(
            self,
            channel_groups: Set[ChannelGroup],
            message_creator: MessageCopyCreator,
            sent: Optional[Set[int]] = None
    ):
        """Sends a message to every channel in channel groups only once"""
        sent_channels = sent or set()
        for channel_group in channel_groups:
            for channel in channel_group.channels:
                if channel.id not in sent_channels:
                    await self.send_message_to_channel(channel, message_creator)
                    sent_channels.add(channel.id)


def setup(bot):
    cog = Sender(bot)
    bot.add_cog(cog)
    return cog
