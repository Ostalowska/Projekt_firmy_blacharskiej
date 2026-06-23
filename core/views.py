from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    KlientForm,
    MaterialForm,
    RozmiarBlachyForm,
    TypUslugiForm,
    ZamowienieForm,
)

from .models import Klient, Material, RozmiarBlachy, TypUslugi, Zamowienie


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