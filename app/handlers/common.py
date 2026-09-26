from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()

@router.message(Command("id"))
async def show_id(message: Message):
    await message.answer(str(message.from_user.id))

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Бот работает")

