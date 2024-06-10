import os.path
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

import scipy
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter, minimum_filter, maximum_filter, uniform_filter, gaussian_filter
from skimage import exposure
from skimage.util import img_as_ubyte

filename_list = ["aerial_view.tif", "blurry-moon.tif", "bonescan.tif", "cboard_pepper_only.tif", "cboard_salt_only.tif",
                 "chest-xray.tif", "cboard_salt_pepper.tif", "circuitmask.tif", "einstein-low-contrast.tif",
                 "hidden-symbols.tif",
                 "pollen-dark.tif", "pollen-ligt.tif", "pollen-lowcontrast.tif", "pout.tif", "spectrum.tif",
                 "text-dipxe-blurred.tif", "zoneplate.tif", "characters_test_pattern.tif", "testpat1.png"]


class ImageClass:
    def __init__(self):
        self.name = None
        self.image = None
        self.set_image()

    def set_image(self):
        filename = combobox_filename.get()
        self.name = filename
        file_path = os.path.abspath(f"static/{filename}")
        im = Image.open(file_path)
        self.image = im


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


def transform_by_const():
    image = get_image()
    grey_image = image.convert('L')
    c = float(simpledialog.askstring("User input", "Enter number to perform transformation"))
    image_array = np.array(grey_image)
    transformed_image_array = np.clip(c * image_array, 0, 255).astype(np.uint8)
    transformed_image = Image.fromarray(transformed_image_array)
    transformed_image.show()


def transform_by_logarithm():
    image = get_image()
    grey_image = image.convert('L')
    c = float(simpledialog.askstring("User input", "Enter number to perform transformation"))
    image_array = np.array(grey_image)
    transformed_image_array = np.clip(c * np.log1p(image_array), 0, 255).astype(np.uint8)
    transformed_image = Image.fromarray(transformed_image_array)
    transformed_image.show()


def transform_to_show_contrast():
    image = get_image()
    grey_image = image.convert('L')
    m = float(simpledialog.askstring("User input", "Enter the value of parameter m"))
    e = float(simpledialog.askstring("User input", "Enter the value of parameter e"))
    image_array = np.array(grey_image)
    transformed_image_array = np.clip(255 * (1 / (1 + (m / (image_array / 255.0)) ** e)), 0, 255).astype(np.uint8)
    transformed_image = Image.fromarray(transformed_image_array)
    transformed_image.show()

    # Plot T(r)
    r = np.linspace(0, 255, 256)
    T_of_r = 255 * (1 / (1 + (m / (r / 255.0)) ** e))
    plt.plot(r, T_of_r)
    plt.title(f"Transformation T(r) with m={m}, e={e}")
    plt.xlabel("Input intensity (r)")
    plt.ylabel("Output intensity (T(r))")
    plt.show()


def gamma_corection():
    image = get_image()
    grey_image = image.convert('L')
    c = float(simpledialog.askstring("User input", "Enter the value of const c"))
    gamma = float(simpledialog.askstring("User input", "Enter the value of gamma"))
    image_array = np.array(grey_image)
    normalize_image_array = image_array / 255.0
    transformed_image_array = np.clip(c * (normalize_image_array ** gamma) * 255, 0, 255).astype(np.uint8)
    transformed_image = Image.fromarray(transformed_image_array)
    transformed_image.show()


def histogram_generation():
    image = ImageClass()
    grey_image = image.image.convert('L')
    image_array = np.array(grey_image)
    plt.hist(image_array.flatten(), bins=256, range=(0, 256), color='black', alpha=0.7)
    plt.title(f"Histogram of {image.name}")
    plt.xlabel("Pixel value")
    plt.ylabel("Frequency")
    plt.show()


def histogram_equalization():
    image = ImageClass()
    grey_image = image.image.convert('L')
    equalization_image = ImageOps.equalize(grey_image)
    image_array = np.array(equalization_image)
    plt.hist(image_array.flatten(), bins=256, range=(0, 256), color='black', alpha=0.7)
    plt.title(f"Histogram after equalization of {image.name}")
    plt.xlabel("Pixel value")
    plt.ylabel("Frequency")
    plt.show()
    equalization_image.show()


def local_histogram_equalization():
    image_object = ImageClass()
    image = get_image()
    grey_image = image.convert('L')
    image_array = np.array(grey_image)
    kernel_size = int(simpledialog.askstring("Input", "Enter the kernel size (e.g., 8 for 8x8 blocks):").strip())
    equalized_image_array = exposure.equalize_adapthist(image_array / 255.0, kernel_size=(kernel_size, kernel_size),
                                                        clip_limit=0.03)
    equalized_image_array = img_as_ubyte(equalized_image_array)
    equalized_image = Image.fromarray(equalized_image_array)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(image_array.flatten(), bins=256, range=(0, 256), color='black', alpha=0.7)
    axes[0].set_title(f"Histogram of {image_object.name} before local equalization")
    axes[0].set_xlabel("Pixel value")
    axes[0].set_ylabel("Frequency")
    axes[1].hist(equalized_image_array.flatten(), bins=256, range=(0, 256), color='black', alpha=0.7)
    axes[1].set_title(f"Histogram of {image_object.name} after local equalization")
    axes[1].set_xlabel("Pixel value")
    axes[1].set_ylabel("Frequency")
    plt.tight_layout()
    plt.show()
    equalized_image.show()


def local_statistical_enhancement():
    image = get_image()
    grey_image = image.convert('L')
    image_array = np.array(grey_image)

    mask_size = int(simpledialog.askstring("Input", "Enter the mask size (e.g., 3 for a 3x3 mask):").strip())
    if mask_size % 2 == 0:
        messagebox.showerror("Error", "Mask size must be an odd number.")
        return

    mean_filter = np.ones((mask_size, mask_size)) / (mask_size ** 2)
    local_mean = scipy.ndimage.convolve(image_array, mean_filter, mode='reflect')
    local_var = scipy.ndimage.generic_filter(image_array, np.var, size=mask_size, mode='reflect')

    C = 22.8
    k0 = k2 = 0
    k1 = k3 = 0.1

    global_mean = np.mean(image_array)
    global_var = np.var(image_array)

    enhanced_image_array = np.where(
        (local_mean <= k1 * global_mean) & (local_var >= k2 * global_var) & (local_var <= k3 * global_var),
        C * image_array,
        image_array
    )

    enhanced_image_array = np.clip(enhanced_image_array, 0, 255).astype(np.uint8)
    enhanced_image = Image.fromarray(enhanced_image_array)

    enhanced_image.show()


def lowpass_averaging_filter():
    image = get_image()
    grey_image = image.convert('L')
    image_array = np.array(grey_image)
    mask_size = int(simpledialog.askstring("Input", "Enter the kernel size (e.g., 3 for 3x3 blocks):").strip())
    filter_kernel = np.ones((mask_size, mask_size)) / (mask_size ** 2)
    filtered_image_array = scipy.ndimage.convolve(image_array, filter_kernel, mode='reflect')
    filtered_image = Image.fromarray(filtered_image_array.astype(np.uint8))

    filtered_image.show()


def apply_median_filter():
    image = get_image()
    grey_image = image.convert('L')
    image_array = np.array(grey_image)

    mask_size = simpledialog.askinteger("Input", "Enter the mask size (e.g., 3 for a 3x3 mask):", minvalue=1, maxvalue=None)
    if mask_size is None:
        return

    if mask_size % 2 == 0:
        messagebox.showerror("Error", "Mask size must be an odd number.")
        return
    filtered_image_array = median_filter(image_array, size=mask_size)
    filtered_image = Image.fromarray(filtered_image_array)
    filtered_image.show()


def apply_minimum_filter():
    image = get_image()
    grey_image = image.convert('L')
    image_array = np.array(grey_image)


    mask_size = simpledialog.askinteger("Input", "Enter the mask size (e.g., 3 for a 3x3 mask):", minvalue=1, maxvalue=None)
    if mask_size is None:
        return

    filtered_image_array = minimum_filter(image_array, size=mask_size)
    filtered_image = Image.fromarray(filtered_image_array)
    filtered_image.show()


def apply_maximum_filter():
    image = get_image()
    grey_image = image.convert('L')
    image_array = np.array(grey_image)
    mask_size = simpledialog.askinteger("Input", "Enter the mask size (e.g., 3 for a 3x3 mask):", minvalue=1, maxvalue=None)
    if mask_size is None:
        return
    filtered_image_array = maximum_filter(image_array, size=mask_size)
    filtered_image = Image.fromarray(filtered_image_array)
    filtered_image.show()


def apply_averaging_filter():
    image = get_image()
    grey_image = image.convert('L')
    image_array = np.array(grey_image)
    mask_size = int(simpledialog.askstring("Input", "Enter the mask size (e.g., 3 for a 3x3 mask):"))
    filtered_image_array = uniform_filter(image_array, size=mask_size)
    filtered_image = Image.fromarray(filtered_image_array)
    filtered_image.show()


def apply_gaussian_filter():
    image = get_image()
    grey_image = image.convert('L')
    image_array = np.array(grey_image)
    sigma = float(simpledialog.askstring("Input", "Enter the sigma value for the Gaussian filter:"))
    filtered_image_array = gaussian_filter(image_array, sigma=sigma)
    filtered_image = Image.fromarray(filtered_image_array)
    filtered_image.show()


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
button_grey_profile.grid(column=0, row=4)

button_select_subimage = ttk.Button(root, text="Select and Save Subimage", command=select_subimage)
button_select_subimage.grid(column=0, row=5)

button_const_transform = ttk.Button(root, text="Transform image by const", command=transform_by_const)
button_const_transform.grid(column=0, row=6)

button_const_log_transform = ttk.Button(root, text="Logarithm transformation", command=transform_by_logarithm)
button_const_log_transform.grid(column=0, row=7)

button_contrast_show = ttk.Button(root, text="Contrast of the picture", command=transform_to_show_contrast)
button_contrast_show.grid(column=0, row=8)

button_gamma_corection = ttk.Button(root, text="Gamma correction", command=gamma_corection)
button_gamma_corection.grid(column=0, row=9)

button_show_histogram = ttk.Button(root, text="Histogram generation", command=histogram_generation)
button_show_histogram.grid(column=0, row=10)

button_show_histogram_after_equalization = ttk.Button(root, text="Histogram after equalization",
                                                      command=histogram_equalization)
button_show_histogram_after_equalization.grid(column=0, row=11)

button_local_histogram_equalization = ttk.Button(root, text="Histogram after local equalization",
                                                 command=local_histogram_equalization)
button_local_histogram_equalization.grid(column=0, row=12)

button_local_statistical_enhancement = ttk.Button(root, text="Local statistical enhancement",
                                                  command=local_statistical_enhancement)
button_local_statistical_enhancement.grid(column=0, row=13)

button_lowpass_averaging_filter = ttk.Button(root, text="Lowpass averaging filter", command=lowpass_averaging_filter)
button_lowpass_averaging_filter.grid(column=0, row=14)

button_lowpass_median_filter = ttk.Button(root, text="Lowpass median filter", command=apply_median_filter)
button_lowpass_median_filter.grid(column=0, row=15)

button_minimum_filter = ttk.Button(root, text="Lowpass minimum filter", command=apply_minimum_filter)
button_minimum_filter.grid(column=0, row=16)

button_maximum_filter = ttk.Button(root, text="Lowpass maximum filter", command=apply_maximum_filter)
button_maximum_filter.grid(column=0, row=17)

button_averaging_filter = ttk.Button(root, text="Averaging filter", command=apply_averaging_filter)
button_averaging_filter.grid(column=0, row=18)

button_gaussian_filter = ttk.Button(root, text="Gaussion filter", command=apply_gaussian_filter)
button_gaussian_filter.grid(column=0, row=19)

root.mainloop()
