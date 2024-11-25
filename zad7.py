import numpy as np

def Mw(wa, wb, xa, xb):
    wa = wa.reshape(wa.shape[0], wa.shape[1], 1)
    wb = wb.reshape(wb.shape[0], wb.shape[1], 1)
    return 1 / (1 + np.exp(-(wa * xa + wb * xb)))

n = 5
wa, wb = np.meshgrid(np.arange(0, 1.1, 0.1), np.arange(2, 3.1, 0.1))

xa = np.array([1.0, 2.2, 2.0, 1.5, 3.2])
xb = np.array([1.3, 1.1, 2.4, 3.2, 1.2])

pr = np.array([0, 1, 1, 0, 1])

Mw_values = Mw(wa, wb, xa, xb)
errors = (pr - Mw_values) ** 2
MSEw = np.sum(errors, axis=2) / n

print(MSEw)
