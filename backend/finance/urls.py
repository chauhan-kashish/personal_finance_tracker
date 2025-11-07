from django.urls import path
from . import views

urlpatterns = [
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('income/<int:pk>/edit/', views.edit_income, name='edit_income'),
    path('income/<int:pk>/delete/', views.delete_income, name='delete_income'),
    path('expense/<int:pk>/edit/', views.edit_expense, name='edit_expense'),
    path('expense/<int:pk>/delete/', views.delete_expense, name='delete_expense'),
    path('transactions/', views.view_transactions, name='view_transactions'),
    path('reports/', views.reports, name='reports'),

    # 👇 this line is the key
    path('categories/add/', views.add_category, name='add_category'),
]
