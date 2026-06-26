import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    CofniecieOperacjiForm,
    InwentaryzacjaForm,
    KlientForm,
    MagazynForm,
    MaterialForm,
    PlatnoscForm,
    PozycjaZamowieniaForm,
    PozycjaZamowieniaFormSet,
    PracownikCreateForm,
    PracownikEditForm,
    ProcesMagazynowyForm,
    RabatForm,
    RozmiarBlachyForm,
    TypUslugiForm,
    ZamowienieForm,
)
from .models import (
    Cennik,
    Klient,
    Magazyn,
    Material,
    Platnosc,
    PozycjaZamowienia,
    PracownikProfil,
    ProcesMagazynowy,
    RozmiarBlachy,
    StanMagazynowy,
    TypUslugi,
    Zadanie,
    Zamowienie,
)


def aktualizuj_platnosc_zamowienia(zamowienie):
    zamowienie.przelicz_kwote()

    platnosc, created = Platnosc.objects.update_or_create(
        zamowienie=zamowienie,
        defaults={
            "kwota": zamowienie.kwota_koncowa,
            "rabat": zamowienie.rabat_wartosc,
        },
    )

    if created:
        platnosc.status = "NIEOPLACONA"
        platnosc.save(update_fields=["status"])

    return platnosc


@login_required
def index(request):
    return render(request, "index.html")


@login_required
def klienci_lista(request):
    query = request.GET.get("q", "")

    klienci = Klient.objects.all().order_by("-id")

    if query:
        klienci = (
            klienci.filter(imie__icontains=query)
            | klienci.filter(nazwisko__icontains=query)
            | klienci.filter(email__icontains=query)
            | klienci.filter(nazwa_firmy__icontains=query)
        )

    return render(
        request,
        "klienci/lista.html",
        {
            "klienci": klienci,
            "query": query,
        },
    )


@login_required
def klient_dodaj(request):
    if request.method == "POST":
        form = KlientForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Klient został dodany.")
            return redirect("core:klienci_lista")
    else:
        form = KlientForm()

    return render(
        request,
        "klienci/formularz.html",
        {
            "form": form,
            "tytul": "Dodaj klienta",
        },
    )


@login_required
def klient_edytuj(request, klient_id):
    klient = get_object_or_404(Klient, id=klient_id)

    if request.method == "POST":
        form = KlientForm(request.POST, instance=klient)

        if form.is_valid():
            form.save()
            messages.success(request, "Dane klienta zostały zaktualizowane.")
            return redirect("core:klienci_lista")
    else:
        form = KlientForm(instance=klient)

    return render(
        request,
        "klienci/formularz.html",
        {
            "form": form,
            "tytul": "Edytuj klienta",
        },
    )


@login_required
def klient_usun(request, klient_id):
    klient = get_object_or_404(Klient, id=klient_id)

    if request.method == "POST":
        klient.delete()
        messages.success(request, "Klient został usunięty.")
        return redirect("core:klienci_lista")

    return render(
        request,
        "klienci/usun.html",
        {
            "klient": klient,
        },
    )


@login_required
def materialy_lista(request):

    query = request.GET.get("q", "")

    materialy = Material.objects.all().order_by("nazwa")

    if query:
        materialy = materialy.filter(nazwa__icontains=query)

    return render(
        request,
        "materialy/lista.html",
        {
            "materialy": materialy,
            "query": query,
        },
    )


@login_required
def material_dodaj(request):

    if request.method == "POST":
        form = MaterialForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Materiał został dodany.")

            return redirect("core:edycja_uslug")

    else:
        form = MaterialForm()

    return render(
        request,
        "materialy/formularz.html",
        {
            "form": form,
            "tytul": "Dodaj materiał",
        },
    )


@login_required
def material_edytuj(request, material_id):

    material = get_object_or_404(
        Material,
        id=material_id,
    )

    if request.method == "POST":
        form = MaterialForm(
            request.POST,
            instance=material,
        )

        if form.is_valid():
            form.save()

            messages.success(request, "Materiał został zaktualizowany.")

            return redirect("core:edycja_uslug")

    else:
        form = MaterialForm(instance=material)

    return render(
        request,
        "materialy/formularz.html",
        {
            "form": form,
            "tytul": "Edytuj materiał",
        },
    )


@login_required
def material_usun(request, material_id):

    material = get_object_or_404(
        Material,
        id=material_id,
    )

    if request.method == "POST":

        material.delete()

        messages.success(request, "Materiał został usunięty.")

        return redirect("core:edycja_uslug")

    return render(
        request,
        "materialy/usun.html",
        {
            "material": material,
        },
    )


@login_required
def rozmiary_lista(request):
    query = request.GET.get("q", "")

    rozmiary = RozmiarBlachy.objects.all().order_by(
        "szerokosc_mm",
        "wysokosc_mm",
    )

    return render(
        request,
        "rozmiary/lista.html",
        {
            "rozmiary": rozmiary,
            "query": query,
        },
    )


@login_required
def rozmiar_dodaj(request):
    if request.method == "POST":
        form = RozmiarBlachyForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Rozmiar blachy został dodany.")
            return redirect("core:edycja_uslug")
    else:
        form = RozmiarBlachyForm()

    return render(
        request,
        "rozmiary/formularz.html",
        {
            "form": form,
            "tytul": "Dodaj rozmiar blachy",
        },
    )


@login_required
def rozmiar_edytuj(request, rozmiar_id):
    rozmiar = get_object_or_404(RozmiarBlachy, id=rozmiar_id)

    if request.method == "POST":
        form = RozmiarBlachyForm(request.POST, instance=rozmiar)

        if form.is_valid():
            form.save()
            messages.success(request, "Rozmiar blachy został zaktualizowany.")
            return redirect("core:edycja_uslug")
    else:
        form = RozmiarBlachyForm(instance=rozmiar)

    return render(
        request,
        "rozmiary/formularz.html",
        {
            "form": form,
            "tytul": "Edytuj rozmiar blachy",
        },
    )


@login_required
def rozmiar_usun(request, rozmiar_id):
    rozmiar = get_object_or_404(RozmiarBlachy, id=rozmiar_id)

    if request.method == "POST":
        rozmiar.delete()
        messages.success(request, "Rozmiar blachy został usunięty.")
        return redirect("core:edycja_uslug")

    return render(
        request,
        "rozmiary/usun.html",
        {
            "rozmiar": rozmiar,
        },
    )


@login_required
def typy_uslug_lista(request):
    query = request.GET.get("q", "")

    typy_uslug = TypUslugi.objects.all().order_by("nazwa")

    ceny_uslug = {}
    for typ in typy_uslug:
        ostatnia_cena = (
            Cennik.objects.filter(typ_uslugi=typ).order_by("-data_od").first()
        )
        ceny_uslug[typ.id] = ostatnia_cena.cena if ostatnia_cena else None

    if query:
        typy_uslug = typy_uslug.filter(nazwa__icontains=query)

    return render(
        request,
        "typy_uslug/lista.html",
        {
            "typy_uslug": typy_uslug,
            "query": query,
        },
    )


@login_required
def typ_uslugi_dodaj(request):
    if request.method == "POST":
        form = TypUslugiForm(request.POST)

        if form.is_valid():
            typ_uslugi = form.save()

            Cennik.objects.create(
                typ_uslugi=typ_uslugi,
                cena=form.cleaned_data["cena"],
                data_od=timezone.now().date(),
            )

            messages.success(request, "Typ usługi został dodany.")
            return redirect("core:edycja_uslug")
    else:
        form = TypUslugiForm()

    return render(
        request,
        "typy_uslug/formularz.html",
        {
            "form": form,
            "tytul": "Dodaj typ usługi",
        },
    )


@login_required
def typ_uslugi_edytuj(request, typ_id):
    typ_uslugi = get_object_or_404(TypUslugi, id=typ_id)

    if request.method == "POST":
        form = TypUslugiForm(request.POST, instance=typ_uslugi)

        if form.is_valid():
            typ_uslugi = form.save()

            ostatnia_cena = (
                Cennik.objects.filter(typ_uslugi=typ_uslugi)
                .order_by("-data_od")
                .first()
            )

            nowa_cena = form.cleaned_data["cena"]

            if not ostatnia_cena or ostatnia_cena.cena != nowa_cena:
                Cennik.objects.create(
                    typ_uslugi=typ_uslugi,
                    cena=nowa_cena,
                    data_od=timezone.now().date(),
                )

            messages.success(request, "Typ usługi został zaktualizowany.")
            return redirect("core:edycja_uslug")
    else:
        form = TypUslugiForm(instance=typ_uslugi)

    return render(
        request,
        "typy_uslug/formularz.html",
        {
            "form": form,
            "tytul": "Edytuj typ usługi",
        },
    )


@login_required
def typ_uslugi_usun(request, typ_id):
    typ_uslugi = get_object_or_404(TypUslugi, id=typ_id)

    if request.method == "POST":
        typ_uslugi.delete()
        messages.success(request, "Typ usługi został usunięty.")
        return redirect("core:edycja_uslug")

    return render(
        request,
        "typy_uslug/usun.html",
        {
            "typ_uslugi": typ_uslugi,
        },
    )


@login_required
def zamowienia_lista(request):
    query = request.GET.get("q", "")
    status = request.GET.get("status", "")

    zamowienia = (
        Zamowienie.objects.select_related("klient")
        .exclude(status="ROBOCZE")
        .order_by("-data_utworzenia")
    )

    if query:
        zamowienia = (
            zamowienia.filter(klient__imie__icontains=query)
            | zamowienia.filter(klient__nazwisko__icontains=query)
            | zamowienia.filter(klient__email__icontains=query)
            | zamowienia.filter(klient__nazwa_firmy__icontains=query)
        )

    if status:
        zamowienia = zamowienia.filter(status=status)

    return render(
        request,
        "zamowienia/lista.html",
        {
            "zamowienia": zamowienia,
            "query": query,
            "status": status,
            "statusy": Zamowienie.STATUS_CHOICES,
        },
    )


@login_required
def zamowienie_dodaj(request):
    stany_magazynowe = (
        StanMagazynowy.objects.select_related("magazyn", "material", "rozmiar")
        .filter(
            ilosc__gt=0,
            rozmiar__isnull=False,
        )
        .order_by(
            "magazyn__nazwa",
            "material__nazwa",
            "material__grubosc_mm",
            "rozmiar__szerokosc_mm",
            "rozmiar__wysokosc_mm",
        )
    )

    typy_uslug = TypUslugi.objects.all().order_by("nazwa")

    stany_json = json.dumps(
        [
            {
                "id": stan.id,
                "magazyn": stan.magazyn.nazwa,
                "material": str(stan.material),
                "material_id": stan.material.id,
                "rozmiar": str(stan.rozmiar) if stan.rozmiar else "",
                "szerokosc": stan.rozmiar.szerokosc_mm if stan.rozmiar else 0,
                "wysokosc": stan.rozmiar.wysokosc_mm if stan.rozmiar else 0,
                "cena_za_m2": float(stan.material.cena_za_m2),
                "ilosc": stan.ilosc,
                "zarezerwowano": stan.zarezerwowano,
                "dostepne": stan.dostepne,
            }
            for stan in stany_magazynowe
            if stan.dostepne > 0
        ]
    )

    uslugi_json = json.dumps(
        [
            {
                "id": typ.id,
                "nazwa": typ.nazwa,
                "cena": (
                    float(
                        Cennik.objects.filter(typ_uslugi=typ)
                        .order_by("-data_od")
                        .first()
                        .cena
                    )
                    if Cennik.objects.filter(typ_uslugi=typ).exists()
                    else 0
                ),
            }
            for typ in typy_uslug
        ]
    )

    if request.method == "POST":
        zamowienie_form = ZamowienieForm(request.POST)
        pozycje_formset = PozycjaZamowieniaFormSet(request.POST, prefix="pozycje")

        if zamowienie_form.is_valid() and pozycje_formset.is_valid():
            poprawne_pozycje = [
                form
                for form in pozycje_formset
                if form.cleaned_data and not form.cleaned_data.get("DELETE")
            ]

            if not poprawne_pozycje:
                messages.error(request, "Dodaj przynajmniej jedną pozycję zamówienia.")
            else:
                zamowienie = zamowienie_form.save(commit=False)
                zamowienie.status = "ROBOCZE"
                zamowienie.save()

                for form in poprawne_pozycje:
                    pozycja = form.save(commit=False)
                    pozycja.zamowienie = zamowienie
                    pozycja.save()

                    form.instance = pozycja
                    form.save_m2m()

                    pozycja.przelicz_i_zapisz()

                zamowienie.przelicz_kwote()

                messages.success(request, "Zamówienie robocze zostało zapisane.")
                return redirect(
                    "core:zamowienie_szczegoly", zamowienie_id=zamowienie.id
                )

    else:
        zamowienie_form = ZamowienieForm()
        pozycje_formset = PozycjaZamowieniaFormSet(prefix="pozycje")

    return render(
        request,
        "zamowienia/formularz.html",
        {
            "zamowienie_form": zamowienie_form,
            "pozycje_formset": pozycje_formset,
            "tytul": "Nowe zamówienie",
            "stany_json": stany_json,
            "uslugi_json": uslugi_json,
        },
    )


@login_required
def zamowienie_edytuj(request, zamowienie_id):
    zamowienie = get_object_or_404(Zamowienie, id=zamowienie_id)

    if request.method == "POST":
        form = ZamowienieForm(request.POST, instance=zamowienie)

        if form.is_valid():
            form.save()
            messages.success(request, "Zamówienie zostało zaktualizowane.")
            return redirect("core:zamowienia_lista")
    else:
        form = ZamowienieForm(instance=zamowienie)

    return render(
        request,
        "zamowienia/formularz.html",
        {
            "form": form,
            "tytul": "Edytuj zamówienie",
        },
    )


@login_required
def zamowienie_usun(request, zamowienie_id):
    zamowienie = get_object_or_404(Zamowienie, id=zamowienie_id)

    if request.method == "POST":
        zamowienie.delete()
        messages.success(request, "Zamówienie zostało usunięte.")
        return redirect("core:zamowienia_lista")

    return render(
        request,
        "zamowienia/usun.html",
        {
            "zamowienie": zamowienie,
        },
    )


@login_required
def zamowienie_szczegoly(request, zamowienie_id):
    zamowienie = get_object_or_404(
        Zamowienie.objects.select_related("klient"),
        id=zamowienie_id,
    )

    pozycje = (
        zamowienie.pozycje.select_related(
            "stan_magazynowy",
            "stan_magazynowy__magazyn",
            "stan_magazynowy__material",
            "stan_magazynowy__rozmiar",
        )
        .prefetch_related("uslugi")
        .all()
    )

    suma = sum(p.wartosc for p in pozycje)

    return render(
        request,
        "zamowienia/szczegoly.html",
        {
            "zamowienie": zamowienie,
            "pozycje": pozycje,
            "suma": suma,
            "rabat_form": RabatForm(instance=zamowienie),
        },
    )


@login_required
def zamowienie_ustaw_rabat(request, zamowienie_id):
    zamowienie = get_object_or_404(Zamowienie, id=zamowienie_id)

    if request.method == "POST":
        form = RabatForm(request.POST, instance=zamowienie)

        if form.is_valid():
            form.save()
            aktualizuj_platnosc_zamowienia(zamowienie)
            messages.success(request, "Rabat został zapisany.")

    return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)


@login_required
def zamowienie_przyjmij(request, zamowienie_id):
    zamowienie = get_object_or_404(
        Zamowienie.objects.prefetch_related(
            "pozycje__stan_magazynowy",
            "pozycje__stan_magazynowy__material",
            "pozycje__stan_magazynowy__rozmiar",
            "pozycje__stan_magazynowy__magazyn",
            "pozycje__uslugi",
        ),
        id=zamowienie_id,
    )

    if request.method != "POST":
        return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)

    if zamowienie.status != "ROBOCZE":
        messages.error(
            request, "To zamówienie zostało już przyjęte albo nie jest robocze."
        )
        return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)

    if not zamowienie.pozycje.exists():
        messages.error(request, "Nie można przyjąć zamówienia bez pozycji.")
        return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)

    try:
        with transaction.atomic():
            for pozycja in (
                zamowienie.pozycje.select_related(
                    "stan_magazynowy",
                    "stan_magazynowy__material",
                    "stan_magazynowy__rozmiar",
                    "stan_magazynowy__magazyn",
                )
                .prefetch_related("uslugi")
                .all()
            ):

                stan = pozycja.stan_magazynowy

                if not stan:
                    messages.error(
                        request,
                        "Jedna z pozycji nie ma wybranego arkusza magazynowego.",
                    )
                    raise ValueError("Brak arkusza")

                stan = StanMagazynowy.objects.select_for_update().get(id=stan.id)

                if stan.dostepne < pozycja.ilosc:
                    messages.error(
                        request,
                        f"Brak wystarczającej ilości: {stan}. "
                        f"Potrzeba {pozycja.ilosc}, dostępne {stan.dostepne}.",
                    )
                    raise ValueError("Brak materiału")

                stan.zarezerwowano += pozycja.ilosc
                stan.save(update_fields=["zarezerwowano"])

                ProcesMagazynowy.objects.create(
                    magazyn=stan.magazyn,
                    material=stan.material,
                    rozmiar=stan.rozmiar,
                    pracownik=request.user,
                    typ="REZERWACJA",
                    ilosc=pozycja.ilosc,
                    opis=f"Rezerwacja do zamówienia {zamowienie.numer or zamowienie.id}",
                )

                Zadanie.objects.get_or_create(
                    pozycja=pozycja,
                    rola_docelowa="MAGAZYN",
                    typ_uslugi=None,
                    defaults={
                        "status": "NOWE",
                        "uwagi": "Przygotowanie materiału do zamówienia.",
                    },
                )

                for usluga in pozycja.uslugi.all():
                    Zadanie.objects.get_or_create(
                        pozycja=pozycja,
                        rola_docelowa="PRODUKCJA",
                        typ_uslugi=usluga,
                        defaults={
                            "status": "NOWE",
                            "uwagi": f"Wykonać usługę: {usluga.nazwa}",
                        },
                    )

            zamowienie.status = "ZATWIERDZONE"
            zamowienie.save(update_fields=["status"])

            aktualizuj_platnosc_zamowienia(zamowienie)

    except ValueError:
        return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)

    messages.success(
        request,
        "Zamówienie zostało przyjęte, materiały zostały zarezerwowane, utworzono zadania i płatność.",
    )
    return redirect("core:zamowienia_lista")


@login_required
def zamowienie_zakoncz(request, zamowienie_id):
    zamowienie = get_object_or_404(
        Zamowienie.objects.prefetch_related(
            "pozycje__stan_magazynowy",
            "pozycje__stan_magazynowy__magazyn",
            "pozycje__stan_magazynowy__material",
            "pozycje__stan_magazynowy__rozmiar",
        ),
        id=zamowienie_id,
    )

    if request.method != "POST":
        return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)

    if zamowienie.status != "WYKONANE":
        messages.error(request, "Zakończyć można tylko zamówienie wykonane.")
        return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)

    with transaction.atomic():
        for pozycja in zamowienie.pozycje.select_related(
            "stan_magazynowy",
            "stan_magazynowy__magazyn",
            "stan_magazynowy__material",
            "stan_magazynowy__rozmiar",
        ):
            stan = pozycja.stan_magazynowy

            if not stan:
                continue

            stan = StanMagazynowy.objects.select_for_update().get(id=stan.id)

            ilosc = pozycja.ilosc

            stan.zarezerwowano = max(0, stan.zarezerwowano - ilosc)
            stan.ilosc = max(0, stan.ilosc - ilosc)

            stan.save(update_fields=["ilosc", "zarezerwowano"])

            ProcesMagazynowy.objects.create(
                magazyn=stan.magazyn,
                material=stan.material,
                rozmiar=stan.rozmiar,
                pracownik=request.user,
                typ="WYDANIE",
                ilosc=ilosc,
                opis=f"Wydanie do zamówienia {zamowienie.numer or zamowienie.id}",
            )

        zamowienie.status = "ZAKONCZONE"
        zamowienie.save(update_fields=["status"])

    messages.success(
        request, "Zamówienie zostało zakończone, a rezerwacja zdjęta z magazynu."
    )
    return redirect("core:zamowienia_lista")


@login_required
def pozycja_dodaj(request, zamowienie_id):
    zamowienie = get_object_or_404(Zamowienie, id=zamowienie_id)

    if request.method == "POST":
        form = PozycjaZamowieniaForm(request.POST)

        if form.is_valid():
            pozycja = form.save(commit=False)
            pozycja.zamowienie = zamowienie
            pozycja.save()
            aktualizuj_platnosc_zamowienia(zamowienie)

            messages.success(request, "Pozycja zamówienia została dodana.")
            return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)
    else:
        form = PozycjaZamowieniaForm()

    return render(
        request,
        "pozycje_zamowienia/formularz.html",
        {
            "form": form,
            "tytul": "Dodaj pozycję zamówienia",
            "zamowienie": zamowienie,
        },
    )


@login_required
def pozycja_edytuj(request, pozycja_id):
    pozycja = get_object_or_404(
        PozycjaZamowienia.objects.select_related(
            "zamowienie",
            "stan_magazynowy",
            "stan_magazynowy__material",
            "stan_magazynowy__rozmiar",
        ),
        id=pozycja_id,
    )

    zamowienie = pozycja.zamowienie

    if request.method == "POST":
        form = PozycjaZamowieniaForm(request.POST, instance=pozycja)

        if form.is_valid():
            form.save()
            aktualizuj_platnosc_zamowienia(zamowienie)
            messages.success(request, "Pozycja zamówienia została zaktualizowana.")
            return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)
    else:
        form = PozycjaZamowieniaForm(instance=pozycja)

    return render(
        request,
        "pozycje_zamowienia/formularz.html",
        {
            "form": form,
            "tytul": "Edytuj pozycję zamówienia",
            "zamowienie": zamowienie,
        },
    )


@login_required
def pozycja_usun(request, pozycja_id):
    pozycja = get_object_or_404(PozycjaZamowienia, id=pozycja_id)
    zamowienie = pozycja.zamowienie

    if request.method == "POST":
        pozycja.delete()
        aktualizuj_platnosc_zamowienia(zamowienie)
        messages.success(request, "Pozycja zamówienia została usunięta.")
        return redirect("core:zamowienie_szczegoly", zamowienie_id=zamowienie.id)

    return render(
        request,
        "pozycje_zamowienia/usun.html",
        {
            "pozycja": pozycja,
            "zamowienie": zamowienie,
        },
    )


@login_required
def moje_prace(request):
    try:
        profil = request.user.pracownikprofil
        rola = profil.rola
    except PracownikProfil.DoesNotExist:
        if request.user.is_superuser:
            rola = "ADMIN"
        else:
            messages.error(
                request, "Twoje konto nie ma przypisanego profilu pracownika."
            )
            return render(
                request,
                "moje_prace/lista.html",
                {
                    "zadania": [],
                },
            )

    zadania = Zadanie.objects.select_related(
        "pozycja",
        "pozycja__zamowienie",
        "pozycja__zamowienie__klient",
        "pozycja__stan_magazynowy",
        "pozycja__stan_magazynowy__material",
        "pozycja__stan_magazynowy__rozmiar",
        "typ_uslugi",
        "przypisany_pracownik",
    ).filter(
        status__in=["NOWE", "W_REALIZACJI"],
    )

    if rola != "ADMIN":
        zadania = zadania.filter(rola_docelowa=rola)

    zadania = zadania.order_by("data_utworzenia")

    return render(
        request,
        "moje_prace/lista.html",
        {
            "zadania": zadania,
        },
    )


@login_required
def zadanie_status(request, zadanie_id, status):
    zadanie = get_object_or_404(Zadanie, id=zadanie_id)

    if request.method != "POST":
        return redirect("core:moje_prace")

    if status not in [
        "W_REALIZACJI",
        "ZREALIZOWANE",
    ]:
        messages.error(request, "Niepoprawny status.")
        return redirect("core:moje_prace")

    zadanie.przypisany_pracownik = request.user
    zadanie.status = status
    zadanie.save()
    zamowienie = zadanie.pozycja.zamowienie

    if status == "W_REALIZACJI" and zamowienie.status == "ZATWIERDZONE":
        zamowienie.status = "W_REALIZACJI"
        zamowienie.save(update_fields=["status"])
    messages.success(request, "Status zadania został zaktualizowany.")

    return redirect("core:moje_prace")


@login_required
def magazyn_lista(request):
    stany = (
        StanMagazynowy.objects.select_related(
            "magazyn",
            "material",
            "rozmiar",
        )
        .exclude(
            ilosc=0,
            zarezerwowano=0,
        )
        .order_by(
            "magazyn__nazwa",
            "material__nazwa",
            "rozmiar__szerokosc_mm",
            "rozmiar__wysokosc_mm",
        )
    )

    return render(
        request,
        "magazyn/lista.html",
        {
            "stany": stany,
        },
    )


@login_required
def proces_magazynowy_dodaj(request):
    if request.method == "POST":
        form = ProcesMagazynowyForm(request.POST)

        if form.is_valid():
            proces = form.save(commit=False)
            proces.pracownik = request.user

            stan, created = StanMagazynowy.objects.get_or_create(
                magazyn=proces.magazyn,
                material=proces.material,
                rozmiar=proces.rozmiar,
                defaults={
                    "ilosc": 0,
                    "zarezerwowano": 0,
                },
            )

            if proces.typ == "PRZYJECIE":
                stan.ilosc += proces.ilosc

            elif proces.typ == "WYDANIE":
                if stan.dostepne < proces.ilosc:
                    messages.error(
                        request,
                        "Nie można wydać więcej materiału niż jest dostępne na magazynie.",
                    )
                    return redirect("core:proces_magazynowy_dodaj")

                stan.ilosc -= proces.ilosc

            else:
                messages.error(request, "Nieobsługiwany typ operacji magazynowej.")
                return redirect("core:proces_magazynowy_dodaj")

            stan.save()
            proces.save()

            messages.success(request, "Czynność magazynowa została zapisana.")
            return redirect("core:magazyn_lista")

    else:
        form = ProcesMagazynowyForm()

    return render(
        request,
        "magazyn/formularz.html",
        {
            "form": form,
            "tytul": "Wykonaj czynność na magazynie",
        },
    )


@login_required
def magazyn_dodaj(request):

    if not (request.user.is_superuser or request.user.pracownikprofil.rola == "ADMIN"):
        messages.error(request, "Brak uprawnień.")
        return redirect("core:magazyn_lista")

    if request.method == "POST":
        form = MagazynForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Magazyn został dodany.")

            return redirect("core:magazyn_lista")

    else:
        form = MagazynForm()

    return render(
        request,
        "magazyn/magazyn_formularz.html",
        {
            "form": form,
            "tytul": "Dodaj magazyn",
        },
    )


@login_required
def inwentaryzacja_magazynu(request, stan_id):
    stan = get_object_or_404(
        StanMagazynowy,
        id=stan_id,
    )

    if request.method == "POST":
        form = InwentaryzacjaForm(request.POST)

        if form.is_valid():
            nowa_ilosc = form.cleaned_data["nowa_ilosc"]

            stan.ilosc = nowa_ilosc
            stan.save()

            ProcesMagazynowy.objects.create(
                magazyn=stan.magazyn,
                material=stan.material,
                rozmiar=stan.rozmiar,
                pracownik=request.user,
                typ="INWENTARYZACJA",
                ilosc=nowa_ilosc,
                opis=form.cleaned_data["opis"],
            )

            messages.success(
                request,
                "Inwentaryzacja została zapisana.",
            )

            return redirect("core:magazyn_lista")

    else:
        form = InwentaryzacjaForm(
            initial={
                "nowa_ilosc": stan.ilosc,
            }
        )

    return render(
        request,
        "magazyn/inwentaryzacja.html",
        {
            "stan": stan,
            "form": form,
        },
    )


@login_required
def historia_magazynu(request):
    procesy = ProcesMagazynowy.objects.select_related(
        "magazyn",
        "material",
        "pracownik",
        "cofnieta_przez",
    ).order_by("-data")

    return render(
        request,
        "magazyn/historia.html",
        {
            "procesy": procesy,
        },
    )


@login_required
def cofnij_operacje_magazynowa(request, proces_id):
    proces = get_object_or_404(
        ProcesMagazynowy.objects.select_related("magazyn", "material"),
        id=proces_id,
    )

    if proces.cofnieta:
        messages.error(request, "Ta operacja została już cofnięta.")
        return redirect("core:historia_magazynu")

    if proces.typ == "COFNIECIE":
        messages.error(request, "Nie można cofnąć operacji cofnięcia.")
        return redirect("core:historia_magazynu")

    if request.method == "POST":
        form = CofniecieOperacjiForm(request.POST)

        if form.is_valid():
            stan, created = StanMagazynowy.objects.get_or_create(
                magazyn=proces.magazyn,
                material=proces.material,
                rozmiar=proces.rozmiar,
                defaults={"ilosc": 0, "zarezerwowano": 0},
            )

            if proces.typ == "PRZYJECIE":
                if stan.ilosc < proces.ilosc:
                    messages.error(
                        request,
                        "Nie można cofnąć przyjęcia, bo stan magazynowy jest za niski.",
                    )
                    return redirect("core:historia_magazynu")

                stan.ilosc -= proces.ilosc

            elif proces.typ == "WYDANIE":
                stan.ilosc += proces.ilosc

            elif proces.typ == "INWENTARYZACJA":
                stan.ilosc -= proces.ilosc

            stan.save()

            proces.cofnieta = True
            proces.powod_cofniecia = form.cleaned_data["powod"]
            proces.cofnieta_przez = request.user
            proces.data_cofniecia = timezone.now()
            proces.save()

            ProcesMagazynowy.objects.create(
                magazyn=proces.magazyn,
                material=proces.material,
                rozmiar=proces.rozmiar,
                pracownik=request.user,
                typ="COFNIECIE",
                ilosc=proces.ilosc,
                opis=form.cleaned_data["powod"],
                operacja_powiazana=proces,
            )

            messages.success(request, "Operacja została cofnięta.")
            return redirect("core:historia_magazynu")
    else:
        form = CofniecieOperacjiForm()

    return render(
        request,
        "magazyn/cofnij.html",
        {
            "form": form,
            "proces": proces,
        },
    )


@login_required
def magazyn_edytuj(request, magazyn_id):

    magazyn = get_object_or_404(
        Magazyn,
        id=magazyn_id,
    )

    if not (request.user.is_superuser or request.user.pracownikprofil.rola == "ADMIN"):
        messages.error(request, "Brak uprawnień.")
        return redirect("core:magazyn_lista")

    if request.method == "POST":
        form = MagazynForm(
            request.POST,
            instance=magazyn,
        )

        if form.is_valid():
            form.save()

            messages.success(request, "Magazyn został zaktualizowany.")

            return redirect("core:magazyn_lista")

    else:
        form = MagazynForm(instance=magazyn)

    return render(
        request,
        "magazyn/magazyn_formularz.html",
        {
            "form": form,
            "tytul": "Edytuj magazyn",
        },
    )


@login_required
def platnosci_lista(request):
    status = request.GET.get("status", "")

    platnosci = Platnosc.objects.select_related(
        "zamowienie",
        "zamowienie__klient",
    ).order_by("-data_utworzenia")

    if status:
        platnosci = platnosci.filter(status=status)

    return render(
        request,
        "platnosci/lista.html",
        {
            "platnosci": platnosci,
            "status": status,
            "statusy": Platnosc.STATUS_CHOICES,
        },
    )


@login_required
def platnosc_oznacz_oplacona(request, platnosc_id):
    platnosc = get_object_or_404(Platnosc, id=platnosc_id)

    if request.method == "POST":
        platnosc.status = "OPLACONA"
        platnosc.save(update_fields=["status"])

        messages.success(request, "Płatność została oznaczona jako opłacona.")

    return redirect("core:platnosci_lista")


@login_required
def platnosc_anuluj_status(request, platnosc_id):
    platnosc = get_object_or_404(Platnosc, id=platnosc_id)

    if request.method == "POST":
        platnosc.status = "ANULOWANA"
        platnosc.save(update_fields=["status"])

        messages.success(request, "Płatność została anulowana.")

    return redirect("core:platnosci_lista")


@login_required
def platnosc_dodaj(request):
    if request.method == "POST":
        form = PlatnoscForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Płatność została dodana.")
            return redirect("core:platnosci_lista")
    else:
        form = PlatnoscForm()

    return render(
        request,
        "platnosci/formularz.html",
        {
            "form": form,
            "tytul": "Dodaj płatność",
        },
    )


@login_required
def platnosc_edytuj(request, platnosc_id):
    platnosc = get_object_or_404(Platnosc, id=platnosc_id)

    if request.method == "POST":
        form = PlatnoscForm(request.POST, instance=platnosc)

        if form.is_valid():
            form.save()
            messages.success(request, "Płatność została zaktualizowana.")
            return redirect("core:platnosci_lista")
    else:
        form = PlatnoscForm(instance=platnosc)

    return render(
        request,
        "platnosci/formularz.html",
        {
            "form": form,
            "tytul": "Edytuj płatność",
        },
    )


@login_required
def platnosc_usun(request, platnosc_id):
    platnosc = get_object_or_404(Platnosc, id=platnosc_id)

    if request.method == "POST":
        platnosc.delete()
        messages.success(request, "Płatność została usunięta.")
        return redirect("core:platnosci_lista")

    return render(
        request,
        "platnosci/usun.html",
        {
            "platnosc": platnosc,
        },
    )


@login_required
def pracownicy_lista(request):
    query = request.GET.get("q", "")

    pracownicy = PracownikProfil.objects.select_related("user").order_by(
        "user__last_name"
    )

    if query:
        pracownicy = (
            pracownicy.filter(user__first_name__icontains=query)
            | pracownicy.filter(user__last_name__icontains=query)
            | pracownicy.filter(user__username__icontains=query)
            | pracownicy.filter(user__email__icontains=query)
        )

    return render(
        request,
        "pracownicy/lista.html",
        {
            "pracownicy": pracownicy,
            "query": query,
        },
    )


@login_required
def pracownik_dodaj(request):
    if request.method == "POST":
        form = PracownikCreateForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["haslo"],
                first_name=form.cleaned_data["imie"],
                last_name=form.cleaned_data["nazwisko"],
                email=form.cleaned_data["email"],
            )

            if form.cleaned_data["rola"] == "ADMIN":
                user.is_staff = True
                user.save()

            PracownikProfil.objects.create(
                user=user,
                telefon=form.cleaned_data["telefon"],
                rola=form.cleaned_data["rola"],
            )

            messages.success(
                request, "Pracownik i konto użytkownika zostały utworzone."
            )
            return redirect("core:pracownicy_lista")
    else:
        form = PracownikCreateForm()

    return render(
        request,
        "pracownicy/formularz.html",
        {
            "form": form,
            "tytul": "Dodaj pracownika",
        },
    )


@login_required
def pracownik_edytuj(request, pracownik_id):
    profil = get_object_or_404(PracownikProfil, id=pracownik_id)
    user = profil.user

    if request.method == "POST":
        form = PracownikEditForm(request.POST, instance=profil)

        if form.is_valid():
            profil = form.save(commit=False)
            profil.save()

            user.first_name = form.cleaned_data["imie"]
            user.last_name = form.cleaned_data["nazwisko"]
            user.email = form.cleaned_data["email"]

            if profil.rola == "ADMIN":
                user.is_staff = True
            else:
                user.is_staff = False

            user.save()

            messages.success(request, "Dane pracownika zostały zaktualizowane.")
            return redirect("core:pracownicy_lista")
    else:
        form = PracownikEditForm(
            instance=profil,
            initial={
                "imie": user.first_name,
                "nazwisko": user.last_name,
                "email": user.email,
            },
        )

    return render(
        request,
        "pracownicy/formularz.html",
        {
            "form": form,
            "tytul": "Edytuj pracownika",
        },
    )


@login_required
def pracownik_aktywuj(request, pracownik_id):
    profil = get_object_or_404(PracownikProfil, id=pracownik_id)

    if request.method == "POST":
        profil.user.is_active = True
        profil.user.save()

        messages.success(request, "Pracownik został aktywowany.")
        return redirect("core:pracownicy_lista")

    return redirect("core:pracownicy_lista")


@login_required
def pracownik_dezaktywuj(request, pracownik_id):
    profil = get_object_or_404(PracownikProfil, id=pracownik_id)

    if request.method == "POST":
        profil.user.is_active = False
        profil.user.save()

        messages.success(request, "Pracownik został dezaktywowany.")
        return redirect("core:pracownicy_lista")

    return redirect("core:pracownicy_lista")


@login_required
def edycja_uslug(request):
    materialy = Material.objects.all().order_by("nazwa")
    rozmiary = RozmiarBlachy.objects.all().order_by("szerokosc_mm", "wysokosc_mm")
    typy_uslug = TypUslugi.objects.all().order_by("nazwa")

    uslugi_z_cenami = []

    for usluga in typy_uslug:
        ostatnia_cena = (
            Cennik.objects.filter(typ_uslugi=usluga).order_by("-data_od").first()
        )

        uslugi_z_cenami.append(
            {
                "usluga": usluga,
                "cena": ostatnia_cena.cena if ostatnia_cena else None,
            }
        )

    return render(
        request,
        "edycja_uslug/panel.html",
        {
            "materialy": materialy,
            "rozmiary": rozmiary,
            "uslugi_z_cenami": uslugi_z_cenami,
        },
    )
