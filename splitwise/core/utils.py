from collections import defaultdict
from typing import Set, Tuple

from splitwise.core.types import BalanceGraph, UserId, MoneyAmount


def reverse_balance_graph(graph: BalanceGraph) -> BalanceGraph:
    reversed_graph = defaultdict(lambda: defaultdict(lambda: .0))
    for user_that_owes, user_balance in graph.items():
        for user_that_pays, money_amount in user_balance.items():
            reversed_graph[user_that_pays][user_that_owes] = money_amount
    return reversed_graph


def show_final_results(graph: BalanceGraph) -> Set[Tuple[UserId, UserId, MoneyAmount]]:
    results = set()
    for out_node, in_nodes in graph.items():
        for in_node, money_amount in in_nodes.items():
            if money_amount == 0:
                continue

            # TODO(zhijun): I don't know why this number is sometimes more than 2 digits
            money_amount = round(money_amount, 2)
            results.add((out_node, in_node, money_amount))
    return results


def cast_to_balance_string(balance_graph: BalanceGraph) -> str:
    balance_string_pairs = []
    for user_that_owes, user_balances in balance_graph.items():
        for user_that_pays, money_amount in user_balances.items():
            if money_amount == 0:
                continue

            balance_string_pairs.append(f"{user_that_owes},{user_that_pays},{money_amount}")
    return "|".join(balance_string_pairs)
