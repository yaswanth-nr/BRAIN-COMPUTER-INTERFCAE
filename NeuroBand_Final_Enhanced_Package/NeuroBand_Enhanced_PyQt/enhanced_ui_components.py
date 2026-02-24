"""
Enhanced UI Components for NeuroBand PyQt Application
Advanced widgets with animations, 3D visualizations, and interactive elements
"""

import sys
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import QOpenGLWidget
import math

class AnimatedProgressRing(QWidget):
    """Animated circular progress ring with gradient colors"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(120, 120)
        self.value = 0
        self.max_value = 100
        self.ring_width = 12
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Colors for gradient
        self.start_color = QColor("#4ECDC4")
        self.end_color = QColor("#44A08D")
        
    def set_value(self, value):
        """Animate to new value"""
        self.animation.setStartValue(self.value)
        self.animation.setEndValue(value)
        self.animation.start()
        
    def paintEvent(self, event):
        """Custom paint event for the ring"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate dimensions
        rect = QRect(self.ring_width // 2, self.ring_width // 2,
                    self.width() - self.ring_width, self.height() - self.ring_width)
        
        # Background ring
        pen = QPen(QColor("#2D3748"), self.ring_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawArc(rect, 0, 360 * 16)
        
        # Progress ring
        gradient = QConicalGradient(rect.center(), -90)
        gradient.setColorAt(0, self.start_color)
        gradient.setColorAt(1, self.end_color)
        
        pen = QPen(QBrush(gradient), self.ring_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        # Draw arc based on value
        span_angle = int((self.value / self.max_value) * 360 * 16)
        painter.drawArc(rect, -90 * 16, span_angle)
        
        # Center text
        painter.setPen(QColor("#E2E8F0"))
        font = QFont("Arial", 16, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{int(self.value)}")

class Brain3DVisualization(QOpenGLWidget):
    """3D brain visualization showing activity patterns"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.brain_activity = np.zeros((10, 10, 10))
        self.rotation_angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rotation)
        self.timer.start(50)  # 20 FPS
        
    def initializeGL(self):
        """Initialize OpenGL"""
        self.gl_widget = gl.GLViewWidget()
        self.gl_widget.setCameraPosition(distance=30)
        
        # Create brain mesh
        self.create_brain_mesh()
        
    def create_brain_mesh(self):
        """Create 3D brain mesh"""
        # Simple brain-like shape using spheres
        self.brain_points = []
        for i in range(50):
            x = np.random.normal(0, 3)
            y = np.random.normal(0, 3)
            z = np.random.normal(0, 2)
            self.brain_points.append([x, y, z])
            
        self.brain_points = np.array(self.brain_points)
        
    def update_brain_activity(self, eeg_data, brainwaves):
        """Update brain activity visualization"""
        # Convert EEG data to activity patterns
        activity_level = abs(eeg_data) / 1000.0 if eeg_data else 0
        
        # Update activity based on brainwave data
        alpha_activity = brainwaves.get('alpha', 0)
        beta_activity = brainwaves.get('beta', 0)
        
        # Simulate activity patterns
        self.brain_activity = np.random.random((10, 10, 10)) * activity_level
        self.update()
        
    def update_rotation(self):
        """Update rotation animation"""
        self.rotation_angle += 1
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        self.update()
        
    def paintGL(self):
        """Paint the 3D brain"""
        # This would contain OpenGL rendering code
        # For now, we'll use a placeholder
        pass

class NeuralNetworkAnimation(QWidget):
    """Animated neural network visualization"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 200)
        self.nodes = []
        self.connections = []
        self.activity_levels = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_network)
        self.timer.start(100)
        
        self.init_network()
        
    def init_network(self):
        """Initialize neural network structure"""
        # Create nodes in layers
        layers = [4, 6, 4, 2]  # Input, hidden1, hidden2, output
        self.nodes = []
        
        layer_x_positions = [50, 120, 190, 260]
        
        for layer_idx, num_nodes in enumerate(layers):
            layer_nodes = []
            x = layer_x_positions[layer_idx]
            
            for node_idx in range(num_nodes):
                y = 30 + (node_idx * (140 / (num_nodes - 1))) if num_nodes > 1 else 100
                layer_nodes.append({'x': x, 'y': y, 'activity': 0})
                
            self.nodes.append(layer_nodes)
            
        # Create connections
        self.connections = []
        for layer_idx in range(len(self.nodes) - 1):
            for node1 in self.nodes[layer_idx]:
                for node2 in self.nodes[layer_idx + 1]:
                    self.connections.append({
                        'start': node1,
                        'end': node2,
                        'weight': np.random.random(),
                        'activity': 0
                    })
                    
    def update_activity(self, brain_signals):
        """Update network activity based on brain signals"""
        # Input layer gets brain signal data
        if len(self.nodes) > 0:
            attention = brain_signals.get('attention_level', 0) / 100.0
            stress = brain_signals.get('stress_level', 0) / 100.0
            alpha = brain_signals.get('brainwaves', {}).get('alpha', 0)
            beta = brain_signals.get('brainwaves', {}).get('beta', 0)
            
            inputs = [attention, stress, alpha, beta]
            
            for i, activity in enumerate(inputs):
                if i < len(self.nodes[0]):
                    self.nodes[0][i]['activity'] = activity
                    
        # Propagate activity through network
        for layer_idx in range(1, len(self.nodes)):
            for node in self.nodes[layer_idx]:
                node['activity'] = np.random.random() * 0.8  # Simplified propagation
                
    def animate_network(self):
        """Animate network activity"""
        # Add some random fluctuation
        for layer in self.nodes:
            for node in layer:
                node['activity'] += (np.random.random() - 0.5) * 0.1
                node['activity'] = max(0, min(1, node['activity']))
                
        self.update()
        
    def paintEvent(self, event):
        """Paint the neural network"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw connections
        for conn in self.connections:
            start = conn['start']
            end = conn['end']
            
            # Connection color based on activity
            activity = (start['activity'] + end['activity']) / 2
            color = QColor(int(66 * activity + 45), int(218 * activity + 45), int(243 * activity + 45))
            
            pen = QPen(color, 2)
            painter.setPen(pen)
            painter.drawLine(int(start['x']), int(start['y']), int(end['x']), int(end['y']))
            
        # Draw nodes
        for layer in self.nodes:
            for node in layer:
                # Node color based on activity
                activity = node['activity']
                color = QColor(int(255 * activity), int(255 * activity), int(255 * activity))
                
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(QColor("#4A5568"), 2))
                painter.drawEllipse(int(node['x'] - 8), int(node['y'] - 8), 16, 16)

class WaveformVisualizer(QWidget):
    """Advanced waveform visualizer with multiple channels"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 300)
        self.channels = {
            'EEG': {'data': [], 'color': '#66DAF3', 'offset': 50},
            'ECG': {'data': [], 'color': '#F6AD55', 'offset': 150},
            'Filtered': {'data': [], 'color': '#48BB78', 'offset': 250}
        }
        self.time_axis = []
        self.max_points = 200
        
    def add_data_point(self, channel, value):
        """Add new data point to channel"""
        if channel in self.channels:
            self.channels[channel]['data'].append(value)
            if len(self.channels[channel]['data']) > self.max_points:
                self.channels[channel]['data'].pop(0)
                
        # Update time axis
        if len(self.time_axis) >= self.max_points:
            self.time_axis.pop(0)
        self.time_axis.append(len(self.time_axis))
        
        self.update()
        
    def paintEvent(self, event):
        """Paint the waveforms"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor("#1A202C"))
        
        # Draw grid
        painter.setPen(QPen(QColor("#4A5568"), 1))
        for i in range(0, self.width(), 40):
            painter.drawLine(i, 0, i, self.height())
        for i in range(0, self.height(), 40):
            painter.drawLine(0, i, self.width(), i)
            
        # Draw waveforms
        for channel_name, channel_data in self.channels.items():
            if len(channel_data['data']) < 2:
                continue
                
            color = QColor(channel_data['color'])
            pen = QPen(color, 2)
            painter.setPen(pen)
            
            points = []
            for i, value in enumerate(channel_data['data']):
                x = int((i / len(channel_data['data'])) * self.width())
                y = int(channel_data['offset'] - (value * 0.1))  # Scale and offset
                points.append(QPoint(x, y))
                
            if len(points) > 1:
                for i in range(len(points) - 1):
                    painter.drawLine(points[i], points[i + 1])
                    
            # Channel label
            painter.setPen(QPen(color, 1))
            painter.drawText(10, channel_data['offset'] - 20, channel_name)

class InteractiveControlPanel(QWidget):
    """Interactive control panel with touch-like interface"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(350, 400)
        self.control_buttons = []
        self.slider_controls = []
        self.init_controls()
        
    def init_controls(self):
        """Initialize interactive controls"""
        layout = QVBoxLayout()
        
        # Mode selection buttons
        mode_group = QGroupBox("Control Mode")
        mode_layout = QHBoxLayout()
        
        modes = ["Focus", "Relax", "Game", "Sleep"]
        self.mode_buttons = []
        
        for mode in modes:
            btn = QPushButton(mode)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4A5568;
                    color: #E2E8F0;
                    border: none;
                    padding: 15px;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:checked {
                    background-color: #66DAF3;
                    color: #1A202C;
                }
                QPushButton:hover {
                    background-color: #5A6578;
                }
            """)
            self.mode_buttons.append(btn)
            mode_layout.addWidget(btn)
            
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # Sensitivity controls
        sensitivity_group = QGroupBox("Sensitivity Controls")
        sensitivity_layout = QVBoxLayout()
        
        controls = [
            ("Blink Sensitivity", 50),
            ("Attention Threshold", 70),
            ("Stress Alert Level", 80)
        ]
        
        for label, default_value in controls:
            control_layout = QHBoxLayout()
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: #E2E8F0; font-weight: bold;")
            
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(default_value)
            slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    border: 1px solid #4A5568;
                    height: 8px;
                    background: #2D3748;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #66DAF3;
                    border: 1px solid #66DAF3;
                    width: 18px;
                    margin: -5px 0;
                    border-radius: 9px;
                }
                QSlider::sub-page:horizontal {
                    background: #66DAF3;
                    border-radius: 4px;
                }
            """)
            
            value_label = QLabel(str(default_value))
            value_label.setFixedWidth(30)
            value_label.setStyleSheet("color: #66DAF3; font-weight: bold;")
            
            slider.valueChanged.connect(lambda v, lbl=value_label: lbl.setText(str(v)))
            
            control_layout.addWidget(label_widget)
            control_layout.addWidget(slider)
            control_layout.addWidget(value_label)
            
            sensitivity_layout.addLayout(control_layout)
            
        sensitivity_group.setLayout(sensitivity_layout)
        layout.addWidget(sensitivity_group)
        
        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QGridLayout()
        
        actions = [
            ("🎯 Calibrate", self.calibrate),
            ("📊 View Stats", self.view_stats),
            ("🔄 Reset", self.reset_system),
            ("💾 Save Profile", self.save_profile)
        ]
        
        for i, (text, callback) in enumerate(actions):
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4A5568;
                    color: #E2E8F0;
                    border: none;
                    padding: 12px;
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
            """)
            actions_layout.addWidget(btn, i // 2, i % 2)
            
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        self.setLayout(layout)
        
    def calibrate(self):
        """Start calibration process"""
        print("Starting calibration...")
        
    def view_stats(self):
        """View statistics"""
        print("Viewing statistics...")
        
    def reset_system(self):
        """Reset system"""
        print("Resetting system...")
        
    def save_profile(self):
        """Save user profile"""
        print("Saving profile...")

class StatusIndicatorWidget(QWidget):
    """Advanced status indicator with multiple states"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 80)
        self.status = "disconnected"  # disconnected, connecting, connected, error
        self.pulse_animation = QPropertyAnimation(self, b"pulse_value")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setLoopCount(-1)  # Infinite loop
        self.pulse_value = 0
        
        # Status colors
        self.status_colors = {
            'disconnected': '#FC8181',
            'connecting': '#F6AD55',
            'connected': '#48BB78',
            'error': '#E53E3E'
        }
        
    def set_status(self, status):
        """Set current status"""
        self.status = status
        
        if status == "connecting":
            self.start_pulse_animation()
        else:
            self.stop_pulse_animation()
            
        self.update()
        
    def start_pulse_animation(self):
        """Start pulsing animation"""
        self.pulse_animation.setStartValue(0)
        self.pulse_animation.setEndValue(1)
        self.pulse_animation.start()
        
    def stop_pulse_animation(self):
        """Stop pulsing animation"""
        self.pulse_animation.stop()
        self.pulse_value = 0
        
    def paintEvent(self, event):
        """Paint the status indicator"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor("#2D3748"))
        
        # Status circle
        center_x = 30
        center_y = self.height() // 2
        radius = 12
        
        color = QColor(self.status_colors[self.status])
        
        # Pulse effect for connecting state
        if self.status == "connecting":
            pulse_radius = radius + (self.pulse_value * 8)
            pulse_color = QColor(color)
            pulse_color.setAlpha(int(100 * (1 - self.pulse_value)))
            painter.setBrush(QBrush(pulse_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center_x - pulse_radius, center_y - pulse_radius,
                              pulse_radius * 2, pulse_radius * 2)
            
        # Main status circle
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
        
        # Status text
        painter.setPen(QPen(QColor("#E2E8F0")))
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        
        text_rect = QRect(60, 0, self.width() - 60, self.height())
        painter.drawText(text_rect, Qt.AlignVCenter, self.status.title())

class EnhancedDataVisualization(QWidget):
    """Enhanced data visualization with multiple chart types"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(500, 400)
        self.chart_type = "line"  # line, bar, polar, heatmap
        self.data_history = {
            'heart_rate': [],
            'stress': [],
            'attention': [],
            'brainwaves': {'alpha': [], 'beta': [], 'theta': [], 'delta': []}
        }
        
    def add_data(self, heart_rate, stress, attention, brainwaves):
        """Add new data point"""
        self.data_history['heart_rate'].append(heart_rate)
        self.data_history['stress'].append(stress)
        self.data_history['attention'].append(attention)
        
        for wave_type, power in brainwaves.items():
            if wave_type in self.data_history['brainwaves']:
                self.data_history['brainwaves'][wave_type].append(power)
                
        # Keep only last 100 points
        for key in self.data_history:
            if isinstance(self.data_history[key], list):
                if len(self.data_history[key]) > 100:
                    self.data_history[key] = self.data_history[key][-100:]
            elif isinstance(self.data_history[key], dict):
                for subkey in self.data_history[key]:
                    if len(self.data_history[key][subkey]) > 100:
                        self.data_history[key][subkey] = self.data_history[key][subkey][-100:]
                        
        self.update()
        
    def set_chart_type(self, chart_type):
        """Set visualization type"""
        self.chart_type = chart_type
        self.update()
        
    def paintEvent(self, event):
        """Paint the data visualization"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor("#1A202C"))
        
        if self.chart_type == "line":
            self.draw_line_chart(painter)
        elif self.chart_type == "bar":
            self.draw_bar_chart(painter)
        elif self.chart_type == "polar":
            self.draw_polar_chart(painter)
        elif self.chart_type == "heatmap":
            self.draw_heatmap(painter)
            
    def draw_line_chart(self, painter):
        """Draw line chart"""
        if not self.data_history['heart_rate']:
            return
            
        # Draw heart rate line
        painter.setPen(QPen(QColor("#F6AD55"), 2))
        points = []
        
        for i, value in enumerate(self.data_history['heart_rate']):
            x = int((i / len(self.data_history['heart_rate'])) * self.width())
            y = int(self.height() - (value / 150.0) * self.height())  # Scale for HR
            points.append(QPoint(x, y))
            
        if len(points) > 1:
            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i + 1])
                
    def draw_bar_chart(self, painter):
        """Draw bar chart for brainwaves"""
        brainwave_types = ['alpha', 'beta', 'theta', 'delta']
        colors = ['#66DAF3', '#F6AD55', '#48BB78', '#9F7AEA']
        
        bar_width = self.width() // len(brainwave_types)
        
        for i, wave_type in enumerate(brainwave_types):
            if wave_type in self.data_history['brainwaves'] and self.data_history['brainwaves'][wave_type]:
                value = self.data_history['brainwaves'][wave_type][-1]  # Latest value
                bar_height = int(value * self.height())
                
                color = QColor(colors[i])
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.NoPen)
                
                x = i * bar_width + 10
                y = self.height() - bar_height
                painter.drawRect(x, y, bar_width - 20, bar_height)
                
                # Label
                painter.setPen(QPen(QColor("#E2E8F0")))
                painter.drawText(x, self.height() - 5, wave_type.title())
                
    def draw_polar_chart(self, painter):
        """Draw polar chart for brainwave distribution"""
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(center_x, center_y) - 20
        
        brainwave_types = ['alpha', 'beta', 'theta', 'delta']
        colors = ['#66DAF3', '#F6AD55', '#48BB78', '#9F7AEA']
        
        angle_step = 360 / len(brainwave_types)
        
        for i, wave_type in enumerate(brainwave_types):
            if wave_type in self.data_history['brainwaves'] and self.data_history['brainwaves'][wave_type]:
                value = self.data_history['brainwaves'][wave_type][-1]  # Latest value
                
                angle = math.radians(i * angle_step)
                end_radius = radius * value
                
                end_x = center_x + end_radius * math.cos(angle)
                end_y = center_y + end_radius * math.sin(angle)
                
                color = QColor(colors[i])
                painter.setPen(QPen(color, 3))
                painter.drawLine(center_x, center_y, int(end_x), int(end_y))
                
                # Draw point at end
                painter.setBrush(QBrush(color))
                painter.drawEllipse(int(end_x - 5), int(end_y - 5), 10, 10)
                
    def draw_heatmap(self, painter):
        """Draw heatmap of recent activity"""
        # Simplified heatmap showing stress levels over time
        if not self.data_history['stress']:
            return
            
        cell_width = self.width() // 20
        cell_height = self.height() // 10
        
        for i in range(min(len(self.data_history['stress']), 200)):
            row = i // 20
            col = i % 20
            
            if row >= 10:
                break
                
            value = self.data_history['stress'][-(i+1)]  # Recent values
            intensity = int(value * 255 / 100)  # Scale to 0-255
            
            color = QColor(intensity, 0, 255 - intensity)  # Blue to red gradient
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            
            x = col * cell_width
            y = row * cell_height
            painter.drawRect(x, y, cell_width - 1, cell_height - 1)

