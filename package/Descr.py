__date__= '<15/05/2019>'
__author__ = 'Thibault Delvaux,             \
             <thibaultdelvaux@outlook.fr>,  \
             <0484381244>'

from tkinter import*

class Descr(Frame):
    def __init__ (self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=controller.bg)
        self.initWidget()

    def initWidget(self):
        '''init all widget'''
        self.initFrame()
        self.initLabel()
        self.initButton()

    def initLabel(self):
        '''init label and text'''
        #label title
        self.label = Label(self, 
                            text="Information\nconcernant l'auteur de l'application :", 
                            font=("Helvetica",12,'bold'),
                            bg= self.controller.bg,
                            fg =self.controller.police)
        self.label.pack(side="top", fill="x", pady=10)
        #main text
        me = Text(self.lower_frame, 
                      font=("Calibri",13,'bold'),
                      bg ='#F6F1FF',
                      fg ='#00163A',
                      wrap ='word')
        me.insert(END, 'Ce programme a été réalisé dans mon stage en tant qu\'étudiant \npour devenir ingénieur informaticien.\
                            \r\n\r\nNom et prénom : Thibault Delvaux\
                            \nEmail : thibaultdelvaux@outlook.fr\
                            \nNuméro de GSM : +32 484 381 244')
        me.place(relwidth = 1, relheight=1)
        me.config(state='disabled')

    def initButton(self):
        #button to go back on the main page
        button = Button(self.lower_frame, 
                        text="Go to the start page",
                        padx = 8,
                        pady = 8,
                        bd = 4,
                        font=("Helvetica",12,'bold'),
                        bg=self.controller.button,
                        fg=self.controller.police,
                        command=lambda: self.controller.show_frame("Index"))
        button.pack(fill = 'both',side=BOTTOM)
        
    def initFrame(self):
        '''frame for containing txt and button'''
        self.lower_frame = Frame(self, bg ='#81C1FF', bd = 10)
        self.lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.7, anchor='n')