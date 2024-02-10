from splitwise.models import Expense, User, Group


if __name__ == '__main__':
    data = {
        "B": {"A": 20, "C": 40},
        "C": {"A": 20, "B": 30},
        "A": {"B": 30, "C": 40}
    }

    user_A = User("A")
    user_B = User("B")
    user_C = User("C")

    test_group = Group("TestGroup")
    test_group.add_user(user_A)
    test_group.add_user(user_B)
    test_group.add_user(user_C)

    # 30 / 60 / 90 = $60 per User
    expense_1 = Expense({
        user_B.id: {user_A.id: 14},
        user_C.id: {user_A.id: 14},
    })
    test_group.add_expense(expense_1)
    print("[1]: ", test_group.show_balance())

    expense_2 = Expense({
        user_A.id: {user_B.id: 20},
        user_C.id: {user_B.id: 20},
    })
    test_group.add_expense(expense_2)
    print("[2]: ", test_group.show_balance())

    expense_3 = Expense({
        user_A.id: {user_C.id: 30},
        user_B.id: {user_C.id: 30}
    })
    test_group.add_expense(expense_3)
    print("[3]: ", test_group.show_balance())

    new_expense_1 = Expense({
        user_B.id: {user_A.id: 10},
        user_C.id: {user_A.id: 10},
    })
    test_group.update_expense(expense_1, new_expense_1)
    print("[4]:", test_group.show_balance())