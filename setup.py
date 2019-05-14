from cx_Freeze import setup, Executable
import os.path
import sys
from getpass import getuser
from datetime import datetime
from tkinter import*
from tkinter import filedialog
from tkinter import messagebox
from os import path
from package.function import*
from re import findall, split

from package.App import App
from package.Exc import Error
from package.Help import Help
from package.Descr import Descr
from package.MenuWindow import MenuWindow
from package.Index import Index
from package.Details import Details

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            'image/logoELLyps.ico',
            'image/logoELLyps.png',
            'config/config.txt'
         ],
    },
}

setup(options = options,
      name='TraductionCC',
      version = '0.6',
      description="GUI for the software traductionCC wich provides a translating of a Revit file and manage data's",
      executables= [Executable("extensionC3A.py", base=base)])