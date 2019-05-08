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
                                 menu =self.subMenu2,
                                 underline = 0)
        self.subMenu2.add_command(label ="Info",
                                  command=lambda: self.controller.show_frame('Help'),
                                  underline = 0)
        self.subMenu2.add_command(label ="Details et erreur", 
                                  command=lambda: self.controller.show_frame('Details'),
                                  underline = 0)
        self.subMenu2.add_command(label ="Credits",
                                  command=lambda: self.controller.show_frame('Descr'),
                                  underline = 0)

    def MenuTools(self):
        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Outils",
                                 menu=self.subMenu)
        self.subsubMenu = Menu(self.subMenu, tearoff=0)
        self.subMenu.add_cascade(label='Changer',
                                 menu=self.subsubMenu,
                                 underline = 0)
        self.subsubMenu.add_command(label='Fichier de traduction',
                                    command = self.controller.browse_file_trad)
        self.subsubMenu.add_command(label='Fichier de détails',
                                    command = self.controller.browse_file_details)
        self.subMenu.add_separator()
        self.subMenu.add_command(label="Exit",
                                 command= self.controller.destroy,
                                 underline = 0)
        self.subMenu.add_command(label="Restart",
                                 command=lambda: self.controller.frames['Index'].restart(),
                                 underline = 0)