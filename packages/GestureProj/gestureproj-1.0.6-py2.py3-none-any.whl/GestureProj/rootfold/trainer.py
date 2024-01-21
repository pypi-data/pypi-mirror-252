def train():
    import tensorflow as tf
    import numpy as np
    import keras
    import os
    import matplotlib.pyplot as plt
    import data_capture
    import global_main
    import time
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # Load the saved model
    try:
        model = keras.models.load_model('model_lowres.keras')
    except:
        print("No model found")
        print("Building init model")
        build_backup_model()

    # Load the dataset
    full_filelist = ['./' + str(i) + '/' + str(j) for i in range(0, 6) for j in os.listdir('./' + str(i))]

    # Shuffle the dataset
    np.random.shuffle(full_filelist)

    # Split the dataset into training and validation sets
    split = int(0.8 * len(full_filelist))
    train_list = full_filelist[:split]
    #split the rest into validation and test sets
    split_2 = int(0.5 * len(full_filelist[split:]))
    val_list = full_filelist[split:split+split_2]
    test_list = full_filelist[split+split_2:]



    def load_data(filelist):
        images = []
        labels = []
        for file in filelist:
            images.append(plt.imread(file))
            labels.append(int(file.split('/')[1]))
        return np.array(images), np.array(labels)

    # Load the training and validation sets
    x_train, y_train = load_data(train_list)
    x_val, y_val = load_data(val_list)
    x_test, y_test = load_data(test_list)

    #load model
    model=keras.models.load_model('model_lowres.keras')
    # Train the model
    train_start_time = time.time()
    history = model.fit(x_train, y_train, epochs=10, validation_data=(x_val, y_val))
    train_end_time = time.time()
    print("Training time: ", train_end_time - train_start_time, "seconds")
    print("Test accuracy: ", model.evaluate(x_test, y_test)[1])

    # Save the model
    model.save('model_lowres.keras')
    print("Model saved successfully")
    print("How do you want to proceed?")
    user_arg = data_capture.y_n("Continue to Main Page/Exit (0/1): ", ['0', '1'], "Please enter a valid input (0/1): ")
    if user_arg == '0':
        global_main.mainpage()
    else:
        # Exit the program without raising an error
        return


def build_backup_model():
    import tensorflow as tf
    import numpy as np
    import keras
    import os

    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation

    # Create a Sequential model
    model = Sequential()

    # First Convolutional Layer
    model.add(Conv2D(15, (6, 6), input_shape=(32, 32, 3)))  # Assuming RGB images
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Activation('relu'))

    # Second Convolutional Layer
    model.add(Conv2D(10, (3, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Activation('relu'))

    # Flatten the output before the fully connected layer
    model.add(Flatten())

    # Fully Connected Layer
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))  # Dropout layer with a probability of 0.5

    # Output layer for multi-class classification
    model.add(Dense(6, activation='softmax'))  # Assuming 6 classes, adjust accordingly

    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Display the summary of the model
    model.summary()

    # Save the model
    model.save('model_lowres.keras')
