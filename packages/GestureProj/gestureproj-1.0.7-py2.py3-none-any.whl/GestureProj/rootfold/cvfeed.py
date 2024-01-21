# Description: This file contains the code for the live webcam feed and the prediction of the model.
def livecam():
    import cv2
    import numpy as np
    #import tensorflow in non-verbose mode
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
    import trainer
    import tensorflow as tf
    import keras
    tryflag=False
    #load keras model in non-verbose mode
    try: model = keras.models.load_model('model_lowres.keras',compile=False)
    except: 
        print("Error: Could not load model.")
        print("Generating new model...")
        trainer.build_backup_model()
        model = keras.models.load_model('model_lowres.keras',compile=False)
        print("Model generated successfully.")
        print("Training model...")
        try: 
            trainer.train()
            print("Model trained successfully.")
            print("Restart the program.")
            tryflag=True
        except: 
            print("Error: Could not train model.")
            print("Please record more data.")
            exit()
    # Open the webcam (you can specify the camera index, usually 0 is the default)
    if tryflag==True:
        exit()
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
    
    print("Press q to quit.\n")
    while True:
        ret, frame = cap.read() # Read a frame from the webcam
        # Check if the frame was successfully read
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.rectangle(frame, (100, 100), (324, 324), (0, 255, 0), 2) # Overlay a bounding box on the frame of size 224x224
        crop = frame[100:324, 100:324]
        frame = cv2.flip(frame, 1) #flip the frame
        cv2.imshow('Webcam', frame)
        crop=cv2.flip(crop,1)
        cv2.imshow('Cropped', crop) # Display the cropped frame
        #downsize the image to 32x32
        crop = cv2.resize(crop, (32, 32))
        crop=np.array(crop)
        #reshape the image to 1x32x32x3
        crop = crop.reshape(1, 32, 32, 3)
        prediction = model.predict(crop,verbose=0)  # Make prediction, non-verbose
        print("Prediction: ", np.argmax(prediction) ,end='\r') # Print prediction and probability
        if cv2.waitKey(1) & 0xFF == ord('q'): # Exit when q is pressed
            break
    cap.release() # Release the camera
    cv2.destroyAllWindows()
