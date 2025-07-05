import asyncio
from datetime import datetime
from pyrogram import Client
from pyrogram.errors import StargiftUsageLimited

from config_buyer import sleep_send_seconds, sleep_checking_seconds, sessions_for_checking, send_config

new_gifts = None


async def buy_gifts(config):
    async with Client(config['session']) as app:  # запускаем основной аккаунт
        balance = await app.get_stars_balance()
        for gift in new_gifts:  # цикл по всем подаркам начиная с самого маленького саплая
            if gift['total']            <= 1000 and gift['price']   > 30000:
                continue
            if 1001 <= gift['total']    <= 3000 and gift['price']   > 30000:
                continue
            if 3001 <= gift['total']    <= 5000 and gift['price']   > 25000:
                continue
            if 5001 <= gift['total']    <= 10000 and gift['price']  > 20000:
                continue
            if 10001 <= gift['total']   <= 20000 and gift['price']  > 15000:
                continue
            if 20001 <= gift['total']   <= 50000 and gift['price']  > 10000:
                continue
            if 50001 <= gift['total']   <= 100000 and gift['price'] > 5000:
                continue
            if 100001 <= gift['total']  <= 200000 and gift['price'] > 1000:
                continue
            if 200001 <= gift['total']  <= 300000 and gift['price'] > 500:
                continue
            if 300001 <= gift['total'] and gift['price'] > 200:
                continue
            count_gifts = balance // gift['price']  # считаем сколько подарков можем купить
            if not count_gifts:  # переходим к следующему если не хватает баланса
                continue
            for _ in range(count_gifts):
                try:
                    await app.send_gift(config['target'], gift['id'], is_private=True)
                    await asyncio.sleep(sleep_send_seconds)
                except StargiftUsageLimited:
                    print(f"[{config['session']} --> {config['target']}] gift with price {gift['price']}: StargiftUsageLimited'")
                    break  # если кончился саплай переходим к следующему подарку
                except Exception as e:
                    print(config['target'], e)
            balance = await app.get_stars_balance()
        print(f"[{config['session']} --> {config['target']}] end ")


async def check_new_gifts(session_list, len_old):
    while True:
        for session in session_list:
            data_gifts = await session.get_available_gifts()    # чекаем новые подарки
            print(f"{datetime.now()} check")
            gifts_limit = [i.id for i in data_gifts if i.is_limited]   # создание списка лимитированных подарков для сравнения
            if len(gifts_limit) > len_old:   # если появились новые подарки
                return data_gifts
        await asyncio.sleep(sleep_checking_seconds)


async def main():
    session_list = [Client(session) for session in  sessions_for_checking]
    try:
        for session in session_list:
            await session.start()
        old_gifts = await session_list[0].get_available_gifts()   # получения списка подарков для сравнения и обнаружения новых
        old_gifts = {i.id for i in old_gifts if i.is_limited}  # создание множество лимитированных подарков для сравнения
        data_gifts = await check_new_gifts(session_list, len(old_gifts))
    finally:
        for session in session_list:
            await session.stop()

    print(f"-====================-\n"
          f"{datetime.now()} find new\n"
          f"-====================-")
    gifts_limit_dict = {gift.id: gift for gift in data_gifts if gift.is_limited}    # создания словаря из подарков для обращения к подарку по id
    global new_gifts
    new_gifts = [gifts_limit_dict[gift_id] for gift_id in gifts_limit_dict.keys() if gift_id not in old_gifts]     # отбираем новые подарки по id
    new_gifts = [{"id": gift.id, "total": gift.total_amount, "price": gift.price} for gift in new_gifts]    # получаем саплай и цену для сортировки
    new_gifts = sorted(new_gifts, key= lambda x:x['total'])   # сортируем по саплаю

    # запускаем все аккаунты на покупку
    await asyncio.gather(*[buy_gifts(config) for config in send_config])


asyncio.run(main())