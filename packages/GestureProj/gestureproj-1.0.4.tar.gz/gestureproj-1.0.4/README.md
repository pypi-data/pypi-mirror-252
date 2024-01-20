# Gesture Recognition Program Readme

**Note:** Ensure you are using Python 3.x (replace x with your particular version in the subsequent codes). It is recommended to use Python 3.11 for optimal compatibility.

## Getting Started

1. Set the working directory to "./GestProj" and run the following command to start the program:
   ```bash
   python3.x main.py
   ```

2. To reset all training data, run the following command and follow the instructions:
   ```bash
   python3.x remover.py
   ```

3. Install the required packages for the program:
   a) numpy
   b) pandas
   c) tensorflow & keras
   d) opencv
   e) matplotlib

   You can use the following command for package installation (replace `<package>` with the package name):
   ```bash
   python3.x -m pip install <package>
   ```

4. If you wish to completely reset the model (remove all previously learned weights), navigate to "./GestProj/rootfold" and manually delete the file "model_lowres.keras". The program will initialize with a new model on the next startup.
5. New training data generation can be done by running the "main.py" file and then entering $1$ into the console. Afterwards again choose option $1$ to proceed.
6. Choosing option $1$ in the main page reveals some options to handle the dataset- including recording new data (as mentioned earlier), keeping the model up-to-date and viewing a log of different recording sessions.
7. The on-screen instructions allow the user to delete an entire session's data in one go. It is useful if that session has become irrevalent/interferes with general learning of the model.
8. During the first run of the program it's recommended to record at least a a couple of frames for every type, as to not run into any odd exceptions. 

## Gesture Recognition

### Gestures Table

| Gesture ID | Description           |
|------------|-----------------------|
| 0          | No gesture            |
| 1          | Index finger pointing up |
| 2          | V sign                |
| 3          | "Three" sign          |
| 4          | "Four" sign           |
| 5          | "Five" sign           |

Refer to "gestures.png" in "GestureProj" to view images of the gestures. The mapping between the gesture ID and description is consistent with the table above.
