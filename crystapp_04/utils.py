#!/usr/bin/env python
import os
import datetime


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
