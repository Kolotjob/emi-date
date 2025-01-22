import os
from django.core.asgi import get_asgi_application
from tortoise import Tortoise
from config import TORTOISE_ORM

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_emi.settings')

async def init_db():
    if not Tortoise._inited:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()

application = get_asgi_application()
