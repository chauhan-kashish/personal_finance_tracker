from django import forms
from .models import Income, Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount','source','category','date','note']
        widgets = {'date': forms.DateInput(attrs={'type':'date'})}

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount','category','date','note']
        widgets = {'date': forms.DateInput(attrs={'type':'date'})}
