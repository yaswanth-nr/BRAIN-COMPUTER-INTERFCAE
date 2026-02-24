import numpy as np
from scipy import signal
from collections import deque
import time

class SignalProcessor:
    def __init__(self, sampling_rate=100):
        self.sampling_rate = sampling_rate
        self.buffer_size = sampling_rate * 5  # 5 seconds buffer
        self.eeg_buffer = deque(maxlen=self.buffer_size)
        self.ecg_buffer = deque(maxlen=self.buffer_size)
        
        # Blink detection parameters
        self.blink_threshold = 2000
        self.last_blink_time = 0
        self.blink_cooldown = 0.5  # seconds
        
        # Heart rate parameters
        self.heart_rate = 0
        self.last_hr_calculation = 0
        
        # Emotion/stress parameters
        self.stress_level = 0
        self.emotion_state = "neutral"
        
    def add_eeg_sample(self, value):
        """Add new EEG sample to buffer"""
        self.eeg_buffer.append(value)
        
    def add_ecg_sample(self, value):
        """Add new ECG sample to buffer"""
        self.ecg_buffer.append(value)
        
    def detect_blink(self):
        """Simple blink detection based on threshold crossing"""
        if len(self.eeg_buffer) < 10:
            return False
            
        current_time = time.time()
        if current_time - self.last_blink_time < self.blink_cooldown:
            return False
            
        recent_values = list(self.eeg_buffer)[-10:]
        current_value = recent_values[-1]
        
        # Check if current value crosses threshold and previous values were below
        if current_value > self.blink_threshold:
            avg_previous = np.mean(recent_values[:-1])
            if avg_previous < self.blink_threshold * 0.8:
                self.last_blink_time = current_time
                return True
        return False
        
    def calculate_heart_rate(self):
        """Calculate heart rate from ECG buffer"""
        if len(self.ecg_buffer) < self.sampling_rate * 2:  # Need at least 2 seconds
            return self.heart_rate
            
        current_time = time.time()
        if current_time - self.last_hr_calculation < 1.0:  # Update every second
            return self.heart_rate
            
        # Convert buffer to numpy array
        ecg_data = np.array(list(self.ecg_buffer))
        
        # Simple peak detection for R-waves
        peaks, _ = signal.find_peaks(ecg_data, height=np.mean(ecg_data) + np.std(ecg_data))
        
        if len(peaks) > 1:
            # Calculate intervals between peaks
            intervals = np.diff(peaks) / self.sampling_rate  # Convert to seconds
            if len(intervals) > 0:
                avg_interval = np.mean(intervals)
                self.heart_rate = 60 / avg_interval  # Convert to BPM
                
        self.last_hr_calculation = current_time
        return self.heart_rate
        
    def calculate_hrv(self):
        """Calculate Heart Rate Variability"""
        if len(self.ecg_buffer) < self.sampling_rate * 5:  # Need at least 5 seconds
            return 0
            
        ecg_data = np.array(list(self.ecg_buffer))
        peaks, _ = signal.find_peaks(ecg_data, height=np.mean(ecg_data) + np.std(ecg_data))
        
        if len(peaks) > 2:
            intervals = np.diff(peaks) / self.sampling_rate
            hrv = np.std(intervals) * 1000  # RMSSD in milliseconds
            return hrv
        return 0
        
    def analyze_brainwaves(self):
        """Analyze EEG for different brainwave bands"""
        if len(self.eeg_buffer) < self.sampling_rate * 2:
            return {"alpha": 0, "beta": 0, "theta": 0, "delta": 0}
            
        eeg_data = np.array(list(self.eeg_buffer))
        
        # Apply FFT
        freqs = np.fft.fftfreq(len(eeg_data), 1/self.sampling_rate)
        fft_values = np.abs(np.fft.fft(eeg_data))
        
        # Define frequency bands
        delta_band = (0.5, 4)    # Deep sleep
        theta_band = (4, 8)      # Drowsiness, meditation
        alpha_band = (8, 13)     # Relaxed, eyes closed
        beta_band = (13, 30)     # Alert, focused
        
        def get_band_power(freq_range):
            mask = (freqs >= freq_range[0]) & (freqs <= freq_range[1])
            return np.mean(fft_values[mask])
            
        return {
            "delta": get_band_power(delta_band),
            "theta": get_band_power(theta_band),
            "alpha": get_band_power(alpha_band),
            "beta": get_band_power(beta_band)
        }
        
    def detect_emotion_stress(self):
        """Detect emotion and stress level based on combined signals"""
        brainwaves = self.analyze_brainwaves()
        hrv = self.calculate_hrv()
        hr = self.calculate_heart_rate()
        
        # Simple stress detection algorithm
        # High beta waves + high heart rate + low HRV = stressed
        stress_score = 0
        
        if brainwaves["beta"] > brainwaves["alpha"] * 1.5:
            stress_score += 30
            
        if hr > 80:  # Assuming resting HR should be lower
            stress_score += 25
            
        if hrv < 30:  # Low HRV indicates stress
            stress_score += 25
            
        # High alpha waves indicate relaxation
        if brainwaves["alpha"] > brainwaves["beta"]:
            stress_score -= 20
            
        self.stress_level = max(0, min(100, stress_score))
        
        # Determine emotion state
        if self.stress_level > 70:
            self.emotion_state = "stressed"
        elif self.stress_level < 30 and brainwaves["alpha"] > brainwaves["beta"]:
            self.emotion_state = "relaxed"
        elif brainwaves["beta"] > brainwaves["alpha"]:
            self.emotion_state = "focused"
        else:
            self.emotion_state = "neutral"
            
        return {
            "stress_level": self.stress_level,
            "emotion": self.emotion_state,
            "heart_rate": hr,
            "hrv": hrv,
            "brainwaves": brainwaves
        }
        
    def get_attention_level(self):
        """Calculate attention level based on beta/alpha ratio"""
        brainwaves = self.analyze_brainwaves()
        
        if brainwaves["alpha"] == 0:
            return 50  # Default neutral attention
            
        attention_ratio = brainwaves["beta"] / brainwaves["alpha"]
        
        # Normalize to 0-100 scale
        attention_level = min(100, max(0, attention_ratio * 25))
        return attention_level
        
    def is_in_alpha_state(self):
        """Check if user is in alpha brainwave state"""
        brainwaves = self.analyze_brainwaves()
        return brainwaves["alpha"] > brainwaves["beta"] * 1.2
        
    def process_realtime_sample(self, eeg_value, ecg_value=None):
        """Process a single sample and return analysis results"""
        self.add_eeg_sample(eeg_value)
        if ecg_value is not None:
            self.add_ecg_sample(ecg_value)
            
        results = {
            "blink_detected": self.detect_blink(),
            "attention_level": self.get_attention_level(),
            "alpha_state": self.is_in_alpha_state(),
            "emotion_analysis": self.detect_emotion_stress()
        }
        
        return results

