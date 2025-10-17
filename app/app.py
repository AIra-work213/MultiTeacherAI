from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import os
import aiohttp
import json


bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


# --------------Вспомогательные команды--------------
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я твой мультимодальный учитель. Могу помочь ответить на ваши вопросы по содержимому документов и провести тестирование")

@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("""
Я помогу вам с обучением. Доступные опции:

/quest <ваш вопрос> - задать вопрос по содержимому загруженных документов
/test <тема> (опционально) - пройти тестирование по загруженным документам. Для выбора темы укажите ее через пробел после команды.
/topics - получить список доступных тем для тестирования на основе загруженных документов.

Загрузка документов возможна без команды. Отправьте файл без команды.
Поддерживаемые форматы: pdf, txt, docx.""")



# ------Обработка загруженных документов-------
@dp.message(F.document)
async def register_handler(message: Message):
    metadata = {
        "user_id": message.from_user.id,
        "file_id": message.document.file_id,
        "file_name": message.document.file_name,
        "file_size": message.document.file_size,
        "file_type": message.document.mime_type
    }
    document = message.document
    file = await bot.get_file(metadata["file_id"])

    data = aiohttp.FormData()
    data.add_field("metadata", json.dumps(metadata), content_type='application/json')
    data.add_field("file", await bot.download_file(file.file_path), filename=document.file_name)

    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post("http://server:8000/upload", data=data)
            res = await response.json()
    except Exception as e:
        await message.answer(f"Произошла ошибка при добавлении документа: {e}")
        return
    if not res.get("status", False):
        await message.answer("Произошла ошибка при добавлении документа. Неподдерживаемый формат файла. Доступные: pdf, txt, docx")
        return
    
    await message.answer("Документ успешно добавлен.")
    await message.answer(f"Имя документа: {res.get('file_name')}\n Тема: {res.get('topic')}\n ID темы: {res.get('topic_id')}")



# -------Обработка текстовых запросов-------
@dp.message(Command("quest"))
async def quest_handler(message: Message):
    user_id = message.from_user.id
    quest = message.text.split(" ", 1)
    if len(quest) < 2:
        await message.answer("Пожалуйста, задайте вопрос.")
        return
    
    quest = ' '.join(quest[1:])
    if len(quest) >= 4096:
        await message.answer("Ваш вопрос слишком длинный и был обрезан. Сократите его.")
        return
    await message.answer(f"Вы задали вопрос: {quest}")
    await message.answer("Обработка вашего запроса...")
    
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post("http://server:8000/quest", json={
                "user_id": user_id,
                "quest": quest
            })
            res = await response.json()
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке вашего запроса: {e}")
        return

    await message.answer(f"Ответ: {res.get('answer')}") 



# --------Проведение теста--------
@dp.message(Command("test"))
async def test_handler(message: Message):
    words = message.text.split(" ")
    if len(words) < 2:
        await message.answer("Тестирование будет проводиться по последнему загруженному файлу.")
        async with aiohttp.ClientSession() as session:
            response = await session.post("http://server:8000/test", json={"user_id": message.from_user.id})
            res = await response.json()
    else:
        topic = ' '.join(words[1:])
        async with aiohttp.ClientSession() as session:
            response = await session.post("http://server:8000/test", json={"user_id": message.from_user.id, "topic": topic})
            res = await response.json()
    
    if res.get('is_success') == False:
        await message.answer("Ошибка в выборе темы. Используйте /topics для получения списка доступных тем.")
        return
    questions = res.get('questions')
    answers = res.get('answers')

    await message.answer("Тестирование начато...")
    for q, ans in zip(questions, answers):
        await message.answer(f"Вопрос: {q}")

    # Здесь можно добавить логику для проведения теста

    await message.answer("Тестирование завершено.")


# --------Доступные темы для теста-------- вроде работает
@dp.message(Command("topics"))
async def topics_handler(message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post("http://server:8000/topics", json={"user_id": message.from_user.id})
            topics = await response.json()
    except Exception as e:
        await message.answer(f"Произошла ошибка при получении тем: {e}")
        return
    text_topics = topics.get('response')
    await message.answer("Доступные темы для проведения теста:\n\n" + text_topics)


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
