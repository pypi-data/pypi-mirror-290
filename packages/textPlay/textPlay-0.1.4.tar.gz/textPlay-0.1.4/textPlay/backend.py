'''
# Helps to run commands in backend

Functions:
    - backend_subprocess(command): Executes the given command in the background using the subprocess module.
    - backend_suppress(command): Executes the given command in the background and suppresses its output.
    - backend_exec(command): Executes the given command in the background and captures its output.
'''

import os
import subprocess

def backend_subprocess(command):
    """
    Executes the given command in the background using the subprocess module.

    Parameters:
    - command (str): The command to be executed.

    Notes:
    - This function uses the subprocess.run() method to execute the given command.
    - The command is executed in a separate process using the shell=True parameter.
    - The check=True parameter is used to raise an exception if the command returns a non-zero exit status.

    Raises:
    - Exception: If the command returns a non-zero exit status.

    Example:
    >>> backend_subprocess("echo 'Hello, World!'")

    Output:
    Hello, World!
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

def backend_suppress(command):
    """
    Executes the given command in the background and suppresses its output.

    Parameters:
    - command (str): The command to be executed.

    Notes:
    - This function uses the subprocess.check_call() method to execute the given command.
    - The command is executed in a separate process.
    - The output of the command is suppressed by redirecting it to the null device (os.devnull).

    Example:
    >>> backend_suppress("echo 'Hello, World!'")

    Output:
    (No output is displayed)
    """
    with open(os.devnull, "w") as devnull:
        command = command.split(" ")
        subprocess.check_call(command, stdout=devnull, stderr=subprocess.STDOUT)


def backend_exec(command):
    """
    Executes the given command in the background and waits for it to complete.

    Parameters:
    - command (str): The command to be executed.

    Notes:
    - This function uses the os.system() method to execute the given command.
    - The command is executed in a separate process and waits for it to complete before continuing.
    - The output of the command is displayed in the terminal.

    Example:
    >>> backend_exec("echo 'Hello, World!'")

    Output:
    Hello, World!
    """
    os.system(command)
