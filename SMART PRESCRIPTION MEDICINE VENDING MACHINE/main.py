from flask import Flask, request, render_template
import speech_recognition as sr
import customtkinter as ctk
import pytesseract as tess
import sounddevice as sd
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import threading
import pyttsx3
import wavio
import serial
import os
import time
import cv2
import re
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate(r'C:\Users\User\OneDrive\Desktop\FYP\FYP6\credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def reduce_product_count(product_name):
    # Reference to the document of the specified product
    product_ref = db.collection('products').document(product_name)

    # Get the document snapshot
    product_doc = product_ref.get()

    if product_doc.exists:
        # Convert the document snapshot to a dictionary
        product_data = product_doc.to_dict()
        # Reduce the number of products by 1
        new_count = product_data.get('count') - 1
        product_ref.update({'count': new_count})

        print(f"Successfully reduced the count of {product_name} by 1.")
        
    else:
        print(f"No product found with the name {product_name}.")

folder_path = r"S:\FYP\FYP\New folder\image"
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Configure the serial connection
ser = serial.Serial('COM9', 115200)  # Replace 'COM8' with the appropriate port

ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
duration =8
fs = 44100 

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    
def find_detected_words(string, words):
    detected_words = {}
    for word in words:
        if word in string:
            text_to_speech(word)
            detected_words[word] = True
    return detected_words



class MedicineVendingMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Medicine Vending Machine")

        # Set the background color to "ice blue"
        self.root.configure(bg="#b3e0ff")  # You can adjust the color code as needed
        
        self.medicines = [
            ("Panadol", "med1.png", "$10"),
            ("Bruffen", "med2.png", "$15"),
            ("Calpol", "med3.png", "$8"),
            ("Tramal", "med4.png", "$12"),
            ("Oxycodone", "med5.png", "$7"),
            ("Flygal", "med6.png", "$9"),
        ]

        self.create_ui()

    def create_ui(self):
        # Navigation Bar
        nav_bar = tk.Frame(self.root, bg="#2c3e50")  # Set the navigation bar background color
        nav_bar.pack(fill=tk.X)

        logo_image = tk.PhotoImage(file="med9.png")  # Replace with the actual path to your company logo
        logo_image_resized = logo_image.subsample(3, 3)  # Resize the image by a factor of 2
        logo_label = tk.Label(nav_bar, image=logo_image_resized, bg="#2c3e50")
        logo_label.photo = logo_image_resized
        logo_label.pack(side=tk.LEFT, padx=10)

        company_label = tk.Frame(nav_bar, bg="#2c3e50")  # Set the navigation bar background color
        company_label.pack(fill=tk.X)
        # Company Name
        company_name_label = tk.Label(company_label, text="FIZ", font=("Helvetica", 18), fg="white", bg="#2c3e50")
        company_name_label.pack(side=tk.LEFT, padx=10)

        company_label1 = tk.Frame(nav_bar, bg="#2c3e50")  # Set the navigation bar background color
        company_label1.pack(fill=tk.X)
         # Company Description
        company_description_label = tk.Label(company_label1, text="Prescription Precision, Instant Medication: Your Health, Automated for Your Convenience.",
                                              font=("Helvetica", 12), fg="white", bg="#2c3e50")
        company_description_label.pack(side=tk.LEFT, padx=10)

        med_row1 = tk.Frame(self.root, bg="#b3e0ff")  # Set the frame background color
        med_row1.pack(expand=True, fill=tk.BOTH,padx=(250,0))

        med_row2 = tk.Frame(self.root, bg="#b3e0ff")  # Set the frame background color
        med_row2.pack(expand=True, fill=tk.BOTH,padx=(250,0))

        for index, (med_name, med_image, med_price) in enumerate(self.medicines):
            med_frame = tk.Frame(med_row1 if index < 3 else med_row2, bg="#b3efff")  # Set the frame background color
            med_frame.pack(side=tk.LEFT, pady=10,padx=10)

            user_image = Image.open(med_image)  # Replace "user1.png" with the actual image file
            user_image = user_image.resize((200, 200))
            image = ImageTk.PhotoImage(user_image)

            med_image_label = tk.Label(med_frame, image=image)  # Set the label background color
            med_image_label.image = image
            med_image_label.pack()

            med_label = tk.Label(med_frame, text=med_name, bg="#b3efff")  # Set the label background color
            med_label.pack()

            price_label = tk.Label(med_frame, text=f"Price: {med_price}", bg="#b3efff")  # Set the label background color
            price_label.pack()

            # Set the button background color to white
            button = ctk.CTkButton(med_frame, text="Buy", command=lambda name=med_name: self.buy_medicine(name), fg_color=("#DB3E39", "#821D1A"))
            button.pack(pady=10)

        # Add a button with an image and label below it at the end of med_row1
        speak_button_image = tk.PhotoImage(file="mic.png")  # Replace with the actual path to your speak button image
        speak_button_image_resized = speak_button_image.subsample(2, 2)  # Resize the image by a factor of 2
        speak_button = tk.Button(med_row1, image=speak_button_image_resized, text="Speak", compound=tk.TOP, command=self.speak_command, font=("Helvetica", 14),bg="#b3e0ff")
        speak_button.photo = speak_button_image_resized
        speak_button.pack(side='right' , padx=70)

        # Add an image with a label below it at the end of med_row2
        additional_image = tk.PhotoImage(file="qrcode.png")  # Replace with the actual path to your additional image
        additional_image_resized = additional_image.subsample(2, 2)  # Resize the image by a factor of 2
        additional_image_label = tk.Label(med_row2, image=additional_image_resized, text="Scan QR", compound=tk.TOP, font=("Helvetica", 14),bg="#b3e0ff")
        additional_image_label.photo = additional_image_resized
        additional_image_label.pack(side='right' , padx=70)

        self.output_label = tk.Label(self.root, text="", bg="#b3e0ff")  # Set the label background color
        self.output_label.pack()  # Pack the output_label widget

    def buy_medicine(self, medicine_name):
        # medicine_number = int(medicine_name.split(" ")[-1])
        # ser.write(str(medicine_number).encode())
        text = text.lower()
        search_keywords = {
            "panadol": 1,
            "bruffen": 2,
            "calpol": 3,
            "tramal": 4,
            "oxycodone": 5,
            "flagyl": 6    
        }

        detected_words = find_detected_words(text, search_keywords.keys())

        for keyword, value in search_keywords.items():
            if detected_words.get(keyword):
                
                ser.write(str(value).encode())

                print(f"Detected: {keyword} (Sending: {value})")
                time.sleep(3.5)

                print("-" * 30)

        reduce_product_count(medicine_name)
        print(f"You bought: {medicine_name}")
        self.output_label.config(text=f"You bought: {medicine_name}")

    def speak_command(self):
        print("Speak command executed.")
        text_to_speech('Welcome to FIZ. Please speak the medicine name you want to buy!')
        
        audio_data = sd.rec(int(fs * duration), samplerate=fs, channels=2, dtype=np.int16)
        print(f"Recording for {duration} seconds...")
        sd.wait()

        # List of patterns with fixed number of characters between starting and ending alphabets
        patterns = [r'\bp.{5}l\b', r'\bb.{5}n\b', r'\bB.{4}n\b', r'\bp.{6}e\b',r'\bc.{4}l\b',r'\bt.{4}l\b',r'\bt.{5}e\b', r'\bf.{4}l\b', r'\bo.{7}e\b', r'\bo.{9}e\b']

        # Dictionary of replacements
        replacements = {
            r'\bp.{5}l\b': 'Panadol',
            r'\bb.{5}n\b': 'Bruffen',
            r'\bB.{4}n\b': 'Bruffen',
            r'\bc.{4}l\b': 'Calpol',
            r'\bt.{5}e\b': 'Tramal',
            r'\bt.{4}l\b': 'Tramal',
            r'\bf.{4}l\b': 'Flagyl',
            r'\bp.{6}e\b': 'Flagyl',
            r'\bo.{7}e\b': 'Oxycodone',
            r'\bo.{9}e\b': 'Oxycodone'
        }


        file_name = "recorded_audio.wav"
        wavio.write(file_name, audio_data, fs, sampwidth=2)

        
        recognizer = sr.Recognizer()
        file_path = "recorded_audio.wav"
        print("Recording End...")
        with sr.AudioFile(file_path) as source:
            #recognizer.adjust_for_ambient_noise(source)
            
            audio_data = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio_data)
                for pattern in patterns:
                    # Find all matches in the text
                    matches = re.findall(pattern, text)

                    # Replace matches with corresponding words
                    for match in matches:
                        replacement = replacements.get(pattern)
                        text = re.sub(re.escape(match), replacement, text)


                print(f"Transcription: {text}")
                text_to_speech(text)
                text = text.lower()

                search_keywords = {
                    "panadol": 1,
                    "bruffen": 2,
                    "calpol": 3,
                    "tramal": 4,
                    "oxycodone": 5,
                    "flagyl": 6
                    
                }

                detected_words = find_detected_words(text, search_keywords.keys())

                for keyword, value in search_keywords.items():
                    if detected_words.get(keyword):
                        
                        ser.write(str(value).encode())

                        print(f"Detected: {keyword} (Sending: {value})")
                        time.sleep(3.5)

                        print("-" * 30)

            except sr.UnknownValueError:
                print("Google Web Speech API could not understand the audio")
                text_to_speech('Sorry I do not understand what you speak!')
            except sr.RequestError:
                print("Could not request results from Google Web Speech API; check your network connection")
                text_to_speech("Could not request results; check your network connection")

def flask_app():
    app = Flask(__name__)
    image_folder = os.path.join(os.getcwd(), 'image')

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            uploaded_file = request.files['fileToUpload']
            if uploaded_file:
                filename = os.path.join(image_folder, uploaded_file.filename)
                uploaded_file.save(filename)
                return render_template('thank.html')

        return render_template('upload.html')

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)


def other_commands():
    while True:
    # List all files in the folder
        files = os.listdir(folder_path)

        if files:
            for filename in files:
                file_path = os.path.join(folder_path, filename)
                
                # Print the file name
                print("New file:", filename)
                
                # Load the image and extract text using Tesseract
                img = cv2.imread(file_path)
                text = tess.image_to_string(img)

                text = text.lower()

                search_keywords = {
                    "panadol": 1,
                    "bruffen": 2,
                    "calpol": 3,
                    "tramal": 4,
                    "oxycodone": 5,
                    "flagyl": 6
                }

                detected_words = find_detected_words(text, search_keywords.keys())

                for keyword, value in search_keywords.items():
                    if detected_words.get(keyword):
                        
                        ser.write(str(value).encode())

                        print(f"Detected: {keyword} (Sending: {value})")
                        time.sleep(3.5)

                        print("-" * 30)
                # Remove the file
                os.remove(file_path)
                print("File removed:", filename)
    else:
        print("No new files found.")
    
    # Wait for a certain interval before checking again
    time.sleep(1)


def tk_main_loop():
    root = tk.Tk()
    root.title("Welcome to the FIZ App!")
    root.attributes("-fullscreen", True)  # Set fullscreen mode

    app = MedicineVendingMachine(root)
    output_label = tk.Label(root, text="", bg="#b3e0ff")
    output_label.pack()
    
    root.mainloop()


def main():
    tk_thread = threading.Thread(target=tk_main_loop)
    other_thread = threading.Thread(target=other_commands)
    flask_thread = threading.Thread(target=flask_app)

    tk_thread.start()
    other_thread.start()
    flask_thread.start()

    tk_thread.join()
    other_thread.join()
    flask_thread.join()

if __name__ == "__main__":
    main()
