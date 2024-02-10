import pytest

from splitwise.models import User, Solver, Group, Expense
from splitwise.utils import show_final_results


class TestResolver:
    def test_simple_example(self):
        user_A = User("A")
        user_B = User("B")
        user_C = User("C")

        group = Group("Simple Example")

        expense_1 = Expense({
            user_B: {user_A: 20},
            user_C: {user_A: 20}
        })
        expense_2 = Expense({
            user_A: {user_B: 30},
            user_C: {user_B: 30}
        })
        expense_3 = Expense({
            user_A: {user_C: 40},
            user_B: {user_C: 40}
        })
        group.add_expense(expense_1)
        group.add_expense(expense_2)
        group.add_expense(expense_3)

        # solver = Solver()
        # solver._add_expense(user_B, user_A, 20)
        # solver._add_expense(user_C, user_A, 20)
        # solver._add_expense(user_A, user_B, 30)
        # solver._add_expense(user_C, user_B, 30)
        # solver._add_expense(user_A, user_C, 40)
        # solver._add_expense(user_B, user_C, 40)

        actual = group.show_balance()
        expected = {(user_A, user_C, 30)}
        assert actual == expected

    #
    # def test_april_30_mammoth(self):
    #     ying = User("ying")
    #     xiang = User("xiang")
    #     bruce = User("bruce")
    #
    #     solver = Solver()
    #     solver._add_expense(ying, bruce, 14)
    #     solver._add_expense(xiang, bruce, 14)
    #     solver._add_expense(ying, bruce, 19.67)
    #     solver._add_expense(xiang, bruce, 19.67)
    #     solver._add_expense(ying, bruce, 19)
    #     solver._add_expense(xiang, bruce, 19)
    #     solver._add_expense(ying, bruce, 27)
    #
    #     solver._erase_redundant_edges_amount_three_nodes()
    #     actual = show_final_results()
    #     expected = {(ying, bruce, 79.67), (xiang, bruce, 52.67)}
    #     assert actual == expected
    #
    #
    # def test_steamboat_trip(self):
    #     chiheng = User("chiheng")
    #     ying = User("ying")
    #     xiang = User("xiang")
    #     bruce = User("bruce")
    #     yuan = User("yuan")
    #     except_chiheng = [ying, xiang, bruce, yuan]
    #     except_bruce = [chiheng, ying, xiang, yuan]
    #
    #     solver = Solver()
    #     solver.split_transaction_among_users(except_chiheng, chiheng, 123)
    #     solver.split_transaction_among_users(except_chiheng, chiheng, 106)
    #     solver.split_transaction_among_users(except_chiheng, chiheng, 429)
    #     solver.split_transaction_among_users([yuan, xiang], chiheng, 24.68)
    #     solver.split_transaction_among_users([yuan], xiang, 42.21)
    #     solver.split_transaction_among_users(except_chiheng, chiheng, 126)
    #     solver.split_transaction_among_users([chiheng, ying, bruce, yuan], xiang, 115.18)
    #     solver.split_transaction_among_users(except_bruce, bruce, 30.77)
    #     solver.split_transaction_among_users(except_chiheng, chiheng, 1609)
    #     solver.split_transaction_among_users(except_chiheng, chiheng, 100)
    #     solver.split_transaction_among_users(except_bruce, bruce, 147)
    #     solver.split_transaction_among_users(except_bruce, bruce, 59.94)
    #     solver.split_transaction_among_users(except_chiheng, chiheng, 16)
    #
    #     solver._erase_redundant_edges_amount_three_nodes()
    #     actual = show_final_results()
    #     expected = {(ying, chiheng, 572.36), (bruce, chiheng, 334.71), (yuan, chiheng, 601.68), (xiang, chiheng, 444.33)}
    #     assert actual == expected
