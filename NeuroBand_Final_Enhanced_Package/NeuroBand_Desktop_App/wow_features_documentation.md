# NeuroBand Wow Features Module (`wow_features.py`)

This document provides a detailed explanation of the `wow_features.py` module, which encapsulates several advanced and innovative functionalities designed to enhance the NeuroBand user experience beyond basic control and monitoring. These features aim to provide proactive health management, engaging interactions, and comprehensive insights into the user's well-being.

## 1. Overview

The `wow_features.py` module integrates various high-impact functionalities, including an Emergency Alert System, a Mindfulness Coach, a Study Mode Tracker, a Weekly Report Generator, and a Game Controller. Each class within this module operates independently but can be triggered or influenced by the biosignal data processed by the `SignalProcessor` and managed by the `EnhancedNeuroBandApp`. The `WowFeaturesManager` class acts as an orchestrator, allowing the main application to easily interact with all these features.

## 2. Key Features and Functionalities

### 2.1. Emergency Alert System (`EmergencyAlertSystem` class)

-   **Purpose:** To provide immediate notification to emergency contacts when critical physiological conditions (e.g., dangerously high heart rate or stress levels) are detected.
-   **Functionality:**
    -   Monitors `heart_rate` and `stress_level` against predefined thresholds.
    -   Triggers an alert if thresholds are exceeded.
    -   Sends email alerts to a list of emergency contacts.
    -   (Placeholder) Displays on-screen alerts and provides text-to-speech warnings.
    -   Logs all emergency events for review.
-   **Configuration:** Requires SMTP server details (e.g., Gmail) and a list of emergency contact email addresses.

### 2.2. Mindfulness Coach (`MindfulnessCoach` class)

-   **Purpose:** To proactively help users manage stress and promote relaxation through guided sessions.
-   **Functionality:**
    -   Detects high stress levels from the `SignalProcessor`.
    -   Automatically launches a relaxation session (e.g., deep breathing, progressive muscle relaxation, guided meditation, nature sounds).
    -   (Placeholder) Guides the user through the chosen technique.
    -   Monitors for improvement (e.g., decrease in heart rate) during the session.
-   **Techniques:** Includes methods for `deep_breathing_exercise`, `progressive_muscle_relaxation`, `guided_meditation`, and `play_nature_sounds`.

### 2.3. Study Mode Tracker (`StudyModeTracker` class)

-   **Purpose:** To help users understand and improve their focus and productivity during study or work sessions.
-   **Functionality:**
    -   Allows users to start and end study sessions.
    -   Logs `attention_level` at regular intervals.
    -   Tracks periods of distraction (low attention).
    -   Calculates a `focus_efficiency` score for each session.
    -   Stores session data for later analysis.

### 2.4. Weekly Report Generator (`WeeklyReportGenerator` class)

-   **Purpose:** To provide users with a comprehensive summary of their physiological and mental well-being over a week.
-   **Functionality:**
    -   Collects all recorded biosignal data from the past seven days.
    -   Calculates weekly statistics (e.g., average HR, stress, attention; max/min HR; stress episodes).
    -   Generates visual charts (e.g., heart rate over time, stress levels, attention levels) using `matplotlib`.
    -   Creates a professional PDF report using `FPDF`, including statistics and embedded charts.
    -   (Placeholder) Allows sharing the report via email.

### 2.5. Game Controller (`GameController` class)

-   **Purpose:** To provide engaging and interactive ways for users to train and utilize their brain-control abilities.
-   **Functionality:**
    -   Implements simple brain-controlled games (e.g., `simple_reaction_game`, `attention_training_game`, `blink_clicker_game`).
    -   Processes brain signals (blinks, attention levels) as game inputs.
    -   Tracks game score and provides feedback.

## 3. Class Structure and Methods

### 3.1. `EmergencyAlertSystem`

-   `__init__(self)`: Initializes alert status and email configuration.
-   `check_emergency_conditions(self, heart_rate, stress_level)`: Checks if current HR and stress exceed thresholds.
-   `trigger_emergency_alert(self, message, heart_rate, stress_level)`: Initiates the alert process in a separate thread.
-   `_execute_emergency_alert(self, message, heart_rate, stress_level)`: Private method to send emails, display warnings, and log events.
-   `send_email_alert(self, message, heart_rate, stress_level)`: Handles sending email notifications via SMTP.
-   `log_emergency_event(self, message, heart_rate, stress_level)`: Records alert details to a JSON log file.

### 3.2. `MindfulnessCoach`

-   `__init__(self)`: Initializes session status and lists relaxation techniques.
-   `detect_stress_and_launch_session(self, stress_level)`: Checks stress level and launches a session if needed.
-   `launch_relaxation_session(self, technique)`: Starts the chosen relaxation technique in a separate thread.
-   `_execute_relaxation_session(self, technique)`: Private method to run the selected relaxation exercise.
-   `deep_breathing_exercise(self)`: Guides a deep breathing routine.
-   `progressive_muscle_relaxation(self)`: Guides a muscle relaxation routine.
-   `guided_meditation(self)`: Provides a simple guided meditation script.
-   `play_nature_sounds(self)`: (Placeholder) Simulates playing nature sounds.

### 3.3. `StudyModeTracker`

-   `__init__(self)`: Initializes tracking status and session data storage.
-   `start_study_session(self)`: Begins a new study session, recording start time.
-   `log_attention_level(self, attention_level)`: Records attention level at intervals and tracks distractions.
-   `end_study_session(self)`: Concludes the session and calculates metrics.
-   `calculate_session_metrics(self)`: Computes focus efficiency, average attention, and distraction count.

### 3.4. `WeeklyReportGenerator`

-   `__init__(self)`: Initializes data file path.
-   `collect_weekly_data(self)`: Reads and filters biosignal data from the past week.
-   `generate_report(self)`: Orchestrates data collection, visualization, and PDF creation.
-   `calculate_weekly_stats(self, data)`: Computes statistical summaries of weekly data.
-   `create_visualizations(self, data, stats)`: Generates `matplotlib` plots for trends and averages.
-   `create_pdf_report(self, stats)`: Creates a PDF document with statistics and embedded charts using `FPDF`.

### 3.5. `GameController`

-   `__init__(self)`: Initializes game status and score.
-   `start_brain_game(self, game_type)`: Starts a specified brain-controlled game in a separate thread.
-   `_run_game(self)`: Private method to execute the game logic.
-   `simple_reaction_game(self)`: Implements a reaction time game.
-   `process_game_input(self, signal_data)`: Processes brain signals to control game actions.

### 3.6. `WowFeaturesManager`

-   `__init__(self)`: Instantiates all individual wow feature classes.
-   `process_all_features(self, signal_data, physiological_data)`: A central method called by the main application to pass current biosignal and physiological data to all relevant wow features for processing and triggering.

## 4. Integration with `enhanced_main.py`

The `WowFeaturesManager` class is instantiated in the `EnhancedNeuroBandApp` class within `enhanced_main.py`. The `on_message` method of `EnhancedNeuroBandApp` passes the processed `signal_results` and `physiological_data` (heart rate, stress, attention, emotion) to `wow_features.process_all_features()`. This allows the wow features to react to the user's real-time state and trigger their respective functionalities.

```python
# In EnhancedNeuroBandApp.__init__
self.wow_features = WowFeaturesManager()

# In EnhancedNeuroBandApp.on_message
# ... (after signal processing)
physiological_data = {
    'heart_rate': heart_rate,
    'stress_level': stress_level,
    'attention_level': attention_level,
    'emotion': emotion
}
wow_results = self.wow_features.process_all_features(signal_results, physiological_data)
# ... (update GUI based on wow_results if needed)
```

## 5. Customization and Extension

-   **Emergency Alert Thresholds:** The thresholds for triggering emergency alerts can be adjusted within the `EmergencyAlertSystem` class.
-   **New Relaxation Techniques:** New methods for guided relaxation can be added to the `MindfulnessCoach` class.
-   **Study Session Metrics:** Additional metrics or analysis can be incorporated into the `StudyModeTracker`.
-   **Report Customization:** The `WeeklyReportGenerator` can be extended to include more types of graphs, data points, or different report formats.
-   **New Brain Games:** New interactive games can be developed and integrated into the `GameController`.
-   **Email/SMS Integration:** For the Emergency Alert System, consider integrating with SMS gateways (like Twilio) for direct text message alerts, or exploring other email service providers.

This module significantly enhances the utility and appeal of the NeuroBand system, transforming it from a mere control device into a comprehensive personal well-being assistant. The modular design allows for easy expansion and the addition of even more innovative features in the future.


