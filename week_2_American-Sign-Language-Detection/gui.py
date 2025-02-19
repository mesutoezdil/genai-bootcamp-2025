import tkinter as tk
import requests
from PIL import Image, ImageTk
from tkinter import filedialog

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "rb") as img:
            response = requests.post("http://localhost:5000/predict", files={"image": img})
            result_label.config(text="Predicted ASL Letter: " + response.json().get("prediction", "Error"))

root = tk.Tk()
root.title("ASL Detector")

button = tk.Button(root, text="Upload ASL Image", command=upload_image)
button.pack()

result_label = tk.Label(root, text="Waiting for prediction...", font=("Arial", 20))
result_label.pack()

root.mainloop()
