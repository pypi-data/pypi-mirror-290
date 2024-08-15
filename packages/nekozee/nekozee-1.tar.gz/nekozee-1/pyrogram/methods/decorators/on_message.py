from typing import Callable, Optional, Union

import pyrogram
from pyrogram.filters import Filter


class OnMessage:
    def on_message(
        self: Union["OnMessage", Filter, None] = None,
        filters: Optional[Filter] = None,
        group: int = 0,
    ) -> Callable:

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(pyrogram.handlers.MessageHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.MessageHandler(func, self),
                        group if filters is None else filters,
                    )
                )

            return func

        return decorator
