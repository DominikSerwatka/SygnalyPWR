import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk


def load_signal(filename):
    """
    Funkcja wczytująca sygnał z pliku tekstowego.
    """
    data = np.loadtxt(filename)
    return data


def plot_signal(data, fs, filename, start_time, end_time):
    """
    Funkcja wizualizująca sygnał.
    """

    time = np.arange(len(data)) / fs

    if start_time is not None and end_time is not None:
        start_index = int(start_time * fs)
        end_index = int(end_time * fs)
        data = data[start_index:end_index]
        time = time[start_index:end_index]

    plt.figure(figsize=(10, 6))
    if filename == "ekg100.txt":
        plt.plot(time, data, label='Sygnał')
        plt.title('ekg100.txt')
    elif filename == "ekg_noise.txt":
        plt.plot(data[:, 0], data[:, 1])
        plt.title('ekg_noise.txt')
    else:
        for i in range(data.shape[1]):
            plt.plot(time, data[:, i], label=f'Odprowadzenie {i + 1}')
        plt.title('ekg1.txt')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    plt.legend(loc='upper right')

    plt.show()


def make_plot():
    filename = file_combobox_1.get()
    data = load_signal(filename)
    if filename == "ekg1.txt":
        fs = 1000
    else:
        fs = 360

    start_time = float(entry_start.get()) if entry_start.get() else None
    end_time = float(entry_end.get()) if entry_end.get() else None

    plot_signal(data, fs, filename, start_time, end_time)
    plt.show()


def save_segment(new_filename, filename, data, start_time, end_time, fs):
    start_index = int(start_time * fs)
    end_index = int(end_time * fs)
    if filename == "ekg100.txt":
        selected_data = data[start_index:end_index]
        with open(new_filename + ".txt", 'w') as file:
            # np.savetxt(file, selected_data, fmt='%d')
            np.savetxt(file, selected_data)
    elif filename == "ekg_noise.txt":
        selected_data = data[start_index:end_index, :]
        # Utwórz plik o nazwie filename i zapisz w nim wycinek sygnału
        with open(new_filename + ".txt", 'w') as file:
            np.savetxt(file, selected_data)
    else:
        selected_data = data[start_index:end_index, :]
        # Utwórz plik o nazwie filename i zapisz w nim wycinek sygnału
        with open(new_filename + ".txt", 'w') as file:
            np.savetxt(file, selected_data, fmt='%d')



def save_segment_to_file():
    filename = file_combobox_1.get()
    new_filename = entry_filename.get()
    if filename:
        if filename == "ekg1.txt":
            fs = 1000
        else:
            fs = 360
        data = load_signal(filename)
        print(data)
        save_segment(new_filename, filename, data, float(entry_start.get()), float(entry_end.get()), fs)

def gen_sinus():
    # Parametry sygnału
    fs = 2000  # Częstotliwość próbkowania (Hz)
    f = 50  # Częstotliwość fali sinusoidalnej (Hz)
    N = 65536  # Długość sygnału

    freq = entry_freq.get()
    if freq != '':
        freq = int(freq)
        fs = freq

    # Generowanie ciągu próbek
    t = np.arange(N) / fs  # Wektor czasu
    x = np.sin(2 * np.pi * f * t)  # Sygnał sinusoidalny

    # Ograniczenie liczby próbek do wyświetlenia dla lepszej wizualizacji
    samples_to_display = 500  # Liczba próbek do wyświetlenia

    # Wykres sygnału sinusoidalnego
    plt.figure(figsize=(10, 6))
    plt.plot(t[:samples_to_display], x[:samples_to_display])
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.title(f'Sygnał sinusoidalny ({f} Hz)')
    plt.grid(True)
    plt.show()

    # Dyskretna transformata Fouriera (DFT)
    X = np.fft.fft(x)
    X_magnitude = np.abs(X) / N  # Normalizacja amplitud

    # Wygenerowanie wektora częstotliwości
    freqs = np.fft.fftfreq(N, 1 / fs)

    # Wybór połowy zakresu (od 0 do fs/2)
    half_N = N // 2
    freqs_half = freqs[:half_N]
    X_magnitude_half = X_magnitude[:half_N]

    # Wykres widma amplitudowego
    plt.figure(figsize=(10, 6))
    plt.plot(freqs_half, X_magnitude_half)
    plt.title('Widmo amplitudowe sygnału')
    plt.xlabel('Częstotliwość (Hz)')
    plt.ylabel('Amplituda')
    plt.grid(True)
    plt.xlim(0, fs / 2)
    plt.show()

def gen_sinus_x_2():
    # Parametry sygnału
    fs = 2000  # Częstotliwość próbkowania (Hz)
    f1 = 50  # Częstotliwość pierwszej fali sinusoidalnej (Hz)
    f2 = 60  # Częstotliwość drugiej fali sinusoidalnej (Hz)
    N = 65536  # Długość sygnału
    freq = entry_freq.get()
    if freq != '':
        freq = int(freq)
        fs = freq

    # Generowanie ciągu próbek dla mieszanki dwóch fal sinusoidalnych
    t = np.arange(N) / fs  # Wektor czasu
    x_mixed = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)  # Mieszanka fal

    # Dyskretna transformata Fouriera (DFT) dla sygnału mieszanki
    X_mixed = np.fft.fft(x_mixed)
    X_mixed_magnitude = np.abs(X_mixed) / N  # Normalizacja amplitud

    # Wygenerowanie wektora częstotliwości
    freqs = np.fft.fftfreq(N, 1 / fs)

    # Wybór połowy zakresu (od 0 do fs/2)
    half_N = N // 2
    freqs_half = freqs[:half_N]
    X_mixed_magnitude_half = X_mixed_magnitude[:half_N]

    # Wykres widma amplitudowego dla sygnału mieszanki
    plt.figure(figsize=(10, 6))
    plt.plot(freqs_half, X_mixed_magnitude_half)
    plt.title('Widmo amplitudowe mieszanki dwóch fal sinusoidalnych')
    plt.xlabel('Częstotliwość (Hz)')
    plt.ylabel('Amplituda')
    plt.grid(True)
    plt.xlim(0, fs / 2)
    plt.show()

def gen_sinus_restore():
    # Parametry sygnału
    fs = 2000  # Częstotliwość próbkowania (Hz)
    f = 50  # Częstotliwość fali sinusoidalnej (Hz)
    N = 65536  # Długość sygnału

    freq = entry_freq.get()
    if freq != '':
        freq = int(freq)
        fs = freq

    # Generowanie ciągu próbek
    t = np.arange(N) / fs  # Wektor czasu
    x = np.sin(2 * np.pi * f * t)  # Sygnał sinusoidalny

    # Dyskretna transformata Fouriera (DFT)
    X = np.fft.fft(x)
    X_magnitude = np.abs(X) / N  # Normalizacja amplitud

    # Wygenerowanie wektora częstotliwości
    freqs = np.fft.fftfreq(N, 1 / fs)

    x_restored = np.fft.ifft(X).real

    # Ograniczenie liczby próbek do wyświetlenia dla lepszej wizualizacji
    samples_to_display = 100  # Liczba próbek do wyświetlenia

    # Wyświetlenie sygnału oryginalnego i odzyskanego
    plt.figure(figsize=(10, 6))
    plt.plot(t[:samples_to_display], x[:samples_to_display], label='Oryginalny sygnał', alpha=0.7)
    plt.plot(t[:samples_to_display], x_restored[:samples_to_display], '--', label='Sygnał odzyskany', alpha=0.7)
    plt.title('Porównanie oryginalnego sygnału z odzyskanym')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.legend()
    plt.grid(True)
    plt.show()







root = tk.Tk()
root.title("Cyfrowe przedtwarzanie sygnałów i obrazów")

file_list = ["ekg1.txt", "ekg100.txt", "ekg_noise.txt"]
label_1 = ttk.Label(root, text="Select file")
label_1.pack(pady=10)
file_combobox_1 = ttk.Combobox(root, values=file_list, state="readonly", width=30)
file_combobox_1.pack(pady=10)
file_combobox_1.set("Select file")

label_2 = ttk.Label(root, text="Starting time [s]")
label_2.pack(pady=5)
entry_start = ttk.Entry(root)
entry_start.pack()

label_3 = ttk.Label(root, text="Ending time [s]")
label_3.pack(pady=5)
entry_end = ttk.Entry(root)
entry_end.pack()

label_4 = ttk.Label(root, text="Enter filename to save")
label_4.pack(pady=5)
entry_filename = ttk.Entry(root)
entry_filename.pack()

label_5 = ttk.Label(root, text="Enter sampling frequency")
label_5.pack(pady=5)
entry_freq = ttk.Entry(root)
entry_freq.pack()

butto_1 = ttk.Button(root, text="Generate plot", command=make_plot)
butto_1.pack(pady=10)

button_2 = ttk.Button(root, text="Save segment to file", command=save_segment_to_file)
button_2.pack(pady=10)

button_3 = ttk.Button(root, text="Sinus generate", command=gen_sinus)
button_3.pack(pady=10)

butto_4 = ttk.Button(root, text="Mix of two sinus generate", command=gen_sinus_x_2)
butto_4.pack(pady=10)

butto_5 = ttk.Button(root, text="Restore signal", command=gen_sinus_restore)
butto_5.pack(pady=10)

root.mainloop()
