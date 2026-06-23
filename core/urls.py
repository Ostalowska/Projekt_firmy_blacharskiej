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
]