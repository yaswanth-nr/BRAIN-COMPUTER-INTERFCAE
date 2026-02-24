# NeuroBand Desktop Application

## Overview

The NeuroBand Desktop Application is a comprehensive brain-computer interface (BCI) software that receives and processes biosignal data from the ESP32 firmware, providing real-time analysis, control capabilities, and advanced "wow" features for health monitoring and accessibility.

## Features

### Core Modules

1. **Signal Processing (`signal_processing.py`)**
   - Real-time EEG and ECG signal analysis
   - Blink detection using threshold-based algorithms
   - Brainwave frequency band analysis (Alpha, Beta, Theta, Delta)
   - Heart rate and Heart Rate Variability (HRV) calculation
   - Emotion and stress level detection
   - Attention level monitoring

2. **Brain Control Interface (`brain_control.py`)**
   - Mouse click control via blink detection
   - Cursor movement based on attention levels
   - Application launching in Alpha brainwave states
   - Smart app launcher with brain signal navigation
   - Gaming control for brain-controlled games
   - Window management and accessibility features

3. **Wow Features (`wow_features.py`)**
   - **Emergency Alert System**: Automatic detection of high stress/heart rate with email/SMS alerts
   - **Mindfulness Coach**: Stress detection with guided relaxation sessions
   - **Study Mode Tracker**: Focus efficiency monitoring and reporting
   - **Weekly Report Generator**: Automated PDF reports with health analytics
   - **Game Controller**: Brain-controlled games for training and entertainment

4. **Enhanced Main Application (`enhanced_main.py`)**
   - Modern GUI with real-time dashboards
   - Live plotting of EEG, heart rate, stress, and attention data
   - Tabbed interface for different functionalities
   - WebSocket communication with ESP32
   - Settings and configuration management

## Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **ESP32 with NeuroBand firmware running**
3. **BioAmp sensor connected to ESP32**

### Setup Instructions

1. **Clone or download the NeuroBand Desktop Application files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure ESP32 IP Address:**
   - Update the IP address in the Settings tab of the application
   - Or modify the default IP in `enhanced_main.py` (line 287)

4. **Configure Email Settings (for Emergency Alerts):**
   - Edit `wow_features.py` lines 15-21
   - Add your Gmail credentials and emergency contact emails
   - Enable "App Passwords" in your Google account for security

## Usage

### Running the Application

```bash
python enhanced_main.py
```

### Main Interface Tabs

#### 1. Live Dashboard
- **Vital Signs Panel**: Real-time display of heart rate, stress level, attention, and emotion
- **Real-time Graphs**: Live plotting of EEG signals, heart rate trends, stress levels, and attention patterns
- **Visual Indicators**: Color-coded status indicators for quick health assessment

#### 2. Brain Control
- **Blink Control**: Perform mouse clicks by blinking
- **Attention Control**: Move cursor based on focus levels
- **Alpha State Control**: Trigger actions when in relaxed brainwave state
- **Status Monitoring**: Track control actions and cursor position

#### 3. Signal Analysis
- **Brainwave Analysis**: Real-time frequency band decomposition
- **Signal Quality**: Monitor electrode connection and signal integrity
- **Threshold Monitoring**: Visualize detection thresholds and signal patterns

#### 4. Wow Features
- **Emergency Alerts**: Configure and test emergency notification system
- **Mindfulness Coach**: Start guided relaxation sessions
- **Study Tracker**: Monitor focus during study sessions
- **Brain Games**: Play attention and blink-controlled games
- **Weekly Reports**: Generate comprehensive health reports

#### 5. Settings
- **Connection Settings**: Configure ESP32 IP address and reconnection
- **Detection Thresholds**: Adjust blink detection and other sensitivity settings
- **Calibration**: Fine-tune signal processing parameters

## Signal Processing Details

### EEG Processing Pipeline

1. **Raw Signal Acquisition**: Receives analog values from ESP32
2. **Buffer Management**: Maintains rolling buffers for real-time analysis
3. **Blink Detection**: Threshold-based detection with cooldown periods
4. **Frequency Analysis**: FFT-based brainwave band extraction
5. **Attention Calculation**: Beta/Alpha ratio for focus assessment
6. **Alpha State Detection**: Relaxation state identification

### ECG Processing Pipeline

1. **Heart Rate Calculation**: Peak detection for R-wave identification
2. **HRV Analysis**: Inter-beat interval variability measurement
3. **Stress Assessment**: Combined physiological stress indicators
4. **Emergency Detection**: Threshold-based alert triggering

## Brain Control Commands

### Available Actions

| Brain Signal | Action | Description |
|-------------|--------|-------------|
| Blink | Mouse Click | Single click at current cursor position |
| High Attention | Cursor Movement | Move cursor based on focus direction |
| Alpha State | App Launch | Cycle through predefined applications |
| Sustained Focus | Window Control | Minimize, maximize, or switch windows |
| Stress Detection | Mindfulness | Auto-launch relaxation session |

### Customization

Brain control actions can be customized by modifying the `brain_control.py` file:

- **Blink Actions**: Edit `execute_blink_action()` method
- **Attention Control**: Modify `control_cursor_with_attention()` method
- **Alpha Actions**: Update `alpha_actions` deque with custom functions
- **Gaming Controls**: Extend `gaming_control()` method

## Wow Features Configuration

### Emergency Alert System

1. **Email Configuration**:
   ```python
   self.email_config = {
       'smtp_server': 'smtp.gmail.com',
       'smtp_port': 587,
       'email': 'your_email@gmail.com',
       'password': 'your_app_password',
       'emergency_contacts': ['emergency1@gmail.com', 'emergency2@gmail.com']
   }
   ```

2. **Alert Thresholds**:
   - Heart Rate: > 120 BPM
   - Stress Level: > 85%
   - Customizable in `check_emergency_conditions()` method

### Mindfulness Coach

- **Relaxation Techniques**: Deep breathing, progressive muscle relaxation, guided meditation, nature sounds
- **Auto-Trigger**: Activates when stress level > 70%
- **Session Duration**: Configurable (default: 5-10 minutes)

### Study Mode Tracker

- **Metrics Tracked**: Attention levels, distraction count, focus efficiency
- **Logging Interval**: Every 5 minutes (configurable)
- **Report Generation**: Session summary with focus efficiency score

### Weekly Report Generator

- **Data Collection**: Aggregates past 7 days of biosignal data
- **Visualizations**: Heart rate trends, stress patterns, attention analysis
- **PDF Output**: Professional report with graphs and statistics
- **Email Sharing**: Automatic report distribution (optional)

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Verify ESP32 IP address in settings
   - Check Wi-Fi network connectivity
   - Ensure ESP32 firmware is running and accessible

2. **No Signal Data Received**
   - Check BioAmp sensor connections
   - Verify electrode placement on forehead
   - Ensure proper skin contact and conductivity

3. **Blink Detection Not Working**
   - Adjust blink threshold in settings
   - Check signal quality indicators
   - Verify electrode placement for EEG signals

4. **Emergency Alerts Not Sending**
   - Configure email settings with valid credentials
   - Enable "App Passwords" for Gmail accounts
   - Check internet connectivity

5. **Performance Issues**
   - Reduce plot update frequency in `update_plots()` method
   - Decrease buffer sizes for lower memory usage
   - Close unnecessary applications to free system resources

### Debug Mode

Enable debug output by adding print statements or using Python's logging module:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Customization

### Adding New Brain Control Actions

1. **Create Action Function**:
   ```python
   def custom_action(self):
       # Your custom action code here
       pass
   ```

2. **Add to Alpha Actions**:
   ```python
   self.alpha_actions.append(self.custom_action)
   ```

3. **Map to Brain Signal**:
   ```python
   if specific_brain_pattern_detected:
       self.custom_action()
   ```

### Extending Signal Processing

1. **Add New Analysis Method**:
   ```python
   def custom_analysis(self, signal_data):
       # Your analysis code
       return analysis_result
   ```

2. **Integrate in Processing Pipeline**:
   ```python
   custom_result = self.custom_analysis(eeg_data)
   ```

### Creating Custom Wow Features

1. **Inherit from Base Class**:
   ```python
   class CustomFeature:
       def __init__(self):
           # Initialize feature
           pass
       
       def process(self, signal_data):
           # Process signals and trigger feature
           pass
   ```

2. **Add to Wow Features Manager**:
   ```python
   self.custom_feature = CustomFeature()
   ```

## Data Privacy and Security

- **Local Processing**: All signal processing occurs locally on your computer
- **No Cloud Storage**: Raw biosignal data is not transmitted to external servers
- **Encrypted Communications**: WebSocket connections can be secured with WSS
- **Data Retention**: Configure automatic data deletion after specified periods
- **Emergency Contacts**: Ensure emergency contact consent before adding to alert system

## Performance Optimization

### For Real-time Performance

1. **Reduce Buffer Sizes**: Smaller buffers for faster processing
2. **Optimize Plot Updates**: Lower refresh rates for GUI elements
3. **Parallel Processing**: Use threading for intensive computations
4. **Memory Management**: Regular cleanup of old data

### For Accuracy

1. **Increase Buffer Sizes**: More data for better signal analysis
2. **Higher Sampling Rates**: More frequent data collection
3. **Advanced Filtering**: Implement noise reduction algorithms
4. **Calibration Procedures**: User-specific threshold adjustment

## Future Enhancements

- **Machine Learning Integration**: Personalized pattern recognition
- **Multi-user Support**: Individual profiles and settings
- **Cloud Synchronization**: Optional data backup and sharing
- **Mobile App Integration**: Companion smartphone application
- **Advanced Visualizations**: 3D brain activity mapping
- **Therapy Integration**: Clinical-grade health monitoring

## Support and Contributing

For questions, bug reports, or feature requests:

1. **Documentation**: Refer to inline code comments
2. **Community**: Join NeuroBand user forums
3. **Issues**: Report bugs through project issue tracker
4. **Contributions**: Submit pull requests for improvements

## License

This software is provided for educational and research purposes. Please ensure compliance with local regulations regarding medical devices and health monitoring applications.

---

**Note**: This application is designed for research and educational purposes. It is not intended for medical diagnosis or treatment. Always consult healthcare professionals for medical advice.

