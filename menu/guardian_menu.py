from menu import UserMenuStrategy
from system import Guardian, PaymentMethod


class GuardianMenuStrategy(UserMenuStrategy):
    guardian: Guardian

    def __init__(self, guardian: Guardian):
        super().__init__()
        self.guardian = guardian
        self.menu_title = f"👪 Bem-vindo, {self.guardian.name}!"

    def show_menu_options(self):
        print("\n--- Menu do Responsável ---")
        print("1. Consultar dados do aluno")
        print("2. Pagar mensalidade")
        print("3. Rastrear transporte escolar")

    def match_option_to_function(self, selected_option: str) -> bool:
        match selected_option:
            case "1":
                self.school.consultar_dados_aluno(self.guardian.student)
            case "2":
                print("💳 Formas de pagamento: PIX | Cartão | Boleto")
                forma_pagamento = input("Digite a forma de pagamento: ")
                try:
                    payment_method = PaymentMethod[forma_pagamento.upper()]
                    self.school.processar_pagamento(
                        self.guardian.student, payment_method
                    )
                except Exception:
                    print("Opção inválida.")
            case "3":
                self.school.rastrear_transporte(self.guardian.student)
            case _:
                print("Opção inválida.")

        return True
