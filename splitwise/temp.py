import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'splitwise.settings')
django.setup()

from splitwise.core.models import Expense, User, Group


if __name__ == '__main__':
    user_A = User(name="A")
    user_B = User(name="B")
    user_C = User(name="C")
    test_group = Group(title="TestGroup")

    # 30 / 60 / 90 = $60 per User
    expense_1 = Expense(balance="B,A,14|C,A,14")
    test_group.add_delta_balance_graph(expense_1.balance_graph)
    print("[1]: ", test_group.show_balance())

    expense_2 = Expense(balance="A,B,20|C,B,20")
    test_group.add_delta_balance_graph(expense_2.balance_graph)
    print("[2]: ", test_group.show_balance())

    expense_3 = Expense(balance="A,C,30|B,C,30")
    test_group.add_delta_balance_graph(expense_3.balance_graph)
    print("[3]: ", test_group.show_balance())

    updated_expense_1 = Expense(balance="B,A,10|C,A,10")
    expense_1.update(updated_expense_1, test_group)
    print("[4]:", test_group.show_balance())
