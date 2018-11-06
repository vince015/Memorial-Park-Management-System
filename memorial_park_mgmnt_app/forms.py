from datetime import date, datetime, timedelta

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
                    'rank',
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
            'rank': forms.Select(attrs={'class': 'form-control',
                                        'placeholder': 'Select Rank'}),
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


class ContractForm(forms.ModelForm):

    class Meta:
        model = models.Contract
        fields = [  'number',
                    'date',
                    'buyer_type',
                    'payment_terms',
                    'lot',
                    'client',
                    'reservation',
                    'sales_agent',
                    'unit_manager',
                    'sales_leader',
                    'referent',
                    'sold_by',
                    'remarks'
                ]

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Contract No.'}),
            'date': forms.DateInput(format='%m/%d/%Y',
                                    attrs={'class': 'form-control datepicker',
                                           'placeholder': 'Date'}),
            'lot': forms.HiddenInput(),
            'client': forms.HiddenInput(),
            'buyer_type': forms.Select(attrs={'class': 'form-control',
                                              'placeholder': 'Buyer Type'}),
            'payment_terms': forms.Select(attrs={'class': 'form-control',
                                                 'placeholder': 'Buyer Type'}),
            'contract_type': forms.Select(attrs={'class': 'form-control',
                                                 'placeholder': 'Contract Type'}),
            'reservation': forms.NumberInput(attrs={'step': 0.01,
                                                    'min': 0.00,
                                                    'class': 'form-control'}),
            'sales_agent': forms.HiddenInput(),
            'unit_manager': forms.HiddenInput(),
            'sales_leader': forms.HiddenInput(),
            'referent': forms.HiddenInput(),
            'sold_by': forms.Select(attrs={'class': 'form-control',
                                           'placeholder': 'Buyer Type'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }


class ContractUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Contract
        fields = [  'lot',
                    'client',
                    'sales_agent',
                    'unit_manager',
                    'sales_leader',
                    'referent',
                    'sold_by',
                    'remarks'
                ]

        widgets = {
            'lot': forms.HiddenInput(),
            'client': forms.HiddenInput(),
            'sales_agent': forms.HiddenInput(),
            'unit_manager': forms.HiddenInput(),
            'sales_leader': forms.HiddenInput(),
            'referent': forms.HiddenInput(),
            'sold_by': forms.Select(attrs={'class': 'form-control',
                                           'placeholder': 'Buyer Type'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }


class InstallmentOptionForm(forms.Form):

    pst = datetime.utcnow() + timedelta(hours=8)

    valid_downpayment_promos = models.DownpaymentPromo.objects.filter(start_date__lte=pst.date(),
                                                                      end_date__gte=pst.date()).order_by('-start_date')
    valid_installment_promos = models.InstallmentPromo.objects.filter(start_date__lte=pst.date(),
                                                                      end_date__gte=pst.date()).order_by('-start_date')

    downpayment_option = forms.ModelChoiceField(queryset=valid_downpayment_promos, required=True)
    installment_option = forms.ModelChoiceField(queryset=valid_installment_promos, required=True)

    class Meta:
        widgets = {
            'downpayment_option': forms.Select(attrs={'class': 'form-control',
                                                      'placeholder': 'Select Downpayment Option'}),
            'installment_option': forms.Select(attrs={'class': 'form-control',
                                                      'placeholder': 'Select Installment Option'})
        }


class ServiceForm(forms.ModelForm):

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
                                               'min': 0.00,
                                               'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control',
                                                'placeholder': 'Service Type'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }


class BillForm(forms.ModelForm):

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
                                                   'min': 0.00,
                                                   'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }


class BillStatusForm(forms.ModelForm):

    class Meta:
        model = models.Bill
        fields = ['status']

        widgets = {
            'status': forms.Select(attrs={'class': 'form-control',
                                          'placeholder': 'Service Type'}),
        }

class ReceiptForm(forms.ModelForm):

    class Meta:
        model = models.Receipt
        fields = ['number',
                  'date',
                  'amount',
                  'remarks']

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Input number'}),
            'date': forms.DateInput(format='%m/%d/%Y',
                                     attrs={'class': 'form-control datepicker',
                                            'placeholder': 'mm/dd/yyyy'}),
            'amount': forms.NumberInput(attrs={'step': 0.01,
                                               'min': 0.00,
                                               'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }

class PaymentForm(forms.ModelForm):

    class Meta:
        model = models.Payment
        fields = ['date',
                  'amount',
                  'remarks']

        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y',
                                     attrs={'class': 'form-control datepicker',
                                            'placeholder': 'mm/dd/yyyy'}),
            'amount': forms.NumberInput(attrs={'step': 0.01,
                                               'min': 0.00,
                                               'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 3,
                                             'placeholder': 'Remarks'}),
        }
