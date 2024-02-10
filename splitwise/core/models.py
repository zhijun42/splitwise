from collections import defaultdict

from django.db import models
from splitwise.core.solver import Solver
from splitwise.core.utils import reverse_balance_graph, show_final_results
from splitwise.core.types import UserId, BalanceGraph

MAX_ITERATIONS = 5


class User(models.Model):

    user_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"My ID is {self.user_id}"


class Expense(models.Model):

    expense_id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=20)
    balance = models.CharField(max_length=200)

    # def __init__(self, balance=None):
    #     # self.title = ""
    #     # self.paid_date = ""
    #     # self.added_date = ""
    #     if balance:
    #         self.balance = balance
    #     else:
    #         self.balance: BalanceGraph = defaultdict(lambda: defaultdict(lambda: 0))

    def update(self, new_expense: "Expense") -> None:
        """ What to do here??"""
        # self.balance = new_expense.balance
        return

    def find_delta_graph(self, updated_expense: "Expense") -> BalanceGraph:
        """
        Compare the current balance and the updated balance for this given expense
        to compute the net change.
        :param updated_expense:
        :return:
        """
        reversed_balance_graph = reverse_balance_graph(self.balance)
        solver = Solver(reversed_balance_graph)
        solver.combine_balance_graphs(updated_expense.balance)
        self.balance = solver.get_balance()
        return self.balance


class Group(models.Model):

    group_id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=20)
    balance = models.CharField(max_length=200)

    # def __init__(self, title=None):
    #     self.title = title
    #     self.user_ids = []
    #     self.balance = defaultdict(lambda: defaultdict(lambda: 0))
    #
    # def add_user(self, user_id: UserId) -> None:
    #     self.user_ids.append(user_id)

    def show_balance(self):
        return show_final_results(self.balance)

    def add_expense(self, new_expense: Expense) -> None:
        solver = Solver(self.balance)
        solver.combine_balance_graphs(new_expense.balance)
        self.balance = solver.get_balance()

    def update_expense(self, original_expense: Expense, updated_expense: Expense) -> None:
        original_expense.update(updated_expense)
        delta_graph = original_expense.find_delta_graph(updated_expense)
        solver = Solver(self.balance)
        solver.combine_balance_graphs(delta_graph)
        self.balance = solver.get_balance()
