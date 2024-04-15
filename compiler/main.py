from tkinter import *
import customtkinter
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
from tkcode import CodeEditor  # Import the CodeEditor class
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Token
from tkinter.scrolledtext import ScrolledText
from tkinter.scrolledtext import ScrolledText
import openai
import os
import autocomplete



root = customtkinter.CTk()
root.geometry("1920x1080")
customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("blue")


file_path = ''






def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*')])
    with open(path, 'r') as file:
        code = file.read()
        code_input.delete('1.0', END)
        code_input.insert('1.0', code)
        set_file_path(path)


def save_file():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = code_input.get('1.0', END)
        file.write(code)
        set_file_path(path)

def run_file():
    if file_path == '':
        CTkMessagebox(title="Error", message="Save your code", icon="cancel")
        return

    # Get user input from the text area
    user_input = user_input_text.get('1.0', 'end-1c')

    # Use subprocess to run the file with user input
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    
    # Provide user input to the subprocess
    output, error = process.communicate(input=user_input.encode())

    # Display the program output
    code_output.configure(state="normal")
    code_output.delete('1.0', END)
    code_output.insert('1.0', output.decode())
    code_output.insert('1.0', error.decode())
    code_output.configure(state="disabled")

    # Check if the program is waiting for user input
    if b"input" in output:
        # You can customize this prompt or use a separate input widget
        user_input = input("Enter your input: ")
        
        # Provide the updated user input to the subprocess
        process.stdin.write(user_input.encode())
        process.stdin.flush()

        # Get the updated output after providing input
        output, error = process.communicate()
        code_output.configure(state="normal")
        code_output.insert('1.0', output.decode())
        code_output.insert('1.0', error.decode())
        code_output.configure(state="disabled")

root.state("zoom")


# input - Use CodeEditor instead of CTkTextbox

code_input = CodeEditor(root, language='python', font="Consolas" , highlighter="dracula", width=89,height=41)
code_input.place(x=280, y=0)





# output
code_output = customtkinter.CTkTextbox(root, text_color="lightgreen" ,fg_color="black", width=420, height=360,state="normal")
code_output.place(x=860, y=0)

label_output=customtkinter.CTkLabel(root, text="Output view ------------------------------------", text_color="black", fg_color="lightgreen")
label_output.place(x=860, y=300)

# buttons
Open = PhotoImage(file="folder2-open.png")
Open = customtkinter.CTkButton(root, image=Open, text="Open", compound="left", command=open_file)
Open.place(x=20, y=30)

Save = PhotoImage(file="download (2).png")
Save = customtkinter.CTkButton(root, image=Save, text="Save", compound="left", command=save_file)
Save.place(x=20, y=70)

Run = PhotoImage(file="play-fill.png")
Run = customtkinter.CTkButton(root, image=Run, text="Run", compound="left", command=run_file)
Run.place(x=20, y=110)

user_input_text = customtkinter.CTkTextbox(root, width=420, height=300, fg_color="#878f99", text_color="black")
user_input_text.place(x=860, y=350)
label_input=customtkinter.CTkLabel(root, text="Input view ------------------------------------", text_color="black", fg_color="lightgreen")
label_input.place(x=860, y=595)


credit=customtkinter.CTkLabel(root, text="Made by Aditya Borkar", text_color="grey" )
credit.place(x=20,y=150)






root.mainloop()

