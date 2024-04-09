import cv2
import os
import re
import pymongo
from dotenv import load_dotenv
import pytesseract as tess
from PIL import Image
from tkinter import messagebox
tess.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

# Load environment variables from .env file
load_dotenv()

#variable declaration
min_area = 500
count = 0
mongodb_uri = "mongodb+srv://js9316713287:js9316713287@cluster0.f016fd1.mongodb.net/"
database_name = "test"
collection = "students"

def preprocess_image(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    # Perform adaptive thresholding to binarize the image
    threshold_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return threshold_image


def preprocess_text_method(text) :
    # Remove non-alphanumeric characters and whitespace
    text = re.sub(r'[^a-zA-Z0-9]', '', text)
    # Convert text to uppercase
    text = text.upper()
    return text

#mongodb connection 
my_client = pymongo.MongoClient(mongodb_uri)
database = my_client[database_name]
studentCollection = database[collection]

def is_matched_registration_number(vehicle_Number) :
     # Query database for matching registration number
    query = {"numberPlate":vehicle_Number}
    print(query)
    result = studentCollection.find_one(query)
    print(result)
    
    if result:
        # If a match is found, return the details
        return result
    else:
        return False

#harcascade model training  dataset
harcascade = 'model/haarcascade_russian_plate_number.xml'

cap = cv2.VideoCapture(0)

cap.set(3 , 840)
cap.set(4 , 580)

while True:
    success , img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray , 1.1 , 2 )

    for(x , y , w , h) in plates :
        area = w * h

        if area > min_area:
            cv2.rectangle(img , (x,y) , (x+w , y+h) , (0,255,0) , 2)
            cv2.putText(img , "Number Plate" , (x , y - 5) , cv2.FONT_HERSHEY_COMPLEX_SMALL , 1 , (255,0,255) , 2)

            img_Roi = img[y: y+h , x : x+w]
            cv2.imshow("ROI" , img_Roi)
            


    cv2.imshow("Result" , img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('Plates/scaned_img_' + str(count) + ".jpg" , img_Roi)
        cv2.rectangle(img , (0,200) , (640,300) , (0,250,0) , cv2.FILLED)
        cv2.putText(img , "Plate Saved" , (150 , 265) , cv2.FONT_HERSHEY_COMPLEX_SMALL , 2 , (0,0.255) , 2)
        cv2.waitKey(500)
        saved_image_path = 'Plates/scaned_img_' + str(count) + ".jpg"
        
        savedImage = cv2.imread(saved_image_path)
        
        #extracting text from the image
        vehicle_Number = tess.image_to_string(savedImage , lang='eng')
        
        if savedImage is not None:
            savedImage = preprocess_image(savedImage)
            vehicle_Number = tess.image_to_string(savedImage, lang='eng')
        else:
            print("Error: Failed to read the saved image file.")
        
        #method to remove the noise or unwanted characters(like #//>|\) that are not alphanumeric
        vehicle_Number = preprocess_text_method(vehicle_Number)

        # Method to match the extracted text from the camera with the database
        matched_entry = is_matched_registration_number(vehicle_Number)

        if matched_entry:
            print('Successfull')
            messagebox.showinfo("Query Successfull" , "The vehicle is registered in the database.")
        else :
            print("not matched")
            messagebox.showinfo("Matching Failed!" , "The vehicle is not registered in the database. It might be an Outsider.")
            
        print(vehicle_Number)
        count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        os.remove('Plates/')
        break
