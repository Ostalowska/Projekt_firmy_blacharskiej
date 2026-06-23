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
]