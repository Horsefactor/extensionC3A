__date__= '<15/05/2019>'
__author__ = 'Thibault Delvaux,             \
             <thibaultdelvaux@outlook.fr>,  \
             <0484381244>'

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from os import path
from package.function import createTabFromRevit, createTabFromTrad, applyTradFile, writeTab

class Index(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.width = 200
        self.height = 200
        self.controller = controller
        self.initWidget()

        #Init file path
        self.nomenclature_File_Path = ''
        self.nomenclature_Modified_Path = ''
        self.done = False

    def initCheckbox(self):
        #var which contain de state of checkbox
        self.state_hvac = IntVar()
        self.state_san = IntVar()
        self.state_el = IntVar()

        #checkbox to decide if you translate by hvac/san/el
        hvac = Checkbutton(self.bottom_left_frame,
                           bg=self.controller.bg,
                           padx = 3,
                           activebackground=self.controller.police,
                           font=("Helvetica",14,'bold'),
                           selectcolor = self.controller.button,
                           fg=self.controller.police,
                           text='HVAC',
                           variable=self.state_hvac)
        san = Checkbutton(self.bottom_left_frame,
                          bg=self.controller.bg,
                          padx = 3,
                          activebackground=self.controller.police,
                          font=("Helvetica",14,'bold'),
                          selectcolor = self.controller.button,
                          fg=self.controller.police,
                          text='SAN',
                          variable=self.state_san)
        el = Checkbutton(self.bottom_left_frame,
                         bg=self.controller.bg,
                         padx = 3,
                         activebackground=self.controller.police,
                         selectcolor = self.controller.button,
                         font=("Helvetica",14,'bold'),
                         fg=self.controller.police,
                         text='EL',
                         variable= self.state_el)

        san.pack(fill=X, side=LEFT)
        hvac.pack(fill=X, side=RIGHT)
        el.pack(fill=X)

    def initButton(self):
        #init buttons
        self.button1= Button(self.right_frame, 
                             text ="Ouvrir un fichier", 
                             padx = 8,
                             pady =8,
                             bd = 4,
                             bg=self.controller.button,
                             fg=self.controller.police,
                             font=("Helvetica",14,'bold'),
                             command = self.browse_file_init)
        self.button2= Button(self.right_frame, 
                             padx = 8,
                             pady =8,
                             bd = 4,
                             bg=self.controller.button,
                             fg=self.controller.police,
                             font=("Helvetica",14,'bold'),
                             text ="Enregistrer sous", 
                             command = self.save_file_final)
        self.button3= Button(self.right_frame, 
                             text ="Run", 
                             padx = 8,
                             pady =8,
                             bd = 4,
                             bg=self.controller.button,
                             fg=self.controller.police,
                             font=("Helvetica",14,'bold'),
                             state = 'disabled',
                             disabledforeground = '#850000',
                             command = self.main)
        self.button4= Button(self.right_frame, 
                             text ="Exit",
                             padx = 8,
                             pady =8,
                             bd = 4,
                             bg=self.controller.button,
                             fg=self.controller.police,
                             font=("Helvetica",14,'bold'),
                             command = self.controller.destroy)

        self.button1.pack(fill=X)
        self.button2.pack(fill=X)
        self.button3.pack(fill=X)
        self.button4.pack(fill=X, side=BOTTOM)

    def initFrame(self):
        '''structure of the page'''
        self.left_frame = Frame(self, width = 150, bg=self.controller.bg)
        self.bottom_left_frame = Frame(self.left_frame,width = 150,bg=self.controller.bg)
        self.top_left_frame = Frame(self.left_frame,width = 150,bg=self.controller.bg)
        self.right_frame = Frame(self,bg=self.controller.bg, padx=6,pady =6)

        self.left_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.right_frame.grid(row=0, column=1, sticky='nsew')
        self.top_left_frame.grid(row=0, column=0, sticky='nse')
        self.bottom_left_frame.grid(row=1, column=0, sticky='ew')
        
        Grid.rowconfigure(self, 0, weight=1)

        for x in (0,1):
            Grid.columnconfigure(self, x, weight=1)

    def initImage(self):
        '''init image in a canvas'''
        self.image = PhotoImage(file="image/logoELLYPS.png").zoom(20).subsample(32)
        self.canvas = Canvas(self.top_left_frame,
                             width= self.width,
                             height= self.height,
                             bg= self.controller.bg, 
                             bd=0,
                             highlightthickness=0)
        self.canvas.create_image(self.width/2, self.height/2, image=self.image)
        self.canvas.grid(row=0, column=0, sticky='nse')

    def initLabel(self):
        self.label_title = Label(self.right_frame,
                                 text ="Traduction cc",
                                 font=("Helvetica",20,'bold'),
                                 bg=self.controller.bg,
                                 fg =self.controller.police)
        self.label_title.pack()

    def initWidget(self):
        '''init all widget'''
        self.initFrame()
        self.initImage()
        self.initCheckbox()
        self.initLabel()
        self.initButton()

    def save_file_final(self):
        '''get output file from user'''
        f = filedialog.asksaveasfile(defaultextension=".txt")

        if f is None:
            return

        self.nomenclature_Modified_Path=f.name
        pathfinal = path.split(self.nomenclature_Modified_Path)
        string ='To :  {}'.format(pathfinal[1])
        self.button2.config(text=string)
        self.controller.details_And_Err_Path = pathfinal[0] + '/Details.txt'

        if self.nomenclature_Modified_Path != '' and self.nomenclature_File_Path != '':
            self.button3.config(state='normal')

    def browse_file_init(self):
        '''get input file from user'''
        try:
            self.nomenclature_File_Path = filedialog.askopenfilename(title="select file", 
                                                                              filetypes = (("text files", ".txt"),("all files", "*.*")))
            string ='From :  {}'.format(path.split(self.nomenclature_File_Path)[1])
            self.button1.config(text=string)
            self.loadRevitTab()

            if self.nomenclature_Modified_Path != '' and self.nomenclature_File_Path != '':
                self.button3.config(state='normal')

        except Exception as e:
            messagebox.showinfo(e)

    def main(self):
        '''main program, run all things'''
        self.load_trad_file()
        self.translate()

        if(self.done==True):
            self.button3.config(text='Done', state='disabled')

    def restart(self):
        '''re-init all except trad's files'''
        self.button1.config(text='Ouvrir un fichier')
        self.button2.config(text='Enregistrer sous')
        self.button3.config(text='Run', state='disabled')
        self.nomenclature_File_Path = ''
        self.nomenclature_Modified_Path = ''
        self.controller.details = ''
        self.done = False

    def loadRevitTab(self):
        '''load tab from C3A txt file'''
        self.tabREVIT = createTabFromRevit(self.nomenclature_File_Path)
        self.controller.details += '1.\tVotre nomenclature a été importée pour modification.\n'

    def load_trad_file(self):
        '''load in a trad array all trad file which are required'''
        if self.state_hvac.get():
            self.tabTRAD = createTabFromTrad(self.controller.trad_hvac_File_Path)[2:]

        if self.state_san.get():
            tab = createTabFromTrad(self.controller.trad_san_File_Path)[2:]

            try:
                self.tabTRAD += tab

            except AttributeError as e:
                self.tabTRAD = tab

        if self.state_el.get():
            tab = createTabFromTrad(self.controller.trad_el_File_Path)[2:]

            try:
                self.tabTRAD += tab

            except AttributeError as e:
                self.tabTRAD = tab

        self.controller.details += '2.\tLe(s) tableau de traduction a(ont) été chargé(s).\n'

    def translate(self):
        '''apply translating from trad file on the revit file'''
        try:
            tabXLS, warningsElemMissing, warningsNoModif = applyTradFile(self.tabREVIT, self.tabTRAD)
            self.controller.details += '3.\tTout a été traduit.\r\n\r\n\t------------------------------------------------------------------------------------------\r\n\r\n'
            
            if warningsElemMissing != '':
                self.controller.details += '/!\\ Attention les éléments suivant ont été marqués d\'un check obligatoire dans le fichier de traduction et sont manquant dans l\'export revit:\r\n\r\n'
                self.controller.details += warningsElemMissing

            self.controller.details+= '\r\n\r\n\t------------------------------------------------------------------------------------------\r\n\r\n'

            if warningsNoModif != '':
                self.controller.details += '\r\n\r\n\r\n\r\n/!\\ Les éléments suivants n\'ont pas été modifiés par le fichier de traduction alors qu\'ils ont été exportés par revit.\nIl manque surement une ligne associée à cet élément dans le fichier de traduction :\r\n\r\n'
                self.controller.details += warningsNoModif

            #re-write C3A file
            writeTab(self.nomenclature_Modified_Path, tabXLS)
            self.controller.majTxt('Details')
            self.done = True

        except AttributeError as e:
            messagebox.showinfo('Erreur !',
                                '''Vous devez selectionner au moins un fichier de traduction ci-dessous:\r\n\r\n-\tHVAC\n-\tEL\n-\tSAN''')