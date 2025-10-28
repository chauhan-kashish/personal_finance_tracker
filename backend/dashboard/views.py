from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from finance.models import Income, Expense
from django.db.models import Sum

@login_required
def dashboard(request):
    total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    recent_income = Income.objects.filter(user=request.user).order_by('-date')[:5]
    recent_expense = Expense.objects.filter(user=request.user).order_by('-date')[:5]

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_income': recent_income,
        'recent_expense': recent_expense,
    }
    return render(request, 'dashboard/dashboard.html', context)
