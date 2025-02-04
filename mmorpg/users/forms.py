from django import forms

class VerificationCodeForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, required=True, label="Введите код")