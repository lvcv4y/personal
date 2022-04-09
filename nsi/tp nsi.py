"""
Random exercises we had to do.
"""

# exo 1
somme3 = lambda x, y, z: x+y+z
"""
def somme3(x: int, y: int, z: int) -> int:
    return x+y+z
"""


#exo 2
def conversionTemps(sec: int) -> str:
    heure = sec // 3600
    sec -= (3600 * heure)

    min = sec // 60
    sec -= (60 * min)
    h_s = "heures " if heure > 1 else "heure "
    min_s = "minutes " if min > 1 else "minute "
    sec_s = "secondes" if sec > 1 else "seconde"

    res = ""
    if heure > 0:
        res += str(heure) + " " + h_s

    if min > 0:
        res += str(min) + " " + min_s

    if sec > 0:
        res += str(sec) + " " + sec_s

    return res


#exo 4
def get_v(height: int, width: int, depth: int) -> int:
    return height*width*depth
# get_v = lambda x,y,z: x*y*z


#exo 5
def is_num(n) -> bool:
    assert isinstance(n, int)
    return not (n // 10)
# is_num = lambda n : not n // 10


#exo 6
def appartient(char: str, texte: str) -> bool:
    return char in texte

# appartient = lambda c, t: c in t


# exo 3 part 2
def somme_carre(n: int) -> int:
    s = 0
    for i in range(1, n+1):
        s += i**2

    return s


# exo 1 part 3
def is_product_negative(a: int, b: int) -> bool:
    return bool(a < 0) ^ bool(b < 0)

# is_product_negative = lambda a, b: bool(a < 0) ^ bool(b < 0)


# exo 2 part 3
def remise():
    achats = []
    while True:
        a = input("prix du produit numéro {}".format(len(achats) + 1))

        if len(a) <= 0:
            break

        try:
            achats.append(float(a))
        except Exception:
            if a.lower() in ["stop", "arret", "fini", "finish"]:
                break

            print("vous avez rentré une mauvaise valeur !")

    total = 0
    for i in achats:
        total += i

    if total < 50:
        print("3% de remise")
    elif 50 <= total <= 100:
        print("5% de remise")
    else:
        print("7% de remise")


# exo 4, 5 part 3
def affiche(n: int = 10, txt: str = "Hello World"):
    print("".join(txt + "\n" for _ in range(n))[:-1])

    """
    for _ in range(n):
        print(txt)
    """


# exo 6 part 3
def vitesse(d_km: int, t_h: int) -> int:
    return round((d_km*1000) / (t_h * 3600), 5)


# exo 7 part 3
def maximum(*args: int):
    a = args[0]
    for i in args:
        if i > a:
            a = i

    return a
