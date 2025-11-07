from django import forms
from .models import Income, Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount','source','date','note']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            # Render amount as a text field to avoid browser spin buttons,
            # still validated as Decimal by the form field
            'amount': forms.TextInput(attrs={
                'inputmode': 'decimal',
                'placeholder': '0.00',
            }),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount','category','date','note']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'amount': forms.TextInput(attrs={
                'inputmode': 'decimal',
                'placeholder': '0.00',
            }),
        }
