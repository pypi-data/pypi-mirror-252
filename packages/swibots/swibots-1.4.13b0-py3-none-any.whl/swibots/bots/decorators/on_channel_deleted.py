from typing import Callable, Optional
import swibots
from swibots.bots.filters.filter import Filter


class OnChannelDeleted:
    def on_channel_created(
        self: "swibots.BotApp" = None, filter: Optional[Filter] = None
    ) -> Callable:
        """Decorator for handling channel creations."""

        def decorator(func: Callable) -> Callable:
            if isinstance(self, swibots.BotApp):
                self.add_handler(
                    swibots.bots.handlers.ChannelDeletedHandler(func, filter)
                )

            return func

        return decorator
