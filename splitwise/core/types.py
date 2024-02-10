from typing import Dict

UserId = str
MoneyAmount = float

# A core structure for our application.
# The expenses are represented as a directed graph where a node
# represents a user and an edge from node A to node B with value X
# represents that user A owes X amount of money to user B.
# This graph is stored as a dictionary, for example
# {
#     "B": {"A": 20, "C": 40},
#     "C": {"A": 20, "B": 30}
# }
# where user B owes 20 to user A, and 40 to user C.
BalanceGraph = Dict[UserId, Dict[UserId, MoneyAmount]]
