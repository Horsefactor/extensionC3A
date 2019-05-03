from tkinter import*
from os import path
from tkinter import filedialog

class Index(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.width = 300
        self.height = 300
        self.controller = controller
        self.initWidget()
        
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
                        disabledforeground = '#FF0000',
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

        self.controller.nomenclatureModifiedPath=f.name
        string ='To :  {}'.format(path.split(self.controller.nomenclatureModifiedPath)[1])
        self.button2.config(text=string)

        if self.controller.nomenclatureModifiedPath != '' and self.controller.nomenclatureFilePath != '':
            self.button3.config(state='normal')

    def browse_file_init(self):
        self.controller.nomenclatureFilePath = filedialog.askopenfilename(title="select file", 
                                                                          filetypes = (("text files", ".txt"),("all files", "*.*")))
        string ='From :  {}'.format(path.split(self.controller.nomenclatureFilePath)[1])
        self.button1.config(text=string)

        if self.controller.nomenclatureModifiedPath != '' and self.controller.nomenclatureFilePath != '':
            self.button3.config(state='normal')

    def run(self):
        self.controller.main()
        self.button3.config(text='Done',fg=self.controller.bg)

    def restart(self):
        self.button1.config(text='Ouvrir un fichier')
        self.button2.config(text='Enregistrer sous')
        self.button3.config(text='Run', state='disabled')
        self.nomenclatureFilePath = ''
        self.nomenclatureModifiedPath = ''

