"""
# TextPlay 💬

**Welcome to the TextPlay repository! 👋**  
This versatile Python module provides a range of text-related functions and tools to enhance your text experience in your terminal and projects.

## Functions

1. **GOOGLE SEARCH**
    - g_search(query, num_results=1): Performs a google search with number of search results
    
2. **MORSE CODE**
    - Morse: A class for encoding and decoding text to/from Morse code
    - coder(text): Encodes text to morse code
    - decoder(morse_code): Decodes morse code to text

3. **OPTIONS**
    - options(option, index, head): Displays a menu with options and handles user input for navigation and selection.

4. **PASSWORD GENERATOR**
    - create_password(length = 12): Generate a random password with specified length.

5. **ENCRYPTION ANIMATION**
    - encrypted(word = "Encrypted 🔐", sleep_time=0.1, end_color=BLUE, special_characters="!@#$%^&*()_+-=[]{}|;:,.<>?/"): Simulate the encryption process by displaying random special characters before revealing the actual word.

6. **BOX**
    - create_box(title, content, width_percentage): Create a box with a title and content to display in the terminal.

7. **PROGRESS BAR**
    - progress_bar_loader(length=50, symbol='█', empty_symbol='-', color_on_completion=GREEN): Simulate and display a progress bar incrementing from 0% to 100%.

8. **FILES**
    - crt_dir(folder_name: str, exist= True): create folder from current directory 
    - crt_file(file_name): create file from current directory
    - del_file(file_name): delete file from current directory
    - del_folder(file_name): delete folder from current directory
    - rename_folder(old_fld, new_fld): rename folder from current directory
    - move_folder(old_fld, new_fld): move folder from current directory
    - list_dir(dir): list folder from current directory
    - write_file(file_name, content='', tell_me= True): write file from current directory
    - read_file(file_name): read file from current directory

9. **BACKEND**
    - backend_subprocess(command): Executes the given command in the background using the subprocess module.
    - backend_suppress(command): Executes the given command in the background and suppresses its output.
    - backend_exec(command): Executes the given command in the background and captures its output.

10. **CLI**
    
```bash
textPlay --help
```
or
```bash
textPlay -h
```
To display all the CLI options

```bash
textPlay --version
```
or
```bash
textPlay -v
```
To display the version of textPlay.

```bash
textPlay --menu
```
or
```bash
textPlay -m
```
To display the menu of textPlay.

```bash
textPlay --contact
```
or
```bash
textPlay -c
```
To display the contact details of textPlay.
"""

# __init__.py

from .colors import *
from .Gsearch import g_search
from .morse import Morse
from .options import options
from .password_generator import create_password
from .encrypt_animation import encrypted
from .box import create_box
from .progress_bar import progress_bar_loader
from .cli import textPlay_cli
from .files import crt_dir, del_file, del_folder, rename_folder, move_folder, list_dir, write_file, read_file
from .backend import backend_subprocess, backend_suppress, backend_exec

__all__ = [
    "g_search",
    "Morse",
    "options",
    "create_password",
    "encrypted",
    "create_box",
    "progress_bar_loader",
    "textPlay_cli",
    "crt_dir", "del_file", "del_folder", 
    "rename_folder", "move_folder", 
    "list_dir", "write_file", "read_file",
    "backend_subprocess", "backend_suppress", "backend_exec"
]
