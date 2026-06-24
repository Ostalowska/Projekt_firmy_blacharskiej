from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .forms import (
    KlientForm,
    MaterialForm,
    RozmiarBlachyForm,
    TypUslugiForm,
    ZamowienieForm,
    PozycjaZamowieniaForm,
    ProcesMagazynowyForm,
    PlatnoscForm,
    PracownikCreateForm,
    PracownikEditForm,
)

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


@login_required
def index(request):
    return render(request, "index.html")


@login_required
def klienci_lista(request):
    query = request.GET.get("q", "")

    klienci = Klient.objects.all().order_by("-id")

    if query:
        klienci = klienci.filter(
            imie__icontains=query
        ) | klienci.filter(
            nazwisko__icontains=query
        ) | klienci.filter(
            email__icontains=query
        ) | klienci.filter(
            nazwa_firmy__icontains=query
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
        materialy = materialy.filter(
            nazwa__icontains=query
        )

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

            messages.success(
                request,
                "Materiał został dodany."
            )

            return redirect("core:materialy_lista")

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

            messages.success(
                request,
                "Materiał został zaktualizowany."
            )

            return redirect("core:materialy_lista")

    else:
        form = MaterialForm(
            instance=material
        )

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

        messages.success(
            request,
            "Materiał został usunięty."
        )

        return redirect("core:materialy_lista")

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

    rozmiary = RozmiarBlachy.objects.all().order_by("nazwa")

    if query:
        rozmiary = rozmiary.filter(nazwa__icontains=query)

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
            return redirect("core:rozmiary_lista")
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
            return redirect("core:rozmiary_lista")
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
        return redirect("core:rozmiary_lista")

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
            form.save()
            messages.success(request, "Typ usługi został dodany.")
            return redirect("core:typy_uslug_lista")
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
            form.save()
            messages.success(request, "Typ usługi został zaktualizowany.")
            return redirect("core:typy_uslug_lista")
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
        return redirect("core:typy_uslug_lista")

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

    zamowienia = Zamowienie.objects.select_related("klient").all().order_by("-data_utworzenia")

    if query:
        zamowienia = zamowienia.filter(
            klient__imie__icontains=query
        ) | zamowienia.filter(
            klient__nazwisko__icontains=query
        ) | zamowienia.filter(
            klient__email__icontains=query
        ) | zamowienia.filter(
            klient__nazwa_firmy__icontains=query
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
    if request.method == "POST":
        form = ZamowienieForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Zamówienie zostało utworzone.")
            return redirect("core:zamowienia_lista")
    else:
        form = ZamowienieForm()

    return render(
        request,
        "zamowienia/formularz.html",
        {
            "form": form,
            "tytul": "Dodaj zamówienie",
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

    pozycje = zamowienie.pozycje.select_related(
        "material",
        "rozmiar",
        "typ_uslugi",
        "przypisany_pracownik",
    ).all()

    suma = sum(p.cena * p.ilosc for p in pozycje)

    return render(
        request,
        "zamowienia/szczegoly.html",
        {
            "zamowienie": zamowienie,
            "pozycje": pozycje,
            "suma": suma,
        },
    )


@login_required
def pozycja_dodaj(request, zamowienie_id):
    zamowienie = get_object_or_404(Zamowienie, id=zamowienie_id)

    if request.method == "POST":
        form = PozycjaZamowieniaForm(request.POST)

        if form.is_valid():
            pozycja = form.save(commit=False)
            pozycja.zamowienie = zamowienie
            pozycja.save()

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
    pozycja = get_object_or_404(PozycjaZamowienia, id=pozycja_id)
    zamowienie = pozycja.zamowienie

    if request.method == "POST":
        form = PozycjaZamowieniaForm(request.POST, instance=pozycja)

        if form.is_valid():
            form.save()
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
    pozycje = PozycjaZamowienia.objects.select_related(
        "zamowienie",
        "zamowienie__klient",
        "material",
        "rozmiar",
        "typ_uslugi",
    ).filter(
        przypisany_pracownik=request.user
    ).order_by("-id")

    return render(
        request,
        "moje_prace/lista.html",
        {
            "pozycje": pozycje,
        },
    )


@login_required
def zmien_status_pozycji(request, pozycja_id):
    pozycja = get_object_or_404(
        PozycjaZamowienia,
        id=pozycja_id,
        przypisany_pracownik=request.user,
    )

    if request.method == "POST":
        nowy_status = request.POST.get("status")

        if nowy_status in ["PRZYJETA", "REALIZACJA", "ZREALIZOWANA"]:
            pozycja.status = nowy_status
            pozycja.save()

            zamowienie = pozycja.zamowienie
            wszystkie_zrealizowane = zamowienie.pozycje.exists() and all(
                p.status == "ZREALIZOWANA"
                for p in zamowienie.pozycje.all()
            )

            if wszystkie_zrealizowane:
                zamowienie.status = "GOTOWE"
                zamowienie.save()
                messages.success(
                    request,
                    f"Pozycja zaktualizowana. Zamówienie #{zamowienie.id} jest gotowe do odbioru.",
                )
            else:
                if zamowienie.status == "PRZYJETE":
                    zamowienie.status = "REALIZACJA"
                    zamowienie.save()

                messages.success(request, "Status pozycji został zaktualizowany.")

    return redirect("core:moje_prace")

@login_required
def magazyn_lista(request):
    stany = StanMagazynowy.objects.select_related(
        "magazyn",
        "material",
    ).order_by("material__nazwa")

    procesy = ProcesMagazynowy.objects.select_related(
        "magazyn",
        "material",
        "pracownik",
    ).order_by("-data")[:20]

    return render(
        request,
        "magazyn/lista.html",
        {
            "stany": stany,
            "procesy": procesy,
        },
    )


@login_required
def proces_magazynowy_dodaj(request):
    if request.method == "POST":
        form = ProcesMagazynowyForm(request.POST)

        if form.is_valid():
            proces = form.save(commit=False)
            proces.pracownik = request.user

            magazyn = proces.magazyn
            material = proces.material
            ilosc = proces.ilosc

            stan, created = StanMagazynowy.objects.get_or_create(
                magazyn=magazyn,
                material=material,
                defaults={"ilosc": 0},
            )

            if proces.typ == "PRZYJECIE":
                stan.ilosc += ilosc
                stan.save()
                proces.save()

                messages.success(
                    request,
                    "Materiał został przyjęty na magazyn.",
                )

                return redirect("core:magazyn_lista")

            if proces.typ == "WYDANIE":
                if stan.ilosc < ilosc:
                    messages.error(
                        request,
                        "Nie można wydać więcej materiału niż jest na stanie.",
                    )
                    return redirect("core:proces_magazynowy_dodaj")

                stan.ilosc -= ilosc
                stan.save()
                proces.save()

                messages.success(
                    request,
                    "Materiał został wydany z magazynu.",
                )

                return redirect("core:magazyn_lista")

            if proces.typ == "INWENTARYZACJA":
                stan.ilosc = ilosc
                stan.save()
                proces.save()

                messages.success(
                    request,
                    "Stan magazynowy został zaktualizowany przez inwentaryzację.",
                )

                return redirect("core:magazyn_lista")

    else:
        form = ProcesMagazynowyForm()

    return render(
        request,
        "magazyn/formularz.html",
        {
            "form": form,
            "tytul": "Dodaj proces magazynowy",
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

    pracownicy = PracownikProfil.objects.select_related("user").order_by("user__last_name")

    if query:
        pracownicy = pracownicy.filter(
            user__first_name__icontains=query
        ) | pracownicy.filter(
            user__last_name__icontains=query
        ) | pracownicy.filter(
            user__username__icontains=query
        ) | pracownicy.filter(
            user__email__icontains=query
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

            messages.success(request, "Pracownik i konto użytkownika zostały utworzone.")
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
            user.is_active = form.cleaned_data["aktywny"]

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
                "aktywny": user.is_active,
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
def pracownik_dezaktywuj(request, pracownik_id):
    profil = get_object_or_404(PracownikProfil, id=pracownik_id)

    if request.method == "POST":
        profil.user.is_active = False
        profil.user.save()

        messages.success(request, "Pracownik został dezaktywowany.")
        return redirect("core:pracownicy_lista")

    return render(
        request,
        "pracownicy/dezaktywuj.html",
        {
            "pracownik": profil,
        },
    )