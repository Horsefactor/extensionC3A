__date__= '<15/05/2019>'
__author__ = 'Thibault Delvaux,             \
             <thibaultdelvaux@outlook.fr>,  \
             <0484381244>'

from cx_Freeze import setup, Executable
import os.path
import sys

base = None

#To hide the terminal
if sys.platform == 'win32':
    base = 'Win32GUI'

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

#Include files
options = {
    'build_exe': {
        'include_files':[
            (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')),
            (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll')),
            'image/logoELLyps.ico',
            'image/logoELLyps.png',
            'config/config.txt'
         ],
        'include_msvcr' :True,
    },
}

#Setup of the executable
setup(
    options = options,
    name = 'TraductionCC',
    version = '0.6',
    author = 'Thibault Delvaux',
    author_email = 'thibaultdelvaux@outlook.fr',
    url = 'https://github.com/Horsefactor',
    description = "GUI for the software traductionCC wich provides a translating of a Revit file and manage data's",
    executables = [Executable("traductionCC.py", base=base)]
)