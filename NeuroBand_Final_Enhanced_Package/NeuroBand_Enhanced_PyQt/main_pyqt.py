import sys
import json
import time
import threading
import numpy as np
from collections import deque
from datetime import datetime

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QLabel, QPushButton, 
                             QFrame, QGridLayout, QLineEdit, QSlider, QProgressBar,
                             QTextEdit, QGroupBox, QComboBox, QSpinBox, QCheckBox)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QPainter, QBrush, QLinearGradient

import pyqtgraph as pg
import websocket

# Import our custom modules
from signal_processing import SignalProcessor
from brain_control import BrainControlInterface
from wow_features import WowFeaturesManager

class WebSocketThread(QThread):
    """Thread for handling WebSocket communication"""
    data_received = pyqtSignal(dict)
    connection_status = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.ws = None
        self.running = False
        
    def run(self):
        try:
            self.ws = websocket.WebSocketApp(
                self.url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.running = True
            self.ws.run_forever()
        except Exception as e:
            self.connection_status.emit(f"Error: {str(e)}")
            
    def on_open(self, ws):
        self.connection_status.emit("Connected")
        
    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            self.data_received.emit(data)
        except json.JSONDecodeError:
            pass
            
    def on_error(self, ws, error):
        self.connection_status.emit(f"Error: {str(error)}")
        
    def on_close(self, ws, close_status_code, close_msg):
        self.connection_status.emit("Disconnected")
        
    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()

class AnimatedLabel(QLabel):
    """Custom label with animation capabilities"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def animate_value_change(self):
        """Animate when value changes"""
        current_rect = self.geometry()
        self.animation.setStartValue(current_rect)
        end_rect = QRect(current_rect.x(), current_rect.y() - 5, 
                        current_rect.width(), current_rect.height())
        self.animation.setEndValue(end_rect)
        self.animation.finished.connect(self.reset_position)
        self.animation.start()
        
    def reset_position(self):
        current_rect = self.geometry()
        reset_rect = QRect(current_rect.x(), current_rect.y() + 5, 
                          current_rect.width(), current_rect.height())
        self.setGeometry(reset_rect)

class VitalSignWidget(QFrame):
    """Custom widget for displaying vital signs with animations"""
    def __init__(self, title, unit, color, parent=None):
        super().__init__(parent)
        self.title = title
        self.unit = unit
        self.color = color
        self.current_value = 0
        
        self.setFixedSize(200, 120)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 rgba(0,0,0,0.3));
                border-radius: 15px;
                border: 2px solid {color};
            }}
        """)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        
        # Value
        self.value_label = AnimatedLabel("--")
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("color: white; font-weight: bold; font-size: 24px;")
        
        # Unit
        unit_label = QLabel(unit)
        unit_label.setAlignment(Qt.AlignCenter)
        unit_label.setStyleSheet("color: white; font-size: 12px;")
        
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(unit_label)
        
        self.setLayout(layout)
        
    def update_value(self, value):
        if value != self.current_value:
            self.current_value = value
            self.value_label.setText(f"{value:.1f}")
            self.value_label.animate_value_change()

class BrainwaveWidget(QFrame):
    """Widget for displaying brainwave analysis"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 200)
        self.setStyleSheet("""
            QFrame {
                background-color: #2D3748;
                border-radius: 10px;
                border: 1px solid #4A5568;
            }
        """)
        
        layout = QVBoxLayout()
        
        title = QLabel("Brainwave Analysis")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #E2E8F0; font-weight: bold; font-size: 16px; margin: 10px;")
        
        # Brainwave bars
        self.bars_layout = QVBoxLayout()
        self.bars = {}
        
        brainwaves = [
            ("Delta", "#FF6B6B"),
            ("Theta", "#4ECDC4"), 
            ("Alpha", "#45B7D1"),
            ("Beta", "#96CEB4")
        ]
        
        for name, color in brainwaves:
            bar_layout = QHBoxLayout()
            
            label = QLabel(name)
            label.setFixedWidth(60)
            label.setStyleSheet("color: #E2E8F0; font-size: 12px;")
            
            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(0)
            progress.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #4A5568;
                    border-radius: 5px;
                    background-color: #1A202C;
                    text-align: center;
                    color: white;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 5px;
                }}
            """)
            
            self.bars[name.lower()] = progress
            
            bar_layout.addWidget(label)
            bar_layout.addWidget(progress)
            
            self.bars_layout.addLayout(bar_layout)
        
        layout.addWidget(title)
        layout.addLayout(self.bars_layout)
        self.setLayout(layout)
        
    def update_brainwaves(self, brainwave_data):
        for wave_type, value in brainwave_data.items():
            if wave_type in self.bars:
                # Normalize value to 0-100 range
                normalized_value = min(100, max(0, value * 10))
                self.bars[wave_type].setValue(int(normalized_value))

class EnhancedNeuroBandApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroBand - Enhanced Brain-Computer Interface")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize core components
        self.signal_processor = SignalProcessor()
        self.brain_controller = BrainControlInterface()
        self.wow_features = WowFeaturesManager()
        
        # WebSocket connection
        self.ws_thread = None
        self.is_connected = False
        
        # Data storage for real-time plotting
        self.eeg_data = deque(maxlen=500)
        self.heart_rate_data = deque(maxlen=100)
        self.stress_data = deque(maxlen=100)
        self.attention_data = deque(maxlen=100)
        self.timestamps = deque(maxlen=500)
        
        # Current values
        self.current_heart_rate = 0
        self.current_stress = 0
        self.current_attention = 0
        self.current_emotion = "neutral"
        
        # Setup UI
        self.setup_dark_theme()
        self.init_ui()
        self.setup_timers()
        
        # Connect to ESP32
        self.connect_websocket("192.168.1.100")  # Default IP
        
    def setup_dark_theme(self):
        """Setup dark theme for the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A202C;
                color: #E2E8F0;
            }
            QTabWidget::pane {
                border: 1px solid #4A5568;
                background-color: #2D3748;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #4A5568;
                color: #E2E8F0;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #66DAF3;
                color: #1A202C;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #5A6578;
            }
            QPushButton {
                background-color: #4A5568;
                color: #E2E8F0;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66DAF3;
                color: #1A202C;
            }
            QPushButton:pressed {
                background-color: #5A9FD4;
            }
            QLabel {
                color: #E2E8F0;
            }
            QLineEdit {
                background-color: #4A5568;
                color: #E2E8F0;
                border: 1px solid #66DAF3;
                padding: 8px;
                border-radius: 5px;
            }
            QGroupBox {
                color: #E2E8F0;
                font-weight: bold;
                border: 2px solid #4A5568;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Main content with tabs
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_brain_control_tab()
        self.create_signal_analysis_tab()
        self.create_wow_features_tab()
        self.create_settings_tab()
        
        layout.addWidget(self.tab_widget)
        central_widget.setLayout(layout)
        
    def create_header(self):
        """Create the application header"""
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2D3748, stop:1 #4A5568);
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Title
        title = QLabel("🧠 NeuroBand Control Center")
        title.setStyleSheet("color: #66DAF3; font-size: 24px; font-weight: bold; margin: 20px;")
        
        # Connection status
        self.status_label = QLabel("● Disconnected")
        self.status_label.setStyleSheet("color: #FC8181; font-size: 16px; font-weight: bold; margin: 20px;")
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status_label)
        
        header.setLayout(layout)
        return header
        
    def create_dashboard_tab(self):
        """Create the live dashboard tab"""
        dashboard = QWidget()
        layout = QHBoxLayout()
        
        # Left panel - Vital signs
        left_panel = QFrame()
        left_panel.setFixedWidth(450)
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #2D3748;
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        left_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Vital Signs")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #E2E8F0; font-size: 20px; font-weight: bold; margin: 20px;")
        left_layout.addWidget(title)
        
        # Vital sign widgets
        vital_signs_layout = QVBoxLayout()
        
        self.hr_widget = VitalSignWidget("❤️ Heart Rate", "BPM", "#F6AD55")
        self.stress_widget = VitalSignWidget("⚡ Stress Level", "%", "#FC8181")
        self.attention_widget = VitalSignWidget("🎯 Attention", "%", "#66DAF3")
        self.emotion_widget = VitalSignWidget("😊 Emotion", "", "#9F7AEA")
        
        vital_signs_layout.addWidget(self.hr_widget)
        vital_signs_layout.addWidget(self.stress_widget)
        vital_signs_layout.addWidget(self.attention_widget)
        vital_signs_layout.addWidget(self.emotion_widget)
        
        left_layout.addLayout(vital_signs_layout)
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        # Right panel - Graphs
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: #2D3748;
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        right_layout = QVBoxLayout()
        
        # Graph title
        graph_title = QLabel("Real-time Data Visualization")
        graph_title.setAlignment(Qt.AlignCenter)
        graph_title.setStyleSheet("color: #E2E8F0; font-size: 20px; font-weight: bold; margin: 20px;")
        right_layout.addWidget(graph_title)
        
        # Setup plots
        self.setup_plots(right_layout)
        
        # Brainwave widget
        self.brainwave_widget = BrainwaveWidget()
        right_layout.addWidget(self.brainwave_widget)
        
        right_panel.setLayout(right_layout)
        
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)
        dashboard.setLayout(layout)
        
        self.tab_widget.addTab(dashboard, "📊 Live Dashboard")
        
    def setup_plots(self, layout):
        """Setup real-time plots"""
        # Configure pyqtgraph
        pg.setConfigOption('background', '#1A202C')
        pg.setConfigOption('foreground', '#E2E8F0')
        
        # Create plot widgets
        plots_layout = QGridLayout()
        
        # EEG plot
        self.eeg_plot = pg.PlotWidget(title="EEG Signal")
        self.eeg_plot.setLabel('left', 'Amplitude')
        self.eeg_plot.setLabel('bottom', 'Time')
        self.eeg_curve = self.eeg_plot.plot(pen=pg.mkPen('#66DAF3', width=2))
        
        # Heart rate plot
        self.hr_plot = pg.PlotWidget(title="Heart Rate")
        self.hr_plot.setLabel('left', 'BPM')
        self.hr_plot.setLabel('bottom', 'Time')
        self.hr_curve = self.hr_plot.plot(pen=pg.mkPen('#F6AD55', width=2))
        
        # Stress plot
        self.stress_plot = pg.PlotWidget(title="Stress Level")
        self.stress_plot.setLabel('left', 'Stress %')
        self.stress_plot.setLabel('bottom', 'Time')
        self.stress_curve = self.stress_plot.plot(pen=pg.mkPen('#FC8181', width=2))
        
        # Attention plot
        self.attention_plot = pg.PlotWidget(title="Attention Level")
        self.attention_plot.setLabel('left', 'Attention %')
        self.attention_plot.setLabel('bottom', 'Time')
        self.attention_curve = self.attention_plot.plot(pen=pg.mkPen('#48BB78', width=2))
        
        plots_layout.addWidget(self.eeg_plot, 0, 0)
        plots_layout.addWidget(self.hr_plot, 0, 1)
        plots_layout.addWidget(self.stress_plot, 1, 0)
        plots_layout.addWidget(self.attention_plot, 1, 1)
        
        layout.addLayout(plots_layout)
        
    def create_brain_control_tab(self):
        """Create brain control interface tab"""
        control_widget = QWidget()
        layout = QVBoxLayout()
        
        # Status panel
        status_group = QGroupBox("Brain Control Status")
        status_layout = QVBoxLayout()
        
        self.control_status_label = QLabel("Status: Monitoring brain signals...")
        self.control_status_label.setStyleSheet("font-size: 14px; margin: 10px;")
        status_layout.addWidget(self.control_status_label)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Control panels
        controls_layout = QHBoxLayout()
        
        # Blink control
        blink_group = QGroupBox("👁️ Blink Control")
        blink_layout = QVBoxLayout()
        
        blink_info = QLabel("• Blink to perform mouse click")
        self.blink_count_label = QLabel("Blinks detected: 0")
        self.blink_count_label.setStyleSheet("font-weight: bold; color: #66DAF3;")
        
        blink_layout.addWidget(blink_info)
        blink_layout.addWidget(self.blink_count_label)
        blink_group.setLayout(blink_layout)
        
        # Attention control
        attention_group = QGroupBox("🎯 Attention Control")
        attention_layout = QVBoxLayout()
        
        attention_info = QLabel("• Focus to control cursor movement")
        self.cursor_pos_label = QLabel("Cursor position: (0, 0)")
        self.cursor_pos_label.setStyleSheet("font-weight: bold; color: #66DAF3;")
        
        attention_layout.addWidget(attention_info)
        attention_layout.addWidget(self.cursor_pos_label)
        attention_group.setLayout(attention_layout)
        
        # Alpha state control
        alpha_group = QGroupBox("🧘 Alpha State Control")
        alpha_layout = QVBoxLayout()
        
        alpha_info = QLabel("• Enter relaxed state to trigger actions")
        self.alpha_action_label = QLabel("Last action: None")
        self.alpha_action_label.setStyleSheet("font-weight: bold; color: #66DAF3;")
        
        alpha_layout.addWidget(alpha_info)
        alpha_layout.addWidget(self.alpha_action_label)
        alpha_group.setLayout(alpha_layout)
        
        controls_layout.addWidget(blink_group)
        controls_layout.addWidget(attention_group)
        controls_layout.addWidget(alpha_group)
        
        layout.addLayout(controls_layout)
        layout.addStretch()
        
        control_widget.setLayout(layout)
        self.tab_widget.addTab(control_widget, "🧠 Brain Control")
        
    def create_signal_analysis_tab(self):
        """Create signal analysis tab"""
        analysis_widget = QWidget()
        layout = QVBoxLayout()
        
        # Signal quality
        quality_group = QGroupBox("Signal Quality")
        quality_layout = QVBoxLayout()
        
        self.signal_quality_label = QLabel("Signal Quality: Good")
        self.signal_quality_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #48BB78;")
        quality_layout.addWidget(self.signal_quality_label)
        
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Advanced metrics
        metrics_group = QGroupBox("Advanced Metrics")
        metrics_layout = QGridLayout()
        
        # HRV
        hrv_label = QLabel("Heart Rate Variability:")
        self.hrv_value_label = QLabel("-- ms")
        self.hrv_value_label.setStyleSheet("font-weight: bold; color: #F6AD55;")
        
        # Attention score
        attention_score_label = QLabel("Attention Score:")
        self.attention_score_label = QLabel("-- / 100")
        self.attention_score_label.setStyleSheet("font-weight: bold; color: #66DAF3;")
        
        metrics_layout.addWidget(hrv_label, 0, 0)
        metrics_layout.addWidget(self.hrv_value_label, 0, 1)
        metrics_layout.addWidget(attention_score_label, 1, 0)
        metrics_layout.addWidget(self.attention_score_label, 1, 1)
        
        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)
        
        layout.addStretch()
        analysis_widget.setLayout(layout)
        
        self.tab_widget.addTab(analysis_widget, "📈 Signal Analysis")
        
    def create_wow_features_tab(self):
        """Create wow features tab"""
        wow_widget = QWidget()
        layout = QVBoxLayout()
        
        # Emergency Alert System
        emergency_group = QGroupBox("🚨 Emergency Alert System")
        emergency_layout = QVBoxLayout()
        
        self.emergency_status_label = QLabel("Status: Monitoring")
        self.emergency_status_label.setStyleSheet("font-weight: bold; color: #48BB78;")
        
        test_alert_btn = QPushButton("Test Emergency Alert")
        test_alert_btn.clicked.connect(self.test_emergency_alert)
        
        emergency_layout.addWidget(self.emergency_status_label)
        emergency_layout.addWidget(test_alert_btn)
        emergency_group.setLayout(emergency_layout)
        
        # Mindfulness Coach
        mindfulness_group = QGroupBox("🧘 Mindfulness Coach")
        mindfulness_layout = QVBoxLayout()
        
        self.mindfulness_status_label = QLabel("Status: Ready")
        self.mindfulness_status_label.setStyleSheet("font-weight: bold; color: #48BB78;")
        
        start_session_btn = QPushButton("Start Relaxation Session")
        start_session_btn.clicked.connect(self.start_relaxation_session)
        
        mindfulness_layout.addWidget(self.mindfulness_status_label)
        mindfulness_layout.addWidget(start_session_btn)
        mindfulness_group.setLayout(mindfulness_layout)
        
        # Study Mode Tracker
        study_group = QGroupBox("📚 Study Mode Tracker")
        study_layout = QVBoxLayout()
        
        study_buttons_layout = QHBoxLayout()
        start_study_btn = QPushButton("Start Study Session")
        end_study_btn = QPushButton("End Study Session")
        
        start_study_btn.clicked.connect(self.start_study_session)
        end_study_btn.clicked.connect(self.end_study_session)
        
        study_buttons_layout.addWidget(start_study_btn)
        study_buttons_layout.addWidget(end_study_btn)
        
        self.study_status_label = QLabel("Status: Not tracking")
        self.study_status_label.setStyleSheet("font-weight: bold; color: #A0AEC0;")
        
        study_layout.addLayout(study_buttons_layout)
        study_layout.addWidget(self.study_status_label)
        study_group.setLayout(study_layout)
        
        # Brain Games
        games_group = QGroupBox("🎮 Brain Games")
        games_layout = QVBoxLayout()
        
        games_buttons_layout = QHBoxLayout()
        blink_game_btn = QPushButton("Blink Game")
        attention_game_btn = QPushButton("Attention Game")
        
        blink_game_btn.clicked.connect(lambda: self.start_brain_game("blink_clicker"))
        attention_game_btn.clicked.connect(lambda: self.start_brain_game("attention_trainer"))
        
        games_buttons_layout.addWidget(blink_game_btn)
        games_buttons_layout.addWidget(attention_game_btn)
        
        self.game_status_label = QLabel("Status: No game active")
        self.game_status_label.setStyleSheet("font-weight: bold; color: #A0AEC0;")
        
        games_layout.addLayout(games_buttons_layout)
        games_layout.addWidget(self.game_status_label)
        games_group.setLayout(games_layout)
        
        # Weekly Report
        report_group = QGroupBox("📄 Weekly Report")
        report_layout = QVBoxLayout()
        
        generate_report_btn = QPushButton("Generate Weekly Report")
        generate_report_btn.clicked.connect(self.generate_weekly_report)
        
        report_layout.addWidget(generate_report_btn)
        report_group.setLayout(report_layout)
        
        # Add all groups
        features_layout = QGridLayout()
        features_layout.addWidget(emergency_group, 0, 0)
        features_layout.addWidget(mindfulness_group, 0, 1)
        features_layout.addWidget(study_group, 1, 0)
        features_layout.addWidget(games_group, 1, 1)
        
        layout.addLayout(features_layout)
        layout.addWidget(report_group)
        layout.addStretch()
        
        wow_widget.setLayout(layout)
        self.tab_widget.addTab(wow_widget, "✨ Wow Features")
        
    def create_settings_tab(self):
        """Create settings tab"""
        settings_widget = QWidget()
        layout = QVBoxLayout()
        
        # Connection settings
        conn_group = QGroupBox("Connection Settings")
        conn_layout = QVBoxLayout()
        
        ip_layout = QHBoxLayout()
        ip_label = QLabel("ESP32 IP Address:")
        self.ip_entry = QLineEdit("192.168.1.100")
        reconnect_btn = QPushButton("Reconnect")
        reconnect_btn.clicked.connect(self.reconnect_websocket)
        
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_entry)
        ip_layout.addWidget(reconnect_btn)
        
        conn_layout.addLayout(ip_layout)
        conn_group.setLayout(conn_layout)
        
        # Threshold settings
        threshold_group = QGroupBox("Detection Thresholds")
        threshold_layout = QVBoxLayout()
        
        blink_layout = QHBoxLayout()
        blink_label = QLabel("Blink Detection Threshold:")
        self.blink_threshold_slider = QSlider(Qt.Horizontal)
        self.blink_threshold_slider.setRange(500, 5000)
        self.blink_threshold_slider.setValue(2000)
        self.blink_threshold_value = QLabel("2000")
        
        self.blink_threshold_slider.valueChanged.connect(
            lambda v: self.blink_threshold_value.setText(str(v))
        )
        
        blink_layout.addWidget(blink_label)
        blink_layout.addWidget(self.blink_threshold_slider)
        blink_layout.addWidget(self.blink_threshold_value)
        
        apply_btn = QPushButton("Apply Settings")
        apply_btn.clicked.connect(self.apply_settings)
        
        threshold_layout.addLayout(blink_layout)
        threshold_layout.addWidget(apply_btn)
        threshold_group.setLayout(threshold_layout)
        
        layout.addWidget(conn_group)
        layout.addWidget(threshold_group)
        layout.addStretch()
        
        settings_widget.setLayout(layout)
        self.tab_widget.addTab(settings_widget, "⚙️ Settings")
        
    def setup_timers(self):
        """Setup update timers"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_plots)
        self.update_timer.start(100)  # Update every 100ms
        
    def connect_websocket(self, ip_address):
        """Connect to ESP32 WebSocket"""
        if self.ws_thread and self.ws_thread.isRunning():
            self.ws_thread.stop()
            self.ws_thread.wait()
            
        url = f"ws://{ip_address}:8080/ws"
        self.ws_thread = WebSocketThread(url)
        self.ws_thread.data_received.connect(self.on_data_received)
        self.ws_thread.connection_status.connect(self.on_connection_status)
        self.ws_thread.start()
        
    def on_connection_status(self, status):
        """Handle connection status updates"""
        if status == "Connected":
            self.status_label.setText("● Connected")
            self.status_label.setStyleSheet("color: #48BB78; font-size: 16px; font-weight: bold; margin: 20px;")
            self.is_connected = True
        elif status == "Disconnected":
            self.status_label.setText("● Disconnected")
            self.status_label.setStyleSheet("color: #FC8181; font-size: 16px; font-weight: bold; margin: 20px;")
            self.is_connected = False
        else:
            self.status_label.setText(f"● {status}")
            self.status_label.setStyleSheet("color: #F6AD55; font-size: 16px; font-weight: bold; margin: 20px;")
            
    def on_data_received(self, data):
        """Process incoming WebSocket data"""
        try:
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
            brainwaves = emotion_analysis.get('brainwaves', {})
            
            # Update data buffers for plotting
            self.heart_rate_data.append(heart_rate)
            self.stress_data.append(stress_level)
            self.attention_data.append(attention_level)
            
            # Store current values
            self.current_heart_rate = heart_rate
            self.current_stress = stress_level
            self.current_attention = attention_level
            self.current_emotion = emotion
            
            # Update vital signs widgets
            self.hr_widget.update_value(heart_rate)
            self.stress_widget.update_value(stress_level)
            self.attention_widget.update_value(attention_level)
            
            # Update emotion widget
            emotion_text = emotion.title()
            self.emotion_widget.value_label.setText(emotion_text)
            
            # Update brainwave widget
            if brainwaves:
                self.brainwave_widget.update_brainwaves(brainwaves)
            
            # Process brain control
            control_results = self.brain_controller.process_brain_signals(signal_results)
            self.update_control_status(control_results, signal_results)
            
            # Process wow features
            physiological_data = {
                'heart_rate': heart_rate,
                'stress_level': stress_level,
                'attention_level': attention_level,
                'emotion': emotion
            }
            
            wow_results = self.wow_features.process_all_features(signal_results, physiological_data)
            
            # Update advanced metrics
            hrv = emotion_analysis.get('hrv', 0)
            self.hrv_value_label.setText(f"{hrv:.1f} ms")
            self.attention_score_label.setText(f"{attention_level:.0f} / 100")
            
        except Exception as e:
            print(f"Error processing data: {e}")
            
    def update_control_status(self, control_results, signal_results):
        """Update brain control interface status"""
        try:
            # Update blink count
            if signal_results.get('blink_detected', False):
                current_text = self.blink_count_label.text()
                count = int(current_text.split(": ")[1]) + 1
                self.blink_count_label.setText(f"Blinks detected: {count}")
                
            # Update cursor position
            cursor_pos = control_results.get('cursor_position', [0, 0])
            self.cursor_pos_label.setText(f"Cursor position: ({cursor_pos[0]}, {cursor_pos[1]})")
            
            # Update alpha action
            actions = control_results.get('actions_executed', [])
            if 'alpha_action' in actions:
                self.alpha_action_label.setText("Last action: Alpha state triggered")
                
        except Exception as e:
            print(f"Error updating control status: {e}")
            
    def update_plots(self):
        """Update real-time plots"""
        try:
            if len(self.eeg_data) > 10:
                # Update EEG plot
                eeg_array = np.array(list(self.eeg_data)[-100:])
                self.eeg_curve.setData(eeg_array)
                
                # Update other plots
                if len(self.heart_rate_data) > 1:
                    hr_array = np.array(list(self.heart_rate_data))
                    self.hr_curve.setData(hr_array)
                    
                if len(self.stress_data) > 1:
                    stress_array = np.array(list(self.stress_data))
                    self.stress_curve.setData(stress_array)
                    
                if len(self.attention_data) > 1:
                    attention_array = np.array(list(self.attention_data))
                    self.attention_curve.setData(attention_array)
                    
        except Exception as e:
            print(f"Error updating plots: {e}")
            
    # Wow Features Methods
    def test_emergency_alert(self):
        """Test emergency alert system"""
        self.wow_features.emergency_system.trigger_emergency_alert(
            "Test alert triggered by user", 120, 85
        )
        self.emergency_status_label.setText("Status: Test alert sent!")
        self.emergency_status_label.setStyleSheet("font-weight: bold; color: #F6AD55;")
        
    def start_relaxation_session(self):
        """Start mindfulness relaxation session"""
        self.wow_features.mindfulness_coach.launch_relaxation_session("deep_breathing")
        self.mindfulness_status_label.setText("Status: Relaxation session active")
        self.mindfulness_status_label.setStyleSheet("font-weight: bold; color: #66DAF3;")
        
    def start_study_session(self):
        """Start study tracking session"""
        self.wow_features.study_tracker.start_study_session()
        self.study_status_label.setText("Status: Tracking study session")
        self.study_status_label.setStyleSheet("font-weight: bold; color: #48BB78;")
        
    def end_study_session(self):
        """End study tracking session"""
        metrics = self.wow_features.study_tracker.end_study_session()
        if metrics:
            self.study_status_label.setText(f"Status: Session ended. Focus: {metrics['focus_efficiency']:.1f}%")
            self.study_status_label.setStyleSheet("font-weight: bold; color: #66DAF3;")
        else:
            self.study_status_label.setText("Status: No active session")
            self.study_status_label.setStyleSheet("font-weight: bold; color: #A0AEC0;")
            
    def start_brain_game(self, game_type):
        """Start brain-controlled game"""
        self.wow_features.game_controller.start_brain_game(game_type)
        self.game_status_label.setText(f"Status: {game_type} active")
        self.game_status_label.setStyleSheet("font-weight: bold; color: #48BB78;")
        
    def generate_weekly_report(self):
        """Generate weekly health report"""
        try:
            report_path = self.wow_features.report_generator.generate_report()
            if report_path:
                self.status_label.setText(f"● Report generated: {report_path}")
            else:
                self.status_label.setText("● Report generation failed")
        except Exception as e:
            print(f"Error generating report: {e}")
            
    def reconnect_websocket(self):
        """Reconnect to WebSocket"""
        ip_address = self.ip_entry.text()
        self.connect_websocket(ip_address)
        
    def apply_settings(self):
        """Apply threshold settings"""
        try:
            new_threshold = self.blink_threshold_slider.value()
            self.signal_processor.blink_threshold = new_threshold
            self.status_label.setText("● Settings applied successfully")
        except Exception as e:
            print(f"Error applying settings: {e}")
            
    def closeEvent(self, event):
        """Handle application closing"""
        if self.ws_thread and self.ws_thread.isRunning():
            self.ws_thread.stop()
            self.ws_thread.wait()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better dark theme support
    
    window = EnhancedNeuroBandApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

