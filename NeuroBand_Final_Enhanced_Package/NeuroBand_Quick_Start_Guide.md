# NeuroBand Quick Start Guide

## 🚀 Get Started in 5 Minutes

### What You Have
- **ESP32 Firmware**: Ready-to-upload code for your ESP32 + BioAmp hardware
- **Original Desktop App**: Functional tkinter-based application (NeuroBand_Desktop_App/)
- **Enhanced PyQt App**: Advanced application with world-class UI/UX (NeuroBand_Enhanced_PyQt/)
- **Comprehensive Documentation**: Complete setup and user guides

### Option 1: Quick Demo (Original App)
1. **Upload ESP32 Firmware**:
   - Open `NeuroBand_ESP32_Firmware/NeuroBand_ESP32_Firmware.ino` in Arduino IDE
   - Update WiFi credentials (lines 8-9)
   - Upload to your ESP32

2. **Run Original Desktop App**:
   ```bash
   cd NeuroBand_Desktop_App
   pip install -r requirements.txt
   python enhanced_main.py
   ```

3. **Update IP Address**: Enter your ESP32's IP in the Settings tab

### Option 2: Enhanced Experience (PyQt App)
1. **Upload ESP32 Firmware** (same as above)

2. **Install Enhanced App**:
   ```bash
   cd NeuroBand_Enhanced_PyQt
   pip install -r requirements_pyqt.txt
   python main_pyqt.py
   ```

3. **Enjoy Advanced Features**:
   - Beautiful dark theme UI
   - Real-time 3D brain visualization
   - Advanced biofeedback training
   - Smart home integration
   - Machine learning personalization

### Hardware Setup
- Connect BioAmp analog output to ESP32 pin 34 (or update `bioAmpPin` in firmware)
- Place EEG electrodes on forehead
- Power ESP32 and connect to WiFi

### Key Features
- **Brain Control**: Blink to click, focus to move cursor
- **Health Monitoring**: Real-time heart rate, stress, emotion tracking
- **Emergency Alerts**: Automatic notifications for critical conditions
- **Mindfulness Coach**: Guided relaxation sessions
- **Study Tracker**: Focus monitoring and productivity analytics
- **Weekly Reports**: Comprehensive health summaries

### Troubleshooting
- **Connection Issues**: Check ESP32 IP address and WiFi connection
- **No Signal**: Verify electrode placement and BioAmp wiring
- **Performance**: Close other applications, check system resources

### What's New in Enhanced Version
- **Modern UI**: Professional dark theme with smooth animations
- **3D Visualizations**: Interactive brain activity displays
- **Advanced ML**: Personalized signal processing
- **Voice Commands**: Hybrid brain + voice control
- **Smart Home**: Control IoT devices with thoughts
- **Sleep Monitoring**: EEG-based sleep quality analysis

### Next Steps
1. Read the comprehensive `NeuroBand_User_Guide.md` for detailed setup
2. Explore the enhanced PyQt application for advanced features
3. Check `README_Enhanced.md` for technical details
4. Experiment with different control modes and features

### Support
- All code is well-documented with inline comments
- Multiple README files provide different levels of detail
- Modular architecture allows easy customization and extension

**Enjoy your NeuroBand experience! 🧠✨**

