from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import SellerProfile, User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class SellerRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = [
            "store_name",
            "description",
            "logo",
            "phone",
            "email_contact",
            "website",
            "payment_info",
            "shipping_info",
            "is_active",
            "auto_accept_orders",
            "facebook",
            "instagram",
            "telegram",
        ]
        widgets = {
            "store_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "logo": forms.FileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email_contact": forms.EmailInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "payment_info": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "shipping_info": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "auto_accept_orders": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "facebook": forms.URLInput(attrs={"class": "form-control"}),
            "instagram": forms.URLInput(attrs={"class": "form-control"}),
            "telegram": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["store_name"].widget.attrs["readonly"] = True
            self.fields["store_name"].help_text = (
                "Назву магазину неможливо змінити після створення"
            )
