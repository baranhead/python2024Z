import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

# parametry
np.random.seed(int(time.time()))
num_samples = 1000
num_frames = 60
sample_size = 50


# tworzenie probki
def create_sample(sample_size, num_samples):
    return [np.mean(np.random.exponential(scale=1, size=sample_size)) for _ in range(num_samples)]

# dane do animacji
frame_sample_sizes = np.linspace(2, sample_size, num_frames, dtype=int)
data = [create_sample(size, num_samples) for size in frame_sample_sizes]

#aktualizacja wykresu
fig, ax = plt.subplots(figsize=(8, 6))
def anim(frame):
    ax.clear()
    ax.set_title("Centralne Twierdzenie Graniczne")
    ax.set_xlabel("Średnia próby")
    ax.set_ylabel("Gęstość")
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 4)
    histogram, bins, _ = ax.hist(data[frame], bins=50, density=True, color="pink")
    sample_size = frame_sample_sizes[frame]
    ax.text(0.05, 3.7, f"Rozmiar próby: {sample_size}")
    return histogram

# zapisanie gifa
anim = FuncAnimation(fig, anim, frames=num_frames, interval=100)
anim.save("central_limit_theorem.gif", writer="pillow")

plt.show()
