from django.db import models
from django.contrib.auth.models import User


# =====================
# KLIENCI
# =====================

class Klient(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    adres = models.CharField(max_length=255)

    nazwa_firmy = models.CharField(max_length=100, blank=True)
    nip = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


# =====================
# PRACOWNICY
# =====================

class PracownikProfil(models.Model):

    ROLE_CHOICES = [
        ("ADMIN", "Administrator"),
        ("MAGAZYN", "Magazynier"),
        ("PRODUKCJA", "Pracownik produkcji"),
        ("KSIEGOWOSC", "Księgowość"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    telefon = models.CharField(
        max_length=20,
        blank=True
    )

    rola = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# =====================
# MATERIAŁY
# =====================

class Material(models.Model):

    nazwa = models.CharField(max_length=100)

    producent = models.CharField(
        max_length=100,
        blank=True
    )

    grubosc_mm = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    cena_za_m2 = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.nazwa


# =====================
# ROZMIARY BLACH
# =====================

class RozmiarBlachy(models.Model):

    nazwa = models.CharField(max_length=100)

    szerokosc_mm = models.IntegerField()

    wysokosc_mm = models.IntegerField()

    standardowy = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.nazwa


# =====================
# TYPY USŁUG
# =====================

class TypUslugi(models.Model):

    nazwa = models.CharField(max_length=100)

    jednostka = models.CharField(
        max_length=20,
        default="szt."
    )

    def __str__(self):
        return self.nazwa


# =====================
# CENNIK
# =====================

class Cennik(models.Model):

    typ_uslugi = models.ForeignKey(
        TypUslugi,
        on_delete=models.CASCADE
    )

    cena = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data_od = models.DateField()

    def __str__(self):
        return f"{self.typ_uslugi} - {self.cena} PLN"


# =====================
# MAGAZYN
# =====================

class Magazyn(models.Model):

    nazwa = models.CharField(max_length=100)

    adres = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa


# =====================
# STAN MAGAZYNOWY
# =====================

class StanMagazynowy(models.Model):

    magazyn = models.ForeignKey(
        Magazyn,
        on_delete=models.CASCADE
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE
    )

    ilosc = models.IntegerField(default=0)

    class Meta:
        unique_together = ("magazyn", "material")

    def __str__(self):
        return f"{self.material} ({self.ilosc})"


# =====================
# ZAMÓWIENIA
# =====================

class Zamowienie(models.Model):

    STATUS_CHOICES = [
        ("PRZYJETE", "Przyjęte"),
        ("REALIZACJA", "W realizacji"),
        ("GOTOWE", "Gotowe do odbioru"),
        ("ZAKONCZONE", "Zakończone"),
        ("ANULOWANE", "Anulowane"),
    ]

    klient = models.ForeignKey(
        Klient,
        on_delete=models.CASCADE
    )

    data_utworzenia = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PRZYJETE"
    )

    uwagi = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Zamówienie #{self.id}"


# =====================
# POZYCJE ZAMÓWIENIA
# =====================

class PozycjaZamowienia(models.Model):

    STATUS_CHOICES = [
        ("PRZYJETA", "Przyjęta"),
        ("REALIZACJA", "W realizacji"),
        ("ZREALIZOWANA", "Zrealizowana"),
        ("ODRZUCONA", "Odrzucona"),
    ]

    zamowienie = models.ForeignKey(
        Zamowienie,
        on_delete=models.CASCADE,
        related_name="pozycje"
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE
    )

    rozmiar = models.ForeignKey(
        RozmiarBlachy,
        on_delete=models.CASCADE
    )

    typ_uslugi = models.ForeignKey(
        TypUslugi,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    przypisany_pracownik = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ilosc = models.PositiveIntegerField(default=1)

    cena = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PRZYJETA"
    )

    czy_powstal_odpad = models.BooleanField(
        default=False
    )

    opis_odpadu = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Pozycja #{self.id}"


# =====================
# PŁATNOŚCI
# =====================

class Platnosc(models.Model):

    STATUS_CHOICES = [
        ("NIEOPLACONA", "Nieopłacona"),
        ("OPLACONA", "Opłacona"),
        ("ANULOWANA", "Anulowana"),
    ]

    zamowienie = models.OneToOneField(
        Zamowienie,
        on_delete=models.CASCADE
    )

    kwota = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    rabat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="NIEOPLACONA"
    )

    data_utworzenia = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Płatność #{self.id}"


# =====================
# PROCESY MAGAZYNOWE
# =====================

class ProcesMagazynowy(models.Model):

    TYP_CHOICES = [
        ("PRZYJECIE", "Przyjęcie materiału"),
        ("WYDANIE", "Wydanie materiału"),
        ("INWENTARYZACJA", "Inwentaryzacja"),
    ]

    magazyn = models.ForeignKey(
        Magazyn,
        on_delete=models.CASCADE
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE
    )

    pracownik = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    typ = models.CharField(
        max_length=20,
        choices=TYP_CHOICES
    )

    ilosc = models.IntegerField()

    data = models.DateTimeField(
        auto_now_add=True
    )

    opis = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.typ} - {self.material}"