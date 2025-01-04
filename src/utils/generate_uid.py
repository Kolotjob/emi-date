import random
import string

async def generate_uid_code(uids ):
    length=5
    uid=""
    while uid =="":

        """
        Генерирует уникальный код указанной длины, содержащий латинские заглавные и строчные буквы и цифры.

        :param length: Длина кода (по умолчанию 5).
        :return: Сгенерированный код.
        """
        characters = string.ascii_letters + string.digits  # Латинские буквы (верхний и нижний регистр) + цифры
        x_code=''.join(random.choices(characters, k=length))
        if x_code not in uids:
            uid = x_code
        else:
            continue
    return uid

# Пример использования

