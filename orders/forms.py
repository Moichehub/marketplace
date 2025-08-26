from django import forms
from .models import PaymentMethod

class PaymentMethodForm(forms.Form):
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.filter(is_active=True),
        empty_label="Оберіть спосіб оплати",
        widget=forms.RadioSelect,
        label="Спосіб оплати"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for payment_method in PaymentMethod.objects.filter(is_active=True):
            display_text = f"{payment_method.icon} {payment_method.name}"
            if payment_method.description:
                display_text += f" - {payment_method.description}"
            choices.append((payment_method.id, display_text))
        
        self.fields['payment_method'].choices = [('', "Оберіть спосіб оплати")] + choices

