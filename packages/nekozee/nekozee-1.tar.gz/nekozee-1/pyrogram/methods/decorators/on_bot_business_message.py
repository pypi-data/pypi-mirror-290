from typing import Callable

import pyrogram
from pyrogram.filters import Filter


class OnBotBusinessMessage:
    def on_bot_business_message(self=None, filters=None, group: int = 0) -> Callable:

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.BotBusinessMessageHandler(func, filters), group
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.BotBusinessMessageHandler(func, self),
                        group if filters is None else filters,
                    )
                )

            return func

        return decorator
