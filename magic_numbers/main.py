from pathlib import Path

def next_magic_num(n):
    s = str(n)
    hossz = len(s)

    if set(s) == {"9"}:
        return int("1" + "0" * (hossz - 1) + "1")

    fele = (hossz + 1) // 2
    bal = s[:fele]

    if hossz % 2 == 0:
        palindrom_szam = bal + bal[::-1]
    else:
        palindrom_szam = bal + bal[:-1][::-1]

    if int(palindrom_szam) > n:
        return int(palindrom_szam)

    bal = str(int(bal) + 1)

    if len(bal) > fele:
        return int("1" + "0" * (hossz - 1) + "1")

    if hossz % 2 == 0:
        palindrom_szam = bal + bal[::-1]
    else:
        palindrom_szam = bal + bal[:-1][::-1]

    return int(palindrom_szam)


def main():
    data = Path("input.txt").read_text(encoding="utf-8").splitlines()
    for sor in data:
        sor = sor.strip()
        
        if not sor:
            continue

        if '^' in sor:
            alap, hatvany = map(int, sor.split("^"))
            szam = alap ** hatvany
            
        else:
            szam = int(sor)

        print(next_magic_num(szam))


if __name__ == "__main__":
    main()