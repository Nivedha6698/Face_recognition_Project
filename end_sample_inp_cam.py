from flask import Flask, request
import cv2
import face_recognition
import numpy as np
import pyodbc

#POST http://localhost:5000/camfaces?image_name=my_image.jpg

app = Flask(__name__)

# Connect to the database
connection_string = 'Driver={SQL Server};Server=DESKTOP-CIRT352;Database=Face_recogntion;Trusted_Connection=yes;'
mydb = pyodbc.connect(connection_string)
cursor = mydb.cursor()

# Create the endpoint for the POST request
@app.route('/camfaces', methods=['GET','POST'])
def faces_read():
    #image name from parameter
    img_filename = request.args.get('image_name')

    #img_name from form
    # img_filename = request.form.get('image_name')
    image = cv2.imread(img_filename)

    # Open a video capture object for the camera
    video_capture = cv2.VideoCapture(0)

    # Display the video capture feed in a window
    cv2.namedWindow("Camera Feed")
    while True:
        # Capture a frame from the video feed
        ret, frame = video_capture.read()

        # Resize the frame for faster processing
        small_frame = cv2.resize(frame, (640,480), fx=0.25, fy=0.25)

        # Display the frame in the window
        cv2.imshow('Camera Feed', small_frame)

        # Check if the user has clicked on the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('c'):
            # User has clicked on the window, so capture the current frame
            rgb_small_frame = small_frame[:, :, ::-1]  # Convert from BGR to RGB

            # Encode the image to JPEG format
            _, img_encoded = cv2.imencode('.jpg', rgb_small_frame)

            # Detect faces in the image
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            # Insert the image data, filename, and ID into the database
            img_data = pyodbc.Binary(img_encoded)
            #img_filename = request.form.get('image_name')
            if img_filename is not None and len(face_encodings) > 0:
                cursor.execute("INSERT INTO images (name, encoding, image) VALUES (?, ?, ?)", img_filename, face_encodings[0].tobytes(), img_data)
                mydb.commit()
            else:
                print("Image name is none or No face detected in the image.")

            # Break out of the loop and close the window
            break

    # Release the camera and database connection
    video_capture.release()
    cursor.close()
    mydb.close()
    cv2.destroyAllWindows()

    return 'Image Uploaded Successfully!'

if __name__ == '__main__':
    app.run()
