import json
import os

from vk_api import VkApi, VkUpload
import traceback
from app.controller import Controller
from app.menus import MenuTree
from app.models_menu import TypeItem
import random
import logging
import threading
from app.models.models_other import Log


class App:
    __button_colors = {TypeItem.GATE: 'primary',
                       TypeItem.BACK: 'negative',
                       TypeItem.MENU: 'positive',
                       TypeItem.SIMPLE: 'default'}

    def __init__(self, vk: VkApi, vk_upload: VkUpload, menus_tree: MenuTree, controller: Controller, models):

        self.controller = controller
        self.vk = vk
        self.models = models
        self.vk_upload = vk_upload
        self.images_dir = os.path.join(os.getcwd(), 'images')
        self.menus = menus_tree

        logging.basicConfig(filename="config/history.log", level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='[%m-%d-%Y %I:%M:%S]')

    @staticmethod
    def __get_button_json(label, color, payload=""):
        return {
            "action": {
                "type": "text",
                "payload": json.dumps(payload),
                "label": label
            },
            "color": color
        }

    @staticmethod
    def __get_keyboard(items: dict, *args, **kwargs):
        buttons = []
        group = []

        for label, obj in items.items():
            limit = 30 // (len(group) + 1)
            label = obj[2](*args, **kwargs) if obj[2] else label
            group.append((label, App.__button_colors.get(obj[1], "default")))
            if any(map(lambda x: len(x[0]) > limit, group)) or (len(group) > 4):
                buttons.append(list(map(lambda i: App.__get_button_json(label=i[0], color=i[1]), group[:-1])))
                group = group[-1:]
                if len(buttons) == 9:
                    break
        buttons.append(list(map(lambda i: App.__get_button_json(label=i[0], color=i[1]), group)))

        keyboard = {
            "one_time": True,
            "buttons": buttons
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        return str(keyboard.decode('utf-8'))

    def __send_message(self, answer, menu, id_user):
        if answer:
            result = ""
            if answer[1]:
                path_file = os.path.join(self.images_dir, answer[1])
                if os.path.exists(path_file):
                    photo = self.vk_upload.photo_messages(path_file)
                    result = 'photo' + str(photo[0].get('owner_id')) + '_' + str(photo[0].get('id'))
            self.vk.method("messages.send",
                           {"peer_id": id_user,
                            "message": answer[0],
                            "keyboard": self.__get_keyboard(menu.items,
                                                            user_id=id_user) if menu and menu.items else None,
                            "attachment": result,
                            "random_id": random.randint(1, 2147483647)})
        elif menu:
            self.vk.method("messages.send",
                           {"peer_id": id_user, "message": menu.get_menu(),
                            "keyboard": self.__get_keyboard(menu.items, user_id=id_user),
                            "random_id": random.randint(1, 2147483647)})

    # обработка сообщения
    def __handling_message(self, user_id: int, text_message: str):
        user_info = self.vk.method("users.get", values={"user_ids": user_id})
        user = self.models.User.create(user_id, user_info[0]['first_name'],
                                       user_info[0]['last_name']).create_cache(self.menus.root.index).inc_request()
        answer, menu = self.controller.get_answer(text_message, user)
        self.__send_message(answer, menu, user_id)

    # запуск цикла
    def run(self):
        print('[*] Цикл обработки сообщений запущен')
        while True:
            user_id = None
            try:
                messages = self.vk.method("messages.getConversations",
                                          {"offset": 0, "count": 20, "filter": "unanswered"})
                if messages["count"] >= 1:
                    user_id = messages["items"][0]["last_message"]["from_id"]
                    text_message = messages["items"][0]["last_message"]["text"]
                    logging.info("From id: %d, message: %s" % (user_id, text_message))

                    if not any(thread.name == str(user_id) for thread in threading.enumerate()):
                        threading.Thread(target=self.__handling_message, args=(user_id, text_message), name=user_id).start()
            except Exception as E:
                Log.create(text=str(traceback.format_exc()), vk_id=user_id)
                if user_id:
                    self.__send_message(('Вы что-то сломали:(', None), menu=self.menus.root, id_user=user_id)
