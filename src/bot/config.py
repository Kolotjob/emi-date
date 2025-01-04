BOT_TOKEN = "6137952629:AAENt0V0fK9pwDNo2NRxP4_GiiLNdXqKtHk"


TORTOISE_ORM = {
    "connections": {
        # Использование вашего IPv6-адреса и учетных данных
        "default": "mysql://maxemidate:id!125678!@platina.pro:3306/emidate_db"
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],  # Пути к вашим моделям
            "default_connection": "default",
        },
    },
}


