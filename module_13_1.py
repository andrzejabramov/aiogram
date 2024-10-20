import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования')
    for sphere in range (5):
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял шар {sphere + 1}')
    print(f'Силач {name} закончил соревнования')


async def start_tournament():
    pasha = asyncio.create_task(start_strongman('Pasha', 3))
    denis = asyncio.create_task(start_strongman('Denis', 4))
    apollon = asyncio.create_task(start_strongman('Apollon', 5))
    await pasha
    await denis
    await apollon


asyncio.run(start_tournament())