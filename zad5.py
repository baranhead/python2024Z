import math

class Ułamek:
    def __init__ (self, licznik, mianownik):
            
        #niezerowy mianownik
        assert mianownik != 0

        #znak w liczniku
        if mianownik < 0:
            licznik = -licznik
            mianownik = -mianownik

        #skrócony ułamek
        gcd = math.gcd(licznik, mianownik)
        self.mianownik = mianownik // gcd
        self.licznik = licznik // gcd

    #dodawanie
    def __add__(self, other):
        licznik = self.licznik * other.mianownik + self.mianownik * other.licznik
        mianownik = self.mianownik * other.mianownik
        
        return Ułamek(licznik, mianownik)

    #odejmowanie
    def __sub__(self, other):
        licznik = self.licznik * other.mianownik - self.mianownik * other.licznik
        mianownik = self.mianownik * other.mianownik
        return Ułamek(licznik, mianownik)

    #mnozenie
    def __mul__(self, other):
        licznik = self.licznik * other.licznik
        mianownik = self.mianownik * other.mianownik
        return Ułamek(licznik, mianownik)

    #dzielenie
    def __truediv__(self, other):
        assert other.licznik != 0, "Dzielenie przez zero!"
        licznik = self.licznik * other.mianownik
        mianownik = self.mianownik * other.licznik
        return Ułamek(licznik, mianownik)

    #rownosc
    def __eq__(self, other):
        return self.licznik == other.licznik and self.mianownik == other.mianownik
            
    #<
    def __lt__(self, other):
        return self.licznik * other.mianownik < self.mianownik * other.licznik

    #<=
    def __le__(self, other):
        return self.licznik * other.mianownik <= self.mianownik * other.licznik

    #zamiana na napis
    def __str__(self):
        return f"{self.licznik}/{self.mianownik}"

    #reprenzentacja
    def __repr__(self):
        return f"Ułamek({self.licznik}, {self.mianownik})"


if __name__ == "__main__":
    u1 = Ułamek(2, 6)
    u2 = Ułamek(6, 9)

    print(f"Ułamek 1: {u1}")
    print(f"Ułamek 2: {u2}")

    suma = u1 + u2
    print(f"Suma: {suma}")

    roznica = u1 - u2
    print(f"Różnica: {roznica}")

    iloczyn = u1 * u2
    print(f"Iloczyn: {iloczyn}")

    iloraz = u1 / u2
    print(f"Iloraz: {iloraz}")

    print(f"Czy ułamek 1 jest równy ułamkowi 2? {u1 == u2}")
    print(f"Czy ułamek 1 jest mniejszy niż ułamek 2? {u1 < u2}")
    print(f"Czy ułamek 1 jest mniejszy lub równy ułamek 2? {u1 <= u2}")

    try:
        u3 = Ułamek(1, 0)
    except AssertionError as e:
        print(e)

    u4 = Ułamek(0, 5)
    print(f"Ułamek 4: {u4}")