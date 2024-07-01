from contextlib import suppress
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest
from telethon.errors.rpcerrorlist import (
    UserAlreadyParticipantError,
    FloodWaitError,
    HistoryGetFailedError,
    InviteHashEmptyError,
    ChannelInvalidError,
    ChannelPrivateError,
    InviteHashExpiredError,
    ChatAdminRequiredError,
    UsernameInvalidError,
)

async def give_chat_id(client: TelegramClient, group):
    if "+" in group:
        group = group.replace("+", "joinchat/")

    private_prefix = "https://t.me/joinchat/"
    non_private_prefix = "https://t.me/"

    group = group if group.startswith(private_prefix) else group.replace(non_private_prefix, "@")

    try:
        if group.startswith('@'):
            await join_channel(client, group)
        else:
            chat_id = await get_chat_id(client, group)
            if chat_id:
                return chat_id
    except (HistoryGetFailedError, FloodWaitError, UserAlreadyParticipantError):
        pass
    except (
        ChannelInvalidError,
        ChannelPrivateError,
        InviteHashExpiredError,
        InviteHashEmptyError,
        ChatAdminRequiredError,
        ValueError,
        UsernameInvalidError,
    ):
        return None

    return group


async def join_channel(client, group):
    await client(JoinChannelRequest(channel=group))

async def get_chat_id(client, group):
    chat_hash = group.split('/')[-1]

    if chat_info := await client(CheckChatInviteRequest(chat_hash)):
        with suppress(Exception):
            return await client.get_peer_id(chat_info.chat)

    await client(ImportChatInviteRequest(chat_hash))
    return await client.get_peer_id(group)
