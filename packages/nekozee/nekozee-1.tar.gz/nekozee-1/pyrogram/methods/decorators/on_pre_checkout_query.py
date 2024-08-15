from typing import Callable, Optional, Union

import pyrogram
from pyrogram.filters import Filter


class OnPreCheckoutQuery:
    def on_pre_checkout_query(
        self: Union["OnPreCheckoutQuery", Filter, None] = None,
        filters: Optional[Filter] = None,
        group: int = 0,
    ) -> Callable:

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.PreCheckoutQueryHandler(func, filters), group
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.PreCheckoutQueryHandler(func, self),
                        group if filters is None else filters,
                    )
                )

            return func

        return decorator
