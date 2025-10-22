import os

from abc import ABC, abstractmethod
from service import School
from system import User


class UserMenuStrategy(ABC):
    school: School
    menu_title: str
    logged_user: User

    def __init__(self):
        self.school = School()
        self.set_menu_title()

    def execute(self):
        self.set_logged_user()

        while True:
            os.system("clear")
            print(self.get_menu_title())

            self.show_menu_options()
            print("0. Voltar")

            selected_option = input("\nEscolha uma opção: ")
            os.system("clear")
            if selected_option == "0":
                break

            hold = self.match_option_to_function(selected_option)
            if hold:
                input("\nClique Enter para voltar ao menu.")

    def get_menu_title(self) -> str:
        return self.menu_title

    @abstractmethod
    def set_menu_title(self):
        pass

    @abstractmethod
    def set_logged_user(self):
        pass

    @abstractmethod
    def show_menu_options(self):
        pass

    @abstractmethod
    def match_option_to_function(self, selected_option: str) -> bool:
        pass


class UserMenuContext:
    strategy: UserMenuStrategy | None = None

    def show_menu(self):
        if self.strategy is None:
            raise ValueError("You must provide a strategy first")

        self.strategy.execute()

    def set_strategy(self, strategy: UserMenuStrategy):
        self.strategy = strategy
