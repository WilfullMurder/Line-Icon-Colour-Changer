import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps
import os

# **Updated Colorblind-Friendly Colors**
ICON_COLORS = {
    "light": "#000000",
    "dark": "#FFFFFF",
    "deuteranopia": "#005694",  # Royal Blue
    "protanopia": "#FFA666",  # Soft Apricot
    "tritanopia": "#EB60CB",  # Electric Fuchsia
}

def change_line_color(img, color):
    # Convert the image to RGBA
    img = img.convert("RGBA")
    data = img.getdata()

    # Create a new image with the same size
    new_data = []
    for item in data:
        # Change all black (0, 0, 0) pixels to the desired color
        if item[:3] == (0, 0, 0):
            new_data.append(tuple(int(color[i:i + 2], 16) for i in (1, 3, 5)) + (item[3],))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img

def apply_color_scheme(input_path, output_path, color):
    # Open the input image
    img = Image.open(input_path)

    # Change the line color
    img_transformed = change_line_color(img, color)

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Save the transformed image
    output_file = os.path.join(output_path, os.path.basename(input_path))
    img_transformed.save(output_file)

def process_files(files, output_dir):
    # Process each selected file with all color schemes
    for input_file in files:
        for theme, color in ICON_COLORS.items():
            # Create subfolder paths for each theme
            output_path = os.path.join(output_dir, theme)
            apply_color_scheme(input_file, output_path, color)

def browse_files(selected_files_listbox):
    # Open a file dialog to select multiple files
    files = filedialog.askopenfilenames(
        title="Select Icons",
        filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
    )

    if files:
        selected_files_listbox.delete(0, tk.END)  # Clear the listbox
        for file in files:
            selected_files_listbox.insert(tk.END, file)  # Add each file to the listbox

def select_output_folder(output_folder_label):
    # Open a folder dialog to select the output directory
    output_dir = filedialog.askdirectory(title="Select Output Folder")
    if output_dir:
        output_folder_label.config(text=f"Output folder: {output_dir}")
    return output_dir

def main():
    # Create the main GUI window
    root = tk.Tk()
    root.title("Icon Processor")

    # Set window size
    root.geometry("600x400")

    # Variable to store the output directory path
    selected_output_folder = None

    # Label to display selected files
    selected_files_listbox = tk.Listbox(root, height=10, width=80)
    selected_files_listbox.pack(pady=10)

    # Label to display the selected output folder
    output_folder_label = tk.Label(root, text="No output folder selected")
    output_folder_label.pack(pady=10)

    # Function to handle output folder selection
    def browse_output_folder():
        nonlocal selected_output_folder
        # Prompt user to select the output folder
        selected_output_folder = select_output_folder(output_folder_label)

    # Function to process selected files
    def process():
        if not selected_files_listbox.size() or selected_output_folder is None:
            messagebox.showwarning("Missing Information", "Please select both files and output folder.")
            return

        files = selected_files_listbox.get(0, tk.END)  # Get the list of file paths
        process_files(files, selected_output_folder)
        messagebox.showinfo("Processing Complete", "Files processed successfully.")

    # Add buttons for selecting files and output folder
    select_files_button = tk.Button(root, text="Select Files", command=lambda: browse_files(selected_files_listbox))
    select_files_button.pack(pady=10)

    select_output_folder_button = tk.Button(root, text="Select Output Folder", command=browse_output_folder)
    select_output_folder_button.pack(pady=10)

    process_button = tk.Button(root, text="Process Files", command=process)
    process_button.pack(pady=20)

    # Start the Tkinter main loop
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()