from tkinter import*

class Help(Frame):
    def __init__ (self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=controller.bg)
        self.txt = string = '''Mode d'emploi de l'application Extension C3A :
                            \r\n\r\n1. Option principale:
                                \n\t1.1.Ouvrir le fichier .txt sortit de revit par C3A
	                            \n\t\tcelui-ci doit avoir les collones disposées comme ceci:
                                \n\t\tzone = 0\n\t\tnom = 1\n\t\tparam = 2\n\t\tquantité 1 = 3\n\t\tdimension 1 = 4\n\t\tquantité 2 = 5\n\t\tdimension 2 = 6  

                                \n\t1.2. optionnel : changer le fichier de traduction via le sous-menu outil.\n\tCelui-ci doit avoir voir les collones disposées comme ceci et séparées par une tabulation :
	                            \n\t\tcheckmark = 0 (1=check;0=non)\n\t\tnom cible = 1\n\t\tparamètre = 2\n\t\treférence article = 3\n\t\tdescription = 4\n\t\tformule = 5\n\t\tdim = 6 (0=pce;1=m;2=m²;3=m³)

                                \n\t1.3. Choisir le fichier de destination
                                \n\t1.4. Run le programme
                            \r\n\r\n2. Option supplémentaire :
                                \n\t2.1. sous-menu Outil:
	                            \n\t\t2.1.1.   Changer le fichier de traduction ou le fichier de détails\n\t\t2.1.2.	Recommencer le programme\n\t\t2..1.3.	Quitter le programme (ce qui valide la dernière version du fichier de détails

                                \n\t2.2  sous-menu aide :
	                            \n\t\t2.2.1	Page info (ici)\n\t\t2.2.2	Fichier détails, reprénant diverses éléments auxquels il faut faire attention. Ce n'est qu'une version temporaire la derniere version serra dans le fichier texte approprié\n\t\t2.2.3	Credits auteur

                            \r\n\r\n3.Sortie Revit comme ceci :
	                            \n\treférence article = 0\n\tdescription = 1\n\tquantité = 2\n\tdimension = 3\n\tcommentaire = 4\r\n\r\n\r\n\r\n\r\n\r\n
                            '''
        self.initWidget()

    def initWidget(self):
        self.initFrame()
        self.initLabel()
        self.initScrollbar()
        self.initButton()

    def initLabel(self):
        label = Label(self, 
                      text="Comment utiliser l'application:",
                      font=("Helvetica",20,'bold'),
                      bg= self.controller.bg,
                      fg =self.controller.police)
        label.pack(side="top", fill="x")

        self.text = Text(self.lower_frame, 
                         font=("Calibri",15,'bold'),
                         bg ='#F6F1FF',
                         fg ='#00163A')
        self.text.insert(END, self.txt)
        self.text.place(relwidth = 1, relheight=1)
        self.text.config(state='disabled')

    def initButton(self):
        button = Button(self.lower_frame,
                        text="Aller à la page principale",
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
    
    def initScrollbar(self):
        self.scrollbar = Scrollbar(self.lower_frame, command=self.text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)