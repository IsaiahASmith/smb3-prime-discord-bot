from cogs.core import setup as setup_core
from cogs.log import setup as setup_log
from cogs.sender import setup as setup_sender
from cogs.options import setup as setup_options
from cogs.info import setup as setup_info
from cogs.channel_manager import setup as channel_manager_setup
from cogs.translate import setup as setup_translate
from cogs.security import setup as setup_security

COGS = [
    (setup_core, "core"),
    (setup_log, "log"),
    (setup_sender, "sender"),
    (setup_options, "options"),
    (setup_info, "info"),
    (channel_manager_setup, "channel_manager"),
    (setup_translate, "translate"),
    (setup_security, "security"),
]
