from django import forms

from memorial_park_mgmnt_app import models


class ClientForm(forms.ModelForm):

    class Meta:
        model = models.Client
        fields = [
                    'last_name',
                    'first_name',
                    'middle_name',
                    'mobile',
                    'landline',
                    'email',
                    'house_number',
                    'street',
                    'barangay',
                    'town',
                    'province',
                    'valid_id',
                    'birthdate',
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
            'mobile': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': '(+63) 999 999 9999',
                                             'data-inputmask': '"mask": ["(+63) 999 999 9999"]',
                                             'data-mask': True}),
            'landline': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': '(044) 999 9999',
                                               'data-inputmask': '"mask": ["(999) 999 9999"]',
                                               'data-mask': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Email'}),
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
            'other_address': forms.Textarea(attrs={'class': 'form-control',
                                                   'rows': 3,
                                                   'placeholder': 'Other Address'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Business Name'}),
            'business_address': forms.Textarea(attrs={'class': 'form-control',
                                                      'rows': 3,
                                                      'placeholder': 'Other Address'}),
        }

    def clean(self):
        if not self.cleaned_data['mobile'] and not self.cleaned_data['landline']:
            raise forms.ValidationError({'mobile': ['Enter at least one contact number (mobile or landline)'],
                                         'landline': ['Enter at least one contact number (mobile or landline)']})


class AgentForm(forms.ModelForm):

    class Meta:
        model = models.Agent
        fields = [
                    'last_name',
                    'first_name',
                    'middle_name',
                    'mobile',
                    'landline',
                    'email',
                    'house_number',
                    'street',
                    'barangay',
                    'town',
                    'province',
                    'valid_id',
                    'birthdate',
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
            'mobile': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': '(+63) 999 999 9999',
                                             'data-inputmask': '"mask": ["(+63) 999 999 9999"]',
                                             'data-mask': True}),
            'landline': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': '(044) 999 9999',
                                               'data-inputmask': '"mask": ["(999) 999 9999"]',
                                               'data-mask': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Email'}),
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
            'other_address': forms.Textarea(attrs={'class': 'form-control',
                                                   'rows': 3,
                                                   'placeholder': 'Other Address'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Business Name'}),
            'business_address': forms.Textarea(attrs={'class': 'form-control',
                                                      'rows': 3,
                                                      'placeholder': 'Other Address'}),
        }

    def clean(self):
        if not self.cleaned_data['mobile'] and not self.cleaned_data['landline']:
            raise forms.ValidationError({'mobile': ['Enter at least one contact number (mobile or landline)'],
                                         'landline': ['Enter at least one contact number (mobile or landline)']})


class DownpaymentForm(forms.ModelForm)

    class Meta:
        model = models.Downpayment
        fields = ['name',
                  'split',
                  'discount']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Input name'}),
            'split': forms.NumberInput(attrs={'step': 1,
                                              'min': 1
                                              'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'step': 0.01,
                                                 'min': 0.00
                                                 'class': 'form-control'}),
        }


class InstallmentForm(forms.ModelForm)

    class Meta:
        model = models.Installment
        fields = ['name',
                  'split',
                  'discount']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Input name'}),
            'years': forms.NumberInput(attrs={'step': 1,
                                              'min': 1
                                              'class': 'form-control'}),
            'interest': forms.NumberInput(attrs={'step': 0.01,
                                                 'min': 0.00
                                                 'class': 'form-control'}),
        }


class ContractForm(forms.ModelForm):

    class Meta:
        model = models.Contract
        fields = [
                    'date',
                    'buyer_type',
                    'contract_type',
                    'lot',
                    'client',
                    'care_fund',
                    'reservation',
                    'spot_cash_payment',
                    'spot_discount',
                    'downpayment_option',
                    'installment_option',
                    'sales_agent',
                    'unit_manager',
                    'sales_leader',
                    'referral',
                    'sold_by',
                    'remarks'
                ]

        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y',
                                    attrs={'class': 'form-control datepicker',
                                           'placeholder': 'Date'}),
            'buyer_type': forms.Select(attrs={'class': 'form-control',
                                              'placeholder': 'Buyer Type'}),
            'contract_type': forms.Select(attrs={'class': 'form-control',
                                                 'placeholder': 'Contract Type'}),
            'lot': forms.HiddenInput(),
            'client': forms.HiddenInput(),
            'care_fund': forms.NumberInput(attrs={'step': 0.01,
                                                  'min': 0.00
                                                  'class': 'form-control'}),
            'reservation': forms.NumberInput(attrs={'step': 0.01,
                                                    'min': 0.00
                                                    'class': 'form-control'}),
            'spot_cash_payment': forms.NumberInput(attrs={'step': 0.01,
                                                          'min': 0.00
                                                          'class': 'form-control'}),
            'spot_discount': forms.NumberInput(attrs={'step': 0.01,
                                                      'min': 0.00
                                                      'class': 'form-control'}),
            'downpayment_option': forms.Select(attrs={'class': 'form-control',
                                                      'placeholder': 'N/A'}),
            'installment_option': forms.Select(attrs={'class': 'form-control',
                                                      'placeholder': 'N/A'}),
            'sales_agent': forms.HiddenInput(),
            'unit_manager': forms.HiddenInput(),
            'sales_leader': forms.HiddenInput(),
            'referral': forms.HiddenInput(),
            'sold_by': forms.Select(attrs={'class': 'form-control',
                                           'placeholder': 'Buyer Type'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }


class ServiceForm(forms.ModelForm)

    class Meta:
        model = models.Service
        fields = ['date',
                  'amount',
                  'service_type',
                  'remarks']

        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y',
                                    attrs={'class': 'form-control datepicker',
                                           'placeholder': 'Date'}),
            'amount': forms.NumberInput(attrs={'step': 0.01,
                                               'min': 0.00
                                               'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control',
                                                'placeholder': 'Service Type'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }


class BillForm(forms.ModelForm)

    class Meta:
        model = models.Bill
        fields = ['start',
                  'end',
                  'issue_date',
                  'due_date',
                  'amount_due',
                  'remarks']

        widgets = {
            'start': forms.DateInput(format='%m/%d/%Y',
                                     attrs={'class': 'form-control datepicker',
                                            'placeholder': 'Date'}),
            'end': forms.DateInput(format='%m/%d/%Y',
                                   attrs={'class': 'form-control datepicker',
                                          'placeholder': 'Date'}),
            'issue_date': forms.DateInput(format='%m/%d/%Y',
                                          attrs={'class': 'form-control datepicker',
                                                 'placeholder': 'Date'}),
            'due_date': forms.DateInput(format='%m/%d/%Y',
                                        attrs={'class': 'form-control datepicker',
                                               'placeholder': 'Date'}),
            'amount_due': forms.NumberInput(attrs={'step': 0.01,
                                                   'min': 0.00
                                                   'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }


class PaymentForm(forms.ModelForm)

    class Meta:
        model = models.Payment
        fields = ['number',
                  'date',
                  'amount',
                  'payment_type',
                  'remarks']

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Input name'}),
            'date': forms.DateInput(format='%m/%d/%Y',
                                     attrs={'class': 'form-control datepicker',
                                            'placeholder': 'Date'}),
            'amount': forms.NumberInput(attrs={'step': 0.01,
                                               'min': 0.00
                                               'class': 'form-control'}),
            'payment_type': forms.Select(attrs={'class': 'form-control',
                                                'placeholder': 'Service Type'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }
