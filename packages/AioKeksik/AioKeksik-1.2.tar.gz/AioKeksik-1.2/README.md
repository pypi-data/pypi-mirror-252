# pyKeksik
Асинхронная библиотека для взаимодействия с API [Кексика](https://keksik.io)

[Официальная документация](https://keksik.io/api)
Библиотека была написана на основе [библиотеки](https://github.com/Friendosie/pyKeksik) ув. [Friendosie](https://github.com/Friendosie)

# Примеры кода
```python
from AioKeksik import KeksikApi

keksik_api = KeksikApi(group_id, apikey)
import asyncio
async def main():
    # Список донатов
    print(await keksik_api.donates.get())
    # Список краутфанденговых кампаний
    print(await keksik_api.campaigns.get())
    # Список выплат
    print(await keksik_api.payments.get())
    # Баланс
    print(await keksik_api.balance())
asyncio.run(main())
```