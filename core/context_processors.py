def rola_uzytkownika(request):
    rola = None

    if request.user.is_authenticated:
        try:
            rola = request.user.pracownikprofil.rola
        except Exception:
            rola = None

    return {
        "rola": rola,
        "czy_admin": rola == "ADMIN" or request.user.is_superuser,
        "czy_magazynier": rola == "MAGAZYN",
        "czy_produkcja": rola == "PRODUKCJA",
        "czy_ksiegowosc": rola == "KSIEGOWOSC",
    }
