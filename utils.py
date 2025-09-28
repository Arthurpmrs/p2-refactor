import datetime
import random
import string
from typing import Callable, TypeVar


def generate_random_hash(length: int = 6):
    characters = string.ascii_letters + string.digits
    random_hash = "".join(random.choice(characters) for _ in range(length))
    return random_hash


T = TypeVar("T")


def select_item(
    items: list[T],
    display_fn: Callable[[T], str] = str,
    title: str = "Selecione um item",
) -> T | None:
    """
    Exibe uma lista de itens e permite selecionar um.
    Retorna o item escolhido ou None caso o usuário escolha voltar.

    :param items: Lista de itens para selecionar
    :param display_fn: Função que recebe um item e retorna a string a ser exibida
    :param titulo: Texto exibido antes da lista
    """
    if not items:
        print(f"\nNenhum item disponível em '{title}'.")
        return None

    print(f"\n{title}:")
    for i, item in enumerate(items, start=1):
        print(f"{i}. {display_fn(item)}")
    print("0. Voltar")

    while True:
        try:
            escolha = int(input("\nDigite o número da opção: ").strip())
            if escolha == 0:
                return None
            elif 1 <= escolha <= len(items):
                return items[escolha - 1]
            else:
                print("Opção inválida, tente novamente.")
        except ValueError:
            print("Entrada inválida, digite um número.")


def read_date() -> datetime.date:
    while True:
        date_str = input("Digite a data (YYYY-MM-DD): ")

        try:
            combined_str = f"{date_str}"
            scheduled_datetime = datetime.datetime.strptime(
                combined_str, "%Y-%m-%d"
            ).date()
            return scheduled_datetime
        except ValueError:
            print("Formato de data inválido. Tente novamente.\n")


def read_time() -> datetime.time:
    while True:
        time_str = input("Horário da turma (HH:MM): ").strip()
        try:
            hour, minute = map(int, time_str.split(":"))
            return datetime.time(hour, minute)
        except Exception:
            print("Formato inválido. Use HH:MM, por exemplo 14:30.\n")
