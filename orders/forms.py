from django import forms


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, required=True, widget=forms.TextInput(attrs={'placeholder': 'Card '
                                                                                                             'Number'}))
    expiry_date = forms.CharField(max_length=5, required=True, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_lenght=3, required=True, widget=forms.TextInput(attrs={'placeholder': 'CVV'}))