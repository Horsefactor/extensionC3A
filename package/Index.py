from tkinter import *
from tkinter import filedialog
from os import path
from package.function import createTabFromRevit, createTabFromTrad, applyTradFile, writeTab

class Index(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.width = 300
        self.height = 300
        self.controller = controller
        self.initWidget()

        #Init file path
        self.nomenclatureFilePath = ''
        self.nomenclatureModifiedPath = ''

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
        self.button1.pack(fill=X)

        self.button2= Button(self.right_frame, 
                        padx = 8,
                        pady =8,
                        bd = 4,
                        bg=self.controller.button,
                        fg=self.controller.police,
                        font=("Helvetica",14,'bold'),
                        text ="Enregistrer sous", 
                        command = self.save_file_final)
        self.button2.pack(fill=X)

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
                        command = self.run)
        self.button3.pack(fill=X)

        self.button4= Button(self.right_frame, 
                        text ="Exit",
                        padx = 8,
                        pady =8,
                        bd = 4,
                        bg=self.controller.button,
                        fg=self.controller.police,
                        font=("Helvetica",14,'bold'),
                        command = self.controller.destroy).pack(fill=X, side=BOTTOM)
    def initFrame(self):
        self.right_frame = Frame(self, 
                                 bg=self.controller.bg, 
                                 padx=6, 
                                 pady =6)
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        Grid.rowconfigure(self, 0, weight=1)

        for x in (0,1): 
            Grid.columnconfigure(self, x, weight=1)

    def initImage(self):
        #init image
        self.image = PhotoImage(file="image/factory.png").zoom(13).subsample(32)
        self.canvas = Canvas(self,
                             width= self.width,
                             height= self.height,
                             bg= self.controller.bg, 
                             bd=0,
                             highlightthickness=0)
        self.canvas.create_image(self.width/2, self.height/2, image=self.image)
        self.canvas.grid(row=0, column=0, sticky='nsew')

    def initLabel(self):
        self.label_title = Label(self.right_frame,
                                 text ="C3A EXTENSION",
                                 font=("Helvetica",20,'bold'),
                                 bg=self.controller.bg,
                                 fg =self.controller.police)
        self.label_title.pack()

    def initWidget(self):
        self.initFrame()
        self.initImage()
        self.initLabel()
        self.initButton()

    def save_file_final(self):
        f = filedialog.asksaveasfile(defaultextension=".txt")

        if f is None:
            return

        self.nomenclatureModifiedPath=f.name
        string ='To :  {}'.format(path.split(self.nomenclatureModifiedPath)[1])
        self.button2.config(text=string)

        if self.nomenclatureModifiedPath != '' and self.nomenclatureFilePath != '':
            self.button3.config(state='normal')

    def browse_file_init(self):
        self.nomenclatureFilePath = filedialog.askopenfilename(title="select file", 
                                                                          filetypes = (("text files", ".txt"),("all files", "*.*")))
        string ='From :  {}'.format(path.split(self.nomenclatureFilePath)[1])
        self.button1.config(text=string)
        self.loadRevitTab()

        if self.nomenclatureModifiedPath != '' and self.nomenclatureFilePath != '':
            self.button3.config(state='normal')

    def run(self):
        self.main()
        self.button3.config(text='Done', state='disabled')

    def restart(self):
        self.button1.config(text='Ouvrir un fichier')
        self.button2.config(text='Enregistrer sous')
        self.button3.config(text='Run', state='disabled')
        self.nomenclatureFilePath = ''
        self.nomenclatureModifiedPath = ''
        self.controller.details = ''

    def loadRevitTab(self):
        '''load tab from C3A txt file'''
        self.tabREVIT = createTabFromRevit(self.nomenclatureFilePath)
        self.controller.details += '1.\tVotre nomenclature a été importée pour modification.\n'

    def main(self):
        '''load tab for translating'''
        self.tabTRAD = createTabFromTrad(self.controller.tradFilePath)
        self.controller.details += '2.\tLe tableau de traduction a été chargé.\n'
        self.tabXLS, warningsElemMissing, warningsNoModif = applyTradFile(self.tabREVIT, self.tabTRAD)
        self.controller.details += '3.\tTout a été traduit.\r\n\r\n\t------------------------------------------------------------------------------------------\r\n\r\n'

        if warningsElemMissing != '':
            self.controller.details += '/!\\ Attention les éléments suivant ont été marqués d\'un check obligatoire dans le fichier de traduction et sont manquant dans l\'export revit:\r\n\r\n'
            self.controller.details += warningsElemMissing

        self.controller.details+= '\r\n\r\n\t------------------------------------------------------------------------------------------\r\n\r\n'

        if warningsNoModif != '':
            self.controller.details += '\r\n\r\n\r\n\r\n/!\\ Les éléments suivants n\'ont pas été modifiés par le fichier de traduction alors qu\'ils ont été exportés par revit.\nIl manque surement une ligne associée à cet élément dans le fichier de traduction :\r\n\r\n'
            self.controller.details += warningsNoModif
    
        #4 re-write C3A file
        writeTab(self.nomenclatureModifiedPath, self.tabXLS)
        self.controller.majTxt('Details')