import math
import random

def estimate(i):
    inside = 0

    for j in range(i):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        if(x**2 + y**2 <= 1):
            inside += 1

    return (inside/i) * 4

n = int(input("Podaj liczbe iteracji\n"))
k = int(input("Podaj krok\n"))

for i in range(k, n+1, k):
    pi_est = estimate(i)
    print(f"Przyblizenie pi po {i} iteracjach: {pi_est}")

pi_est = estimate(n)
diff = abs(math.pi - pi_est)

print(f"Roznica miedzy wartoscia estymowana po {n} iteracjach i wartoscia math.pi: {diff}")

