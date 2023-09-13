
import os


#start a process
os.system("python3.9 client_listener/mod_client_listener2.py")
print('Started the process')

#kill a process
os.system("pkill -f mod_client_listener2.py")
