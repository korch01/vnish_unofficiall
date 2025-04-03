import asyncio
from vnish_api import MinerAPI

async def main():
    miner = MinerAPI("192.168.1.1")
    settings = await miner.fetch_settings()

    # Изменяем настройки
    settings.miner.misc.min_operational_chains = 1

    # Отправляем обратно (если отличается)
    result = await miner.send_settings(settings)
    if result is True:
        print("✅ Отправлено!")
    elif result is None:
        print("🔁 Уже совпадает — пропущено.")
    else:
        print("❌ Ошибка при отправке.")

asyncio.run(main())
