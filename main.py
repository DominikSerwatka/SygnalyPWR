import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from scipy.signal import butter, filtfilt


def load_signal(filename):
    """
    Function that load signal from file.
    """
    try:
        data = np.loadtxt(filename)
    except FileNotFoundError:
        print("File not found.")
        return None
    return data


def make_plot(task_3=False):
    """
    Function that manage exception handling.
    """
    filename = combobox_filename.get()
    data = load_signal(filename)
    if type(data) is not np.ndarray:
        messagebox.showwarning(title="Exception", message="File not found.")
    else:
        plot_signal(data, filename, task_3)


def plot_signal(data, filename, task_3=False):
    """
    Function that draw plot.
    """

    plt.figure(figsize=(10, 6))
    if filename == "ekg1.txt":
        fs = 1000
        time = np.arange(len(data)) / fs
        for i in range(data.shape[1]):
            plt.plot(time, data[:, i], label=f"signal {i + 1}")
        plt.title("Signal ekg1.txt")
    else:
        fs = 360
        if filename == "ekg100.txt":
            time = np.arange(len(data)) / fs
            plt.plot(time, data, label="signal")
            plt.title("Signal ekg100.txt")
        if filename == "ekg_noise.txt":
            plt.plot(data[:, 0], data[:, 1], label="signal")
            plt.title("Signal ekg_noise.txt")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()
    if task_3:
        n = len(data)
        x = np.fft.fft(data)
        P2 = np.abs(x)
        P1 = P2[:n // 2+1] / n
        P1[1:-1] = 2 * P1[1:-1]
        f = np.linspace(0, fs / 2, len(P1))
        plt.figure(figsize=(10, 6))
        plt.plot(f, P1)
        plt.title(f"Amplitude spectrum of the signal [{filename}]")
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.xlim(0, fs / 2)
        plt.show()

        data_restored = np.fft.ifft(x).real

        diff = data - data_restored

        plt.figure(figsize=(15, 9))

        plt.subplot(3, 1, 1)
        plt.plot(time, data, label=f'Original signal [{filename}]')
        plt.title('Original signal EKG')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(time, data_restored, label=f'Inverse signal EKG [{filename}]', linestyle='--')
        plt.title('Inverse signal EKG z IDFT')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(time, diff, label='Signal Difference', color='red')
        plt.title(f'Difference between original and inverse EKG signal [{filename}]')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.legend()

        plt.tight_layout()
        plt.show()





def sinus_plot(*arg, ttf=False, inverse=False):
    """
    Function that generate sinus plot.
    """
    entry_hz = entry_sinus.get()
    if entry_hz != "50":
        entry_hz = entry_hz.split(', ')
        entry = [int(hz) for hz in entry_hz]
        arg = entry

    entry_fre = enter_freq.get()
    if entry_fre != "2000":
        fs = int(entry_fre)
    else:
        fs = 2000

    N = 65536
    if len(arg) == 0:
        f = 50
        arg = [50]
    else:
        f = arg[0]

    time = np.arange(N) / fs
    x = np.sin(2 * np.pi * f * time)

    for f in arg[1:]:
        x = x + np.sin(2 * np.pi * f * time)

    samples_to_display = 500

    plt.figure(figsize=(10, 6))
    plt.plot(time[:samples_to_display], x[:samples_to_display])
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title(f"Sinus signal {arg} Hz")
    plt.grid(True)
    plt.show()

    if ttf:
        x_fft = np.fft.fft(x)
        x_magnitude = np.abs(x_fft) / N

        freqs = np.fft.fftfreq(N, 1 / fs)

        half_N = N // 2
        freqs_half = freqs[:half_N]
        x_magnitude_half = x_magnitude[:half_N]
        plt.figure(figsize=(10, 6))
        plt.plot(freqs_half, x_magnitude_half)
        plt.title('Amplitude spectrum of signal')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.xlim(0, fs / 2)
        plt.show()
        if inverse:
            data_restored = np.fft.ifft(x_fft)
            plt.figure(figsize=(10, 6))
            plt.plot(time[:samples_to_display], x[:samples_to_display], label='Original signal', alpha=0.7)
            plt.plot(time[:samples_to_display], data_restored[:samples_to_display], '--', label='Inverse signal', alpha=0.7)
            plt.title('Original signal and inverse signal')
            plt.xlabel('Time [s]')
            plt.ylabel('Amplitude')
            plt.legend()
            plt.grid(True)
            plt.show()


def filter(filename="ekg_noise.txt"):
    data = load_signal("ekg_noise.txt")
    fs = 360
    time = data[:, 0]
    amplitude = data[:, 1]
    plt.figure(figsize=(10, 6))
    plt.plot(time, amplitude, label="signal")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()


    N = len(time)
    T = time[1] - time[0]
    yf = np.fft.fft(amplitude)
    xf = np.fft.fftfreq(N, T)[:N // 2]

    plt.figure(figsize=(10, 6))
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    plt.title('Frequency Spectrum of ECG Signal')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.xlim(0, 100)
    plt.show()

    b, a = butter(N=5, Wn=58, fs=1 / T, btype='low')
    filtered_ecg_low = filtfilt(b, a, amplitude)

    yf_filtered_low = np.fft.fft(filtered_ecg_low)

    plt.figure(figsize=(10, 6))
    plt.plot(time, amplitude, label=f'Original {filename}', alpha=0.5)
    plt.plot(time, filtered_ecg_low, label='Low-pass Filtered ECG', alpha=0.75)
    plt.title('ECG Signal Before and After Low-pass Filtering')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]), label='Original ECG', alpha=0.5)
    plt.plot(xf, 2.0 / N * np.abs(yf_filtered_low[0:N // 2]), label='Low-pass Filtered ECG', alpha=0.75)
    plt.title('Frequency Spectrum After Low-pass Filtering')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.xlim(0, 100)
    plt.legend()
    plt.grid(True)
    plt.show()

    b_high, a_high = butter(N=5, Wn=5, fs=1 / T, btype='high')

    filtered_ecg_high = filtfilt(b_high, a_high, filtered_ecg_low)

    yf_filtered_high = np.fft.fft(filtered_ecg_high)

    plt.figure(figsize=(10, 6))
    plt.plot(time, filtered_ecg_low, label='Low-pass Filtered ECG', alpha=0.5)
    plt.plot(time, filtered_ecg_high, label='High-pass Filtered ECG', alpha=0.75)
    plt.title('ECG Signal After Low-pass and High-pass Filtering')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(xf, 2.0 / N * np.abs(yf_filtered_low[0:N // 2]), label='Low-pass Filtered ECG', alpha=0.5)
    plt.plot(xf, 2.0 / N * np.abs(yf_filtered_high[0:N // 2]), label='High-pass Filtered ECG', alpha=0.75)
    plt.title('Frequency Spectrum After High-pass Filtering')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.xlim(0, 100)
    plt.legend()
    plt.grid(True)
    plt.show()






filename_list = ["ekg1.txt", "ekg100.txt", "ekg_noise.txt"]
root = tk.Tk()
root.title("Cyfrowe przetwarzanie sygnałów i obrazów")
root.config(padx=50, pady=50)

label_filename = ttk.Label(root, text="Select file")
label_filename.grid(column=0, row=0)
combobox_filename = ttk.Combobox(root, values=filename_list, width=20)
combobox_filename.current(0)
combobox_filename.grid(column=0, row=1)

button_plot = ttk.Button(root, text="Generate plot of selected signal", command=make_plot)
button_plot.grid(column=0, row=2)

label_sinus = ttk.Label(root, text="Sinus")
label_sinus.grid(column=1, row=0)

button_sinus = ttk.Button(root, text="Sinus plot generate", command=sinus_plot)
button_sinus.grid(column=1, row=1)

label_sinus_hz = ttk.Label(root, text="Enter sinus Hz exp. 50, 60, 70 ...")
label_sinus_hz.grid(column=1, row=2)
entry_sinus = ttk.Entry(root)
entry_sinus.insert(0, '50')
entry_sinus.grid(column=1, row=3)

button_sinus_fft = ttk.Button(root, text="Sinus plot and Fourier", command=lambda: sinus_plot(ttf=True))
button_sinus_fft.grid(column=1, row=4)

label_freq = ttk.Label(root, text="Enter sampling frequency")
label_freq.grid(column=1, row=5)

enter_freq = ttk.Entry(root)
enter_freq.insert(0, '2000')
enter_freq.grid(column=1, row=6)

button_restore = ttk.Button(root, text="Inverse Fourier Transform", command=lambda: sinus_plot(inverse=True, ttf=True))
button_restore.grid(column=1, row=7)

label_task_3 = ttk.Label(root, text="Task number 3")
label_task_3.grid(column=2, row=0)

button_task_3 = ttk.Button(root, text="show plot", command=lambda: make_plot(task_3=True))
button_task_3.grid(column=2, row=1)

label_filter = ttk.Label(root, text="Filter task")
label_filter.grid(column=3, row=0)

button_filter = ttk.Button(root, text="Generate plot", command=filter)
button_filter.grid(column=3, row=1)

filename_list = ["ekg1.txt", "ekg100.txt", "ekg_noise.txt"]


root.mainloop()