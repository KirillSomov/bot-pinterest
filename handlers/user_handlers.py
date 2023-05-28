
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.methods import SendPhoto
import re
import requests
from config_data.config import get_target_chat_id
from lexicon.lexicon import LEXICON_RU
from filters.is_admin import IsAdminChat


target_chat_id: int = get_target_chat_id(None)


# router init
router: Router = Router()


# START
@router.message(CommandStart())
async def process_start_command(msg: Message):
    await msg.answer(text=LEXICON_RU["/start"])


# HELP
@router.message(Command(commands="help"))
async def process_help_command(msg: Message):
    await msg.answer(text=LEXICON_RU["/help"])


share_link_regex = r"https.*"
pin_url_regex = r"http.*?(?=/sent)"
source_raw_regex = r"\"orig\".*?https.*?\""
source_regex = r"https.*(?=\")"

# send pinterest pin
@router.message(IsAdminChat())
async def process_msg(msg: Message):
    try:
        share_url = (re.findall(share_link_regex, msg.text))[0]
        pin_url = (re.findall(pin_url_regex, requests.get(share_url).url))[0]
        source_raw = (re.findall(source_raw_regex, requests.get(pin_url).text))[0]
        source = (re.findall(source_regex, source_raw))[0]
        await SendPhoto(chat_id=target_chat_id, photo=source)
    except:
        await msg.answer(text=f"wtf?...")
