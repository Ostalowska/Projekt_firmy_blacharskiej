from django.contrib import admin

from .models import (
    Klient,
    PracownikProfil,
    Material,
    RozmiarBlachy,
    TypUslugi,
    Cennik,
    Magazyn,
    StanMagazynowy,
    Zamowienie,
    PozycjaZamowienia,
    Platnosc,
    ProcesMagazynowy,
)


@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display = ("id", "imie", "nazwisko", "email", "telefon", "nazwa_firmy")
    search_fields = ("imie", "nazwisko", "email", "telefon", "nazwa_firmy", "nip")


@admin.register(PracownikProfil)
class PracownikProfilAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rola", "telefon")
    list_filter = ("rola",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "telefon")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "nazwa", "producent", "grubosc_mm", "cena_za_m2")
    search_fields = ("nazwa", "producent")


@admin.register(RozmiarBlachy)
class RozmiarBlachyAdmin(admin.ModelAdmin):
    list_display = ("id", "nazwa", "szerokosc_mm", "wysokosc_mm", "standardowy")
    list_filter = ("standardowy",)
    search_fields = ("nazwa",)


@admin.register(TypUslugi)
class TypUslugiAdmin(admin.ModelAdmin):
    list_display = ("id", "nazwa", "jednostka")
    search_fields = ("nazwa",)


@admin.register(Cennik)
class CennikAdmin(admin.ModelAdmin):
    list_display = ("id", "typ_uslugi", "cena", "data_od")
    list_filter = ("typ_uslugi", "data_od")


@admin.register(Magazyn)
class MagazynAdmin(admin.ModelAdmin):
    list_display = ("id", "nazwa", "adres")
    search_fields = ("nazwa", "adres")


@admin.register(StanMagazynowy)
class StanMagazynowyAdmin(admin.ModelAdmin):
    list_display = ("id", "magazyn", "material", "ilosc")
    list_filter = ("magazyn", "material")


class PozycjaZamowieniaInline(admin.TabularInline):
    model = PozycjaZamowienia
    extra = 1


@admin.register(Zamowienie)
class ZamowienieAdmin(admin.ModelAdmin):
    list_display = ("id", "klient", "status", "data_utworzenia")
    list_filter = ("status", "data_utworzenia")
    search_fields = ("klient__imie", "klient__nazwisko", "klient__email")
    inlines = [PozycjaZamowieniaInline]


@admin.register(PozycjaZamowienia)
class PozycjaZamowieniaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "zamowienie",
        "material",
        "rozmiar",
        "typ_uslugi",
        "przypisany_pracownik",
        "ilosc",
        "cena",
        "status",
    )
    list_filter = ("status", "material", "typ_uslugi")
    search_fields = ("zamowienie__id", "material__nazwa")


@admin.register(Platnosc)
class PlatnoscAdmin(admin.ModelAdmin):
    list_display = ("id", "zamowienie", "kwota", "rabat", "status", "data_utworzenia")
    list_filter = ("status", "data_utworzenia")


@admin.register(ProcesMagazynowy)
class ProcesMagazynowyAdmin(admin.ModelAdmin):
    list_display = ("id", "typ", "magazyn", "material", "ilosc", "pracownik", "data")
    list_filter = ("typ", "magazyn", "material", "data")
    search_fields = ("material__nazwa", "opis")