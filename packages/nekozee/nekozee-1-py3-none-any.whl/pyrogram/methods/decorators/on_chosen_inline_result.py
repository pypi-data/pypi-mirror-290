from typing import Callable, Optional, Union

import pyrogram
from pyrogram.filters import Filter


class OnChosenInlineResult:
    def on_chosen_inline_result(
        self: Union["OnChosenInlineResult", Filter, None] = None,
        filters: Optional[Filter] = None,
        group: int = 0,
    ) -> Callable:

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.ChosenInlineResultHandler(func, filters), group
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.ChosenInlineResultHandler(func, self),
                        group if filters is None else filters,
                    )
                )

            return func

        return decorator
