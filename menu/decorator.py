from datetime import datetime
from menu import UserMenuStrategy
from config import LOG_FILE_PATH


class MenuDecorator(UserMenuStrategy):
    menu: UserMenuStrategy

    def __init__(self, menu: UserMenuStrategy) -> None:
        self.menu = menu

    def get_menu_title(self) -> str:
        return self.menu.get_menu_title()

    def set_menu_title(self):
        return self.menu.set_menu_title()

    def match_option_to_function(self, selected_option: str) -> bool:
        return self.menu.match_option_to_function(selected_option)

    def set_logged_user(self):
        self.menu.set_logged_user()

    def show_menu_options(self):
        self.menu.show_menu_options()


class LogMenuDectorator(MenuDecorator):
    def match_option_to_function(self, selected_option: str) -> bool:
        user_name = self.menu.logged_user.name
        menu_name = self.menu.__class__.__name__
        log = f"[{user_name}@{datetime.now()}] escolheu a opção {selected_option} no menu {menu_name}\n"

        with open(LOG_FILE_PATH, "a") as f:
            f.write(log)

        return self.menu.match_option_to_function(selected_option)
