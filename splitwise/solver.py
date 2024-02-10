from collections import defaultdict
import logging
from math import floor
from typing import Dict, Set, Tuple

from splitwise.types import UserId, BalanceGraph, MoneyAmount
from splitwise.utils import show_final_results


MAX_ITERATIONS = 5

logger = logging.getLogger(__name__)


class Solver:
    def __init__(self, balance_graph: BalanceGraph = None) -> None:

        self.graph: BalanceGraph
        if balance_graph is None:
            self.graph = defaultdict(lambda: defaultdict(lambda: 0))
        else:
            self.graph = balance_graph

    def get_balance(self) -> BalanceGraph:
        return self.graph

    def _find_transient_nodes(self) -> Set[Tuple[UserId, UserId, UserId]]:
        """
        A transient node is one with both incoming and outgoing edges
        :return:
        """
        redundant_edges = set()
        for user_that_owes in self.graph:
            for user_that_pays, money_amount in self.graph[user_that_owes].items():
                if money_amount == 0:
                    continue

                for further_in_node, secondary_money_amount in self.graph[user_that_pays].items():
                    if secondary_money_amount == 0:
                        continue

                    redundant_edges.add((user_that_owes, user_that_pays, further_in_node))
        logger.error(f"Redundant edges: {redundant_edges}")
        return redundant_edges

    # @staticmethod
    def combine_balance_graphs(self, new_graph: BalanceGraph) -> None:
        print("Before merging", show_final_results(self.graph))
        for user_that_owes in new_graph:
            for user_that_pays, money_amount in new_graph[user_that_owes].items():
                self._add_expense(user_that_owes, user_that_pays, money_amount)

        # Doing the erasing on the fly
        self._erase_redundant_edges_amount_three_nodes()
        print("After merging", show_final_results(self.graph))

    # def _new_add_expense(graph, user_that_owes: UserId, user_that_pays: UserId, money_amount: MoneyAmount) -> None:
    #     print(f"[{user_that_owes}] owes [{user_that_pays}] amount of [{money_amount}]")
    #     graph[user_that_owes][user_that_pays] += money_amount
    #     total_owe_amount = graph[user_that_owes][user_that_pays]
    #     reversed_amount = graph[user_that_pays][user_that_owes]
    #     if reversed_amount > 0:
    #         redundant_amount = min(total_owe_amount, reversed_amount)
    #         graph[user_that_owes][user_that_pays] -= redundant_amount
    #         graph[user_that_pays][user_that_owes] -= redundant_amount

    def _add_expense(self, user_that_owes: UserId, user_that_pays: UserId, money_amount: MoneyAmount) -> None:
        print(f"[{user_that_owes}] owes [{user_that_pays}] amount of [{money_amount}]")
        self.graph[user_that_owes][user_that_pays] += money_amount
        total_owe_amount = self.graph[user_that_owes][user_that_pays]
        reversed_amount = self.graph[user_that_pays][user_that_owes]
        if reversed_amount > 0:
            redundant_amount = min(total_owe_amount, reversed_amount)
            self.graph[user_that_owes][user_that_pays] -= redundant_amount
            self.graph[user_that_pays][user_that_owes] -= redundant_amount

    def split_transaction_among_users(self, users_that_owe, user_that_pays, money_amount) -> None:
        amount_each_user_owes = floor(money_amount / (len(users_that_owe) + 1) * 100) / 100
        for user_that_owes in users_that_owe:
            self._add_expense(user_that_owes, user_that_pays, amount_each_user_owes)

    def erase_redundant_edges_between_two_nodes(self) -> None:
        for out_node, in_nodes in self.graph.items():
            for in_node, money_amount in in_nodes.items():
                if money_amount == 0:
                    continue

                reversed_money_amount = self.graph[in_node][out_node]
                if reversed_money_amount == 0:
                    continue

                redundant_amount = min(money_amount, reversed_money_amount)
                self.graph[out_node][in_node] -= redundant_amount
                self.graph[in_node][out_node] -= redundant_amount

    def _erase_redundant_edges_amount_three_nodes(self) -> None:
        num_iteration = 0
        while num_iteration < MAX_ITERATIONS:
            num_iteration += 1
            transient_nodes_pairs = self._find_transient_nodes()
            if not transient_nodes_pairs:
                return

            logger.error(f"Before erasing: {show_final_results(self.graph)}")
            for pair in transient_nodes_pairs:
                out_node_user_id, in_node, further_in_node = pair
                source_node_out_amount = self.graph[out_node_user_id][in_node]
                transient_node_out_amount = self.graph[in_node][further_in_node]

                if source_node_out_amount < transient_node_out_amount:
                    self.graph[out_node_user_id][in_node] = 0
                    self.graph[out_node_user_id][further_in_node] += source_node_out_amount
                    self.graph[in_node][further_in_node] -= source_node_out_amount
                elif source_node_out_amount > transient_node_out_amount:
                    self.graph[in_node][further_in_node] = 0
                    self.graph[out_node_user_id][in_node] -= transient_node_out_amount
                    self.graph[out_node_user_id][further_in_node] += transient_node_out_amount
                else:
                    self.graph[out_node_user_id][in_node] = 0
                    self.graph[in_node][further_in_node] = 0
                    self.graph[out_node_user_id][further_in_node] += source_node_out_amount
            logger.error(f"After erasing: {show_final_results(self.graph)}")
