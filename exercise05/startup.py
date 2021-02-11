import os
import logging
from os.path import expanduser
home = expanduser("~")

folder_path = os.path.join(home, ".ex05")
subdir_path = os.path.join(folder_path, "ruppasur")
log_path=os.path.join(subdir_path,'log')
data_path=os.path.join(subdir_path,'data')
if os.path.isdir(log_path) is False:  # If false, assumes other directories were not made yet
    os.mkdir(folder_path)
    os.mkdir(subdir_path)
    os.mkdir(log_path)
    os.mkdir(data_path)
    logging.basicConfig(filename=os.path.join(log_path, 'sample.log'),
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug("The directories were created successfully!")

else:  # Log folder is there and assumes other directories were made
    logging.basicConfig(filename=os.path.join(log_path, 'sample.log'),
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("Directory Already Exists!")





# full correct