# NeuroBand Signal Processing Module (`signal_processing.py`)

This document provides a detailed explanation of the `signal_processing.py` module, which is a core component of the NeuroBand Desktop Application. This module is responsible for taking raw biosignal data (EEG and ECG) received from the ESP32 and transforming it into meaningful metrics and insights, such as blink detection, brainwave analysis, heart rate, heart rate variability, and emotion/stress levels.

## 1. Overview

The `SignalProcessor` class within this module acts as the analytical engine of the NeuroBand system. It continuously processes incoming biosignal samples, maintains historical data in buffers, and applies various digital signal processing (DSP) techniques to extract relevant physiological and neurological information. This processed data then feeds into other modules, such as the Brain Control Interface and the Wow Features, enabling intelligent control and health monitoring.

## 2. Key Features and Functionalities

The `SignalProcessor` class implements the following key functionalities:

-   **Real-time Data Buffering:** Efficiently stores incoming EEG and ECG samples in fixed-size buffers for continuous analysis.
-   **Blink Detection:** Identifies distinct blink events from EEG signals based on amplitude thresholds.
-   **Heart Rate (HR) Calculation:** Determines the user's heart rate in beats per minute (BPM) from ECG signals.
-   **Heart Rate Variability (HRV) Analysis:** Quantifies the variation in time between heartbeats, a key indicator of autonomic nervous system activity and stress.
-   **Brainwave Analysis:** Decomposes EEG signals into standard frequency bands (Delta, Theta, Alpha, Beta) to assess different mental states.
-   **Attention Level Estimation:** Provides an estimate of the user's attention or focus level based on brainwave ratios.
-   **Alpha State Detection:** Identifies periods when the user is in an Alpha brainwave state, typically associated with relaxation.
-   **Emotion and Stress Detection:** Combines insights from brainwaves, heart rate, and HRV to infer the user's emotional state and stress level.

## 3. Class Structure: `SignalProcessor`

### `__init__(self, sampling_rate=100)`

-   **Purpose:** Initializes the `SignalProcessor` with a specified `sampling_rate` (defaulting to 100 Hz, matching the ESP32 firmware's `delay(10)` which implies 100 samples per second).
-   **Attributes Initialized:**
    -   `sampling_rate`: The rate at which biosignals are sampled.
    -   `buffer_size`: The maximum number of samples to store in EEG and ECG buffers (e.g., 5 seconds of data).
    -   `eeg_buffer`: A `deque` (double-ended queue) to store incoming EEG samples.
    -   `ecg_buffer`: A `deque` to store incoming ECG samples.
    -   `blink_threshold`: An amplitude value used to detect blinks in EEG signals.
    -   `last_blink_time`: Timestamp of the last detected blink to implement a cooldown period.
    -   `blink_cooldown`: Minimum time between consecutive blink detections.
    -   `heart_rate`: Stores the calculated heart rate.
    -   `last_hr_calculation`: Timestamp of the last heart rate calculation.
    -   `stress_level`: Stores the calculated stress level.
    -   `emotion_state`: Stores the inferred emotional state.

### `add_eeg_sample(self, value)`

-   **Purpose:** Appends a new EEG sample `value` to the `eeg_buffer`.

### `add_ecg_sample(self, value)`

-   **Purpose:** Appends a new ECG sample `value` to the `ecg_buffer`.

### `detect_blink(self)`

-   **Purpose:** Detects a blink event from the EEG buffer.
-   **Logic:**
    1.  Checks if there are enough samples in the `eeg_buffer`.
    2.  Applies a `blink_cooldown` to prevent multiple detections from a single blink.
    3.  Examines the most recent EEG values. If the current value crosses a predefined `blink_threshold` and previous values were significantly lower, it indicates a blink.
    4.  Updates `last_blink_time` upon detection.
-   **Returns:** `True` if a blink is detected, `False` otherwise.

### `calculate_heart_rate(self)`

-   **Purpose:** Calculates the heart rate (BPM) from the ECG buffer.
-   **Logic:**
    1.  Requires at least 2 seconds of ECG data in the buffer.
    2.  Uses `scipy.signal.find_peaks` to identify R-waves (peaks) in the ECG data.
    3.  Calculates the average interval between detected peaks.
    4.  Converts the average interval to BPM (60 / average_interval_in_seconds).
    5.  Updates `heart_rate` and `last_hr_calculation`.
-   **Returns:** The calculated heart rate in BPM.

### `calculate_hrv(self)`

-   **Purpose:** Calculates Heart Rate Variability (HRV) from the ECG buffer.
-   **Logic:**
    1.  Requires at least 5 seconds of ECG data.
    2.  Identifies R-waves similar to heart rate calculation.
    3.  Computes the standard deviation of the inter-beat intervals (RMSSD method is commonly used for time-domain HRV, though a simplified standard deviation is used here for demonstration).
-   **Returns:** The HRV value (in milliseconds).

### `analyze_brainwaves(self)`

-   **Purpose:** Analyzes the EEG buffer to determine the power of different brainwave frequency bands.
-   **Logic:**
    1.  Applies a Fast Fourier Transform (FFT) to the EEG data to convert it from the time domain to the frequency domain.
    2.  Defines standard frequency bands:
        -   **Delta:** 0.5 - 4 Hz (deep sleep)
        -   **Theta:** 4 - 8 Hz (drowsiness, meditation)
        -   **Alpha:** 8 - 13 Hz (relaxed, eyes closed)
        -   **Beta:** 13 - 30 Hz (alert, focused)
    3.  Calculates the mean power within each frequency band.
-   **Returns:** A dictionary containing the power values for Delta, Theta, Alpha, and Beta waves.

### `detect_emotion_stress(self)`

-   **Purpose:** Infers the user's emotional state and stress level by combining insights from brainwaves, heart rate, and HRV.
-   **Logic (Simplified for demonstration):**
    1.  Retrieves brainwave power, HRV, and heart rate.
    2.  Increases a `stress_score` based on indicators like high Beta waves (alertness/anxiety), high heart rate, and low HRV.
    3.  Decreases `stress_score` for indicators like high Alpha waves (relaxation).
    4.  Normalizes the `stress_score` to a 0-100 scale.
    5.  Categorizes `emotion_state` (e.g., 


    "stressed", "relaxed", "focused", "neutral") based on the calculated stress score and brainwave patterns.
-   **Returns:** A dictionary containing `stress_level`, `emotion`, `heart_rate`, `hrv`, and `brainwaves`.

### `get_attention_level(self)`

-   **Purpose:** Estimates the user's attention level.
-   **Logic:** Calculates the ratio of Beta wave power to Alpha wave power. A higher Beta/Alpha ratio generally indicates increased alertness and attention.
-   **Returns:** An attention level score (normalized to 0-100).

### `is_in_alpha_state(self)`

-   **Purpose:** Determines if the user is currently in an Alpha brainwave state.
-   **Logic:** Checks if the Alpha wave power is significantly higher than the Beta wave power.
-   **Returns:** `True` if in Alpha state, `False` otherwise.

### `process_realtime_sample(self, eeg_value, ecg_value=None)`

-   **Purpose:** The main entry point for processing a single incoming biosignal sample.
-   **Logic:**
    1.  Adds the `eeg_value` to the `eeg_buffer`.
    2.  If `ecg_value` is provided, adds it to the `ecg_buffer`.
    3.  Calls all relevant analysis methods (`detect_blink`, `get_attention_level`, `is_in_alpha_state`, `detect_emotion_stress`).
    4.  Aggregates the results into a single dictionary.
-   **Returns:** A dictionary containing the processed results, including `blink_detected`, `attention_level`, `alpha_state`, and `emotion_analysis`.

## 4. Usage Example

```python
from signal_processing import SignalProcessor
import time
import random

# Initialize the signal processor
processor = SignalProcessor(sampling_rate=100)

print("Simulating real-time biosignal data...")

for i in range(500): # Simulate 5 seconds of data
    # Simulate EEG data (e.g., a blink spike around sample 200)
    if 190 < i < 210:
        eeg_sample = random.randint(2500, 3500) # Simulate a blink
    else:
        eeg_sample = random.randint(500, 1500) # Normal EEG range

    # Simulate ECG data (simple sine wave for heart beat)
    ecg_sample = int(1000 + 500 * (np.sin(i * 0.1) + np.sin(i * 0.3)))

    # Process the sample
    results = processor.process_realtime_sample(eeg_sample, ecg_sample)

    if i % 50 == 0: # Print results every 0.5 seconds
        print(f"\n--- Sample {i} ---")
        print(f"Blink Detected: {results['blink_detected']}")
        print(f"Attention Level: {results['attention_level']:.2f}")
        print(f"Alpha State: {results['alpha_state']}")
        print(f"Emotion: {results['emotion_analysis']['emotion']}")
        print(f"Stress Level: {results['emotion_analysis']['stress_level']:.2f}")
        print(f"Heart Rate: {results['emotion_analysis']['heart_rate']:.2f} BPM")
        print(f"HRV: {results['emotion_analysis']['hrv']:.2f} ms")
        print(f"Brainwaves: {results['emotion_analysis']['brainwaves']}")

    time.sleep(0.01) # Simulate 100 Hz sampling rate

print("\nSimulation complete.")
```

## 5. Integration with `enhanced_main.py`

The `SignalProcessor` class is instantiated in the `EnhancedNeuroBandApp` class within `enhanced_main.py`. The `on_message` method of `EnhancedNeuroBandApp` receives raw EEG/ECG data from the WebSocket and passes it to `signal_processor.process_realtime_sample()` for analysis. The results are then used to update the GUI, trigger brain control actions, and feed into the "Wow Features" module.

```python
# In EnhancedNeuroBandApp.__init__
self.signal_processor = SignalProcessor()

# In EnhancedNeuroBandApp.on_message
signal_results = self.signal_processor.process_realtime_sample(eeg_value, ecg_value)
# ... then use signal_results to update GUI and other modules
```

## 6. Customization and Extension

-   **Threshold Adjustment:** The `blink_threshold` and other internal thresholds can be adjusted in the `SignalProcessor` class or exposed via the `Settings` tab in the GUI for user calibration.
-   **Advanced Filtering:** Implement more sophisticated digital filters (e.g., Butterworth, Chebyshev) to remove noise and artifacts from raw signals.
-   **Machine Learning Models:** Replace rule-based emotion/stress detection with trained machine learning models for improved accuracy and personalization.
-   **Additional Biosignals:** Extend the class to handle other biosignals like Electromyography (EMG) or Galvanic Skin Response (GSR) for more comprehensive monitoring.
-   **Feature Extraction:** Implement more advanced feature extraction techniques for biosignals, such as wavelet transforms or independent component analysis (ICA).

This module forms the analytical backbone of the NeuroBand system, providing the necessary intelligence to interpret complex human biosignals. Its robust design allows for future expansion and integration of more advanced signal processing techniques.


