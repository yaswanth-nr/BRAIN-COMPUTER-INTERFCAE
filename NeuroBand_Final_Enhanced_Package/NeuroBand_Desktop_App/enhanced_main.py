import tkinter as tk
from tkinter import ttk, messagebox
import websocket
import threading
import json
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque

# Import our custom modules
from signal_processing import SignalProcessor
from brain_control import BrainControlInterface
from wow_features import WowFeaturesManager

class EnhancedNeuroBandApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroBand - Advanced Brain-Computer Interface")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')

        # Initialize core components
        self.signal_processor = SignalProcessor()
        self.brain_controller = BrainControlInterface()
        self.wow_features = WowFeaturesManager()

        # WebSocket connection
        self.ws = None
        self.ws_thread = None
        self.is_connected = False

        # Data storage for real-time plotting
        self.eeg_data = deque(maxlen=500)  # Store last 500 samples
        self.heart_rate_data = deque(maxlen=100)
        self.stress_data = deque(maxlen=100)
        self.attention_data = deque(maxlen=100)
        self.timestamps = deque(maxlen=500)

        # Current values
        self.current_heart_rate = 0
        self.current_stress = 0
        self.current_attention = 0
        self.current_emotion = "neutral"

        self.create_enhanced_ui()
        self.setup_real_time_plots()
        self.connect_websocket()

    def create_enhanced_ui(self):
        """Create enhanced user interface with modern styling"""
        
        # Main container
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Header with connection status
        header_frame = tk.Frame(main_container, bg='#34495e', height=60)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(header_frame, text="🧠 NeuroBand Control Center", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#34495e')
        title_label.pack(side='left', padx=20, pady=15)

        # Connection status
        self.status_label = tk.Label(header_frame, text="● Disconnected", 
                                    font=('Arial', 12, 'bold'), fg='#e74c3c', bg='#34495e')
        self.status_label.pack(side='right', padx=20, pady=15)

        # Main content area with notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(expand=True, fill="both")

        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2c3e50')
        style.configure('TNotebook.Tab', padding=[20, 10])

        # Create tabs
        self.create_dashboard_tab()
        self.create_brain_control_tab()
        self.create_signal_analysis_tab()
        self.create_wow_features_tab()
        self.create_settings_tab()

    def create_dashboard_tab(self):
        """Create live dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Live Dashboard")

        # Create main dashboard layout
        left_panel = tk.Frame(dashboard_frame, bg='#ecf0f1', width=400)
        left_panel.pack(side='left', fill='y', padx=5, pady=5)
        left_panel.pack_propagate(False)

        right_panel = tk.Frame(dashboard_frame, bg='#ecf0f1')
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        # Left panel - Current values
        self.create_vital_signs_panel(left_panel)

        # Right panel - Real-time graphs
        self.create_graphs_panel(right_panel)

    def create_vital_signs_panel(self, parent):
        """Create vital signs display panel"""
        # Title
        title = tk.Label(parent, text="Vital Signs", font=('Arial', 16, 'bold'), 
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=10)

        # Heart Rate
        hr_frame = tk.Frame(parent, bg='#e74c3c', height=80)
        hr_frame.pack(fill='x', padx=20, pady=5)
        hr_frame.pack_propagate(False)

        tk.Label(hr_frame, text="❤️ Heart Rate", font=('Arial', 12, 'bold'), 
                bg='#e74c3c', fg='white').pack(pady=5)
        self.hr_value_label = tk.Label(hr_frame, text="-- BPM", font=('Arial', 18, 'bold'), 
                                      bg='#e74c3c', fg='white')
        self.hr_value_label.pack()

        # Stress Level
        stress_frame = tk.Frame(parent, bg='#f39c12', height=80)
        stress_frame.pack(fill='x', padx=20, pady=5)
        stress_frame.pack_propagate(False)

        tk.Label(stress_frame, text="⚡ Stress Level", font=('Arial', 12, 'bold'), 
                bg='#f39c12', fg='white').pack(pady=5)
        self.stress_value_label = tk.Label(stress_frame, text="--%", font=('Arial', 18, 'bold'), 
                                          bg='#f39c12', fg='white')
        self.stress_value_label.pack()

        # Attention Level
        attention_frame = tk.Frame(parent, bg='#3498db', height=80)
        attention_frame.pack(fill='x', padx=20, pady=5)
        attention_frame.pack_propagate(False)

        tk.Label(attention_frame, text="🎯 Attention", font=('Arial', 12, 'bold'), 
                bg='#3498db', fg='white').pack(pady=5)
        self.attention_value_label = tk.Label(attention_frame, text="--%", font=('Arial', 18, 'bold'), 
                                             bg='#3498db', fg='white')
        self.attention_value_label.pack()

        # Emotion State
        emotion_frame = tk.Frame(parent, bg='#9b59b6', height=80)
        emotion_frame.pack(fill='x', padx=20, pady=5)
        emotion_frame.pack_propagate(False)

        tk.Label(emotion_frame, text="😊 Emotion", font=('Arial', 12, 'bold'), 
                bg='#9b59b6', fg='white').pack(pady=5)
        self.emotion_value_label = tk.Label(emotion_frame, text="Neutral", font=('Arial', 18, 'bold'), 
                                           bg='#9b59b6', fg='white')
        self.emotion_value_label.pack()

    def create_graphs_panel(self, parent):
        """Create real-time graphs panel"""
        # This will be populated by setup_real_time_plots()
        self.graphs_frame = parent

    def setup_real_time_plots(self):
        """Setup real-time plotting"""
        # Create matplotlib figure
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(10, 8))
        self.fig.patch.set_facecolor('#ecf0f1')

        # Configure subplots
        self.ax1.set_title('EEG Signal', fontsize=12, fontweight='bold')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.grid(True, alpha=0.3)

        self.ax2.set_title('Heart Rate', fontsize=12, fontweight='bold')
        self.ax2.set_ylabel('BPM')
        self.ax2.grid(True, alpha=0.3)

        self.ax3.set_title('Stress Level', fontsize=12, fontweight='bold')
        self.ax3.set_ylabel('Stress %')
        self.ax3.grid(True, alpha=0.3)

        self.ax4.set_title('Attention Level', fontsize=12, fontweight='bold')
        self.ax4.set_ylabel('Attention %')
        self.ax4.grid(True, alpha=0.3)

        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.graphs_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Start real-time update
        self.update_plots()

    def create_brain_control_tab(self):
        """Create brain control interface tab"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="🧠 Brain Control")

        # Control status
        status_frame = tk.Frame(control_frame, bg='#ecf0f1', height=100)
        status_frame.pack(fill='x', padx=10, pady=10)
        status_frame.pack_propagate(False)

        tk.Label(status_frame, text="Brain Control Interface", font=('Arial', 16, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=10)

        self.control_status_label = tk.Label(status_frame, text="Status: Monitoring brain signals...", 
                                           font=('Arial', 12), bg='#ecf0f1', fg='#7f8c8d')
        self.control_status_label.pack()

        # Control options
        options_frame = tk.Frame(control_frame, bg='#ecf0f1')
        options_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Blink control
        blink_frame = tk.LabelFrame(options_frame, text="Blink Control", font=('Arial', 12, 'bold'),
                                   bg='#ecf0f1', fg='#2c3e50')
        blink_frame.pack(fill='x', pady=10)

        tk.Label(blink_frame, text="• Blink to perform mouse click", bg='#ecf0f1').pack(anchor='w', padx=10, pady=5)
        self.blink_count_label = tk.Label(blink_frame, text="Blinks detected: 0", bg='#ecf0f1')
        self.blink_count_label.pack(anchor='w', padx=10, pady=5)

        # Attention control
        attention_frame = tk.LabelFrame(options_frame, text="Attention Control", font=('Arial', 12, 'bold'),
                                       bg='#ecf0f1', fg='#2c3e50')
        attention_frame.pack(fill='x', pady=10)

        tk.Label(attention_frame, text="• Focus to control cursor movement", bg='#ecf0f1').pack(anchor='w', padx=10, pady=5)
        self.cursor_pos_label = tk.Label(attention_frame, text="Cursor position: (0, 0)", bg='#ecf0f1')
        self.cursor_pos_label.pack(anchor='w', padx=10, pady=5)

        # Alpha state control
        alpha_frame = tk.LabelFrame(options_frame, text="Alpha State Control", font=('Arial', 12, 'bold'),
                                   bg='#ecf0f1', fg='#2c3e50')
        alpha_frame.pack(fill='x', pady=10)

        tk.Label(alpha_frame, text="• Enter relaxed state to trigger actions", bg='#ecf0f1').pack(anchor='w', padx=10, pady=5)
        self.alpha_action_label = tk.Label(alpha_frame, text="Last action: None", bg='#ecf0f1')
        self.alpha_action_label.pack(anchor='w', padx=10, pady=5)

    def create_signal_analysis_tab(self):
        """Create signal analysis tab"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="📈 Signal Analysis")

        # Brainwave analysis
        brainwave_frame = tk.LabelFrame(analysis_frame, text="Brainwave Analysis", 
                                       font=('Arial', 14, 'bold'))
        brainwave_frame.pack(fill='x', padx=10, pady=10)

        self.brainwave_labels = {}
        brainwave_types = ['Delta (0.5-4 Hz)', 'Theta (4-8 Hz)', 'Alpha (8-13 Hz)', 'Beta (13-30 Hz)']
        
        for i, wave_type in enumerate(brainwave_types):
            frame = tk.Frame(brainwave_frame)
            frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(frame, text=wave_type, font=('Arial', 12)).pack(side='left')
            self.brainwave_labels[wave_type.split()[0].lower()] = tk.Label(frame, text="0.0", 
                                                                          font=('Arial', 12, 'bold'))
            self.brainwave_labels[wave_type.split()[0].lower()].pack(side='right')

        # Signal quality
        quality_frame = tk.LabelFrame(analysis_frame, text="Signal Quality", 
                                     font=('Arial', 14, 'bold'))
        quality_frame.pack(fill='x', padx=10, pady=10)

        self.signal_quality_label = tk.Label(quality_frame, text="Signal Quality: Good", 
                                           font=('Arial', 12))
        self.signal_quality_label.pack(pady=10)

    def create_wow_features_tab(self):
        """Create wow features tab"""
        wow_frame = ttk.Frame(self.notebook)
        self.notebook.add(wow_frame, text="✨ Wow Features")

        # Emergency Alert System
        emergency_frame = tk.LabelFrame(wow_frame, text="Emergency Alert System", 
                                       font=('Arial', 14, 'bold'))
        emergency_frame.pack(fill='x', padx=10, pady=10)

        self.emergency_status_label = tk.Label(emergency_frame, text="Status: Monitoring", 
                                             font=('Arial', 12))
        self.emergency_status_label.pack(pady=5)

        tk.Button(emergency_frame, text="Test Emergency Alert", 
                 command=self.test_emergency_alert).pack(pady=5)

        # Mindfulness Coach
        mindfulness_frame = tk.LabelFrame(wow_frame, text="Mindfulness Coach", 
                                         font=('Arial', 14, 'bold'))
        mindfulness_frame.pack(fill='x', padx=10, pady=10)

        self.mindfulness_status_label = tk.Label(mindfulness_frame, text="Status: Ready", 
                                                font=('Arial', 12))
        self.mindfulness_status_label.pack(pady=5)

        tk.Button(mindfulness_frame, text="Start Relaxation Session", 
                 command=self.start_relaxation_session).pack(pady=5)

        # Study Mode Tracker
        study_frame = tk.LabelFrame(wow_frame, text="Study Mode Tracker", 
                                   font=('Arial', 14, 'bold'))
        study_frame.pack(fill='x', padx=10, pady=10)

        study_buttons_frame = tk.Frame(study_frame)
        study_buttons_frame.pack(pady=5)

        tk.Button(study_buttons_frame, text="Start Study Session", 
                 command=self.start_study_session).pack(side='left', padx=5)
        tk.Button(study_buttons_frame, text="End Study Session", 
                 command=self.end_study_session).pack(side='left', padx=5)

        self.study_status_label = tk.Label(study_frame, text="Status: Not tracking", 
                                          font=('Arial', 12))
        self.study_status_label.pack(pady=5)

        # Game Controller
        game_frame = tk.LabelFrame(wow_frame, text="Brain Games", 
                                  font=('Arial', 14, 'bold'))
        game_frame.pack(fill='x', padx=10, pady=10)

        game_buttons_frame = tk.Frame(game_frame)
        game_buttons_frame.pack(pady=5)

        tk.Button(game_buttons_frame, text="Blink Game", 
                 command=lambda: self.start_brain_game("blink_clicker")).pack(side='left', padx=5)
        tk.Button(game_buttons_frame, text="Attention Game", 
                 command=lambda: self.start_brain_game("attention_trainer")).pack(side='left', padx=5)

        self.game_status_label = tk.Label(game_frame, text="Status: No game active", 
                                         font=('Arial', 12))
        self.game_status_label.pack(pady=5)

        # Weekly Report
        report_frame = tk.LabelFrame(wow_frame, text="Weekly Report", 
                                    font=('Arial', 14, 'bold'))
        report_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(report_frame, text="Generate Weekly Report", 
                 command=self.generate_weekly_report).pack(pady=5)

    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")

        # Connection settings
        conn_frame = tk.LabelFrame(settings_frame, text="Connection Settings", 
                                  font=('Arial', 14, 'bold'))
        conn_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(conn_frame, text="ESP32 IP Address:").pack(anchor='w', padx=10, pady=5)
        self.ip_entry = tk.Entry(conn_frame, width=20)
        self.ip_entry.pack(anchor='w', padx=10, pady=5)
        self.ip_entry.insert(0, "192.168.1.100")  # Default IP

        tk.Button(conn_frame, text="Reconnect", command=self.reconnect_websocket).pack(anchor='w', padx=10, pady=5)

        # Threshold settings
        threshold_frame = tk.LabelFrame(settings_frame, text="Detection Thresholds", 
                                       font=('Arial', 14, 'bold'))
        threshold_frame.pack(fill='x', padx=10, pady=10)

        # Blink threshold
        tk.Label(threshold_frame, text="Blink Detection Threshold:").pack(anchor='w', padx=10, pady=5)
        self.blink_threshold_var = tk.StringVar(value="2000")
        tk.Entry(threshold_frame, textvariable=self.blink_threshold_var, width=10).pack(anchor='w', padx=10, pady=5)

        tk.Button(threshold_frame, text="Apply Settings", command=self.apply_settings).pack(anchor='w', padx=10, pady=10)

    def connect_websocket(self):
        """Connect to ESP32 WebSocket"""
        esp32_ip = self.ip_entry.get() if hasattr(self, 'ip_entry') else "192.168.1.100"
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
            
            self.status_label.config(text="● Connecting...", fg='#f39c12')
            
        except Exception as e:
            self.status_label.config(text="● Connection Error", fg='#e74c3c')
            print(f"WebSocket connection error: {e}")

    def on_open(self, ws):
        """WebSocket connection opened"""
        self.is_connected = True
        self.root.after(0, lambda: self.status_label.config(text="● Connected", fg='#27ae60'))
        print("WebSocket connection opened")

    def on_message(self, ws, message):
        """Process incoming WebSocket message"""
        try:
            data = json.loads(message)
            timestamp = data.get("timestamp", time.time())
            eeg_value = data.get("eeg", 0)
            ecg_value = data.get("ecg", None)

            # Process signals
            signal_results = self.signal_processor.process_realtime_sample(eeg_value, ecg_value)
            
            # Update data buffers
            self.eeg_data.append(eeg_value)
            self.timestamps.append(timestamp)
            
            # Extract processed data
            emotion_analysis = signal_results.get('emotion_analysis', {})
            heart_rate = emotion_analysis.get('heart_rate', 0)
            stress_level = emotion_analysis.get('stress_level', 0)
            attention_level = signal_results.get('attention_level', 0)
            emotion = emotion_analysis.get('emotion', 'neutral')

            # Update data buffers for plotting
            self.heart_rate_data.append(heart_rate)
            self.stress_data.append(stress_level)
            self.attention_data.append(attention_level)

            # Store current values
            self.current_heart_rate = heart_rate
            self.current_stress = stress_level
            self.current_attention = attention_level
            self.current_emotion = emotion

            # Update GUI
            self.root.after(0, lambda: self.update_dashboard_values())

            # Process brain control
            control_results = self.brain_controller.process_brain_signals(signal_results)
            
            # Process wow features
            physiological_data = {
                'heart_rate': heart_rate,
                'stress_level': stress_level,
                'attention_level': attention_level,
                'emotion': emotion
            }
            
            wow_results = self.wow_features.process_all_features(signal_results, physiological_data)
            
            # Update control interface status
            self.root.after(0, lambda: self.update_control_status(control_results, signal_results))

        except json.JSONDecodeError:
            print(f"Received non-JSON message: {message}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def update_dashboard_values(self):
        """Update dashboard display values"""
        try:
            # Update vital signs
            self.hr_value_label.config(text=f"{self.current_heart_rate:.0f} BPM")
            self.stress_value_label.config(text=f"{self.current_stress:.0f}%")
            self.attention_value_label.config(text=f"{self.current_attention:.0f}%")
            self.emotion_value_label.config(text=self.current_emotion.title())

            # Update brainwave analysis if available
            if hasattr(self, 'brainwave_labels'):
                brainwaves = self.signal_processor.analyze_brainwaves()
                for wave_type, value in brainwaves.items():
                    if wave_type in self.brainwave_labels:
                        self.brainwave_labels[wave_type].config(text=f"{value:.2f}")

        except Exception as e:
            print(f"Error updating dashboard: {e}")

    def update_control_status(self, control_results, signal_results):
        """Update brain control interface status"""
        try:
            # Update blink count
            if signal_results.get('blink_detected', False):
                current_text = self.blink_count_label.cget("text")
                count = int(current_text.split(": ")[1]) + 1
                self.blink_count_label.config(text=f"Blinks detected: {count}")

            # Update cursor position
            cursor_pos = control_results.get('cursor_position', [0, 0])
            self.cursor_pos_label.config(text=f"Cursor position: ({cursor_pos[0]}, {cursor_pos[1]})")

            # Update alpha action
            actions = control_results.get('actions_executed', [])
            if 'alpha_action' in actions:
                self.alpha_action_label.config(text="Last action: Alpha state triggered")

        except Exception as e:
            print(f"Error updating control status: {e}")

    def update_plots(self):
        """Update real-time plots"""
        try:
            if len(self.eeg_data) > 10:  # Only plot if we have enough data
                # Clear previous plots
                self.ax1.clear()
                self.ax2.clear()
                self.ax3.clear()
                self.ax4.clear()

                # EEG Signal
                self.ax1.plot(list(self.eeg_data)[-100:], 'b-', linewidth=1)
                self.ax1.set_title('EEG Signal', fontsize=12, fontweight='bold')
                self.ax1.set_ylabel('Amplitude')
                self.ax1.grid(True, alpha=0.3)

                # Heart Rate
                if len(self.heart_rate_data) > 1:
                    self.ax2.plot(list(self.heart_rate_data), 'r-', linewidth=2)
                    self.ax2.set_title('Heart Rate', fontsize=12, fontweight='bold')
                    self.ax2.set_ylabel('BPM')
                    self.ax2.grid(True, alpha=0.3)

                # Stress Level
                if len(self.stress_data) > 1:
                    self.ax3.plot(list(self.stress_data), 'orange', linewidth=2)
                    self.ax3.set_title('Stress Level', fontsize=12, fontweight='bold')
                    self.ax3.set_ylabel('Stress %')
                    self.ax3.grid(True, alpha=0.3)

                # Attention Level
                if len(self.attention_data) > 1:
                    self.ax4.plot(list(self.attention_data), 'g-', linewidth=2)
                    self.ax4.set_title('Attention Level', fontsize=12, fontweight='bold')
                    self.ax4.set_ylabel('Attention %')
                    self.ax4.grid(True, alpha=0.3)

                # Refresh canvas
                self.canvas.draw()

        except Exception as e:
            print(f"Error updating plots: {e}")

        # Schedule next update
        self.root.after(1000, self.update_plots)  # Update every second

    def on_error(self, ws, error):
        """WebSocket error handler"""
        self.is_connected = False
        self.root.after(0, lambda: self.status_label.config(text="● Error", fg='#e74c3c'))
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """WebSocket close handler"""
        self.is_connected = False
        self.root.after(0, lambda: self.status_label.config(text="● Disconnected", fg='#e74c3c'))
        print(f"WebSocket closed: {close_status_code} - {close_msg}")
        
        # Attempt to reconnect after delay
        self.root.after(5000, self.connect_websocket)

    # Wow Features Methods
    def test_emergency_alert(self):
        """Test emergency alert system"""
        self.wow_features.emergency_system.trigger_emergency_alert(
            "Test alert triggered by user", 120, 85
        )
        self.emergency_status_label.config(text="Status: Test alert sent!")

    def start_relaxation_session(self):
        """Start mindfulness relaxation session"""
        self.wow_features.mindfulness_coach.launch_relaxation_session("deep_breathing")
        self.mindfulness_status_label.config(text="Status: Relaxation session active")

    def start_study_session(self):
        """Start study tracking session"""
        self.wow_features.study_tracker.start_study_session()
        self.study_status_label.config(text="Status: Tracking study session")

    def end_study_session(self):
        """End study tracking session"""
        metrics = self.wow_features.study_tracker.end_study_session()
        if metrics:
            self.study_status_label.config(text=f"Status: Session ended. Focus: {metrics['focus_efficiency']:.1f}%")
        else:
            self.study_status_label.config(text="Status: No active session")

    def start_brain_game(self, game_type):
        """Start brain-controlled game"""
        self.wow_features.game_controller.start_brain_game(game_type)
        self.game_status_label.config(text=f"Status: {game_type} active")

    def generate_weekly_report(self):
        """Generate weekly health report"""
        try:
            report_path = self.wow_features.report_generator.generate_report()
            if report_path:
                messagebox.showinfo("Report Generated", f"Weekly report saved as: {report_path}")
            else:
                messagebox.showwarning("Report Error", "Could not generate report. Check data availability.")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {e}")

    def reconnect_websocket(self):
        """Reconnect to WebSocket"""
        if self.ws:
            self.ws.close()
        self.connect_websocket()

    def apply_settings(self):
        """Apply threshold settings"""
        try:
            new_threshold = float(self.blink_threshold_var.get())
            self.signal_processor.blink_threshold = new_threshold
            messagebox.showinfo("Settings Applied", "Threshold settings updated successfully!")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for threshold.")

    def on_closing(self):
        """Handle application closing"""
        if self.ws:
            self.ws.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedNeuroBandApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

