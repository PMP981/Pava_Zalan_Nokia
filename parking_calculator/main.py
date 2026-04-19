from datetime import datetime
from pathlib import Path
import math

def parkolasi_dij_szamolo(erkezes: datetime, tavozas: datetime) -> int:
    if tavozas < erkezes:
        raise ValueError("A kilépesi idő nem lehet korábbi a belépési időnél...")

    kulonbseg = tavozas - erkezes
    osszes_perc = int(kulonbseg.total_seconds() / 60)

    if osszes_perc <= 30:
        return 0
    else:
        teljes_napok = osszes_perc // 1440
        maradek_perc = osszes_perc % 1440
        napi_dij = teljes_napok * 10000
        maradek_dij = toredek_nap(maradek_perc)

        return napi_dij + maradek_dij

def toredek_nap(percek: int) -> int:
    if percek <= 30:
        return 0

    fizetendo_percek = percek - 30
    elso_zona_perc = min(fizetendo_percek, 180)
    masodik_zona_perc = max(0, fizetendo_percek - 180)

    elso_zona_orak = math.ceil(elso_zona_perc / 60)
    masodik_zona_orak = math.ceil(masodik_zona_perc / 60) if masodik_zona_perc > 0 else 0

    elso_zona_dij = elso_zona_orak * 300
    masodik_zona_dij = masodik_zona_orak * 500

    return elso_zona_dij + masodik_zona_dij

def adat_beolvasas(fajlnev: str) -> list:
    adatok = []
    path = Path(fajlnev)

    with open(path, "r", encoding="utf-8") as f:
        for sor in f:
            sor = sor.strip()

            if not sor or sor.startswith("=") or sor.startswith("RENDSZAM"):
                continue

            reszek = sor.split()

            try:
                rendszam = reszek[0]
                erkezes_str = f"{reszek[1]} {reszek[2]}"
                tavozas_str = f"{reszek[3]} {reszek[4]}"

                erkezes = datetime.strptime(erkezes_str, "%Y-%m-%d %H:%M:%S")
                tavozas = datetime.strptime(tavozas_str, "%Y-%m-%d %H:%M:%S")

                adatok.append((rendszam, erkezes, tavozas))

            except:
                continue

    return adatok

def ido_kiiras(percek: int) -> str:
    napok = percek // (24*60)
    maradek = percek % (24*60)
    orak = maradek // 60
    percek_maradek = maradek % 60

    reszek = []
    if napok > 0:
        reszek.append(f"{napok} nap")
        
    if orak > 0:
        reszek.append(f"{orak} óra")
        
    if percek_maradek > 0:
        reszek.append(f"{percek_maradek} perc")

    return " ".join(reszek) if reszek else "0 perc"

def main():
    bemenet = "input.txt"
    kimenet = "output.txt"

    try:
        adatok = adat_beolvasas(bemenet)
    except:
        return

    eredmenyek = []
    for rendszam, erkezes, tavozas in adatok:
        try:
            dij = parkolasi_dij_szamolo(erkezes, tavozas)

            kulonbseg = tavozas - erkezes
            osszes_perc = int(kulonbseg.total_seconds() / 60)
            idotartam = ido_kiiras(osszes_perc)

            sor = (
                f"Rendszám: {rendszam:10s} | "
                f"Időtartam: {idotartam:20s} | "
                f"Díj: {dij:>8} Ft"
            )
            eredmenyek.append(sor)
            print(sor)

        except:
            continue

    with open(kimenet, "w", encoding="utf-8") as f:
        f.write("=== Parkolási Díjszámítás Eredménye ===\n\n")
        for sor in eredmenyek:
            f.write(sor + "\n")

if __name__ == "__main__":
    main()