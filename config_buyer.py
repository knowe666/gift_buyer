# аккаунты для проверки выхода новых подарков
sessions_for_checking = ["dasha", "pasha", "masha"]

# аккаунт со звёздами и получатель подарков
send_config = [{"session": "andrei", "target": "@trackaton"},
               {"session": "oleg", "target": "@trackaton"}]

# задержка между запросами на отправку подарков
sleep_send_seconds = 0.2
# задержка между циклами проверки новых подарков
sleep_checking_seconds = 1