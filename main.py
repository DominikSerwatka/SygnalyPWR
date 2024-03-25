import numpy as np
import matplotlib.pyplot as plt


def load_signal(filename):
    """
    Funkcja wczytująca sygnał z pliku tekstowego.
    """
    data = np.loadtxt(filename)
    return data


def plot_signal(data, fs, save_filename=None):
    """
    Funkcja wizualizująca sygnał.
    """
    time = np.arange(len(data)) / fs
    print(data.shape[1])

    plt.figure(figsize=(10, 6))
    for i in range(data.shape[1]):
        plt.plot(time, data[:, i], label=f'Odprowadzenie {i + 1}')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.title('Sygnały EKG z różnych odprowadzeń')
    plt.grid(True)
    plt.legend()

    if save_filename:
        plt.savefig(save_filename)

    plt.show()


# Wczytanie sygnału
filename = "ekg1.txt"
data = load_signal(filename)

# Częstotliwość próbkowania
fs = 1000

# Wizualizacja sygnału
plot_signal(data, fs, save_filename="sygnaly_EKG.png")
