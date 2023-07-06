from typing import Any

from aiogram.types import ContentType, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Group, Row, Start, SwitchTo
from aiogram_dialog.widgets.media import Media, StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from loguru import logger

from tele_gpt import utils
from tele_gpt.dialogs.admin import AdminSG
from tele_gpt.exceptions import OpenAIError
from tele_gpt.openai import get_response
from tele_gpt.states import MainSG, TranslateSG
from tele_gpt.utils import get_placeholder_image_url, is_admin


async def main_getter(dialog_manager: DialogManager, **kwargs: Any) -> dict:
    if not dialog_manager.event.from_user:
        raise AttributeError
    data = {
        "is_admin": await is_admin(dialog_manager.event.from_user.id),
        }
    if 'messages' in dialog_manager.dialog_data:
        if dialog_manager.dialog_data["messages"][-1]['role'] != 'system':
            data['last_message'] = dialog_manager.dialog_data["messages"][-1]['content']
        else:
            data['last_message'] = "Начинайте чат"
    return data

async def role_handler(
    message: Message, message_input: TextInput, manager: DialogManager, t
):
    if not message.text:
        return
    if 'messages' not in manager.dialog_data:
        manager.dialog_data["messages"] = list()
    manager.dialog_data["messages"].append({
        'role':'system',
        'content': message.text
    })
    await manager.switch_to(MainSG.get_message)

async def message_handler(
    message: Message, message_input: TextInput, manager: DialogManager, t
):
    if not message.text:
        return
    manager.dialog_data["messages"].append({
        'role':'user',
        'content': message.text
    })
    try:
        response = get_response(manager.dialog_data["messages"])
    except OpenAIError as e:
        logger.info("openaierror")
        del manager.dialog_data["messages"]
        await manager.switch_to(MainSG.main)
    else:
        manager.dialog_data["messages"].append(response)
        await manager.switch_to(MainSG.get_message)


index_dialog = Dialog(  # type: ignore
    Window(
        StaticMedia(
            url=Const(get_placeholder_image_url(text="Your ChatGPT 3.5")),
            type=ContentType.PHOTO,
        ),
        Const("Выберите роль:"),
        TextInput(id="role_input", on_success=role_handler),
        Start(
            id="btn_goto_admin_index",
            text=Const("Admin panel"),
            state=AdminSG.index,
            when="is_admin",
        ),
        getter=main_getter,
        state=MainSG.main,
    ),
    Window(
        Format("{last_message}"),
        TextInput(id="message_input", on_success=message_handler),
        getter=main_getter,
        state=MainSG.get_message,
    ),
)
