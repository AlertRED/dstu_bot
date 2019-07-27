from app.models.models_menu import Menu
from app.models.orm_models import User


class Controller:

    # def __init__(self, userDAO):
    #     self.userDAO = userDAO

    def parse_answer(self, data_answer: dict, user: User, current_menu: Menu):
        answer = data_answer.get("answer", None)
        new_menu = data_answer.get("new_menu", None)
        special_answers = data_answer.get("special_answers", [])
        special_index = data_answer.get("special_index", None)

        if new_menu is not None:
            current_menu = new_menu

        user.set_index(special_index).set_menu(current_menu.index).set_answers(special_answers)

        return answer, current_menu

    def get_answer(self, request: str, user: User):
        current_menu = Menu.menues[int(user.user_cache.current_menu)]

        result = current_menu.get_answer(request,
                                         special_index=user.user_cache.special_index,
                                         special_answers=[i.answer for i in user.answers],
                                         vk_id=user.vk_id)

        result = self.parse_answer(result, user, current_menu)
        return result
