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
        signal.append([float(x) for x in line.split()])
    return np.array(signal)
#kacper rakowski
# Dominik 


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
file_path2 = "ekg100.txt"
signal = load_signal_from_file(file_path2)

# Możliwość dostosowania osi czasu
time_scale = np.arange(0, len(signal))  # Przykładowa skala czasu
plot_signal(signal, time_scale, title="EKG Signal 1", xlabel="Czas [s]", ylabel="Amplituda")

# Możliwość zapisu wycinka sygnału do pliku
fragment_signal = signal[100:200]  # Przykładowy wycinek sygnału
plot_signal(fragment_signal, np.arange(100, 200), title="EKG Signal 2", xlabel="Czas [s]", ylabel="Amplituda")

