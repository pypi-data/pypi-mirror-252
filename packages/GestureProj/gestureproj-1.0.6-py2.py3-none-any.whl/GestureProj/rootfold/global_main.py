#ask the user to whether update the model or just proceed with detection
def mainpage():
    import os
    import trainer
    import cvfeed
    import data_capture

    print("Welcome to the main page")
    user_stuff=data_capture.y_n("Do you want to detect gestures or proceed with other options? (0/1): ",['0','1'],"Please enter a valid input (0/1)")

    if user_stuff == '0':
        cvfeed.livecam()
    else:
        data_capture.master()

if __name__=="__main__":
    mainpage()