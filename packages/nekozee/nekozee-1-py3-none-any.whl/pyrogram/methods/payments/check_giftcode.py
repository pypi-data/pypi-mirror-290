import re

import pyrogram
from pyrogram import raw, types


class CheckGiftCode:
    async def check_gift_code(
        self: "pyrogram.Client",
        link: str,
    ) -> "types.CheckedGiftCode":
        match = re.match(
            r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:giftcode/|\+))([\w-]+)$",
            link,
        )

        if match:
            slug = match.group(1)
        elif isinstance(link, str):
            slug = link
        else:
            raise ValueError("Invalid gift code link")

        r = await self.invoke(raw.functions.payments.CheckGiftCode(slug=slug))

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        return types.CheckedGiftCode._parse(self, r, users, chats)
