from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(Command("id"))
async def show_id(message: Message):
    await message.answer(str(message.from_user.id))


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Добро пожаловать в BloomFlow 🌸", reply_markup=0)


# Обработчик команды /cancel
@router.message(Command("cancel"))
@router.message(F.text == "Отмена")
async def cancel_command(message: Message):
    await message.answer(
        "Добро пожаловать в BloomFlow 🌸",
        reply_markup=0,
    )


# Обработчик непонятных сообщений
@router.message()
async def unknown_message(message: Message):

    await message.answer(
        "Я не понимаю это сообщение.",
        reply_markup=0,
    )
