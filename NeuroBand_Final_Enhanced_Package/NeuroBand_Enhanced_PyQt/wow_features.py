import smtplib
import threading
import time
import json
import os
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import pygame
import random

class EmergencyAlertSystem:
    def __init__(self):
        self.alert_active = False
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': 'your_email@gmail.com',
            'password': 'your_app_password',
            'emergency_contacts': ['emergency1@gmail.com', 'emergency2@gmail.com']
        }
        
    def check_emergency_conditions(self, heart_rate, stress_level):
        """Check if emergency conditions are met"""
        emergency_triggered = False
        alert_message = ""
        
        # High heart rate alert
        if heart_rate > 120:  # Adjust threshold as needed
            emergency_triggered = True
            alert_message += f"High heart rate detected: {heart_rate} BPM. "
            
        # High stress level alert
        if stress_level > 85:
            emergency_triggered = True
            alert_message += f"Extreme stress level detected: {stress_level}%. "
            
        if emergency_triggered and not self.alert_active:
            self.trigger_emergency_alert(alert_message, heart_rate, stress_level)
            
        return emergency_triggered
        
    def trigger_emergency_alert(self, message, heart_rate, stress_level):
        """Trigger emergency alert with multiple notification methods"""
        self.alert_active = True
        
        # Start alert thread to avoid blocking main application
        alert_thread = threading.Thread(
            target=self._execute_emergency_alert,
            args=(message, heart_rate, stress_level)
        )
        alert_thread.daemon = True
        alert_thread.start()
        
    def _execute_emergency_alert(self, message, heart_rate, stress_level):
        """Execute emergency alert procedures"""
        try:
            # 1. Send email alerts
            self.send_email_alert(message, heart_rate, stress_level)
            
            # 2. Display on-screen alert (would be integrated with main GUI)
            print(f"🚨 EMERGENCY ALERT: {message}")
            
            # 3. Text-to-speech warning (requires pyttsx3)
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(f"Emergency alert. {message}")
                engine.runAndWait()
            except ImportError:
                print("Text-to-speech not available. Install pyttsx3 for audio alerts.")
                
            # 4. Log emergency event
            self.log_emergency_event(message, heart_rate, stress_level)
            
            # Reset alert after cooldown period
            time.sleep(300)  # 5 minutes cooldown
            self.alert_active = False
            
        except Exception as e:
            print(f"Error executing emergency alert: {e}")
            self.alert_active = False
            
    def send_email_alert(self, message, heart_rate, stress_level):
        """Send email alert to emergency contacts"""
        try:
            msg = MimeMultipart()
            msg['From'] = self.email_config['email']
            msg['Subject'] = "NeuroBand Emergency Alert"
            
            body = f"""
            EMERGENCY ALERT FROM NEUROBAND DEVICE
            
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Alert: {message}
            Heart Rate: {heart_rate} BPM
            Stress Level: {stress_level}%
            
            Please check on the device user immediately.
            
            This is an automated message from NeuroBand health monitoring system.
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['email'], self.email_config['password'])
            
            for contact in self.email_config['emergency_contacts']:
                msg['To'] = contact
                server.send_message(msg)
                print(f"Emergency email sent to {contact}")
                
            server.quit()
            
        except Exception as e:
            print(f"Error sending emergency email: {e}")
            
    def log_emergency_event(self, message, heart_rate, stress_level):
        """Log emergency event to file"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'message': message,
                'heart_rate': heart_rate,
                'stress_level': stress_level
            }
            
            with open('emergency_log.json', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Error logging emergency event: {e}")

class MindfulnessCoach:
    def __init__(self):
        self.session_active = False
        self.relaxation_techniques = [
            "deep_breathing",
            "progressive_muscle_relaxation",
            "guided_meditation",
            "nature_sounds"
        ]
        
    def detect_stress_and_launch_session(self, stress_level):
        """Detect stress and automatically launch relaxation session"""
        if stress_level > 70 and not self.session_active:
            technique = random.choice(self.relaxation_techniques)
            self.launch_relaxation_session(technique)
            return True
        return False
        
    def launch_relaxation_session(self, technique):
        """Launch specific relaxation technique"""
        self.session_active = True
        
        session_thread = threading.Thread(
            target=self._execute_relaxation_session,
            args=(technique,)
        )
        session_thread.daemon = True
        session_thread.start()
        
    def _execute_relaxation_session(self, technique):
        """Execute relaxation session"""
        try:
            print(f"🧘 Starting {technique} session...")
            
            if technique == "deep_breathing":
                self.deep_breathing_exercise()
            elif technique == "progressive_muscle_relaxation":
                self.progressive_muscle_relaxation()
            elif technique == "guided_meditation":
                self.guided_meditation()
            elif technique == "nature_sounds":
                self.play_nature_sounds()
                
            self.session_active = False
            print("Relaxation session completed.")
            
        except Exception as e:
            print(f"Error in relaxation session: {e}")
            self.session_active = False
            
    def deep_breathing_exercise(self):
        """Guide user through deep breathing exercise"""
        cycles = 5
        for i in range(cycles):
            print(f"Breathe in slowly... (Cycle {i+1}/{cycles})")
            time.sleep(4)
            print("Hold...")
            time.sleep(2)
            print("Breathe out slowly...")
            time.sleep(6)
            time.sleep(2)  # Pause between cycles
            
    def progressive_muscle_relaxation(self):
        """Guide user through progressive muscle relaxation"""
        muscle_groups = [
            "feet and calves",
            "thighs and glutes",
            "hands and arms",
            "abdomen",
            "chest and shoulders",
            "neck and face"
        ]
        
        for group in muscle_groups:
            print(f"Tense your {group} for 5 seconds...")
            time.sleep(5)
            print(f"Release and relax your {group}...")
            time.sleep(10)
            
    def guided_meditation(self):
        """Simple guided meditation"""
        meditation_script = [
            "Close your eyes and find a comfortable position...",
            "Focus on your breathing, in and out...",
            "Notice any tension in your body and let it go...",
            "Bring your attention to the present moment...",
            "Let thoughts come and go without judgment...",
            "Feel yourself becoming more relaxed with each breath..."
        ]
        
        for instruction in meditation_script:
            print(instruction)
            time.sleep(30)  # 30 seconds per instruction
            
    def play_nature_sounds(self):
        """Play calming nature sounds (placeholder)"""
        print("🌊 Playing calming ocean sounds...")
        # In a real implementation, you would play actual audio files
        time.sleep(300)  # 5 minutes of nature sounds

class StudyModeTracker:
    def __init__(self):
        self.tracking_active = False
        self.session_data = []
        self.current_session = None
        
    def start_study_session(self):
        """Start tracking a study session"""
        self.tracking_active = True
        self.current_session = {
            'start_time': datetime.now(),
            'attention_logs': [],
            'distraction_count': 0,
            'focus_periods': []
        }
        print("📚 Study session started. Tracking focus levels...")
        
    def log_attention_level(self, attention_level):
        """Log attention level every 5 minutes"""
        if not self.tracking_active:
            return
            
        timestamp = datetime.now()
        self.current_session['attention_logs'].append({
            'timestamp': timestamp,
            'attention_level': attention_level
        })
        
        # Check for distraction (low attention)
        if attention_level < 30:
            self.current_session['distraction_count'] += 1
            print(f"⚠️ Distraction detected at {timestamp.strftime('%H:%M:%S')}")
        elif attention_level > 70:
            print(f"✅ High focus detected at {timestamp.strftime('%H:%M:%S')}")
            
    def end_study_session(self):
        """End study session and calculate metrics"""
        if not self.tracking_active or not self.current_session:
            return None
            
        self.tracking_active = False
        self.current_session['end_time'] = datetime.now()
        
        # Calculate session metrics
        metrics = self.calculate_session_metrics()
        self.current_session['metrics'] = metrics
        
        # Save session data
        self.session_data.append(self.current_session)
        
        print(f"📊 Study session ended. Focus efficiency: {metrics['focus_efficiency']:.1f}%")
        return metrics
        
    def calculate_session_metrics(self):
        """Calculate focus efficiency and other metrics"""
        if not self.current_session['attention_logs']:
            return {'focus_efficiency': 0}
            
        attention_levels = [log['attention_level'] for log in self.current_session['attention_logs']]
        
        avg_attention = np.mean(attention_levels)
        focus_time = sum(1 for level in attention_levels if level > 60)
        total_time = len(attention_levels)
        
        focus_efficiency = (focus_time / total_time * 100) if total_time > 0 else 0
        
        return {
            'focus_efficiency': focus_efficiency,
            'average_attention': avg_attention,
            'distraction_count': self.current_session['distraction_count'],
            'total_duration': (self.current_session['end_time'] - self.current_session['start_time']).total_seconds() / 60
        }

class WeeklyReportGenerator:
    def __init__(self):
        self.data_file = 'neuroband_data.json'
        
    def collect_weekly_data(self):
        """Collect data from the past week"""
        try:
            if not os.path.exists(self.data_file):
                return None
                
            with open(self.data_file, 'r') as f:
                all_data = [json.loads(line) for line in f]
                
            # Filter data from past week
            week_ago = datetime.now() - timedelta(days=7)
            weekly_data = [
                data for data in all_data 
                if datetime.fromisoformat(data['timestamp']) > week_ago
            ]
            
            return weekly_data
            
        except Exception as e:
            print(f"Error collecting weekly data: {e}")
            return None
            
    def generate_report(self):
        """Generate comprehensive weekly report"""
        weekly_data = self.collect_weekly_data()
        if not weekly_data:
            print("No data available for weekly report")
            return None
            
        try:
            # Calculate weekly statistics
            stats = self.calculate_weekly_stats(weekly_data)
            
            # Generate visualizations
            self.create_visualizations(weekly_data, stats)
            
            # Create PDF report
            pdf_path = self.create_pdf_report(stats)
            
            print(f"📄 Weekly report generated: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            print(f"Error generating weekly report: {e}")
            return None
            
    def calculate_weekly_stats(self, data):
        """Calculate weekly statistics"""
        heart_rates = [d['heart_rate'] for d in data if 'heart_rate' in d]
        stress_levels = [d['stress_level'] for d in data if 'stress_level' in d]
        attention_levels = [d['attention_level'] for d in data if 'attention_level' in d]
        
        return {
            'avg_heart_rate': np.mean(heart_rates) if heart_rates else 0,
            'avg_stress_level': np.mean(stress_levels) if stress_levels else 0,
            'avg_attention_level': np.mean(attention_levels) if attention_levels else 0,
            'max_heart_rate': max(heart_rates) if heart_rates else 0,
            'min_heart_rate': min(heart_rates) if heart_rates else 0,
            'stress_episodes': len([s for s in stress_levels if s > 70]),
            'high_focus_periods': len([a for a in attention_levels if a > 80]),
            'total_data_points': len(data)
        }
        
    def create_visualizations(self, data, stats):
        """Create visualization charts"""
        try:
            # Heart rate over time
            plt.figure(figsize=(12, 8))
            
            plt.subplot(2, 2, 1)
            timestamps = [datetime.fromisoformat(d['timestamp']) for d in data if 'heart_rate' in d]
            heart_rates = [d['heart_rate'] for d in data if 'heart_rate' in d]
            plt.plot(timestamps, heart_rates, 'r-', linewidth=2)
            plt.title('Heart Rate Over Time')
            plt.ylabel('BPM')
            plt.xticks(rotation=45)
            
            # Stress levels
            plt.subplot(2, 2, 2)
            stress_timestamps = [datetime.fromisoformat(d['timestamp']) for d in data if 'stress_level' in d]
            stress_levels = [d['stress_level'] for d in data if 'stress_level' in d]
            plt.plot(stress_timestamps, stress_levels, 'orange', linewidth=2)
            plt.title('Stress Levels')
            plt.ylabel('Stress %')
            plt.xticks(rotation=45)
            
            # Attention levels
            plt.subplot(2, 2, 3)
            attention_timestamps = [datetime.fromisoformat(d['timestamp']) for d in data if 'attention_level' in d]
            attention_levels = [d['attention_level'] for d in data if 'attention_level' in d]
            plt.plot(attention_timestamps, attention_levels, 'blue', linewidth=2)
            plt.title('Attention Levels')
            plt.ylabel('Attention %')
            plt.xticks(rotation=45)
            
            # Weekly summary bar chart
            plt.subplot(2, 2, 4)
            categories = ['Avg HR', 'Avg Stress', 'Avg Attention']
            values = [stats['avg_heart_rate'], stats['avg_stress_level'], stats['avg_attention_level']]
            plt.bar(categories, values, color=['red', 'orange', 'blue'])
            plt.title('Weekly Averages')
            plt.ylabel('Values')
            
            plt.tight_layout()
            plt.savefig('weekly_charts.png', dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            print(f"Error creating visualizations: {e}")
            
    def create_pdf_report(self, stats):
        """Create PDF report with statistics and charts"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            
            # Title
            pdf.cell(0, 10, 'NeuroBand Weekly Health Report', 0, 1, 'C')
            pdf.ln(10)
            
            # Date range
            pdf.set_font('Arial', '', 12)
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            pdf.cell(0, 10, f'Report Period: {start_date} to {end_date}', 0, 1)
            pdf.ln(5)
            
            # Statistics
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, 'Weekly Statistics:', 0, 1)
            pdf.set_font('Arial', '', 12)
            
            stats_text = [
                f'Average Heart Rate: {stats["avg_heart_rate"]:.1f} BPM',
                f'Average Stress Level: {stats["avg_stress_level"]:.1f}%',
                f'Average Attention Level: {stats["avg_attention_level"]:.1f}%',
                f'Maximum Heart Rate: {stats["max_heart_rate"]:.1f} BPM',
                f'Minimum Heart Rate: {stats["min_heart_rate"]:.1f} BPM',
                f'High Stress Episodes: {stats["stress_episodes"]}',
                f'High Focus Periods: {stats["high_focus_periods"]}',
                f'Total Data Points: {stats["total_data_points"]}'
            ]
            
            for stat in stats_text:
                pdf.cell(0, 8, stat, 0, 1)
                
            # Add chart if it exists
            if os.path.exists('weekly_charts.png'):
                pdf.ln(10)
                pdf.cell(0, 10, 'Weekly Trends:', 0, 1)
                pdf.image('weekly_charts.png', x=10, y=pdf.get_y(), w=190)
                
            # Save PDF
            pdf_filename = f'neuroband_weekly_report_{datetime.now().strftime("%Y%m%d")}.pdf'
            pdf.output(pdf_filename)
            
            return pdf_filename
            
        except Exception as e:
            print(f"Error creating PDF report: {e}")
            return None

class GameController:
    def __init__(self):
        self.game_active = False
        self.score = 0
        self.game_type = "simple_reaction"
        
    def start_brain_game(self, game_type="simple_reaction"):
        """Start a brain-controlled game"""
        self.game_type = game_type
        self.game_active = True
        self.score = 0
        
        game_thread = threading.Thread(target=self._run_game)
        game_thread.daemon = True
        game_thread.start()
        
    def _run_game(self):
        """Run the selected game"""
        try:
            if self.game_type == "simple_reaction":
                self.simple_reaction_game()
            elif self.game_type == "attention_trainer":
                self.attention_training_game()
            elif self.game_type == "blink_clicker":
                self.blink_clicker_game()
                
        except Exception as e:
            print(f"Error running game: {e}")
        finally:
            self.game_active = False
            
    def simple_reaction_game(self):
        """Simple reaction time game using blinks"""
        print("🎮 Starting Simple Reaction Game!")
        print("Blink when you see the signal!")
        
        for round_num in range(5):
            wait_time = random.uniform(2, 5)
            time.sleep(wait_time)
            
            print(f"🔴 SIGNAL! Blink now! (Round {round_num + 1}/5)")
            
            # Wait for blink detection (would be integrated with signal processing)
            # For demo, we'll simulate
            time.sleep(2)
            
        print(f"Game completed! Final score: {self.score}")
        
    def process_game_input(self, signal_data):
        """Process brain signals for game control"""
        if not self.game_active:
            return
            
        blink_detected = signal_data.get('blink_detected', False)
        attention_level = signal_data.get('attention_level', 0)
        
        if self.game_type == "blink_clicker" and blink_detected:
            self.score += 10
            print(f"Blink registered! Score: {self.score}")
        elif self.game_type == "attention_trainer" and attention_level > 80:
            self.score += 5
            print(f"High attention! Score: {self.score}")

# Integration class for all wow features
class WowFeaturesManager:
    def __init__(self):
        self.emergency_system = EmergencyAlertSystem()
        self.mindfulness_coach = MindfulnessCoach()
        self.study_tracker = StudyModeTracker()
        self.report_generator = WeeklyReportGenerator()
        self.game_controller = GameController()
        
    def process_all_features(self, signal_data, physiological_data):
        """Process all wow features with current data"""
        results = {}
        
        try:
            # Emergency alert system
            heart_rate = physiological_data.get('heart_rate', 0)
            stress_level = physiological_data.get('stress_level', 0)
            
            emergency_triggered = self.emergency_system.check_emergency_conditions(heart_rate, stress_level)
            results['emergency_alert'] = emergency_triggered
            
            # Mindfulness coach
            relaxation_started = self.mindfulness_coach.detect_stress_and_launch_session(stress_level)
            results['mindfulness_session'] = relaxation_started
            
            # Study mode tracker
            if self.study_tracker.tracking_active:
                attention_level = signal_data.get('attention_level', 0)
                self.study_tracker.log_attention_level(attention_level)
                results['study_tracking'] = True
            else:
                results['study_tracking'] = False
                
            # Game controller
            if self.game_controller.game_active:
                self.game_controller.process_game_input(signal_data)
                results['game_active'] = True
            else:
                results['game_active'] = False
                
            return results
            
        except Exception as e:
            print(f"Error processing wow features: {e}")
            return {"error": str(e)}

