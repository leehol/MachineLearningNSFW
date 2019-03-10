import os
from shutil import rmtree
CURRENT_PATH = os.getcwd()

def make_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError as e:
        print "Directory was not created: %s... \n%s" % (dir_name, e)
    else:
        print "Successfully created directory: %s" % dir_name


def del_dir(dir_name):
    try:
        rmtree(dir_name)
    except OSError as e:
        print "Directory was not deleted: %s... \n%s" % (dir_name, e)
    else:
        print "Successfully deleted directory: %s" % dir_name

