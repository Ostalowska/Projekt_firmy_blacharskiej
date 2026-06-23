from django import forms
from .models import Klient


class KlientForm(forms.ModelForm):
    class Meta:
        model = Klient
        fields = [
            "imie",
            "nazwisko",
            "telefon",
            "email",
            "adres",
            "nazwa_firmy",
            "nip",
        ]

        labels = {
            "imie": "Imię",
            "nazwisko": "Nazwisko",
            "telefon": "Telefon",
            "email": "Email",
            "adres": "Adres",
            "nazwa_firmy": "Nazwa firmy",
            "nip": "NIP",
        }

        widgets = {
            "imie": forms.TextInput(attrs={"placeholder": "Imię"}),
            "nazwisko": forms.TextInput(attrs={"placeholder": "Nazwisko"}),
            "telefon": forms.TextInput(attrs={"placeholder": "Telefon"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "adres": forms.TextInput(attrs={"placeholder": "Adres"}),
            "nazwa_firmy": forms.TextInput(attrs={"placeholder": "Nazwa firmy opcjonalnie"}),
            "nip": forms.TextInput(attrs={"placeholder": "NIP opcjonalnie"}),
        }

    def clean_imie(self):
        imie = self.cleaned_data["imie"]
        if any(char.isdigit() for char in imie):
            raise forms.ValidationError("Imię nie może zawierać cyfr.")
        return imie

    def clean_nazwisko(self):
        nazwisko = self.cleaned_data["nazwisko"]
        if any(char.isdigit() for char in nazwisko):
            raise forms.ValidationError("Nazwisko nie może zawierać cyfr.")
        return nazwisko

    def clean_telefon(self):
        telefon = self.cleaned_data.get("telefon")
        if telefon and not telefon.isdigit():
            raise forms.ValidationError("Telefon może zawierać tylko cyfry.")
        if telefon and len(telefon) != 9:
            raise forms.ValidationError("Telefon powinien mieć 9 cyfr.")
        return telefon