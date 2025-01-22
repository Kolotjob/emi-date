from tortoise.models import Model
from tortoise import fields



class User(Model):
    user_id = fields.BigIntField(pk=True, unique=True)  # Уникальный Telegram ID пользователя
    uid_code = fields.CharField(max_length=50, unique=True)  # Уникальный код пользователя
    status_block = fields.CharField(max_length=255, default="Active")  # Статус (например, "Active", "Blocked")
    name = fields.CharField(max_length=50, null=True)  # Имя
    age = fields.IntField(null=True)  # Возраст
    orientation = fields.CharField(max_length=255, null=True)
    gender = fields.CharField(max_length=10, null=True)  # Пол (например, "male", "female", "other")
    medias = fields.JSONField(null=True)  # Ссылки на медиа (фото/видео)
    about = fields.TextField(null=True)  # Описание "О себе"
    location = fields.CharField(max_length=255, null=True)  # Локация
    preferences = fields.CharField(max_length=255, null=True)  # Кого ищет (например, "friends", "relationship")
    hobbies = fields.JSONField(null=True)  # Список увлечений (до 5)
    for_whom = fields.CharField(max_length=255, null=True)  # Кого показывать (например, "all", "man" , 'girl')
    subscription = fields.CharField(max_length=50, default="Free") 
    localstatus = fields.CharField(max_length=50, default="active") 

     # Тариф подписки (например, "Free", "Premium")
    subscription_start = fields.DatetimeField(null=True)  # Дата начала подписки (только для платных)
    subscription_end = fields.DatetimeField(null=True)  # Дата окончания подписки
    referral_uid = fields.CharField(max_length=50, unique=True, null=True)  # Telegram ID реферера
    balance = fields.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Баланс
    level = fields.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # % от реферальной программы
    date_registered = fields.DatetimeField(auto_now_add=True)  # Дата регистрации
    lang = fields.CharField(max_length=50, default="nochoise") #язык поользователя
    class Meta:
        table = "users"





class Like(Model):
    like_id = fields.IntField(pk=True)  # Уникальный ID лайка
    from_user = fields.ForeignKeyField("models.User", related_name="sent_likes")  # Кто лайкнул
    to_user = fields.ForeignKeyField("models.User", related_name="received_likes")  # Кто получил лайк
    is_superlike = fields.BooleanField(default=False)  # Это суперлайк или обычный лайк
    message = fields.TextField(null=True)  # Сообщение, если было отправлено
    created_at = fields.DatetimeField(auto_now_add=True)  # Дата создания лайка

    class Meta:
        table = "likes"


class Block(Model):
    block_id = fields.IntField(pk=True)  # Уникальный ID блокировки
    from_user = fields.ForeignKeyField("models.User", related_name="blocked_users")  # Кто заблокировал
    to_user = fields.ForeignKeyField("models.User", related_name="blocked_by")  # Кто заблокирован
    can_message = fields.BooleanField(default=False)  # Разрешены ли сообщения
    created_at = fields.DatetimeField(auto_now_add=True)  # Дата блокировки

    class Meta:
        table = "blocks"


class Statement(Model):
    statement_id = fields.IntField(pk=True)  # Уникальный ID записи
    user = fields.ForeignKeyField("models.User", related_name="statements")  # Пользователь
    referral_count = fields.IntField(default=0)  # Количество рефералов
    subscription_level = fields.CharField(max_length=20, default="basic")  # Уровень подписки
    price = fields.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Цена подписки/транзакции
    referral_percentage = fields.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Процент отчислений за реферал
    payment_method = fields.CharField(max_length=50, null=True)  # Метод оплаты (например, "card", "paypal")
    transaction_id = fields.CharField(max_length=255, null=True)  # Уникальный ID транзакции
    status = fields.CharField(max_length=20, default="pending")  # Статус транзакции (успешно, ошибка)
    created_at = fields.DatetimeField(auto_now_add=True)  # Дата создания записи

    class Meta:
        table = "statements"
