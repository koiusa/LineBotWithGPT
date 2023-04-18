import os
import glob


class info:
    def get_taskfiles():
        print(os.getcwd())
        files = glob.glob("{}/*".format(os.getcwd()))
        print(files)
