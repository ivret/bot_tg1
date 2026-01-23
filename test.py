import asyncio
from googletrans import Translator


async def translate_text():
    translator = Translator()
    # Асинхронный вызов перевода
    result = await translator.translate("что делать цуам", dest="en")
    print(result.text)  # Теперь .text доступен


# Запуск асинхронной функции
asyncio.run(translate_text())
