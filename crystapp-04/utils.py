#!/usr/bin/env python
import os

def file_exists(path):
    if os.path.exists(path):
        return True
    return False
