__date__= '<15/05/2019>'
__author__ = 'Thibault Delvaux,             \
             <thibaultdelvaux@outlook.fr>,  \
             <0484381244>'

from tkinter import*
from tkinter import filedialog
from package.function import write
from package.Help import Help
from package.Descr import Descr
from package.MenuWindow import MenuWindow
from package.Index import Index
from package.Details import Details
from tkinter import messagebox
from os import path

class App(Tk):
    '''router of differents page with the same menu bar and some attributes'''
    def __init__(self, *args, **kwargs) :
        Tk.__init__(self, *args, **kwargs)
        self.initConfig()
        self.initFrames()
        MenuWindow(self)

        #Show First page
        self.show_frame('Index')

    def initConfig(self):
        '''App config'''
        self.bg = '#99B2DD'
        self.police = 'white'
        self.button = '#2060B1'
        self.details = ''
        self.title("Traduction cc")
        self.config(background = self.bg)
        self.iconbitmap('image/logoELLYPS.ico')
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.sizeWindow = '560x300' if (560 < self.w and 300 < self.h) else "%dx%d+0+0" % (self.w, self.h)
        self.geometry(self.sizeWindow)
        self.resizable(0, 0)

        #Init file path
        self.configFile = 'config/config.txt'
        self.details_And_Err_Path = ''
        self.getTradsPath()

    def getTradsPath(self):
        '''get config from config file'''
        file = open(self.configFile, 'r', encoding="utf-16-le")
        self.trad_hvac_File_Path = file.readline().rstrip('\n').lstrip('\ufeff')
        self.trad_san_File_Path = file.readline().rstrip('\n')
        self.trad_el_File_Path = file.readline()
        file.close()

    def initFrames(self):
        # The container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = Frame(self, bg=self.bg)
        self.container.pack(side ='top', expand=True, fill='both')
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (Index, Descr, Help, Details):
            frame =  F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame

            # Put all of the pages in the same location.
            # The one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        
        #adapt the title and windows size
        if page_name == 'Index':
            self.title("Traduction cc")
            self.geometry(self.sizeWindow)

        if page_name == 'Descr':
            self.title("Crédits auteur")
            self.geometry(self.sizeWindow)

        if page_name == 'Help':
            self.title("Information d'utilisation")
            self.geometry("%dx%d+0+0" % (self.w, self.h))

        if page_name == 'Details':
            self.title("Détails")
            self.geometry("%dx%d+0+0" % (self.w, self.h))

        frame.tkraise()

    def browse_file_trad_hvac(self):
        '''get input from user to know path of trad_hvac file'''
        try:
            self.trad_hvac_File_Path = filedialog.askopenfilename(title="select file",
                                                       filetypes = (("text files", ".txt"),("all files", "*.*")))
            self.majPath()

        except FileNotFoundError as e:
            messagebox.showinfo(e)
       
    def browse_file_trad_san(self):
        '''get input from user to know path of trad_san file'''
        try:
            self.trad_san_File_Path = filedialog.askopenfilename(title="select file",
                                                       filetypes = (("text files", ".txt"),("all files", "*.*")))
            self.majPath()

        except FileNotFoundError as e:
            messagebox.showinfo(e)

    def browse_file_trad_el(self):
        '''get input from user to know path of trad_el file'''
        try:
            self.trad_el_File_Path = filedialog.askopenfilename(title="select file",
                                                       filetypes = (("text files", ".txt"),("all files", "*.*")))
            self.majPath()

        except FileNotFoundError as e:
            messagebox.showinfo(e)

    def majPath(self):
        '''maj of different path to any file, maj of app's config'''
        with open(self.configFile, 'w', encoding='utf-16-le') as file :
            file.write(self.trad_hvac_File_Path+ '\n' + 
                       self.trad_san_File_Path+ '\n' + 
                       self.trad_el_File_Path)

    def writeDetails(self, string):
        '''write a string on the current details file'''
        write(self.details_And_Err_Path,  string)

    def majTxt(self, frame_name):
        '''maj of a text frame'''
        self.frames[frame_name].text.config(state='normal')
        self.frames[frame_name].text.delete('0.0',END)
        self.frames[frame_name].text.insert(END,self.details)
        self.frames[frame_name].text.config(state='disabled')