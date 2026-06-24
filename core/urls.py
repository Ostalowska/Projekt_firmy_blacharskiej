from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),

    path("klienci/", views.klienci_lista, name="klienci_lista"),
    path("klienci/dodaj/", views.klient_dodaj, name="klient_dodaj"),
    path("klienci/<int:klient_id>/edytuj/", views.klient_edytuj, name="klient_edytuj"),
    path("klienci/<int:klient_id>/usun/", views.klient_usun, name="klient_usun"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
    "materialy/",
    views.materialy_lista,
    name="materialy_lista",
    ),

    path(
        "materialy/dodaj/",
        views.material_dodaj,
        name="material_dodaj",
    ),

    path(
        "materialy/<int:material_id>/edytuj/",
        views.material_edytuj,
        name="material_edytuj",
    ),

    path(
        "materialy/<int:material_id>/usun/",
        views.material_usun,
        name="material_usun",
    ),
    path("rozmiary/", views.rozmiary_lista, name="rozmiary_lista"),
    path("rozmiary/dodaj/", views.rozmiar_dodaj, name="rozmiar_dodaj"),
    path("rozmiary/<int:rozmiar_id>/edytuj/", views.rozmiar_edytuj, name="rozmiar_edytuj"),
    path("rozmiary/<int:rozmiar_id>/usun/", views.rozmiar_usun, name="rozmiar_usun"),
    path("typy-uslug/", views.typy_uslug_lista, name="typy_uslug_lista"),
    path("typy-uslug/dodaj/", views.typ_uslugi_dodaj, name="typ_uslugi_dodaj"),
    path("typy-uslug/<int:typ_id>/edytuj/", views.typ_uslugi_edytuj, name="typ_uslugi_edytuj"),
    path("typy-uslug/<int:typ_id>/usun/", views.typ_uslugi_usun, name="typ_uslugi_usun"),
    path("zamowienia/", views.zamowienia_lista, name="zamowienia_lista"),
    path("zamowienia/dodaj/", views.zamowienie_dodaj, name="zamowienie_dodaj"),
    path("zamowienia/<int:zamowienie_id>/edytuj/", views.zamowienie_edytuj, name="zamowienie_edytuj"),
    path("zamowienia/<int:zamowienie_id>/usun/", views.zamowienie_usun, name="zamowienie_usun"),
    
    path("zamowienia/<int:zamowienie_id>/", views.zamowienie_szczegoly, name="zamowienie_szczegoly"),

    path("zamowienia/<int:zamowienie_id>/pozycje/dodaj/", views.pozycja_dodaj, name="pozycja_dodaj"),
    path("pozycje/<int:pozycja_id>/edytuj/", views.pozycja_edytuj, name="pozycja_edytuj"),
    path("pozycje/<int:pozycja_id>/usun/", views.pozycja_usun, name="pozycja_usun"),
    
    path("moje-prace/", views.moje_prace, name="moje_prace"),
    
    path("magazyn/", views.magazyn_lista, name="magazyn_lista"),
    path("magazyn/proces/dodaj/", views.proces_magazynowy_dodaj, name="proces_magazynowy_dodaj"),
    
    path("platnosci/", views.platnosci_lista, name="platnosci_lista"),
    path("platnosci/dodaj/", views.platnosc_dodaj, name="platnosc_dodaj"),
    path("platnosci/<int:platnosc_id>/edytuj/", views.platnosc_edytuj, name="platnosc_edytuj"),
    path("platnosci/<int:platnosc_id>/usun/", views.platnosc_usun, name="platnosc_usun"),
    
    path("pracownicy/", views.pracownicy_lista, name="pracownicy_lista"),
    path("pracownicy/dodaj/", views.pracownik_dodaj, name="pracownik_dodaj"),
    path("pracownicy/<int:pracownik_id>/edytuj/", views.pracownik_edytuj, name="pracownik_edytuj"),
    path("pracownicy/<int:pracownik_id>/dezaktywuj/", views.pracownik_dezaktywuj, name="pracownik_dezaktywuj"),
    path("zamowienia/<int:zamowienie_id>/rabat/", views.zamowienie_ustaw_rabat, name="zamowienie_ustaw_rabat"),
    path("zamowienia/<int:zamowienie_id>/przyjmij/", views.zamowienie_przyjmij, name="zamowienie_przyjmij"),
    path("pracownicy/<int:pracownik_id>/aktywuj/", views.pracownik_aktywuj, name="pracownik_aktywuj"),
]