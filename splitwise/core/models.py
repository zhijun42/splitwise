from collections import defaultdict

from django.db import models
from splitwise.core.solver import Solver
from splitwise.core.utils import reverse_balance_graph, show_final_results, cast_to_balance_string
from splitwise.core.types import BalanceGraph


class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"User ID: {self.user_id} Name: {self.name}"


class Expense(models.Model):
    expense_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=20)
    balance = models.CharField(max_length=200, default="")

    @property
    def balance_graph(self) -> BalanceGraph:
        balance_graph = defaultdict(lambda: defaultdict(lambda: 0))
        for expense_split in str(self.balance).split("|"):
            if expense_split == "":
                continue
            user_id_that_owes, user_id_that_pays, money_amount_str = expense_split.split(",")
            balance_graph[user_id_that_owes][user_id_that_pays] = float(money_amount_str)
        return balance_graph

    def __str__(self):
        return f"Expense ID: {self.expense_id}, Title: {self.title}, Balance: {self.balance}"

    def update(self, new_expense: "Expense", group: "Group") -> None:
        """
        Save the updated expense to DB, compute the delta balance to update the
        corresponding group, and then also save the updated group to DB.
        """
        delta_balance_graph = self.find_delta_balance_graph(new_expense)
        self.balance = new_expense.balance
        # self.save()

        # Hacky!!
        # group = Group.objects.get(group_id=group_id)
        group.add_delta_balance_graph(delta_balance_graph)

    def find_delta_balance_graph(self, updated_expense: "Expense") -> BalanceGraph:
        """
        Compare the current balance and the updated balance for this given expense
        to compute the net change.
        :param updated_expense:
        :return:
        """
        reversed_balance_graph = reverse_balance_graph(self.balance_graph)
        solver = Solver(reversed_balance_graph)
        delta_balance_graph = solver.combine_balance_graphs(updated_expense.balance_graph)
        return delta_balance_graph


class Group(models.Model):
    group_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=20)
    balance = models.CharField(max_length=200, default="")

    @property
    def balance_graph(self) -> BalanceGraph:
        balance_graph = defaultdict(lambda: defaultdict(lambda: 0))
        for expense_split in str(self.balance).split("|"):
            if expense_split == "":
                continue
            user_id_that_owes, user_id_that_pays, money_amount_str = expense_split.split(",")
            balance_graph[user_id_that_owes][user_id_that_pays] = float(money_amount_str)
        return balance_graph

    def __str__(self):
        return f"Group ID: {self.group_id}, Title: {self.title}, Balance: {self.balance}"

    def show_balance(self):
        return show_final_results(self.balance_graph)

    def add_delta_balance_graph(self, delta_balance_graph: BalanceGraph) -> None:
        """
        Every time we add, update or delete an Expense, we create a net delta balance
        graph to be used by the Group to compute the latest status of balance.
        :param delta_balance_graph: The net delta balance graph to be combined
        """
        solver = Solver(self.balance_graph)
        combined_balance_graph = solver.combine_balance_graphs(delta_balance_graph)
        self.balance = cast_to_balance_string(combined_balance_graph)
        # self.save()

    # Deprecated
    def add_expense(self, new_expense: Expense) -> None:
        solver = Solver(self.balance_graph)
        combined_balance_graph = solver.combine_balance_graphs(new_expense.balance_graph)
        self.balance = cast_to_balance_string(combined_balance_graph)
