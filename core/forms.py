from django import forms
from django.contrib.auth.models import User
from django.forms import formset_factory

from .models import (
    Klient,
    Material,
    RozmiarBlachy,
    TypUslugi,
    Zamowienie,
    PozycjaZamowienia,
    Magazyn,
    StanMagazynowy,
    ProcesMagazynowy,
    Platnosc,
    PracownikProfil,
)


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
            "szerokosc_mm",
            "wysokosc_mm",
        ]

        labels = {
            "szerokosc_mm": "Szerokość (mm)",
            "wysokosc_mm": "Wysokość (mm)",
        }

    def clean_szerokosc_mm(self):
        szerokosc = self.cleaned_data["szerokosc_mm"]

        if szerokosc <= 0:
            raise forms.ValidationError("Szerokość musi być większa od zera.")

        return szerokosc

    def clean_wysokosc_mm(self):
        wysokosc = self.cleaned_data["wysokosc_mm"]

        if wysokosc <= 0:
            raise forms.ValidationError("Wysokość musi być większa od zera.")

        return wysokosc

class TypUslugiForm(forms.ModelForm):
    class Meta:
        model = TypUslugi
        fields = [
            "nazwa",
        ]

        labels = {
            "nazwa": "Nazwa usługi",
        }

        widgets = {
            "nazwa": forms.TextInput(attrs={"placeholder": "Np. Cięcie"}),
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
            "uwagi",
        ]

        labels = {
            "klient": "Klient",
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
            "czy_niestandardowy",
            "szerokosc_niestandardowa_mm",
            "wysokosc_niestandardowa_mm",
            "typ_uslugi",
            "ilosc",
        ]

        labels = {
            "material": "Materiał",
            "rozmiar": "Rozmiar standardowy",
            "czy_niestandardowy": "Rozmiar niestandardowy",
            "szerokosc_niestandardowa_mm": "Szerokość niestandardowa (mm)",
            "wysokosc_niestandardowa_mm": "Wysokość niestandardowa (mm)",
            "typ_uslugi": "Typ usługi",
            "ilosc": "Ilość",
        }

    def clean_ilosc(self):
        ilosc = self.cleaned_data["ilosc"]

        if ilosc <= 0:
            raise forms.ValidationError("Ilość musi być większa od zera.")

        return ilosc

    def clean(self):
        cleaned_data = super().clean()

        czy_niestandardowy = cleaned_data.get("czy_niestandardowy")
        rozmiar = cleaned_data.get("rozmiar")
        szerokosc = cleaned_data.get("szerokosc_niestandardowa_mm")
        wysokosc = cleaned_data.get("wysokosc_niestandardowa_mm")

        if czy_niestandardowy:
            if not szerokosc or not wysokosc:
                raise forms.ValidationError(
                    "Dla rozmiaru niestandardowego podaj szerokość i wysokość."
                )

            if szerokosc <= 0 or wysokosc <= 0:
                raise forms.ValidationError(
                    "Wymiary niestandardowe muszą być większe od zera."
                )

        else:
            if not rozmiar:
                raise forms.ValidationError(
                    "Wybierz rozmiar standardowy albo zaznacz rozmiar niestandardowy."
                )

        return cleaned_data


PozycjaZamowieniaFormSet = formset_factory(
    PozycjaZamowieniaForm,
    extra=1,
    can_delete=True
)


class RabatForm(forms.ModelForm):
    class Meta:
        model = Zamowienie
        fields = [
            "rabat_typ",
            "rabat_wartosc",
        ]

        labels = {
            "rabat_typ": "Typ rabatu",
            "rabat_wartosc": "Wartość rabatu",
        }

    def clean_rabat_wartosc(self):
        rabat = self.cleaned_data["rabat_wartosc"]

        if rabat < 0:
            raise forms.ValidationError("Rabat nie może być ujemny.")

        return rabat
        
class ProcesMagazynowyForm(forms.ModelForm):
    class Meta:
        model = ProcesMagazynowy
        fields = [
            "magazyn",
            "material",
            "typ",
            "ilosc",
            "opis",
        ]

        labels = {
            "magazyn": "Magazyn",
            "material": "Materiał",
            "typ": "Typ operacji",
            "ilosc": "Ilość",
            "opis": "Opis",
        }

        widgets = {
            "opis": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Np. dostawa materiału albo wydanie do produkcji..."
            }),
        }

    def clean_ilosc(self):
        ilosc = self.cleaned_data["ilosc"]

        if ilosc <= 0:
            raise forms.ValidationError("Ilość musi być większa od zera.")

        return ilosc
        
class PlatnoscForm(forms.ModelForm):
    class Meta:
        model = Platnosc
        fields = [
            "zamowienie",
            "kwota",
            "rabat",
            "status",
        ]

        labels = {
            "zamowienie": "Zamówienie",
            "kwota": "Kwota",
            "rabat": "Rabat",
            "status": "Status płatności",
        }

    def clean_kwota(self):
        kwota = self.cleaned_data["kwota"]

        if kwota < 0:
            raise forms.ValidationError("Kwota nie może być ujemna.")

        return kwota

    def clean_rabat(self):
        rabat = self.cleaned_data["rabat"]

        if rabat < 0:
            raise forms.ValidationError("Rabat nie może być ujemny.")

        return rabat

class PracownikCreateForm(forms.Form):
    username = forms.CharField(label="Login", max_length=150)
    imie = forms.CharField(label="Imię", max_length=50)
    nazwisko = forms.CharField(label="Nazwisko", max_length=50)
    email = forms.EmailField(label="Email", required=False)
    telefon = forms.CharField(label="Telefon", max_length=20, required=False)
    rola = forms.ChoiceField(label="Rola", choices=PracownikProfil.ROLE_CHOICES)
    haslo = forms.CharField(label="Hasło", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Użytkownik o takim loginie już istnieje.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Użytkownik o takim emailu już istnieje.")
        return email


class PracownikEditForm(forms.ModelForm):
    imie = forms.CharField(label="Imię", max_length=50)
    nazwisko = forms.CharField(label="Nazwisko", max_length=50)
    email = forms.EmailField(label="Email", required=False)
    aktywny = forms.BooleanField(label="Aktywny", required=False)

    class Meta:
        model = PracownikProfil
        fields = ["telefon", "rola"]
        labels = {
            "telefon": "Telefon",
            "rola": "Rola",
        }