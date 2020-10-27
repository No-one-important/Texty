import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import Tk, simpledialog
from tkinter import filedialog
import os
import subprocess
import webbrowser


python_path = 'python3'
python_repl = 'python3'
js_path = 'node'
js_repl = 'node'
ruby_path = 'ruby'
ruby_repl = 'irb'
C_path = 'gcc'
C_executable = './a.out'


# Defining TextEditor Class
class TextEditor:

    # Defining Constructor
    def __init__(self, window, font, size, text, file):
        self.fullScreenState = False
        self.locked = False

        # Assigning root
        self.root = window
        # Window Geometry
        self.root.geometry("700x500+200+150")
        # Initializing filename
        self.filename = None
        # Declaring Status variable
        self.status = StringVar()

        self.font = font
        self.size = size

        self.filename = file

        # Calling Settitle Function
        self.settitle()

        # Creating Status_bar
        self.status_bar = Label(self.root, textvariable=self.status, font=(font, size, "normal"), bd=2, relief=GROOVE)
        # Packing status bar to root window
        self.status_bar.pack(side=BOTTOM, fill=BOTH)
        # Initializing Status
        self.status.set("Welcome To Texty")

        # Creating Menu_bar
        self.menu_bar = Menu(self.root, font=(font, size, "normal"), activebackground="skyblue")
        # Configuring menu_bar on root window
        self.root.config(menu=self.menu_bar)

        # Creating File Menu
        self.file_menu = Menu(self.menu_bar, font=(font, size, "normal"), activebackground="skyblue", tearoff=0)
        # Adding New file Command
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.newfile)
        # Adding Open file Command
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.openfile)
        # Adding Save File Command
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.savefile)
        # Adding Save As file Command
        self.file_menu.add_command(label="Save As", accelerator="Ctrl+D", command=self.save_as_file)
        # adding reload file
        self.file_menu.add_command(label="Reload", accelerator="Ctrl+R", command=self.reload)
        # Adding Separator
        self.file_menu.add_separator()
        # Adding Exit window Command
        self.file_menu.add_command(label="Exit", accelerator="Ctrl+E", command=self.exit)

        # Cascading file_menu to menu_bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Creating Python Menu
        self.python_menu = Menu(self.menu_bar, font=(font, size, "normal"), activebackground="skyblue", tearoff=0)
        # adding run file
        self.python_menu.add_command(label="Run", accelerator="F12", command=self.run)
        # adding REPL
        self.python_menu.add_command(label="REPL", accelerator="F10", command=self.REPL)
        # adding open command prompt
        self.python_menu.add_command(label="Open command prompt", accelerator="F9", command=self.open_cmd)
        # Cascading Python_menu to menu_bar
        self.menu_bar.add_cascade(label="Code", menu=self.python_menu)

        # Creating Edit Menu
        self.edit_menu = Menu(self.menu_bar, font=(font, size, "normal"), activebackground="skyblue", tearoff=0)
        # Adding Cut text Command
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        # Adding Copy text Command
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        # Adding Paste text command
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
        # Adding search command
        self.edit_menu.add_command(label="Search", accelerator="Ctrl+B", command=self.search)
        # Adding dictionary command
        self.edit_menu.add_command(label="Dictionary", accelerator="Ctrl+Q", command=self.dictionary)
        # Adding lock command
        self.edit_menu.add_command(label="Lock", accelerator="Ctrl+L", command=self.lock)
        # Cascading editmenu to menubar
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Creating appearance Menu
        self.looks_menu = Menu(self.menu_bar, font=(font, size, "normal"), activebackground="skyblue", tearoff=0)
        # Adding font size Command
        self.looks_menu.add_command(label="Font Size", accelerator="Ctrl+Shift+F", command=self.font_size)
        # Adding font Command
        self.looks_menu.add_command(label="Font", accelerator="Ctrl+F", command=self.font_change)
        # Adding full_screen Command
        self.looks_menu.add_command(label="Full Screen", accelerator="F11", command=self.fullscreen)
        # Cascading appearance menu to menu_bar
        self.menu_bar.add_cascade(label="Appearance", menu=self.looks_menu)

        # Creating Help Menu
        self.help_menu = Menu(self.menu_bar, font=(font, size, "normal"), activebackground="skyblue", tearoff=0)
        # Adding About Command
        self.help_menu.add_command(label="About", command=self.infoabout)
        # Cascading help_menu to menu_bar
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Creating Scrollbar
        scrod_y = Scrollbar(self.root, orient=VERTICAL)
        # Creating Text Area
        self.txtarea = Text(self.root, yscrollcommand=scrod_y.set, font=(font, size, "normal"), state="normal", relief=GROOVE)
        # Packing scrollbar to root window
        scrod_y.pack(side=RIGHT, fill=Y)
        # Adding Scrollbar to text area
        scrod_y.config(command=self.txtarea.yview)
        # Packing Text Area to root window
        self.txtarea.pack(fill=BOTH, expand=1)

        if text:
            for x in text.split('\n'):
                self.txtarea.insert(END, x + '\n')


        # Calling shortcuts function
        self.shortcuts()

    # Defining settitle function
    def settitle(self):
        # Checking if Filename is not None
        if self.filename:
            # Updating Title as filename
            self.root.title('Texty - ' + self.filename.split('/')[-1])
        else:
            # Updating Title as Untitled
            self.root.title("Texty")

    # Defining New file Function
    def newfile(self, *args):
        # Clearing the Text Area
        self.txtarea.delete("1.0", END)
        # Updating filename as None
        self.filename = None
        # Calling settitle function
        self.settitle()
        # updating status
        self.status.set("New File Created")

    # Defining Open File Function
    def openfile(self, *args):
        # Exception handling
        try:
            # Asking for file to open
            self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", ('*.py', '*.pyw')),("Javascript Files", "*.js"),("Html Files", "*.html"), ("Ruby Files", "*.rb"), ("C files", "*.c")), parent=self.root)
            # checking if filename not none
            if self.filename:
                # opening file in readmode
                infile = open(self.filename, "r")
                # Clearing text area
                self.txtarea.delete("1.0", END)
                # Inserting data Line by line into text area
                for line in infile:
                    self.txtarea.insert(END, line)
                # Closing the file
                infile.close()
                # Calling Set title
                self.settitle()
                # Updating Status
                self.status.set("Opened Successfully")
        except Exception as e:
            messagebox.showerror("Exception", e, parent=self.root)

    # Defining Save File Function
    def savefile(self, *args):
        # Exception handling
        try:
            # checking if filename not none
            if self.filename:
                # Reading the data from text area
                data = self.txtarea.get("1.0", END)
                # opening File in write mode
                outfile = open(self.filename, "w")
                # Writing Data into file
                outfile.write(data)
                # Closing File
                outfile.close()
                # Calling Set title
                self.settitle()
                # Updating Status
                self.status.set("Saved Successfully")
            else:
                self.save_as_file()
        except Exception as e:
            messagebox.showerror("Exception", e, parent=self.root)

    # Defining Save As File function
    def save_as_file(self, *args):
        # Exception handling
        try:
            # Asking for file name and type to save
            untitled_file = filedialog.asksaveasfilename(title="Save file As", defaultextension=".py", initialfile="Untitled.py", filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("Javascript Files", "*.js"),("Html Files", "*.html"), ("Ruby Files", "*.rb"), ("C files", "*.c")), parent=self.root)
            # Reading the data from text area
            data = self.txtarea.get("1.0", END)
            # opening File in write mode
            outfile = open(untitled_file, "w")
            # Writing Data into file
            outfile.write(data)
            # Closing File
            outfile.close()
            # Updating filename as Untitled
            self.filename = untitled_file
            # Calling Set title
            self.settitle()
            # Updating Status
            self.status.set("Saved Successfully")
        except Exception as e:
            messagebox.showerror("Exception", e, parent=self.root)

    # Defining Exit function
    def exit(self, *args):
        op = messagebox.askyesno("WARNING", "Your Unsaved Data May be Lost!!")
        if op > 0:
            self.root.destroy()
        else:
            return

    # Defining Cut function
    def cut(self, *args):
        self.txtarea.event_generate("<<Cut>>")

    # Defining Copy function
    def copy(self, *args):
        self.txtarea.event_generate("<<Copy>>")

    # Defining Paste function
    def paste(self, *args):
        self.txtarea.event_generate("<<Paste>>")

    def run(self, *args):
        if self.filename.endswith('.js'):
            os.system(js_path + ' ' + self.filename)
        elif self.filename.endswith('.rb'):
            os.system(ruby_path + ' ' + self.filename)
        elif self.filename.endswith('.html'):
            webbrowser.open(self.filename)
        elif self.filename.endswith('.c'):
            os.system(C_path + ' ' + self.filename)
            os.system(C_executable)
            os.remove(C_executable)
        else:
            os.system(python_path + ' ' + self.filename)
        self.status.set('Run Successfully')


    
    def font_size(self, *args):
        self.size = int(simpledialog.askstring('Size', 'Enter a new font size (default 12):', parent=self.root))
        if self.filename:
            self.savefile()
        TextEditor(Tk(), self.font, self.size, self.txtarea.get('1.0', END), self.filename)
        self.root.destroy()

    def font_change(self, *args):
        self.font = simpledialog.askstring('Font', 'Enter a new font (default Microsoft Yi Baiti):', parent=self.root)
        if self.filename:
            self.savefile()
        TextEditor(Tk(), self.font, self.size, self.txtarea.get('1.0', END), self.filename)
        self.root.destroy()

    def dictionary (self, *args):
        webbrowser.open(f'https://dictionary.cambridge.org/search/english/?q={self.get_selected()}')

    def open_cmd(self, *args):
        os.system("bash")

    def REPL(self, *args):
        if self.filename.endswith('.js'):
            os.system(js_repl)
        elif self.filename.endswith('.rb'):
            os.system(ruby_repl)
        else:
            os.system(python_repl)

    def search (self, *args):
        webbrowser.open(f'https://www.bing.com/search?q={self.get_selected()}')

    def get_selected(self, *args):
        return self.txtarea.get(tk.SEL_FIRST, tk.SEL_LAST)

    def fullscreen(self, *args):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)

    def lock(self, *args):
        if not self.locked:
            self.txtarea.config(state='disabled')
            self.locked = not self.locked
        else:
            self.txtarea.config(state='normal')
            self.locked = not self.locked

    # Defining reload function
    def reload(self, *args):
        if messagebox.askyesno('Reload', 'You may lose changes\nDo you wish to proceed?'):
            # Exception handling
            try:
                # checking if filename not none
                if self.filename:
                    # Clearing Text Area
                    self.txtarea.delete("1.0", END)
                    # opening File in read mode
                    infile = open(self.filename, "r")
                    # Inserting data Line by line into text area
                    for line in infile:
                        self.txtarea.insert(END, line)
                    # Closing File
                    infile.close()
                    # Calling Set title
                    self.settitle()
                    # Updating Status
                    self.status.set("Reloaded Successfully")
                else:
                    # Clearing Text Area
                    self.txtarea.delete("1.0", END)
                    # Updating filename as None
                    self.filename = None
                    # Calling Set title
                    self.settitle()
                    # Updating Status
                    self.status.set("No File To Reload")
            except Exception as e:
                messagebox.showerror("Exception", e, parent=self.root)

    # Defining About function
    def infoabout(self):
        messagebox.showinfo( "About Text Editor", "A Simple Text Editor\nCreated using Python.", parent=self.root)

    # Defining shortcuts function
    def shortcuts(self):
        # Binding Ctrl+n to newfile function
        self.txtarea.bind("<Control-n>", self.newfile)
        # Binding Ctrl+o to openfile function
        self.txtarea.bind("<Control-o>", self.openfile)
        # Binding Ctrl+s to savefile function
        self.txtarea.bind("<Control-s>", self.savefile)
        # Binding Ctrl+d to saveasfile function
        self.txtarea.bind("<Control-d>", self.save_as_file)
        # Binding Ctrl+e to exit function
        self.txtarea.bind("<Control-e>", self.exit)
        # Binding Ctrl+x to cut function
        self.txtarea.bind("<Control-x>", self.cut)
        # Binding Ctrl+c to copy function
        self.txtarea.bind("<Control-c>", self.copy)
        # Binding Ctrl+v to paste function
        #      self.txtarea.bind("<Control-v>", self.paste)
        #  already set in windows resulted in double paste
        # Binding Ctrl+r to reload function
        self.txtarea.bind("<Control-r>", self.reload)
        # bind ctrl+b to run
        self.txtarea.bind('<Key-F12>', self.run)
        # bind ctrl+F to size
        self.txtarea.bind('<Control-F>', self.font_size)
        # bind ctrl+f to font
        self.txtarea.bind('<Control-f>', self.font_change)
        # bind f9 to command line
        self.txtarea.bind('<Key-F9>', self.open_cmd)
        # bind f10 to REPL
        self.txtarea.bind('<Key-F10>', self.REPL)
        # bind f11 to fullscreen
        self.txtarea.bind('<Key-F11>', self.fullscreen)
        # bind ctrl+b to search
        self.txtarea.bind('<Control-b>', self.search)
        # bind ctrl+q to dictionary
        self.txtarea.bind('<Control-q>', self.dictionary)
        # bind ctrl+l to lock
        self.txtarea.bind('<Control-l>', self.lock)



# Creating TK Container
root = Tk()
# Passing Root to TextEditor Class
editor = TextEditor(root, "microsoft YI Baiti", 12, '', None)

# Root Window Looping
root.mainloop()
