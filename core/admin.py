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
    Zadanie,
    Platnosc,
    ProcesMagazynowy,
)


@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display = ("imie", "nazwisko", "email", "telefon", "nazwa_firmy")
    search_fields = ("imie", "nazwisko", "email", "telefon", "nazwa_firmy", "nip")


@admin.register(PracownikProfil)
class PracownikProfilAdmin(admin.ModelAdmin):
    list_display = ("user", "rola", "telefon")
    list_filter = ("rola",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "telefon")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("nazwa", "producent", "grubosc_mm", "cena_za_m2")
    search_fields = ("nazwa", "producent")


@admin.register(RozmiarBlachy)
class RozmiarBlachyAdmin(admin.ModelAdmin):
    list_display = ("szerokosc_mm", "wysokosc_mm")


@admin.register(TypUslugi)
class TypUslugiAdmin(admin.ModelAdmin):
    list_display = ("nazwa",)
    search_fields = ("nazwa",)


@admin.register(Cennik)
class CennikAdmin(admin.ModelAdmin):
    list_display = ("typ_uslugi", "cena", "data_od")
    list_filter = ("typ_uslugi", "data_od")


@admin.register(Magazyn)
class MagazynAdmin(admin.ModelAdmin):
    list_display = ("nazwa", "adres")
    search_fields = ("nazwa", "adres")


@admin.register(StanMagazynowy)
class StanMagazynowyAdmin(admin.ModelAdmin):
    list_display = ("magazyn", "material", "ilosc", "zarezerwowano", "dostepne")
    list_filter = ("magazyn", "material")


class PozycjaZamowieniaInline(admin.TabularInline):
    model = PozycjaZamowienia
    extra = 1
    fields = (
        "material",
        "rozmiar",
        "czy_niestandardowy",
        "szerokosc_niestandardowa_mm",
        "wysokosc_niestandardowa_mm",
        "typ_uslugi",
        "ilosc",
        "cena_jednostkowa",
        "wartosc",
    )
    readonly_fields = ("cena_jednostkowa", "wartosc")


class ZadanieInline(admin.TabularInline):
    model = Zadanie
    extra = 0


@admin.register(Zamowienie)
class ZamowienieAdmin(admin.ModelAdmin):
    list_display = ("numer", "klient", "status", "data_utworzenia", "kwota_koncowa")
    list_filter = ("status", "data_utworzenia")
    search_fields = ("numer", "klient__imie", "klient__nazwisko", "klient__email")
    inlines = [PozycjaZamowieniaInline]


@admin.register(PozycjaZamowienia)
class PozycjaZamowieniaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "zamowienie",
        "stan_magazynowy",
        "lista_uslug",
        "ilosc",
        "cena_jednostkowa",
        "wartosc",
    )

    list_filter = (
        "czy_niestandardowy",
        "uslugi",
    )

    search_fields = (
        "zamowienie__numer",
        "stan_magazynowy__material__nazwa",
        "stan_magazynowy__magazyn__nazwa",
        "stan_magazynowy__rozmiar__szerokosc_mm",
        "stan_magazynowy__rozmiar__wysokosc_mm",
    )

    def lista_uslug(self, obj):
        return ", ".join(usluga.nazwa for usluga in obj.uslugi.all())

    lista_uslug.short_description = "Usługi"


@admin.register(Zadanie)
class ZadanieAdmin(admin.ModelAdmin):
    list_display = (
        "pozycja",
        "typ_uslugi",
        "rola_docelowa",
        "przypisany_pracownik",
        "status",
        "data_utworzenia",
        "data_zakonczenia",
    )
    list_filter = ("status", "rola_docelowa", "typ_uslugi")
    search_fields = ("pozycja__zamowienie__numer",)


@admin.register(Platnosc)
class PlatnoscAdmin(admin.ModelAdmin):
    list_display = ("zamowienie", "kwota", "rabat", "status", "data_utworzenia")
    list_filter = ("status", "data_utworzenia")


@admin.register(ProcesMagazynowy)
class ProcesMagazynowyAdmin(admin.ModelAdmin):
    list_display = (
        "typ",
        "magazyn",
        "material",
        "ilosc",
        "pracownik",
        "data",
        "cofnieta",
    )
    list_filter = ("typ", "magazyn", "material", "data", "cofnieta")
    search_fields = ("material__nazwa", "opis", "powod_cofniecia")