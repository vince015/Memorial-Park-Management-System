from django import forms
from dal import autocomplete

from memorial_park_mgmnt_app import models


class DownpaymentForm(forms.ModelForm):

    class Meta:
        model = models.Downpayment
        fields = [
                    'date',
                    'amount',
                    'remarks'
                ]
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y',
                                    attrs={'class': 'form-control datepicker',
                                           'placeholder': 'Date'}),
            'amount': forms.NumberInput(attrs={'step': 0.01,
                                               'min': 0.00,
                                               'value': 0.00,
                                               'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }


class CommissionForm(forms.ModelForm):

    class Meta:
        model = models.Commission
        fields = [
                    'date',
                    'amount',
                    'remarks'
                ]
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y',
                                    attrs={'class': 'form-control datepicker',
                                           'placeholder': 'Date'}),
            'amount': forms.NumberInput(attrs={'step': 0.01,
                                               'min': 0.00,
                                               'value': 0.00,
                                               'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }


class ClientForm(forms.ModelForm):

    class Meta:
        model = models.Client
        fields = [
                    'last_name',
                    'first_name',
                    'middle_name',
                    'house_number',
                    'street',
                    'barangay',
                    'town',
                    'province',
                    'valid_id',
                    'birthdate',
                    'contact_number',
                    'email',
                    'other_address',
                    'business_name',
                    'business_address',
                ]
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Last Name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Middle Name'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'House #'}),
            'street': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Street'}),
            'barangay': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Barangay'}),
            'town': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Town'}),
            'province': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Province'}),
            'valid_id': forms.FileInput(attrs={'class': 'form-control',
                                               'placeholder': 'Valid ID'}),
            'birthdate': forms.DateInput(format='%m/%d/%Y',
                                         attrs={'class': 'form-control datepicker',
                                                'placeholder': 'Date'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Email'}),
            'other_address': forms.Textarea(attrs={'class': 'form-control',
                                                   'rows': 3,
                                                   'placeholder': 'Other Address'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Business Name'}),
            'business_address': forms.Textarea(attrs={'class': 'form-control',
                                                      'rows': 3,
                                                      'placeholder': 'Other Address'}),
        }


class AgentForm(forms.ModelForm):

    class Meta:
        model = models.Agent
        fields = [
                    'last_name',
                    'first_name',
                    'middle_name',
                    'house_number',
                    'street',
                    'barangay',
                    'town',
                    'province',
                    'valid_id',
                    'birthdate',
                    'contact_number',
                    'email',
                    'other_address',
                    'business_name',
                    'business_address',
                ]
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Last Name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Middle Name'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'House #'}),
            'street': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Street'}),
            'barangay': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Barangay'}),
            'town': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Town'}),
            'province': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Province'}),
            'valid_id': forms.FileInput(attrs={'class': 'form-control',
                                               'placeholder': 'Valid ID'}),
            'birthdate': forms.DateInput(format='%m/%d/%Y',
                                         attrs={'class': 'form-control datepicker',
                                                'placeholder': 'Date'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Email'}),
            'other_address': forms.Textarea(attrs={'class': 'form-control',
                                                   'rows': 3,
                                                   'placeholder': 'Other Address'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Business Name'}),
            'business_address': forms.Textarea(attrs={'class': 'form-control',
                                                      'rows': 3,
                                                      'placeholder': 'Other Address'}),
        }

class ContractForm(forms.ModelForm):

    class Meta:
        model = models.Contract
        fields = [
                    'date',
                    'lot',
                    'buyer_type',
                    'lot_price',
                    'care_fund',
                    'discount_spot_cash',
                    'discount_spot_dp',
                    'interest_on_installment',
                    'certificate_of_ownership',
                    'change_of_title',
                    'interment',
                    'reservation_loi',
                    'spot_cash_payment',
                    'remarks'
                ]
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y',
                                    attrs={'class': 'form-control datepicker',
                                           'placeholder': 'Date'}),
            'lot': autocomplete.ListSelect2(url='lot_autocomplete',
                                             attrs={'class': 'form-control'}),
            'buyer_type': forms.Select(attrs={'class': 'form-control',
                                              'placeholder': 'Buyer Type'}),
            'lot_price': forms.NumberInput(attrs={'step': 0.01,
                                                  'min': 0.00,
                                                  'value': 0.00,
                                                  'class': 'form-control'}),
            'care_fund': forms.NumberInput(attrs={'step': 0.01,
                                                  'min': 0.00,
                                                  'value': 0.00,
                                                  'class': 'form-control'}),
            'discount_spot_cash': forms.NumberInput(attrs={'step': 0.01,
                                                           'min': 0.00,
                                                           'value': 0.00,
                                                           'class': 'form-control'}),
            'discount_spot_dp': forms.NumberInput(attrs={'step': 0.01,
                                                           'min': 0.00,
                                                           'value': 0.00,
                                                           'class': 'form-control'}),
            'interest_on_installment': forms.NumberInput(attrs={'step': 0.01,
                                                           'min': 0.00,
                                                           'value': 0.00,
                                                           'class': 'form-control'}),
            'certificate_of_ownership': forms.NumberInput(attrs={'step': 0.01,
                                                           'min': 0.00,
                                                           'value': 0.00,
                                                           'class': 'form-control'}),
            'change_of_title': forms.NumberInput(attrs={'step': 0.01,
                                                        'min': 0.00,
                                                        'value': 0.00,
                                                        'class': 'form-control'}),
            'interment': forms.NumberInput(attrs={'step': 0.01,
                                                           'min': 0.00,
                                                           'value': 0.00,
                                                           'class': 'form-control'}),
            'reservation_loi': forms.NumberInput(attrs={'step': 0.01,
                                                           'min': 0.00,
                                                           'value': 0.00,
                                                           'class': 'form-control'}),
            'spot_cash_payment': forms.NumberInput(attrs={'step': 0.01,
                                                           'min': 0.00,
                                                           'value': 0.00,
                                                           'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }
