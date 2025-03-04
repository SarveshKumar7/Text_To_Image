import torch
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from diffusers import StableDiffusionPipeline

# Load Stable Diffusion model (first-time download may take time)
try:
    pipeline = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipeline.to("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available
except Exception as e:
    messagebox.showerror("Error", f"Failed to load the model: {e}")
    exit()

saved_image = None  # Variable to store the generated image

# Function to generate an image from text
def generate_image():
    global saved_image
    prompt = entry.get()
    
    if not prompt:
        messagebox.showerror("Error", "Please enter a text prompt!")
        return

    label_status.config(text="Generating image... Please wait.", fg="blue")
    root.update()

    try:
        image = pipeline(prompt).images[0]  # Generate image
        image.thumbnail((300, 300))  # Resize for display
        img_tk = ImageTk.PhotoImage(image)

        label_image.config(image=img_tk)
        label_image.image = img_tk
        saved_image = image  # Store the generated image

        label_status.config(text="Image generated successfully!", fg="green")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate image: {e}")
        label_status.config(text="Image generation failed.", fg="red")

# Function to save the generated image
def save_image():
    if saved_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            saved_image.save(file_path)
            messagebox.showinfo("Success", f"Image saved as {file_path}")
    else:
        messagebox.showerror("Error", "No image to save!")

# Create GUI Window
root = tk.Tk()
root.title("Text-to-Image Generator (Stable Diffusion)")
root.geometry("500x550")
root.resizable(False, False)

# UI Elements
tk.Label(root, text="Enter a text description:", font=("Arial", 12)).pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

btn_generate = tk.Button(root, text="Generate Image", command=generate_image, bg="blue", fg="white")
btn_generate.pack(pady=10)

label_status = tk.Label(root, text="", font=("Arial", 10))
label_status.pack()

label_image = tk.Label(root)
label_image.pack(pady=10)

btn_save = tk.Button(root, text="Save Image", command=save_image, bg="green", fg="white")
btn_save.pack(pady=10)

# Run the GUI
root.mainloop()