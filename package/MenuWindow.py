__date__= '<15/05/2019>'
__author__ = 'Thibault Delvaux,             \
             <thibaultdelvaux@outlook.fr>,  \
             <0484381244>'

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
        self.change = Menu(self.subMenu, tearoff=0)
        self.trad_menu = Menu(self.change, tearoff=0)

        self.menubar.add_cascade(label="Outils",
                                 menu=self.subMenu)
        self.subMenu.add_cascade(label='Fichier de traduction',
                                 menu=self.change,
                                 underline = 0)
        self.subMenu.add_separator()
        self.subMenu.add_command(label="Exit",
                                 command= self.controller.destroy,
                                 underline = 0)
        self.subMenu.add_command(label="Restart",
                                 command=self.controller.frames['Index'].restart,
                                 underline = 0)

        self.change.add_command(label='HVAC',
                                command=self.controller.browse_file_trad_hvac,
                                underline = 0)
        self.change.add_separator()
        self.change.add_command(label='SAN',
                                command=self.controller.browse_file_trad_san,
                                underline = 0)
        self.change.add_separator()
        self.change.add_command(label='EL',
                                command=self.controller.browse_file_trad_el,
                                underline = 0)