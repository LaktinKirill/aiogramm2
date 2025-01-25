import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import random
import os
from googletrans import Translator
from gtts import gTTS


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.text) 
async def translate_to_english(message: Message):
    try:
       
        translator = Translator()

        
        translation = translator.translate(message.text, dest='en')
        
       
        tts = gTTS(text=translation.text, lang='en')
        voice_file = f"tmp/{message.message_id}.mp3"
        os.makedirs('tmp', exist_ok=True)
        tts.save(voice_file)
        
       
        await message.reply(
            f"Перевод: {translation.text}\n"
        )
      
       
        voice = FSInputFile(voice_file)
        await message.reply_voice(voice)
        
       
        os.remove(voice_file)
        
    except Exception as e:
        await message.reply("Извините, произошла ошибка при переводе.")
        print(f"Ошибка перевода: {e}")

@dp.message(Command('voise'))
async def voise(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="upload_video")
    video = FSInputFile("VID-20250123-WA0000.mp4")
    await message.reply_video(video)


@dp.message(Command('video'))
async def video(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="upload_video")
    video = FSInputFile("VID-20250123-WA0000.mp4")
    await message.reply_video(video)

    
@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile("audio.mp3")
    await message.reply_audio(audio)


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполняить команды: \n /start, \n /help, \n /weather')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')

@dp.message(F.photo)
async def react_photo(message: Message):
    os.makedirs('tmp', exist_ok=True)
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


@dp.message()
async def start(message: Message):
    await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)






if __name__ == '__main__':
    asyncio.run(main())
