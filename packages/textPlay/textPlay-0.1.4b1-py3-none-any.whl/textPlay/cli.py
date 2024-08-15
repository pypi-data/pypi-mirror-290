import webbrowser
import sys
import time
from textPlay.colors import *
from textPlay.options import options
from textPlay.Gsearch import g_search
from textPlay.password_generator import create_password
from textPlay.encrypt_animation import encrypted
from textPlay.morse import Morse
from textPlay.files import *
from textPlay.backend import backend_exec

VERSION = 'v0.1.4'
TITLE = f"{YELLOW}TextPlay {GREEN}{VERSION}{RESET}\n"
FOOTER = f"\n\nRakesh Kanna \n{BLUE}Happy Coding!{RESET}"
breaker = f'\n{YELLOW}--------------------{RESET}'
contact = f'''
Github : {CYAN}https://github.com/rakeshkanna-rk{RESET}
Mail : {CYAN}rakeshkanna0108@gmail.com{RESET}
'''
fle_opr = '''
1. Create Folder
2. Create File
3. Delete Folder
4. Delete File
5. Rename Folder
6. Move Folder
7. List Folder
8. Write File
9. Read File
'''
help_cli = '''Usage: textPlay <option>

Options:
 -h, --help          show this help message and exit
 -v, --version       show the version number and exit
 -m, --menu          Open main menu
 -c, --contact       Get author contact
'''

# COLORS
red = RED
green = GREEN
blue = BLUE
yellow = YELLOW
magenta = MAGENTA
cyan = CYAN
reset = RESET
lit_red = LIGHT_RED

def textPlay_cli():
    print(f"\t{TITLE}")
    try:
        if len(sys.argv) > 2:
            print(f"{RED}Invalid Input Provided{RESET}")
            print(help_cli)


        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print(help_cli)

        elif sys.argv[1] == '--menu' or sys.argv[1] == '-m':
            print(f"{GREEN} Opening Menu...{RESET}")
            time.sleep(2)
            menu()

        elif sys.argv[1] == '--version' or sys.argv[1] == '-v':
            print()

        elif sys.argv[1] == '--contact' or sys.argv[1] == '-c':
            print(contact)

        elif sys.argv[1] == '--fof':
            print(f"{GREEN}Opening File Opration Menu{RESET}")
            time.sleep(2)
            file_opration()

        else:
            print(f"{RED}Invalid Input Provided{RESET}")
            print(help_cli)

    except IndexError :
        print(f"{GREEN} Opening Menu...{RESET}")
        time.sleep(2)
        menu()

    print(FOOTER)

# MENU
def menu():
    options([(f'Web Search {RESET}', lambda: search()),
             (f'Morse Code/Decode {RESET}', lambda: morse()),
             (f'File Operations {RESET}', lambda: files()),
             (f'Password Generator {RESET}', lambda: pws_gen()),
             (f'Colors {RESET}{breaker}', lambda: colors_set()),
             (f'Text Play Tools {RESET}', lambda: tp_tools()),
             (f'{CYAN}Source Code {RESET}', lambda: source_code()),
             (f'{RED}Exit {RESET}\n', lambda: exiting())],
             index=f"{magenta}>",
             head = f"\t{TITLE}")

def exiting():
    print(f"{RED}Exiting...{RESET}")
    sys.exit()

def colors_set():
    print(ALL_COLORS)

# PASSWORD GENERATOR
def pws_gen():
    loop = True
    while loop:
        try:
            len = input("Enter the length of the password [12]: ")
            if len == "":
                len = 12
            loop = False
        except ValueError:
            print(f"{RED}Invalid Input Provided{RESET}")
    psw = create_password(length=int(len))
    encrypted(psw, end_color=GREEN)


# FILES

def file_opration():
    crt_loc = os.getcwd()
    loc = f"{TITLE}\nCurrent Location: {YELLOW}{crt_loc}{RESET}"
    options([(f'Create Folder {RESET}', lambda: fo_crt_dir()),
             (f'Create File {RESET}', lambda: fo_crt_file()),
             (f'Delete Folder {RESET}', lambda: fo_del_folder()),
             (f'Delete File {RESET}', lambda: fo_del_file()),
             (f'Rename Folder {RESET}', lambda: fo_rename_folder()),
             (f'Move Folder {RESET}', lambda: fo_move_folder()),
             (f'List Folder {RESET}', lambda: fo_list_folder()),
             (f'Write File {RESET}', lambda: fo_write_file()),
             (f'Read File {RESET}', lambda: fo_read_file())],
             index=f"{magenta}>",
             head=f"{BLUE}{loc}{RESET}")

def fo_crt_dir():
    file = ask()
    crt_dir(file)
    print(f"{GREEN}Folder created successfully!{RESET}")

def fo_crt_file():
    file = ask()
    write_file(file, tell_me=False)
    print(f"{GREEN}File created successfully!{RESET}")

def fo_del_folder():
    file = ask()
    del_folder(file)
    print(f"{GREEN}Folder deleted successfully!{RESET}")

def fo_del_file():
    file = ask()
    del_file(file)
    print(f"{GREEN}File deleted successfully!{RESET}")

def fo_rename_folder():
    old = ask(f"{BLUE}Enter folder name to rename: {RESET}")
    new = ask(f"{BLUE}Enter new folder name: {RESET}")
    rename_folder(old, new)
    print(f"{GREEN}Folder renamed successfully!{RESET}")

def fo_move_folder():
    old = ask(f"{BLUE}Enter folder name to move: {RESET}")
    new = ask(f"{BLUE}Enter new folder name: {RESET}")
    if not os.path.exists(new):
        move_folder(old, new)
        print(f"{GREEN}Folder moved successfully!{RESET}")
    else:
        new = os.path.join(new, old)
        move_folder(old, new)
        print(f"{GREEN}Folder moved successfully!{RESET}")


def fo_list_folder():
    file = ask()
    lst = list_dir(file)
    for i in lst: 
        print(i)

def fo_write_file():
    file = ask()
    content = input(f"{BLUE}Enter file content: {RESET}")
    write_file(file, content, tell_me=False)
    print(f"{GREEN}File Written sucessfully{RESET}")

def fo_read_file():
    file = ask()
    read = read_file(file)
    print(read)

def files():
    backend_exec("textplay --fof")
        

def ask(text=f"{BLUE}Enter a folder name or location: {RESET}"):
    loop = True
    while loop:
        file = input(text)
        if file == "":
            print(f"{RED}Folder name can't be empty!{RESET}")
        else:
            loop = False
    return file

# SEARCH
def search():
    srch = input(f"Search: ")
    if srch == "":
        print(f"Search can't be empty!{RESET}")
        search()
    else:
        pass
    
    result = input(f"Number of results[1]: ")
    if result == "":
        result = 1
    else:
        pass
    
    print(f"Searching for: {srch}")
    print(f"{UNDERLINE}{BOLD}Search results{RESET}\n{g_search(srch, int(result))}")

# MORSE
def morse():
    input_text = input("Enter text/Morse code: ")
    if input_text == "":
        print(f"{RED}Text can't be empty!{RESET}")
        morse()
    else:
        pass
    
    morse_instance = Morse()
    
    if "/" in input_text:
        decoded_text = morse_instance.decoder(input_text)
        print(f"Decoded Text: {decoded_text}")
    else:
        encoded_text = morse_instance.coder(input_text)
        print(f"Encoded Morse Code: {encoded_text + ' /'}")
        
def tp_tools():
    tools = f"""
\t{TITLE}

{BOLD}• Web Search {RESET}
    This tool will search Google for a query and display the results.
    you can specify the number of results to display.

{BOLD}• Morse Code/Decode {RESET}
    This tool will convert text to morse code and vice versa.
    It will automatically detect if the input is morse code or text.

{BOLD}• Files {RESET}
    This tool will create, delete, rename, move, list files and folders.

{BOLD}• Backend {RESET}
    This tool will help to run backend commands.

{BOLD}• Box {RESET}
    This tool will print a box with a message and a title with specified length.

{BOLD}• Colors {RESET}
    This tool will print text with different colors and styles.

{BOLD}• Options {RESET}
    This tool will display a menu with options and handle user input for navigation and selection.

{BOLD}• Password Generator {RESET}
    This tool will generate a random password with the specified length.

{BOLD}• Progress Bar {RESET}
    This tool will display a progress bar with a specified terminal length.

{BOLD}• Encryption Animation {RESET}
    This tool will display an encryption animation in the terminal with a specified word.

{BOLD}• Files {RESET}
    This tool will handle file creation, deletion, read, write and more.
    
{BOLD}• Source Code {RESET}
    View our source code at github. {BRIGHT_BLUE}https://github.com/rakeshkanna-rk/textPlay{RESET}
    Author: {MAGENTA}Rakesh Kanna S{reset}
"""

    print(tools)


def source_code():
    print(f"Source code at: {BRIGHT_BLUE}https://github.com/rakeshkanna-rk/textPlay{RESET}")
    try:
        webbrowser.open('https://github.com/rakeshkanna-rk/textPlay')
        print(f"{GREEN}Auto opening browser...{RESET}")
    except:
        print(f"{RED}Auto opening browser failed...{RESET}")