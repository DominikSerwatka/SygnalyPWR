import tkinter as tk
from tkinter import ttk
from PIL import Image



filename_list = ["aerial_view.tif", "blurry-moon.tif", "bonescan.tif", "cboard_pepper_only.tif", "cboard_salt_only.tif",
                 "chest-xray.tif", "circuitmask.tif", "einstein-low-contrast.tif", "hidden-symbols.tif",
                 "pollen-dark.tif", "pollen-ligt.tif", "pollen-lowcontrast.tif", "pout.tif", "spectrum.tif",
                 "text-dipxe-blurred.tif", "zoneplate.tif"]


def get_image():
    filename = combobox_filename.get()
    im = Image.open(rf".\static\{filename}")
    im.show()


root = tk.Tk()
root.title("Cyfrowe przetwarzanie sygnałów i obrazów")
root.config(padx=50, pady=50)

label_filename = ttk.Label(root, text="Select file")
label_filename.grid(column=0, row=0)
combobox_filename = ttk.Combobox(root, values=filename_list, width=20)
combobox_filename.current(0)
combobox_filename.grid(column=0, row=1)

button_plot = ttk.Button(root, text="Get image from list", command=get_image)
button_plot.grid(column=0, row=2)

root.mainloop()