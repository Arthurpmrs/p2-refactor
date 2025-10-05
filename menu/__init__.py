import os

from abc import ABC, abstractmethod
from service import School


class UserMenuStrategy(ABC):
    school: School
    menu_title: str

    def __init__(self):
        self.school = School()

    def execute(self):
        while True:
            os.system("clear")
            print(self.menu_title)

            self.show_menu_options()
            print("0. Voltar")

            selected_option = input("\nEscolha uma opção: ")
            os.system("clear")
            if selected_option == "0":
                break

            hold = self.match_option_to_function(selected_option)
            if hold:
                input("\nClique Enter para voltar ao menu.")

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
