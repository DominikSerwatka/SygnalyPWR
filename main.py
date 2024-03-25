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


def plot_signal(data, fs, filename):
    """
    Funkcja wizualizująca sygnał.
    """

    time = np.arange(len(data)) / fs

    plt.figure(figsize=(10, 6))
    if filename == "ekg100.txt":
        plt.plot(time, data, label='Sygnał')
    elif filename=="ekg_noise.txt":
        plt.plot(data[:,0], data[:,1])
    else:
        for i in range(data.shape[1]):
            plt.plot(time, data[:, i], label=f'Odprowadzenie {i + 1}')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.title('Sygnały EKG z różnych odprowadzeń')
    plt.grid(True)
    plt.legend(loc='upper right')


    plt.show()


def make_plot():
    filename=file_combobox_1.get()
    data = load_signal(filename)
    if filename=="ekg1.txt":
        fs=1000
    else:
        fs=360

    plot_signal(data, fs, filename)


root = tk.Tk()
root.title("Cyfrowe przedtwarzanie sygnałów i obrazów")

file_list = ["ekg1.txt", "ekg100.txt", "ekg_noise.txt"]
label_1 = ttk.Label(root, text="Select file")
label_1.pack(pady=10)
file_combobox_1 = ttk.Combobox(root, values=file_list, state="readonly", width=30)
file_combobox_1.pack(pady=10)
file_combobox_1.set("Select file")

butto_1 = ttk.Button(root, text="Generate plot", command=make_plot)
butto_1.pack(pady=10)

root.mainloop()

