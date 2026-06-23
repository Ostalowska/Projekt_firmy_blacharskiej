from django import forms
from .models import Klient, Material, RozmiarBlachy, TypUslugi, Zamowienie, PozycjaZamowienia


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
        
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            "nazwa",
            "grubosc_mm",
            "producent",
            "cena_za_m2",
        ]

        labels = {
            "nazwa": "Nazwa materiału",
            "grubosc_mm": "Grubość (mm)",
            "producent": "Producent",
            "cena_za_m2": "Cena za m²",
        }

    def clean_grubosc_mm(self):
        grubosc = self.cleaned_data["grubosc_mm"]

        if grubosc <= 0:
            raise forms.ValidationError(
                "Grubość musi być większa od zera."
            )

        return grubosc

    def clean_cena_za_m2(self):
        cena = self.cleaned_data["cena_za_m2"]

        if cena < 0:
            raise forms.ValidationError(
                "Cena nie może być ujemna."
            )

        return cena

class RozmiarBlachyForm(forms.ModelForm):
    class Meta:
        model = RozmiarBlachy
        fields = [
            "nazwa",
            "szerokosc_mm",
            "wysokosc_mm",
            "standardowy",
        ]

        labels = {
            "nazwa": "Nazwa rozmiaru",
            "szerokosc_mm": "Szerokość (mm)",
            "wysokosc_mm": "Wysokość (mm)",
            "standardowy": "Rozmiar standardowy",
        }

    def clean_szerokosc_mm(self):
        szerokosc = self.cleaned_data["szerokosc_mm"]
        standardowy = self.cleaned_data.get("standardowy")

        if standardowy and szerokosc <= 0:
            raise forms.ValidationError("Szerokość musi być większa od zera.")

        return szerokosc

    def clean_wysokosc_mm(self):
        wysokosc = self.cleaned_data["wysokosc_mm"]
        standardowy = self.cleaned_data.get("standardowy")

        if standardowy and wysokosc <= 0:
            raise forms.ValidationError("Wysokość musi być większa od zera.")

        return wysokosc

class TypUslugiForm(forms.ModelForm):
    class Meta:
        model = TypUslugi
        fields = [
            "nazwa",
            "jednostka",
        ]

        labels = {
            "nazwa": "Nazwa usługi",
            "jednostka": "Jednostka",
        }

        widgets = {
            "nazwa": forms.TextInput(attrs={"placeholder": "Np. Cięcie"}),
            "jednostka": forms.TextInput(attrs={"placeholder": "Np. szt., m², mb"}),
        }

    def clean_nazwa(self):
        nazwa = self.cleaned_data["nazwa"]

        if len(nazwa) < 3:
            raise forms.ValidationError("Nazwa usługi musi mieć minimum 3 znaki.")

        return nazwa
        
class ZamowienieForm(forms.ModelForm):
    class Meta:
        model = Zamowienie
        fields = [
            "klient",
            "status",
            "uwagi",
        ]

        labels = {
            "klient": "Klient",
            "status": "Status",
            "uwagi": "Uwagi",
        }

        widgets = {
            "uwagi": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Dodatkowe informacje do zamówienia..."
            }),
        }
        
class PozycjaZamowieniaForm(forms.ModelForm):
    class Meta:
        model = PozycjaZamowienia
        fields = [
            "material",
            "rozmiar",
            "typ_uslugi",
            "przypisany_pracownik",
            "ilosc",
            "cena",
            "status",
            "czy_powstal_odpad",
            "opis_odpadu",
        ]

        labels = {
            "material": "Materiał",
            "rozmiar": "Rozmiar blachy",
            "typ_uslugi": "Typ usługi",
            "przypisany_pracownik": "Przypisany pracownik",
            "ilosc": "Ilość",
            "cena": "Cena",
            "status": "Status",
            "czy_powstal_odpad": "Czy powstał odpad?",
            "opis_odpadu": "Opis odpadu",
        }

        widgets = {
            "opis_odpadu": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Opcjonalny opis odpadu..."
            }),
        }

    def clean_ilosc(self):
        ilosc = self.cleaned_data["ilosc"]
        if ilosc <= 0:
            raise forms.ValidationError("Ilość musi być większa od zera.")
        return ilosc

    def clean_cena(self):
        cena = self.cleaned_data["cena"]
        if cena < 0:
            raise forms.ValidationError("Cena nie może być ujemna.")
        return cena