Note: python3.x is the version of python that you are using. For example, if you are using python 3.6, then you should use python3.6 instead of python3.x.
Recommend to use python 3.11

1. Set the working directory to "./GestProj" and run ```python3.x main.py``` to start the program.
2. If you want to reset all the training data, run ``` python3.x remover.py ``` and follow the instructions.
3  For missing packages, install the following:
	a) numpy
	b) pandas
	c) tensorflow & keras
	d) opencv
	e) matplotlib
   
   If you want to install for a specific python version using pip, you can use: ```python3.x -m pip install <package>```

4. If you intend to completely reset the model (remove all the previously learned weights), navigate to "./GestProj/rootfold" and manually delete the file "model_lowres.keras". 
   Next time the program starts, it'll start off with a completely new model.


------------------------------------------------------------------------------------------------------------

What are the gestures that the program can recognize?

       ____Table_1_____
	0. No gesture
	1. Index finger pointing up
	2. V sign
	3. "Three" sign
	4. "Four" sign
	5. "Five" sign

Open "gestures.png" to see the images of the gestures. 

The mapping is exactly the same as index vs description as given in Table 1.


------------------------------------------------------------------------------------------------------------
