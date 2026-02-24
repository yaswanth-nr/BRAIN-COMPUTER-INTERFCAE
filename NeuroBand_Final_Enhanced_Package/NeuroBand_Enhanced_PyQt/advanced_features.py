"""
Advanced Features Module for NeuroBand
This module contains innovative new features that extend the capabilities of the NeuroBand system.
"""

import numpy as np
import time
import json
import threading
import sqlite3
import os
from datetime import datetime, timedelta
from collections import deque
import cv2
import speech_recognition as sr
import pyttsx3
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

class BiofeedbackTrainer:
    """Advanced biofeedback training system for brain state control"""
    
    def __init__(self):
        self.training_active = False
        self.target_state = "alpha"  # alpha, beta, theta, relaxed, focused
        self.training_data = []
        self.feedback_history = deque(maxlen=1000)
        self.success_rate = 0.0
        self.training_session_start = None
        
    def start_training_session(self, target_state="alpha", duration_minutes=10):
        """Start a biofeedback training session"""
        self.training_active = True
        self.target_state = target_state
        self.training_session_start = time.time()
        self.training_data = []
        
        print(f"Starting biofeedback training for {target_state} state")
        print(f"Session duration: {duration_minutes} minutes")
        
        # Start training thread
        training_thread = threading.Thread(
            target=self._run_training_session,
            args=(duration_minutes * 60,)
        )
        training_thread.daemon = True
        training_thread.start()
        
    def _run_training_session(self, duration_seconds):
        """Run the training session"""
        end_time = time.time() + duration_seconds
        
        while time.time() < end_time and self.training_active:
            # Provide feedback every 2 seconds
            time.sleep(2)
            
            if hasattr(self, 'current_brainwaves'):
                feedback = self._calculate_feedback(self.current_brainwaves)
                self.feedback_history.append(feedback)
                
                # Calculate success rate
                recent_feedback = list(self.feedback_history)[-20:]  # Last 40 seconds
                if recent_feedback:
                    self.success_rate = sum(f['success'] for f in recent_feedback) / len(recent_feedback)
                    
        self.training_active = False
        self._save_training_results()
        
    def _calculate_feedback(self, brainwaves):
        """Calculate feedback based on target state and current brainwaves"""
        feedback = {
            'timestamp': time.time(),
            'target_state': self.target_state,
            'success': False,
            'score': 0.0,
            'message': ""
        }
        
        if self.target_state == "alpha":
            alpha_power = brainwaves.get('alpha', 0)
            beta_power = brainwaves.get('beta', 0)
            
            # Success if alpha is dominant
            if alpha_power > beta_power and alpha_power > 0.3:
                feedback['success'] = True
                feedback['score'] = alpha_power
                feedback['message'] = "Great! You're in a relaxed alpha state!"
            else:
                feedback['message'] = "Try to relax and clear your mind..."
                
        elif self.target_state == "focused":
            beta_power = brainwaves.get('beta', 0)
            alpha_power = brainwaves.get('alpha', 0)
            
            # Success if beta is dominant
            if beta_power > alpha_power and beta_power > 0.4:
                feedback['success'] = True
                feedback['score'] = beta_power
                feedback['message'] = "Excellent focus! Keep concentrating!"
            else:
                feedback['message'] = "Focus your attention on a specific task..."
                
        return feedback
        
    def update_brainwaves(self, brainwaves):
        """Update current brainwave data"""
        self.current_brainwaves = brainwaves
        
    def _save_training_results(self):
        """Save training session results"""
        results = {
            'session_date': datetime.now().isoformat(),
            'target_state': self.target_state,
            'duration': time.time() - self.training_session_start,
            'success_rate': self.success_rate,
            'feedback_count': len(self.feedback_history)
        }
        
        # Save to file
        with open('biofeedback_training_log.json', 'a') as f:
            f.write(json.dumps(results) + '\n')

class SmartHomeController:
    """Control smart home devices using brain signals"""
    
    def __init__(self):
        self.connected_devices = {}
        self.device_states = {}
        self.control_mapping = {
            'blink_double': 'toggle_lights',
            'alpha_state': 'dim_lights',
            'high_stress': 'play_calming_music',
            'focused_state': 'set_work_mode'
        }
        
    def register_device(self, device_id, device_type, control_method="http"):
        """Register a smart home device"""
        self.connected_devices[device_id] = {
            'type': device_type,
            'control_method': control_method,
            'last_command': None
        }
        self.device_states[device_id] = {'power': False, 'brightness': 50}
        
    def process_brain_command(self, signal_type, signal_data):
        """Process brain signals and execute smart home commands"""
        if signal_type in self.control_mapping:
            command = self.control_mapping[signal_type]
            self._execute_command(command, signal_data)
            
    def _execute_command(self, command, data):
        """Execute smart home command"""
        if command == 'toggle_lights':
            self._toggle_lights()
        elif command == 'dim_lights':
            self._dim_lights(data.get('alpha_power', 0.5))
        elif command == 'play_calming_music':
            self._play_calming_music()
        elif command == 'set_work_mode':
            self._set_work_mode()
            
    def _toggle_lights(self):
        """Toggle smart lights"""
        for device_id, device in self.connected_devices.items():
            if device['type'] == 'light':
                current_state = self.device_states[device_id]['power']
                self.device_states[device_id]['power'] = not current_state
                print(f"Light {device_id}: {'ON' if not current_state else 'OFF'}")
                
    def _dim_lights(self, alpha_power):
        """Dim lights based on alpha wave power"""
        brightness = int(alpha_power * 100)
        for device_id, device in self.connected_devices.items():
            if device['type'] == 'light':
                self.device_states[device_id]['brightness'] = brightness
                print(f"Light {device_id} brightness: {brightness}%")
                
    def _play_calming_music(self):
        """Play calming music when stress is detected"""
        print("Playing calming music to reduce stress...")
        # Integration with Spotify, YouTube Music, etc.
        
    def _set_work_mode(self):
        """Set environment for focused work"""
        print("Setting work mode: optimal lighting and temperature...")

class PersonalizedMLModel:
    """Machine learning model that adapts to individual user patterns"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.training_data = []
        self.labels = []
        self.feature_names = ['heart_rate', 'stress_level', 'attention_level', 
                             'alpha_power', 'beta_power', 'theta_power', 'delta_power']
        
    def collect_training_data(self, biosignal_data, user_state_label):
        """Collect training data with user-provided labels"""
        features = [
            biosignal_data.get('heart_rate', 0),
            biosignal_data.get('stress_level', 0),
            biosignal_data.get('attention_level', 0),
            biosignal_data.get('brainwaves', {}).get('alpha', 0),
            biosignal_data.get('brainwaves', {}).get('beta', 0),
            biosignal_data.get('brainwaves', {}).get('theta', 0),
            biosignal_data.get('brainwaves', {}).get('delta', 0)
        ]
        
        self.training_data.append(features)
        self.labels.append(user_state_label)
        
        # Auto-train when we have enough data
        if len(self.training_data) >= 50 and len(self.training_data) % 10 == 0:
            self.train_model()
            
    def train_model(self):
        """Train the personalized model"""
        if len(self.training_data) < 10:
            return False
            
        X = np.array(self.training_data)
        y = np.array(self.labels)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Save model
        self._save_model()
        
        print(f"Model trained with {len(self.training_data)} samples")
        return True
        
    def predict_user_state(self, biosignal_data):
        """Predict user's current state using the trained model"""
        if not self.is_trained:
            return None
            
        features = [
            biosignal_data.get('heart_rate', 0),
            biosignal_data.get('stress_level', 0),
            biosignal_data.get('attention_level', 0),
            biosignal_data.get('brainwaves', {}).get('alpha', 0),
            biosignal_data.get('brainwaves', {}).get('beta', 0),
            biosignal_data.get('brainwaves', {}).get('theta', 0),
            biosignal_data.get('brainwaves', {}).get('delta', 0)
        ]
        
        X = np.array([features])
        X_scaled = self.scaler.transform(X)
        
        prediction = self.model.predict(X_scaled)[0]
        confidence = np.max(self.model.predict_proba(X_scaled))
        
        return {
            'predicted_state': prediction,
            'confidence': confidence
        }
        
    def _save_model(self):
        """Save the trained model"""
        joblib.dump(self.model, 'personalized_model.pkl')
        joblib.dump(self.scaler, 'personalized_scaler.pkl')
        
    def load_model(self):
        """Load a previously trained model"""
        try:
            self.model = joblib.load('personalized_model.pkl')
            self.scaler = joblib.load('personalized_scaler.pkl')
            self.is_trained = True
            return True
        except FileNotFoundError:
            return False

class VoiceCommandIntegration:
    """Integrate voice commands with brain control"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.listening = False
        self.voice_commands = {
            'start recording': self._start_recording,
            'stop recording': self._stop_recording,
            'calibrate blink': self._calibrate_blink,
            'emergency mode': self._emergency_mode,
            'relax mode': self._relax_mode,
            'focus mode': self._focus_mode
        }
        
    def start_listening(self):
        """Start listening for voice commands"""
        self.listening = True
        listen_thread = threading.Thread(target=self._listen_for_commands)
        listen_thread.daemon = True
        listen_thread.start()
        
    def _listen_for_commands(self):
        """Listen for voice commands in background"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
        while self.listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                # Recognize speech
                command = self.recognizer.recognize_google(audio).lower()
                
                # Process command
                if command in self.voice_commands:
                    self.voice_commands[command]()
                    self._speak(f"Executing {command}")
                    
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Voice recognition error: {e}")
                
    def _speak(self, text):
        """Text-to-speech output"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        
    def _start_recording(self):
        """Start recording biosignal data"""
        print("Starting data recording...")
        
    def _stop_recording(self):
        """Stop recording biosignal data"""
        print("Stopping data recording...")
        
    def _calibrate_blink(self):
        """Start blink calibration process"""
        print("Starting blink calibration...")
        
    def _emergency_mode(self):
        """Activate emergency mode"""
        print("Emergency mode activated!")
        
    def _relax_mode(self):
        """Activate relaxation mode"""
        print("Relaxation mode activated")
        
    def _focus_mode(self):
        """Activate focus mode"""
        print("Focus mode activated")

class SleepQualityMonitor:
    """Monitor sleep quality using EEG patterns"""
    
    def __init__(self):
        self.monitoring = False
        self.sleep_stages = []
        self.sleep_start_time = None
        self.current_stage = "awake"
        self.stage_history = deque(maxlen=1000)
        
    def start_sleep_monitoring(self):
        """Start monitoring sleep patterns"""
        self.monitoring = True
        self.sleep_start_time = time.time()
        self.sleep_stages = []
        
        monitor_thread = threading.Thread(target=self._monitor_sleep)
        monitor_thread.daemon = True
        monitor_thread.start()
        
    def _monitor_sleep(self):
        """Monitor sleep stages throughout the night"""
        while self.monitoring:
            time.sleep(30)  # Check every 30 seconds
            
            if hasattr(self, 'current_brainwaves'):
                stage = self._classify_sleep_stage(self.current_brainwaves)
                
                if stage != self.current_stage:
                    self.current_stage = stage
                    self.stage_history.append({
                        'timestamp': time.time(),
                        'stage': stage
                    })
                    
    def _classify_sleep_stage(self, brainwaves):
        """Classify current sleep stage based on brainwave patterns"""
        delta_power = brainwaves.get('delta', 0)
        theta_power = brainwaves.get('theta', 0)
        alpha_power = brainwaves.get('alpha', 0)
        beta_power = brainwaves.get('beta', 0)
        
        # Simplified sleep stage classification
        if beta_power > 0.4:
            return "awake"
        elif alpha_power > 0.3 and beta_power < 0.2:
            return "drowsy"
        elif theta_power > 0.3:
            return "light_sleep"
        elif delta_power > 0.4:
            return "deep_sleep"
        else:
            return "rem_sleep"
            
    def update_brainwaves(self, brainwaves):
        """Update current brainwave data"""
        self.current_brainwaves = brainwaves
        
    def generate_sleep_report(self):
        """Generate comprehensive sleep quality report"""
        if not self.stage_history:
            return None
            
        total_sleep_time = time.time() - self.sleep_start_time
        
        # Calculate time in each stage
        stage_durations = {}
        for i, stage_data in enumerate(self.stage_history):
            stage = stage_data['stage']
            if stage not in stage_durations:
                stage_durations[stage] = 0
                
            if i < len(self.stage_history) - 1:
                duration = self.stage_history[i + 1]['timestamp'] - stage_data['timestamp']
                stage_durations[stage] += duration
                
        # Calculate sleep efficiency
        sleep_time = sum(duration for stage, duration in stage_durations.items() 
                        if stage != "awake")
        sleep_efficiency = (sleep_time / total_sleep_time) * 100 if total_sleep_time > 0 else 0
        
        report = {
            'sleep_date': datetime.now().strftime('%Y-%m-%d'),
            'total_time_in_bed': total_sleep_time / 3600,  # hours
            'total_sleep_time': sleep_time / 3600,  # hours
            'sleep_efficiency': sleep_efficiency,
            'stage_durations': {stage: duration / 3600 for stage, duration in stage_durations.items()},
            'sleep_quality_score': self._calculate_sleep_quality_score(stage_durations, sleep_efficiency)
        }
        
        return report
        
    def _calculate_sleep_quality_score(self, stage_durations, sleep_efficiency):
        """Calculate overall sleep quality score (0-100)"""
        score = 0
        
        # Sleep efficiency component (40% of score)
        score += (sleep_efficiency / 100) * 40
        
        # Deep sleep component (30% of score)
        deep_sleep_ratio = stage_durations.get('deep_sleep', 0) / sum(stage_durations.values())
        score += min(deep_sleep_ratio * 5, 1) * 30  # Optimal deep sleep is ~20%
        
        # REM sleep component (20% of score)
        rem_sleep_ratio = stage_durations.get('rem_sleep', 0) / sum(stage_durations.values())
        score += min(rem_sleep_ratio * 4, 1) * 20  # Optimal REM sleep is ~25%
        
        # Sleep continuity (10% of score)
        # Fewer stage transitions indicate better sleep continuity
        transitions = len(self.stage_history)
        continuity_score = max(0, 1 - (transitions / 100)) * 10
        score += continuity_score
        
        return min(100, score)

class AdvancedFeaturesManager:
    """Manager class for all advanced features"""
    
    def __init__(self):
        self.biofeedback_trainer = BiofeedbackTrainer()
        self.smart_home_controller = SmartHomeController()
        self.ml_model = PersonalizedMLModel()
        self.voice_integration = VoiceCommandIntegration()
        self.sleep_monitor = SleepQualityMonitor()
        
        # Load existing ML model if available
        self.ml_model.load_model()
        
    def process_advanced_features(self, signal_data, physiological_data):
        """Process all advanced features with current data"""
        results = {}
        
        # Update biofeedback trainer
        if self.biofeedback_trainer.training_active:
            brainwaves = physiological_data.get('brainwaves', {})
            self.biofeedback_trainer.update_brainwaves(brainwaves)
            
        # Process smart home commands
        if signal_data.get('blink_detected'):
            self.smart_home_controller.process_brain_command('blink_double', signal_data)
            
        if signal_data.get('alpha_state'):
            self.smart_home_controller.process_brain_command('alpha_state', physiological_data)
            
        # Collect ML training data (when user provides labels)
        if hasattr(self, 'current_user_label') and self.current_user_label:
            self.ml_model.collect_training_data(physiological_data, self.current_user_label)
            self.current_user_label = None
            
        # Get ML prediction
        if self.ml_model.is_trained:
            prediction = self.ml_model.predict_user_state(physiological_data)
            results['ml_prediction'] = prediction
            
        # Update sleep monitor
        if self.sleep_monitor.monitoring:
            brainwaves = physiological_data.get('brainwaves', {})
            self.sleep_monitor.update_brainwaves(brainwaves)
            
        return results
        
    def set_user_state_label(self, label):
        """Set current user state label for ML training"""
        self.current_user_label = label
        
    def start_voice_commands(self):
        """Start voice command integration"""
        self.voice_integration.start_listening()
        
    def register_smart_device(self, device_id, device_type):
        """Register a new smart home device"""
        self.smart_home_controller.register_device(device_id, device_type)

