from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import KlientForm, MaterialForm
from .models import Klient, Material


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