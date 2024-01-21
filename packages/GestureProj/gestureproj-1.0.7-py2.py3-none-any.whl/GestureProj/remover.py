import os
import sys
sys.path.append('./rootfold/')
import remover__
os.chdir('./rootfold/')

#generate a random number between 1000000000 and 9999999999
import random
randomnumber = random.randint(1000000000,9999999999)
print("Enter: ",randomnumber," to confirm deletion of all saved data.")
print("Press Ctrl+C to cancel.")

try:
    while not input() == str(randomnumber):
        print("Incorrect input. Enter again.")
        print("Enter: ",randomnumber," to confirm deletion of all saved data.")

except KeyboardInterrupt:
    print("\nDeletion aborted.")
    exit()

remover__.delall()
