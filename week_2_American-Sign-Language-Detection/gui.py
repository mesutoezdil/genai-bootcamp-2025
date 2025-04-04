import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import numpy as np
import json
from pathlib import Path

class ASLDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ASL Detector")
        self.root.geometry("800x600")
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Create frames
        self.create_header_frame()
        self.create_main_frame()
        self.create_status_frame()
        
        # Initialize camera variables
        self.camera = None
        self.is_camera_active = False
        
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
    def create_header_frame(self):
        """Create the header frame with title and buttons."""
        header = ttk.Frame(self.root, padding="10")
        header.grid(row=0, column=0, sticky="ew")
        
        title = ttk.Label(header, text="ASL Sign Language Detector", font=("Arial", 20))
        title.pack(side=tk.TOP, pady=10)
        
        btn_frame = ttk.Frame(header)
        btn_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Upload Image", command=self.upload_image).pack(side=tk.LEFT, padx=5)
        self.camera_btn = ttk.Button(btn_frame, text="Start Camera", command=self.toggle_camera)
        self.camera_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Check API", command=self.check_api_status).pack(side=tk.LEFT, padx=5)
        
    def create_main_frame(self):
        """Create the main frame with image display and prediction."""
        main = ttk.Frame(self.root, padding="10")
        main.grid(row=1, column=0, sticky="nsew")
        
        # Image display
        self.image_label = ttk.Label(main)
        self.image_label.pack(expand=True, fill=tk.BOTH)
        
        # Prediction display
        self.prediction_frame = ttk.Frame(main, padding="10")
        self.prediction_frame.pack(fill=tk.X)
        
        self.prediction_label = ttk.Label(
            self.prediction_frame, 
            text="Waiting for input...", 
            font=("Arial", 16)
        )
        self.prediction_label.pack()
        
    def create_status_frame(self):
        """Create the status frame."""
        status = ttk.Frame(self.root, padding="5")
        status.grid(row=2, column=0, sticky="ew")
        
        self.status_label = ttk.Label(status, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
    def upload_image(self):
        """Handle image upload and prediction."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if not file_path:
            return
            
        try:
            # Display image
            image = Image.open(file_path)
            image.thumbnail((600, 400))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            
            # Send to API
            with open(file_path, "rb") as img:
                response = requests.post(
                    "http://localhost:5001/predict", 
                    files={"image": img},
                    timeout=5
                )
                
            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    self.show_prediction(f"Error: {result['error']}")
                else:
                    confidence = result.get("confidence", 0) * 100
                    self.show_prediction(
                        f"Predicted Letter: {result['prediction']}\n"
                        f"Confidence: {confidence:.1f}%"
                    )
            else:
                self.show_prediction(f"Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Failed to connect to API: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def toggle_camera(self):
        """Toggle webcam capture on/off."""
        if self.is_camera_active:
            self.stop_camera()
        else:
            self.start_camera()
            
    def start_camera(self):
        """Start webcam capture."""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise ValueError("Could not open camera")
                
            self.is_camera_active = True
            self.camera_btn.configure(text="Stop Camera")
            self.update_camera()
            
        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to start camera: {str(e)}")
            
    def stop_camera(self):
        """Stop webcam capture."""
        if self.camera:
            self.camera.release()
        self.is_camera_active = False
        self.camera_btn.configure(text="Start Camera")
        self.image_label.configure(image="")
        
    def update_camera(self):
        """Update camera feed and perform real-time detection."""
        if self.is_camera_active:
            ret, frame = self.camera.read()
            if ret:
                # Process frame with MediaPipe
                with self.mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=1,
                    min_detection_confidence=0.7
                ) as hands:
                    # Convert color and process
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(rgb_frame)
                    
                    # Draw landmarks if detected
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_draw.draw_landmarks(
                                frame,
                                hand_landmarks,
                                self.mp_hands.HAND_CONNECTIONS
                            )
                            
                            # Extract landmarks and predict
                            try:
                                response = requests.post(
                                    "http://localhost:5001/predict",
                                    files={"image": cv2.imencode('.jpg', frame)[1].tobytes()},
                                    timeout=0.5
                                )
                                if response.status_code == 200:
                                    result = response.json()
                                    if "prediction" in result:
                                        confidence = result.get("confidence", 0) * 100
                                        self.show_prediction(
                                            f"Predicted Letter: {result['prediction']}\n"
                                            f"Confidence: {confidence:.1f}%"
                                        )
                            except:
                                pass  # Ignore API errors during live feed
                
                # Convert frame for display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)  # Mirror image
                image = Image.fromarray(frame)
                image.thumbnail((600, 400))
                photo = ImageTk.PhotoImage(image=image)
                self.image_label.configure(image=photo)
                self.image_label.image = photo
            
            # Schedule next update
            self.root.after(10, self.update_camera)
            
    def show_prediction(self, text):
        """Update prediction display."""
        self.prediction_label.configure(text=text)
        
    def check_api_status(self):
        """Check if the API is running."""
        try:
            response = requests.get("http://localhost:5001/health", timeout=2)
            if response.status_code == 200:
                result = response.json()
                if result.get("model_loaded"):
                    messagebox.showinfo("API Status", "API is running and model is loaded")
                else:
                    messagebox.showwarning("API Status", "API is running but model is not loaded")
            else:
                messagebox.showerror("API Status", "API is not responding correctly")
        except requests.exceptions.RequestException:
            messagebox.showerror("API Status", "Could not connect to API")
            
    def on_closing(self):
        """Handle window closing."""
        if self.camera:
            self.camera.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ASLDetectorGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
