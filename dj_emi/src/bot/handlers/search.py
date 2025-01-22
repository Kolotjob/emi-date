

# import ssl
# import certifi
# from geopy.geocoders import Nominatim

# def get_location_by_coordinates(latitude, longitude):
#     geolocator = Nominatim(
#         user_agent="my_geopy_app",
#         timeout=10,
#         ssl_context=ssl.create_default_context(cafile=certifi.where())
#     )
#     try:
#         location = geolocator.reverse((latitude, longitude), exactly_one=True)
#         if location:
#             address = location.raw.get('address', {})
#             city = address.get('city') or address.get('town') or address.get('village') or address.get('hamlet')
#             return city or location.address
#         else:
#             return "Местоположение не найдено"
#     except Exception as e:
#         return f"Ошибка при определении местоположения: {e}"
    

# @router.message(Command("myprofile"))
# async def my_profile_handler(message: types.Message,state: FSMContext):
#     user = await User.get_or_none(user_id=message.from_user.id)

#     if not user:
#         lang = "ru"
#         await message.answer("<b>Профиль не найден.</b>\nПожалуйста, зарегистрируйтесь с помощью команды /start.")
#         return

#     lang = user.lang if user.lang in ["ru", "en"] else "ru"
#     hobbies_text = ", ".join([
#         (interest[1] if lang == "ru" else interest[2])
#         for interest in INTERESTS
#         if str(interest[0]) in (user.hobbies or [])
#     ])

#     location_text = user.location or ("Локация не указана" if lang == "ru" else "Location not provided")
#     if "," in location_text:
#         latitude, longitude = map(float, location_text.split(","))
#         location_text = get_location_by_coordinates(latitude, longitude)

#     subscription_text = (
#         f"<b>{'Подписка' if lang == 'ru' else 'Subscription'}:</b> {user.subscription}\n"
#     )
#     if user.subscription != "Free":
#         subscription_text += (
#             f"<b>{'Дата окончания подписки' if lang == 'ru' else 'Subscription end date'}:</b> {user.subscription_end}\n"
#         )

#     description = (
#         f"<b>{user.name}</b> \n"
#         f"<b>{'Возраст' if lang == 'ru' else 'Age'}:</b> {user.age}\n"
#         f"{GENDER[lang][user.gender]}\n"
#         f"<b>{'Ориентация' if lang == 'ru' else 'Orientation'}:</b> {ORI[lang][user.orientation]}\n"
#         f"{location_text}\n"

#         f"<b>{'Цели' if lang == 'ru' else 'Goals'}:</b> {PREFERENCES[lang][user.preferences]}\n"
#         f"<b>{'Увлечения' if lang == 'ru' else 'Hobbies'}:</b> {hobbies_text}\n\n"
#         f"_________________________\n{user.about or ''}\n"
#     )



#     media = user.medias or []
#     if len(media) == 1:
#         media_file = media[0]['file_id']
#         if media[0]['type'] == 'photo':
#             msg= await message.bot.send_photo(message.from_user.id, media_file, caption=description)
#         elif media[0]['type'] == 'video':
#             msg= await message.bot.send_video(message.from_user.id, media_file, caption=description)
#     else:
#         files=[]
#         i =0
#         for media_file in media:
            
#             caption=description if i == 0 else None
            
#             if media_file["type"] =="video":
#                 files.append(InputMediaVideo(media=f"{media_file['file_id']}", caption=caption))
#                 i = i+1
#             elif media_file['type'] == 'photo':
#                 files.append(InputMediaPhoto(media=f"{media_file['file_id']}", caption=caption))
#                 i = i+1
#             else:
#                 continue
                 

#     # Отправка медиа-группы
#         msg= await message.bot.send_media_group(chat_id=message.from_user.id, media=files)
#         data= await state.get_data()
#         data["id_card_profile"]=None
#         await state.update_data(data=data)
    
    

   
        
    
