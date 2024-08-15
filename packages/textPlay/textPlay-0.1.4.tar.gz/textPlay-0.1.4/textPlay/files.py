'''
# Manipulate between Files creation, deletion, read, write and more

Functions:
    - crt_dir(folder_name: str, exist= True): create folder from current directory 
    - crt_file(file_name): create file from current directory
    - del_file(file_name): delete file from current directory
    - del_folder(file_name): delete folder from current directory
    - rename_folder(old_fld, new_fld): rename folder from current directory
    - move_folder(old_fld, new_fld): move folder from current directory
    - list_dir(dir): list folder from current directory
    - write_file(file_name, content='', tell_me= True): write file from current directory
    - read_file(file_name): read file from current directory
'''

import os

USER = os.path.expanduser("~/")

def crt_dir(folder_name: str, exist= True):
    """
    # create folder from current directory to folder_name
    """
    os.makedirs(folder_name, exist_ok= exist)

def del_file(file_name):
    """
    # delete file from current directory to file_name
    """
    os.remove(file_name)

def del_folder(file_name):
    """
    # delete folder from current directory to file_name
    """
    os.rmdir(file_name)

def rename_folder(old_fld, new_fld):
    """
    # rename folder from current directory to old_fld to new_fld
    """
    os.rename(old_fld, new_fld)

def move_folder(old_fld, new_fld):
    """
    # move folder from current directory to old_fld to new_fld
    """
    os.rename(old_fld, new_fld)

def list_dir(dir):
    """
    # list folder from current directory to dir
    """
    return os.listdir(dir)

def write_file(file_name, content='', tell_me= True):
    """
    # write file from current directory to file_name
    """
    if content == '':
        with open(file_name, 'w') as fh:
            pass
    else:
        with open(file_name, 'w') as fh:
            fh.write(content)

    if tell_me:
        print("File Written sucessfully")


def read_file(file_name):
    """
    # read file from current directory to file_name
    """
    with open(file_name, 'r') as fh:
        read = fh.read()
        return read
            