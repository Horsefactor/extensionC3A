from tkinter import Menu

class MenuWindow:
    def __init__(self, controller):
        self.controller = controller
        self.initMenu()
        self.MenuTools()
        self.MenuHelp()

    def initMenu(self):
        self.menubar = Menu(self.controller)
        self.controller.config(menu=self.menubar)

    def MenuHelp(self):
        self.subMenu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Aide", 
                                 menu =self.subMenu2)
        self.subMenu2.add_command(label ="Info", 
                                  command=lambda: self.controller.show_frame('Help'))
        self.subMenu2.add_command(label ="Details et erreur", 
                                  command=lambda: self.controller.show_frame('Details'))
        self.subMenu2.add_command(label ="Credits", 
                                  command=lambda: self.controller.show_frame('Descr'))

    def MenuTools(self):
        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Outils",
                                 menu=self.subMenu)
        self.subMenu.add_command(label="Changer de fichier de traduction", 
                                 command = self.controller.browse_file_trad)
        self.subMenu.add_command(label="Exit", 
                                 command= self.controller.destroy)
        self.subMenu.add_command(label="Restart", 
                                 command=lambda: self.controller.frames['Index'].restart())