
from aiogram.types import Message
from aiogram.filters import BaseFilter
from config_data.config import get_admin_ids


admin_chat_ids: list[int] = get_admin_ids(None)


class IsAdminChat(BaseFilter):
    def __init__(self) -> None:
        self.admin_chat_ids: list[int] = admin_chat_ids

    async def __call__(self, msg: Message) -> bool:
        return msg.chat.id in self.admin_chat_ids
