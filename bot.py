import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import json
from datetime import *
from time import sleep
from threading import Thread
from os.path import abspath as tdir
import traceback
import requests
from sqlite import BotDB
import os
import requests
import urllib.request

BotDB = BotDB('bd.db')
if not(bool(BotDB.get_parametrs())):
    BotDB.add_parametr("info", "Инфо: ")
    BotDB.add_parametr("Contacrs", "Контакты - ")
    BotDB.add_parametr("admins", "[486290555, 565444877]")

vk = vk_api.VkApi(token= "vk1.a.nzULi3uVtJnPhO97ElfDil9DZjO070-lVvC_OGAdYkgAbRBKcDQENJ8BT2qwpgzHWlRgF3axTZdQsNm-h6lVbPBwMriZ2LXsLgXiHDXSjTzdXD-ClZU-opmj7jzKyd3mwfC1irUxjHVk73c9GiMl5JhYx4oGd8smQcifvcQFRZI0erA8jK9NHy-J9hb4JrIWk-VpwGJudKjUci_K_-Wwuw")
vk._auth_token()
api = vk.get_api()
longpoll = VkBotLongPoll(vk, 212719108)


def sender(user_id, text, keyboard=None, template=None, forward=None, attachment = None):
    vk.method("messages.send", {"user_id": user_id, 'attachment': attachment,  'forward_messages': forward, "message": text, "random_id": random.randint(-9223372036854775807, 9223372036854775807), "keyboard": keyboard, "template": template})

    

#add_key
add_key = VkKeyboard(one_time=False)
add_key.add_button("Обои", color=VkKeyboardColor.POSITIVE)
add_key.add_line()
add_key.add_button("Инфо")
#end add_key

#esc_key
esc_key = VkKeyboard(one_time=False)
esc_key.add_button("Отмена")
#end esc_key

#esc_key
end_key = VkKeyboard(one_time=False)
end_key.add_button("Закончить", color=VkKeyboardColor.NEGATIVE)
#end esc_key

#url_key
url_key = VkKeyboard(inline=True)
url_key.add_button("Ещё", color=VkKeyboardColor.POSITIVE)
url_key.add_line()
url_key.add_openlink_button("Поблагодарить подпиской", "https://vk.com/fang02")
#end url_key

#admin_key
admin_key = VkKeyboard(one_time=False)
admin_key.add_button("Добавить обои", color=VkKeyboardColor.POSITIVE)
admin_key.add_line()
admin_key.add_button("Категории", color=VkKeyboardColor.POSITIVE)
admin_key.add_line()
admin_key.add_button("Изменить инфо")
admin_key.add_line()
admin_key.add_button("Изменить контакты")
#end admin_key

def get_cat():
    cat = BotDB.get_categories()
    cat_key = VkKeyboard(inline=True)
    if cat:
        for i in cat:
            check = True
            cat_key.add_button(i)
            cat_key.add_line()
        return cat_key
    else:
        return 0


def bott(event): 
    if True:
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.object.message["text"]
                id = event.object.message["from_id"]
                settings = BotDB.get_parametrs()
                try:
                    user = BotDB.get_user_id(id)
                except:
                    pass
                if id in eval(settings["admins"]):
                    if not(BotDB.user_check(id)):
                        sender(id, 'Админка', keyboard=admin_key.get_keyboard())
                        BotDB.add_user(id)
                    else:
                        if user["mode"] == "start":
                            category = BotDB.get_categories()
                            if msg == "Изменить инфо":
                                BotDB.update_user(id, mode = "info")
                                sender(id, f"""Отправьте информацию

Текущая информация:
{settings['info']}""", keyboard=esc_key.get_keyboard())
                            if msg == "Категории":
                                #BotDB.update_user(id, mode = "category")
                                cat_key = get_cat()
                                if cat_key != 0:
                                    cat_key.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)
                                    sender(id, 'Категории', keyboard=cat_key.get_keyboard())
                                else:
                                    cat_key = VkKeyboard(inline=True)
                                    cat_key.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)
                                    sender(id, 'Категории', keyboard=cat_key.get_keyboard())
                            if msg == "Добавить категорию":
                                xx = len(BotDB.get_categories())
                                if xx < 9:
                                    BotDB.update_user(id, mode = "category_get")
                                    sender(id, 'Введите название категории', keyboard=esc_key.get_keyboard())
                                else:
                                    sender(id, 'Максимальное кол-во категорий: 9')

                            if "Изменить" in msg and not("инфо" in msg):
                                cat_update = msg.split(": ")[1]
                                BotDB.update_user(id, mode = f"update:{cat_update}")
                                sender(id, 'Введите новое название', keyboard=esc_key.get_keyboard())
                                
                            if "Удалить" in msg:
                                cat_delete = msg.split(": ")[1]
                                id_cat = BotDB.get_categories_name(cat_delete)[0]
                                BotDB.delete_categories(id_cat)
                                sender(id, 'Категория удалена')

                            if msg == "Добавить обои":
                                BotDB.update_user(id, mode = "oboi_get")
                                sender(id, 'Добавление картинок', keyboard=esc_key.get_keyboard())
                                cat_key = get_cat()
                                cat_key.add_button("Отмена", color=VkKeyboardColor.NEGATIVE)
                                sender(id, 'Выберите категорию', keyboard=cat_key.get_keyboard())
                                

                                
                            if msg in category: 
                                kol_oboi = len(BotDB.get_oboi(category = msg))
                                cat_up_key = VkKeyboard(inline=True)
                                cat_up_key.add_button(f"Изменить: {msg}", color=VkKeyboardColor.PRIMARY)
                                cat_up_key.add_button(f"Удалить: {msg}", color=VkKeyboardColor.NEGATIVE)
                                sender(id, f'''Категория: {msg}

{kol_oboi} картинок
''', keyboard=cat_up_key.get_keyboard())


                        if "update" in user["mode"]:
                            cat_updatex = user["mode"].split(":")[1]
                            if msg == "Отмена":
                                BotDB.update_user(id, mode = "start")
                                sender(id, 'Отмена', keyboard=admin_key.get_keyboard())
                                kol_oboi = len(BotDB.get_oboi(category = cat_updatex))
                                cat_up_key = VkKeyboard(inline=True)
                                cat_up_key.add_button(f"Изменить: {cat_updatex}", color=VkKeyboardColor.PRIMARY)
                                cat_up_key.add_button(f"Удалить: {cat_updatex}", color=VkKeyboardColor.NEGATIVE)
                                sender(id, f'''Категория: {cat_updatex}

{kol_oboi} картинок
''', keyboard=cat_up_key.get_keyboard())
                            else:
                                id_cat = BotDB.get_categories_name(cat_updatex)[0]
                                BotDB.update_categories(id_cat, name = msg)
                                sender(id, 'Категория изменена', keyboard=admin_key.get_keyboard())
                                cat_key = get_cat()
                                if cat_key == 0:
                                    cat_key = VkKeyboard(inline=True)
                                    cat_key.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)
                                    sender(id, 'Категории', keyboard=cat_key.get_keyboard())
                                else:
                                    cat_key.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)
                                    sender(id, 'Категории', keyboard=cat_key.get_keyboard())
                                BotDB.update_user(id, mode = "start")

                                 
                        if user["mode"] == "category_get":
                            if msg == "Отмена":
                                BotDB.update_user(id, mode = "start")
                                sender(id, 'Отмена', keyboard=admin_key.get_keyboard())
                                cat_key = get_cat()
                                if cat_key == 0:
                                    cat_key = VkKeyboard(inline=True)
                                    cat_key.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)
                                    sender(id, 'Категории', keyboard=cat_key.get_keyboard())
                                else:
                                    cat_key.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)
                                    sender(id, 'Категории', keyboard=cat_key.get_keyboard())
                            else:
                                BotDB.add_categories(msg)
                                cat_key = get_cat()
                                BotDB.update_user(id, mode = "start")
                                sender(id, 'Категория добавлена', keyboard=admin_key.get_keyboard())
                                if cat_key == 0:
                                    cat_key = VkKeyboard(inline=True)
                                    cat_key.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)
                                    sender(id, 'Категории', keyboard=cat_key.get_keyboard())
                                else:
                                    cat_key.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)
                                    sender(id, 'Категории', keyboard=cat_key.get_keyboard())

                        if user["mode"] == "info":
                            if msg == "Отмена":
                                BotDB.update_user(id, mode = "start")
                                sender(id, 'Админка', keyboard=admin_key.get_keyboard())
                            else:
                                BotDB.update_parametrs("info", value = msg)
                                BotDB.update_user(id, mode = "start")
                                sender(id, 'Админка', keyboard=admin_key.get_keyboard())
                                    
                        if "oboi_get" in user["mode"]:
                            category = BotDB.get_categories()
                            if msg in category:
                                BotDB.update_user(id, mode = "oboi_get" + ":" + msg)
                                sender(id, 'Отправьте картинки', keyboard=end_key.get_keyboard())
                            elif msg == "Закончить":
                                BotDB.update_user(id, mode = "oboi_get")
                                sender(id, 'Добавление картинок', keyboard=esc_key.get_keyboard())
                                cat_key = get_cat()
                                cat_key.add_button("Отмена", color=VkKeyboardColor.NEGATIVE)
                                sender(id, 'Выберите категорию', keyboard=cat_key.get_keyboard())

                            elif msg == "Отмена":
                                BotDB.update_user(id, mode = "start")
                                sender(id, 'Админка', keyboard=admin_key.get_keyboard())
                            else:
                                category = user["mode"].split(":")[1]
                                for item in event.object['message']['attachments']:
                                    if item['type'] == 'photo':
                                        img_msg_get = item['photo']['sizes'][-1]['url']#event.object.message["attachments"][0]['photo']['sizes'][-1]['url']
                                        urllib.request.urlretrieve(img_msg_get, str(id)+'.jpg')
                                        a = vk.method("photos.getMessagesUploadServer")
                                        b = requests.post(a['upload_url'], files={'photo': open(str(id)+'.jpg', 'rb')}).json()
                                        c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
                                        d = "photo{}_{}".format(c["owner_id"], c["id"])
                                        BotDB.add_oboi(d, category)
                                        os.remove(str(id)+'.jpg')

                else:
                    category = BotDB.get_categories()
                    if not(BotDB.user_check(id)):
                        sender(id, 'Привет , если хочешь получить обои , жми на кнопку обои ниже.', keyboard=add_key.get_keyboard())
                        BotDB.add_user(id)
                    else:
                        if "бои" in msg:
                            cat_key = get_cat()
                            cat_key.add_openlink_button("Паблик", "https://vk.com/fang02")
                            sender(id, 'Выбирай категорию по которой хочешь получить обои', keyboard=cat_key.get_keyboard())
                        if msg in category:
                            oboi = BotDB.get_oboi(category = msg)
                            check = True
                            if len(eval(user["oboi_get"])) == len(oboi):
                                BotDB.update_user(id, oboi_get = "[]")
                                user = BotDB.get_user_id(id)
                            oboi_get = eval(user["oboi_get"])
                            while check:
                                ob = random.choice(oboi)
                                if ob[0] in oboi_get:
                                    pass
                                else:
                                    check = False
                            sender(id, 'Обои для вас', attachment = ob[1], keyboard=url_key.get_keyboard())
                            oboi_get.append(ob[0])
                            BotDB.update_user(id, mode = msg)
                            BotDB.update_user(id, oboi_get = str(oboi_get))
                        if "Ещё" == msg and user["mode"] != "start":
                            oboi = BotDB.get_oboi(category = user["mode"])
                            check = True
                            if len(eval(user["oboi_get"])) == len(oboi):
                                BotDB.update_user(id, oboi_get = "[]")
                                user = BotDB.get_user_id(id)
                            oboi_get = eval(user["oboi_get"])
                            while check:
                                ob = random.choice(oboi)
                                if ob[0] in oboi_get:
                                    pass
                                else:
                                    check = False
                            sender(id, 'Обои для вас', attachment = ob[1], keyboard=url_key.get_keyboard())
                            oboi_get.append(ob[0])
                            BotDB.update_user(id, oboi_get = str(oboi_get))
                        if "Инфо" == msg:
                            sender(id, settings["info"])
                            
                                
                                
        except:
            print('Ошибка:\n', traceback.format_exc())


while True:
    for event in longpoll.listen():
        t = Thread(target=bott, args=(event,))
        t.start()
        
