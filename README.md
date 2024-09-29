# Smart Prescription Medicine Vending Machine

## Project Overview

The **Smart Prescription Medicine Vending Machine (SPMVM)** is an innovative system designed to automate the dispensing of prescription medications. The machine accepts inputs through a manual graphical user interface (GUI), a web-based system via QR code scanning, and voice commands. By integrating advanced technologies such as image processing, voice recognition, and continuous servo motor control, this system ensures accurate and efficient dispensing of medicines. The project aims to improve the accessibility, accuracy, and user-friendliness of medication dispensing.

## Screenshots

![image](https://github.com/user-attachments/assets/ff997168-4c95-4057-9401-9535effec5bc)

![image](https://github.com/user-attachments/assets/f85d1d2b-553c-4bab-ad9c-67b0c7545b40)

![image](https://github.com/user-attachments/assets/46891641-ba9c-4eae-8284-2c2135263d10)

![image](https://github.com/user-attachments/assets/83f3c1dc-1b3b-4224-99c3-8fedf1ba9219)

![image](https://github.com/user-attachments/assets/a592e287-3b12-4f2d-a916-77c264c7213b)

## Features

- **Manual Input via GUI**: Users can select medications through a touchscreen interface, displaying available medicines, their images, and prices.
- **QR Code Scanning and Prescription Upload**: Users can scan a QR code to access a web page where they can upload a computer-written prescription image. The system uses OCR (Optical Character Recognition) to process and extract the required medication.
- **Voice Command Dispensing**: Users can issue voice commands to request medications, using Google Speech-to-Text API for accurate recognition.
- **Automated Dispensing Mechanism**: The system uses a spring-loaded mechanism powered by DS04-NFC continuous servo motors, controlled by a NodeMCU ESP8266 microcontroller, to dispense the correct medication.
- **Real-Time Database and Inventory Management**: Integrated with Firebase for real-time inventory tracking. The system updates stock levels after each dispensing action, displaying out-of-stock alerts and low inventory warnings on the GUI and web page.

## Technologies Used

- **Hardware**:
  - **Intel Core i3 M-Generation Processor**: Handles image processing and graphical user interface operations.
  - **NodeMCU ESP8266 Microcontroller**: Manages motor control and Wi-Fi communication.
  - **DS04-NFC Continuous Servo Motors**: Powers the spring-loaded dispensing mechanism.
  - **Acrylic Sheets**: Used for the machine's structure, providing durability and cost-effectiveness.
  
- **Software**:
  - **Python with Pytesseract**: For OCR (Optical Character Recognition) to process prescription images.
  - **Flask**: For hosting the local web page used for prescription upload.
  - **Google Speech-to-Text API**: For processing voice commands.
  - **Firebase**: For real-time database management and inventory tracking.
  - **HTML/CSS**: Used for the front-end design of the web interface.
  - **Tkinter/CustomTkinter**: For GUI development on the machine.

## How It Works

1. **Manual Input (GUI)**: The user selects a medication via the touchscreen. The system sends the selection to the ESP8266, which activates the corresponding servo motor to dispense the medication.

2. **QR Code Scanning**: After scanning a QR code, the user uploads a computer-written prescription image to a web page. The image is processed using OCR to extract the medication name. The ESP8266 then triggers the motor for dispensing.

3. **Voice Commands**: The user clicks the mic button on the GUI and speaks the name of the medication. The system processes the voice command using Google’s API and dispenses the correct medication.

4. **Real-Time Updates**: After dispensing, the system updates inventory levels in the Firebase database and reflects the changes on the web page. If a medication runs out or drops below a set threshold, the system marks it in red and stops further dispensing.

## Installation and Setup

1. **Hardware Setup**:
   - Assemble the vending machine using the provided acrylic sheets and integrate the necessary components (ESP8266, servo motors, etc.).
   - Connect the touchscreen display to the Intel Core i3 processor for GUI interaction.

2. **Software Setup**:
   - Clone the project repository from [GitHub] (add your GitHub repository link).
   - Install the required libraries using `pip`:
     ```bash
     pip install flask pytesseract firebase-admin google-api-python-client
     ```
   - Set up Firebase for real-time database management and configure it in the `firebase_config.py` file.
   - Start the Flask server for the web interface:
     ```bash
     python app.py
     ```

3. **Run the System**:
   - Launch the GUI interface using Python (`main.py`).
   - The system will be ready to accept inputs via GUI, QR code, and voice commands.

## Usage

1. **Manual Mode**: Select medication on the GUI and click "Buy."
2. **QR Code Mode**: Scan the QR code and upload the prescription image for OCR processing.
3. **Voice Command Mode**: Click the mic button on the GUI and say the name of the medication.

## Future Enhancements

- Integration with electronic health records (EHR) for automatic prescription verification.
- Expanding the database to handle a larger variety of medications.
- Improved voice recognition support for multiple languages.
- Remote monitoring of machine performance and inventory levels.

## Funding

This project is Funded by Pakistan Engineering Concil(PEC)

## Contact

For further inquiries or support, contact at farhanahmad@engineer.com
