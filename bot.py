import json
import io
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from main import check_vacancy
from config import TOKEN, user_id

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    buttons = (
        'All jobs', 'New jobs'
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer("Jobs bot", reply_markup=keyboard)


@dp.message_handler(Text("All jobs"))
async def all_jobs(message: types.Message):
    with io.open("new_jobs.json", encoding="utf-8") as file:
        jobs = json.load(file)

    for key, value in sorted(jobs.items()):
        jobs_response = f"{value['link']}"

        await message.answer(jobs_response)


@dp.message_handler(Text("New jobs"))
async def get_new_vacancy(message: types.Message):
    fresh_jobs = check_vacancy()

    if len(fresh_jobs) >= 1:
        for key, value in sorted(fresh_jobs.items()):
            jobs_response = f"{value['link']}"

        await message.answer(jobs_response)

    else:
        await message.answer("No new vacancies")

    await asyncio.sleep(604800)


async def check_week_jobs():
    while True:
        fresh_jobs = check_vacancy()
        if len(fresh_jobs) >= 1:
            for key, value in sorted(fresh_jobs.items()):
                jobs_response = f"{value['link']}"

                # your user_id
                await bot.send_message(user_id, fresh_jobs, disable_notification=True)
        else:
            await bot.send_message("No new vacancies")


if __name__ == '__main__':
    executor.start_polling(dp)
