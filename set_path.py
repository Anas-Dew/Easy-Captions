import os
from os import name


def setPath(main_folder,data_folder):
  
    # for windows
    if name == 'nt':
        _ = os.chdir(f'C:/{main_folder}/{data_folder}/')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        username = os.getlogin()
        _ = os.chdir(f'/home/{username}/Projects/{main_folder}/{data_folder}/')

if __name__ == "__main__":
    print("Working fine !")
