import asyncio
from module.connect_data import connect_OPC_UA 



async def function2():
    while True:
        
        # Ваш код для функции 2
        await asyncio.sleep(60)

# Запуск функций
async def main():
    await asyncio.gather(connect_OPC_UA(), function2())

asyncio.run(main())
