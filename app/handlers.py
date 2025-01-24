import asyncio

from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from qr_code.qrcode_generator import qr_generate
from data.colors_data import colors, max_value_of_border, values_of_ord

router = Router()

class States(StatesGroup):
    fill_color = State()
    back_color = State()
    border = State()
    link = State()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Добро пожаловать в QRcode Generator. Чтобы посмотреть список команд, напишите /help")

@router.message(Command('help'))
async def help(message: Message):
    await message.answer('''/start - запуск бота
/help - список команд бота
/generate - сгенерировать qr код''')


@router.message(Command('generate'))
async def generate(message: Message, state: FSMContext):
    await state.set_state(States.fill_color)
    await message.answer('Enter a color of cipter for your qrcode')


@router.message(States.fill_color)
async def get_fill_color(message: Message, state: FSMContext):
    if message.text.startswith("rgb(") and message.text.endswith(")"):
        await state.set_state(States.back_color)
        await message.answer('Enter a color of background for your qrcode')
        await state.update_data(fill_color=message.text)
    elif message.text not in colors:
        await message.answer(
            "This color is not in my database, pls try to enter your color in rgb format")
    else:
        await state.set_state(States.back_color)
        await message.answer('Enter a color of background for your qrcode')
        await state.update_data(fill_color=message.text)

@router.message(States.back_color)
async def get_back_color(message: Message, state: FSMContext):
    if message.text.startswith("rgb(") and message.text.endswith(")"):
        await state.set_state(States.border)
        await message.answer('Enter a width of border for your qrcode (example: 4)')
        await state.update_data(back_color=message.text)
    elif message.text not in colors:
        await message.answer(
            "This color is not in my database, pls try to enter your color in rgb format")
    else:
        await state.set_state(States.border)
        await message.answer('Enter a width of border for your qrcode (example: 4)')
        await state.update_data(back_color=message.text)

@router.message(States.border)
async def get_border(message: Message, state: FSMContext):

    for i in message.text:
        if ord(i) not in values_of_ord:
            await message.answer("You have entered incorrect symbol")
            break
    if int(message.text) > max_value_of_border:
        await message.answer("Max value of border is 10")
    else:
        await state.update_data(border=message.text)
        await state.set_state(States.link)
        await message.answer("Enter a link for your qrcode")


@router.message(States.link)
async def get_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    await message.answer("Generation...")
    await asyncio.sleep(4)
    qr_generate(data["border"], data["fill_color"], data["back_color"], data["link"])
    qrc = FSInputFile('qr_code.png')
    await message.answer("Your qrcode has been succefully generated")
    await message.answer_photo(qrc)
    await state.clear()