from collections import defaultdict
from typing import Set, Tuple

from splitwise.types import BalanceGraph, UserId, MoneyAmount


def reverse_balance_graph(graph: BalanceGraph) -> BalanceGraph:
    reversed_graph = defaultdict(lambda: defaultdict(lambda: 0))
    for user_that_owes, user_balance in graph.items():
        for user_that_pays, money_amount in user_balance.items():
            reversed_graph[user_that_pays][user_that_owes] = money_amount
    return reversed_graph


def show_final_results(graph: BalanceGraph, showcase=False) -> Set[Tuple[UserId, UserId, MoneyAmount]]:
    results = set()
    for out_node, in_nodes in graph.items():
        for in_node, money_amount in in_nodes.items():
            if money_amount == 0:
                continue

            # TODO(zhijun): I don't know why this number is sometimes more than 2 digits
            money_amount = round(money_amount, 2)
            # if showcase:
            #     results.add((str(out_node), str(in_node), money_amount))
            # else:
            results.add((out_node, in_node, money_amount))
    return results
