from tkinter import*

class MenuWindow:
    def __init__(self, controller):
        self.menubar = Menu(controller)
        controller.config(menu=self.menubar)
        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Outils",
                                 menu=self.subMenu)
        self.subMenu.add_command(label="Changer de fichier de traduction", 
                                 command = controller.browse_file_trad)
        self.subMenu.add_command(label="Exit", 
                                 command= controller.destroy)
        self.subMenu.add_command(label="Restart", 
                                 command=lambda: controller.frames['Index'].restart())

        self.subMenu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Aide", 
                                 menu =self.subMenu2)
        self.subMenu2.add_command(label ="Info", 
                                  command=lambda: controller.show_frame('Help'))
        self.subMenu2.add_command(label ="Details et erreur", 
                                  command=lambda: controller.show_frame('Details'))
        self.subMenu2.add_command(label ="Credits", 
                                  command=lambda: controller.show_frame('Descr'))

    def about_me(self):
        pass

    def info(self):
        pass