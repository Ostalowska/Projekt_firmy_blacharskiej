from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from core.models import (
    Cennik,
    Klient,
    Magazyn,
    Material,
    PozycjaZamowienia,
    RozmiarBlachy,
    StanMagazynowy,
    TypUslugi,
    Zadanie,
    Zamowienie,
)


class ZamowienieModelTests(TestCase):
    def setUp(self):
        self.klient = Klient.objects.create(
            imie="Anna",
            nazwisko="Kowalska",
            telefon="123456789",
            email="anna@example.com",
            adres="Testowa 1",
        )

    def test_zamowienie_generuje_numer_po_zapisie(self):
        zamowienie = Zamowienie.objects.create(klient=self.klient)

        self.assertIsNotNone(zamowienie.numer)
        self.assertTrue(zamowienie.numer.startswith("ZAM-"))

    def test_rabat_kwotowy_nie_obniza_kwoty_ponizej_zera(self):
        zamowienie = Zamowienie.objects.create(
            klient=self.klient,
            rabat_typ="KWOTA",
            rabat_wartosc=Decimal("999.00"),
        )

        wynik = zamowienie.przelicz_kwote()

        self.assertEqual(wynik, Decimal("0.00"))


class PozycjaZamowieniaModelTests(TestCase):
    def setUp(self):
        self.klient = Klient.objects.create(
            imie="Anna",
            nazwisko="Kowalska",
            telefon="123456789",
            email="anna2@example.com",
            adres="Testowa 1",
        )
        self.zamowienie = Zamowienie.objects.create(klient=self.klient)
        self.magazyn = Magazyn.objects.create(
            nazwa="Magazyn główny",
            adres="Testowa 1",
        )
        self.material = Material.objects.create(
            nazwa="Blacha stalowa",
            producent="Test",
            grubosc_mm=Decimal("2.00"),
            cena_za_m2=Decimal("100.00"),
        )
        self.rozmiar = RozmiarBlachy.objects.create(
            szerokosc_mm=1000,
            wysokosc_mm=2000,
        )
        self.stan = StanMagazynowy.objects.create(
            magazyn=self.magazyn,
            material=self.material,
            rozmiar=self.rozmiar,
            ilosc=10,
            zarezerwowano=0,
        )

    def test_powierzchnia_standardowa_liczona_z_rozmiaru_stanu(self):
        pozycja = PozycjaZamowienia.objects.create(
            zamowienie=self.zamowienie,
            stan_magazynowy=self.stan,
            ilosc=1,
        )

        self.assertEqual(pozycja.powierzchnia_m2(), Decimal("2"))

    def test_przelicz_cene_materialu_bez_uslug(self):
        pozycja = PozycjaZamowienia.objects.create(
            zamowienie=self.zamowienie,
            stan_magazynowy=self.stan,
            ilosc=2,
        )

        pozycja.przelicz_i_zapisz()

        self.assertEqual(pozycja.cena_jednostkowa, Decimal("200.00"))
        self.assertEqual(pozycja.wartosc, Decimal("400.00"))

    def test_przelicz_cene_z_usluga(self):
        usluga = TypUslugi.objects.create(nazwa="Cięcie")
        Cennik.objects.create(
            typ_uslugi=usluga,
            cena=Decimal("50.00"),
            data_od=timezone.now().date(),
        )

        pozycja = PozycjaZamowienia.objects.create(
            zamowienie=self.zamowienie,
            stan_magazynowy=self.stan,
            ilosc=1,
        )
        pozycja.uslugi.add(usluga)
        pozycja.przelicz_i_zapisz()

        self.assertEqual(pozycja.cena_jednostkowa, Decimal("250.00"))
        self.assertEqual(pozycja.wartosc, Decimal("250.00"))


class StanMagazynowyModelTests(TestCase):
    def test_dostepne_to_ilosc_minus_zarezerwowano(self):
        magazyn = Magazyn.objects.create(nazwa="Magazyn", adres="Adres")
        material = Material.objects.create(
            nazwa="Blacha",
            producent="Test",
            grubosc_mm=Decimal("1.00"),
            cena_za_m2=Decimal("100.00"),
        )
        rozmiar = RozmiarBlachy.objects.create(
            szerokosc_mm=1000,
            wysokosc_mm=1000,
        )
        stan = StanMagazynowy.objects.create(
            magazyn=magazyn,
            material=material,
            rozmiar=rozmiar,
            ilosc=10,
            zarezerwowano=3,
        )

        self.assertEqual(stan.dostepne, 7)


class ZadanieModelTests(TestCase):
    def test_zamowienie_przechodzi_na_wykonane_gdy_zadania_zakonczone(self):
        klient = Klient.objects.create(
            imie="Jan",
            nazwisko="Nowak",
            telefon="123456789",
            email="jan@example.com",
            adres="Testowa 1",
        )
        zamowienie = Zamowienie.objects.create(
            klient=klient,
            status="ZATWIERDZONE",
        )
        magazyn = Magazyn.objects.create(nazwa="Magazyn", adres="Adres")
        material = Material.objects.create(
            nazwa="Blacha",
            producent="Test",
            grubosc_mm=Decimal("1.00"),
            cena_za_m2=Decimal("100.00"),
        )
        rozmiar = RozmiarBlachy.objects.create(
            szerokosc_mm=1000,
            wysokosc_mm=1000,
        )
        stan = StanMagazynowy.objects.create(
            magazyn=magazyn,
            material=material,
            rozmiar=rozmiar,
            ilosc=10,
            zarezerwowano=0,
        )
        pozycja = PozycjaZamowienia.objects.create(
            zamowienie=zamowienie,
            stan_magazynowy=stan,
            ilosc=1,
        )
        user = User.objects.create_user(username="pracownik", password="test123")

        zadanie = Zadanie.objects.create(
            pozycja=pozycja,
            przypisany_pracownik=user,
            rola_docelowa="PRODUKCJA",
            status="NOWE",
        )

        zadanie.status = "ZREALIZOWANE"
        zadanie.save()

        zamowienie.refresh_from_db()
        self.assertEqual(zamowienie.status, "WYKONANE")