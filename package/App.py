from tkinter import*
from tkinter import filedialog
from package import function as fn
from package.Help import Help
from package.Descr import Descr
from package.MenuWindow import MenuWindow
from package.Index import Index
from package.Details import Details

class App(Tk):
    def __init__(self, *args, **kwargs) :
        Tk.__init__(self, *args, **kwargs)
        self.initConfig()
        self.initFrames()
        MenuWindow(self)

        #Show First page
        self.show_frame('Index')

    def initConfig(self):
        #App config
        self.bg = '#63CD9B'
        self.police = '#FBE332'
        self.button = '#0EA5F1'
        self.details = ''
        self.title("extensionC3A")
        self.config(background = self.bg)
        self.iconbitmap('image/logoELLYPS.ico')
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        if 560 > self.w or 300 > self.h : self.sizeWindow = "%dx%d+0+0" % (self.w, self.h)
        else : self.sizeWindow = '560x300'
        self.geometry(self.sizeWindow)
        self.resizable(0, 0)

        #Init file path
        self.nomenclatureFilePath = ''
        self.nomenclatureModifiedPath = ''
        self.tradFilePath = 'TXT/trad.txt'
        self.detailsAndErrPath = 'TXT/Details_and_errors.txt'

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

            # Put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        
        if page_name == 'Index':
            self.title("ExtensionC3A")
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

    def browse_file_trad(self):
        self.tradFilePath = filedialog.askopenfilename(title="select file", 
                                                       filetypes = (("text files", ".txt"),("all files", "*.*")))

    def main(self):
        self.details = ''

        #1. load tab from C3A txt file
        tabREVIT = fn.createTabFromRevit(self.nomenclatureFilePath)
        self.details += '1.\tVotre nomenclature a été importée pour modification.\n'

        #2. load tab for translating
        tabTRAD = fn.createTabFromTrad(self.tradFilePath)
        self.details += '2.\tLe tableau de traduction a été chargé.\n'

        #3. applying translating
        tabXLS, warningsElemMissing, warningsNoModif = fn.applyTradFile(tabREVIT, tabTRAD)
        self.details += '3.\tTout a été traduit.\r\n\r\n\t------------------------------------------------------------------------------------------\r\n\r\n'

        if warningsElemMissing != '':
            self.details += '/!\\ Attention les éléments suivant ont été marqués d\'un check obligatoire dans le fichier de traduction et sont manquant dans l\'export revit:\r\n\r\n'
            self.details += warningsElemMissing

        self.details+= '\r\n\r\n\t------------------------------------------------------------------------------------------\r\n\r\n'
        if warningsNoModif != '':
            self.details += '\r\n\r\n\r\n\r\n/!\\ Les éléments suivants n\'ont pas été modifiés par le fichier de traduction alors qu\'ils ont été exportés par revit.\nIl manque surement une ligne associée à cet élément dans le fichier de traduction :\r\n\r\n'
            self.details += warningsNoModif
    
        #4 re-write C3A file
        fn.writeTab(self.nomenclatureModifiedPath, tabXLS)

        #maj app
        self.frames['Details'].text.config(state='normal')
        self.frames['Details'].text.insert(END,self.details)
        self.frames['Details'].text.config(state='disabled')

    def writeDetails(self, string):
        fn.write(self.detailsAndErrPath,string)