import tkinter as tk
from tkinter import ttk
import websocket
import threading
import json
import time

class NeuroBandApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroBand Desktop Application")
        self.root.geometry("800x600")

        self.ws = None
        self.ws_thread = None
        self.is_connected = False

        self.create_widgets()
        self.connect_websocket()

    def create_widgets(self):
        # Connection Status
        self.status_label = ttk.Label(self.root, text="Status: Disconnected", foreground="red")
        self.status_label.pack(pady=10)

        # Notebook for different modules
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Live GUI Dashboard Tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Live GUI Dashboard")
        self.create_dashboard_widgets(self.dashboard_frame)

        # Brain-Controlled Interface Tab (Placeholder)
        self.bci_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bci_frame, text="Brain-Controlled Interface")
        ttk.Label(self.bci_frame, text="Brain-Controlled Interface features will go here.").pack(pady=20)

        # Signal Processing Tab (Placeholder)
        self.signal_processing_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.signal_processing_frame, text="Signal Processing")
        ttk.Label(self.signal_processing_frame, text="Signal Processing details and visualizations will go here.").pack(pady=20)

        # Other Wow Features Tab (Placeholder)
        self.wow_features_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.wow_features_frame, text="Wow Features")
        ttk.Label(self.wow_features_frame, text="Emergency Alert, Mindfulness Coach, etc., will go here.").pack(pady=20)

    def create_dashboard_widgets(self, parent_frame):
        # Example: Displaying raw EEG value
        self.eeg_value_label = ttk.Label(parent_frame, text="Raw EEG Value: N/A", font=("Arial", 16))
        self.eeg_value_label.pack(pady=20)

        # Placeholder for Heart Rate Graph
        ttk.Label(parent_frame, text="[Heart Rate Graph Placeholder]").pack(pady=10)

        # Placeholder for Emotion Indicators
        self.emotion_label = ttk.Label(parent_frame, text="Emotion: N/A", font=("Arial", 14))
        self.emotion_label.pack(pady=10)

        # Placeholder for Stress Score Bar
        ttk.Label(parent_frame, text="[Stress Score Bar Placeholder]").pack(pady=10)

    def connect_websocket(self):
        # Replace with your ESP32's IP address
        esp32_ip = "YOUR_ESP32_IP_ADDRESS"
        websocket_url = f"ws://{esp32_ip}:8080/ws"

        try:
            self.ws = websocket.WebSocketApp(websocket_url,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close)
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            self.status_label.config(text="Status: Connecting...", foreground="orange")
        except Exception as e:
            self.status_label.config(text=f"Status: Connection Error: {e}", foreground="red")
            self.is_connected = False

    def on_open(self, ws):
        self.is_connected = True
        self.root.after(0, lambda: self.status_label.config(text="Status: Connected", foreground="green"))
        print("WebSocket connection opened")

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            timestamp = data.get("timestamp")
            eeg_value = data.get("eeg")

            # Update GUI from the main thread
            self.root.after(0, lambda: self.eeg_value_label.config(text=f"Raw EEG Value: {eeg_value}"))
            # In a real application, you'd pass this data to signal processing functions
            self.process_signal(eeg_value)

        except json.JSONDecodeError:
            print(f"Received non-JSON message: {message}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def on_error(self, ws, error):
        self.is_connected = False
        self.root.after(0, lambda: self.status_label.config(text=f"Status: Error: {error}", foreground="red"))
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self.is_connected = False
        self.root.after(0, lambda: self.status_label.config(text="Status: Disconnected", foreground="red"))
        print(f"WebSocket closed: {close_status_code} - {close_msg}")
        # Attempt to reconnect after a delay
        self.root.after(5000, self.connect_websocket) # Reconnect after 5 seconds

    def process_signal(self, raw_eeg_value):
        # This is a placeholder for actual signal processing logic
        # In a real scenario, you'd use NeuroKit2 or SciPy here.
        # For demonstration, let's simulate some basic logic.

        # Example: Simple blink detection (if value crosses a threshold)
        blink_threshold = 2000 # Example threshold
        if raw_eeg_value > blink_threshold:
            self.root.after(0, lambda: self.emotion_label.config(text="Emotion: Blink Detected!"))
            # Trigger pyautogui action here (e.g., mouse click)
            # import pyautogui
            # pyautogui.click()
        elif raw_eeg_value < 1000:
            self.root.after(0, lambda: self.emotion_label.config(text="Emotion: Relaxed"))
        else:
            self.root.after(0, lambda: self.emotion_label.config(text="Emotion: Neutral"))

        # Placeholder for more complex signal processing (e.g., FFT for brainwaves, HRV for ECG)
        # You would integrate libraries like NeuroKit2 here.

    def on_closing(self):
        if self.ws:
            self.ws.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroBandApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


