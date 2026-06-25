from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Klient(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    adres = models.CharField(max_length=255)
    nazwa_firmy = models.CharField(max_length=100, blank=True)
    nip = models.CharField(max_length=20, blank=True)

    def __str__(self):
        firma = f" ({self.nazwa_firmy})" if self.nazwa_firmy else ""
        return f"{self.imie} {self.nazwisko}{firma}"


class PracownikProfil(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Administrator"),
        ("MAGAZYN", "Magazynier"),
        ("PRODUKCJA", "Pracownik produkcji"),
        ("KSIEGOWOSC", "Księgowość"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=20, blank=True)
    rola = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.get_rola_display()}"


class Material(models.Model):
    nazwa = models.CharField(max_length=100)
    producent = models.CharField(max_length=100, blank=True)
    grubosc_mm = models.DecimalField(max_digits=5, decimal_places=2)
    cena_za_m2 = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nazwa} {self.grubosc_mm} mm"


class RozmiarBlachy(models.Model):
    szerokosc_mm = models.PositiveIntegerField()
    wysokosc_mm = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.szerokosc_mm} x {self.wysokosc_mm} mm"


class TypUslugi(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa


class Cennik(models.Model):
    typ_uslugi = models.ForeignKey(TypUslugi, on_delete=models.CASCADE)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    data_od = models.DateField()

    def __str__(self):
        return f"{self.typ_uslugi} - {self.cena} PLN"


class Magazyn(models.Model):
    nazwa = models.CharField(max_length=100)
    adres = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa


class StanMagazynowy(models.Model):
    magazyn = models.ForeignKey(Magazyn, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    rozmiar = models.ForeignKey(
        RozmiarBlachy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    ilosc = models.IntegerField(default=0)
    zarezerwowano = models.IntegerField(default=0)

    class Meta:
        unique_together = ("magazyn", "material", "rozmiar")

    @property
    def dostepne(self):
        return self.ilosc - self.zarezerwowano

    def __str__(self):
        return f"{self.material} | {self.rozmiar} | stan: {self.ilosc}, rezerwacja: {self.zarezerwowano}"

class Zamowienie(models.Model):
    STATUS_CHOICES = [
        ("ROBOCZE", "Robocze"),
        ("ZATWIERDZONE", "Zatwierdzone"),
        ("W_REALIZACJI", "W realizacji"),
        ("WYKONANE", "Wykonane"),
        ("GOTOWE_DO_ODBIORU", "Gotowe do odbioru"),
        ("ZAKONCZONE", "Zakończone"),
        ("ANULOWANE", "Anulowane"),
    ]

    RABAT_CHOICES = [
        ("BRAK", "Brak rabatu"),
        ("PROCENT", "Procentowy"),
        ("KWOTA", "Kwotowy"),
    ]

    numer = models.CharField(max_length=30, unique=True, blank=True, null=True)

    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)

    data_utworzenia = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="ROBOCZE",
    )

    uwagi = models.TextField(blank=True)

    rabat_typ = models.CharField(
        max_length=20,
        choices=RABAT_CHOICES,
        default="BRAK",
    )

    rabat_wartosc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    kwota_koncowa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.numer:
            self.numer = f"ZAM-{self.data_utworzenia.year}-{self.id:04d}"
            super().save(update_fields=["numer"])

    def suma_pozycji(self):
        return sum((pozycja.wartosc for pozycja in self.pozycje.all()), Decimal("0.00"))

    def przelicz_kwote(self):
        suma = self.suma_pozycji()

        if self.rabat_typ == "PROCENT":
            rabat = suma * (self.rabat_wartosc / Decimal("100"))
            wynik = suma - rabat
        elif self.rabat_typ == "KWOTA":
            wynik = suma - self.rabat_wartosc
        else:
            wynik = suma

        if wynik < 0:
            wynik = Decimal("0.00")

        self.kwota_koncowa = wynik
        self.save(update_fields=["kwota_koncowa"])

        return self.kwota_koncowa

    def __str__(self):
        return self.numer or f"Zamówienie #{self.id}"


class PozycjaZamowienia(models.Model):
    zamowienie = models.ForeignKey(
        Zamowienie,
        on_delete=models.CASCADE,
        related_name="pozycje",
    )

    stan_magazynowy = models.ForeignKey(
        StanMagazynowy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    rozmiar = models.ForeignKey(
        RozmiarBlachy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    czy_niestandardowy = models.BooleanField(default=False)

    szerokosc_niestandardowa_mm = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    wysokosc_niestandardowa_mm = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    typ_uslugi = models.ForeignKey(
        TypUslugi,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    ilosc = models.PositiveIntegerField(default=1)

    cena_jednostkowa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    wartosc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    def powierzchnia_m2(self):
        if self.czy_niestandardowy:
            szer = self.szerokosc_niestandardowa_mm or 0
            wys = self.wysokosc_niestandardowa_mm or 0
        elif self.rozmiar:
            szer = self.rozmiar.szerokosc_mm
            wys = self.rozmiar.wysokosc_mm
        else:
            szer = 0
            wys = 0

        return Decimal(szer * wys) / Decimal("1000000")

    def przelicz_cene(self):
        powierzchnia = self.powierzchnia_m2()
        cena_materialu = powierzchnia * self.material.cena_za_m2

        cena_uslugi = Decimal("0.00")
        if self.typ_uslugi:
            cennik = (
                Cennik.objects.filter(typ_uslugi=self.typ_uslugi)
                .order_by("-data_od")
                .first()
            )
            if cennik:
                cena_uslugi = cennik.cena

        self.cena_jednostkowa = cena_materialu + cena_uslugi
        self.wartosc = self.cena_jednostkowa * self.ilosc

    def save(self, *args, **kwargs):
        self.przelicz_cene()
        super().save(*args, **kwargs)
        self.zamowienie.przelicz_kwote()

    def delete(self, *args, **kwargs):
        zamowienie = self.zamowienie
        super().delete(*args, **kwargs)
        zamowienie.przelicz_kwote()

    def __str__(self):
        return f"{self.material} x {self.ilosc}"


class Zadanie(models.Model):
    STATUS_CHOICES = [
        ("NOWE", "Nowe"),
        ("W_REALIZACJI", "W realizacji"),
        ("ZREALIZOWANE", "Zrealizowane"),
        ("ODRZUCONE", "Odrzucone"),
    ]

    ROLA_DOCELOWA_CHOICES = [
        ("MAGAZYN", "Magazynier"),
        ("PRODUKCJA", "Pracownik produkcji"),
    ]

    pozycja = models.ForeignKey(
        PozycjaZamowienia,
        on_delete=models.CASCADE,
        related_name="zadania",
    )

    typ_uslugi = models.ForeignKey(
        TypUslugi,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    rola_docelowa = models.CharField(
        max_length=20,
        choices=ROLA_DOCELOWA_CHOICES,
    )

    przypisany_pracownik = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="NOWE",
    )

    data_utworzenia = models.DateTimeField(auto_now_add=True)
    data_zakonczenia = models.DateTimeField(null=True, blank=True)
    uwagi = models.TextField(blank=True)

    def czy_zakonczone(self):
        return self.status in ["ZREALIZOWANE", "ODRZUCONE"]

    def save(self, *args, **kwargs):
        if self.status in ["ZREALIZOWANE", "ODRZUCONE"] and not self.data_zakonczenia:
            self.data_zakonczenia = timezone.now()

        super().save(*args, **kwargs)

        zamowienie = self.pozycja.zamowienie
        zadania = Zadanie.objects.filter(pozycja__zamowienie=zamowienie)

        if zadania.exists() and all(z.czy_zakonczone() for z in zadania):
            zamowienie.status = "WYKONANE"
            zamowienie.save(update_fields=["status"])

    def __str__(self):
        return f"Zadanie #{self.id} - {self.get_status_display()}"


class Platnosc(models.Model):
    STATUS_CHOICES = [
        ("NIEOPLACONA", "Nieopłacona"),
        ("OPLACONA", "Opłacona"),
        ("ANULOWANA", "Anulowana"),
    ]

    zamowienie = models.OneToOneField(Zamowienie, on_delete=models.CASCADE)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    rabat = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="NIEOPLACONA",
    )

    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Płatność {self.zamowienie} - {self.get_status_display()}"


class ProcesMagazynowy(models.Model):
    TYP_CHOICES = [
    ("PRZYJECIE", "Przyjęcie materiału"),
    ("WYDANIE", "Wydanie materiału"),

    ("REZERWACJA", "Rezerwacja materiału"),
    ("ZWOLNIENIE_REZERWACJI", "Zwolnienie rezerwacji"),

    ("INWENTARYZACJA", "Inwentaryzacja"),
    ("COFNIECIE", "Cofnięcie operacji"),
    ]

    magazyn = models.ForeignKey(Magazyn, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    rozmiar = models.ForeignKey(
        RozmiarBlachy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    pracownik = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="procesy_magazynowe",
    )

    typ = models.CharField(max_length=40,choices=TYP_CHOICES,)
    ilosc = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    opis = models.TextField(blank=True)

    cofnieta = models.BooleanField(default=False)
    powod_cofniecia = models.TextField(blank=True)

    cofnieta_przez = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cofniete_operacje_magazynowe",
    )

    data_cofniecia = models.DateTimeField(null=True, blank=True)

    operacja_powiazana = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="operacje_cofajace",
    )

    def __str__(self):
        return f"{self.get_typ_display()} - {self.material}"