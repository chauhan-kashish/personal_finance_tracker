from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum
from .models import Category, Income, Expense
from .forms import IncomeForm, ExpenseForm
from collections import defaultdict
import datetime
import json


def home(request):
    return render(request, 'home.html')

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            inc = form.save(commit=False)
            inc.user = request.user
            inc.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'finance/add_income.html', {'form': form})

@login_required
def edit_income(request, pk):
    income = Income.objects.filter(pk=pk, user=request.user).first()
    if not income:
        messages.error(request, 'Income not found.')
        return redirect('view_transactions')
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully.')
            return redirect('view_transactions')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'finance/edit_income.html', {'form': form, 'income': income})

@login_required
def delete_income(request, pk):
    income = Income.objects.filter(pk=pk, user=request.user).first()
    if not income:
        messages.error(request, 'Income not found.')
        return redirect('view_transactions')
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted successfully.')
        return redirect('view_transactions')
    return render(request, 'finance/delete_income.html', {'income': income})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
    return render(request, 'finance/add_expense.html', {'form': form})

@login_required
def edit_expense(request, pk):
    expense = Expense.objects.filter(pk=pk, user=request.user).first()
    if not expense:
        messages.error(request, 'Expense not found.')
        return redirect('view_transactions')
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('view_transactions')
    else:
        form = ExpenseForm(instance=expense)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
    return render(request, 'finance/edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, pk):
    expense = Expense.objects.filter(pk=pk, user=request.user).first()
    if not expense:
        messages.error(request, 'Expense not found.')
        return redirect('view_transactions')
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
        return redirect('view_transactions')
    return render(request, 'finance/delete_expense.html', {'expense': expense})

@login_required
def view_transactions(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')[:20]
    expenses = Expense.objects.filter(user=request.user).order_by('-date')[:20]
    return render(request, 'finance/view_transactions.html', {'incomes': incomes, 'expenses': expenses})

@login_required
def reports(request):
    """
    Render the reports page with:
      - total_income, total_expense, balance
      - category_labels & category_values for pie chart (expenses by category)
      - trend_labels, trend_incomes, trend_expenses for line chart (by date)
    """
    # simple totals
    total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    # ---- Expense by category (pie chart) ----
    cat_qs = (
        Expense.objects.filter(user=request.user)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    category_labels = []
    category_values = []
    for row in cat_qs:
        name = row['category__name'] or 'Uncategorized'
        category_labels.append(str(name))
        # convert Decimal to float for JSON/Chart.js compatibility
        category_values.append(float(row['total'] or 0))

    # ---- Income vs Expense over time (line chart) ----
    inc_qs = (
        Income.objects.filter(user=request.user)
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )
    exp_qs = (
        Expense.objects.filter(user=request.user)
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    inc_by_date = {row['date']: float(row['total'] or 0) for row in inc_qs}
    exp_by_date = {row['date']: float(row['total'] or 0) for row in exp_qs}

    # union and sort dates
    dates = sorted(set(list(inc_by_date.keys()) + list(exp_by_date.keys())))
    labels = [d.strftime('%b %d, %Y') for d in dates]
    incomes_list = [inc_by_date.get(d, 0.0) for d in dates]
    expenses_list = [exp_by_date.get(d, 0.0) for d in dates]

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        # chart data
        'category_labels': category_labels,
        'category_values': category_values,
        'trend_labels': labels,
        'trend_incomes': incomes_list,
        'trend_expenses': expenses_list,
    }
    return render(request, 'finance/reports.html', context)

@login_required
def add_category(request):
    """
    Simple page-based category creation.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, "Category name cannot be empty.")
        else:
            Category.objects.create(user=request.user, name=name)
            messages.success(request, f"Category '{name}' created.")
            return redirect('add_expense')
    return render(request, 'finance/add_category.html')

@login_required
@require_POST
def add_category_ajax(request):
    """
    AJAX endpoint to create a category and return JSON.
    Accepts form-encoded POST with 'name'.
    Useful for modal/AJAX UX.
    """
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'success': False, 'error': 'Category name cannot be empty.'}, status=400)

    # Prevent duplicate names for the same user (case-insensitive)
    existing = Category.objects.filter(user=request.user, name__iexact=name).first()
    if existing:
        return JsonResponse({'success': True, 'id': existing.id, 'name': existing.name, 'message': 'Category already exists.'})

    cat = Category.objects.create(user=request.user, name=name)
    return JsonResponse({'success': True, 'id': cat.id, 'name': cat.name})

