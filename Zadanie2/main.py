import os.path
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

filename_list = ["aerial_view.tif", "blurry-moon.tif", "bonescan.tif", "cboard_pepper_only.tif", "cboard_salt_only.tif",
                 "chest-xray.tif", "circuitmask.tif", "einstein-low-contrast.tif", "hidden-symbols.tif",
                 "pollen-dark.tif", "pollen-ligt.tif", "pollen-lowcontrast.tif", "pout.tif", "spectrum.tif",
                 "text-dipxe-blurred.tif", "zoneplate.tif"]


def get_image():
    filename = combobox_filename.get()
    file_path = os.path.abspath(f"static/{filename}")
    im = Image.open(file_path)
    return im


def show_image():
    image = get_image()
    image.show()


def get_direction():
    direction = simpledialog.askstring("User Input", "Enter direction (horizontal/vertival)").strip().lower()
    while not (direction == 'horizontal' or direction == 'vertical'):
        messagebox.showinfo(message="Try again, please provide correct value")
        direction = simpledialog.askstring("User Input", "Enter direction (horizontal/vertival)").strip().lower()
    return direction


def get_coord(image_array, direction):
    horizontal_elements = np.size(image_array, 1)
    vertical_elements = np.size(image_array, 0)
    print(horizontal_elements)
    print(vertical_elements)
    direction_mapping = {
        'vertical': vertical_elements,
        'horizontal': horizontal_elements,
    }

    position = int(simpledialog
                   .askstring("User Input", f"Enter number form 0 to {direction_mapping[direction]}")
                   .strip())
    while not (0 <= position <= direction_mapping[direction]):
        messagebox.showinfo(message="Try again, please provide correct value")
        position = int(simpledialog
                       .askstring("User Input", f"Enter number form 0 to {direction_mapping[direction]}")
                       .strip())
    return position


def plot_greyscale_profile():
    image = get_image()
    grey_image = image.convert('L')
    direction = get_direction()
    image_array = np.array(grey_image)
    print(image_array)
    position = get_coord(image_array, direction)
    if direction == 'horizontal':
        profile = image_array[position, :]
        plt.plot(profile)
        plt.title(f'{direction} greyscale profile at y={position}')
        plt.xlabel('Pixel Index')
        plt.ylabel('Greyscale value')
        plt.show()
    else:
        profile = image_array[:, position]
        plt.plot(profile)
        plt.title(f'{direction} greyscale profile at x={position}')
        plt.xlabel('Pixel Index')
        plt.ylabel('Greyscale value')
        plt.show()


def select_subimage():
    image = get_image()
    image_array = np.array(image)

    x1 = int(
        simpledialog.askstring("User Input", f"Enter x1 coordinate(from 0 to {np.size(image_array, 1)}): ").strip())
    y1 = int(
        simpledialog.askstring("User Input", f"Enter y1 coordinate(from 0 to {np.size(image_array, 0)}): ").strip())
    x2 = int(
        simpledialog.askstring("User Input", f"Enter x2 coordinate(from 0 to {np.size(image_array, 1)}): ").strip())
    y2 = int(
        simpledialog.askstring("User Input", f"Enter y2 coordinate(from 0 to {np.size(image_array, 0)}): ").strip())

    while (x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0 or x1 > np.size(image_array, 1) or x2 > np.size(image_array,
                                                                                                1) or y1 > np.size(
            image_array, 0) or y2 > np.size(image_array, 0) or x1 > x2 or y1 > y2):
        messagebox.showinfo(message="Invalid dat, please provide valid data")
        x1 = int(
            simpledialog.askstring("User Input", f"Enter x1 coordinate(from 0 to {np.size(image_array, 1)}): ").strip())
        y1 = int(
            simpledialog.askstring("User Input", f"Enter y1 coordinate(from 0 to {np.size(image_array, 0)}): ").strip())
        x2 = int(
            simpledialog.askstring("User Input", f"Enter x2 coordinate(from 0 to {np.size(image_array, 1)}): ").strip())
        y2 = int(
            simpledialog.askstring("User Input", f"Enter y2 coordinate(from 0 to {np.size(image_array, 0)}): ").strip())
    subimage = image_array[y1:y2, x1:x2]
    subimage_pil = Image.fromarray(subimage)
    subimage_pil.show()
    save_subimage(subimage_pil)


def save_subimage(subimage):
    file_name = simpledialog.askstring("User Input", "Enter filename to save").strip()
    save_dir = os.path.abspath("new_image")
    if not file_name.endswith(".tif"):
        file_name += ".tif"
    full_file_path = os.path.join(save_dir, file_name)
    subimage.save(full_file_path)


root = tk.Tk()
root.title("Cyfrowe przetwarzanie sygnałów i obrazów")
root.config(padx=50, pady=50)

label_filename = ttk.Label(root, text="Select file")
label_filename.grid(column=0, row=0)
combobox_filename = ttk.Combobox(root, values=filename_list, width=20)
combobox_filename.current(0)
combobox_filename.grid(column=0, row=1)

button_plot = ttk.Button(root, text="Get image from list", command=show_image)
button_plot.grid(column=0, row=2)

button_grey_profile = ttk.Button(root, text="Plot Greyscale Profile", command=plot_greyscale_profile)
button_grey_profile.grid(column=0, row=3)

button_select_subimage = ttk.Button(root, text="Select and Save Subimage", command=select_subimage)
button_select_subimage.grid(column=0, row=3)

root.mainloop()
