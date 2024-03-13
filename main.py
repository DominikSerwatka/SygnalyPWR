import numpy as np
import matplotlib.pyplot as plt

def load_signal_from_file(file_path):
    """
    Wczytuje sygnał z pliku tekstowego.
    Plik powinien zawierać wartości próbek sygnału EKG.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    signal = []
    for line in lines:
        signal.append([int(x) for x in line.split()])
    return np.array(signal)

def plot_signal(signal, time_scale=None, title=None, xlabel=None, ylabel=None):
    """
    Wizualizuje sygnał na wykresie.
    """
    plt.figure(figsize=(10, 6))
    if time_scale is not None:
        plt.plot(time_scale, signal)
    else:
        plt.plot(signal)
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def save_signal_to_file(signal, file_name):
    """
    Zapisuje sygnał do pliku o podanej nazwie.
    """
    np.savetxt(file_name, signal)

# Przykładowe użycie funkcji:
file_path = "ekg1.txt"
signal = load_signal_from_file(file_path)

# Możliwość dostosowania osi czasu
time_scale = np.arange(0, len(signal))  # Przykładowa skala czasu
plot_signal(signal, time_scale, title="EKG Signal", xlabel="Czas [s]", ylabel="Amplituda")

# Możliwość zapisu wycinka sygnału do pliku
fragment_signal = signal[100:200]  # Przykładowy wycinek sygnału
save_signal_to_file(fragment_signal, "fragment_sygnalu.txt")
