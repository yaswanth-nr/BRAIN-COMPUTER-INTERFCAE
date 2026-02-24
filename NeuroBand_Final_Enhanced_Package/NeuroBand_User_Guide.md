# NeuroBand System: Comprehensive Setup and User Guide

This guide provides a comprehensive overview of setting up, configuring, and using the NeuroBand system. It covers both the hardware (ESP32 with BioAmp) and the software (Desktop Application), detailing the steps required to get your NeuroBand up and running, and how to utilize its various features for brain-computer interface control and health monitoring.

## 1. Introduction to NeuroBand

The NeuroBand is an innovative, wireless brain-heart interface designed to provide full control over a Windows laptop using brain signals, while simultaneously monitoring vital health metrics such as heart rate, emotional state, and stress levels. This system combines cutting-edge biosignal acquisition with a user-friendly desktop application to offer a unique blend of accessibility, mental wellness support, and interactive experiences.

**Key Capabilities:**

-   **Brain-Computer Interface (BCI):** Control your laptop with blinks, focus, and mental states.
-   **Real-time Health Monitoring:** Track heart rate, stress, and emotional states.
-   **Mindfulness Coaching:** Guided sessions to help manage stress.
-   **Study Mode Tracking:** Monitor and improve focus during study or work.
-   **Emergency Alerts:** Proactive notifications for critical health changes.
-   **Weekly Health Reports:** Comprehensive summaries of your well-being.
-   **Brain Games:** Engaging activities to train and utilize BCI skills.

## 2. System Architecture Overview

The NeuroBand system comprises two main components that communicate wirelessly:

1.  **NeuroBand Headband (ESP32 Firmware):** This wearable device integrates the BioAmp sensor and an ESP32 microcontroller. It is responsible for:
    -   Acquiring raw EEG (brain) and ECG (heart) signals.
    -   Digitizing and packaging the biosignal data.
    -   Transmitting data wirelessly via Wi-Fi to the Desktop Application.

2.  **NeuroBand Desktop Application (Python):** This software runs on your Windows laptop and serves as the central hub for the system. It performs:
    -   Receiving real-time biosignal data from the ESP32 via WebSockets.
    -   Advanced signal processing to extract meaningful insights (e.g., blink detection, brainwave analysis, heart rate calculation, emotion/stress classification).
    -   Translating brain signals into laptop control commands (e.g., mouse clicks, application launches).
    -   Displaying real-time health metrics and visualizations on an intuitive graphical user interface (GUI).
    -   Managing and executing advanced "wow" features like emergency alerts, mindfulness coaching, and report generation.

**Communication Flow:**

Raw Biosignals (EEG/ECG) → BioAmp Sensor → ESP32 (Firmware) → Wi-Fi (WebSocket) → NeuroBand Desktop Application (Python) → Signal Processing, BCI Control, Health Monitoring, and UI Display.

## 3. Hardware Setup

Before you can use the NeuroBand system, you need to assemble and configure the hardware components.

### 3.1. Components Required

-   **ESP32 Development Board:** (e.g., ESP32 DevKitC, NodeMCU ESP32)
-   **BioAmp Sensor:** (e.g., EXG Pill or similar biosignal amplifier)
-   **EEG/ECG Electrodes:** (3 electrodes recommended for forehead/head placement for EEG, and optional chest placement for ECG)
-   **Rechargeable Battery Unit:** (e.g., 3.7V Li-ion battery with charging circuit)
-   **Custom Headband:** (Cloth or 3D printed, designed to comfortably hold the electronics and electrodes)
-   **Jumper Wires:** For connecting the BioAmp to the ESP32.
-   **USB Cable:** For programming the ESP32.
-   **Optional Add-ons:** Vibration motor, LED strip, temperature sensor.

### 3.2. Wiring Instructions (Conceptual)

**Disclaimer:** The exact wiring will depend on your specific BioAmp module and ESP32 board. Always refer to the datasheets and pinout diagrams for your components. The following is a general guide:

1.  **BioAmp to ESP32:**
    -   **BioAmp VCC → ESP32 3.3V/5V:** Connect the power supply for the BioAmp. Ensure it matches the BioAmp's voltage requirements.
    -   **BioAmp GND → ESP32 GND:** Connect the ground pins.
    -   **BioAmp Analog Output (e.g., `OUT`) → ESP32 Analog Input Pin:** Connect the analog signal output from the BioAmp to an ADC (Analog-to-Digital Converter) enabled pin on the ESP32. Common choices are GPIO32-39. **Note the `bioAmpPin` in the ESP32 firmware (default `34`) and ensure your wiring matches.**

2.  **Electrodes to BioAmp:**
    -   **Reference Electrode:** Typically placed on a neutral point (e.g., mastoid bone behind the ear or earlobe) or a non-active area on the forehead.
    -   **Input Electrodes (2):** Placed on the forehead or scalp according to standard EEG electrode placement for the signals you wish to capture (e.g., frontal lobe for blinks and attention).
    -   **For ECG:** If you plan to switch to ECG, two electrodes would typically be placed on the chest, and a reference electrode elsewhere.

3.  **Battery Connection:**
    -   Connect the 3.7V Li-ion battery to a suitable battery management system (BMS) or charging circuit, and then connect the output of the BMS to the ESP32's power input (e.g., `VIN` or `5V` pin if using a voltage regulator, or directly to `3.3V` if the BMS provides regulated 3.3V).

4.  **Optional Add-ons:**
    -   **Vibration Motor/LED Strip:** Connect to appropriate digital output pins on the ESP32, usually through a transistor or motor driver if they require more current than the ESP32 pin can supply.
    -   **Temperature Sensor:** Connect to an analog or digital pin as per the sensor's specifications.

### 3.3. Headband Assembly

-   Integrate the ESP32, BioAmp, battery, and electrodes securely within the custom headband. Ensure electrodes make good, consistent contact with the skin. Minimize external wires for comfort and aesthetics.

## 4. ESP32 Firmware Setup

This section guides you through uploading the necessary firmware to your ESP32 board.

### 4.1. Software Requirements

-   **Arduino IDE:** Download and install the Arduino IDE from [arduino.cc](https://www.arduino.cc/en/software).
-   **ESP32 Board Package:**
    1.  In Arduino IDE, go to `File > Preferences`.
    2.  In "Additional Boards Manager URLs," add: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
    3.  Go to `Tools > Board > Boards Manager...`.
    4.  Search for "esp32" and install the "esp32 by Espressif Systems" package.
-   **Required Libraries:**
    1.  In Arduino IDE, go to `Sketch > Include Library > Manage Libraries...`.
    2.  Search for and install `AsyncTCP`.
    3.  Search for and install `ESPAsyncWebServer`.

### 4.2. Firmware Configuration and Upload

1.  **Open the Firmware:** Open the `NeuroBand_ESP32_Firmware.ino` file (provided in the `NeuroBand_ESP32_Firmware` folder of the project ZIP) in the Arduino IDE.
2.  **Update Wi-Fi Credentials:** Locate the following lines and replace `


YOUR_WIFI_SSID` and `YOUR_WIFI_PASSWORD` with your actual Wi-Fi network name and password:

    ```cpp
    const char* ssid = "YOUR_WIFI_SSID";
    const char* password = "YOUR_WIFI_PASSWORD";
    ```
3.  **Verify BioAmp Pin:** Ensure the `bioAmpPin` constant matches the GPIO pin on your ESP32 where the BioAmp analog output is connected. The default is `34`:

    ```cpp
    const int bioAmpPin = 34; // Assuming analog input pin
    ```
    If your wiring uses a different pin, update this value accordingly.
4.  **Select Board:** Go to `Tools > Board > ESP32 Arduino` and select your specific ESP32 development board (e.g., "ESP32 Dev Module").
5.  **Select Port:** Go to `Tools > Port` and select the serial port connected to your ESP32. If you don't see it, you might need to install the appropriate USB-to-Serial driver (e.g., CP210x or CH340).
6.  **Upload:** Click the "Upload" button (right arrow icon) in the Arduino IDE. The IDE will compile the code and upload it to your ESP32. You should see "Done uploading" once complete.
7.  **Monitor Serial Output:** Open the Serial Monitor (`Tools > Serial Monitor`) and set the baud rate to `115200`. You should see messages indicating the ESP32 connecting to your Wi-Fi network and its assigned IP address. **Note down this IP address**, as you will need it for the Desktop Application.

    ```
    Connecting to WiFi: YOUR_WIFI_SSID
    Connecting...
    WiFi connected
    IP Address: 192.168.1.100  <-- IMPORTANT: Note this IP address
    Web Server started
    ```

Your ESP32 is now configured to acquire biosignal data and stream it wirelessly via WebSockets. Keep the ESP32 powered on and connected to your Wi-Fi network.

## 5. Desktop Application Setup

This section details how to set up and run the NeuroBand Desktop Application on your Windows laptop. This application will receive data from the ESP32, process it, and provide the user interface for control and monitoring.

### 5.1. Software Requirements

-   **Python 3.8 or higher:** Download and install Python from [python.org](https://www.python.org/downloads/). Ensure you check the option "Add Python to PATH" during installation.
-   **Required Python Libraries:** The application relies on several Python libraries. These can be installed using `pip`.

### 5.2. Installation Steps

1.  **Download Project Files:** If you haven't already, download the entire NeuroBand project ZIP file (e.g., `NeuroBand_Project.zip`) and extract its contents to a convenient location on your computer (e.g., `C:\NeuroBand`).
2.  **Open Command Prompt/Terminal:** Navigate to the `NeuroBand_Desktop_App` directory within the extracted project folder using your command prompt or terminal:

    ```bash
    cd C:\NeuroBand\NeuroBand_Desktop_App
    ```
    (Replace `C:\NeuroBand` with your actual path)
3.  **Install Python Dependencies:** Run the following command to install all required libraries. It's recommended to do this in a virtual environment, but for simplicity, you can install globally.

    ```bash
    pip install -r requirements.txt
    ```
    This command will install `tkinter`, `websocket-client`, `numpy`, `scipy`, `matplotlib`, `pyautogui`, `neurokit2`, `pygame`, `fpdf2`, `pyttsx3`, `Pillow`, `pandas`, and `seaborn`.
4.  **Configure ESP32 IP Address in Application:**
    -   Open the `enhanced_main.py` file (located in the `NeuroBand_Desktop_App` folder) using a text editor (e.g., Notepad++, VS Code).
    -   Locate the `connect_websocket` method (around line 287) and find the line `esp32_ip = 


"YOUR_ESP32_IP_ADDRESS"`.
    -   Replace `

YOUR_ESP32_IP_ADDRESS` with the actual IP address you noted down from the ESP32 Serial Monitor (e.g., `192.168.1.100`).

    ```python
    # Replace with your ESP32's IP address
    esp32_ip = "192.168.1.100" # <--- UPDATE THIS LINE
    websocket_url = f"ws://{esp32_ip}:8080/ws"
    ```
    Alternatively, you can leave this line as is and enter the IP address directly in the application's 


Settings tab once it's running.
5.  **Configure Email Settings (for Emergency Alerts - Optional):**
    -   If you plan to use the Emergency Alert System, you need to configure your email credentials. Open `wow_features.py` (located in the `NeuroBand_Desktop_App` folder) in a text editor.
    -   Locate the `email_config` dictionary (around line 15) and update the `email`, `password`, and `emergency_contacts` fields:

        ```python
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': 'your_email@gmail.com', # <--- YOUR GMAIL ADDRESS
            'password': 'your_app_password', # <--- GENERATED APP PASSWORD
            'emergency_contacts': ['emergency1@gmail.com', 'emergency2@gmail.com'] # <--- RECIPIENT EMAILS
        }
        ```
    -   **Important for Gmail Users:** You cannot use your regular Gmail password directly. You must generate an "App password" for the application. Go to your Google Account Security settings, enable 2-Step Verification, and then generate an App password. Use this generated password in the `password` field above.

## 6. Running the NeuroBand Desktop Application

Once all the setup steps are complete, you can run the application:

1.  **Ensure ESP32 is Running:** Make sure your ESP32 is powered on, connected to your Wi-Fi network, and successfully streaming data.
2.  **Run the Application:** From your command prompt (still in the `NeuroBand_Desktop_App` directory), execute:

    ```bash
    python enhanced_main.py
    ```

    The NeuroBand Desktop Application window should appear.

## 7. Using the NeuroBand Desktop Application

The application features a tabbed interface, organizing its functionalities into different sections:

### 7.1. 📊 Live Dashboard

This is your primary view for real-time health and signal monitoring.

-   **Vital Signs Panel (Left):** Displays your current Heart Rate (BPM), Stress Level (%), Attention Level (%), and inferred Emotion. These values update in real-time.
-   **Real-time Graphs (Right):** Shows live plots of:
    -   **EEG Signal:** Raw brainwave data.
    -   **Heart Rate:** Your heart rate trend over time.
    -   **Stress Level:** Your stress level trend.
    -   **Attention Level:** Your attention level trend.
-   **Signal Quality Indicator:** Located on the dashboard, this indicates the reliability of the biosignal input. Ensure it shows "Good" for accurate readings.

### 7.2. 🧠 Brain Control

This tab allows you to interact with your Windows laptop using your brain signals.

-   **Blink Control:** When a distinct blink is detected by the system, it will trigger a mouse click. You can observe the "Blinks detected" counter increase.
-   **Attention Control:** Your focus level (derived from EEG) can influence cursor movement. Higher attention might lead to more precise or faster cursor control. Observe the "Cursor position" updates.
-   **Alpha State Control:** When you enter a relaxed, alpha brainwave state, the system can trigger predefined actions (e.g., typing letters, launching applications). The "Last action" label will indicate what was triggered.

### 7.3. 📈 Signal Analysis

This tab provides deeper insights into your biosignal data.

-   **Brainwave Analysis:** Displays the power of different brainwave frequency bands (Delta, Theta, Alpha, Beta). These values indicate your current mental state (e.g., high Alpha for relaxation, high Beta for alertness).
-   **Signal Quality:** Provides more detailed information about the quality of the incoming signals.

### 7.4. ✨ Wow Features

This section houses the advanced and innovative functionalities of NeuroBand.

-   **Emergency Alert System:**
    -   **Status:** Shows if the system is monitoring for critical conditions.
    -   **Test Emergency Alert Button:** Click this to simulate an emergency alert and test your email configuration. **Use with caution and inform your emergency contacts beforehand.**
-   **Mindfulness Coach:**
    -   **Status:** Indicates if a relaxation session is active.
    -   **Start Relaxation Session Button:** Click to initiate a guided mindfulness exercise. The system can also automatically launch a session if high stress is detected.
-   **Study Mode Tracker:**
    -   **Start Study Session Button:** Begins tracking your attention and focus during a study or work period.
    -   **End Study Session Button:** Concludes the session and provides a focus efficiency score.
-   **Brain Games:**
    -   **Blink Game / Attention Game Buttons:** Engage in simple games designed to train and demonstrate your brain control abilities.
-   **Weekly Report:**
    -   **Generate Weekly Report Button:** Creates a comprehensive PDF report summarizing your health metrics and trends over the past week. The report will be saved in the application directory.

### 7.5. ⚙️ Settings

This tab allows you to configure various aspects of the application.

-   **Connection Settings:**
    -   **ESP32 IP Address:** If you didn't hardcode the IP in `enhanced_main.py`, you can enter your ESP32's IP address here. Click "Reconnect" to establish a new connection.
-   **Detection Thresholds:**
    -   **Blink Detection Threshold:** Adjust this value to fine-tune the sensitivity of blink detection. A higher value requires a stronger signal change to register a blink.
    -   **Apply Settings Button:** Click to save your changes.

## 8. Troubleshooting Common Issues

-   **"Status: Disconnected" or "Connection Error"**: 
    -   **Check ESP32:** Ensure your ESP32 is powered on, connected to the same Wi-Fi network as your laptop, and the firmware is running (check Serial Monitor).
    -   **Verify IP Address:** Double-check that the ESP32 IP address configured in `enhanced_main.py` (or entered in the Settings tab) is correct and matches the IP shown in the ESP32 Serial Monitor.
    -   **Firewall:** Your computer's firewall might be blocking the connection. Temporarily disable it or add an exception for Python.
-   **No Signal Data / Flat Graphs**: 
    -   **BioAmp Connection:** Ensure the BioAmp sensor is correctly wired to the ESP32.
    -   **Electrode Contact:** Verify that the electrodes are making good, consistent contact with your skin. Clean the skin and electrodes if necessary.
    -   **BioAmp Power:** Confirm the BioAmp is receiving power.
-   **Blink Detection Not Reliable**: 
    -   **Adjust Threshold:** Go to the `Settings` tab and adjust the "Blink Detection Threshold." Experiment with higher or lower values.
    -   **Electrode Placement:** Ensure EEG electrodes are placed optimally for capturing blink artifacts (typically on the forehead).
-   **Emergency Alerts Not Sending Emails**: 
    -   **Email Configuration:** Re-check your `email_config` in `wow_features.py`. Ensure the email address, app password (for Gmail), and recipient addresses are correct.
    -   **Internet Connection:** Verify your laptop has an active internet connection.
    -   **SMTP Server/Port:** Ensure `smtp_server` and `smtp_port` are correct for your email provider.
-   **Application Freezes/Slows Down**: 
    -   **System Resources:** Close other demanding applications. 
    -   **Sampling Rate:** If you modified the `delay()` in ESP32 firmware to be very low, it might be sending too much data. Increase the `delay()` value.
    -   **Plotting Frequency:** The graphs update every second. If your system is struggling, you might need to optimize the plotting or reduce the update frequency (in `update_plots` function in `enhanced_main.py`).

## 9. Future Enhancements and Ideas

Here are some ideas for further enhancing the NeuroBand system, building upon the current foundation:

### 9.1. Advanced Signal Processing and Machine Learning

-   **Personalized Calibration:** Implement a guided calibration routine where the user performs specific actions (e.g., blinks, focus/relax) to train a personalized machine learning model for more accurate signal interpretation and control.
-   **Emotion Recognition Refinement:** Integrate more sophisticated machine learning models (e.g., SVM, Neural Networks) trained on a larger dataset of biosignals and corresponding emotional states for more nuanced emotion detection.
-   **Artifact Removal:** Implement advanced signal processing techniques (e.g., Independent Component Analysis - ICA) to automatically remove eye blinks, muscle movements, and other artifacts from EEG signals, leading to cleaner data for analysis.
-   **Sleep Stage Detection:** Extend EEG analysis to detect different sleep stages (REM, NREM stages) for sleep quality monitoring.

### 9.2. Enhanced Brain Control Features

-   **Gaze Tracking Integration:** Combine brain signals with eye-gaze tracking (using a webcam) for more precise cursor control and selection, offering a hybrid BCI approach.
-   **Virtual Keyboard:** Develop a brain-controlled virtual keyboard where users can type by focusing on letters or using specific brain patterns.
-   **Application-Specific Profiles:** Allow users to create custom brain control profiles for different applications or games, optimizing sensitivity and actions for specific tasks.
-   **Voice Command Integration:** Integrate speech recognition to allow users to combine brain commands with voice commands for a more natural interaction.

### 9.3. "World-Class" UI/UX Enhancements (Conceptual)

While the current application uses `tkinter` with some enhancements, a truly "world-class" UI/UX would involve a complete migration to a more powerful framework like **PyQt/PySide** (as discussed in the `ui_ux_strategy.md` and `ui_ux_design_document.md`). This would enable:

-   **Sophisticated Data Visualizations:** Implement custom, animated 3D brain models that show real-time brain activity, heatmaps of neural engagement, and fluid, interactive graphs with zooming and panning capabilities.
-   **Motion Graphics and Micro-interactions:** Integrate subtle yet impactful animations for every interaction – buttons glowing on hover, data points smoothly transitioning, dynamic backgrounds reacting to stress levels, and animated icons for emotional states.
-   **Themed Interface:** A professional, dark-themed interface with customizable accent colors, allowing users to personalize their experience.
-   **Responsive Design:** Ensure the UI adapts seamlessly to different screen sizes and resolutions.
-   **Haptic Feedback Integration:** If the headband includes a vibration motor, integrate haptic feedback for certain events (e.g., successful blink detection, high stress alert).

### 9.4. Innovative "Wow" Features

-   **Biofeedback Training Modules:** Develop interactive biofeedback games or exercises that help users learn to control their brainwaves (e.g., increase Alpha for relaxation, increase Beta for focus) or heart rate variability, with real-time visual and auditory feedback.
-   **Smart Home Integration:** Allow brain signals to control smart home devices (e.g., turn lights on/off, adjust thermostat) via a central hub or API.
-   **Augmented Reality (AR) Overlay:** (Future concept) If paired with AR glasses, project BCI controls and health metrics directly into the user's field of vision.
-   **Personalized Mental Wellness Journeys:** Based on long-term data, the system could suggest personalized mindfulness exercises, sleep recommendations, or cognitive training programs.
-   **Social Sharing and Community:** (Optional, with privacy considerations) Allow users to securely share their progress or insights with friends, family, or a supportive community.
-   **Gamified Health Challenges:** Introduce challenges and rewards to encourage users to maintain healthy stress levels, improve focus, or engage in mindfulness practices.

### 9.5. Data Logging and Cloud Integration (Optional)

-   **Secure Cloud Storage:** Offer an option for users to securely store their long-term biosignal data in a cloud database (e.g., Firebase, AWS S3) for advanced analysis and backup.
-   **Web Dashboard Enhancement:** Expand the optional Flask-based web dashboard to include more interactive charts, historical data analysis, and remote monitoring capabilities for authorized users.

## 10. Conclusion

The NeuroBand system, with its current capabilities and the proposed enhancements, represents a powerful tool for personal well-being and human-computer interaction. This guide provides the foundation for setting up and utilizing the system. By continuously exploring advanced signal processing, innovative control mechanisms, and a world-class user experience, the NeuroBand can evolve into an indispensable companion for managing mental health, enhancing productivity, and unlocking new forms of interaction with technology.


