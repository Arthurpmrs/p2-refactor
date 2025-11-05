import datetime
import random
import string
from typing import Callable, TypeVar

from exceptions import InvalidExamDate, InvalidMenuOptionException


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
                raise InvalidMenuOptionException()
        except (ValueError, InvalidMenuOptionException):
            print("Entrada inválida. Digite um número dentro das opções.")


def read_date() -> datetime.date:
    while True:
        date_str = input("Digite a data (YYYY-MM-DD): ")

        try:
            combined_str = f"{date_str}"
            scheduled_datetime = datetime.datetime.strptime(
                combined_str, "%Y-%m-%d"
            ).date()

            if scheduled_datetime < datetime.date.today():
                raise InvalidExamDate("Data deve ser no futuro.")

            return scheduled_datetime
        except ValueError:
            print("Formato de data inválido. Tente novamente.\n")
        except InvalidExamDate as e:
            print(f"{e}\n")


def read_time() -> datetime.time:
    while True:
        time_str = input("Horário da turma (HH:MM): ").strip()
        try:
            hour, minute = map(int, time_str.split(":"))
            return datetime.time(hour, minute)
        except ValueError:
            print("Formato inválido. Use HH:MM, por exemplo 14:30.\n")


def read_non_empty_string(prop_name: str) -> str:
    while True:
        name = input(f"{prop_name}: ").strip()

        if len(name) == 0:
            print(f"{prop_name} não pode ser vazio.\n")
            continue

        return name


def select_multiple_options(collection: list[T]) -> list[T]:
    while True:
        entrada = input("Digite os números separados por vírgula (ex: 1,3,5): ").strip()
        try:
            indices = [int(x) for x in entrada.split(",") if x.strip()]
            if not indices:
                raise ValueError
            if all(1 <= idx <= len(collection) for idx in indices):
                return [collection[idx - 1] for idx in indices]
            else:
                print("Algum número está fora da lista. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Use números separados por vírgula.")
