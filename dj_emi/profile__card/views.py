from django.http import JsonResponse
import asyncio
from tortoise import Tortoise
from config import TORTOISE_ORM
from src.models import User

async def init_db():
    if not Tortoise._inited:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()

def get_user_cards(request):
    # Инициализация базы данных
    asyncio.run(init_db())

    # Получение данных
    async def fetch_users():
        current_user_id = request.GET.get('user_id')
        return await User.filter(localstatus="active").exclude(user_id=current_user_id).values(
            "name", "age", "about", "medias"
        )

    users = asyncio.run(fetch_users())

    return JsonResponse({"users": list(users)})
