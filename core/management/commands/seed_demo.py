from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import (
    Cennik,
    Klient,
    Magazyn,
    Material,
    PracownikProfil,
    RozmiarBlachy,
    StanMagazynowy,
    TypUslugi,
)


class Command(BaseCommand):
    help = "Tworzy dane demonstracyjne"

    def handle(self, *args, **kwargs):

        self.stdout.write("Tworzenie danych demo...")

        # ==========================
        # UŻYTKOWNICY
        # ==========================

        admin_user, _ = User.objects.get_or_create(
            username="admin_demo",
            defaults={
                "first_name": "Adam",
                "last_name": "Administrator",
                "email": "admin@firma.pl",
                "is_staff": True,
            },
        )

        admin_user.set_password("admin123")
        admin_user.save()

        PracownikProfil.objects.get_or_create(
            user=admin_user,
            defaults={
                "rola": "ADMIN",
                "telefon": "500100100",
            },
        )

        magazynier_user, _ = User.objects.get_or_create(
            username="magazynier",
            defaults={
                "first_name": "Marek",
                "last_name": "Magazynier",
                "email": "magazyn@firma.pl",
            },
        )

        magazynier_user.set_password("test123")
        magazynier_user.save()

        PracownikProfil.objects.get_or_create(
            user=magazynier_user,
            defaults={
                "rola": "MAGAZYN",
                "telefon": "500200200",
            },
        )

        produkcja_user, _ = User.objects.get_or_create(
            username="spawacz",
            defaults={
                "first_name": "Piotr",
                "last_name": "Produkcja",
                "email": "produkcja@firma.pl",
            },
        )

        produkcja_user.set_password("test123")
        produkcja_user.save()

        PracownikProfil.objects.get_or_create(
            user=produkcja_user,
            defaults={
                "rola": "PRODUKCJA",
                "telefon": "500300300",
            },
        )

        ksiegowosc_user, _ = User.objects.get_or_create(
            username="ksiegowosc",
            defaults={
                "first_name": "Katarzyna",
                "last_name": "Księgowa",
                "email": "ksiegowosc@firma.pl",
            },
        )

        ksiegowosc_user.set_password("test123")
        ksiegowosc_user.save()

        PracownikProfil.objects.get_or_create(
            user=ksiegowosc_user,
            defaults={
                "rola": "KSIEGOWOSC",
                "telefon": "500400400",
            },
        )

        # ==========================
        # KLIENCI
        # ==========================

        Klient.objects.get_or_create(
            email="jan@test.pl",
            defaults={
                "imie": "Jan",
                "nazwisko": "Kowalski",
                "telefon": "600111111",
                "adres": "Warszawa, ul. Kwiatowa 1",
            },
        )

        Klient.objects.get_or_create(
            email="anna@test.pl",
            defaults={
                "imie": "Anna",
                "nazwisko": "Nowak",
                "telefon": "600222222",
                "adres": "Radom, ul. Słoneczna 15",
            },
        )

        Klient.objects.get_or_create(
            email="firma@test.pl",
            defaults={
                "imie": "Tomasz",
                "nazwisko": "Wiśniewski",
                "telefon": "600333333",
                "adres": "Lublin, ul. Przemysłowa 7",
                "nazwa_firmy": "Metal-Tech",
                "nip": "1234567890",
            },
        )

        # ==========================
        # MATERIAŁY
        # ==========================

        materialy = [
            ("Blacha ocynkowana", 0.5, 40),
            ("Blacha ocynkowana", 1.0, 60),
            ("Blacha aluminiowa", 1.0, 85),
            ("Blacha nierdzewna", 1.5, 120),
            ("Blacha miedziana", 1.0, 200),
        ]

        for nazwa, grubosc, cena in materialy:
            Material.objects.get_or_create(
                nazwa=nazwa,
                grubosc_mm=grubosc,
                defaults={
                    "producent": "Demo Producent",
                    "cena_za_m2": cena,
                },
            )

        # ==========================
        # ROZMIARY
        # ==========================

        rozmiary = [
            ("1000x2000", 1000, 2000, True),
            ("1250x2500", 1250, 2500, True),
            ("1500x3000", 1500, 3000, True),
            ("Niestandardowy", 0, 0, False),
        ]

        for nazwa, szer, wys, standard in rozmiary:
            RozmiarBlachy.objects.get_or_create(
                nazwa=nazwa,
                defaults={
                    "szerokosc_mm": szer,
                    "wysokosc_mm": wys,
                    "standardowy": standard,
                },
            )

        # ==========================
        # TYPY USŁUG
        # ==========================

        uslugi = [
            "Cięcie",
            "Gięcie",
            "Spawanie",
            "Formowanie",
        ]

        for usluga in uslugi:
            typ, _ = TypUslugi.objects.get_or_create(
                nazwa=usluga,
                defaults={"jednostka": "szt."},
            )

            Cennik.objects.get_or_create(
                typ_uslugi=typ,
                data_od=date.today(),
                defaults={
                    "cena": 50,
                },
            )

        # ==========================
        # MAGAZYN
        # ==========================

        magazyn, _ = Magazyn.objects.get_or_create(
            nazwa="Magazyn Główny",
            defaults={
                "adres": "Warszawa, ul. Hutnicza 1",
            },
        )

        for material in Material.objects.all():
            StanMagazynowy.objects.get_or_create(
                magazyn=magazyn,
                material=material,
                defaults={
                    "ilosc": 100,
                },
            )

        self.stdout.write(self.style.SUCCESS("Dane demo zostały utworzone."))
