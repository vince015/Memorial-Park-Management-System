from django import forms

from expense_report import models


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = models.Expense
        fields = [
                    'date',
                    'reference_number',
                    'payee',
                    'amount',
                    'category',
                    'from_petty_cash',
                    'description'
                ]
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y',
                                    attrs={'class': 'form-control datepicker',
                                           'placeholder': 'Date'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Reference Number'}),
            'payee': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Payee'}),
            'amount': forms.NumberInput(attrs={'step': 0.01,
                                               'min': 0.00,
                                               'value': 0.00,
                                               'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control',
                                            'placeholder': 'Category'}),
            'from_petty_cash': forms.CheckboxInput(),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 3,
                                                 'placeholder': 'Description'}),
        }
