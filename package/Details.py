__date__= '<15/05/2019>'
__author__ = 'Thibault Delvaux,             \
             <thibaultdelvaux@outlook.fr>,  \
             <0484381244>'

from tkinter import*

class Details(Frame):
    def __init__ (self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=controller.bg)
        self.initWidget()
    
    def initWidget(self):
        self.initFrame()
        self.initText()
        self.initButton()
        self.initScrollbar()

    def initText(self):

        #init title label
        self.label = Label(self, 
                           text="Details de l'opération\nChemin du fichier de détails:{}".format(self.controller.details_And_Err_Path),
                           font=("Helvetica",20,'bold'),
                           bg= self.controller.bg,
                           fg =self.controller.police)
        self.label.pack(side="top")

        #init main text
        self.text = Text(self.lower_frame,
                         font=("Calibri",15,'bold'),
                         state='disabled',
                         bg ='#F6F1FF',
                         fg ='#00163A',
                         wrap ='word')
        self.text.place(relwidth = 1, relheight=1)

    def initButton(self):
        #button to go back to the main menu
        self.button = Button(self.lower_frame, 
                             text="Aller à la page principale",
                             padx = 8,
                             pady = 8,
                             bd = 4,
                             font=("Helvetica",12,'bold'),
                             bg=self.controller.button,
                             fg=self.controller.police,
                             command=lambda: self.controller.show_frame("Index"))
        self.button.pack(fill = 'both',side=BOTTOM)

    def initFrame(self):
        '''frame for containing txt and button'''
        self.lower_frame = Frame(self, bg ='#81C1FF', bd = 10)
        self.lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.7, anchor='n')

    def initScrollbar(self):
        self.scrollbar = Scrollbar(self.lower_frame, command=self.text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)