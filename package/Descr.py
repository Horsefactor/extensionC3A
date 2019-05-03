from tkinter import*

class Descr(Frame):
    def __init__ (self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=controller.bg)
        self.initWidget()

    def initWidget(self):
        self.initFrame()
        self.initLabel()
        self.initButton()

    def initLabel(self):
        self.label1 = Label(self, 
                            text="Information\nconcernant l'auteur de l'application :", 
                            font=("Helvetica",12,'bold'),
                            bg= self.controller.bg,
                            fg =self.controller.police)
        self.label1.pack(side="top", fill="x", pady=10)

        label2 = Text(self.lower_frame, 
                      font=("Helvetica",10,'bold'),
                      bg ='#FAFACE')
        label2.insert(END, 'Ce programme a été réalisé dans mon stage en tant qu\'étudiant \npour deveniringénieur informaticien.\
                            \r\n\r\nNom et prénom : Thibault Delvaux\
                            \nEmail : thibaultdelvaux@outlook.fr\
                            \nNuméro de GSM : +32 484 381 244 \
                            \r\n\r\nMention à l\'auteur de l\'image du menu principal : Kiranshastry')
        label2.place(relwidth = 1, relheight=1)
        label2.config(state='disabled')

    def initButton(self):
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
        self.lower_frame = Frame(self, bg ='#81C1FF', bd = 10)
        self.lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.7, anchor='n')
