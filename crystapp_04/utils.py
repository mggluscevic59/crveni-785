import os
import datetime
import logging


def path_exists(folder_path):
    if os.path.exists(folder_path):
        return True
    return False


def set_filename(file_count=True, timestamp=True, folder=""):
    foo_path = folder

    if timestamp:
        foo_path += datetime.datetime.now().strftime('%Y_%m_%d')
    if file_count:
        counter = 1
        while path_exists(foo_path+"-"+str(counter)+".csv"):
            counter += 1
        foo_path += "-" + str(counter)
    foo_path += ".csv"
    return foo_path


def calc_wait(start:datetime.datetime, stop:datetime.datetime, delay):
    passed = int((stop - start).microseconds*0.001)
    logging.debug("{0:5d} miliseconds".format(passed))
    if passed > delay:
        return 0
    supstracted = delay - passed
    logging.info(f"{supstracted} miliseconds async sleep")
    return supstracted*0.001
