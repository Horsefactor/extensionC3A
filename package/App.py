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

        #config
        self.bg = '#63CD9B'
        self.police = '#FBE332'
        self.button = '#0EA5F1'
        self.details = ''
        self.title("extensionC3A")
        self.config(background = self.bg)
        self.iconbitmap('image/logoELLYPS.ico')
        self.geometry('560x300')
        self.resizable(0, 0)
        #init file path
        self.nomenclatureFilePath = ''
        self.nomenclatureModifiedPath = ''
        self.tradFilePath = 'TXT/trad.txt'
        self.detailsAndErrPath = 'TXT/Details_and_errors.txt'

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self, bg=self.bg)
        container.pack(side ='top', expand=YES, fill='both')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Index, Descr, Help, Details):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        MenuWindow(self)
        self.show_frame('Index')

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        
        if page_name == 'Index':
            self.title("extensionC3A")
            self.geometry('560x300')

        if page_name == 'Descr':
            self.title("Crédits auteur")
            self.geometry("560x300")

        if page_name == 'Help':
            self.title("Information d'utilisation")
            self.geometry("%dx%d+0+0" % (w, h))

        if page_name == 'Details':
            self.title("details")
            self.geometry("%dx%d+0+0" % (w, h))

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
            self.details += '/!\\ Attention les éléments suivant ont été marqué d\'un check obligatoire dans le fichier de traduction et sont manquant dans l\'export revit:\r\n\r\n'
            self.details += warningsElemMissing

        self.details+= '\r\n\r\n\t------------------------------------------------------------------------------------------\r\n\r\n'
        if warningsNoModif != '':
            self.details += '\r\n\r\n\r\n\r\n/!\\ Les éléments suivants n\'ont pas été modifié par le fichier de traduction alors qu\'ils ont été exporté par revit.\nIl manque surement une ligne associé à cet élément dans le fichier de traduction :\r\n\r\n'
            self.details += warningsNoModif
    
        #4 re-write C3A file
        fn.writeTab(self.nomenclatureModifiedPath, tabXLS)
        self.frames['Details'].text.config(state='normal')
        self.frames['Details'].text.insert(END,self.details)
        self.frames['Details'].text.config(state='disabled')

    def writeDetails(self, string):
        fn.write(self.detailsAndErrPath,string)