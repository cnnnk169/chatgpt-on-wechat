"""Simple WeChat bot extracted from the project.

This module exposes a minimal API similar to Python Wechaty.
"""

from typing import Callable, List

from lib import itchat
from lib.itchat.content import ATTACHMENT, NOTE, PICTURE, SHARING, TEXT, VOICE


class WeChatBot:
    """A lightweight wrapper around itchat with a Wechaty like interface."""

    def __init__(self):
        self._message_handlers: List[Callable] = []

    def on_message(self, func: Callable):
        """Register a message handler."""
        self._message_handlers.append(func)
        return func

    def _handle(self, msg):
        for handler in self._message_handlers:
            handler(msg)

    def start(self, hot_reload: bool = True):
        """Start the bot and begin listening for messages."""

        @itchat.msg_register([TEXT, VOICE, PICTURE, NOTE, ATTACHMENT, SHARING], isFriendChat=True, isGroupChat=True)
        def _(msg):
            self._handle(msg)

        itchat.auto_login(hotReload=hot_reload)
        itchat.run()

    def send_text(self, user: str, text: str):
        """Send a text message to a user or group."""
        itchat.send(text, toUserName=user)
