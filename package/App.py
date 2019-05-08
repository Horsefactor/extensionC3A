from tkinter import*
from tkinter import filedialog
from package.function import write
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
        self.sizeWindow = '560x300' if (560 < self.w and 300 < self.h) else "%dx%d+0+0" % (self.w, self.h)
        self.geometry(self.sizeWindow)
        self.resizable(0, 0)
        self.details = ''

        #Init file path
        self.configFile = 'config/config.txt'
        self.getTradAndDetailsPath()

    def getTradAndDetailsPath(self):
            file = open(self.configFile, 'r', encoding="utf-16-le")
            self.detailsAndErrPath = file.readline().rstrip('\n')
            self.tradFilePath = file.readline()
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
        self.majPath()

    def browse_file_details(self):
        f = filedialog.asksaveasfile(defaultextension=".txt")

        if f is None:
            return

        self.detailsAndErrPath=f.name
        self.majPath()

    def majPath(self):
        with open(self.configFile, 'w', encoding='utf-16-le') as file :
            file.write(self.detailsAndErrPath + '\n' + self.tradFilePath)

    def writeDetails(self, string):
        write(self.detailsAndErrPath,  string)

    def majTxt(self, frame_name):
        '''maj of a text frame'''
        self.frames[frame_name].text.config(state='normal')
        self.frames[frame_name].text.insert(END,self.details)
        self.frames[frame_name].text.config(state='disabled')