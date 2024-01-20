def delall():
	import os
	import pandas as pd
	os.system('rm -rf 0')
	os.system('rm -rf 1')
	os.system('rm -rf 2')
	os.system('rm -rf 3')
	os.system('rm -rf 4')
	os.system('rm -rf 5')
	os.system('rm -rf log.csv')
	for i in range(6):
		os.mkdir(str(i))
	
	#generate a new log.csv
	log=pd.DataFrame()
	log.to_csv('log.csv',index=False)

	print("All saved data has been deleted.")
