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

butto_1 = ttk.Button(root, text="Generate plot", command=make_plot)
butto_1.pack(pady=10)

button_2 = ttk.Button(root, text="Save segment to file", command=save_segment_to_file)
button_2.pack(pady=10)

root.mainloop()
