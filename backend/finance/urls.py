from django.urls import path
from . import views

urlpatterns = [
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('transactions/', views.view_transactions, name='view_transactions'),
    path('reports/', views.reports, name='reports'),

    # 👇 this line is the key
    path('categories/add/', views.add_category, name='add_category'),
]
