TORTOISE_ORM = {
    "connections": {
        "default": "mysql://maxemidate:id!125678!@platina.pro:3306/emidate_db"
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
