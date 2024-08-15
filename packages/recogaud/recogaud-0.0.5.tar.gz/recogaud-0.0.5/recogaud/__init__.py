import speech_recognition as sr
from pydub import AudioSegment
from telethon import TelegramClient, events
import asyncio

def recognize_speech(audio_file):
    audio = AudioSegment.from_file(audio_file)
    audio.export("converted_audio.wav", format="wav")
    recognizer = sr.Recognizer()
    with sr.AudioFile("converted_audio.wav") as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        return text
    except sr.UnknownValueError:
        print("Не удалось распознать аудио.")
        return None
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания: {e}")
        return None

async def process_with_telegram(api_id, api_hash, audio_file):
    recognized_text = recognize_speech(audio_file)
    if recognized_text is None:
        print("Распознавание текста не удалось. Скрипт завершён.")
        return

    bot_username = 'forgetgpt_bot'  # Имя бота по умолчанию

    async with TelegramClient('session', api_id, api_hash) as client:
        # Отправка команды /claude боту
        await client.send_message(bot_username, '/claude')
        await asyncio.sleep(8)
        
        processed_text = f""" Request: Text to process: {recognized_text} \n\nInstructions: 1. Correct spelling mistakes. 2. Improve the grammar and syntax of the text. 3. Preserve the original meaning and style of the text. 4. Replace words with more appropriate synonyms. Write a corrected version of the text in Russian, or in English, depending on the original version of the text."""
        
        # Отправка распознанного текста с инструкциями боту
        await client.send_message(bot_username, processed_text)

        # Обработка ответа от бота
        @client.on(events.NewMessage(from_users=bot_username))
        async def handler(event):
            print(f"Ответ бота: {event.message.text}")
            await asyncio.sleep(30)
            await client.send_message(bot_username, '/stop')
            print("Отправлена команда /stop")

def recog(api_id, api_hash, audio_file):
    asyncio.run(process_with_telegram(api_id, api_hash, audio_file))