import cv2
import numpy as np
import time
import os
import pandas as pd
import trainer
import cvfeed
import global_main

def master():

    #Write the instructions for the user
    print("\nOptions: ")
    print("1. Enter 1 to record gestures")
    print("2. Enter 2 to refresh the model")
    print("3. Enter 3 to delete a session or to take a look at the log file")
    print("4. Enter 4 to quit")

    #Ask the user to enter the choice
    user_input = y_n("Enter your choice: ",['1','2','3','4'],"Please enter a valid input (1/2/3/4): ")
    
    if user_input == '1':
        capture()
    elif user_input == '2':
        refresh()
    elif user_input == '3':
        delete_session()
    else: quit_all()



def quit_all():
    os.system("rm -rf *_temp")
    exit()


def delete_session():

    try: log = pd.read_csv('log.csv',header=None)
    except: 
        print("No sessions found")
        return

    print("Few lines of the log file: ")
    print(log.head())

    log_stamp = log[6].unique()

    print("Session stamps: ", log_stamp)

    #print the session stamps and ask the user to select the session to be processed

    for i in range(len(log_stamp)):
        #print the time in a readable format
        print(i,": ",time.ctime(float(log_stamp[i])))



        #delete the files matching the selected session stamp and remove the session stamp from the log file

    selected_session = input("Select the session to be processed: ")

    selected_session_stamp = log_stamp[int(selected_session)]

    print("Selected session stamp: ", time.ctime(float(selected_session_stamp)))

    selected_session_files = log[log[6]==selected_session_stamp]

    ask_delete = y_n("View/Delete Session (1/2): ",['1','2'],"Please enter a valid input (1/2)")

    if ask_delete == '1':
        #print the session and stop the function
        print("Session not deleted")
        #print the contents of the session
        print("Session contents: ")
        print(selected_session_files)

    else:

        #ask the user to confirm the deletion
        confirm_delete = y_n("Are you sure you want to delete the session? (y/n): ",['y','n'],"Please enter a valid input (y/n)")

        if confirm_delete == 'y':
            for i in range(len(selected_session_files)):
                #from the folders temp_0, temp_1, temp_2, temp_3, temp_4, temp_5, delete the files matching the selected session stamp
                os.remove('0/'+selected_session_files[0].iloc[i])
                os.remove('1/'+selected_session_files[1].iloc[i])
                os.remove('2/'+selected_session_files[2].iloc[i])
                os.remove('3/'+selected_session_files[3].iloc[i])
                os.remove('4/'+selected_session_files[4].iloc[i])
                os.remove('5/'+selected_session_files[5].iloc[i])

            #remove the selected session stamp from the log file
                
            log = log[log[6]!=selected_session_stamp]

            log.to_csv('log.csv',index=False,header=False,mode='w')
            print("Session deleted successfully")
        else:
            print("Session not deleted")

    user_back=y_n("Do you want to go back to the main page? (y/n): ",['y','n'],"Please enter a valid input (y/n)")
    if user_back == 'y':
        global_main.mainpage()
    else:
        exit()


def capture():
    try:
        session_id = time.time()
        print("\nSession Time: ", time.ctime(session_id), "Session ID: ", session_id)
        print("Instructions: ")
        print("1. Press 'r' to record a frame")
        print("2. Number of frames to be recorded per gesture will be the same (to avoid class imbalance)")
        print("3. Press 'q' or 'esc' or 'Ctrl+C' to exit. Exiting will delete the current session, without saving the data.")
        frame_count = int(input("\nEnter the number of frames to be recorded: "))
        temp_dir_list = [str(i) + "_temp" for i in range(6)]
        temp_list = [0, 0, 0, 0, 0, 0]
        key = 0
        index_gesture = 0
        while index_gesture < 6 and key not in (ord('p'), 27):
            try:
                os.mkdir(str(index_gesture) + "_temp")
            except:
                os.system("rm -rf " + str(index_gesture) + "_temp")
                os.mkdir(str(index_gesture) + "_temp")
            gesture_name_file = index_gesture
            print("\nRecording gesture: ", gesture_name_file)
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open webcam.")
                exit()
            count_recorded = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame.")
                    break
                cv2.rectangle(frame, (100, 100), (324, 324), (0, 255, 0), 2)
                crop = frame[100:324, 100:324]
                frame = cv2.flip(frame, 1)
                cv2.imshow('Webcam', frame)
                crop = cv2.flip(crop, 1)
                cv2.imshow('Cropped', crop)
                if count_recorded == frame_count:
                    break
                key = cv2.waitKey(1)
                if key == ord('r'):
                    count_recorded += 1
                    crop = cv2.resize(crop, (32, 32))
                    cv2.imwrite(str(gesture_name_file) + "_temp" + '/' + str(time.time()) + '.png', crop)
                    print("Frames recorded: ", count_recorded, end='\r')
                if key in (ord('q'), 27):
                    exit_flag = True
                    break
            cap.release()
            cv2.destroyAllWindows()
            if key == ord('p'):
                break
            user_happy = input("\nAre you happy with the recording? (y/n): ")
            if user_happy == 'y':
                for name_file in os.listdir(str(gesture_name_file) + "_temp"):
                    os.system("cp " + str(gesture_name_file) + "_temp/" + str(name_file) + " " + str(gesture_name_file) + "/" + str(name_file))
                temp_list[gesture_name_file] = os.listdir(str(gesture_name_file) + "_temp")
                index_gesture += 1
            else:
                os.system("rm -rf " + str(gesture_name_file) + "_temp")
        
        if key in (27, ord('q')):
            print("\nExited.")
            quit_all()
        
        else:
            print("\nRecording complete.")
            filenames_written = pd.DataFrame(columns=['0', '1', '2', '3', '4', '5', 'session_id'])
            for i in range(6):
                filenames_written[str(i)] = temp_list[i]
            filenames_written['session_id'] = session_id
            filenames_written.to_csv('log.csv', mode='a', header=False, index=False)
            os.system("rm -rf *_temp")
            print("Data saved and entries written to the log file")
            user_input=y_n("Do you want to train the model? (y/n): ",['y','n'],"Please enter a valid input (y/n)")
            if user_input == 'y':
                trainer.train()
            else:
                quit_all()

    except KeyboardInterrupt:
        print("\nExiting.")
        quit_all()
        

def refresh():
    print("\nRefreshing the model")
    trainer.train()


def y_n(prompt_line,choices,validity_prompt):
    user_choice=input(prompt_line)
    while user_choice not in choices:
        user_choice=input(validity_prompt)
    return user_choice