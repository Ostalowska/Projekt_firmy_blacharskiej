from decimal import Decimal

from django.test import TestCase

from core.forms import (
    KlientForm,
    MaterialForm,
    PozycjaZamowieniaForm,
    RozmiarBlachyForm,
)
from core.models import Magazyn, Material, RozmiarBlachy, StanMagazynowy


class KlientFormTests(TestCase):
    def test_klient_form_odrzuca_cyfry_w_imieniu(self):
        form = KlientForm(
            data={
                "imie": "Anna1",
                "nazwisko": "Kowalska",
                "telefon": "123456789",
                "email": "anna@example.com",
                "adres": "Testowa 1",
                "nazwa_firmy": "",
                "nip": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("imie", form.errors)

    def test_klient_form_odrzuca_nieprawidlowy_telefon(self):
        form = KlientForm(
            data={
                "imie": "Anna",
                "nazwisko": "Kowalska",
                "telefon": "123ABC789",
                "email": "anna@example.com",
                "adres": "Testowa 1",
                "nazwa_firmy": "",
                "nip": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("telefon", form.errors)


class MaterialFormTests(TestCase):
    def test_material_form_odrzuca_ujemna_cene(self):
        form = MaterialForm(
            data={
                "nazwa": "Blacha stalowa",
                "grubosc_mm": Decimal("2.00"),
                "producent": "Test",
                "cena_za_m2": Decimal("-1.00"),
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("cena_za_m2", form.errors)

    def test_material_form_odrzuca_zerowa_grubosc(self):
        form = MaterialForm(
            data={
                "nazwa": "Blacha stalowa",
                "grubosc_mm": Decimal("0.00"),
                "producent": "Test",
                "cena_za_m2": Decimal("100.00"),
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("grubosc_mm", form.errors)


class RozmiarBlachyFormTests(TestCase):
    def test_rozmiar_form_odrzuca_zerowa_szerokosc(self):
        form = RozmiarBlachyForm(
            data={
                "szerokosc_mm": 0,
                "wysokosc_mm": 1000,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("szerokosc_mm", form.errors)


class PozycjaZamowieniaFormTests(TestCase):
    def setUp(self):
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
            ilosc=5,
            zarezerwowano=1,
        )

    def test_form_odrzuca_ilosc_wieksza_niz_dostepna(self):
        form = PozycjaZamowieniaForm(
            data={
                "stan_magazynowy": self.stan.id,
                "czy_niestandardowy": "",
                "szerokosc_niestandardowa_mm": "",
                "wysokosc_niestandardowa_mm": "",
                "uslugi": [],
                "ilosc": 10,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_form_odrzuca_niestandardowy_rozmiar_wiekszy_niz_arkusz(self):
        form = PozycjaZamowieniaForm(
            data={
                "stan_magazynowy": self.stan.id,
                "czy_niestandardowy": "on",
                "szerokosc_niestandardowa_mm": 1500,
                "wysokosc_niestandardowa_mm": 2500,
                "uslugi": [],
                "ilosc": 1,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)