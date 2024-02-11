from django.http import JsonResponse
from rest_framework.decorators import api_view

from splitwise.core.models import Expense, Group


@api_view(["GET"])
def hello(request):
    return JsonResponse(data={"message": "Welcome to my version of Splitwise!"}, status=200)


@api_view(["POST"])
def update_expense(request):
    expense_id = ""
    group_id = ""
    original_expense: Expense = Expense.objects.get(expense_id=expense_id)
    group = Group.objects.get(group_id=group_id)

    # Use the request body to construct the edited expense
    updated_expense = Expense()

    original_expense.update(updated_expense, group)
    return JsonResponse(data={"Successfully updated the expense and group"}, status=200)
